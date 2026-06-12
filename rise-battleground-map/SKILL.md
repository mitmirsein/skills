---
name: rise-battleground-map
description: >
  Maps the contested terrain of a theological topic across 7 axes of
  tension (objective/subjective/transcendent domains), scoring each
  position 0–10 with scholarly evidence and rendering an interactive HTML
  radar chart (Chart.js), Mermaid radar, or ASCII fallback. Use when the
  user asks for a battleground map, position comparison, or tension
  topology of a doctrine. 키워드: 신학 지형도, 논쟁 지도, 입장 비교, 레이더 차트
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#battleground"
  - "지형도 그려줘"
  - "이 교리 논쟁 지도"
references_path: ./references
---

# 🗺️ RISE Battleground Map (신학 논쟁 지형도)

신학 주제를 둘러싼 학자·전통들의 입장을 7축 긴장 구조로 점수화하고 시각화합니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- **증거 없는 점수 금지**: 모든 점수는 대표 저작·어록 등 학문적 근거와 함께 산출합니다.
- **아포리아 보존(볼트 헌법)**: 긴장을 단일 결론으로 평탄화하지 않습니다 — 지도는
  긴장을 드러내는 도구이지 해소하는 도구가 아닙니다.

## Phase 1 — 축 설계 (정본: [axis-definition.md](./references/axis-definition.md))

- 7축 구성: 🔵 객관/이성(1–3축: 역사성·논리·증거) + 🔴 주관/실존(4–5축: 경험·결단) +
  🟢 초월/말씀(6–7축: 성경 권위·계시 독자성).
- RISE Reflection: 주제의 본질적 긴장이 잘 드러나도록 세션마다 축 명칭을 미세 조정 가능.

## Phase 2 — 점수화 (Scoring)

- 비교 대상(학자·전통·문헌)별로 각 축에 0–10점 부여, 각 점수에 근거 1줄 명기.
- 불확실한 점수는 범위(예: 6–8)로 표기하고 불확실성을 밝힙니다.

## Phase 3 — 시각화 (정본: [visualization-specs.md](./references/visualization-specs.md))

| 우선순위 | 형식 | 비고 |
|---|---|---|
| 🥇 | 단일 HTML 인터랙티브 차트 (Chart.js + Tailwind) | Dark Academia 테마 |
| 🥈 | Mermaid `radar` 다이어그램 | 마크다운 내 즉시 렌더 |
| 🥉 | ASCII 레이더 | 텍스트 전용 환경 |

- 모든 시각화 하단 푸터: `powered by 케리그마출판사 | [Visit Website](https://kerygma.co.kr)`

## 검증·보고

- 점수표(근거 포함)와 시각화 산출물 경로를 함께 보고합니다.
- HTML 산출물은 브라우저에서 열리는지 확인하고, 임시 파일은 정리합니다.
