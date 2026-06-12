#!/usr/bin/env python3
import os
import sys
import argparse

# 프레임워크 경로 추가
FRAMEWORK_DIR = os.path.expanduser("~/Desktop/MS_Dev.nosync/projects/omni-academic-framework")
if FRAMEWORK_DIR not in sys.path:
    sys.path.append(FRAMEWORK_DIR)

from src.analyze.lens_analyzer import LensAnalyzer, LensAnalysisReport

def get_llm_provider(use_mock: bool, api_key: str = None):
    if use_mock:
        from src.llm.provider import MockProvider
        return MockProvider()
    
    actual_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not actual_key:
        print("[⚠️ warning] ANTHROPIC_API_KEY가 없으므로 Mock LLM Provider를 강제 사용합니다.")
        from src.llm.provider import MockProvider
        return MockProvider()
    
    from src.llm.provider import AnthropicProvider
    return AnthropicProvider(api_key=actual_key)

def translate_mock_text(text: str) -> str:
    """Mock 데이터의 영어 텍스트를 한국어 평서문으로 보정하여 규칙을 준수한다."""
    translations = {
        "Mock LLM analysis generated from real paragraph anchors.": "실제 문단 앵커로부터 모의 LLM 분석을 생성한다.",
        "Mock source-bound analysis for pipeline verification.": "파이프라인 검증을 위한 원문 기반의 모의 분석을 수행한다.",
        "MockProvider output is not interpretive analysis.": "MockProvider의 출력은 해석적 분석이 아니며 파이프라인 검증만을 목적으로 한다.",
        "Mock Focus 1": "모의 분석 항목 1",
        "Mock Focus 2": "모의 분석 항목 2",
        "Mock Focus 3": "모의 분석 항목 3",
        "Mock Focus 4": "모의 분석 항목 4"
    }
    return translations.get(text, text)

def render_exegesis_report(reports: list[LensAnalysisReport]) -> str:
    """4대 렌즈 분석 리포트를 종합하여 하나의 한국어 평서문 마크다운 보고서로 렌더링한다."""
    lines = []
    lines.append("# 📖 신학 석의 종합 보고서 (Theological Exegesis Report)")
    lines.append("")
    lines.append("본 보고서는 성서학, 조직신학, 역사신학, 실천신학의 4대 학술 렌즈를 적용하여 본문을 다차원적으로 석의하고 평가한 결과이다.")
    lines.append("각 분과별 분석은 텍스트의 고유한 맥락과 사상적 긴장을 훼손하지 않는 범위 내에서 상호 교차 검토를 통하여 수행된다.")
    lines.append("")

    for report in reports:
        lens_display = {
            "biblical": "성서학 렌즈 (Biblical Studies Lens)",
            "systematic": "조직신학 렌즈 (Systematic Theology Lens)",
            "historical": "역사신학 렌즈 (Historical Theology Lens)",
            "practical": "실천신학 렌즈 (Practical Theology Lens)"
        }.get(report.lens, f"{report.lens.capitalize()} 렌즈")
        
        lines.append(f"## 🎯 {lens_display}")
        lines.append("")
        
        # 요약
        summary = translate_mock_text(report.executive_summary)
        lines.append(f"### 1. 개요 및 요약")
        lines.append(summary)
        lines.append("")
        
        # 발견점
        lines.append(f"### 2. 핵심 분석 및 텍스트 근거 (Findings)")
        if report.findings:
            for finding in report.findings:
                focus_area = translate_mock_text(finding.focus_area)
                analysis_text = translate_mock_text(finding.analysis)
                lines.append(f"#### 🔍 {focus_area} ({finding.paragraph_id})")
                lines.append(f"> {finding.source_quote}")
                lines.append("")
                lines.append(analysis_text)
                lines.append("")
        else:
            lines.append("해당 렌즈에서 감지된 핵심 분석 결과가 존재하지 않는다.")
            lines.append("")
            
        # 한계점
        lines.append(f"### 3. 해석학적 한계 및 아포리아 (Limitations)")
        if report.limitations:
            for lim in report.limitations:
                lim_text = translate_mock_text(lim)
                lines.append(f"- {lim_text}")
        else:
            lines.append("- 감지된 명시적인 해석학적 한계가 존재하지 않는다.")
        lines.append("")
        lines.append("---")
        lines.append("")
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="4대 신학 렌즈 기반 정밀 주해 분석 실행 도구")
    parser.add_argument("-f", "--file", required=True, help="분석 대상 신학 마크다운 문서 경로")
    parser.add_argument("-o", "--output", help="출력할 분석 보고서 경로")
    parser.add_argument("--mock", action="store_true", help="LLM 호출 없이 Mock 데이터로 실행 테스트 수행")
    parser.add_argument("--api-key", help="Anthropic API Key")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"[❌ Error] 대상 파일이 존재하지 않습니다: {args.file}")
        sys.exit(1)
        
    print(f"📖 문서 주해 분석을 준비 중입니다: {args.file}")
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
        
    provider = get_llm_provider(args.mock, args.api_key)
    
    # 4대 렌즈 리스트
    lenses = ["biblical", "systematic", "historical", "practical"]
    
    # theology-exegesis 스킬 내 lenses 폴더 경로 지정
    lens_dir = os.path.expanduser("~/Desktop/MS_Dev.nosync/.skills/theology-exegesis/lenses")
    analyzer = LensAnalyzer(lens_dir=lens_dir)
    
    reports = []
    for lens in lenses:
        print(f"🎯 [{lens.capitalize()}] 렌즈 분석을 실행합니다...")
        try:
            report = analyzer.build_llm_analysis(content, lens, provider)
            reports.append(report)
        except Exception as e:
            print(f"[❌ Error] {lens} 렌즈 분석 중 오류 발생: {e}")
            sys.exit(1)
            
    # 최종 보고서 렌더링
    final_report = render_exegesis_report(reports)
    
    # 출력 경로 결정
    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(args.file)
        output_path = f"{base}_exegesis.md"
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_report)
        
    print(f"💾 신학 석의 종합 보고서가 생성되었습니다: {output_path}")

if __name__ == "__main__":
    main()
