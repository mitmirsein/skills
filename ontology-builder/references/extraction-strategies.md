# Ontology Builder: Extraction Strategies & Modes

텍스트의 성격과 규모에 따른 지식 추출 전략 및 운용 가이드입니다.

## 🔬 Strategy Modes
1. **Micro-Mode (단일 챕터 정밀 타격)**: 특정 파일의 메타포, 감정선, 구체적 맥락을 최우선으로 분석하여 즉시 DB에 주입합니다.
2. **Macro-Hybrid Mode (전체 통독 및 통합)**: 전역 온톨로지 구축 시 사용합니다. 각 챕터를 반복 분석(Iterative)하여 충돌과 중복을 조정한 뒤 `add-bulk`로 일괄 주입합니다.

## 🕳️ Negative Ontology (부정 온톨로지)
- **Protocol**: "분해되지 않는 것들의 지도를 그린다."
- **Detection**: "말로 표현이 안 돼", "분해하면 상실됨", "역설/신비/침묵" 등의 표현 감지 시 발동합니다.
- **Workflow**: 
    1. 사용자의 저항 표현 감지.
    2. "분해 불가능 영역"임을 확인 후 인터뷰(시도한 분해, 상실 가치 등)를 거쳐 `add_aporia` 명령으로 기록합니다.

## 🚦 HITL (Human-in-the-Loop)
- 추출된 입력을 바로 저장하지 말고, 반드시 사용자에게 리스트를 보여주고 최종 승인(Commit)을 받으십시오.
