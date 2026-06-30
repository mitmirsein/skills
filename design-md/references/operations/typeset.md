# 동사: typeset — 한·영 타이포 시스템

한글이 등장하면 이 규칙은 **무조건** 적용된다(SKILL.md Phase 0).

## 폰트 전략
- **Sans (UI/모던)**: 투박한 Noto Sans KR 대신 **Pretendard**를 기본. 영문은 Inter/SF Pro와 baseline이 맞는다.
- **Serif (에디토리얼/학술/Kerygma)**: **Noto Serif KR** 또는 **KoPubBatang**으로 인쇄급 격조.
- 제목 Serif + 본문 Sans, 또는 그 반대로 **이분화**해 위계를 만든다. 한 폰트 도배 금지.
- 폰트는 토큰화: `--font-sans`, `--font-serif`, `--font-mono`.

## 마이크로 타이포 (한글)
- `word-break: keep-all;` **필수** — 단어 중간 줄바꿈 방지.
- 자간 `letter-spacing: -0.01em ~ -0.02em`로 미세하게 조여 시각 밀도 ↑ (영문 본문은 0).
- 줄간 `line-height`: 한글 본문 1.7~1.8, 영문 1.5~1.6, 제목 1.1~1.25.
- 숫자·약물은 `font-feature-settings`로 tabular/lining 정렬(표·가격).

## 위계 스케일
- 모듈러 스케일(1.2~1.333배수)로 `--text-xs … --text-4xl` 정의. 인접 레벨 간 대비를 충분히.
- Weight도 위계 도구: 본문 400, 강조 600, 제목 700. 회색조 농담으로 secondary 텍스트 처리.

## 측정폭·정렬
- 본문 컬럼 45–75자(한글은 35~45자 체감). 양쪽 정렬(justify)은 한글에서 어색하니 좌측 정렬 기본.
- 인쇄 출력은 [print-grade.md](./print-grade.md)의 금칙·하이픈 규칙으로 넘어간다.

## 함정
- 한글에 영문 전용 폰트만 지정 → 폴백이 굴림/맑은고딕으로 깨짐.
- `text-align: justify` + `keep-all` 조합 시 한글 줄 끝 들쭉날쭉 → 좌측 정렬 권장.
