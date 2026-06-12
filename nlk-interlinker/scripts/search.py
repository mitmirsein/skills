#!/usr/bin/env python3
"""
NLK Interlinker — CLI Entry Point (lod.nl.go.kr SPARQL 기반)
==========================================================
국립중앙도서관 LOD(lod.nl.go.kr) SPARQL 엔드포인트를 직접 조회하여
제어번호(controlNumber)의 owl:sameAs 국내외 연계 식별자(VIAF/LoC/GND/BnF/
DBpedia/NDL/ISNI/Wikidata 등)를 수집하고 Obsidian 노트 YAML에 주입한다.

기존 data.go.kr InterlinkingInformationService 게이트웨이는 기관 백엔드 장애로
무응답이라 폐기하고, 동일 데이터의 권위 원천인 LOD SPARQL로 전환했다(무키).

사용법:
    python search.py <controlNumber> [options]
    python search.py --control-number <controlNumber> [options]
    python search.py --file "path/to/note.md"
"""

import asyncio
import argparse
import json
import sys
import os
import re
import httpx
import yaml

SPARQL_ENDPOINT = "https://lod.nl.go.kr/sparql"
RESOURCE_BASE = "http://lod.nl.go.kr/resource/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


# 외부 권위 식별자 호스트 → (기관 표시명, datatype 코드)
AUTHORITY_HOSTS = [
    ("viaf.org", "VIAF", "viaf"),
    ("id.loc.gov", "미국의회도서관(LoC)", "loc"),
    ("d-nb.info", "독일국립도서관(GND/DNB)", "dnb"),
    ("data.bnf.fr", "프랑스국립도서관(BnF)", "bnf"),
    ("datos.bne.es", "스페인국립도서관(BNE)", "bne"),
    ("dbpedia.org", "DBpedia", "dbpedia"),
    ("wikidata.org", "Wikidata", "wikidata"),
    ("id.ndl.go.jp", "일본국립국회도서관(NDL)", "ndl"),
    ("isni.org", "ISNI", "isni"),
    ("idref.fr", "IdRef(ABES)", "idref"),
    ("id.oclc.org", "OCLC WorldCat", "oclc"),
    ("data.kdata.kr", "한국데이터(KData)", "kdata"),
    ("lod.nl.go.kr", "국립중앙도서관(NLK)", "nlk"),
]


def classify_uri(uri: str) -> tuple[str, str, str]:
    """sameAs 대상 URI에서 (기관명, datatype, 식별자ID)를 추출한다."""
    institution, datatype = "", ""
    for host, name, code in AUTHORITY_HOSTS:
        if host in uri:
            institution, datatype = name, code
            break
    # 식별자 ID 추출
    identifier = ""
    if "wikidata.org" in uri:
        m = re.search(r"Q\d+", uri)
        identifier = m.group(0) if m else ""
    elif "bnf.fr" in uri:
        m = re.search(r"cb\d+[a-z0-9]?", uri)
        identifier = m.group(0) if m else ""
    elif "idref.fr" in uri:
        m = re.search(r"/(\d{6,})", uri)  # /033173672/id → 033173672
        identifier = m.group(1) if m else ""
    if not identifier:
        seg = uri.rstrip("/").split("/")[-1].split("#")[0]
        identifier = seg if seg and seg != "id" else ""
    return institution, datatype, identifier


def load_env_file(env_path: str = os.path.expanduser("~/Desktop/MS_Dev.nosync/.env")):
    """선택적: .env 로드(SPARQL은 키 불필요, 호환성 위해 유지)."""
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")


class NLKInterlinker:
    def __init__(self, endpoint: str = SPARQL_ENDPOINT):
        self.endpoint = endpoint

    @staticmethod
    def _resource_uri(control_number: str) -> str:
        cn = control_number.strip()
        if cn.startswith("http://") or cn.startswith("https://"):
            return cn
        return RESOURCE_BASE + cn

    async def fetch_lod(
        self,
        control_number: str,
        page: int = 1,
        limit: int = 50,
        result_type: str = "json",
    ) -> tuple[list[dict], dict]:
        """제어번호 → 리소스 URI → owl:sameAs 연계 목록 (SPARQL)."""
        uri = self._resource_uri(control_number)
        query = (
            "SELECT ?o WHERE { <%s> "
            "<http://www.w3.org/2002/07/owl#sameAs> ?o } LIMIT %d" % (uri, limit)
        )
        params = {"query": query}
        headers = {"User-Agent": UA, "Accept": "application/sparql-results+json"}
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                resp = await client.get(self.endpoint, params=params, headers=headers)
        except httpx.TimeoutException:
            return [], {"error": "SPARQL 요청 타임아웃 (lod.nl.go.kr 응답 지연)", "resource_uri": uri}
        except Exception as e:
            return [], {"error": str(e), "resource_uri": uri}

        if resp.status_code != 200:
            return [], {"error": f"HTTP {resp.status_code}", "resource_uri": uri, "body": resp.text[:300]}

        try:
            data = json.loads(resp.text)
        except json.JSONDecodeError as e:
            return [], {"error": f"SPARQL JSON 파싱 실패: {e}", "resource_uri": uri}

        bindings = data.get("results", {}).get("bindings", [])
        results = []
        seen = set()
        for b in bindings:
            target = (b.get("o", {}).get("value") or "").strip()
            if not target or target in seen:
                continue
            seen.add(target)
            institution, datatype, identifier = classify_uri(target)
            results.append({
                "datatype": datatype,
                "id": identifier,
                "institution": institution,
                "source_uri": uri,
                "target_uri": target,
            })
        return results, {"total_fetched": len(results), "total_count": len(results), "resource_uri": uri}


# ─────────────────────────────────────────────
# Obsidian 프론트매터 자동 인젝션 로직
# ─────────────────────────────────────────────

def extract_ids_from_uris(uris: list[str]) -> dict:
    """LOD URI 목록에서 대표 식별자 ID들을 추출한다."""
    extracted = {"wikidata": None, "lccn": None, "dnb": None, "bnf": None, "viaf": None, "isni": None}
    for uri in uris:
        if "wikidata.org" in uri:
            m = re.search(r"Q\d+", uri)
            if m:
                extracted["wikidata"] = m.group(0)
        elif "id.loc.gov" in uri:
            extracted["lccn"] = uri.rstrip("/").split("/")[-1]
        elif "d-nb.info" in uri:
            extracted["dnb"] = uri.rstrip("/").split("/")[-1]
        elif "bnf.fr" in uri:
            m = re.search(r"cb\d+[a-z0-9]?", uri)
            if m:
                extracted["bnf"] = m.group(0)
        elif "viaf.org" in uri:
            extracted["viaf"] = uri.rstrip("/").split("/")[-1]
        elif "isni.org" in uri:
            extracted["isni"] = uri.rstrip("/").split("/")[-1]
    return extracted


def enrich_markdown_file(file_path: str, lod_results: list[dict]) -> str:
    """마크다운 파일의 YAML 프론트매터에 LOD 정보를 안전하게 주입한다."""
    if not os.path.exists(file_path):
        return f"파일을 찾을 수 없습니다: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw_content, re.DOTALL)
    existing_yaml = {}
    body_content = raw_content
    if frontmatter_match:
        yaml_block = frontmatter_match.group(1)
        body_content = frontmatter_match.group(2)
        try:
            existing_yaml = yaml.safe_load(yaml_block) or {}
        except Exception as e:
            return f"YAML 파싱 실패: {e}"

    uris = []
    for item in lod_results:
        target = item.get("target_uri")
        if target and target not in uris:
            uris.append(target)

    if not uris:
        return "LOD 매핑 링크를 찾지 못해 파일을 업데이트하지 않았습니다."

    ids = extract_ids_from_uris(uris)

    if "owl_same_as" not in existing_yaml or not isinstance(existing_yaml.get("owl_same_as"), list):
        existing_yaml["owl_same_as"] = []
    for u in uris:
        if u not in existing_yaml["owl_same_as"]:
            existing_yaml["owl_same_as"].append(u)

    for key, val in ids.items():
        if val:
            existing_yaml[key] = val

    new_yaml_block = yaml.safe_dump(existing_yaml, allow_unicode=True, default_flow_style=False).strip()
    new_content = f"---\n{new_yaml_block}\n---\n{body_content}"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return "성공적으로 노트의 YAML 프론트매터에 LOD 식별자를 주입했습니다!"


# ─────────────────────────────────────────────
# 출력 포맷터
# ─────────────────────────────────────────────

def format_json(control_number: str, results: list[dict], stats: dict) -> str:
    return json.dumps({
        "control_number": control_number,
        "resource_uri": stats.get("resource_uri", ""),
        "total": len(results),
        "results": results,
        "stats": stats,
    }, ensure_ascii=False, indent=2)


def format_markdown(control_number: str, results: list[dict], stats: dict) -> str:
    lines = [
        f"## 국립중앙도서관 인터링킹 LOD 연계 결과: `{control_number}`",
        "",
        f"- 리소스 URI: `{stats.get('resource_uri', '')}`",
        f"- 조회 매핑 수: **{len(results)}건**",
        "",
    ]
    if not results:
        lines.append(f"> ⚠️ {stats.get('error', 'LOD 매핑 정보 없음 (제어번호/리소스 URI 확인)')}")
        return "\n".join(lines)

    lines.append("| # | 기관 | ID | URI |")
    lines.append("|---|------|----|-----|")
    for i, r in enumerate(results):
        institution = r.get("institution") or "-"
        identifier = r.get("id") or "-"
        target = r.get("target_uri") or "-"
        target_link = f"[{target}]({target})" if target.startswith("http") else target
        lines.append(f"| {i+1} | {institution} | `{identifier}` | {target_link} |")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 진입점
# ─────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(
        description="국립중앙도서관 LOD(SPARQL) 인터링킹 조회 및 Obsidian 연동 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python search.py KAC199600018 --output markdown
  python search.py --control-number KAC199600018 --output json
  python search.py --file "path/to/note.md"
        """,
    )
    parser.add_argument("control_number_arg", nargs="?", help="조회할 국립중앙도서관 제어번호 또는 리소스 URI")
    parser.add_argument("--control-number", help="조회할 국립중앙도서관 제어번호")
    parser.add_argument("--file", help="LOD 정보를 주입할 마크다운 파일. YAML에 control_number/nlk_control_number/controlNumber 중 하나 필요.")
    parser.add_argument("--limit", type=int, default=50, help="최대 연계 수 (기본: 50)")
    parser.add_argument("--output", default="json", choices=["json", "markdown"], help="출력 형식 (기본: json)")
    # 하위호환(무시): 과거 data.go.kr 시절 인자
    parser.add_argument("--page", type=int, default=1, help=argparse.SUPPRESS)
    parser.add_argument("--type", default="json", help=argparse.SUPPRESS)
    args = parser.parse_args()

    load_env_file()
    interlinker = NLKInterlinker()

    if args.file:
        file_path = os.path.abspath(args.file)
        if not os.path.exists(file_path):
            print(json.dumps({"error": f"지정된 파일을 찾을 수 없습니다: {file_path}"}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        control_number = None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if match:
                yaml_data = yaml.safe_load(match.group(1)) or {}
                for key in ("control_number", "nlk_control_number", "controlNumber"):
                    if yaml_data.get(key):
                        control_number = str(yaml_data[key])
                        break
        except Exception:
            pass

        if not control_number:
            print(json.dumps({"error": "파일 YAML에서 control_number/nlk_control_number/controlNumber를 찾지 못했습니다. 이 API는 제어번호 조회용입니다."}, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(f"노트 분석 완료. 제어번호 '{control_number}'로 LOD SPARQL을 조회합니다...", file=sys.stderr)
        results, stats = await interlinker.fetch_lod(control_number, limit=args.limit)
        if "error" in stats and not results:
            print(json.dumps({"error": stats["error"]}, ensure_ascii=False, indent=2))
            sys.exit(1)
        print(enrich_markdown_file(file_path, results))
        sys.exit(0)

    control_number = args.control_number or args.control_number_arg
    if not control_number:
        parser.print_help()
        sys.exit(1)
    results, stats = await interlinker.fetch_lod(control_number, limit=args.limit)
    if "error" in stats and not results:
        if args.output == "json":
            print(json.dumps({"error": stats["error"], "resource_uri": stats.get("resource_uri", "")}, ensure_ascii=False, indent=2))
        else:
            print(f"### ⚠️ 오류 발생\n- {stats['error']}")
        sys.exit(1)

    if args.output == "json":
        print(format_json(control_number, results, stats))
    else:
        print(format_markdown(control_number, results, stats))


if __name__ == "__main__":
    asyncio.run(main())
