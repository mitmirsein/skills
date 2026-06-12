#!/usr/bin/env python3
"""MS_Dev .skills 라이브러리 표준(STANDARDS.md) 검증기.

deps: Python 3.9+ stdlib only.
실행:
  python3 .skills/_meta/validate.py            # 전체 감사 → _meta/AUDIT.md, _meta/audit.json
  python3 .skills/_meta/validate.py <skill>    # 단일 스킬 콘솔 검사
  python3 .skills/_meta/validate.py --index    # 전체 감사 + INDEX.md 생성
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1]

# 등급 산정 제외 대상 (gws는 외부 유래 묶음 — 인벤토리만)
EXCLUDE_DIRS = {"_meta", "_template", "gws"}

SCAN_EXTS = {".md", ".py", ".json", ".sh", ".js", ".ts", ".yaml", ".yml", ".toml", ".txt", ".html"}
SCAN_SKIP_DIRS = {".venv", "node_modules", ".playwright-cli", "__pycache__", ".git", "output", "results", "bin"}

# 실존 의심 모델명 목록 — 2026-06-12 재평가: GPT-5.5/Claude 4.7/Gemini 3.1은 지식 컷오프
# 이후 실재 가능성이 있어 철회. 명백한 오기를 발견할 때만 추가한다.
PHANTOM_MODELS: list = []
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
USER_PATH_RE = re.compile(r"/Users/([A-Za-z0-9._-]+)/")
REQUIRED_FIELDS = ["name", "description", "version"]
LINE_SOFT_CAP, LINE_HARD_CAP = 150, 200

CATEGORY = {
    "theology": [
        "faith-compass", "theology-research", "theology-exegesis", "theology-scholar",
        "theology-reviewer", "theology-redteam", "theology-reader", "theology-citation-linker",
        "theology-discourse-mapper", "theology-pdf-maker", "theology-terminology-linter",
        "theology-chunker", "theology-translator", "theology-local-searcher",
        "barth-kd-navigator", "sermon-insight", "rise-battleground-map", "bible-meditation",
    ],
    "academic-search": [
        "paper-xray", "kci-api-searcher",
        "nlk-biblio-searcher", "nlk-subject-searcher", "nlk-interlinker", "riss-searcher",
        "google-scholar-quick", "google-scholar-semantic", "crossref-journal-searcher",
        "ixtheo-searcher", "semantic-scholar", "notebooklm", "notebooklm-researcher",
        "tawp", "journal-collector",
    ],
    "media": [
        "slide", "create-slide-from-markdown", "create-slide-image-prompts",
        "lecture-video-generator", "remotion-studio", "yt-digest", "yt-subtitle-helper",
        "epub-bindery", "pdf-extractor", "hwp-converter", "media-factory", "academic-illustrator",
    ],
    "dev-tools": [
        "insane-search",
        "git-workflow", "github-ops", "code-simplifier", "tech-tdd", "tech-reviewer",
        "tech-architect", "tech-strategist", "agent-forge", "prompt-engineer",
        "stealth-browser", "langgraph-supervisor", "react-components", "log-miner",
        "lightpanda-recon",
    ],
    "vault": [
        "obsidian-cli", "obsidian-web-clipper", "zettel-capture", "note-share",
        "knowledge-archivist", "arc-librarian", "vault-query", "wiki",
        "knowledge-gardener", "digital-curator",
    ],
    "writing": [
        "clear-english-writer", "clear-korean-writer", "slash-criticalthink",
        "eng-student-consultant", "voca-guide",
    ],
    "utilities": [
        "mole-manager", "batch-operator", "design-md", "dictionary-editor",
        "visual-feedback", "continuous-learner", "research-mentor", "thoughtbox-lite",
        "btw", "grafeo-connector", "ontology-builder",
    ],
}
SKILL_CATEGORY = {s: c for c, skills in CATEGORY.items() for s in skills}


def parse_frontmatter(text: str):
    """PyYAML 없이 관용적으로 frontmatter를 파싱한다. 실패 시 None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fm: dict = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            return fm
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val in (">", "|", ">-", "|-", ""):
                block, j = [], i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if nxt.strip() == "---" or re.match(r"^[A-Za-z_][\w-]*:", nxt):
                        break
                    block.append(nxt.strip())
                    j += 1
                items = [b for b in block if b]
                if items and all(b.startswith("- ") for b in items):
                    fm[key] = [b[2:].strip().strip("\"'") for b in items]
                else:
                    fm[key] = " ".join(items)
                i = j
                continue
            fm[key] = val.strip("\"'")
        i += 1
    return None  # 닫는 --- 없음


def iter_text_files(skill_dir: Path):
    for p in skill_dir.rglob("*"):
        if any(part in SCAN_SKIP_DIRS for part in p.relative_to(skill_dir).parts):
            continue
        if p.is_file() and p.suffix.lower() in SCAN_EXTS:
            yield p


def check_skill(skill_dir: Path) -> dict:
    name = skill_dir.name
    errors, warnings = [], []
    r: dict = {"skill": name, "category": SKILL_CATEGORY.get(name, "uncategorized"),
               "symlink": skill_dir.is_symlink(), "lines": 0, "status": "",
               "description": "", "version": ""}

    if skill_dir.is_symlink() and not skill_dir.resolve().exists():
        errors.append("E08 심링크 대상 없음 (broken symlink)")
        r.update(errors=errors, warnings=warnings, grade="F")
        return r

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append("E01 SKILL.md 없음")
    else:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        n_lines = len(text.splitlines())
        r["lines"] = n_lines
        if n_lines > LINE_HARD_CAP:
            errors.append(f"E06 SKILL.md {n_lines}줄 (상한 {LINE_HARD_CAP}줄 초과)")
        elif n_lines > LINE_SOFT_CAP:
            warnings.append(f"W06 SKILL.md {n_lines}줄 (권장 {LINE_SOFT_CAP}줄 초과)")

        fm = parse_frontmatter(text)
        if fm is None:
            errors.append("E02 frontmatter 누락/파싱 불가")
        else:
            for f in REQUIRED_FIELDS:
                if not fm.get(f):
                    errors.append(f"E03 필수 필드 없음: {f}")
            desc = fm.get("description", "")
            desc = desc if isinstance(desc, str) else " ".join(desc)
            r["description"] = desc
            r["version"] = str(fm.get("version", ""))
            r["status"] = str(fm.get("status", ""))
            fm_name = str(fm.get("name", ""))
            if fm_name and fm_name != name:
                warnings.append(f"W04 name '{fm_name}' ≠ 디렉토리명")
            if desc and ("Use when" not in desc or "키워드" not in desc):
                warnings.append("W05 description 하이브리드 형식 아님 (§3)")
            ver = r["version"]
            if ver and not SEMVER_RE.match(ver):
                errors.append(f"E12 version SemVer 아님: '{ver}'")
            if not r["status"]:
                warnings.append("W13 status 필드 없음 (active|stub|deprecated)")
            elif r["status"] not in ("active", "stub", "deprecated"):
                warnings.append(f"W13 status 값 비표준: '{r['status']}'")

        # 본문이 참조하는 로컬 파일 존재 확인 (경로 경계 앵커 — 긴 외부 경로 내부 매칭 방지)
        missing_refs = set()
        for ref in re.findall(r"(?<![\w가-힣/~.-])(?:references|scripts|templates|assets|evals)/[\w가-힣./-]+", text):
            ref = ref.rstrip(".,)»`'\"")
            if not (skill_dir / ref).exists():
                missing_refs.add(ref)
        if missing_refs:
            warnings.append("W09 참조 파일 없음: " + ", ".join(sorted(missing_refs)[:5]))

    # 스킬 전체 파일 스캔: 절대 사용자 경로 / 유령 모델 / 내부 심링크
    path_hits: dict = {}
    phantom_hits = set()
    for p in iter_text_files(skill_dir):
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for user in USER_PATH_RE.findall(content):
            path_hits.setdefault(user, set()).add(str(p.relative_to(skill_dir)))
        for model in PHANTOM_MODELS:
            if model in content:
                phantom_hits.add(model)
    for user, files in sorted(path_hits.items()):
        errors.append(f"E07 절대경로 /Users/{user}/ 하드코딩 ({len(files)}개 파일)")
    if phantom_hits:
        warnings.append("W10 실존하지 않는 모델명: " + ", ".join(sorted(phantom_hits)))

    for sub in skill_dir.rglob("*"):
        if sub.is_symlink() and not sub.resolve().exists():
            errors.append(f"E08 내부 심링크 깨짐: {sub.relative_to(skill_dir)}")
    for bad in (".venv", "node_modules"):
        if (skill_dir / bad).is_dir():
            warnings.append(f"W11 스킬 내부 {bad}/ 존재 (§1 위반)")

    # 폐기 스킬은 형식 경고(W05/W06/W13) 면제 — 오류만 추적
    if r["status"] == "deprecated":
        warnings = [w for w in warnings if not w.startswith(("W05", "W06", "W13"))]
        r["warnings"] = warnings
    # 스텁 스킬은 W09(참조 파일 부재) 면제 — 본문에 '구현 부재'를 명시한 설계 명세 허용
    if r["status"] == "stub":
        warnings = [w for w in warnings if not w.startswith("W09")]
        r["warnings"] = warnings

    if not skill_md.is_file():
        grade = "F"
    elif len(errors) >= 3:
        grade = "D"
    elif errors:
        grade = "C"
    elif warnings:
        grade = "B"
    else:
        grade = "A"
    r.update(errors=errors, warnings=warnings, grade=grade)
    return r


def run_audit():
    results = []
    for entry in sorted(SKILLS_ROOT.iterdir()):
        if entry.name.startswith(".") or entry.name in EXCLUDE_DIRS:
            continue
        if not (entry.is_dir() or entry.is_symlink()):
            continue
        results.append(check_skill(entry))
    return results


def write_audit_md(results):
    today = date.today().isoformat()
    dist = {}
    for r in results:
        dist[r["grade"]] = dist.get(r["grade"], 0) + 1
    lines = [
        "# .skills 감사 결과 (AUDIT)", "",
        f"생성: {today} / 검사 대상: {len(results)}개 (gws, _template 제외) / 도구: `_meta/validate.py`", "",
        "## 등급 분포", "",
        "| A | B | C | D | F |", "|---|---|---|---|---|",
        "| " + " | ".join(str(dist.get(g, 0)) for g in "ABCDF") + " |", "",
        "## 스킬별 결과", "",
        "| 스킬 | 등급 | 분류 | 줄수 | 문제 |", "|---|---|---|---|---|",
    ]
    order = {"F": 0, "D": 1, "C": 2, "B": 3, "A": 4}
    for r in sorted(results, key=lambda x: (order[x["grade"]], x["skill"])):
        issues = r["errors"] + r["warnings"]
        mark = " 🔗" if r["symlink"] else ""
        lines.append(
            f"| {r['skill']}{mark} | {r['grade']} | {r['category']} | {r['lines'] or '—'} | "
            + ("; ".join(issues) if issues else "—") + " |"
        )
    lines += ["", "🔗 = 심링크 스킬 (본체는 MS_Brain 등 외부에서 관리)", ""]
    (SKILLS_ROOT / "_meta" / "AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    (SKILLS_ROOT / "_meta" / "audit.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1, default=list), encoding="utf-8")
    return dist


def write_index_md(results):
    today = date.today().isoformat()
    lines = [
        "# .skills 스킬 인덱스 (INDEX)", "",
        f"갱신: {today} / `python3 _meta/validate.py --index`로 재생성", "",
        "gws/(Google Workspace 하위 스킬 98개)는 외부 유래 묶음으로 본 인덱스에서 제외.", "",
    ]
    by_cat: dict = {}
    for r in results:
        by_cat.setdefault(r["category"], []).append(r)
    for cat in sorted(by_cat):
        lines += [f"## {cat} ({len(by_cat[cat])})", "",
                  "| 스킬 | 상태 | 등급 | 설명 |", "|---|---|---|---|"]
        for r in sorted(by_cat[cat], key=lambda x: x["skill"]):
            desc = (r["description"][:90] + "…") if len(r["description"]) > 90 else (r["description"] or "—")
            lines.append(f"| {r['skill']} | {r['status'] or '—'} | {r['grade']} | {desc} |")
        lines.append("")
    (SKILLS_ROOT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    args = [a for a in sys.argv[1:]]
    if args and not args[0].startswith("--"):
        target = SKILLS_ROOT / args[0]
        if not (target.is_dir() or target.is_symlink()):
            print(f"스킬 없음: {args[0]}")
            sys.exit(2)
        r = check_skill(target)
        print(f"[{r['grade']}] {r['skill']} ({r['lines']}줄)")
        for e in r["errors"]:
            print(f"  ERROR {e}")
        for w in r["warnings"]:
            print(f"  WARN  {w}")
        sys.exit(1 if r["errors"] else 0)

    results = run_audit()
    dist = write_audit_md(results)
    if "--index" in args:
        write_index_md(results)
        print("INDEX.md 생성됨")
    total_err = sum(len(r["errors"]) for r in results)
    total_warn = sum(len(r["warnings"]) for r in results)
    print(f"검사 {len(results)}개 | 등급 " + " ".join(f"{g}:{dist.get(g,0)}" for g in "ABCDF")
          + f" | 오류 {total_err} 경고 {total_warn}")
    print(f"보고서: {SKILLS_ROOT / '_meta' / 'AUDIT.md'}")


if __name__ == "__main__":
    main()
