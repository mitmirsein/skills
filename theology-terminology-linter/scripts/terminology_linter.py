#!/usr/bin/env python3
import os
import sys
import csv
import argparse

COMMON_EQUIVOCATIONS = {
    "칭의 / 의인": ["칭의", "의인"],
    "기독론 / 그리스도론": ["기독론", "그리스도론"],
    "성만찬 / 성찬식 / 성찬 예식": ["성만찬", "성찬식", "성찬 예식"],
    "하나님 / 하느님": ["하나님", "하느님"],
    "여호와 / 야훼": ["여호와", "야훼"],
    "개혁주의 / 칼빈주의": ["개혁주의", "칼빈주의"],
    "계시 / 묵시 / 아포칼립스": ["계시", "묵시", "아포칼립스"]
}

def load_tre_terms(csv_path: str) -> list:
    """tre_terms.csv 파일을 로드하여 슬래시(/)가 포함된 한국어 필드 행을 추출한다."""
    terms_with_slashes = []
    if not os.path.exists(csv_path):
        print(f"[⚠️ warning] {csv_path} 파일을 찾을 수 없어 빌트인 검사만 실행합니다.")
        return terms_with_slashes
        
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
                # 슬래시로 쪼개기
                parts = [p.strip() for p in korean.split("/") if p.strip()]
                # 각 파트가 빈칸이 아니고 2글자 이상인 것만 필터링
                parts = [p for p in parts if len(p) >= 2]
                if len(parts) >= 2:
                    terms_with_slashes.append({
                        "german": german,
                        "english": english,
                        "korean_raw": korean,
                        "parts": parts
                    })
    return terms_with_slashes

def scan_file_for_terms(file_path: str, all_candidates: list) -> dict:
    """문서를 읽어서 라인별로 용어를 스캔하여 일관성 붕괴(Equivocation)를 검출한다."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    warnings = []
    
    # 1. tre_terms.csv 슬래시 분리어 검사
    for item in all_candidates:
        detected_parts = {}
        for part in item["parts"]:
            occurrences = []
            for line_idx, line in enumerate(lines, 1):
                if part in line:
                    occurrences.append((line_idx, line.strip()))
            if occurrences:
                detected_parts[part] = occurrences
                
        # 2개 이상의 대체 역어가 동시에 검출된 경우 경고
        if len(detected_parts) >= 2:
            warnings.append({
                "type": "tre_term",
                "concept": f"{item['german']} ({item['english']})",
                "detected": detected_parts
            })
            
    # 2. 빌트인 공통 혼용어 검사
    for concept, parts in COMMON_EQUIVOCATIONS.items():
        detected_parts = {}
        for part in parts:
            occurrences = []
            for line_idx, line in enumerate(lines, 1):
                if part in line:
                    occurrences.append((line_idx, line.strip()))
            if occurrences:
                detected_parts[part] = occurrences
                
        if len(detected_parts) >= 2:
            warnings.append({
                "type": "builtin",
                "concept": concept,
                "detected": detected_parts
            })
            
    return {
        "warnings": warnings,
        "total_lines": len(lines)
    }

def generate_linter_report(scan_results: dict, target_file: str) -> str:
    """한국어 평서문 어조를 준수하는 용어 일관성 검사 보고서 마크다운을 렌더링한다."""
    lines = []
    lines.append("# 🔍 신학 용어 일관성 검사 보고서 (Theological Terminology Linter Report)")
    lines.append("")
    lines.append("본 보고서는 `tre_terms.csv`에 등록된 신학 전문 용어 및 공통 혼용어 목록을 기준으로 문서 내 의미 일관성 붕괴(Equivocation) 현상을 진단한 결과이다.")
    lines.append(f"대상 문서: `{os.path.basename(target_file)}` (총 {scan_results['total_lines']}행)")
    lines.append("")
    
    warnings = scan_results["warnings"]
    if not warnings:
        lines.append("## 🎉 진단 결과: 우수")
        lines.append("문서 내에서 검사 대상 신학 용어의 일관성 분열이나 번역어 혼용이 감지되지 않았다.")
        return "\n".join(lines)
        
    lines.append(f"## ⚠️ 일관성 붕괴 경고 (총 {len(warnings)}건)")
    lines.append("동일한 신학적 개념에 대하여 서로 다른 번역어나 표기법이 혼용되는 현상이 감지되었다. 개념의 명료성을 위해 일관된 용어로 수정할 것을 권고한다. (단, 강제적인 자동 치환은 수행하지 않는다.)")
    lines.append("")
    
    for idx, w in enumerate(warnings, 1):
        lines.append(f"### [{idx}] {w['concept']} 개념의 혼용")
        lines.append(f"- **이슈 유형**: {'TRE 표준 용어 분열' if w['type'] == 'tre_term' else '신학 일반 혼용어'}")
        lines.append("- **감지된 혼용 단어 및 검출 행 번호**:")
        for part, occurrences in w["detected"].items():
            line_numbers = ", ".join(str(o[0]) for o in occurrences[:5])
            if len(occurrences) > 5:
                line_numbers += " 외"
            lines.append(f"  - `{part}`: {line_numbers}행")
        lines.append("- **세부 위치 및 문맥 예시**:")
        for part, occurrences in w["detected"].items():
            for line_idx, line_text in occurrences[:2]:  # 각 단어당 최대 2개 예시만 출력
                if len(line_text) > 80:
                    line_text = line_text[:77] + "..."
                lines.append(f"  - `{line_idx}행`: \"{line_text}\"")
        lines.append("")
        lines.append("---")
        lines.append("")
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="신학 용어 일관성 린터 스크립트")
    parser.add_argument("-f", "--file", required=True, help="분석 대상 신학 마크다운 문서 경로")
    parser.add_argument("-o", "--output", help="출력할 분석 보고서 경로")
    parser.add_argument("--csv", default=os.path.expanduser("~/Desktop/MS_Dev.nosync/data/tre_terms.csv"), help="tre_terms.csv 경로")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"[❌ Error] 대상 파일이 존재하지 않습니다: {args.file}")
        sys.exit(1)
        
    print(f"📖 문서 용어 스캔을 준비 중입니다: {args.file}")
    
    # 1. 용어 로드
    tre_candidates = load_tre_terms(args.csv)
    print(f"📌 tre_terms.csv에서 슬래시(/) 분리 용어 {len(tre_candidates)}개를 추출하여 로드했습니다.")
    
    # 2. 문서 검사
    results = scan_file_for_terms(args.file, tre_candidates)
    
    # 3. 리포트 생성
    report_md = generate_linter_report(results, args.file)
    
    # 4. 파일 쓰기
    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(args.file)
        output_path = f"{base}_terminology_audit.md"
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_md)
        
    print(f"💾 용어 일관성 검사 보고서가 생성되었습니다: {output_path}")

if __name__ == "__main__":
    main()
