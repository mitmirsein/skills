# AF-01 · Baseline 출력 (스킬 미사용, #forge 트리거 없음)

> 프롬프트: "신학 논문의 참고문헌 목록(BibTeX 또는 주석 형태)을 입력받아 SBL 규격으로 자동 변환해주는 에이전트 스킬을 설계해줘."
> 실행일: 2026-05-18 · 실행자: Claude (agent-forge 비활성, 일반 응답)

---

신학 논문 참고문헌을 SBL 양식으로 변환하는 스킬을 만들어 보겠습니다.

## 접근 방식

1. **입력 파싱**: BibTeX(`@book`, `@article`, `@incollection`)나 주석형 텍스트를 받아 필드(저자, 제목, 출판사, 연도, 페이지)를 추출합니다.
2. **SBL 규칙 적용**: SBL Handbook of Style에 따라 각주 양식과 참고문헌 목록 양식으로 포맷팅합니다.
   - 각주: 이름 성 순, 콤마 구분, 괄호 안 출판정보
   - 참고문헌: 성, 이름 순, 마침표 구분
3. **출력**: 변환된 두 가지 양식을 마크다운으로 반환합니다.

## SKILL.md 초안

```
이름: sbl-converter
설명: 참고문헌을 SBL 형식으로 변환하는 스킬

사용법:
- 사용자가 BibTeX나 참고문헌 텍스트를 제공
- 스킬이 SBL 각주/참고문헌 양식으로 변환
- 결과를 반환
```

## 변환 예시

입력 (BibTeX):
```
@book{barth1956, author={Karl Barth}, title={Church Dogmatics}, year={1956}, publisher={T&T Clark}}
```

출력 (SBL 각주):
> Karl Barth, *Church Dogmatics* (Edinburgh: T&T Clark, 1956).

출력 (SBL 참고문헌):
> Barth, Karl. *Church Dogmatics*. Edinburgh: T&T Clark, 1956.

## 구현 팁

- 시리즈 약어(WUNT 등)는 별도 매핑 테이블을 두면 좋습니다.
- 재인용 시 단축형(ibid., 저자명+단축 제목)을 처리해야 합니다.
- 독일어/프랑스어 출판지는 원어를 유지하세요.

이 정도 구조로 스킬을 만들면 대부분의 신학 논문 참고문헌을 SBL로 변환할 수 있습니다. 추가로 원하시는 세부 양식(주석 스타일, 특정 시리즈)이 있으면 알려주세요.
