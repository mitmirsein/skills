# 🛡️ Theological Research Verification Harness (v1.0)

> 검색 결과의 'Vibe'에 의존하지 않고, 물리적 소스로부터 추출된 데이터만을 사용하여 할루시네이션을 원천 차단하는 검증 프로토콜.

## Phase 0: Source Integrity Gate (소스 무결성 검문소)

연구 노트를 작성하기 전, 반드시 다음 정보를 **물리적으로 확인**하고 내부 메모리에 기록해야 한다.

1.  **Metadata Cross-Check**:
    - [ ] 제목(Title)이 원문과 토씨 하나 틀리지 않고 일치하는가?
    - [ ] 저자(Author)의 이름과 소속 기관이 정확한가?
    - [ ] 발행 연도(Year) 및 학술지/학위 유형이 일치하는가?
2.  **ID Validation**:
    - [ ] DOI, S2, RISS 등의 고유 식별자가 유효하며 클릭 시 해당 페이지로 연결되는가?

## Phase 1: Abstract Forensic (초록 포렌식)

단순 요약이 아닌, 원문 초록에서 **증거**를 추출한다.

1.  **Anchor Sentence**: 초록에서 논문의 핵심 논지를 담은 문장 하나를 **있는 그대로 인용**하여 'Anchoring' 한다.
2.  **Logic Trace**: 저자가 설정한 문제 제기(Aporia)와 결론(Thesis)이 초록의 문맥과 논리적으로 일치하는지 재검토한다.

## Phase 2: Audit Checklist (최종 감사)

- [ ] **Hallucination Check**: 검색 결과가 없는데 임의로 저자나 연도를 생성하지 않았는가?
- [ ] **Type Check**: 학위 논문(Thesis)을 학술지 논문(Journal Article)으로 혼동하여 인용하지 않았는가?
- [ ] **Link Check**: RISS의 경우 `p_mat_type`이 해당 논문 유형(학위/학술지)에 맞게 설정되었는가?

## Failure Recovery (실패 시 대응)

1.  검색 결과가 모호하거나 데이터가 부족할 경우, 절대 추측하지 않는다.
2.  사용자에게 "데이터 부족으로 인한 검증 불가"를 보고하고, 직접 링크나 추가 정보를 요청한다.
3.  `lightpanda-recon` 또는 `insane-search`를 통해 직접 페이지를 정찰하여 텍스트를 추출한다.
4.  유럽/독일어권 학술 DB인 `ixtheo-searcher` 및 프리미엄 신학 저널용 `crossref-journal-searcher`를 추가 가동하여 서지 데이터와 DOI 실존 여부를 검증한다.
