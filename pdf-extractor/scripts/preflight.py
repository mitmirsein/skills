#!/usr/bin/env python3
"""
preflight.py — PDF 추출 전(前) 경량 라우팅 탐지기 (Pre-flight Triage)
====================================================================

무거운 구조 파싱을 수행하기 전, PDF의 첫 3페이지만 고속 0.2초 스캔하여
텍스트 상태를 분석하고 최적의 추출 경로(Core vs Elite Vision)를 제안합니다.

[판단 기준]
1. Text-less (스캔본): 텍스트가 거의 없으면 -> VISION 강제
2. Noise-heavy (깨짐): 자음 분리, 고아 괄호 비율이 임계치 초과 시 -> VISION 제안
3. Clean (정상): 한국어 위주, 노이즈 적음 -> CORE 파싱
"""

import sys
import re
import json
import argparse
try:
    from pypdf import PdfReader
except ImportError:
    print("❌ Error: pypdf 패키지가 설치되지 않았습니다. 'uv add pypdf' 또는 "
          "requirements.txt 설치를 실행하세요.", file=sys.stderr)
    sys.exit(2)

def analyze_pdf(file_path):
    print(f"🛫 Pre-flight Scan 가동 중: {file_path}", file=sys.stderr)
    try:
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)
        scan_limit = min(3, num_pages)  # 최대 3페이지만 훑어봄
        
        extracted_text = ""
        for i in range(scan_limit):
            text = reader.pages[i].extract_text()
            if text:
                extracted_text += text + "\n"
        
        total_chars = len(extracted_text.strip())
        
        # 1. 스캔본 판독
        if total_chars < 150:
            return {
                "route": "VISION",
                "route_code": "VISION",
                "reason": f"텍스트 레이어가 거의 비어 있습니다 (분석량: {total_chars}자). 이미지 스캔본이 확실합니다.",
                "action": "Elite Vision 모드로 즉시 직행하십시오.",
                "metrics": {"pages_scanned": scan_limit, "total_chars": total_chars},
            }
            
        # 2. 노이즈 레벨 측정
        # 패턴 1: 고아 괄호 (예: ( 123 ) 또는 ( a ))
        orphan_brackets = len(re.findall(r'\(\s*\d+\s*\)', extracted_text))
        orphan_brackets += len(re.findall(r'\([a-zA-Z]\)', extracted_text))
        
        # 패턴 2: 외래어 자음 분리 (예: v o n, G o t t - 공백 문자가 연속된 철자들)
        spaced_chars = len(re.findall(r'[a-zA-Z] [a-zA-Z] [a-zA-Z]', extracted_text))
        
        noise_score = orphan_brackets + (spaced_chars * 2)
        
        print(f"📊 스캔 리포트: 총 {total_chars}자 / 노이즈 스코어 {noise_score}",
              file=sys.stderr)
        
        metrics = {
            "pages_scanned": scan_limit,
            "total_chars": total_chars,
            "orphan_brackets": orphan_brackets,
            "spaced_chars": spaced_chars,
            "noise_score": noise_score,
            "noise_threshold": 15,
        }

        if noise_score > 15:
            return {
                "route": "VISION (Suggested)",
                "route_code": "VISION",
                "reason": f"고위험군 노이즈(외래어 자음 분리, 고아 괄호 등) 집중 발견 (스코어: {noise_score}). 파싱 시 텍스트 붕괴 예상.",
                "action": "Elite Vision 모드 가동을 제안합니다.",
                "metrics": metrics,
            }
        else:
            return {
                "route": "CORE",
                "route_code": "CORE",
                "reason": f"텍스트 레이어가 양호합니다 (노이즈 평점: {noise_score}).",
                "action": "기본 파싱 엔진(extract_pdf.py)으로 진행하십시오.",
                "metrics": metrics,
            }

    except Exception as e:
        return {
            "route": "VISION",
            "route_code": "VISION",
            "reason": f"PDF 텍스트 레이어 접근 실패 ({str(e)})",
            "action": "Elite Vision 모드로 즉시 직행하십시오.",
            "metrics": {"error": str(e)},
        }

def main():
    parser = argparse.ArgumentParser(description="PDF 추출 전 Triage 스캐너")
    parser.add_argument("pdf_path", help="분석할 PDF 파일 경로")
    parser.add_argument(
        "--json", action="store_true",
        help="결과를 JSON으로 stdout에 출력 (에이전트 자동 라우팅용). "
             "진단 로그는 stderr로 분리됨.",
    )
    args = parser.parse_args()

    result = analyze_pdf(args.pdf_path)

    if args.json:
        # stdout = 순수 JSON (route_code ∈ {CORE, VISION} 로 분기)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("─────────────────────────────────────────────────────")
    print(f"🚦 판정 결과: {result['route']}")
    print(f"📝 판단 사유: {result['reason']}")
    print(f"🎯 권장 조치: {result['action']}")
    print("─────────────────────────────────────────────────────")

if __name__ == "__main__":
    main()
