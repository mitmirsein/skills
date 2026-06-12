# Knowledge Traps & Gotchas (프롬프트 엔지니어링 함정)

## ❌ 안티 패턴 (Anti-patterns)
1. **명령 과부하 (Instruction Overload)**: 너무 많은 지시를 한 번에 내리면 모델의 어텐션이 분산됨. (핵심 6섹션 위주 구성 권장)
2. **구버전 문법 고수**: GPT-5 계열에 GPT-3.5 방식의 "Step-by-step"만 강조하는 것은 비효율적. (Reasoning Effort 활용)
3. **모호한 형용사**: "멋지게", "전문적으로" 대신 구체적인 평가 기준(Success Criteria) 제시.
4. **Haiku 4.5에 Opus급 추론 기대**: 경량 모델에는 추론(Thinking) 단계보다 명확한 패턴 매칭 지시가 유리함.

## ✅ 해결책 (Solutions)
- **Modular Prompting**: 복잡한 작업은 여러 개의 프롬프트로 쪼개어 단계별로 실행.
- **Prefill (Legacy Models)**: Claude 4.6 이하 모델에서는 답변의 시작 부분을 미리 채워주는(pre-fill) 기법이 여전히 유효함.
