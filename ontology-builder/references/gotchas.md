# 🕸️ Ontology Builder: Gotchas & Anti-Patterns

신학적 지식 추출 및 온톨로지 구축 시 에이전트가 주의해야 할 사항입니다.

## 1. Extraction Pitfalls (추출의 함정)
- **과도한 개체(Entity) 생성**: 일반 명사(예: '책', '사람')를 모두 개체로 등록하지 마십시오. 고유 명사, 신학적 개념, 역사적 사건 등 '지식적 가치'가 있는 대상만 추출하십시오.
- **관계(Relation)의 모호함**: 'A와 B는 관련 있음'과 같은 모호한 관계는 지식 그래프의 품질을 떨어뜨립니다. 'A는 B를 비판함', 'A는 B의 제자임'과 같이 구체적 술어(Predicate)를 사용하십시오.

## 2. Theological Failures (신학적 실패)
- **부정 온톨로지(Aporia) 무시**: 인간의 지성으로 파악되지 않는 '신비'나 '모순'을 억지로 논리적 관계로 치환하지 마십시오. 반드시 `Aporia` 타입으로 격리하여 저장하십시오.
- **Confessional Nuance**: 특정 개체가 교파에 따라 다른 의미로 사용될 때(예: '성찬'), 그 맥락(Context)을 소스 정보에 명시하십시오.

## 3. Commit Errors (주입 오류)
- **Source Isolation 위반**: 여러 소스에서 온 지식을 분리하지 않고 한곳에 섞어서 `commit`하지 마십시오. 지식의 출처(Provenance)가 불분명해집니다.
- **Schema 불일치**: `tosk_bot.py`가 요구하는 JSONL 스키마를 준수하지 않으면 DB 주입 시 에러가 발생합니다.

---
*Created by MS_Dev Third Gen Standard*
