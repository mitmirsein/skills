#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""econ_gate.py — econ-redteam 결정론 게이트

용도:
  경제 레드팀 비평 패킷의 *형식*을 기계 판정한다. 원칙은 "코드는 형식의 판사,
  에이전트는 실질의 판사"다. 코드는 존재/부재·grounding·enum·커버리지만 차단하고,
  지적이 참인가·반론이 최강인가·대상이 그것을 대면했는가는 판정 슬롯(UNJUDGED)에
  남겨 에이전트/HITL이 증거에서 채운다. 코드는 의미 진리를 자동 선언하지 않는다.

  grounding은 대상 문서의 *산문*에만 작동한다. 마크다운 표 행과 코드 블록은 제거한
  뒤 대조하므로, 회귀표의 숫자 셀을 인용하면 ungrounded로 차단된다(omni ARCHITECTURE
  범위 경계: omni는 결과 검증기가 아니라 논증 분석기다).

의존성: Python 3.9+ stdlib only. 외부 패키지·API 키·네트워크 없음.

실행법:
  python3 scripts/econ_gate.py classify --target doc.md
  python3 scripts/econ_gate.py check --critiques packet.json --target doc.md \
      [--paragraphs paragraphs.json] [--report out.md] \
      [--fail-on-schema] [--fail-on-ungrounded] [--fail-on-missing-axis] [--fail-on-mode-unset]
  python3 scripts/econ_gate.py prepare --critiques packet.json --out worklist.json
  python3 scripts/econ_gate.py decide --worklist worklist.json [--report out.md] \
      [--fail-on-strawman] [--fail-on-unengaged] [--fail-on-flattened]
  python3 scripts/econ_gate.py sync [--check]

종료 코드: 0 통과/자문 · 1 스크립트 내부 오류(sync drift 포함) · 2 입력 오류 또는 hard 게이트 실패.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

# 종료 코드 — theological_research/scripts/common_io.py 와 동일 의미론.
# 스킬 캡슐화(단독 배포) 원칙상 import 하지 않고 로컬 사본을 유지한다.
EXIT_OK = 0
EXIT_SCRIPT_ERROR = 1
EXIT_INPUT_OR_GATE = 2

SKILL_DIR = Path(__file__).resolve().parents[1]
MIRROR_RELPATH = ("projects", "omni-academic-framework", "skills", "econ-redteam")
SYNC_FILES = ("SKILL.md", "CANONICAL_NOTICE.md")
SYNC_DIRS = ("references", "scripts", "evals")

MODES = ("ex-ante", "ex-post", "mixed")
ATTACK_SECTIONS = ("Leap-Alert", "Evidence-Check", "Concept-Tension")
DIRECTIVE_SECTION = "Policy-Directives"
SEVERITIES = ("blocking", "major", "minor")
EX_ANTE_AXES = ("A1", "A2", "A3", "A4", "A5")
EX_POST_AXES = ("E1", "E2", "E3")
ENGAGED = ("UNJUDGED", "대면", "미대면", "무관")
IS_STRONGEST = ("UNJUDGED", "true", "false")
VERDICTS = ("UNJUDGED", "valid", "strawman", "moot")
APORIA_VERDICTS = ("UNJUDGED", "보존", "평탄화", "의도된 종합")

REQUIRED_AXES = {
    "ex-ante": set(EX_ANTE_AXES),
    "ex-post": set(EX_POST_AXES),
    "mixed": set(EX_ANTE_AXES) | set(EX_POST_AXES),
}
AXIS_PART = {"A": "proposal", "E": "empirical"}

_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
_TABLE_ROW_RE = re.compile(r"^\s*\|")
_WS_RE = re.compile(r"\s+")


# ── 입출력 ────────────────────────────────────────────────────────────────
def _die_input(msg: str):
    print(f"[입력 오류] {msg}", file=sys.stderr)
    sys.exit(EXIT_INPUT_OR_GATE)


def load_json(path: str, label: str):
    p = Path(path)
    if not p.is_file():
        _die_input(f"{label} 경로 없음: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        _die_input(f"{label} 파싱 실패({path}): {exc}")


def read_text(path: str, label: str) -> str:
    p = Path(path)
    if not p.is_file():
        _die_input(f"{label} 경로 없음: {path}")
    try:
        return p.read_text(encoding="utf-8")
    except OSError as exc:
        _die_input(f"{label} 읽기 실패({path}): {exc}")


def dump_json(obj, path: str):
    p = Path(path)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def write_report(lines, path):
    if path:
        Path(path).write_text("\n".join(lines), encoding="utf-8")
        print(f"💾 리포트: {path}")


# ── 정규화·산문 추출 ──────────────────────────────────────────────────────
def prose_of(text: str) -> str:
    """마크다운 표 행과 펜스 코드 블록을 제거해 *산문*만 남긴다.

    회귀표의 숫자 셀은 grounding 대상이 아니다(범위 경계). 계수를 공격하려면
    그 계수를 해석하는 산문 문장을 인용해야 한다.
    """
    out, in_fence = [], False
    for line in text.splitlines():
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or _TABLE_ROW_RE.match(line):
            continue
        out.append(line)
    return "\n".join(out)


def norm(s) -> str:
    return _WS_RE.sub(" ", unicodedata.normalize("NFKC", str(s or ""))).strip()


def load_paragraphs(path: str):
    """omni paragraphs.json({"P_0001": "본문", ...})을 *소비*한다. 문단번호를 재발명하지 않는다."""
    raw = load_json(path, "paragraphs")
    if isinstance(raw, dict) and isinstance(raw.get("paragraphs"), dict):
        raw = raw["paragraphs"]
    if not isinstance(raw, dict):
        _die_input("paragraphs.json 형식 불명 — {\"P_0001\": \"본문\"} 평면 매핑이어야 함")
    return {str(k): norm(prose_of(str(v))) for k, v in raw.items()}


# ── classify ─────────────────────────────────────────────────────────────
EXPOST_TERMS = (
    "regression", "coefficient", "estimate", "standard error", "confidence interval",
    "difference-in-differences", "instrumental variable", "regression discontinuity",
    "event study", "p-value", "we find", "we estimate", "did", "iv", "rdd", "rct",
    "회귀", "계수", "추정치", "표준오차", "신뢰구간", "이중차분", "도구변수",
    "단절회귀", "처치효과", "표본", "유의수준", "평행추세",
)
EXANTE_TERMS = (
    "proposal", "proposed", "bill", "budget", "appropriation", "regulation",
    "will be implemented", "expected to", "projected", "forecast", "enact",
    "법안", "예산안", "규제안", "도입", "시행", "추진", "전망", "추계",
    "예상효과", "소요재원", "목표치", "제안한다", "신설",
)


def _count(text_low: str, terms) -> dict:
    hits = {}
    for t in terms:
        pat = rf"\b{re.escape(t)}\b" if t.isascii() else re.escape(t)
        n = len(re.findall(pat, text_low))
        if n:
            hits[t] = n
    return hits


def cmd_classify(args):
    low = norm(prose_of(read_text(args.target, "대상 문서"))).lower()
    post, ante = _count(low, EXPOST_TERMS), _count(low, EXANTE_TERMS)
    sp, sa = sum(post.values()), sum(ante.values())
    print(f"📊 어휘 tally — ex-post {sp} / ex-ante {sa}")
    for label, hits in (("ex-post", post), ("ex-ante", ante)):
        top = sorted(hits.items(), key=lambda kv: -kv[1])[:6]
        print(f"  {label}: " + (", ".join(f"{k}×{v}" for k, v in top) or "없음"))
    if sp and sa and min(sp, sa) >= max(sp, sa) * 0.4:
        lean = "mixed 가능성"
    elif sp > sa:
        lean = "ex-post 쪽"
    elif sa > sp:
        lean = "ex-ante 쪽"
    else:
        lean = "판단 근거 부족"
    print(f"🧭 자문 신호: {lean}. **판별은 코드가 아니라 에이전트가 선언한다** — "
          f"실현 outcome 데이터에 묶인 인과 추정의 유무가 기준이다.")
    sys.exit(EXIT_OK)


# ── check ────────────────────────────────────────────────────────────────
def _nonempty(v) -> bool:
    return bool(str(v or "").strip())


def _slot(v) -> str:
    return str(v).strip() if v is not None else "UNJUDGED"


def _strongest(v) -> str:
    """is_strongest는 JSON bool·문자열 어느 쪽으로도 올 수 있다. UNJUDGED는 대소문자 보존."""
    s = _slot(v)
    return "UNJUDGED" if s.upper() == "UNJUDGED" else s.lower()


def cmd_check(args):
    packet = load_json(args.critiques, "비평 패킷")
    if not isinstance(packet, dict):
        _die_input("비평 패킷은 최상위 객체여야 함")
    prose = norm(prose_of(read_text(args.target, "대상 문서")))
    paragraphs = load_paragraphs(args.paragraphs) if args.paragraphs else None

    schema, ungrounded, warnings = [], [], []

    mode = str(packet.get("mode") or "").strip()
    mode_unset = not mode
    if mode and mode not in MODES:
        schema.append(f"mode 값 비표준: '{mode}' (허용 {MODES})")
        mode = ""

    critiques = packet.get("critiques")
    if not isinstance(critiques, list) or not critiques:
        schema.append("critiques[]가 비어 있거나 리스트가 아님")
        critiques = []

    attacks, directives, seen_ids, seen_quotes = [], [], set(), {}
    for i, c in enumerate(critiques):
        if not isinstance(c, dict):
            schema.append(f"critiques[{i}]가 객체가 아님")
            continue
        cid = str(c.get("id") or "").strip() or f"<critiques[{i}] id 없음>"
        if not _nonempty(c.get("id")):
            schema.append(f"critiques[{i}] id 없음")
        elif cid in seen_ids:
            schema.append(f"{cid} id 중복")
        seen_ids.add(cid)

        section = str(c.get("section") or "").strip()
        if section == DIRECTIVE_SECTION:
            directives.append((cid, c))
            continue
        if section not in ATTACK_SECTIONS:
            schema.append(f"{cid} section 비표준: '{section}'")
            continue
        attacks.append((cid, c))

        axis = str(c.get("axis") or "").strip()
        allowed = REQUIRED_AXES.get(mode, set(EX_ANTE_AXES) | set(EX_POST_AXES))
        if axis not in allowed:
            other = set(EX_ANTE_AXES) | set(EX_POST_AXES)
            if mode and axis in other:
                schema.append(f"{cid} 범주 오류: mode={mode}인데 axis={axis} (gotcha ⑧)")
            else:
                schema.append(f"{cid} axis 비표준: '{axis}'")
            axis = ""

        if str(c.get("severity") or "").strip() not in SEVERITIES:
            schema.append(f"{cid} severity 비표준: '{c.get('severity')}'")

        for field in ("critique", "steelman", "falsification_condition"):
            if not _nonempty(c.get(field)):
                schema.append(f"{cid} {field} 비어 있음")
        if _nonempty(c.get("steelman")) and norm(c.get("steelman")) == norm(c.get("critique")):
            schema.append(f"{cid} steelman이 critique와 동일 — 최강 버전을 세우지 않았음 (gotcha ⑤)")

        if mode == "mixed" and axis:
            expect = AXIS_PART[axis[0]]
            if str(c.get("part") or "").strip() != expect:
                schema.append(f"{cid} mixed 모드: axis={axis}는 part='{expect}'여야 함")

        for field, enum in (("engaged_by_target", ENGAGED), ("verdict", VERDICTS)):
            if _slot(c.get(field)) not in enum:
                schema.append(f"{cid} {field} 비표준: '{c.get(field)}'")
        if _strongest(c.get("is_strongest")) not in IS_STRONGEST:
            schema.append(f"{cid} is_strongest 비표준: '{c.get('is_strongest')}'")

        quote = c.get("source_quote")
        if not _nonempty(quote):
            schema.append(f"{cid} source_quote 비어 있음 — 유령 비판")
        else:
            nq = norm(quote)
            if nq in seen_quotes:
                warnings.append(f"{cid} source_quote 재사용 (앵커 중복, {seen_quotes[nq]}와 동일)")
            seen_quotes.setdefault(nq, cid)
            if nq not in prose:
                ungrounded.append(f"{cid} source_quote가 대상 산문에 없음 (표 셀·코드 블록은 산문 아님)")
            elif paragraphs is not None:
                pid = str(c.get("paragraph_id") or "").strip()
                if not pid:
                    ungrounded.append(f"{cid} paragraph_id 없음 (--paragraphs 제공 시 필수)")
                elif pid not in paragraphs:
                    ungrounded.append(f"{cid} paragraph_id '{pid}' 실존하지 않음")
                elif nq not in paragraphs[pid]:
                    ungrounded.append(f"{cid} source_quote가 {pid} 문단 안에 없음")

    attack_ids = {cid for cid, _ in attacks}
    for cid, d in directives:
        refs = d.get("refs")
        if not isinstance(refs, list) or not refs:
            schema.append(f"{cid} Policy-Directives에 refs 없음 — 처방은 지적을 참조해야 함 (gotcha ⑦)")
            continue
        for r in refs:
            if str(r) not in attack_ids:
                schema.append(f"{cid} refs '{r}'가 존재하지 않는 critique.id")
        if not _nonempty(d.get("critique")):
            schema.append(f"{cid} directive 본문 비어 있음")

    aporia = packet.get("aporia") or []
    if not isinstance(aporia, list):
        schema.append("aporia[]가 리스트가 아님")
        aporia = []
    linked = set()
    for i, a in enumerate(aporia):
        if not isinstance(a, dict):
            schema.append(f"aporia[{i}]가 객체가 아님")
            continue
        if not _nonempty(a.get("name")):
            schema.append(f"aporia[{i}] name 비어 있음")
        poles = a.get("poles")
        if not isinstance(poles, list) or len(poles) < 2:
            schema.append(f"aporia[{i}] poles가 2개 미만 — 긴장에는 두 극이 필요")
        if _slot(a.get("verdict")) not in APORIA_VERDICTS:
            schema.append(f"aporia[{i}] verdict 비표준: '{a.get('verdict')}'")
        if _nonempty(a.get("critique_id")):
            linked.add(str(a["critique_id"]).strip())
    for cid, c in attacks:
        if str(c.get("section") or "") == "Concept-Tension" and cid not in linked:
            warnings.append(f"{cid} Concept-Tension인데 대응하는 aporia 항목 없음 (평탄화 위험)")

    covered = {str(c.get("axis") or "").strip() for _, c in attacks}
    required = REQUIRED_AXES.get(mode, set())
    missing = sorted(required - covered) if mode else []

    lines = ["# 📈 econ-redteam check — 형식·정박·커버리지", "",
             f"- 대상: `{args.target}` | 모드: **{mode or '(미선언)'}**",
             f"- 공격 지적 {len(attacks)}건 · 처방 {len(directives)}건 · 아포리아 {len(aporia)}건", ""]
    for title, items in (("스키마·범주 오류", schema), ("Grounding 실패", ungrounded)):
        lines.append(f"## {title} ({len(items)})")
        lines += [f"- ❌ {m}" for m in items] or ["- 없음"]
        lines.append("")
    lines.append(f"## 축 커버리지 — 누락 {len(missing)}")
    lines.append("- " + (", ".join(f"❌ {m}" for m in missing) if missing
                         else f"✅ 전 축 커버 ({', '.join(sorted(covered)) or '—'})"))
    lines += ["", f"## 경고 ({len(warnings)})"] + ([f"- ⚠️ {m}" for m in warnings] or ["- 없음"])
    write_report(lines, args.report)

    print(f"📈 check — 스키마 {len(schema)} / ungrounded {len(ungrounded)} / "
          f"누락 축 {len(missing)} / 경고 {len(warnings)}"
          + (" / mode 미선언" if mode_unset else ""))
    for m in schema + ungrounded:
        print(f"  ❌ {m}", file=sys.stderr)
    for m in warnings:
        print(f"  ⚠️ {m}", file=sys.stderr)

    fail = ((mode_unset and args.fail_on_mode_unset)
            or (schema and args.fail_on_schema)
            or (ungrounded and args.fail_on_ungrounded)
            or (missing and args.fail_on_missing_axis))
    sys.exit(EXIT_INPUT_OR_GATE if fail else EXIT_OK)


# ── prepare / decide ─────────────────────────────────────────────────────
INSTRUCTION = (
    "각 항목은 *판정 패킷*이다(코드 판정 아님). source_quote(글자 그대로의 앵커)와 steelman을 읽고: "
    "① is_strongest — 이 지점의 *가장 강한* 반론이면 true. "
    "② engaged_by_target — 대상이 그 반론을 대면했으면 '대면', 안 했으면 '미대면', 무관하면 '무관'. "
    "③ verdict — 'valid' | 'strawman'(약한 버전을 때렸다) | 'moot'(쟁점이 아니다). "
    "aporia[].verdict는 '보존' | '평탄화' | '의도된 종합'. "
    "최강 반론이 '미대면'이면 대상이 그 공격을 피해 간 것이고, verdict가 'strawman'이면 레드팀이 실패한 것이다. "
    "채운 뒤 econ_gate.py decide로 집계한다."
)


def cmd_prepare(args):
    packet = load_json(args.critiques, "비평 패킷")
    items = []
    for c in packet.get("critiques") or []:
        if not isinstance(c, dict) or str(c.get("section") or "") == DIRECTIVE_SECTION:
            continue
        items.append({
            "id": c.get("id"), "section": c.get("section"), "axis": c.get("axis"),
            "part": c.get("part"), "severity": c.get("severity"),
            "paragraph_id": c.get("paragraph_id"), "source_quote": c.get("source_quote"),
            "critique": c.get("critique"), "steelman": c.get("steelman"),
            "falsification_condition": c.get("falsification_condition"),
            "is_strongest": _strongest(c.get("is_strongest")),
            "engaged_by_target": _slot(c.get("engaged_by_target")),
            "verdict": _slot(c.get("verdict")),
            "needs_judgment": True,
        })
    aporia = [{**a, "verdict": _slot(a.get("verdict"))}
              for a in (packet.get("aporia") or []) if isinstance(a, dict)]
    worklist = {"schema_version": 1, "mode": packet.get("mode"),
                "target_ref": packet.get("target_ref"),
                "total_items": len(items), "instruction": INSTRUCTION,
                "items": items, "aporia": aporia}
    dump_json(worklist, args.out)
    print(f"🛡️ 판정 패킷 생성: {args.out} — 공격 지적 {len(items)}건, 아포리아 {len(aporia)}건. "
          f"is_strongest·engaged_by_target·verdict는 코드가 채우지 않는다.")
    sys.exit(EXIT_OK)


def cmd_decide(args):
    wl = load_json(args.worklist, "worklist")
    items = wl.get("items") or []
    aporia = wl.get("aporia") or []

    for it in items:
        for field, enum in (("engaged_by_target", ENGAGED), ("verdict", VERDICTS)):
            if _slot(it.get(field)) not in enum:
                _die_input(f"{it.get('id')} {field} 비표준: '{it.get(field)}' (허용 {enum})")
        if _strongest(it.get("is_strongest")) not in IS_STRONGEST:
            _die_input(f"{it.get('id')} is_strongest 비표준: '{it.get('is_strongest')}'")
    for a in aporia:
        if _slot(a.get("verdict")) not in APORIA_VERDICTS:
            _die_input(f"aporia '{a.get('name')}' verdict 비표준: '{a.get('verdict')}'")

    strawman = [i for i in items if _slot(i.get("verdict")) == "strawman"]
    unengaged = [i for i in items
                 if _strongest(i.get("is_strongest")) == "true"
                 and _slot(i.get("engaged_by_target")) == "미대면"]
    flattened = [a for a in aporia if _slot(a.get("verdict")) == "평탄화"]
    unjudged = [i for i in items if _slot(i.get("verdict")) == "UNJUDGED"]

    lines = ["# 🛡️ econ-redteam decide — 실질 판정 집계", "",
             f"- 공격 지적 {len(items)}건 | 허수아비 {len(strawman)} / "
             f"최강 반론 미대면 {len(unengaged)} / 미판정 {len(unjudged)}",
             f"- 아포리아 {len(aporia)}건 | 평탄화 {len(flattened)}", "",
             "## 허수아비 (레드팀 실패 — 약한 버전을 때렸다)"]
    lines += [f"- ❌ {i.get('id')} [{i.get('axis')}] {str(i.get('critique'))[:80]}"
              for i in strawman] or ["- 없음"]
    lines += ["", "## 최강 반론 미대면 (대상이 이 공격을 피해 갔다)"]
    lines += [f"- ❗ {i.get('id')} [{i.get('axis')}] \"{str(i.get('source_quote'))[:70]}\""
              for i in unengaged] or ["- 없음"]
    lines += ["", "## 평탄화된 아포리아 (긴장을 단일 결론으로 뭉갰다)"]
    lines += [f"- ❌ {a.get('name')}" for a in flattened] or ["- 없음"]
    lines += ["", "## 미판정 (판정 슬롯 미기입)"]
    lines += [f"- {i.get('id')}" for i in unjudged] or ["- 없음"]
    write_report(lines, args.report)

    print(f"🛡️ decide — 허수아비 {len(strawman)} / 미대면 {len(unengaged)} / "
          f"평탄화 {len(flattened)} / 미판정 {len(unjudged)}")
    for i in strawman:
        print(f"  ❌ {i.get('id')}: 허수아비 공격", file=sys.stderr)
    for i in unengaged:
        print(f"  ❗ {i.get('id')}: 최강 반론 미대면", file=sys.stderr)
    for a in flattened:
        print(f"  ❌ 아포리아 '{a.get('name')}' 평탄화", file=sys.stderr)

    fail = ((strawman and args.fail_on_strawman)
            or (unengaged and args.fail_on_unengaged)
            or (flattened and args.fail_on_flattened))
    sys.exit(EXIT_INPUT_OR_GATE if fail else EXIT_OK)


# ── sync ─────────────────────────────────────────────────────────────────
def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sync_items(root: Path):
    """정본↔미러 대조 대상의 상대경로 목록. tests/는 정본 전용이라 제외."""
    rels = [Path(f) for f in SYNC_FILES if (root / f).is_file()]
    for d in SYNC_DIRS:
        base = root / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
                rels.append(p.relative_to(root))
    return rels


def resolve_mirror():
    skills_root = SKILL_DIR.parent
    if skills_root.name != ".skills":
        return None
    return skills_root.parent.joinpath(*MIRROR_RELPATH)


def cmd_sync(args):
    mirror = resolve_mirror()
    if mirror is None:
        print("ℹ️ 정본(.skills/econ-redteam)이 아닌 위치에서 실행됨 — sync는 정본에서만 수행한다. skip.")
        sys.exit(EXIT_OK)
    if not mirror.is_dir():
        print(f"ℹ️ 미러 없음({mirror}) — 단독 배포로 간주. skip.")
        sys.exit(EXIT_OK)

    canon_rels = sync_items(SKILL_DIR)
    mirror_rels = set(sync_items(mirror))
    drift, copied = [], 0

    for rel in canon_rels:
        src, dst = SKILL_DIR / rel, mirror / rel
        if not dst.is_file():
            drift.append(f"미러 누락: {rel}")
        elif _sha256(src) != _sha256(dst):
            drift.append(f"내용 불일치: {rel}")
        if not args.check:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
    for rel in sorted(mirror_rels - set(canon_rels)):
        drift.append(f"미러 전용 잔여 파일: {rel}")

    if args.check:
        if drift:
            print("❌ drift 발견 (정본과 불일치):")
            for d in drift:
                print(f"  - {d}")
            print("   → 정본에서 고친 뒤 `econ_gate.py sync`로 전파하라.")
            sys.exit(EXIT_SCRIPT_ERROR)
        print(f"✅ 정본↔미러 동일 ({len(canon_rels)}개 파일)")
        sys.exit(EXIT_OK)

    print(f"✅ 미러 전파 완료: {copied}개 파일 → {mirror}")
    if mirror_rels - set(canon_rels):
        print("⚠️ 미러 전용 잔여 파일이 있다(수동 확인):")
        for rel in sorted(mirror_rels - set(canon_rels)):
            print(f"  - {rel}")
    sys.exit(EXIT_OK)


# ── CLI ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="econ-redteam 결정론 게이트 (형식의 판사)")
    sub = ap.add_subparsers(dest="command", required=True)

    c = sub.add_parser("classify", help="ex-ante/ex-post 어휘 tally 자문 (항상 exit 0)")
    c.add_argument("--target", required=True)
    c.set_defaults(func=cmd_classify)

    k = sub.add_parser("check", help="형식·grounding·커버리지 결정론 게이트")
    k.add_argument("--critiques", required=True)
    k.add_argument("--target", required=True)
    k.add_argument("--paragraphs", help="omni paragraphs.json (있으면 paragraph_id 실존까지 검증)")
    k.add_argument("--report")
    k.add_argument("--fail-on-schema", action="store_true")
    k.add_argument("--fail-on-ungrounded", action="store_true")
    k.add_argument("--fail-on-missing-axis", action="store_true")
    k.add_argument("--fail-on-mode-unset", action="store_true")
    k.set_defaults(func=cmd_check)

    p = sub.add_parser("prepare", help="실질 판정용 worklist 산출 (항상 exit 0)")
    p.add_argument("--critiques", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_prepare)

    d = sub.add_parser("decide", help="채워진 판정 슬롯 집계")
    d.add_argument("--worklist", required=True)
    d.add_argument("--report")
    d.add_argument("--fail-on-strawman", action="store_true")
    d.add_argument("--fail-on-unengaged", action="store_true")
    d.add_argument("--fail-on-flattened", action="store_true")
    d.set_defaults(func=cmd_decide)

    s = sub.add_parser("sync", help="정본→미러 전파 / --check는 drift만 보고(불일치 시 exit 1)")
    s.add_argument("--check", action="store_true")
    s.set_defaults(func=cmd_sync)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
