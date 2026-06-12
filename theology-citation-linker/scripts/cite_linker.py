#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import sys
import argparse
from difflib import SequenceMatcher
from collections import Counter

FOOTNOTE_CALL_RE = re.compile(r'\[\^([^\]\s]+)\]')
FOOTNOTE_DEF_RE = re.compile(r'(?ms)^\[\^([^\]]+)\]:\s*(.*?)(?=^\[\^[^\]]+\]:|\Z)')
FOOTNOTE_DEF_START_RE = re.compile(r'(?m)^\[\^[^\]]+\]:')
ADJACENT_FOOTNOTE_RE = re.compile(r'(?:\[\^[^\]\s]+\]){2,}')


def split_footnote_sections(content):
    """문서를 본문과 각주 정의 블록으로 분리한다."""
    match = FOOTNOTE_DEF_START_RE.search(content)
    if not match:
        return content, ""
    return content[:match.start()], content[match.start():]


def parse_footnote_definitions(defs_text):
    """멀티라인 각주 정의를 파싱한다."""
    return [(key, text.strip()) for key, text in FOOTNOTE_DEF_RE.findall(defs_text)]


def line_number_for_offset(text, offset):
    return text.count("\n", 0, offset) + 1


def audit_footnotes(content):
    """
    Markdown 각주 구조를 점검한다.

    핵심 판정:
    - 같은 위치의 연속 각주: 하나의 각주 안에 병합해야 할 후보
    - 서로 다른 위치의 반복 각주 호출: PDF 변환 시 새 번호가 추가될 위험
    - 본문 호출/하단 정의 누락 및 미사용 정의
    """
    body, defs_text = split_footnote_sections(content)
    calls = [
        {
            "id": match.group(1),
            "line": line_number_for_offset(body, match.start()),
            "offset": match.start(),
            "marker": match.group(0),
        }
        for match in FOOTNOTE_CALL_RE.finditer(body)
    ]
    definitions = parse_footnote_definitions(defs_text)
    def_ids = [key for key, _ in definitions]
    call_ids = [call["id"] for call in calls]

    adjacent_groups = []
    for match in ADJACENT_FOOTNOTE_RE.finditer(body):
        ids = FOOTNOTE_CALL_RE.findall(match.group(0))
        if len(ids) >= 2:
            adjacent_groups.append({
                "ids": ids,
                "line": line_number_for_offset(body, match.start()),
                "marker": match.group(0),
            })

    call_counter = Counter(call_ids)
    repeated_calls = []
    for key, count in sorted(call_counter.items(), key=lambda item: item[0]):
        if count > 1:
            repeated_calls.append({
                "id": key,
                "count": count,
                "lines": [call["line"] for call in calls if call["id"] == key],
            })

    duplicate_definitions = [
        {"id": key, "count": count}
        for key, count in sorted(Counter(def_ids).items(), key=lambda item: item[0])
        if count > 1
    ]

    missing_definitions = sorted(set(call_ids) - set(def_ids), key=str)
    unused_definitions = sorted(set(def_ids) - set(call_ids), key=str)

    issue_count = (
        len(adjacent_groups)
        + len(repeated_calls)
        + len(duplicate_definitions)
        + len(missing_definitions)
        + len(unused_definitions)
    )

    return {
        "body_call_count": len(call_ids),
        "body_unique_call_count": len(set(call_ids)),
        "definition_count": len(def_ids),
        "definition_unique_count": len(set(def_ids)),
        "pdf_footnote_projection": len(call_ids),
        "definition_projection": len(def_ids),
        "adjacent_groups": adjacent_groups,
        "repeated_calls": repeated_calls,
        "duplicate_definitions": duplicate_definitions,
        "missing_definitions": missing_definitions,
        "unused_definitions": unused_definitions,
        "issue_count": issue_count,
        "passed": issue_count == 0,
    }


def print_footnote_audit_report(report):
    """각주 구조 감사 결과를 사람이 읽을 수 있게 출력한다."""
    print("\n=== Footnote Structure Audit ===")
    print(f"Body footnote calls:       {report['body_call_count']}")
    print(f"Unique body footnote IDs:  {report['body_unique_call_count']}")
    print(f"Footnote definitions:      {report['definition_count']}")
    print(f"Unique definition IDs:     {report['definition_unique_count']}")
    print(f"Projected PDF footnotes:   {report['pdf_footnote_projection']}")
    print(f"Markdown definition count: {report['definition_projection']}")

    if report["adjacent_groups"]:
        print("\n[MERGE-CANDIDATE] Same-position adjacent footnotes:")
        for group in report["adjacent_groups"]:
            joined = ", ".join(group["ids"])
            print(f"  - line {group['line']}: {group['marker']} (merge IDs: {joined})")

    if report["repeated_calls"]:
        print("\n[REPEAT-CALL] Same footnote ID reused at distinct body positions:")
        for item in report["repeated_calls"]:
            lines = ", ".join(str(line) for line in item["lines"])
            print(f"  - [^{item['id']}] appears {item['count']} times at lines {lines}")

    if report["duplicate_definitions"]:
        print("\n[DUPLICATE-DEF] Duplicate footnote definitions:")
        for item in report["duplicate_definitions"]:
            print(f"  - [^{item['id']}] defined {item['count']} times")

    if report["missing_definitions"]:
        print("\n[MISSING-DEF] Calls without definitions:")
        print("  - " + ", ".join(f"[^{key}]" for key in report["missing_definitions"]))

    if report["unused_definitions"]:
        print("\n[UNUSED-DEF] Definitions not called in body:")
        print("  - " + ", ".join(f"[^{key}]" for key in report["unused_definitions"]))

    if report["passed"]:
        print("\nFootnote audit: PASS")
    else:
        print("\nFootnote audit: FAIL")
        print("Recommended policy:")
        print("  - Adjacent footnotes at the same location should be merged into one note.")
        print("  - Repeated footnote calls at different locations should become independent short notes.")
        print("  - Body calls and footnote definitions should be one-to-one after reindexing.")

def normalize_authors(authors):
    """저자 리스트 중 성과 이름이 분절된 항목들을 감지하여 단일 저자명으로 병합한다."""
    if not authors:
        return []
    
    # authors가 단일 문자열인 경우 리스트로 변환
    if isinstance(authors, str):
        authors = [authors]
        
    normalized = []
    i = 0
    while i < len(authors):
        current = authors[i].strip()
        if not current:
            i += 1
            continue
            
        # 다음 요소가 있고, 분절된 이름인지 검사
        if i + 1 < len(authors):
            nxt = authors[i+1].strip()
            # 분절 조건 판단:
            # 1. 영문 분절: current가 공백 없는 한 단어이고, nxt에 공백이나 마침표가 있는 경우
            #    예: current="Smith", nxt="Brandon D." -> "Brandon D. Smith"
            #    또는 current="Smith", nxt="B." -> "B. Smith"
            is_eng_split = (
                re.search(r'[a-zA-Z]', current) is not None and 
                re.search(r'[a-zA-Z]', nxt) is not None and 
                ' ' not in current and 
                ( ' ' in nxt or '.' in nxt or len(nxt) <= 3 )
            )
            
            # 2. 국문 분절: current가 1글자 성(예: 김, 이, 박)이고, nxt가 1~3글자 이름인 경우
            #    예: current="안", nxt="상혁" -> "안상혁"
            is_kor_split = (
                re.match(r'^[ㄱ-ㅎㅏ-ㅣ가-힣]$', current) is not None and
                re.match(r'^[ㄱ-ㅎㅏ-ㅣ가-힣]{1,3}$', nxt) is not None
            )
            
            if is_eng_split:
                merged = f"{nxt} {current}"
                normalized.append(merged)
                i += 2
                continue
            elif is_kor_split:
                merged = f"{current}{nxt}"
                normalized.append(merged)
                i += 2
                continue
                
        normalized.append(current)
        i += 1
        
    return normalized

def clean_author_name(author):
    """저자 이름을 SBL 스타일로 정제한다."""
    if not author:
        return ""
    author = author.strip()
    # 영어 이름에서 'Last, First' 형식인 경우 'First Last'로 변환
    if ',' in author:
        parts = [p.strip() for p in author.split(',')]
        if len(parts) >= 2:
            # Last, First -> First Last
            # 단, 뒤쪽에 Jr. 등이 올 수도 있으므로 간단히 뒤집는다.
            return f"{parts[1]} {parts[0]}"
    return author

def format_author_list(authors, for_bib=False):
    """저자 리스트를 SBL 포맷으로 합친다."""
    if not authors:
        return "저자 미상"
    
    if isinstance(authors, str):
        authors = [authors]
        
    authors = normalize_authors(authors)
    if not authors:
        return "저자 미상"
        
    cleaned = [clean_author_name(a) for a in authors]
    
    # 참고문헌(Bibliography)인 경우 첫 번째 저자는 '성, 이름'으로 표기
    if for_bib:
        first_author = authors[0].strip()
        # 이미 쉼표가 있으면 그대로 쓰고, 없으면 영어의 경우 성과 이름을 분리해서 성, 이름으로 바꾼다.
        if ',' not in first_author:
            # 한국어 저자인 경우 그냥 쓴다.
            # 영어 이름 판정 (알파벳이 있으면 영어)
            if re.search(r'[a-zA-Z]', first_author):
                parts = first_author.split()
                if len(parts) >= 2:
                    first_author = f"{parts[-1]}, {' '.join(parts[:-1])}"
        else:
            # 'Last, First' 형식이면 그대로 쓴다
            pass
            
        if len(cleaned) == 1:
            return first_author
        elif len(cleaned) == 2:
            return f"{first_author}, and {cleaned[1]}"
        else:
            return f"{first_author}, {', '.join(cleaned[1:-1])}, and {cleaned[-1]}"
            
    # 각주(Footnote)인 경우 모두 'First Last'로 표기
    else:
        if len(cleaned) == 1:
            return cleaned[0]
        elif len(cleaned) == 2:
            return f"{cleaned[0]} and {cleaned[1]}"
        else:
            return f"{', '.join(cleaned[:-1])}, and {cleaned[-1]}"

def get_author_lastname(author):
    """단축 인용을 위해 저자의 성(LastName)을 추출한다."""
    if not author:
        return "Unknown"
    author = author.strip()
    # 한국어 저자인 경우 (한글 글자수가 4자 이하이고 공백이 없는 경우) 성과 이름을 구분하기 어려우므로 이름 전체를 쓴다
    if re.match(r'^[ㄱ-ㅎㅏ-ㅣ가-힣]+$', author) and len(author) <= 4:
        return author
    
    # 영어 이름인 경우
    if ',' in author:
        return author.split(',')[0].strip()
    parts = author.split()
    if parts:
        return parts[-1]
    return author

def get_short_title(title):
    """제목을 단축형(Short Title)으로 가공한다."""
    if not title:
        return "Untitled"
    title = title.strip()
    # 구두점 기준으로 자르거나 글자수 제한
    title_clean = re.split(r'[:?.]', title)[0]
    words = title_clean.split()
    if len(words) > 4:
        return " ".join(words[:4]) + "..."
    return title_clean

def parse_anchor(anchor_text):
    """[Ref: Waltke 2007, 145] 형식의 앵커 텍스트를 파싱하여 저자쿼리, 연도, 페이지를 반환한다."""
    # 연도 추출 (1900~2099)
    year_match = re.search(r'\b(19\d{2}|20\d{2})[a-z]?\b', anchor_text)
    year = year_match.group(0) if year_match else None
    
    # 앵커를 쉼표로 분할하여 페이지 번호 추출 시도
    parts = anchor_text.split(',')
    page = None
    if len(parts) >= 2:
        # 마지막 파트가 페이지 번호일 가능성이 큼
        last_part = parts[-1].strip()
        # 'p. 145', 'pp. 145-146', '145' 등 매칭
        page_match = re.search(r'\b(?:p\.|pp\.)?\s*(\d+(?:-\d+)?)\b', last_part)
        if page_match:
            page = page_match.group(1)
            # 페이지를 앵커 텍스트에서 제거하여 순수 저자 쿼리 획득
            anchor_text = ",".join(parts[:-1])
            
    # 페이지가 명시적으로 안 잘렸어도 뒤에 숫자가 남았다면 페이지로 의심
    if not page:
        num_matches = re.findall(r'\b\d+(?:-\d+)?\b', anchor_text)
        if num_matches:
            # 연도를 제외한 마지막 숫자가 있다면 그것을 페이지로 처리
            for num in reversed(num_matches):
                if num != year:
                    page = num
                    anchor_text = anchor_text.replace(num, "").replace(",", "").strip()
                    break
                    
    # 연도 제거
    if year:
        # 연도 뒤의 a-z (예: 2012a) 까지 제거
        anchor_text = re.sub(r'\b' + re.escape(year) + r'\b', '', anchor_text)
        
    author_query = anchor_text.replace(",", "").replace("[Ref:", "").replace("]", "").strip()
    author_query = re.sub(r'\s+', ' ', author_query)
    
    return {
        "author_query": author_query,
        "year": year,
        "page": page
    }

def calculate_similarity(parsed, doc):
    """앵커 파싱 정보와 EvidencePack 문헌 정보 간의 매핑 유사도를 구한다."""
    title = doc.get("title", "")
    venue = doc.get("venue", "") or doc.get("journal", "") or ""
    
    # doc에서 저자 정보 수집
    doc_authors = doc.get("authors", [])
    if not doc_authors and "raw" in doc:
        raw_authors = doc["raw"].get("authors", [])
        if isinstance(raw_authors, list):
            doc_authors = raw_authors
        elif isinstance(raw_authors, str):
            doc_authors = [raw_authors]
    doc_authors = normalize_authors(doc_authors)
            
    doc_year = str(doc.get("year", ""))
    if not doc_year and "raw" in doc:
        doc_year = str(doc["raw"].get("year", ""))
        
    # 1. 연도 일치도 (연도가 명시된 경우만 계산)
    year_score = 0.0
    if parsed["year"] and doc_year:
        # 2012a 같은 경우 알파벳 떼고 비교
        parsed_year_clean = re.sub(r'[a-zA-Z]', '', parsed["year"])
        doc_year_clean = re.sub(r'[a-zA-Z]', '', doc_year)
        if parsed_year_clean == doc_year_clean:
            year_score = 1.0
        elif parsed_year_clean[:3] == doc_year_clean[:3]: # 10년 단위 일치
            year_score = 0.5
            
    # 2. 저자 일치도
    author_score = 0.0
    author_query = parsed["author_query"].lower()
    
    if doc_authors:
        for author in doc_authors:
            author_lower = author.lower()
            ratio = SequenceMatcher(None, author_query, author_lower).ratio()
            # 부분 포함 관계인 경우 점수 보정
            if author_query in author_lower or author_lower in author_query:
                ratio = max(ratio, 0.85)
            # 성(LastName)과 쿼리가 정확히 일치하는 경우 가중치
            lastname = get_author_lastname(author).lower()
            if author_query == lastname:
                ratio = max(ratio, 0.95)
            author_score = max(author_score, ratio)
    else:
        # 저자가 누락된 경우 제목과 비교
        ratio = SequenceMatcher(None, author_query, title.lower()).ratio()
        author_score = ratio * 0.4
        
    # 3. 제목 및 저널명 보조 비교 (저자 매칭이 낮을 경우 보완)
    title_score = SequenceMatcher(None, author_query, title.lower()).ratio()
    
    # 종합 신뢰도 계산
    if parsed["year"]:
        # 연도 정보가 있는 경우
        confidence = (author_score * 0.6) + (year_score * 0.3) + (title_score * 0.1)
    else:
        # 연도 정보가 없는 경우
        confidence = (author_score * 0.8) + (title_score * 0.2)
        
    return confidence

def is_korean_doc(doc):
    """한국어 문헌인지 판별한다."""
    # 저자 판별
    doc_authors = doc.get("authors", [])
    if not doc_authors and "raw" in doc:
        raw_authors = doc["raw"].get("authors", [])
        if isinstance(raw_authors, list):
            doc_authors = raw_authors
        elif isinstance(raw_authors, str):
            doc_authors = [raw_authors]
            
    for author in doc_authors:
        if re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', author):
            return True
            
    # 제목 판별
    title = doc.get("title", "")
    if re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', title):
        return True
        
    # 저널/출판사 판별
    venue = doc.get("venue", "") or doc.get("raw", {}).get("journal", "") or ""
    if re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', venue):
        return True
        
    return False

def format_sbl_footnote(doc, page=None):
    """SBL 스타일로 각주를 포맷팅한다. 한국어 문헌일 경우 한국어 SBL 스타일을 적용한다."""
    raw = doc.get("raw", {})
    fmt = raw.get("format", "Book")
    
    title = doc.get("title", "").strip()
    venue = doc.get("venue", "") or raw.get("journal", "") or ""
    venue = venue.strip()
    
    # 저자 리스트 정제
    doc_authors = doc.get("authors", [])
    if not doc_authors and "raw" in doc:
        raw_authors = raw.get("authors", [])
        if isinstance(raw_authors, list):
            doc_authors = raw_authors
        elif isinstance(raw_authors, str):
            doc_authors = [raw_authors]
            
    authors_formatted = format_author_list(doc_authors, for_bib=False)
    
    year = doc.get("year") or raw.get("year")
    year_str = f" ({year})" if year else ""
    
    is_kor = is_korean_doc(doc)
    
    # 1. Journal Article (저널 논문)
    if fmt == "Journal Article" or venue:
        volume = raw.get("volume", "")
        issue = raw.get("issue", "")
        vol_issue = ""
        if volume and issue:
            vol_issue = f" {volume}, no. {issue}"
        elif volume:
            vol_issue = f" {volume}"
        elif issue:
            vol_issue = f" no. {issue}"
            
        page_str = ""
        if page:
            if is_kor:
                page_str = f": {page}"
            else:
                page_str = f", {page}"
        else:
            pages = raw.get("pages")
            if pages:
                if is_kor:
                    page_str = f": {pages}"
                else:
                    page_str = f", {pages}"
                
        if is_kor:
            return f'{authors_formatted}, 「{title}」, 『{venue}』{vol_issue}{year_str}{page_str}.'
        else:
            return f'{authors_formatted}, "{title}," *{venue}*{vol_issue}{year_str}{page_str}.'
        
    # 2. Dictionary / Lexicon (사전 항목)
    elif fmt == "Dictionary" or "dictionary" in title.lower() or "lexicon" in title.lower():
        publisher = raw.get("publisher", "")
        pub_place = raw.get("pub_place", "")
        editor = raw.get("editor", "")
        
        pub_info = ""
        if pub_place and publisher:
            pub_info = f" ({pub_place}: {publisher}, {year})"
        elif publisher:
            pub_info = f" ({publisher}, {year})"
        else:
            pub_info = f" ({year})"
            
        editor_str = f", ed. {editor}" if editor else ""
        page_str = f", {page}" if page else ""
        
        if is_kor:
            editor_str = f", 편. {editor}" if editor else ""
            return f'{authors_formatted}, 「{title}」, 『{venue or "사전"}』{editor_str}{pub_info}{page_str}.'
        else:
            return f'{authors_formatted}, "{title}," in *{venue or "Dictionary"}*{editor_str}{pub_info}{page_str}.'
        
    # 3. Book (단행본)
    else:
        publisher = raw.get("publisher", "")
        pub_place = raw.get("pub_place", "")
        
        pub_info = ""
        if pub_place and publisher:
            pub_info = f" ({pub_place}: {publisher}, {year})"
        elif publisher:
            pub_info = f" ({publisher}, {year})"
        else:
            pub_info = f" ({year})"
            
        page_str = f", {page}" if page else ""
        
        if is_kor:
            return f"{authors_formatted}, 『{title}』{pub_info}{page_str}."
        else:
            return f"{authors_formatted}, *{title}*{pub_info}{page_str}."

def format_sbl_short_footnote(doc, page=None):
    """동일 문헌 반복 인용 시 SBL 단축형(Short Title)으로 작성한다."""
    doc_authors = doc.get("authors", [])
    if not doc_authors and "raw" in doc:
        raw_authors = doc["raw"].get("authors", [])
        if isinstance(raw_authors, list):
            doc_authors = raw_authors
        elif isinstance(raw_authors, str):
            doc_authors = [raw_authors]
    doc_authors = normalize_authors(doc_authors)
    author = doc_authors[0] if doc_authors else "Unknown"
    lastname = get_author_lastname(author)
    title = doc.get("title", "")
    short_title = get_short_title(title)
    
    page_str = f", {page}" if page else ""
    
    raw = doc.get("raw", {})
    fmt = raw.get("format", "Book")
    venue = doc.get("venue", "") or raw.get("journal", "") or ""
    
    is_kor = is_korean_doc(doc)
    
    if fmt == "Journal Article" or venue:
        if is_kor:
            return f'{lastname}, 「{short_title}」{page_str}.'
        else:
            return f'{lastname}, "{short_title}"{page_str}.'
    else:
        if is_kor:
            return f"{lastname}, 『{short_title}』{page_str}."
        else:
            return f"{lastname}, *{short_title}*{page_str}."

def format_sbl_bibliography(doc):
    """SBL 스타일로 참고문헌(Bibliography)을 포맷팅한다."""
    raw = doc.get("raw", {})
    fmt = raw.get("format", "Book")
    
    title = doc.get("title", "").strip()
    venue = doc.get("venue", "") or raw.get("journal", "") or ""
    venue = venue.strip()
    
    doc_authors = doc.get("authors", [])
    if not doc_authors and "raw" in doc:
        raw_authors = raw.get("authors", [])
        if isinstance(raw_authors, list):
            doc_authors = raw_authors
        elif isinstance(raw_authors, str):
            doc_authors = [raw_authors]
            
    authors_formatted = format_author_list(doc_authors, for_bib=True)
    year = doc.get("year") or raw.get("year")
    
    is_kor = is_korean_doc(doc)
    
    # 1. Journal Article
    if fmt == "Journal Article" or venue:
        volume = raw.get("volume", "")
        issue = raw.get("issue", "")
        vol_issue = ""
        if volume and issue:
            vol_issue = f" {volume}, no. {issue}"
        elif volume:
            vol_issue = f" {volume}"
        elif issue:
            vol_issue = f" no. {issue}"
            
        year_str = f" ({year})" if year else ""
        pages = raw.get("pages", "")
        pages_str = f": {pages}" if pages else ""
        
        if is_kor:
            return f'{authors_formatted}. 「{title}」. 『{venue}』{vol_issue}{year_str}{pages_str}.'
        else:
            return f'{authors_formatted}. "{title}." *{venue}*{vol_issue}{year_str}{pages_str}.'
        
    # 2. Book
    else:
        publisher = raw.get("publisher", "")
        pub_place = raw.get("pub_place", "")
        
        pub_info = ""
        if pub_place and publisher:
            pub_info = f" {pub_place}: {publisher}, {year}."
        elif publisher:
            pub_info = f" {publisher}, {year}."
        else:
            pub_info = f" {year}."
            
        if is_kor:
            return f"{authors_formatted}. 『{title}』." + (f" {pub_info}" if pub_info else "")
        else:
            return f"{authors_formatted}. *{title}*." + (f" {pub_info}" if pub_info else "")

def main():
    parser = argparse.ArgumentParser(description="TAWP Theology Citation Linker")
    parser.add_argument("--file", required=True, help="Path to the target markdown file")
    parser.add_argument("--evidence", help="Path to EvidencePack.json")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the original file with linked citations")
    parser.add_argument(
        "--audit-footnotes",
        action="store_true",
        help="Audit existing Markdown footnote structure without requiring EvidencePack.json.",
    )
    parser.add_argument(
        "--fail-on-footnote-issues",
        action="store_true",
        help="Exit with a non-zero status when footnote audit finds structural issues.",
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: Target file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Read markdown early so footnote-only audit can run without EvidencePack.json.
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    if args.audit_footnotes:
        report = audit_footnotes(content)
        print_footnote_audit_report(report)
        if args.fail_on_footnote_issues and not report["passed"]:
            sys.exit(2)
        if not args.evidence:
            return

    if not args.evidence:
        print("Error: Evidence pack is required unless --audit-footnotes is used alone.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.evidence):
        print(f"Error: Evidence pack not found: {args.evidence}", file=sys.stderr)
        sys.exit(1)
        
    # Load evidence pack
    with open(args.evidence, "r", encoding="utf-8") as f:
        evidence_pack = json.load(f)
        
    abstracts = evidence_pack.get("abstracts", [])
    if not abstracts:
        print("Warning: No abstracts found in EvidencePack.json", file=sys.stderr)
        
    # [Verification & Cleanup] 최종 에세이 본문 내 개발/리서치 부속 섹션 분리 감지 및 본문에서 제거
    # 가로선(---)을 동반한 섹션 매칭 패턴 정의 (각 섹션의 경계를 전방탐색으로 명확화하여 오버랩 방지)
    inventory_pattern = r'(?:---\s*\n*)?(### Appendix: Research Inventory[\s\S]*?)(?=\n---\s*\n*|### Forensic Audit Log|## 참고문헌|## Bibliography|\Z)'
    audit_pattern = r'(?:---\s*\n*)?(### Forensic Audit Log[\s\S]*?)(?=\n---\s*\n*|### Appendix: Research Inventory|## 참고문헌|## Bibliography|\Z)'
    
    inventory_match = re.search(inventory_pattern, content)
    inventory_content = ""
    if inventory_match:
        inventory_content = inventory_match.group(1).strip()
        content = re.sub(inventory_pattern, '', content)
        
    audit_match = re.search(audit_pattern, content)
    audit_content = ""
    if audit_match:
        audit_content = audit_match.group(1).strip()
        content = re.sub(audit_pattern, '', content)

    # 연속된 가로선 및 불필요한 개행 청소
    content = re.sub(r'\n+---\n+---\n+', '\n\n---\n\n', content)
    content = re.sub(r'---\s*\n*---', '---', content)
    # 여러 개의 빈 라인 단일화
    content = re.sub(r'\n{3,}', '\n\n', content)
        
    # 1. 본문의 임시 앵커 [Ref: ...] 추출
    # 정규식 패턴: [Ref: Waltke 2007, 145] 혹은 [Ref:안상혁 2011]
    pattern = r'\[Ref:\s*([^\]\n]+)\]'
    anchors = re.findall(pattern, content)
    
    if not anchors:
        print("No [Ref: ...] anchors found in target file. Proceeding to footnote recovery and bibliography restructuring.")
    else:
        print(f"Found {len(anchors)} citation anchors in the document.")
    
    # 2. 매핑 분석 및 보고서 작성
    mappings = []
    failed_mappings = []
    
    for i, anchor in enumerate(anchors, 1):
        parsed = parse_anchor(anchor)
        print(f"\nProcessing Anchor #{i}: '{anchor}' -> Parsed: {parsed}")
        
        # EvidencePack에서 유사도 가장 높은 문헌 탐색
        best_doc = None
        best_score = 0.0
        
        for doc in abstracts:
            score = calculate_similarity(parsed, doc)
            if score > best_score:
                best_score = score
                best_doc = doc
                
        print(f"  Best Match: '{best_doc.get('title') if best_doc else 'None'}' with confidence {best_score:.2f}")
        
        if best_doc and best_score >= 0.60:
            mappings.append({
                "anchor": anchor,
                "parsed": parsed,
                "doc": best_doc,
                "confidence": best_score
            })
        else:
            failed_mappings.append({
                "anchor": anchor,
                "parsed": parsed,
                "best_match": best_doc.get("title") if best_doc else "None",
                "confidence": best_score
            })
            
    # 매핑 실패 보고
    if failed_mappings:
        print("\n=== WARNING: Unresolved Citations (Confidence < 60%) ===")
        for f in failed_mappings:
            print(f"- Anchor: [Ref: {f['anchor']}] (Best guess: '{f['best_match']}' with score {f['confidence']:.2f})")
        print("Please review and refine your anchors or update the EvidencePack.json.")
        # 실패가 있을 경우 진행할지 경고하지만, 이 스크립트는 우선 매핑 가능한 것들만 처리하도록 구현
        
    # 3. 본문 각주 치환 및 SBL 생성
    # 기존 각주 목록을 파싱하여 새로운 순서로 재배치하거나 넘버링을 이어간다.
    # 기존 각주 정의를 추출하여 본문 내에서 순차적으로 매칭한다.
    # 단, 우리는 [Ref: ...]만을 SBL 각주로 변환하여 본문 최하단에 주입할 것이다.
    # 현재 초안에 기존 각주가 존재할 수 있으므로, 기존 각주 번호와 겹치지 않게 '마지막 각주 번호'를 찾거나
    # 전체 각주를 파싱하여 인덱스를 재정렬하는 방안을 적용하자.
    
    # 기존 각주 정의 찾기
    existing_footnotes = re.findall(r'^\[\^(\d+)\]:\s*(.+)$', content, re.MULTILINE)
    max_fn_num = 0
    if existing_footnotes:
        max_fn_num = max(int(num) for num, _ in existing_footnotes)
    
    print(f"\nExisting footnotes found: {len(existing_footnotes)} (Max number: {max_fn_num})")
    
    # 앵커별 각주 생성
    new_footnote_definitions = []
    # 이전 인용 문헌을 추적하여 Ibid. 또는 Short Title 처리하기 위함
    # (각주 번호, doc_id) 튜플 저장
    citation_history = []
    
    # 임시 각주 앵커 치환을 위한 딕셔너리 구축
    # [Ref: ...] -> [^NewNum]
    anchor_to_citation_num = {}
    current_num = max_fn_num
    
    # 본문 텍스트 내에서 순서대로 매칭하기 위해 re.sub의 replacement 함수를 정의
    # 이를 위해 매핑 결과를 앵커 텍스트 기준 맵으로 변환
    mapping_by_anchor = {m["anchor"]: m for m in mappings}
    
    def repl_func(match):
        nonlocal current_num
        anchor_text = match.group(1)
        if anchor_text not in mapping_by_anchor:
            # 매핑에 실패한 경우 그대로 둔다
            return match.group(0)
            
        m = mapping_by_anchor[anchor_text]
        doc = m["doc"]
        page = m["parsed"]["page"]
        doc_id = doc.get("url") or doc.get("title") # 고유 식별자
        
        # Ibid. 및 Short Title 판정
        current_num += 1
        fn_text = ""
        
        # 바로 이전 각주와 동일 문헌인지 체크
        is_ibid = False
        if citation_history:
            prev_num, prev_doc_id, prev_page = citation_history[-1]
            if prev_doc_id == doc_id:
                is_ibid = True
                if page == prev_page:
                    fn_text = "Ibid."
                else:
                    fn_text = f"Ibid., {page}." if page else "Ibid."
                    
        # 이전에 인용한 적은 있으나 바로 이전은 아닌 경우 (Short Title)
        is_short = False
        if not is_ibid:
            for prev_num, prev_doc_id, prev_page in citation_history:
                if prev_doc_id == doc_id:
                    is_short = True
                    break
            if is_short:
                fn_text = format_sbl_short_footnote(doc, page)
                
        # 최초 인용인 경우 Full Citation
        if not is_ibid and not is_short:
            fn_text = format_sbl_footnote(doc, page)
            
        # 히스토리 기록
        citation_history.append((current_num, doc_id, page))
        
        # 신규 각주 정의 저장
        new_footnote_definitions.append(f"[^{current_num}]: {fn_text}")
        
        return f"[^{current_num}]"
        
    # 본문 본문 내의 [Ref: ...] 치환
    linked_content = re.sub(pattern, repl_func, content)
    
    # 4. 종합 참고문헌(Bibliography) 리스트 구축 (인용 문헌과 그 외 제너럴 자료 이원화)
    # 4-1. [Ref: ...] 매핑을 통해 인용된 고유 문헌 추출
    cited_docs = {}
    for m in mappings:
        doc = m["doc"]
        doc_id = doc.get("url") or doc.get("title")
        if doc_id not in cited_docs:
            cited_docs[doc_id] = doc
            
    # 4-2. 기존 참고문헌 항목 파싱 및 보존
    existing_bib_items = []
    # 참고문헌 섹션 헤더 아래의 본문을 가져옴
    bib_section_match = re.search(r'##\s*(?:참고문헌|Bibliography)([\s\S]*?)(?=\n---|\Z)', content)
    if bib_section_match:
        bib_section_text = bib_section_match.group(1)
        for line in bib_section_text.split('\n'):
            line_stripped = line.strip()
            # 헤더(###)나 비어있는 라인은 스킵
            if line_stripped and not line_stripped.startswith('#'):
                # 진짜 bullet 형식(* 또는 - 뒤에 공백)인 경우 제거하여 원본 텍스트 획득
                if line_stripped.startswith('* ') or line_stripped.startswith('- '):
                    existing_bib_items.append(line_stripped[2:].strip())
                else:
                    existing_bib_items.append(line_stripped)

    # 4-3. 본문의 모든 각주 정의들 수집 (기존 각주 + 신규 치환 각주)
    existing_footnotes = re.findall(r'^\[\^(\d+)\]:\s*(.+)$', content, re.MULTILINE)
    all_footnote_texts = [fn_text.strip() for _, fn_text in existing_footnotes]
    for fn_def in new_footnote_definitions:
        match = re.match(r'^\[\^\d+\]:\s*(.+)$', fn_def)
        if match:
            all_footnote_texts.append(match.group(1).strip())

    # 4-4. 기존 참고문헌 항목들의 Cited / General 이원화 분류 수행
    cited_bib_items = []
    general_bib_items = []
    
    for bib_item in existing_bib_items:
        is_cited = False
        
        # 저자명 추출 (마침표나 쉼표 기준 첫 토큰)
        author_part = bib_item.split('.')[0].split(',')[0].strip('*_# ')
        
        # 제목 추출 (이탤릭 *...* 또는 『...』 또는 「...」 또는 "...")
        title_matches = re.findall(r'\*([^*]+)\*|『([^』]+)』|「([^」]+)」|"([^"]+)"', bib_item)
        titles = [t for group in title_matches for t in group if t]
        
        for fn_text in all_footnote_texts:
            if author_part and len(author_part) >= 2 and author_part.lower() in fn_text.lower():
                if titles:
                    for t in titles:
                        t_clean = t.strip()
                        if len(t_clean) >= 3 and (t_clean.lower() in fn_text.lower() or fn_text.lower() in t_clean.lower()):
                            is_cited = True
                            break
                else:
                    is_cited = True
            
            # 성서 원전 예외 처리
            if "Biblia Hebraica" in bib_item and "BHS" in fn_text:
                is_cited = True
            if "Septuaginta" in bib_item and "LXX" in fn_text:
                is_cited = True
                
            if is_cited:
                break
                
        if is_cited:
            cited_bib_items.append(bib_item)
        else:
            general_bib_items.append(bib_item)

    # 4-5. EvidencePack.json의 Abstracts 정보 결합 (중복 방지 융합)
    # EvidencePack에서 인용된 것으로 나온 항목들
    for doc in cited_docs.values():
        new_entry = format_sbl_bibliography(doc)
        dup = False
        for item in cited_bib_items + general_bib_items:
            if SequenceMatcher(None, new_entry.lower(), item.lower()).ratio() >= 0.8:
                dup = True
                break
        if not dup:
            cited_bib_items.append(new_entry)
            
    # EvidencePack.json에 들어있는 전체 문헌 중 인용되지 않은 일반 자료 추출 및 추가
    general_docs = {}
    for doc in abstracts:
        doc_id = doc.get("url") or doc.get("title")
        if doc_id not in cited_docs:
            general_docs[doc_id] = doc
            
    for doc in general_docs.values():
        new_entry = format_sbl_bibliography(doc)
        dup = False
        for item in cited_bib_items + general_bib_items:
            if SequenceMatcher(None, new_entry.lower(), item.lower()).ratio() >= 0.8:
                dup = True
                break
        if not dup:
            general_bib_items.append(new_entry)

    # 4-6. 정렬 키 적용 (한국어 가나다 정렬 후 영어 알파벳 정렬)
    def sort_bib_key(item):
        clean_item = item.strip('*_# ').replace('"', '').replace('「', '').replace('[]', '').replace('『', '')
        if not clean_item:
            return (2, "")
        first_char = clean_item[0]
        if re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', first_char):
            return (0, clean_item)
        elif re.search(r'[a-zA-Z]', first_char):
            return (1, clean_item.lower())
        else:
            return (2, clean_item.lower())
            
    sorted_cited = sorted(list(set(cited_bib_items)), key=sort_bib_key)
    sorted_general = sorted(list(set(general_bib_items)), key=sort_bib_key)
    
    # 문서의 언어 판별 (한국어 비율이 높으면 국문, 그렇지 않으면 영문으로 참고문헌 타이틀 적용)
    kor_chars = len(re.findall(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', linked_content))
    is_korean_essay = kor_chars > 100
    
    if is_korean_essay:
        bib_title = "## 참고문헌"
        cited_section_title = "### 인용 문헌"
        general_section_title = "### 일반 참고 문헌"
    else:
        bib_title = "## Bibliography"
        cited_section_title = "### Cited Works"
        general_section_title = "### General References"
        
    bib_parts = [bib_title]
    if sorted_cited:
        bib_parts.append(cited_section_title + "\n\n" + "\n\n".join(sorted_cited))
    if sorted_general:
        bib_parts.append(general_section_title + "\n\n" + "\n\n".join(sorted_general))
        
    bib_content = "\n\n".join(bib_parts) + "\n"
    
    # 5. 각주 정의 및 Bibliography 주입
    if new_footnote_definitions:
        last_fn_match = list(re.finditer(r'^\[\^\d+\]:\s*(.+)$', linked_content, re.MULTILINE))
        if last_fn_match:
            last_pos = last_fn_match[-1].end()
            insert_text = "\n" + "\n".join(new_footnote_definitions)
            linked_content = linked_content[:last_pos] + insert_text + linked_content[last_pos:]
        else:
            bib_section_match = re.search(r'##\s*(?:참고문헌|Bibliography)', linked_content)
            if bib_section_match:
                insert_pos = bib_section_match.start()
                insert_text = "\n".join(new_footnote_definitions) + "\n\n"
                linked_content = linked_content[:insert_pos] + insert_text + linked_content[insert_pos:]
            else:
                linked_content += "\n\n" + "\n".join(new_footnote_definitions)
                
    # 참고문헌 섹션 업데이트 (인용 문헌과 일반 참고 문헌으로 구분하여 갱신)
    bib_section_regex = r'(##\s*(?:참고문헌|Bibliography)[\s\S]*?)(?=\n---|\Z)'
    
    if re.search(bib_section_regex, linked_content):
        linked_content = re.sub(bib_section_regex, bib_content, linked_content)
    else:
        linked_content = re.sub(r'\n*---\s*$', '', linked_content)
        linked_content += "\n\n" + bib_content

    final_footnote_report = audit_footnotes(linked_content)
    print_footnote_audit_report(final_footnote_report)
    if args.fail_on_footnote_issues and not final_footnote_report["passed"]:
        print("Error: Footnote audit failed after citation linking.", file=sys.stderr)
        sys.exit(2)
        
    # 결과 저장
    if args.overwrite:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(linked_content)
        print(f"\nSuccessfully overwrote the file: {args.file}")
        print(f"Added {len(new_footnote_definitions)} new footnotes and updated bibliography.")
        
        # 분리된 리서치 인벤토리 및 포렌식 감사 로그를 별도 파일로 저장
        base_path, ext = os.path.splitext(args.file)
        if inventory_content:
            inv_file = f"{base_path}_inventory{ext}"
            with open(inv_file, "w", encoding="utf-8") as f:
                f.write(inventory_content + "\n")
            print(f"Extracted Research Inventory to: {inv_file}")
            
        if audit_content:
            audit_file = f"{base_path}_audit_log{ext}"
            with open(audit_file, "w", encoding="utf-8") as f:
                f.write(audit_content + "\n")
            print(f"Extracted Forensic Audit Log to: {audit_file}")
    else:
        print("\n=== DRY RUN RESULT (No Overwrite) ===")
        print(f"Would write {len(new_footnote_definitions)} new footnotes:")
        for fn in new_footnote_definitions:
            print(fn)
        print("\nWould write Bibliography:")
        for bib in (sorted_cited + sorted_general):
            print(f"- {bib}")
            
        if inventory_content:
            print("\nWould extract Research Inventory to a separate file.")
        if audit_content:
            print("\nWould extract Forensic Audit Log to a separate file.")

if __name__ == "__main__":
    main()
