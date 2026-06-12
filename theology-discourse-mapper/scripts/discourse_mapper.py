#!/usr/bin/env python3
import os
import sys
import re
import argparse
import json
from typing import Dict, List, Tuple

# 프레임워크 경로 추가
FRAMEWORK_DIR = os.path.expanduser("~/Desktop/MS_Dev.nosync/projects/omni-academic-framework")
if FRAMEWORK_DIR not in sys.path:
    sys.path.append(FRAMEWORK_DIR)

from src.text.paragraphs import assign_paragraph_ids
from src.ontology.extractor import EntityClass, RelationPredicate, Node, Edge, OntologyMap

def get_llm_provider(use_mock: bool, api_key: str = None):
    """지정된 모드에 맞는 LLM Provider를 생성한다."""
    if use_mock:
        from src.llm.provider import MockProvider
        return MockProvider()
    
    # API 키 검색 순서: 1) 매개변수 2) 환경변수
    actual_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not actual_key:
        print("[⚠️ warning] ANTHROPIC_API_KEY가 없으므로 Mock LLM Provider를 강제 사용합니다.")
        from src.llm.provider import MockProvider
        return MockProvider()
    
    from src.llm.provider import AnthropicProvider
    return AnthropicProvider(api_key=actual_key)

def build_mermaid_graph(ontology_map: OntologyMap) -> str:
    """OntologyMap을 정밀 스타일링이 적용된 Mermaid 그래프 코드로 변환한다."""
    lines = ["graph TD"]
    
    # 노드 클래스별 색상/스타일 정의 (Harmonious curated colors)
    # Concept: #f5f5f5, Actor: #e0f7fa, Method: #e8f5e9, Claim: #fff3e0, Artifact: #f3e5f5, Context: #efebe9, Limitation: #ffebee
    styles = {
        EntityClass.CONCEPT: "fill:#eceff1,stroke:#37474f,stroke-width:2px,color:#263238",
        EntityClass.ACTOR: "fill:#e0f7fa,stroke:#00838f,stroke-width:2px,color:#006064,font-weight:bold",
        EntityClass.METHOD: "fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20",
        EntityClass.CLAIM: "fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#e65100",
        EntityClass.ARTIFACT: "fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#4a148c",
        EntityClass.CONTEXT: "fill:#efebe9,stroke:#4e342e,stroke-width:2px,color:#3e2723",
        EntityClass.LIMITATION: "fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#b71c1c"
    }
    
    # 노드 형태 정의 함수
    def format_node_shape(node: Node) -> str:
        label_escaped = node.label.replace('"', '\\"')
        if node.entity_class == EntityClass.CONCEPT:
            return f'{node.id}(["{label_escaped}"])'
        elif node.entity_class == EntityClass.ACTOR:
            return f'{node.id}(({{"{label_escaped}"}}))'
        elif node.entity_class == EntityClass.METHOD:
            return f'{node.id}[/"{label_escaped}"/]'
        elif node.entity_class == EntityClass.CLAIM:
            return f'{node.id}["{label_escaped}"]'
        elif node.entity_class == EntityClass.ARTIFACT:
            return f'{node.id}[\\"{label_escaped}"\\]'
        elif node.entity_class == EntityClass.CONTEXT:
            return f'{node.id}(("{label_escaped}"))'
        elif node.entity_class == EntityClass.LIMITATION:
            return f'{node.id}{{"{label_escaped}"}}'
        return f'{node.id}["{label_escaped}"]'

    # 노드 선언 및 모양 설정
    for node in ontology_map.nodes:
        lines.append(f"    {format_node_shape(node)}")
        
    # 엣지 선언 (관계 방향 및 텍스트 추가)
    for edge in ontology_map.edges:
        pred_label = edge.predicate.value
        lines.append(f"    {edge.source_id} -->|{pred_label}| {edge.target_id}")
        
    # 노드 스타일 강제 주입
    for i, node in enumerate(ontology_map.nodes):
        style = styles.get(node.entity_class, "fill:#fff,stroke:#333")
        lines.append(f"    style {node.id} {style}")
        
    return "\n".join(lines)

def build_discourse_report(ontology_map: OntologyMap, original_text: str) -> str:
    """추출된 온톨로지 정보를 바탕으로 학술 대립 및 담론 보고서를 한국어 평서문으로 작성한다."""
    report = []
    report.append("# 🕸️ 신학 담론 구조 보고서 (Theological Discourse Report)")
    report.append("")
    report.append("## 1. 개요 및 온톨로지 현황")
    report.append(f"본 보고서는 입력 텍스트에서 학자들의 논쟁, 핵심 개념 및 주장 관계를 구조적으로 분석한 결과이다.")
    report.append(f"추출된 총 노드 수는 {len(ontology_map.nodes)}개이며, 총 엣지(관계) 수는 {len(ontology_map.edges)}개이다.")
    report.append("")
    
    # 2. 학자 간 대립 구도 분석 (Actor-Claim-Conflict)
    report.append("## 2. 학자 및 주장 대립 지형도")
    actors = [n for n in ontology_map.nodes if n.entity_class == EntityClass.ACTOR]
    claims = [n for n in ontology_map.nodes if n.entity_class == EntityClass.CLAIM]
    limitations = [n for n in ontology_map.nodes if n.entity_class == EntityClass.LIMITATION]
    
    node_dict = {n.id: n for n in ontology_map.nodes}
    
    # 대립 관계(conflicts_with) 추출 및 서술
    conflict_edges = [e for e in ontology_map.edges if e.predicate == RelationPredicate.CONFLICTS_WITH]
    
    if conflict_edges:
        report.append("학설 및 텍스트 해석학적 대립 구도는 다음과 같다.")
        for edge in conflict_edges:
            src = node_dict.get(edge.source_id)
            tgt = node_dict.get(edge.target_id)
            if src and tgt:
                report.append(f"- **{src.label}** (대립범주: {src.entity_class.value}) ─── 〈대립〉 ─── **{tgt.label}** (대립범주: {tgt.entity_class.value})")
                report.append(f"  - **관계 성립 근거**: {edge.reasoning}")
                if edge.source_quote:
                    report.append(f"  - **텍스트 근거**: \"{edge.source_quote}\"")
                report.append("")
    else:
        report.append("본 텍스트 내에서 명시적인 학설/주장 간의 conflicts_with 대립 관계는 감지되지 않았다.")
        report.append("")

    # 3. 학파/학자별 세부 주장 요약
    report.append("## 3. 핵심 행위자(Actor) 및 주장 구조 분석")
    if actors:
        for actor in actors:
            report.append(f"### 👤 학자: {actor.label}")
            if actor.source_quote:
                report.append(f"- **텍스트 기원**: \"{actor.source_quote}\" (문단 ID: {actor.paragraph_id})")
            
            # 이 학자로부터 출발하거나 이 학자에게 향하는 엣지 분석
            actor_edges_out = [e for e in ontology_map.edges if e.source_id == actor.id]
            actor_edges_in = [e for e in ontology_map.edges if e.target_id == actor.id]
            
            if actor_edges_out:
                report.append("- **관계 엣지 (Outflow)**:")
                for edge in actor_edges_out:
                    tgt = node_dict.get(edge.target_id)
                    if tgt:
                        report.append(f"  - [{edge.predicate.value}] → **{tgt.label}** ({tgt.entity_class.value})")
                        report.append(f"    * 근거: {edge.reasoning}")
            
            if actor_edges_in:
                report.append("- **관계 엣지 (Inflow)**:")
                for edge in actor_edges_in:
                    src = node_dict.get(edge.source_id)
                    if src:
                        report.append(f"  - **{src.label}** ({src.entity_class.value}) → [{edge.predicate.value}]")
                        report.append(f"    * 근거: {edge.reasoning}")
            report.append("")
    else:
        report.append("감지된 주요 학자(Actor) 노드가 존재하지 않는다.")
        report.append("")

    # 4. 한계 및 해석학적 아포리아(Limitation) 분석
    if limitations:
        report.append("## 4. 선행 학설의 한계 및 연구의 공백 (Limitations & Gaps)")
        for lim in limitations:
            report.append(f"### ⚠️ 한계요소: {lim.label}")
            if lim.source_quote:
                report.append(f"- **텍스트 기원**: \"{lim.source_quote}\" (문단 ID: {lim.paragraph_id})")
            
            # 한계와 연관된 엣지 검색
            lim_edges = [e for e in ontology_map.edges if e.source_id == lim.id or e.target_id == lim.id]
            for edge in lim_edges:
                other_id = edge.target_id if edge.source_id == lim.id else edge.source_id
                other_node = node_dict.get(other_id)
                if other_node:
                    role = "대상" if edge.source_id == lim.id else "원인"
                    report.append(f"  - **관계**: {role} **{other_node.label}** ({other_node.entity_class.value}) [관계형태: {edge.predicate.value}]")
                    report.append(f"    * 해석학적 판단: {edge.reasoning}")
            report.append("")

    # 5. Mermaid 다이어그램 추가
    report.append("## 5. 담론 시각화 다이어그램 (Mermaid Graph)")
    report.append("```mermaid")
    report.append(build_mermaid_graph(ontology_map))
    report.append("```")
    report.append("")
    
    # 6. RDF Triples 테이블
    report.append("## 6. RDF Triples 추출 메타데이터")
    report.append("| 주어 (Subject / Source) | 관계 술어 (Predicate) | 목적어 (Object / Target) | 판단 근거 (Reasoning) | 문단 ID |")
    report.append("| :--- | :--- | :--- | :--- | :--- |")
    for edge in ontology_map.edges:
        src = node_dict.get(edge.source_id)
        tgt = node_dict.get(edge.target_id)
        src_label = f"{src.label} ({src.entity_class.value})" if src else edge.source_id
        tgt_label = f"{tgt.label} ({tgt.entity_class.value})" if tgt else edge.target_id
        pid = src.paragraph_id if src else "-"
        report.append(f"| {src_label} | `{edge.predicate.value}` | {tgt_label} | {edge.reasoning} | {pid} |")
        
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="신학 마크다운 분석을 통한 RDF 온톨로지 담론 맵 생성 스크립트")
    parser.add_argument("-f", "--file", required=True, help="분석 대상 신학 마크다운 문서 경로")
    parser.add_argument("-o", "--output", help="출력할 분석 보고서 경로")
    parser.add_argument("--mock", action="store_true", help="LLM 호출 없이 Mock 데이터로 실행 테스트 수행")
    parser.add_argument("--api-key", help="Anthropic API Key")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"[❌ Error] 대상 파일이 존재하지 않습니다: {args.file}")
        sys.exit(1)
        
    print(f"📖 문서 분석을 준비 중입니다: {args.file}")
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 문단 주석 부여
    annotated_text, paragraph_map = assign_paragraph_ids(content)
    
    if not paragraph_map:
        print("[❌ Error] 문서에서 유효한 문단을 감지하지 못했습니다.")
        sys.exit(1)
        
    print(f"📌 총 {len(paragraph_map)}개의 문단을 분리하여 주석을 부여했습니다.")
    
    # LLM Provider 주입 및 익스트랙터 기동
    try:
        provider = get_llm_provider(args.mock, args.api_key)
        from src.ontology.extractor import OntologyExtractor
        extractor = OntologyExtractor(llm_provider=provider)
        
        ontology_map = extractor.extract(annotated_text)
    except Exception as e:
        print(f"[❌ Error] 온톨로지 맵 추출 중 예외가 발생했습니다: {e}")
        sys.exit(1)
        
    print(f"✨ 온톨로지 맵 분석 성공. {len(ontology_map.nodes)}개의 노드와 {len(ontology_map.edges)}개의 엣지를 획득했습니다.")
    
    # 보고서 텍스트 빌드
    report_md = build_discourse_report(ontology_map, content)
    
    # 출력 경로 결정
    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(args.file)
        output_path = f"{base}_discourse.md"
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_md)
        
    print(f"💾 담론 구조 분석 보고서가 생성되었습니다: {output_path}")

if __name__ == "__main__":
    main()
