#!/usr/bin/env python3
"""
RISS Searcher — CLI Entry Point
==================================
RISS(학술연구정보서비스) 논문 검색 스킬의 메인 실행 스크립트.

사용법:
    uv run python search.py <query> [options]
    uv run python search.py --detail --control-no <id> --mat-type <type>

출력 형식:
    --output json      에이전트 파싱 최적화 (기본값)
    --output markdown  인간 가독 테이블

⚠️  핵심 원칙:
    - curl_cffi InsaneRecon으로 TLS 핑거프린트 위장 (WAF 우회)
    - ForensicAudit 필터 의무 적용
    - httpx fallback 자동 지원
"""

import asyncio
import argparse
import json
import sys
import re
import urllib.parse
from typing import Optional

import httpx
from bs4 import BeautifulSoup

# 로컬 유틸리티 (같은 scripts/ 디렉토리)
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from recon_utils import InsaneRecon, ForensicAudit, logger


# ─────────────────────────────────────────────
# RISS Scraper (MCP 버전을 CLI용으로 리팩토링)
# ─────────────────────────────────────────────

class RissScraper:
    BASE_URL = "https://www.riss.kr"
    SEARCH_URL = f"{BASE_URL}/search/Search.do"
    DETAIL_URL = f"{BASE_URL}/search/detail/DetailView.do"

    # 카테고리 코드 매핑
    CATEGORIES = {
        "journal": "re_a_kor",     # 국내학술지논문 (기본값)
        "journal_over": "re_a_over",# 해외학술지논문
        "domestic": "re_d_kor",   # 국내 학위논문
        "foreign": "re_d_for",    # 해외 학위논문
        "book": "re_b_over",      # 단행본
        "report": "re_r_kor",     # 연구보고서
        # 코드 직접 입력도 지원
    }

    # 언어 코드 매핑
    LANG_MAP = {
        "kor": "KOR", "eng": "ENG", "ger": "GER",
        "fre": "FRE", "jpn": "JPN", "chi": "CHI",
    }

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.riss.kr/index.do",
        }

    # ── 검색 ─────────────────────────────────────────────────────────────────

    async def search(
        self,
        keyword: str,
        category: str = "re_a_over",
        page: int = 1,
        limit: int = 10,
        languages: Optional[list[str]] = None,
    ) -> tuple[list[dict], dict]:
        """
        RISS 논문 검색 (InsaneRecon TLS 우회 + ForensicAudit)
        
        Returns:
            (verified_results, audit_stats)
        """
        # 카테고리 별칭 처리
        category = self.CATEGORIES.get(category, category)
        start_count = (page - 1) * 10

        params: dict = {
            "isDetailSearch": "Y" if languages else "N",
            "searchGubun": "true",
            "viewYn": "OP",
            "query": keyword,
            "colName": category,
            "iStartCount": str(start_count),
            "iNextCount": str(limit),
            "pageScale": str(limit),
            "orderBy": "",
            "list_type": "list",
        }

        if languages:
            primary_lang = languages[0].lower()
            params["p_lang"] = self.LANG_MAP.get(primary_lang, primary_lang.upper())
            ex_queries = [f"language:{lang.lower()}\u25c8" for lang in languages]
            params["exQuery"] = "".join(ex_queries)

        query_str = urllib.parse.urlencode(params)
        search_url = f"{self.SEARCH_URL}?{query_str}"

        audit_stats = {"total_fetched": 0, "passed": 0, "rejected": 0}

        # 1. InsaneRecon (curl_cffi) 시도
        html = InsaneRecon.fetch(search_url)

        # 2. httpx fallback
        if not html:
            logger.warning("InsaneRecon 실패 — httpx fallback 시도")
            try:
                async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                    response = await client.get(
                        self.SEARCH_URL, params=params, headers=self.headers
                    )
                    if response.status_code == 200:
                        html = response.text
                    else:
                        audit_stats["error"] = f"HTTP {response.status_code}"
                        return [], audit_stats
            except Exception as e:
                audit_stats["error"] = str(e)
                return [], audit_stats

        raw_results = self._parse_search_results(html, category)
        audit_stats["total_fetched"] = len(raw_results)

        if not raw_results:
            audit_stats["warning"] = "검색 결과 없음"
            return [], audit_stats

        # ForensicAudit 필터링
        verified, rejected = ForensicAudit.audit_results(keyword, raw_results)
        audit_stats["passed"] = len(verified)
        audit_stats["rejected"] = len(rejected)

        if not verified:
            audit_stats["warning"] = "ForensicAudit 전체 실패 — 키워드 파편화 또는 카테고리 확인 필요"
            return [], audit_stats

        return verified[:limit], audit_stats

    def _parse_search_results(self, html: str, category: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        results = []

        items = soup.select("div.srchResultListW > ul > li")

        for item in items:
            title_tag = item.select_one("p.title a")
            if not title_tag:
                continue

            title = self._clean_text(title_tag.get_text(strip=True))
            href = title_tag.get("href", "")

            control_no = ""
            p_mat_type = ""
            if "control_no=" in href:
                parsed_url = urllib.parse.urlparse(href)
                query = urllib.parse.parse_qs(parsed_url.query)
                control_no = query.get("control_no", [""])[0]
                p_mat_type = query.get("p_mat_type", [""])[0]

            etc_tag = item.select_one("p.etc")
            info_text = self._clean_text(etc_tag.get_text(" ", strip=True)) if etc_tag else ""

            download_links = []
            info_div = item.select_one("div.info")
            if info_div:
                for a in info_div.select("a"):
                    label = a.get_text(strip=True)
                    url = a.get("href", "")
                    if "원문보기" in label or "Full Text" in label:
                        if url.startswith("/"):
                            url = self.BASE_URL + url
                        download_links.append({"type": label, "url": url})

            results.append({
                "title": title,
                "control_no": control_no,
                "p_mat_type": p_mat_type,
                "info": info_text,
                "url": self.BASE_URL + href if href.startswith("/") else href,
                "download_links": download_links,
            })

        return results

    # ── 상세 조회 ────────────────────────────────────────────────────────────

    async def get_detail(self, control_no: str, p_mat_type: str) -> dict:
        """RISS 논문 상세 (InsaneRecon 우선 + httpx fallback)"""
        params = {"control_no": control_no, "p_mat_type": p_mat_type}
        detail_url = f"{self.DETAIL_URL}?{urllib.parse.urlencode(params)}"

        html = InsaneRecon.fetch(detail_url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            return self._parse_detail(soup, control_no)

        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(self.DETAIL_URL, params=params, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                return self._parse_detail(soup, control_no)

        return {"control_no": control_no, "abstract": "상세 정보를 불러올 수 없습니다.", "metadata": {}}

    def _parse_detail(self, soup: BeautifulSoup, control_no: str) -> dict:
        # div.textWrap, div.text.off, div.abstractFull 등 다양한 태그 탐색
        abstract_tags = soup.select(
            "div.abstractFull, div.abstract_box, #abstract, .abstract_txt, div.textWrap, div.text.off"
        )
        abstract = ""
        for tag in abstract_tags:
            text = tag.get_text(strip=True)
            if text:
                abstract += text + "\n\n"

        if not abstract:
            abstract = "초록 정보가 제공되지 않습니다."

        metadata = {}
        info_table = soup.select_one("div.infoDetail, div.infoDetailL, div.inner_info_table, .info_txt, .detail_info")
        if info_table:
            for row in info_table.select("li, tr"):
                th = row.select_one("span.strong, th, span.th, dt")
                td = row.select_one("div, td, span.td, dd")
                if th and td:
                    key = th.get_text(strip=True)
                    val = td.get_text(separator=" ", strip=True)
                    if key and val:
                        # 불필요한 연속 공백 제거
                        val = " ".join(val.split())
                        metadata[key] = val

        return {
            "control_no": control_no,
            "abstract": abstract.strip(),
            "metadata": metadata,
        }

    # ── 헬퍼 ─────────────────────────────────────────────────────────────────

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        return re.sub(r"\s+", " ", text).strip()


# ─────────────────────────────────────────────
# 출력 포맷터
# ─────────────────────────────────────────────

def format_json(query: str, results: list[dict], audit_stats: dict) -> str:
    output = {
        "query": query,
        "total": len(results),
        "results": [
            {
                "rank": i + 1,
                "title": r.get("title", ""),
                "control_no": r.get("control_no", ""),
                "p_mat_type": r.get("p_mat_type", ""),
                "info": r.get("info", ""),
                "url": r.get("url", ""),
                "download_links": r.get("download_links", []),
            }
            for i, r in enumerate(results)
        ],
        "forensic_audit": audit_stats,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def format_markdown(query: str, results: list[dict], audit_stats: dict) -> str:
    lines = [
        f"## RISS 검색 결과: `{query}`",
        f"",
        f"- 검색 총량: {audit_stats.get('total_fetched', 0)}건",
        f"- ForensicAudit 통과: **{audit_stats.get('passed', 0)}건**",
        f"- 노이즈 제거: {audit_stats.get('rejected', 0)}건",
        f"",
    ]

    if not results:
        lines.append(f"> ⚠️ {audit_stats.get('warning', audit_stats.get('error', '결과 없음'))}")
        return "\n".join(lines)

    lines.append("| # | 제목 | 정보 | control_no |")
    lines.append("|---|------|------|------------|")
    for i, r in enumerate(results):
        title = r.get("title", "")
        url = r.get("url", "")
        title_link = f"[{title}]({url})" if url else title
        info = r.get("info", "-")[:60]
        control_no = r.get("control_no", "")
        lines.append(f"| {i+1} | {title_link} | {info} | `{control_no}` |")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 진입점
# ─────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(
        description="RISS 논문 검색 CLI (InsaneRecon TLS 우회 + ForensicAudit)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  uv run python search.py "바르트 계시론" --output json
  uv run python search.py "구원론" --category domestic --lang kor
  uv run python search.py "pneumatology" --lang eng --output markdown
  uv run python search.py --detail --control-no RBIB0000123456 --mat-type 1

카테고리:
  journal   학술지 논문 (기본값)
  domestic  국내 학위논문
  foreign   해외 학위논문
  book      단행본
  report    연구보고서
        """,
    )
    parser.add_argument("query", nargs="?", help="검색 키워드")
    parser.add_argument("--detail", action="store_true", help="상세 조회 모드")
    parser.add_argument("--control-no", metavar="ID", help="RISS control_no")
    parser.add_argument("--mat-type", metavar="TYPE", default="1", help="p_mat_type (기본값: 1)")
    parser.add_argument(
        "--output", choices=["json", "markdown"], default="json",
        help="출력 형식 (기본값: json)"
    )
    parser.add_argument("--page", type=int, default=1, help="검색 페이지 (기본값: 1)")
    parser.add_argument(
        "--category", default="journal",
        help="검색 카테고리 (journal/domestic/foreign/book/report 또는 RISS 코드 직접 입력)"
    )
    parser.add_argument(
        "--lang", dest="languages", action="append",
        metavar="LANG", help="언어 필터 (kor/eng/ger/fre/jpn, 반복 가능)"
    )
    parser.add_argument("--limit", type=int, default=10, help="최대 결과 수 (기본값: 10)")

    args = parser.parse_args()
    scraper = RissScraper()

    if args.detail:
        if not args.control_no:
            print("오류: --detail 모드에는 --control-no가 필요합니다.", file=sys.stderr)
            sys.exit(1)
        result = await scraper.get_detail(args.control_no, args.mat_type)
        if args.output == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"## RISS 상세: `{args.control_no}`\n")
            print(f"**초록**:\n{result.get('abstract', '초록 없음')}")
            if result.get("metadata"):
                print("\n**메타데이터**:")
                for k, v in result["metadata"].items():
                    print(f"- **{k}**: {v}")

    elif args.query:
        results, audit_stats = await scraper.search(
            keyword=args.query,
            category=args.category,
            page=args.page,
            limit=args.limit,
            languages=args.languages,
        )
        if args.output == "json":
            print(format_json(args.query, results, audit_stats))
        else:
            print(format_markdown(args.query, results, audit_stats))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
