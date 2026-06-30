# 토큰 시스템: OKLCH 베이스

색을 hex로 흩뿌리지 않고, **OKLCH(L 명도 · C 채도 · H 색상)** 로 토큰화한다. OKLCH는 명도가 지각적으로 균일해 사다리·대비·다크모드·색조 변주를 *수학적으로* 파생할 수 있다. colorize 동사가 이 파일을 사용한다.

## 왜 OKLCH인가
- 같은 L이면 색상(H)이 달라도 *체감 밝기*가 일정 → 위계·대비 설계가 예측 가능.
- H만 회전하면 명도·채도 구조를 보존한 채 팔레트 색조만 변주(전례력 변주의 근거).
- `oklch(L% C H)` — 예: `oklch(62% 0.17 256)`. 브라우저 네이티브 지원.

## 토큰 계층 (3층)
1. **원시(primitive) 사다리**: 시드 색의 H·C를 고정하고 L만 95→10으로 단계화.
   ```css
   :root{
     --brand-h: 256; --brand-c: 0.16;
     --brand-50:  oklch(97% 0.02 var(--brand-h));
     --brand-100: oklch(93% 0.04 var(--brand-h));
     --brand-300: oklch(78% 0.10 var(--brand-h));
     --brand-500: oklch(62% var(--brand-c) var(--brand-h)); /* 시드 */
     --brand-700: oklch(48% 0.14 var(--brand-h));
     --brand-900: oklch(28% 0.08 var(--brand-h));
   }
   ```
2. **시맨틱(semantic)**: 컴포넌트는 *오직 이것만* 참조.
   ```css
   :root{
     --bg: oklch(99% 0.004 var(--brand-h));
     --surface: #fff; --text: oklch(25% 0.02 var(--brand-h));
     --text-muted: oklch(55% 0.02 var(--brand-h));
     --border: oklch(90% 0.01 var(--brand-h));
     --primary: var(--brand-500); --accent: oklch(70% 0.15 30);
   }
   ```
3. **다크모드**: H·C 유지, L 반전·재배치(채도 소폭 ↓).
   ```css
   @media (prefers-color-scheme: dark){:root{
     --bg: oklch(18% 0.02 var(--brand-h));
     --text: oklch(92% 0.01 var(--brand-h));
     --border: oklch(32% 0.02 var(--brand-h));
     --primary: oklch(70% 0.13 var(--brand-h));
   }}
   ```

## 회색에 브랜드 H 주입
- 순회색(C=0) 대신 `--brand-h`에 C=0.01~0.02를 주면 화면 전체가 미세하게 한 색조로 묶여 고급스러워진다.

## 창발: 전례력(Liturgical) 색조 변주
같은 명도 사다리 위에서 `--brand-h`(와 accent H)만 회전해 절기 테마를 파생한다. 시드 예시:
| 절기 | 주조 H 방향 | 무드 |
|---|---|---|
| 대림(Advent) | 보라 ~290 | 기다림·절제 |
| 성탄(Christmas) | 따뜻한 적금 ~40 | 기쁨·온기 |
| 사순(Lent) | 자보라 ~330, C↓ | 회개·금욕 |
| 부활(Easter) | 백금/연노랑 ~95, L↑ | 영광·밝음 |
| 연중(Ordinary) | 녹 ~150 | 성장·평상 |

- 명도 구조가 동일하므로 대비·접근성은 한 번만 설계하면 모든 절기에 유지된다.

## 검증
- 텍스트/배경 L 차이가 대비 4.5:1을 만족하는지 확인(L 차 ≈ 40%p 이상이 안전선, 정확히는 대비식으로).
- 흑백 인쇄 변환 시 사다리 단계가 구분되는지(print-grade).

## 함정
- L을 등간격으로 두지 말 것 — 밝은 쪽은 촘촘히, 어두운 쪽은 성기게(지각 곡선).
- 시드 hex를 그대로 쓰고 사다리를 안 만들면 토큰화 의미 없음.
