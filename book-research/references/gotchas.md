# book-research 함정과 실패 사례

## Claim 상태 혼동

`generated`는 모델이 만든 후보일 뿐 원문 대조를 뜻하지 않음. `source-checked` evidence에는 locator가 실제 source segment를 다시 찾는지 확인한 기록이 있어야 함. `human-reviewed`는 source-checked evidence 없이 직접 부여하지 않음.

## 잘못된 저자 귀속

두 저자가 같은 `concept/*` 태그를 사용해도 같은 명제를 주장하거나 서로 영향을 주었다는 뜻이 아님. 결과 표에는 claim ID와 attribution을 유지하고, 비교자가 만든 연결은 `basis=inferred`로 표시함.

## locator 과신

PDF 내부 페이지 인덱스와 인쇄 페이지 표기는 다를 수 있음. EPUB spine item은 화면 페이지가 아님. locator reliability가 낮거나 원문 파일이 없으면 이를 숨기지 말고 재확인 불가로 보고함.

## 단일 책 결과의 과잉 종합

한 권만 관련 claim을 제공하면 저자 간 비교는 성립하지 않음. 낮은 관련성의 도서를 억지로 추가하지 말고, 한 도서 근거라는 제한을 밝힘.
