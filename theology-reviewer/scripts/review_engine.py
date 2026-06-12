"""
Theology Review Engine v10.5
Parrehsia Unified Protocol — Phase 0 + Phase 1 + Phase 2 오케스트레이터

Phase 0: 핵심 용어 추출 → QuerySet 생성 → S2/Labs/Quick EvidencePack 저장
Phase 1: 8차원 unified_review 핸드오프 패킷 구성
Phase 2: Dialectical Verification — 삼각 검증 + 적대적 재구성 + 신뢰도 교정
"""
import argparse
import os
import json
import re
import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# Skill-level config.json 로딩 (internal_db 활성화 여부 등)
SKILL_DIR = Path(__file__).resolve().parents[1]
SKILLS_ROOT = SKILL_DIR.parent
DEV_ROOT = SKILLS_ROOT.parent
_SKILL_CONFIG_PATH = SKILL_DIR / "config.json"
CONFIG_SCHEMA_VERSION = 1
CITATION_DEPTH_CHOICES = {"all", "top5", "none"}


def _load_skill_config() -> dict:
    if not _SKILL_CONFIG_PATH.exists():
        return {}
    config = json.loads(_SKILL_CONFIG_PATH.read_text(encoding="utf-8"))
    meta = config.get("_meta", {})
    schema_version = int(meta.get("schema_version", CONFIG_SCHEMA_VERSION))
    if schema_version != CONFIG_SCHEMA_VERSION:
        raise ValueError(f"Unsupported theology-reviewer config schema_version={schema_version}")

    gs_cfg = config.get("integration", {}).get("google_scholar_semantic", {})
    citation_depth = gs_cfg.get("citation_depth", "all")
    if citation_depth not in CITATION_DEPTH_CHOICES:
        raise ValueError(f"google_scholar_semantic.citation_depth must be one of {sorted(CITATION_DEPTH_CHOICES)}")
    max_qps = int(gs_cfg.get("max_queries_per_session", 4))
    if max_qps < 1 or max_qps > 4:
        raise ValueError("google_scholar_semantic.max_queries_per_session must be between 1 and 4")
    return config


SKILL_CONFIG = _load_skill_config()
INTEGRATION_CFG = SKILL_CONFIG.get("integration", {})
S2_CFG = INTEGRATION_CFG.get("semantic_scholar_api", {})
SCHOLAR_QUICK_CFG = INTEGRATION_CFG.get("google_scholar_quick", {})
GS_SEMANTIC_CFG = INTEGRATION_CFG.get("google_scholar_semantic", {})
IXTHEO_CFG = INTEGRATION_CFG.get("ixtheo_searcher", {})
CROSSREF_CFG = INTEGRATION_CFG.get("crossref_journal_searcher", {})
KCI_CFG = INTEGRATION_CFG.get("kci_searcher", {})
RISS_CFG = INTEGRATION_CFG.get("riss_searcher", {})
INTERNAL_DB_ENABLED = SKILL_CONFIG.get("integration", {}).get("internal_db", {}).get("enabled", False)


def _cfg_path(value: str | None, fallback: Path) -> Path:
    path = Path(value).expanduser() if value else fallback
    if not path.is_absolute():
        path = DEV_ROOT / path
    return path

# --- 경로 설정 (master_config.json.md 참조) ---
PROJECT_ROOT = _cfg_path(SKILL_CONFIG.get("engine_root"), DEV_ROOT / "projects" / "easy-review-system")
BRAIN_ROOT   = _cfg_path(SKILL_CONFIG.get("brain_root"), Path(os.path.expanduser("~/Desktop/MS_Brain.nosync")))

S2_RUNNER = _cfg_path(
    S2_CFG.get("runner_path"),
    SKILLS_ROOT / "semantic-scholar" / "scripts" / "s2_runner.py"
)
SCHOLAR_QUICK_SH = _cfg_path(
    SCHOLAR_QUICK_CFG.get("script_path"),
    SKILLS_ROOT / "google-scholar-quick" / "google_scholar_quick_search.sh"
)
GS_SEMANTIC_RUNNER = _cfg_path(
    GS_SEMANTIC_CFG.get("runner_path"),
    SKILLS_ROOT / "google-scholar-semantic" / "scripts" / "scholar_runner.py"
)
IXTHEO_RUNNER = _cfg_path(
    IXTHEO_CFG.get("script_path"),
    SKILLS_ROOT / "ixtheo-searcher" / "scripts" / "ixtheo_searcher.py"
)
CROSSREF_RUNNER = _cfg_path(
    CROSSREF_CFG.get("script_path"),
    SKILLS_ROOT / "crossref-journal-searcher" / "scripts" / "crossref_journal_searcher.py"
)
KCI_RUNNER = _cfg_path(
    KCI_CFG.get("script_path"),
    SKILLS_ROOT / "kci-api-searcher" / "scripts" / "search.py"
)
RISS_RUNNER = _cfg_path(
    RISS_CFG.get("script_path"),
    SKILLS_ROOT / "riss-searcher" / "scripts" / "search.py"
)

PROMPT_DIR  = PROJECT_ROOT / "prompts"
CONFIG_DIR  = PROJECT_ROOT / "configs"

# master_config에서 output_paths 읽어옴 (동적 로드)
def _load_master_config() -> dict:
    cfg_path = CONFIG_DIR / "master_config.json.md"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.loads(f.read())

MASTER_CFG    = _load_master_config()
OUTPUT_PATHS  = MASTER_CFG.get("output_paths", {})

OUTPUT_CFG = SKILL_CONFIG.get("output", {})
REVIEW_REPORTS_DIR = _cfg_path(
    OUTPUT_CFG.get("review_reports"),
    BRAIN_ROOT / "000 System" / "Inbox" / "Review_Reports"
)
EVIDENCE_DIR = _cfg_path(
    OUTPUT_CFG.get("evidence_packs"),
    BRAIN_ROOT / "000 System" / "Inbox" / "Evidence"
)
SESSION_LOGS_DIR = _cfg_path(
    OUTPUT_CFG.get("session_logs"),
    BRAIN_ROOT / "900 Archive" / "Review_Logs"
)


class TheologyReviewEngine:
    """
        Parrehsia v10.5 Unified Review Engine
    Phase 0: Agentic Evidence Gathering
    Phase 1: 8차원 Unified Review 오케스트레이션
    Phase 2: Dialectical Verification (삼각 검증 + 적대적 재구성 + 투명성 보고)
    """

    def __init__(self, target_file: str):
        self.target_file  = Path(target_file)
        self.session_id   = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir  = EVIDENCE_DIR / self.session_id
        self.evidence_pack = {
            "schema_version": 1,
            "session_id": self.session_id,
            "target":     str(self.target_file),
            "anchors":    [],
            "variants":   [],
            "counterexample_candidates": [],
            "abstracts":  [],
            "provenance": []
        }
        self.tool_log: list[dict] = []

    # ──────────────────────────────────────────────
    # 공통 유틸
    # ──────────────────────────────────────────────

    def load_prompt(self, prompt_name: str) -> dict:
        """프롬프트 파일 로드 (JSON-in-Markdown 지원)"""
        path = PROMPT_DIR / f"{prompt_name}.json.md"
        if not path.exists():
            path = PROMPT_DIR / prompt_name
        if not path.exists():
            raise FileNotFoundError(f"프롬프트 파일을 찾을 수 없습니다: {prompt_name}")

        raw = path.read_text(encoding="utf-8")
        # Markdown 코드 블록 래핑 제거
        raw = re.sub(r"^```(?:json)?\n", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"\n```\s*$", "", raw, flags=re.MULTILINE)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"{prompt_name} 파싱 실패: {e}") from e

    def _log_tool(self, tool_id: str, intent: str, result: str, limit: str = ""):
        """[ToolLogSummary] 규약에 따라 도구 호출 기록"""
        self.tool_log.append({
            "tool_id": tool_id,
            "intent":  intent,
            "result":  result,
            "limit":   limit,
            "ts":      datetime.now().isoformat()
        })

    def _save_json(self, data: dict, dest: Path):
        """디렉토리 자동 생성 후 JSON 저장"""
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✅ 저장 완료: {dest}")

    def _load_target_text(self, purpose: str = "review") -> str:
        """논문 텍스트 로드. PDF는 추출 스킬을 먼저 거치도록 명시적으로 차단한다."""
        if self.target_file.suffix.lower() == ".pdf":
            message = (
                f"PDF 직접 파싱은 {purpose} 단계에서 지원하지 않습니다. "
                "먼저 `pdf-extractor`로 Markdown/Text를 만들고, 필요하면 `paper-xray`로 구조 브리핑을 만든 뒤 "
                "그 산출물을 theology-reviewer에 입력하세요."
            )
            raise ValueError(message)
        return self.target_file.read_text(encoding="utf-8", errors="ignore")

    def _normalize_evidence_item(self, item: dict, source_tool: str) -> dict:
        """Phase 간 공유를 위해 외부 도구 결과를 최소 공통 스키마로 맞춘다.

        RISS의 특유 info 필드(저자|학술지|연도)가 포함된 경우 정규식으로 파싱하여 정규화한다.
        """
        if source_tool == "riss_searcher":
            info_str = item.get("info", "")
            if info_str:
                parsed_year = None
                parsed_authors = []
                parsed_venue = ""
                
                if "|" in info_str:
                    parts = [p.strip() for p in info_str.split("|") if p.strip()]
                    # 연도 추출 (4자리 숫자)
                    for part in parts:
                        match = re.search(r'\b(19\d{2}|20\d{2})\b', part)
                        if match:
                            try:
                                parsed_year = int(match.group(1))
                            except ValueError:
                                pass
                    
                    if len(parts) >= 3:
                        parsed_authors = [parts[0]]
                        parsed_venue = parts[1]
                    elif len(parts) == 2:
                        parsed_authors = [parts[0]]
                        # 연도 매칭이 안 된 것을 venue로 취급
                        if parsed_year and str(parsed_year) in parts[1]:
                            pass
                        else:
                            parsed_venue = parts[1]
                    elif len(parts) == 1:
                        parsed_authors = [parts[0]]
                else:
                    # 수직바가 없는 공백 구분 구조 ("저자 발행처 연도 학술지정보")
                    match = re.search(r'\b(19\d{2}|20\d{2})\b', info_str)
                    if match:
                        try:
                            parsed_year = int(match.group(1))
                        except ValueError:
                            pass
                        year_str = match.group(0)
                        idx = info_str.find(year_str)
                        before_year = info_str[:idx].strip()
                        after_year = info_str[idx + len(year_str):].strip()
                        
                        # 저자 파싱: 첫 어절(괄호 포함 가능)
                        author_match = re.match(r'^([^\s]+(?:\([^\)]+\))?)', before_year)
                        if author_match:
                            parsed_authors = [author_match.group(1).strip()]
                        else:
                            parsed_authors = [before_year] if before_year else []
                            
                        # 학술지명 파싱: Vol/No/숫자 이전
                        venue_match = re.split(r'\b(Vol\.|No\.|v\.|n\.|[0-9])', after_year, maxsplit=1, flags=re.IGNORECASE)
                        parsed_venue = venue_match[0].strip() if venue_match else after_year
                        if not parsed_venue:
                            parsed_venue = after_year
                    else:
                        # 연도가 없는 경우 공백 기준 분할
                        space_parts = info_str.split()
                        if space_parts:
                            parsed_authors = [space_parts[0]]
                            if len(space_parts) > 1:
                                parsed_venue = " ".join(space_parts[1:])
                
                if parsed_year and not item.get("year"):
                    item["year"] = parsed_year
                if parsed_authors and not item.get("authors"):
                    item["authors"] = parsed_authors
                if parsed_venue and not item.get("journal"):
                    item["journal"] = parsed_venue
                    item["venue"] = parsed_venue

        authors = item.get("authors", [])
        if isinstance(authors, str):
            authors = [a.strip() for a in re.split(r",|;|\band\b", authors) if a.strip()]
        if not isinstance(authors, list):
            authors = []

        abstract = item.get("abstract") or item.get("snippet") or item.get("summary") or ""
        citation_status = item.get("citation_status", "")
        return {
            "schema_version": 1,
            "source_tool": source_tool,
            "source": item.get("source", source_tool),
            "query": item.get("query", ""),
            "rank": item.get("rank"),
            "title": item.get("title", ""),
            "authors": authors,
            "authors_text": item.get("authors_text", ""),
            "year": item.get("year"),
            "venue": item.get("venue") or item.get("journal") or "",
            "url": item.get("url") or item.get("link") or "",
            "doi": item.get("doi", ""),
            "abstract": abstract,
            "snippet": item.get("snippet", abstract),
            "citation": item.get("citation", ""),
            "citation_variants": item.get("citation_variants", []),
            "citation_links": item.get("citation_links", []),
            "citation_status": citation_status,
            "citation_count": item.get("citation_count", item.get("citationCount", 0)),
            "provenance": {
                "raw_source_tool": source_tool,
                "source_file": item.get("source_file", ""),
                "retrieved_at": item.get("retrieved_at", datetime.now().isoformat()),
            },
            "raw": item,
        }

    def _validate_evidence_pack(self, evidence_pack: dict) -> list[str]:
        """EvidencePack 최소 계약 점검. 실패해도 저장은 가능하게 경고 목록만 반환."""
        warnings = []
        if evidence_pack.get("schema_version") != 1:
            warnings.append("schema_version is not 1")
        for key in ("session_id", "target", "abstracts", "provenance"):
            if key not in evidence_pack:
                warnings.append(f"missing key: {key}")
        for idx, item in enumerate(evidence_pack.get("abstracts", []), 1):
            for key in ("source_tool", "title", "abstract", "provenance"):
                if key not in item:
                    warnings.append(f"abstracts[{idx}] missing key: {key}")
        return warnings

    # ──────────────────────────────────────────────
    # Phase 0: Evidence Gathering
    # ──────────────────────────────────────────────

    def prepare_pass0(self) -> dict:
        """
        Phase 0: 핵심 용어 추출 → QuerySet 생성 → 삼중 증거 수집 → EvidencePack 저장

        v10.5 증강:
          (1) Semantic Scholar API (s2_runner.py) — 구조화된 메타데이터 자동 수집
          (2) Google Scholar Labs (google-scholar-semantic) — 시맨틱 맥락 자동 수집
          (3) google-scholar-quick (Google Scholar CDP) — 경량 보완 검색
        """
        print(f"\n🚀 [Phase 0] 증거 수집 시작 (v10.5): {self.target_file.name}")

        # 1. agentic_gather 프롬프트 로드
        gather_prompt = self.load_prompt("agentic_gather")
        self._log_tool("agentic_gather", "EvidencePack 수집 지침 로드", "성공", "")

        # 2. 논문 텍스트 읽기
        paper_text = self._load_target_text("Phase 0")

        # 3. QuerySet 생성
        query_set = self._generate_query_set(paper_text)
        query_set_path = self.session_dir / "QuerySet.json"
        self._save_json(query_set, query_set_path)
        self._log_tool("keyword_extractor", "QuerySet 생성", f"{len(query_set['queries'])}개 쿼리 생성", "")

        # 4. 증거 수집 (Semantic Scholar API + Google Scholar Labs + google-scholar-quick)
        evidence_results = self._try_evidence_sources(query_set)

        # 5. EvidencePack 구성 및 저장
        self.evidence_pack["query_set_path"]   = str(query_set_path)
        self.evidence_pack["abstracts"]        = [
            self._normalize_evidence_item(item, item.get("source_tool", "unknown"))
            for item in evidence_results.get("abstracts", [])
        ]
        self.evidence_pack["provenance"]       = evidence_results.get("provenance", [])
        self.evidence_pack["semantic_scholar"]      = evidence_results.get("semantic_scholar", [])
        self.evidence_pack["google_scholar_labs"]   = evidence_results.get("google_scholar_labs", [])
        self.evidence_pack["google_scholar_quick"]  = evidence_results.get("google_scholar_quick", [])
        self.evidence_pack["google_scholar"]        = evidence_results.get("google_scholar", [])
        self.evidence_pack["ixtheo"]                = evidence_results.get("ixtheo", [])
        self.evidence_pack["crossref_journal"]      = evidence_results.get("crossref_journal", [])
        self.evidence_pack["kci"]                   = evidence_results.get("kci", [])
        self.evidence_pack["riss"]                  = evidence_results.get("riss", [])

        evidence_path  = self.session_dir / "EvidencePack.json"
        tool_log_path  = self.session_dir / "ToolLog.json"
        validation_warnings = self._validate_evidence_pack(self.evidence_pack)
        if validation_warnings:
            self.evidence_pack["validation_warnings"] = validation_warnings
            self._log_tool("evidence_pack_schema", "EvidencePack 최소 스키마 점검", "경고", "; ".join(validation_warnings[:5]))
        self._save_json(self.evidence_pack, evidence_path)
        self._save_json({"session_id": self.session_id, "log": self.tool_log}, tool_log_path)

        s2_count = len(self.evidence_pack["semantic_scholar"])
        gs_count = len(self.evidence_pack["google_scholar"])
        labs_count = len(self.evidence_pack["google_scholar_labs"])
        quick_count = len(self.evidence_pack["google_scholar_quick"])
        ixtheo_count = len(self.evidence_pack["ixtheo"])
        crossref_count = len(self.evidence_pack["crossref_journal"])
        kci_count = len(self.evidence_pack["kci"])
        riss_count = len(self.evidence_pack["riss"])
        print(f"\n✅ [Phase 0 완료] 산출물 저장 위치: {self.session_dir}")
        print(f"   - QuerySet.json  ({len(query_set['queries'])}개 쿼리)")
        print(f"   - EvidencePack.json (S2 API: {s2_count}건 / Labs: {labs_count}건 / Quick: {quick_count}건 / IxTheo: {ixtheo_count}건 / Crossref: {crossref_count}건 / KCI: {kci_count}건 / RISS: {riss_count}건 / GS 합계: {gs_count}건 / 전체: {len(self.evidence_pack['abstracts'])}건)")
        print(f"   - ToolLog.json")

        return {
            "query_set":     query_set,
            "evidence_pack": self.evidence_pack,
            "session_dir":   str(self.session_dir)
        }

    # S2 API 도메인 필터 — 신학·종교학·철학 분야만 허용하여 법률/의학 논문 유입 차단
    S2_FIELDS_OF_STUDY = "Philosophy,Religious Studies"

    def _as_semantic_question(self, topic: str, template: str = "recent_scholarship") -> str:
        """Google Scholar Labs용 키워드 백을 자연어 연구 질문으로 변환."""
        clean_topic = re.sub(r"\s+", " ", topic or "").strip().rstrip(".")
        if not clean_topic:
            clean_topic = self.target_file.stem

        lower = clean_topic.lower()
        starters = (
            "how ", "what ", "which ", "when ", "where ", "why ", "whether ",
            "does ", "do ", "did ", "is ", "are ", "was ", "were ",
            "has ", "have ", "can ", "could ", "should ", "would ",
            "to what extent ", "in what ways ",
        )
        if clean_topic.endswith("?") or lower.startswith(starters):
            return clean_topic if clean_topic.endswith("?") else f"{clean_topic}?"

        if template == "debate":
            return f"What are the main scholarly debates about {clean_topic}?"
        if template == "relationship":
            return f"How do scholars explain the relationship between {clean_topic}?"
        if template == "recent":
            return f"Which recent studies support or challenge claims about {clean_topic}?"
        return f"What does recent scholarship say about {clean_topic}?"

    def _generate_query_set(self, paper_text: str) -> dict:
        """
        논문 텍스트에서 핵심 용어를 추출하여 QuerySet 생성.
        
        v10.5 개선:
        - Google Scholar Labs는 키워드 백보다 문장형/의문문형 쿼리에 최적화
        - 따옴표 구문 추출 시 각주/독일어/법률 용어를 필터링
        - 영어 자연어 연구 질문을 우선 생성
        - 파일명 기반 fallback도 의문문 형태로 구성
        """
        # 1단계: 파일명에서 영어 자연어 쿼리 생성 (가장 안정적)
        stem = self.target_file.stem
        # 괄호, 하이픈, 언더스코어 정리
        clean_stem = re.sub(r'[\(\)\[\]]', '', stem)
        clean_stem = clean_stem.replace("_", " ").replace("-", " ").strip()
        # 한국어 파일명이면 영어 키워드로 변환 시도
        has_korean = bool(re.search(r'[가-힣]', clean_stem))
        
        queries = []
        
        # 2단계: 논문 텍스트에서 신학 핵심어 추출 (따옴표 구문 대신 선별적 추출)
        # 히브리어/그리스어 전사 패턴 (실제 신학 용어)
        theological_terms = re.findall(
            r'\b(šabb[aā]t(?:ôn)?|Holiness Code|Priestly|Deuteronomic|Leviticus|Pentateuch|'
            r'pistis|δικαιοσύνη|χάρις|Sabbath|Jubilee|covenant|atonement|'
            r'언약|칭의|성화|종말론|해석학|안식일|안식년|희년|성결)\b',
            paper_text[:8000], re.IGNORECASE
        )
        # 빈도 상위 3개 선택
        from collections import Counter
        term_counts = Counter(t.lower() for t in theological_terms)
        top_terms = [t for t, _ in term_counts.most_common(5)]
        
        # 3단계: 영어 자연어 쿼리 조합 (S2 API ML 리랭커 최적화)
        if top_terms:
            primary_topic = " and ".join(top_terms[:3])
            queries.append(self._as_semantic_question(primary_topic, "recent_scholarship"))
            if len(top_terms) >= 4:
                relationship_topic = " and ".join(top_terms[2:5])
                queries.append(self._as_semantic_question(relationship_topic, "relationship"))
        
        # 4단계: 파일명 기반 영어 자연어 fallback
        if has_korean:
            # 한국어 파일명 → 영어 학술 쿼리로 변환
            # 일반적인 한국어 신학 용어 → 영어 매핑
            kr_en_map = {
                '안식일': 'Sabbath', '안식년': 'Sabbatical year', '희년': 'Jubilee',
                '성결': 'Holiness', '성결 학파': 'Holiness Code', '거룩한': 'sacred holy',
                '레위기': 'Leviticus', '오경': 'Pentateuch', '편집': 'redaction',
                '학파': 'school source', '시간': 'time', '틀': 'framework',
                '신학': 'theology', '구약': 'Old Testament', '제의': 'ritual cult',
            }
            en_parts = []
            for kr, en in kr_en_map.items():
                if kr in clean_stem:
                    en_parts.append(en)
            if en_parts:
                topic = " ".join(en_parts[:4])
                queries.append(self._as_semantic_question(topic, "recent_scholarship"))
                queries.append(self._as_semantic_question(topic, "debate"))
        else:
            queries.append(self._as_semantic_question(clean_stem, "recent_scholarship"))
        
        # 5단계: 최소 3개 보장
        if len(queries) < 3:
            queries.extend([
                self._as_semantic_question(clean_stem, "debate"),
                self._as_semantic_question(clean_stem, "recent")
            ])

        # 중복 제거 + 최대 5개
        unique_queries = list(dict.fromkeys(queries))[:5]
        
        return {
            "session_id":  self.session_id,
            "target_file": self.target_file.name,
            "queries":     unique_queries,
            "generated_at": datetime.now().isoformat(),
            "query_form": "natural_language_interrogative_preferred",
            "manual_input_required": not GS_SEMANTIC_CFG.get("enabled", False),
            "instructions": "Google Scholar Labs는 키워드 나열보다 문장형 연구 질문, 특히 의문문에 최적화되어 있습니다. google-scholar-semantic 스킬이 TRE 기반 독일어/영어/고전어 확장을 질문 문장 안에 주입합니다."
        }

    def _try_evidence_sources(self, query_set: dict) -> dict:
        """
        v10.5 삼중 증거 수집:
          (1) Semantic Scholar API (s2_runner.py) — 구조화된 메타데이터
          (2) Google Scholar Labs — AI 시맨틱 맥락 및 최신 논쟁 지형
          (3) google-scholar-quick Google Scholar — 경량 보완 검색
        """
        results = {
            "abstracts":             [],   # 통합 초록 목록 (Phase 1/2 공용)
            "provenance":            [],   # 출처 추적 로그
            "semantic_scholar":      [],   # S2 API 전용 결과
            "google_scholar_labs":   [],   # Scholar Labs 전용 결과
            "google_scholar_quick":  [],   # google-scholar-quick 전용 결과
            "google_scholar":        [],   # Google Scholar 계열 통합 결과
            "ixtheo":                [],   # IxTheo 전용 결과
            "crossref_journal":      [],   # Crossref 전용 결과
        }

        # --- (1) Semantic Scholar API ---
        s2_items = []
        if S2_CFG.get("enabled", True):
            print("  🔬 [S2 API] Semantic Scholar 검색 중...")
            s2_items = self._run_s2_api(query_set)
        else:
            self._log_tool("s2_api", "config 확인", "비활성화됨", "")
        results["semantic_scholar"] = s2_items
        results["abstracts"].extend(s2_items)
        results["provenance"].append({
            "tool": "semantic_scholar_api",
            "hit_count": len(s2_items)
        })

        # --- (2) Google Scholar Labs (google-scholar-semantic) ---
        labs_items = []
        if GS_SEMANTIC_CFG.get("enabled", False):
            print("  🧭 [Google Scholar Labs] google-scholar-semantic 실행 중...")
            labs_items = self._run_google_scholar_semantic(query_set)
        else:
            self._log_tool("google_scholar_semantic", "config 확인", "비활성화됨", "")
        results["google_scholar_labs"] = labs_items
        results["google_scholar"].extend(labs_items)
        results["abstracts"].extend(labs_items)
        results["provenance"].append({
            "tool": "google_scholar_semantic_labs",
            "hit_count": len(labs_items)
        })

        # --- (3) Google Scholar CDP (google-scholar-quick) ---
        # Phase 0에서는 쿼리당 1회 배치 검색만 수행 (개별 주장 검증은 Phase 2에서)
        quick_items = []
        if SCHOLAR_QUICK_CFG.get("enabled", True):
            print("  📚 [Google Scholar] google-scholar-quick 배치 검색 중...")
            quick_items = self._run_google_scholar_quick_batch(query_set)
        else:
            self._log_tool("google_scholar_quick_batch", "config 확인", "비활성화됨", "")
        results["google_scholar_quick"] = quick_items
        results["google_scholar"].extend(quick_items)
        results["abstracts"].extend(quick_items)
        results["provenance"].append({
            "tool": "google_scholar_quick",
            "hit_count": len(quick_items)
        })

        # --- (4) Tübingen Index Theologicus (ixtheo-searcher) ---
        ixtheo_items = []
        if IXTHEO_CFG.get("enabled", True):
            print("  🧭 [IxTheo] Tübingen Index Theologicus 검색 중...")
            ixtheo_items = self._run_ixtheo_searcher(query_set)
        else:
            self._log_tool("ixtheo_searcher", "config 확인", "비활성화됨", "")
        results["ixtheo"] = ixtheo_items
        results["abstracts"].extend(ixtheo_items)
        results["provenance"].append({
            "tool": "ixtheo_searcher",
            "hit_count": len(ixtheo_items)
        })

        # --- (5) Crossref Premium Theology Journal (crossref-journal-searcher) ---
        crossref_items = []
        if CROSSREF_CFG.get("enabled", True):
            print("  📚 [Crossref Journal] Premium 저널 검색 중...")
            crossref_items = self._run_crossref_journal_searcher(query_set)
        else:
            self._log_tool("crossref_journal_searcher", "config 확인", "비활성화됨", "")
        results["crossref_journal"] = crossref_items
        results["abstracts"].extend(crossref_items)
        results["provenance"].append({
            "tool": "crossref_journal_searcher",
            "hit_count": len(crossref_items)
        })

        # --- (6) KCI (kci-api-searcher) ---
        kci_items = []
        if KCI_CFG.get("enabled", True):
            print("  🇰🇷 [KCI] 한국학술지인용색인 검색 중...")
            kci_items = self._run_kci_searcher(query_set)
        else:
            self._log_tool("kci_searcher", "config 확인", "비활성화됨", "")
        results["kci"] = kci_items
        results["abstracts"].extend(kci_items)
        results["provenance"].append({
            "tool": "kci_searcher",
            "hit_count": len(kci_items)
        })

        # --- (7) RISS (riss-searcher) ---
        riss_items = []
        if RISS_CFG.get("enabled", True):
            print("  🇰🇷 [RISS] 학술연구정보서비스 검색 중...")
            riss_items = self._run_riss_searcher(query_set)
        else:
            self._log_tool("riss_searcher", "config 확인", "비활성화됨", "")
        results["riss"] = riss_items
        results["abstracts"].extend(riss_items)
        results["provenance"].append({
            "tool": "riss_searcher",
            "hit_count": len(riss_items)
        })

        return results

    def _run_google_scholar_semantic(self, query_set: dict) -> list[dict]:
        """
        Google Scholar Labs 배치 검색.
        google-scholar-semantic/scripts/scholar_runner.py를 호출해 Labs HTML을 수집하고
        표준 JSONL을 EvidencePack 항목으로 편입한다.
        """
        if not GS_SEMANTIC_RUNNER.exists():
            self._log_tool("google_scholar_semantic", "러너 확인", "scholar_runner.py 미발견", str(GS_SEMANTIC_RUNNER))
            print(f"  ⚠️  Scholar Labs 러너 미발견: {GS_SEMANTIC_RUNNER}")
            return []

        if GS_SEMANTIC_CFG.get("require_tty", True) and not sys.stdin.isatty():
            self._log_tool(
                "google_scholar_semantic",
                "대화형 브라우저 확인",
                "TTY가 아니어서 자동 브라우저 실행 보류",
                "config.google_scholar_semantic.require_tty=true"
            )
            print("  ⚠️  Google Scholar Labs는 로그인/브라우저 상호작용이 필요해 비대화형 실행에서는 보류했습니다.")
            return []

        output_dir = self.session_dir / "google_scholar_labs"
        output_dir.mkdir(parents=True, exist_ok=True)
        query_set_path = self.session_dir / "QuerySet.json"
        query_set_path.write_text(json.dumps(query_set, ensure_ascii=False, indent=2), encoding="utf-8")

        jsonl_path = output_dir / "scholar_labs.jsonl"
        max_queries = int(GS_SEMANTIC_CFG.get("max_queries", 6))
        results_per_query = int(GS_SEMANTIC_CFG.get("results_per_query", 10))
        max_queries_per_session = min(4, max(1, int(GS_SEMANTIC_CFG.get("max_queries_per_session", 4))))
        citation_depth = GS_SEMANTIC_CFG.get("citation_depth", "all")
        wait_seconds = int(GS_SEMANTIC_CFG.get("wait_seconds", 40))
        timeout_seconds = int(GS_SEMANTIC_CFG.get("timeout_seconds", max(300, max_queries * (wait_seconds + 45))))
        domain = GS_SEMANTIC_CFG.get("domain", "theology")
        tre_expand = bool(GS_SEMANTIC_CFG.get("tre_expand", True))

        cmd = [
            sys.executable,
            str(GS_SEMANTIC_RUNNER),
            "--query-file", str(query_set_path),
            "--output-dir", str(output_dir),
            "--jsonl", str(jsonl_path),
            "--max-queries", str(max_queries),
            "--max-results", str(results_per_query),
            "--max-queries-per-session", str(max_queries_per_session),
            "--citation-depth", str(citation_depth),
            "--wait-seconds", str(wait_seconds),
            "--domain", str(domain),
        ]
        if tre_expand:
            cmd.append("--tre-expand")
        if GS_SEMANTIC_CFG.get("headless", False):
            cmd.append("--headless")

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
            self._log_tool(
                "google_scholar_semantic",
                "Scholar Labs 배치 실행",
                f"returncode={proc.returncode}",
                (proc.stderr or proc.stdout)[-300:]
            )
        except subprocess.TimeoutExpired as e:
            self._log_tool("google_scholar_semantic", "Scholar Labs 배치 실행", "타임아웃", str(e)[:200])
            return []
        except Exception as e:
            self._log_tool("google_scholar_semantic", "Scholar Labs 배치 실행", "예외", str(e)[:200])
            return []

        if not jsonl_path.exists():
            self._log_tool("google_scholar_semantic", "JSONL 확인", "결과 없음", str(jsonl_path))
            return []

        items = []
        for line in jsonl_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            item["source_tool"] = "google_scholar_semantic"
            item["abstract"] = item.get("snippet", "")
            items.append(item)

        self._log_tool(
            "google_scholar_semantic",
            "JSONL 파싱",
            f"{len(items)}건 수집",
            str(jsonl_path)
        )
        print(f"     → Scholar Labs 총 {len(items)}건 수집")
        return items

    def _run_s2_api(self, query_set: dict) -> list[dict]:
        """
        Semantic Scholar API 배치 검색.
        s2_runner.py를 --format json 모드로 호출하여 구조화된 결과 반환.
        """
        if not S2_RUNNER.exists():
            self._log_tool("s2_api", "스크립트 확인", "s2_runner.py 미발견", str(S2_RUNNER))
            print(f"  ⚠️  S2 러너 미발견: {S2_RUNNER}")
            return []

        max_queries = int(S2_CFG.get("max_queries", 3))
        results_per_query = int(S2_CFG.get("results_per_query", 5))

        all_results = []
        for query in query_set["queries"][:max_queries]:
            try:
                proc = subprocess.run(
                    [sys.executable, str(S2_RUNNER),
                     "--query", query, "--limit", str(results_per_query), "--format", "json",
                     "--fields", self.S2_FIELDS_OF_STUDY],
                    capture_output=True, text=True, timeout=30
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    data = json.loads(proc.stdout)
                    papers = data.get("results", [])
                    all_results.extend(papers)
                    self._log_tool(
                        "s2_api",
                        f"쿼리: {query}",
                        f"{len(papers)}건 수집",
                        ""
                    )
                else:
                    self._log_tool("s2_api", f"쿼리: {query}", "실패 또는 빈 응답", proc.stderr[:200])
            except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
                self._log_tool("s2_api", f"쿼리: {query}", "예외", str(e)[:200])
            except Exception as e:
                self._log_tool("s2_api", f"쿼리: {query}", "예상 외 예외", str(e)[:200])

        print(f"     → S2 API 총 {len(all_results)}건 수집")
        return all_results

    def _run_google_scholar_quick_batch(self, query_set: dict) -> list[dict]:
        """
        Phase 0 배치용 Google Scholar 검색.
        google-scholar-quick을 쿼리당 1회 실행하여 간이 결과 확보.
        """
        if not SCHOLAR_QUICK_SH.exists():
            self._log_tool("google_scholar_quick_batch", "CLI 확인", "스크립트 없음", str(SCHOLAR_QUICK_SH))
            return []

        max_queries = int(SCHOLAR_QUICK_CFG.get("max_queries", 2))
        results_per_query = int(SCHOLAR_QUICK_CFG.get("results_per_query", 3))

        all_results = []
        for query in query_set["queries"][:max_queries]:
            try:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    proc = subprocess.run(
                        ["zsh", str(SCHOLAR_QUICK_SH), query, tmp_dir],
                        capture_output=True, text=True, timeout=25
                    )
                    paper_files = list(Path(tmp_dir).glob("papers_*.json"))
                    if paper_files:
                        raw = paper_files[0].read_text(encoding="utf-8", errors="ignore").strip()
                        if raw and raw not in ("null", "[]"):
                            papers = json.loads(raw)
                            if isinstance(papers, list):
                                all_results.extend(papers[:results_per_query])
                                self._log_tool("google_scholar_quick_batch", f"쿼리: {query}",
                                               f"{len(papers)}건 수집", "")
            except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
                self._log_tool("google_scholar_quick_batch", f"쿼리: {query}", "예외", str(e)[:100])

        print(f"     → Google Scholar 총 {len(all_results)}건 수집")
        return all_results

    def _run_ixtheo_searcher(self, query_set: dict) -> list[dict]:
        """Tübingen Index Theologicus (IxTheo) 검색 러너 호출"""
        if not IXTHEO_RUNNER.exists():
            self._log_tool("ixtheo_searcher", "스크립트 확인", "ixtheo_searcher.py 미발견", str(IXTHEO_RUNNER))
            print(f"  ⚠️  IxTheo 러너 미발견: {IXTHEO_RUNNER}")
            return []

        max_queries = int(IXTHEO_CFG.get("max_queries", 2))
        results_per_query = int(IXTHEO_CFG.get("results_per_query", 5))

        all_results = []
        for query in query_set["queries"][:max_queries]:
            try:
                proc = subprocess.run(
                    [sys.executable, str(IXTHEO_RUNNER),
                     "--query", query, "--limit", str(results_per_query), "--format", "json"],
                    capture_output=True, text=True, timeout=40
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    papers = json.loads(proc.stdout)
                    if isinstance(papers, list):
                        for p in papers:
                            p["source_tool"] = "ixtheo_searcher"
                        all_results.extend(papers)
                        self._log_tool("ixtheo_searcher", f"쿼리: {query}", f"{len(papers)}건 수집", "")
                else:
                    self._log_tool("ixtheo_searcher", f"쿼리: {query}", "실패 또는 빈 응답", proc.stderr[:200])
            except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
                self._log_tool("ixtheo_searcher", f"쿼리: {query}", "예외", str(e)[:100])

        print(f"     → IxTheo 총 {len(all_results)}건 수집")
        return all_results

    def _run_crossref_journal_searcher(self, query_set: dict) -> list[dict]:
        """Crossref Premium Theology Journal Searcher 러너 호출"""
        if not CROSSREF_RUNNER.exists():
            self._log_tool("crossref_journal_searcher", "스크립트 확인", "crossref_journal_searcher.py 미발견", str(CROSSREF_RUNNER))
            print(f"  ⚠️  Crossref 러너 미발견: {CROSSREF_RUNNER}")
            return []

        max_queries = int(CROSSREF_CFG.get("max_queries", 2))
        results_per_query = int(CROSSREF_CFG.get("results_per_query", 5))

        all_results = []
        for query in query_set["queries"][:max_queries]:
            try:
                proc = subprocess.run(
                    [sys.executable, str(CROSSREF_RUNNER),
                     "--query", query, "--limit", str(results_per_query), "--format", "json"],
                    capture_output=True, text=True, timeout=40
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    papers = json.loads(proc.stdout)
                    if isinstance(papers, list):
                        for p in papers:
                            p["source_tool"] = "crossref_journal_searcher"
                        all_results.extend(papers)
                        self._log_tool("crossref_journal_searcher", f"쿼리: {query}", f"{len(papers)}건 수집", "")
                else:
                    self._log_tool("crossref_journal_searcher", f"쿼리: {query}", "실패 또는 빈 응답", proc.stderr[:200])
            except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
                self._log_tool("crossref_journal_searcher", f"쿼리: {query}", "예외", str(e)[:100])

        print(f"     → Crossref Journal 총 {len(all_results)}건 수집")
        return all_results

    def _clean_korean_academic_query(self, query: str) -> str:
        """KCI/RISS 최적화: 영어 의문문/학술형 문장 성분을 걷어내고 명사 조각만 남긴다."""
        lower = query.lower()
        # 학술 의문사/조사 걷어내기
        for stopword in [
            "what are the main scholarly debates about",
            "what does recent scholarship say about",
            "how do scholars explain the relationship between",
            "which recent studies support or challenge claims about",
            "recent scholarship", "scholarly debates", "explain the relationship",
            "what ", "how ", "which ", "when ", "where ", "why ", "whether ",
            "does ", "do ", "did ", "is ", "are ", "was ", "were ",
            "has ", "have ", "can ", "could ", "should ", "would ",
            "to what extent ", "in what ways ", "about ", "recent ", "studies ", "claims "
        ]:
            lower = lower.replace(stopword, " ")
        # 물음표 및 특수문자 제거
        lower = lower.replace("?", " ").replace("!", " ").replace(".", " ")
        cleaned = re.sub(r'\s+', ' ', lower).strip()
        if not cleaned:
            cleaned = self.target_file.stem
            # 파일명에 포함된 불필요한 확장자, 괄호 등 제거
            cleaned = re.sub(r'[\(\)\[\]\-_]', ' ', cleaned)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def _run_kci_searcher(self, query_set: dict) -> list[dict]:
        """KCI (한국학술지인용색인) search.py 호출"""
        if not KCI_RUNNER.exists():
            self._log_tool("kci_searcher", "스크립트 확인", "search.py 미발견", str(KCI_RUNNER))
            print(f"  ⚠️  KCI 러너 미발견: {KCI_RUNNER}")
            return []

        max_queries = int(KCI_CFG.get("max_queries", 2))
        results_per_query = int(KCI_CFG.get("results_per_query", 5))

        all_results = []
        for query in query_set["queries"][:max_queries]:
            cleaned_query = self._clean_korean_academic_query(query)
            try:
                proc = subprocess.run(
                    [sys.executable, str(KCI_RUNNER),
                     cleaned_query, "--limit", str(results_per_query), "--output", "json"],
                    capture_output=True, text=True, timeout=60, cwd=str(KCI_RUNNER.parent)
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    data = json.loads(proc.stdout)
                    papers = data.get("results", [])
                    if isinstance(papers, list):
                        for p in papers:
                            p["source_tool"] = "kci_searcher"
                        all_results.extend(papers)
                        self._log_tool("kci_searcher", f"쿼리: {cleaned_query}", f"{len(papers)}건 수집", "")
                else:
                    self._log_tool("kci_searcher", f"쿼리: {cleaned_query}", "실패 또는 빈 응답", proc.stderr[:200])
            except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
                self._log_tool("kci_searcher", f"쿼리: {cleaned_query}", "예외", str(e)[:100])

        print(f"     → KCI 총 {len(all_results)}건 수집")
        return all_results

    def _run_riss_searcher(self, query_set: dict) -> list[dict]:
        """RISS (학술연구정보서비스) search.py 호출"""
        if not RISS_RUNNER.exists():
            self._log_tool("riss_searcher", "스크립트 확인", "search.py 미발견", str(RISS_RUNNER))
            print(f"  ⚠️  RISS 러너 미발견: {RISS_RUNNER}")
            return []

        max_queries = int(RISS_CFG.get("max_queries", 2))
        results_per_query = int(RISS_CFG.get("results_per_query", 5))

        all_results = []
        for query in query_set["queries"][:max_queries]:
            cleaned_query = self._clean_korean_academic_query(query)
            try:
                proc = subprocess.run(
                    [sys.executable, str(RISS_RUNNER),
                     cleaned_query, "--limit", str(results_per_query), "--output", "json"],
                    capture_output=True, text=True, timeout=60, cwd=str(RISS_RUNNER.parent)
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    data = json.loads(proc.stdout)
                    papers = data.get("results", [])
                    if isinstance(papers, list):
                        for p in papers:
                            p["source_tool"] = "riss_searcher"
                        all_results.extend(papers)
                        self._log_tool("riss_searcher", f"쿼리: {cleaned_query}", f"{len(papers)}건 수집", "")
                else:
                    self._log_tool("riss_searcher", f"쿼리: {cleaned_query}", "실패 또는 빈 응답", proc.stderr[:200])
            except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
                self._log_tool("riss_searcher", f"쿼리: {cleaned_query}", "예외", str(e)[:100])

        print(f"     → RISS 총 {len(all_results)}건 수집")
        return all_results

    # ──────────────────────────────────────────────
    # Phase 1: Unified Review 오케스트레이션
    # ──────────────────────────────────────────────

    def prepare_pass1(self, evidence_session_dir: str = "") -> dict:
        """
        Phase 1: EvidencePack + unified_review 프롬프트 → 8차원 리뷰 실행 패키지 구성

        실제 LLM 호출은 에이전트가 수행하므로,
        여기서는 프롬프트 + 인풋을 패키징하여 핸드오프 패킷 생성.
        """
        print(f"\n🚀 [Phase 1] 통합 리뷰 패키지 구성 중...")

        review_prompt = self.load_prompt("unified_review")
        annotation_tokens = json.loads(
            (CONFIG_DIR / "annotation_tokens.json").read_text(encoding="utf-8")
        )

        # EvidencePack 로드 (session_dir 제공 시)
        evidence = {}
        if evidence_session_dir:
            ep_path = Path(evidence_session_dir) / "EvidencePack.json"
            if ep_path.exists():
                evidence = json.loads(ep_path.read_text(encoding="utf-8"))
                print(f"  ✅ EvidencePack 로드: {len(evidence.get('abstracts', []))}건의 초록")

        # 핸드오프 패킷 구성
        handoff_packet = {
            "session_id":       self.session_id,
            "target_file":      str(self.target_file),
            "prompt":           review_prompt,
            "annotation_tokens": annotation_tokens["tokens"],
            "evidence_pack":    evidence,
            "execution_guide": {
                "step_1": f"'{self.target_file.name}'을 분석 대상으로 설정",
                "step_2": "prompts/unified_review.json.md의 8섹션(I~VIII) 순서로 분석 수행",
                "step_3": "annotation_tokens.json의 must 토큰 모두 포함",
                "step_4": f"결과를 {REVIEW_REPORTS_DIR / self.session_id}_review.md 에 저장"
            }
        }

        # 패킷 저장
        packet_path = self.session_dir / "handoff_packet.json"
        self._save_json(handoff_packet, packet_path)
        print(f"  ✅ 핸드오프 패킷 생성: {packet_path}")
        print(f"\n✅ [Phase 1 완료] 에이전트에 전달 준비 완료")

        return handoff_packet

    # ──────────────────────────────────────────────
    # Phase 2: Dialectical Verification
    # ──────────────────────────────────────────────

    def prepare_pass2(self,
                      phase1_review_path: str,
                      evidence_session_dir: str = "") -> dict:
        """
        Phase 2: Dialectical Verification

        5단계 변증법적 검증 파이프라인:
          ① Claim Extraction   — 리뷰의 모든 사실적 주장 파싱
          ② Triangulated Verify — 원본 역참조 + google-scholar-quick + (EvidencePack 보너스)
          ③ Adversarial Recon  — 비평 포인트별 저자 진영 최강 반격 구성 및 돌파 여부 판정
          ④ Confidence Calibrate — Anchored / Unverified / Contradicted 자동 라벨링
          ⑤ Selective Regen    — ❌ 섹션만 외과적 재작성 + 투명성 보고 생성
        """
        print(f"\n🚀 [Phase 2] 변증법적 검증 시작")

        review_path = Path(phase1_review_path)
        if not review_path.exists():
            raise FileNotFoundError(f"Phase 1 리뷰 원고를 찾을 수 없습니다: {phase1_review_path}")

        review_text = review_path.read_text(encoding="utf-8")

        paper_text = self._load_target_text("Phase 2")

        # EvidencePack 로드 (있으면 보너스 축 활성화)
        evidence_pack = {}
        if evidence_session_dir:
            ep_path = Path(evidence_session_dir) / "EvidencePack.json"
            if ep_path.exists():
                evidence_pack = json.loads(ep_path.read_text(encoding="utf-8"))
                print(f"  📦 EvidencePack 로드됨 (보너스 축 활성화): {len(evidence_pack.get('abstracts', []))}건 초록")

        # ① Claim Extraction
        print("\n  ① 사실적 주장 추출 중...")
        claims = self._extract_claims(review_text)
        print(f"     → {len(claims)}건 추출 (인용: {sum(1 for c in claims if c['type']=='citation')}건, "
              f"주장: {sum(1 for c in claims if c['type']=='assertion')}건, "
              f"해석: {sum(1 for c in claims if c['type']=='interpretation')}건)")

        # ② Triangulated Verification
        print("\n  ② 삼각 검증 실행 중...")
        verified_claims = self._triangulate_verify(
            claims, review_text, paper_text, evidence_pack
        )

        # ③ Adversarial Reconstruction
        print("\n  ③ 적대적 재구성 실행 중...")
        critique_results = self._adversarial_reconstruct(review_text)

        # ④ Confidence Calibration
        print("\n  ④ 신뢰도 교정 중...")
        calibration = self._calibrate_confidence(verified_claims)

        # ⑤ Transparency Report 생성
        print("\n  ⑤ 투명성 보고서 생성 중...")
        transparency_report = self._generate_transparency_report(
            calibration, critique_results, verified_claims
        )

        # Phase 2 패킷 저장
        p2_dir = self.session_dir / "phase2"
        p2_dir.mkdir(parents=True, exist_ok=True)

        claims_path = p2_dir / "verified_claims.json"
        report_path = p2_dir / "transparency_report.md"
        packet_path = p2_dir / "p2_handoff_packet.json"

        self._save_json({
            "session_id": self.session_id,
            "claims": verified_claims,
            "critique_results": critique_results,
            "calibration_summary": calibration["summary"]
        }, claims_path)

        report_path.write_text(transparency_report, encoding="utf-8")
        print(f"  ✅ 저장 완료: {report_path}")

        # ❌ 재작성 필요 섹션 목록 생성
        contradicted = [c for c in verified_claims if c["verdict"] == "Contradicted"]
        sections_to_rewrite = list({c["section"] for c in contradicted})

        p2_handoff = {
            "session_id":            self.session_id,
            "phase1_review":         str(review_path),
            "transparency_report":   transparency_report,
            "sections_to_rewrite":   sections_to_rewrite,
            "calibration_summary":   calibration["summary"],
            "critique_results":      critique_results,
            "execution_guide": {
                "step_0": "보고서 최상단(제목 직후)에 [📋 Executive Summary] 섹션 배치 (강점/약점/종합등급/반격문헌 요약 테이블 포함)",
                "step_1": "sections_to_rewrite 목록의 섹션들을 검증 결과를 반영하여 재작성",
                "step_2": "재작성 시 Contradicted 주장에 해당하는 [Evidence_Missing] 태그 유지",
                "step_3": "최종 리뷰 맨 끝에 transparency_report 전문 첨부 (Phase 2 검증 결과)",
                "step_4": f"완성본을 {REVIEW_REPORTS_DIR / self.session_id}_final_review.md 에 저장"
            }
        }
        self._save_json(p2_handoff, packet_path)

        # 콘솔 요약
        s = calibration["summary"]
        print(f"\n✅ [Phase 2 완료]")
        print(f"   총 주장: {s['total']}건")
        print(f"   ✅ Anchored:     {s['anchored']}건 ({s['anchored_pct']:.0f}%)")
        print(f"   ⚠️  Unverified:  {s['unverified']}건 ({s['unverified_pct']:.0f}%)")
        print(f"   ❌ Contradicted: {s['contradicted']}건 ({s['contradicted_pct']:.0f}%)")
        print(f"   📝 재작성 섹션: {sections_to_rewrite or ['없음']}")

        return p2_handoff

    # ── Phase 2 내부 헬퍼 ──────────────────────────

    def _extract_claims(self, review_text: str) -> list[dict]:
        """
        리뷰 텍스트에서 사실적 주장(citation / assertion / interpretation)을 파싱.

        실제 프로덕션에서는 LLM 호출로 대체 — 현재는 패턴 기반 추출.
        """
        claims = []
        claim_id = 0

        # 현재 섹션 추적
        current_section = "preamble"
        section_pattern = re.compile(r"^#{1,3}\s+(I{1,3}V?|V?I{0,3}|\d+)\.?\s+.+", re.MULTILINE)

        # 패턴별 추출
        citation_patterns = [
            # "저자(연도)" 또는 "저자 연도" 형태
            (r'([A-Z][a-zäöüáéí]+(?:\s+[A-Z][a-zäöüáéí]+)?)\s*\((\d{4}[a-z]?)\)',
             "citation"),
            # 「따옴표」 형 인용
            (r'「([^」]{5,80})」', "citation"),
        ]
        assertion_patterns = [
            (r'([A-Z][a-zäöü]+(?:\s+[A-Z][a-zäöü]+)?)는\s+[^.]{10,100}(라고|고|며|다고)\s+주장', "assertion"),
            (r'(대부분의|많은|최근) 학자들?[은이가]\s+[^.]{10,100}', "assertion"),
            (r'학계에서[는]?\s+[^.]{10,100}(합의|통설|정설)', "assertion"),
        ]
        interpretation_patterns = [
            (r'이\s+(구절|본문|텍스트)[은이가]\s+[^.]{10,100}(의미|가리키|나타내|시사)', "interpretation"),
            (r'(πίστις|δικαιοσύνη|λόγος|[가-힣]{2,6})는?\s+[^.]{10,80}(뜻|의미|번역)', "interpretation"),
        ]

        # v10 Token Patterns (ARC Protocol)
        token_patterns = [
            (r'\[primary_source_anchor\]\s*([^\n]+)', "citation"),
            (r'\[HypothesisArena\]\s*([^\n]+)', "assertion"),
            (r'\[Conclusion\]\s*([^\n]+)', "assertion"),
            (r'\[Critique\]\s*([^\n]+)', "interpretation"),
            (r'\[Defense\]\s*([^\n]+)', "interpretation"),
        ]

        all_patterns = citation_patterns + assertion_patterns + interpretation_patterns + token_patterns

        for pat, claim_type in all_patterns:
            for m in re.finditer(pat, review_text):
                claim_id += 1
                # 주변 문맥 추출 (매치 앞뒤 50자)
                start = max(0, m.start() - 30)
                end   = min(len(review_text), m.end() + 50)
                context = review_text[start:end].replace("\n", " ")

                # 섹션 위치 추정 (매치 위치 이전의 마지막 헤더)
                section_matches = list(section_pattern.finditer(review_text[:m.start()]))
                if section_matches:
                    current_section = section_matches[-1].group(0).strip()

                claims.append({
                    "id":           f"C-{claim_id:03d}",
                    "raw_match":    m.group(0),
                    "context":      context,
                    "type":         claim_type,
                    "section":      current_section,
                    "verifiable":   True,
                    "verdict":      None,   # ④에서 채워짐
                    "verify_source": None,  # ②에서 채워짐
                    "evidence_missing": False
                })

        # 중복 제거 (같은 raw_match)
        seen = set()
        unique_claims = []
        for c in claims:
            if c["raw_match"] not in seen:
                seen.add(c["raw_match"])
                unique_claims.append(c)

        return unique_claims

    def _triangulate_verify(self,
                            claims: list[dict],
                            review_text: str,
                            paper_text: str,
                            evidence_pack: dict) -> list[dict]:
        """
        ② 삼각 검증:
          Axis 1 — 원본 논문 역참조 (항상)
          Axis 2 — google-scholar-quick Google Scholar CDP (인용 타입)
          Axis Bonus — EvidencePack 교차 (있는 경우)
        """
        for claim in claims:
            sources_used = []

            # Axis 1: 원본 논문 역참조
            found_in_paper = self._check_paper_anchor(claim, paper_text)
            if found_in_paper:
                claim["verdict"]      = "Anchored"
                claim["verify_source"] = "원본_논문"
                sources_used.append("axis_1_paper")

            # Axis 2: google-scholar-quick Google Scholar (인용 타입이고 아직 미검증인 경우)
            if claim["type"] == "citation" and claim["verdict"] != "Anchored":
                sq_result = self._run_google_scholar_quick(claim)
                if sq_result["found"]:
                    claim["verdict"]       = "Anchored"
                    claim["verify_source"] = "google_scholar_quick"
                    claim["scholar_data"]  = sq_result["data"]
                    sources_used.append("axis_2_google_scholar")
                elif sq_result["searched"]:
                    sources_used.append("axis_2_google_scholar")

            # Axis 3: Semantic Scholar API (Axis 2에서도 미검증된 인용 타입만)
            if claim["type"] == "citation" and claim["verdict"] != "Anchored":
                s2_result = self._run_s2_verify(claim)
                if s2_result["found"]:
                    claim["verdict"]       = "Anchored"
                    claim["verify_source"] = "semantic_scholar_api"
                    claim["s2_data"]       = s2_result["data"]
                    sources_used.append("axis_3_s2_api")
                elif s2_result["searched"]:
                    claim["verdict"]       = "Unverified"
                    claim["verify_source"] = "both_scholar_miss"
                    claim["evidence_missing"] = True
                    sources_used.append("axis_3_s2_api")

            # Axis Bonus: EvidencePack 교차검증 (S2 API, IxTheo, Crossref 수집분 포함)
            if evidence_pack and claim["verdict"] != "Anchored":
                ep_check = self._check_evidence_pack(claim, evidence_pack)
                if ep_check["contradiction"]:
                    claim["verdict"]       = "Contradicted"
                    claim["verify_source"] = f"evidence_pack_contradiction ({ep_check.get('source_tool')})"
                    claim["counter_evidence"] = ep_check.get("counter_evidence", [])
                    sources_used.append("axis_bonus_ep_contradiction")
                elif ep_check["match"]:
                    claim["verdict"]       = "Anchored"
                    claim["verify_source"] = f"evidence_pack ({ep_check.get('source_tool')})"
                    sources_used.append("axis_bonus_ep")

            # 최종 미결 → Unverified
            if claim["verdict"] is None:
                claim["verdict"]       = "Unverified"
                claim["verify_source"] = "not_verified"
                claim["evidence_missing"] = True

            claim["sources_used"] = sources_used
            self._log_tool(
                "triangulate_verify",
                f"{claim['id']}: {claim['raw_match'][:40]}",
                f"{claim['verdict']} ({', '.join(sources_used) or '없음'})",
                ""
            )

        return claims

    def _check_paper_anchor(self, claim: dict, paper_text: str) -> bool:
        """원본 논문 내에 주장의 핵심 문자열이 존재하는지 역참조."""
        if not paper_text or paper_text.startswith("[PDF:"):
            return False
        # 핵심 매치 문자열(raw_match)의 주요 토큰이 원문에 있는지 확인
        tokens = re.findall(r'[A-Za-z가-힣]{4,}', claim["raw_match"])
        hit_count = sum(1 for t in tokens if t.lower() in paper_text.lower())
        return hit_count >= max(1, len(tokens) // 2)

    def _run_google_scholar_quick(self, claim: dict) -> dict:
        """
        google-scholar-quick (CDP Google Scholar) 실행.
        raw_match에서 저자+연도를 추출하여 검색 쿼리 구성.
        """
        result = {"found": False, "searched": False, "data": {}}

        if not SCHOLAR_QUICK_CFG.get("enabled", True):
            self._log_tool("google_scholar_quick", "config 확인", "비활성화됨", "")
            return result

        if not SCHOLAR_QUICK_SH.exists():
            self._log_tool("google_scholar_quick", "CLI 확인", "스크립트 경로 없음", str(SCHOLAR_QUICK_SH))
            return result

        # 검색 쿼리 구성: 저자명 + 연도 추출
        m = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*\((\d{4})', claim["raw_match"])
        if not m:
            # 비-citation 타입이거나 파싱 불가 — 이미 추출된 raw_match 그대로 사용
            query = claim["raw_match"][:60]
        else:
            query = f"{m.group(1)} {m.group(2)}"

        result["searched"] = True

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                proc = subprocess.run(
                    ["zsh", str(SCHOLAR_QUICK_SH), query, tmp_dir],
                    capture_output=True, text=True, timeout=20
                )
                self._log_tool(
                    "google_scholar_quick",
                    f"쿼리: {query}",
                    f"returncode={proc.returncode}",
                    proc.stderr[:100] if proc.stderr else ""
                )

                # papers_*.json 파일 탐색
                paper_files = list(Path(tmp_dir).glob("papers_*.json"))
                if not paper_files:
                    return result

                papers_raw = paper_files[0].read_text(encoding="utf-8", errors="ignore").strip()
                if not papers_raw or papers_raw in ("null", "[]", ""):
                    return result

                # JSON 파싱 시도
                try:
                    papers = json.loads(papers_raw)
                    if isinstance(papers, list) and len(papers) > 0:
                        result["found"] = True
                        result["data"]  = {
                            "query":   query,
                            "results": papers[:3],  # 상위 3건만 보존
                            "hit_count": len(papers)
                        }
                except (json.JSONDecodeError, ValueError):
                    # 파싱 실패 — 검색은 했지만 결과 해석 불가
                    result["searched"] = True

        except subprocess.TimeoutExpired:
            self._log_tool("google_scholar_quick", f"쿼리: {query}", "타임아웃(20s)", "timeout")
        except FileNotFoundError:
            self._log_tool("google_scholar_quick", "zsh 실행", "zsh 또는 스크립트 없음", "")
        except Exception as e:
            self._log_tool("google_scholar_quick", f"쿼리: {query}", "예외", str(e)[:100])

        return result

    def _run_s2_verify(self, claim: dict) -> dict:
        """
        Axis 3 검증: Semantic Scholar API로 인용 주장 실존 여부 확인.
        저자명+연도를 쿼리로 검색하여 일치 여부 판정.
        """
        result = {"found": False, "searched": False, "data": {}}

        if not S2_CFG.get("enabled", True):
            return result

        if not S2_RUNNER.exists():
            return result

        # 검색 쿼리 구성 (저자명 + 연도 추출)
        m = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*\((\d{4})', claim["raw_match"])
        query = f"{m.group(1)} {m.group(2)}" if m else claim["raw_match"][:60]

        result["searched"] = True
        try:
            proc = subprocess.run(
                [sys.executable, str(S2_RUNNER),
                 "--query", query, "--limit", "3", "--format", "json",
                 "--fields", self.S2_FIELDS_OF_STUDY],
                capture_output=True, text=True, timeout=20
            )
            if proc.returncode == 0 and proc.stdout.strip():
                data = json.loads(proc.stdout)
                papers = data.get("results", [])
                if papers:
                    result["found"] = True
                    result["data"]  = {
                        "query":     query,
                        "results":   papers[:2],
                        "hit_count": len(papers)
                    }
                self._log_tool("s2_verify", f"Axis3 검증: {query}",
                               f"{'발견' if result['found'] else '미발견'} ({len(papers)}건)", "")
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            self._log_tool("s2_verify", f"Axis3 검증: {query}", "예외", str(e)[:100])

        return result

    def _check_evidence_pack(self, claim: dict, evidence_pack: dict) -> dict:
        """EvidencePack 내 abstracts와 주장의 키워드를 교차 검증."""
        result = {"match": False, "contradiction": False, "counter_evidence": [], "source_tool": None}
        abstracts = evidence_pack.get("abstracts", [])
        if not abstracts:
            return result

        keywords = re.findall(r'[A-Za-z가-힣0-9]{3,}', claim["raw_match"])
        negative_markers = (
            "challenge", "challenges", "challenged", "contradict", "contradicts",
            "against", "critique", "criticizes", "rejects", "dispute", "disputes",
            "반박", "비판", "부정", "논박", "반대", "논쟁"
        )
        for abstract in abstracts:
            text = json.dumps(abstract, ensure_ascii=False).lower()
            hit = sum(1 for k in keywords if k.lower() in text)
            if hit >= max(1, len(keywords) // 2):
                result["match"] = True
                result["source_tool"] = abstract.get("source_tool", "unknown")
                if any(marker in text for marker in negative_markers):
                    result["contradiction"] = True
                    result["counter_evidence"].append({
                        "source_tool": abstract.get("source_tool", "unknown"),
                        "title": abstract.get("title", ""),
                        "url": abstract.get("url", ""),
                        "snippet": abstract.get("snippet") or abstract.get("abstract", ""),
                    })
                break

        return result

    def _adversarial_reconstruct(self, review_text: str) -> dict:
        """
        ③ 적대적 재구성:
        Phase 1의 [Critique] 토큰을 추출 → google-scholar-quick으로 저자 진영 반론 검색
        → 돌파 여부에 따라 Critique-Validated / Critique-Weakened 판정.
        """
        print("     [Critique] 토큰 추출 중...")

        # [Critique] 또는 **비평**: 패턴으로 비평 섹션 추출
        critique_pattern = re.compile(
            r'(?:\[Critique\]|\*\*비평\*\*|\*\*Critique\*\*)[:\s]*([^\n]{20,200})',
            re.IGNORECASE
        )
        critiques = critique_pattern.findall(review_text)
        results = []

        for i, critique_text in enumerate(critiques[:5]):  # 최대 5건만 처리
            # 비평 대상 키워드 추출
            keywords = re.findall(r'[A-Za-z가-힣]{4,}', critique_text)[:3]
            query = " ".join(keywords) + " defense response" if keywords else critique_text[:40]

            print(f"     비평 {i+1}/{min(len(critiques), 5)}: {critique_text[:50]}...")

            sq_result = self._run_google_scholar_quick({"raw_match": query, "type": "assertion"})

            verdict = "Critique-Validated"  # 기본값: 반격 없으면 비평 유지
            counter_evidence = None

            if sq_result["found"]:
                counter_evidence = sq_result["data"]
                # 반격 문헌이 발견됐다고 해서 자동으로 비평을 약화시키지 않음.
                # 에이전트가 내용을 확인하여 최종 판정해야 함 → Critique-Under-Review
                verdict = "Critique-Under-Review"
                self._log_tool(
                    "adversarial_recon",
                    f"비평 {i+1}: {critique_text[:40]}",
                    f"반격 문헌 {len(counter_evidence.get('results',[]))}건 발견 — 에이전트가 내용 확인 필요",
                    ""
                )
            else:
                self._log_tool(
                    "adversarial_recon",
                    f"비평 {i+1}: {critique_text[:40]}",
                    "반격 문헌 미발견 → 비평 최강 유효성 확인",
                    ""
                )

            # counter_evidence 상세 구조화 (제목/저자/연도 추출)
            ce_structured = []
            if counter_evidence:
                for item in counter_evidence.get("results", [])[:3]:  # 최대 3건
                    ce_structured.append({
                        "title":   item.get("title", "(제목 미상)"),
                        "authors": item.get("authors", ["(저자 미상)"]),
                        "year":    item.get("year", "n.d."),
                        "snippet": item.get("snippet", "")[:120]
                    })

            results.append({
                "critique_text":    critique_text.strip(),
                "verdict":          verdict,
                "counter_evidence": ce_structured,
                "query_used":       query
            })

        if not critiques:
            print("     ℹ️  리뷰에서 [Critique] 토큰을 찾지 못했습니다. 어노테이션 확인 요망.")

        return {"critique_count": len(critiques), "results": results}

    def _calibrate_confidence(self, verified_claims: list[dict]) -> dict:
        """④ 신뢰도 교정: 검증 결과를 집계하여 calibration 요약 산출."""
        total        = len(verified_claims)
        anchored     = sum(1 for c in verified_claims if c["verdict"] == "Anchored")
        unverified   = sum(1 for c in verified_claims if c["verdict"] == "Unverified")
        contradicted = sum(1 for c in verified_claims if c["verdict"] == "Contradicted")

        def pct(n): return (n / total * 100) if total > 0 else 0

        by_source: dict[str, int] = {}
        for c in verified_claims:
            src = c.get("verify_source", "unknown")
            by_source[src] = by_source.get(src, 0) + 1

        return {
            "claims": verified_claims,
            "summary": {
                "total":           total,
                "anchored":        anchored,
                "unverified":      unverified,
                "contradicted":    contradicted,
                "anchored_pct":    pct(anchored),
                "unverified_pct":  pct(unverified),
                "contradicted_pct": pct(contradicted),
                "by_source":       by_source
            }
        }

    def _generate_transparency_report(self,
                                      calibration: dict,
                                      critique_results: dict,
                                      verified_claims: list[dict]) -> str:
        """⑤ 검증 투명성 보고서 마크다운 생성 (Counter-Evidence Appendix 자동 포함)."""
        s   = calibration["summary"]
        cr  = critique_results
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Counter-Evidence Appendix 생성
        ce_lines = []
        for r in cr.get("results", []):
            if r.get("counter_evidence"):
                ce_lines.append(f"\n**🥊 비평 대상**: `{r['critique_text'][:60]}...`")
                for idx, ce in enumerate(r["counter_evidence"], 1):
                    authors_str = ", ".join(ce["authors"])[:50] if isinstance(ce["authors"], list) else str(ce["authors"])[:50]
                    ce_lines.append(
                        f"{idx}. **{authors_str} ({ce['year']}), *{ce['title'][:60]}***\n"
                        f"   - {ce['snippet']}"
                    )
        if ce_lines:
            counter_evidence_appendix = (
                "---\n\n## 🛡️ Appendix: Counter-Evidence (반격 문헌)\n\n"
                "본 비평의 [Critique] 토큰에 대해 시스템이 자동 수집한 반격 문헌입니다.\n"
                + "\n".join(ce_lines)
                + "\n\n"
            )
        else:
            counter_evidence_appendix = ""

        # 소스별 커버리지 문자열
        src_lines = "\n".join(
            f"  - {src}: {cnt}건"
            for src, cnt in s["by_source"].items()
        )

        # Unverified 목록
        unverified_list = [
            f"  - [{c['id']}] {c['context'][:80]}... → `[Evidence_Missing]`"
            for c in verified_claims if c["verdict"] == "Unverified"
        ]
        unverified_block = "\n".join(unverified_list) if unverified_list else "  (없음)"

        # Contradicted 목록
        contradicted_list = [
            f"  - [{c['id']}] {c['context'][:80]}... → 재작성 필요"
            for c in verified_claims if c["verdict"] == "Contradicted"
        ]
        contradicted_block = "\n".join(contradicted_list) if contradicted_list else "  (없음)"

        # Critique 결과 블록
        critique_block_lines = []
        for r in cr.get("results", []):
            v_icon = {"Critique-Validated": "✅", "Critique-Under-Review": "⚠️"}.get(r["verdict"], "❓")
            critique_block_lines.append(
                f"  - {v_icon} `{r['verdict']}` — {r['critique_text'][:80]}"
            )
        critique_block = "\n".join(critique_block_lines) if critique_block_lines else "  (비평 토큰 없음)"

        return f"""---

## 🔒 검증 투명성 보고 (Phase 2 — Dialectical Verification)

> **검증 일시**: {now} | **세션 ID**: {self.session_id}

### 📊 사실적 주장 검증 결과

| 판정 | 건수 | 비율 |
| :--- | ---: | ---: |
| ✅ Anchored (근거 확인) | {s['anchored']} | {s['anchored_pct']:.0f}% |
| ⚠️ Unverified (미확인) | {s['unverified']} | {s['unverified_pct']:.0f}% |
| ❌ Contradicted (반박) | {s['contradicted']} | {s['contradicted_pct']:.0f}% |
| **합계** | **{s['total']}** | **100%** |

### 🔍 검증 소스 커버리지

{src_lines if src_lines else '  (검증 소스 없음)'}
- 🔬 axis_3_s2_api: Semantic Scholar API 검증
- 📚 msn_th_db: **{'활성화' if INTERNAL_DB_ENABLED else '제외 (영구 비활성화 — config.json internal_db.enabled=false)'}**
- 🇩🇪 axis_4_ixtheo: Tübingen Index Theologicus 검증
- 📑 axis_5_crossref: Crossref Premium Theology Journal 검증
- 🇰🇷 axis_7_kci: KCI (한국학술지인용색인) 검증
- 🇰🇷 axis_8_riss: RISS (학술연구정보서비스) 검증

### ⚠️ Unverified 주장 목록 (`[Evidence_Missing]` 적용)

{unverified_block}

### ❌ Contradicted 주장 → 재작성 대상

{contradicted_block}

### 🥊 적대적 재구성 결과 ({cr.get('critique_count', 0)}개 비평 토큰)

{critique_block}

> **주의**: `Critique-Under-Review`는 반격 문헌이 발견됐으나 에이전트가 내용을 확인하여 최종 판정해야 합니다.

{counter_evidence_appendix}
---
*Parrehsia v10 Dialectical Verification — ARC v4.0*
"""

def run_self_test() -> int:
    errors = []

    def check(condition: bool, message: str):
        if not condition:
            errors.append(message)

    check(PROJECT_ROOT.exists(), f"engine_root missing: {PROJECT_ROOT}")
    check((PROMPT_DIR / "unified_review.json.md").exists(), "unified_review prompt missing")
    check((CONFIG_DIR / "annotation_tokens.json").exists(), "annotation_tokens config missing")
    check(GS_SEMANTIC_CFG.get("max_queries_per_session", 4) <= 4, "Scholar Labs session cap exceeds 4")
    check(GS_SEMANTIC_CFG.get("citation_depth", "all") in CITATION_DEPTH_CHOICES, "invalid citation_depth")
    check(KCI_RUNNER is not None, "KCI_RUNNER path is empty")
    check(RISS_RUNNER is not None, "RISS_RUNNER path is empty")

    with tempfile.TemporaryDirectory() as tmp_dir:
        sample = Path(tmp_dir) / "sample_review.md"
        sample.write_text(
            "# I. Test\n\n[Critique] Recent scholars challenge Doe (2024) on justification.\n",
            encoding="utf-8",
        )
        engine = TheologyReviewEngine(str(sample))
        query = engine._as_semantic_question("LLM summary grounding evaluation")
        check(query == "What does recent scholarship say about LLM summary grounding evaluation?", "semantic question rewrite failed")

        pack = {
            "schema_version": 1,
            "session_id": "self-test",
            "target": str(sample),
            "abstracts": [
                {
                    "source_tool": "google_scholar_semantic",
                    "title": "A Challenge to Doe",
                    "abstract": "This paper challenges Doe 2024 on justification.",
                    "snippet": "challenges Doe 2024",
                    "provenance": {"source_file": "selftest"},
                }
            ],
            "provenance": [],
        }
        check(engine._validate_evidence_pack(pack) == [], "EvidencePack validation failed")
        ep = engine._check_evidence_pack({"raw_match": "Doe (2024)", "type": "citation"}, pack)
        check(ep["contradiction"], "EvidencePack contradiction heuristic failed")

    if errors:
        print(json.dumps({"self_test": "failed", "errors": errors}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    print(json.dumps({
        "self_test": "ok",
        "checks": [
            "config_paths",
            "google_scholar_semantic_contract",
            "query_rewrite",
            "evidence_pack_schema",
            "contradiction_heuristic",
        ],
    }, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Theology Reviewer / Easy Review orchestrator")
    parser.add_argument("target", nargs="?", help="논문 텍스트/마크다운 파일 경로. PDF는 pdf-extractor를 먼저 사용.")
    parser.add_argument("--phase", choices=["0", "1", "2", "all"], default="all", help="실행할 Phase")
    parser.add_argument("--review", default="", help="Phase 2 단독 실행 시 Phase 1 리뷰 원고 경로")
    parser.add_argument("--session", default="", help="EvidencePack이 있는 Phase 0 세션 디렉토리")
    parser.add_argument("--self-test", action="store_true", help="브라우저/네트워크 없이 설정과 핵심 헬퍼를 검증")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if not args.target:
        parser.error("target is required unless --self-test is used")

    engine = TheologyReviewEngine(args.target)
    print(f"✅ Theology Review Engine v10.5 초기화: {args.target}")
    print(f"   세션 ID: {engine.session_id}")
    print(f"   Phase  : {args.phase}")

    p0_result = {}

    if args.phase in ("0", "all"):
        p0_result = engine.prepare_pass0()

    if args.phase in ("1", "all"):
        ev_dir = p0_result.get("session_dir", args.session)
        engine.prepare_pass1(evidence_session_dir=ev_dir)

    if args.phase in ("2", "all"):
        review_path = args.review
        if not review_path:
            review_path = args.target
            print("  ℹ️ --review 미지정. 데모 모드: 논문 파일 자체를 대상으로 Phase 2 실행")
        ev_dir = p0_result.get("session_dir", args.session)
        engine.prepare_pass2(
            phase1_review_path=review_path,
            evidence_session_dir=ev_dir
        )

    print(f"\n🏁 완료. 세션 ID: {engine.session_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
