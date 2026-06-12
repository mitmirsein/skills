#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import csv
import sys
import argparse
from typing import Dict, List, Tuple

# 빌트인 공통 혼용어 세트
COMMON_EQUIVOCATIONS = {
    "칭의 / 의인": ["칭의", "의인"],
    "기독론 / 그리스도론": ["기독론", "그리스도론"],
    "성만찬 / 성찬식 / 성찬 예식": ["성만찬", "성찬식", "성찬 예식"],
    "하나님 / 하느님": ["하나님", "하느님"],
    "여호와 / 야훼": ["여호와", "야훼"],
    "개혁주의 / 칼빈주의": ["개혁주의", "칼빈주의"],
    "계시 / 묵시 / 아포칼립스": ["계시", "묵시", "아포칼립스"]
}

def load_tre_terms(csv_path: str) -> List[Dict]:
    """tre_terms.csv 파일을 로드하여 슬래시(/)가 포함된 한국어 필드 행을 추출한다."""
    terms_with_slashes = []
    if not os.path.exists(csv_path):
        print(f"[⚠️ warning] {csv_path} 파일을 찾을 수 없어 빌트인 검사만 실행합니다.")
        return terms_with_slashes
        
    try:
        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader, None) # 헤더 건너뛰기
            for row in reader:
                if len(row) < 4:
                    continue
                german = row[0].strip()
                english = row[1].strip()
                korean = row[3].strip()
                if "/" in korean:
                    parts = [p.strip() for p in korean.split("/") if p.strip()]
                    # 흔히 쓰이는 일반 명사들이 포함되어 오감지되는 것을 막기 위한 필터
                    EXCLUDED_COMMON_WORDS = {"사람", "이름", "언어", "예언", "창조", "축복"}
                    parts = [p for p in parts if len(p) >= 2 and p not in EXCLUDED_COMMON_WORDS]
                    if len(parts) >= 2:
                        terms_with_slashes.append({
                            "german": german,
                            "english": english,
                            "korean_raw": korean,
                            "parts": parts
                        })
    except Exception as e:
        print(f"[⚠️ error] tre_terms.csv 로딩 중 오류 발생: {e}", file=sys.stderr)
    return terms_with_slashes

def audit_purity(content: str) -> Tuple[int, List[str]]:
    """학술적 순수성 보존 검사 (개발 잔재물 감출)"""
    score_deduction = 0
    issues = []
    
    # 1. 개발/리서치 헤더 감지
    forbidden_headers = [
        "### Appendix: Research Inventory",
        "### Forensic Audit Log"
    ]
    for header in forbidden_headers:
        if header in content:
            score_deduction += 15
            issues.append(f"학술적 순수성 위배: 본문 하단에 제거되지 않은 개발 세션 헤더 `{header}`가 발견되었다.")
            
    # 2. 미치환 임시 앵커 감지
    unreplaced_refs = re.findall(r'\[Ref:\s*([^\]\n]+)\]', content)
    if unreplaced_refs:
        score_deduction += 10 * len(unreplaced_refs)
        issues.append(f"인용 오류: 본문에 치환되지 않고 그대로 방치된 임시 앵커 [Ref: ...] {len(unreplaced_refs)}개가 발견되었다.")
        for ref in unreplaced_refs[:3]:
            issues.append(f"  - 미치환 예: `[Ref: {ref}]`")
            
    return score_deduction, issues

def audit_footnotes(content: str) -> Tuple[int, List[str]]:
    """각주 정합성 및 1대1 매핑 검사"""
    score_deduction = 0
    issues = []
    
    # 1. 본문 내 각주 호출 지점 찾기 ([^N], 단 [^N]: 은 정의이므로 제외)
    # 본문 호출 지점 매칭 정규식 (앞에 콜론 : 이 안 붙은 것)
    calls = []
    # 라인 단위로 찾기
    lines = content.split('\n')
    for line_idx, line in enumerate(lines, 1):
        # [^N] 패턴 매칭 (정의가 아닌 호출부)
        matches = re.finditer(r'(?<!^)(?<!\n)\[\^(\d+)\](?!:)', line)
        for m in matches:
            calls.append((int(m.group(1)), line_idx))
            
    # 2. 문서 최하단 각주 정의 찾기 ([^N]: )
    definitions = {}
    for line_idx, line in enumerate(lines, 1):
        match = re.match(r'^\[\^(\d+)\]:\s*(.+)$', line)
        if match:
            definitions[int(match.group(1))] = (line_idx, match.group(2).strip())
            
    call_numbers = [c[0] for c in calls]
    def_numbers = list(definitions.keys())
    
    # 3. 1대1 매핑 검증
    # 3-1. 호출되었으나 정의가 없는 각주
    missing_defs = [num for num in call_numbers if num not in def_numbers]
    if missing_defs:
        score_deduction += 15 * len(missing_defs)
        issues.append(f"각주 정의 누락: 본문에서 호출되었으나 실제 정의가 제공되지 않는 각주 번호가 존재한다: {missing_defs}")
        
    # 3-2. 정의는 있으나 본문에서 호출되지 않는 각주
    unused_defs = [num for num in def_numbers if num not in call_numbers]
    if unused_defs:
        score_deduction += 5 * len(unused_defs)
        issues.append(f"미사용 각주 정의: 정의는 작성되었으나 본문에서 실제 호출되지 않는 각주가 존재한다: {unused_defs}")
        
    # 3-3. 각주 넘버링의 순차성 및 연속성 검증 (중복 호출 및 순서 어긋남 정밀 점검)
    if call_numbers:
        # 1. 1번부터 시작하는지 확인
        if call_numbers[0] != 1:
            score_deduction += 10
            issues.append(f"각주 번호 정합성: 본문 첫 각주 번호가 1번이 아닌 {call_numbers[0]}번으로 시작하고 있다.")
            
        # 2. 본문에서 등장하는 순서대로 1, 2, 3... 순차적이고 연속적인지 확인
        expected = 1
        seen_calls = set()
        for idx, (num, line_idx) in enumerate(calls):
            if num in seen_calls:
                score_deduction += 5
                issues.append(f"각주 번호 중복 호출: 본문 내에서 각주 번호 `{num}`번이 중복 호출되었다. (라인: {line_idx})")
            else:
                seen_calls.add(num)
                if num != expected:
                    score_deduction += 10
                    issues.append(f"각주 순차적 넘버링 위배: {idx+1}번째로 등장한 각주 번호가 `{num}`이다. (예상: `{expected}`, 라인: {line_idx})")
                expected += 1
                
    return score_deduction, issues

def audit_terminology(content: str, tre_candidates: List[Dict]) -> Tuple[int, List[str]]:
    """신학 용어 일관성 분열(Equivocation) 검사"""
    score_deduction = 0
    issues = []
    
    # 참고문헌 섹션 이전 본문만 검사 대상에 포함 (각주 정의 라인도 제외)
    lines = []
    for line in content.split('\n'):
        if line.strip().startswith("## 참고문헌") or line.strip().startswith("## Bibliography") or line.strip().startswith("## References"):
            break
        if re.match(r'^\[\^(\d+)\]:\s*', line.strip()):
            continue
        lines.append(line)
    
    # 1. tre_terms.csv 슬래시 분리어 검사
    for item in tre_candidates:
        detected_parts = {}
        # 긴 파트부터 검사하기 위해 정렬
        sorted_parts = sorted(item["parts"], key=len, reverse=True)
        occurrences_by_part = {part: [] for part in item["parts"]}
        
        for line_idx, line in enumerate(lines, 1):
            temp_line = line
            for part in sorted_parts:
                if part in temp_line:
                    occurrences_by_part[part].append((line_idx, line.strip()))
                    temp_line = temp_line.replace(part, " ")
                    
        for part, occs in occurrences_by_part.items():
            if occs:
                detected_parts[part] = occs
                
        if len(detected_parts) >= 2:
            score_deduction += 8
            parts_str = ", ".join(f"`{k}`" for k in detected_parts.keys())
            issues.append(f"용어 일관성 결여 (TRE 표준): 신학 개념 `{item['german']} ({item['english']})`에 대해 대체 가능한 표기법 {parts_str}이 혼용되었다.")
            
    # 2. 빌트인 공통 혼용어 검사
    for concept, parts in COMMON_EQUIVOCATIONS.items():
        detected_parts = {}
        sorted_parts = sorted(parts, key=len, reverse=True)
        occurrences_by_part = {part: [] for part in parts}
        
        for line_idx, line in enumerate(lines, 1):
            temp_line = line
            for part in sorted_parts:
                if part in temp_line:
                    occurrences_by_part[part].append((line_idx, line.strip()))
                    temp_line = temp_line.replace(part, " ")
                    
        for part, occs in occurrences_by_part.items():
            if occs:
                detected_parts[part] = occs
                
        if len(detected_parts) >= 2:
            score_deduction += 5
            parts_str = ", ".join(f"`{k}`" for k in detected_parts.keys())
            issues.append(f"용어 일관성 결여 (빌트인): 개념 `{concept}`에 대해 표기법 {parts_str}이 문서 전체에 걸쳐 혼용되었다.")
            
    return score_deduction, issues

def audit_layout(content: str) -> Tuple[int, List[str]]:
    """가로선 잔재 및 레이아웃 정합성 검사"""
    score_deduction = 0
    issues = []
    
    # 1. 연속된 가로선 검출
    if re.search(r'---\s*\n+---\s*', content):
        score_deduction += 8
        issues.append("레이아웃 정합성 위배: 문서 하단에 중복되거나 비어 있는 가로선(---) 결합이 감지되었다.")
        
    # 2. 다중 빈 줄 검출 (3개 이상의 연속 개행)
    if re.search(r'\n{4,}', content):
        score_deduction += 5
        issues.append("포맷 지침 위배: 3개 이상의 불필요한 연속 빈 줄이 존재하여 문서 레이아웃이 훼손되었다.")
        
    # 3. 참고문헌의 Cited/General 분리 구조 검증
    # (한국어 문서일 경우 '참고문헌' 아래에 '인용 문헌'과 '일반 참고 문헌'이 하위 제목으로 존재하는지 검사)
    kor_chars = len(re.findall(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', content))
    is_korean_essay = kor_chars > 100
    
    if is_korean_essay:
        if "## 참고문헌" in content:
            if "### 인용 문헌" not in content and "### 일반 참고 문헌" not in content:
                score_deduction += 10
                issues.append("참고문헌 포맷 지침 위배: `## 참고문헌` 하위에 `### 인용 문헌` 및 `### 일반 참고 문헌` 세부 분류가 존재하지 않는다. (이원화 구성 누락)")
    else:
        if "## Bibliography" in content or "## References" in content:
            if "### Cited Works" not in content and "### General References" not in content:
                score_deduction += 10
                issues.append("참고문헌 포맷 지침 위배: Bibliography 하위에 `### Cited Works` 및 `### General References` 세부 분류가 존재하지 않는다. (이원화 구성 누락)")
                
    return score_deduction, issues

def main():
    parser = argparse.ArgumentParser(description="TAWP 통합 감사 및 검수 엔진 (Unified Audit Engine)")
    parser.add_argument("-f", "--file", required=True, help="감사 대상 마크다운 에세이 경로")
    parser.add_argument("-o", "--output", help="감사 보고서 출력 경로")
    parser.add_argument("--csv", default=os.path.expanduser("~/Desktop/MS_Dev.nosync/data/tre_terms.csv"), help="tre_terms.csv 경로")
    parser.add_argument("--halt-on-fail", action="store_true", help="검수 점수가 80점 미만일 경우 프로세스를 에러 코드로 중단")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"[❌ Error] 검사 대상 파일을 찾을 수 없습니다: {args.file}", file=sys.stderr)
        sys.exit(1)
        
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
        
    print(f"🕵️ TAWP 7-Stage Audit 엔진을 기동합니다. 대상 문서: {os.path.basename(args.file)}")
    
    # 1. 각 카테고리별 검수 수행
    purity_deduction, purity_issues = audit_purity(content)
    footnote_deduction, footnote_issues = audit_footnotes(content)
    
    tre_candidates = load_tre_terms(args.csv)
    term_deduction, term_issues = audit_terminology(content, tre_candidates)
    
    layout_deduction, layout_issues = audit_layout(content)
    
    # 2. 종합 검수 스코어 산출
    total_deductions = purity_deduction + footnote_deduction + term_deduction + layout_deduction
    audit_score = max(0, 100 - total_deductions)
    
    # 3. 마크다운 보고서 빌드
    report = []
    report.append(f"# 🏛️ TAWP 통합 감사 보고서 (Unified Audit Report)")
    report.append("")
    report.append("본 보고서는 신학 학술 글쓰기 헌법(Rule 4) 및 SBL 2nd 인용 표준 규격을 기준으로 생성 에세이의 논리적 정합성 및 양식 결함을 정밀 검증한 종합 진단서이다.")
    report.append("")
    report.append("## 📊 종합 검수 등급")
    report.append("")
    
    status_emoji = "🟢 PASS" if audit_score >= 80 else "🔴 FAIL"
    report.append(f"- **최종 평가 점수**: **{audit_score}점** / 100점 ({status_emoji})")
    report.append(f"- **대상 파일**: `{os.path.basename(args.file)}`")
    report.append(f"- **진단 요약**: 총 {len(purity_issues) + len(footnote_issues) + len(term_issues) + len(layout_issues)}건의 잠재적 양식 또는 일관성 결함이 감지되었다.")
    report.append("")
    
    # 세부 진단 결과
    report.append("## 🔍 영역별 세부 진단 내역")
    report.append("")
    
    # 학술적 순수성 보존 영역
    report.append("### 1. 학술적 순수성 보존 및 인용 앵커")
    if purity_issues:
        report.append(f"- ⚠️ 감점 **-{purity_deduction}점**")
        for issue in purity_issues:
            report.append(f"  - {issue}")
    else:
        report.append("- ✅ 무결함 (본문 외 리서치 인벤토리 및 포렌식 로그 격리 완수)")
    report.append("")
    
    # 각주 및 정의 결합 영역
    report.append("### 2. SBL 각주 색인 및 1대1 매핑")
    if footnote_issues:
        report.append(f"- ⚠️ 감점 **-{footnote_deduction}점**")
        for issue in footnote_issues:
            report.append(f"  - {issue}")
    else:
        report.append("- ✅ 무결함 (본문 각주 호출 및 최하단 정의 100% 매핑 정합)")
    report.append("")
    
    # 용어 일관성 영역
    report.append("### 3. 신학 전문 용어 번역 일관성")
    if term_issues:
        report.append(f"- ⚠️ 감점 **-{term_deduction}점**")
        for issue in term_issues:
            report.append(f"  - {issue}")
    else:
        report.append("- ✅ 무결함 (의미론적 일관성 확보 및 단일 용어 역어 유지)")
    report.append("")
    
    # 레이아웃 정합성 영역
    report.append("### 4. 문서 레이아웃 및 참고문헌 이원화 양식")
    if layout_issues:
        report.append(f"- ⚠️ 감점 **-{layout_deduction}점**")
        for issue in layout_issues:
            report.append(f"  - {issue}")
    else:
        report.append("- ✅ 무결함 (참고문헌 Cited/General 이원화 포맷팅 준수 및 레이아웃 청결)")
    report.append("")
    
    report.append("## ✍️ 교정 및 교수학습 권고 사항")
    report.append("")
    if audit_score >= 80:
        report.append("본 문서는 TAWP 최종 헌법을 충족하며 학술적 정합성이 확보된 우수한 텍스트이다. 즉시 발행 및 PDF 컴파일러 이관이 권장된다.")
    else:
        report.append("감점 사유에 명시된 지점들을 수정하여 문서를 재정화할 것을 권고한다. 특히 미치환 인용 앵커나 각주 번호 결함은 최종 학술본 인쇄 시 심각한 컴파일 실패를 야기한다.")
        
    report_content = "\n".join(report)
    
    # 보고서 출력
    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(args.file)
        # _terminology_audit.md 대신에 통합 감사 로그로 _audit_report.md 생성
        output_path = f"{base}_audit_report.md"
        
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"💾 TAWP 통합 감사 보고서 생성 완료: {output_path}")
    except Exception as e:
        print(f"[❌ Error] 감사 보고서 저장 실패: {e}", file=sys.stderr)
        
    # 점수 기준 프로세스 제어
    if args.halt_on_fail and audit_score < 80:
        print(f"[🔴 Halt] TAWP Audit Gate가 빌드를 중단했습니다. 검수 점수가 기준점(80점) 미만입니다. 점수: {audit_score}점", file=sys.stderr)
        sys.exit(1)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
