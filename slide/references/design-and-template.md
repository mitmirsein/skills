# Design System, Starter Template & Assets (정본)

## Design System & Theme Integration

Declare typed design tokens at the top of `index.tsx` so the dev panel can tweak them:

```tsx
import type { DesignSystem, Page } from '@open-slide/core';

export const design: DesignSystem = {
  palette: { bg: '#0f172a', text: '#f8fafc', accent: '#fbbf24' },
  fonts: {
    display: 'system-ui, -apple-system, sans-serif',
    body: 'system-ui, -apple-system, sans-serif',
  },
  typeScale: { hero: 180, body: 40 },
};
```

### CSS Variables Binding
*   Use `var(--osd-X)` for visual properties so the Design panel can preview adjustments in real-time.
*   Available vars: `--osd-bg`, `--osd-text`, `--osd-accent`, `--osd-font-display`, `--osd-font-body`, `--osd-size-hero`, `--osd-size-body`, `--osd-radius`.
*   Example:
    ```tsx
    <div style={{ background: 'var(--osd-bg)', color: 'var(--osd-text)' }}>
    ```

## React Starter Template

```tsx
import type { DesignSystem, Page, SlideMeta } from '@open-slide/core';

export const design: DesignSystem = {
  palette: { bg: '#0f172a', text: '#f8fafc', accent: '#fbbf24' },
  fonts: {
    display: 'system-ui, -apple-system, sans-serif',
    body: 'system-ui, -apple-system, sans-serif',
  },
  typeScale: { hero: 180, body: 40 },
};

const muted = '#94a3b8';

const fill = {
  width: '100%',
  height: '100%',
  fontFamily: 'var(--osd-font-body)',
} as const;

const Cover: Page = () => (
  <div
    style={{
      ...fill,
      background: 'var(--osd-bg)',
      color: 'var(--osd-text)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      padding: '0 160px',
    }}
  >
    <div style={{ fontSize: 28, color: 'var(--osd-accent)', letterSpacing: '0.2em' }}>
      CHAPTER 01
    </div>
    <h1
      style={{
        fontFamily: 'var(--osd-font-display)',
        fontSize: 'var(--osd-size-hero)',
        fontWeight: 900,
        margin: '32px 0',
        lineHeight: 1.05,
      }}
    >
      The Big Idea
    </h1>
    <p style={{ fontSize: 'var(--osd-size-body)', color: muted, maxWidth: 1200 }}>
      A short subtitle that explains what this slide is about.
    </p>
  </div>
);

const Content: Page = () => (
  <div style={{ ...fill, background: 'var(--osd-bg)', color: 'var(--osd-text)', padding: 120 }}>
    <h2 style={{ fontFamily: 'var(--osd-font-display)', fontSize: 80, fontWeight: 800, margin: 0 }}>
      Section heading
    </h2>
    <ul style={{ fontSize: 'var(--osd-size-body)', lineHeight: 1.6, marginTop: 64, paddingLeft: 48 }}>
      <li>One clear point per line</li>
      <li>Keep to 3–5 bullets</li>
      <li>Let the space breathe</li>
    </ul>
  </div>
);

export const meta: SlideMeta = { title: 'The Big Idea' };
export default [Cover, Content] satisfies Page[];
```

## Assets & Image Placeholders

*   Place local assets under `slides/<id>/assets/` and import them as ES modules:
    ```tsx
    import hero from './assets/hero.jpg';
    <img src={hero} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
    ```
*   When a specific image is required but not yet supplied (e.g. product screenshots, specific charts), use `ImagePlaceholder`:
    ```tsx
    import { ImagePlaceholder } from '@open-slide/core';
    <ImagePlaceholder hint="Q3 revenue chart" width={1280} height={720} />
    ```
*   Do **not** use placeholders for generic stock filler.

---

## Standalone HTML Presentation Standard (라이브 필기, 뷰어 & Impeccable 품질 표준)

HTML 기반 단독 슬라이드 생성 시 다음 표준 기능 및 Impeccable 품질 세트를 기본 탑재한다:

1. **캔버스 해상도 & 전체화면 표준**:
   * `body` 및 `.deck-container`를 기본 `width: 100vw; height: 100vh;`로 설정하여 좌우/상하 검은 여백(Pillarbox) 없는 100% 풀스크린 캔버스로 구성.
   * `⛶ 전체화면` 버튼 및 단축키 `F` (또는 `Cmd+Ctrl+F`)를 기본 내장하여 발표 시 탭/주소창 없는 완전 몰입형 전체화면 지원.
   * 프레젠테이션 컨트롤바(도크)는 중앙 대신 **우측 하단 (`bottom: 14px; right: 18px;`)**에 배치하여 콘텐츠 침범 방지.

2. **Impeccable UI 품질 & AI 클리셰(AI Slop) 방지 원칙 (필수)**:
   * **계층 구조 단순화 (No Nested Cards)**: 슬라이드 내부에 하얀 박스+테두리+그림자를 가진 카드 박스를 중첩하지 않는다. 상단 디바이더(`border-top: 2px solid var(--border-col)`)를 가진 오픈 에디토리얼 컬럼 또는 미니멀 배경 패널 사용.
   * **명도 대비 (WCAG AA ≥ 4.5:1 준수)**: 밝은 배경(`#FAF8F3`) 위 모든 텍스트/액센트 컬러는 4.5:1 이상(테라코타 `#94380E`, 포레스트그린 `#1B4E38`, 골드 `#785400`, 뮤트 `#666054`)을 반드시 준수.
   * **No Hero Eyebrow Pill Chips**: 제목(`h1`/`h2`) 위에 둥근 알약형 칩 배지(`badge-pill`)를 띄우지 않는다. 정갈한 텍스트 헤더/서브타이틀(`font-weight: 700; color: var(--text-muted)`) 사용.
   * **No Side-tab Accent Borders**: 비대칭적인 `border-left: 4px~6px` 강조선을 지양하고, 단정한 사방 테두리/배경 또는 상단 디바이더 라인 활용.
   * **No All-caps Body Text**: 긴 본문이나 배지에 `text-transform: uppercase`를 강제하지 않고 단정한 Title Case 사용.
   * **이탤릭체 금지 (No Italics - Use Bold Only)**: 한글 폰트 렌더링 깨짐 및 가독성 저하를 방지하기 위해 이탤릭체(`*text*`, `_text_`, `<i>`, `<em>`, `font-style: italic`)를 일절 사용하지 않는다. 강조가 필요할 때는 볼드(`**text**`, `<b>`, `font-weight: 700~800`)만을 사용한다.
   * **굽은 따옴표 사용 (Curly / Smart Quotes)**: 본문, 인용문, 배지, 대사 등에 곧은 따옴표(`"`, `'`) 대신 타이포그래피 품격을 위해 반드시 굽은 따옴표(`“`, `”`, ‘, ’)를 사용한다.
   * **둥근 요소 위의 단면 보더 강조 금지 (No Border Accent on Rounded Element)**: `border-radius`가 적용된 컨테이너에 `border-top`이나 `border-left` 등 특정 단면에만 굵은 보더를 주면 모서리 곡선과 충돌하는 전형적인 AI 스타일이 발생하므로 금지한다. 전체 균일 테두리(`border: 1px solid ...; border-radius: ...`)에 내부 인디케이터 라인(가로바/배지)을 조합한다.
   * **절제된 자간**: 본문 및 태그 자간은 `0.02em ~ 0.04em` 이내로 단정하게 유지.

3. **좌우 대칭 및 하단 라인 동기화 (Visual Symmetry & Equal Heights)**:
   * 2단 그리드(`grid-2`): `align-items: stretch;`를 기본으로 주어 좌우 컬럼 높이가 100% 일치하도록 구성.
   * 컬럼 내부: `display: flex; flex-direction: column; justify-content: space-between; height: 100%;`를 적용하여 상단 제목, 중간 본문, 하단 콜아웃 박스(예: 핵심 약속/특별 과제)의 하단 밑선이 좌우 1px 오차 없이 정확히 평행을 이루도록 설계.

4. **텍스트 선택 허용 & 라이브 필기 시스템**:
   * 기본 `user-select: text;`로 설정하여 발표 중에도 텍스트 드래그 및 복사 보장.
   * `H` (형광펜, 연노랑 `rgba(255, 230, 80, 0.45)`), `P` (볼펜 `#D9381E`), `L` (레이저 포인터), `C` (지우기), `ESC` (일반 포인터).

5. **발표자 전용 모드 분리 창 (Presenter View & Dual Screen Sync)**:
   * 단축키 `W` 또는 툴바 버튼으로 별도 팝업 창(`*_presenter.html`) 실행.
   * `BroadcastChannel` + `localStorage` 이중 채널을 통한 0ms 양방향 실시간 동기화.
   * 대본(Speaker Notes) 폰트 조절, 경과 시간 스톱워치, 실시간 시계, 다음 슬라이드 미리보기, 1~N 퀵 점프 버튼 내장.

6. **온스크린 QR 코드 모달 & 모바일 리모컨 초고속 무선 연동**:
   * **QR 코드 팝업 (`Q` 키 / 툴바 `📱 리모컨 QR` 버튼)**: 프로젝터 화면에 스마트폰 카메라로 스캔 가능한 연결용 QR 코드 모달 표시.
   * **초고속 무선 연동 (`serve_deck.py`)**: 100ms Fast Polling + POST 구조로 맥북과 모바일 기기 간 지연 없는 실시간 양방향 전환.
   * **모바일 최적화 터치 UX**: 모바일 화면 1열 대본 뷰, 좌우 터치 스와이프 슬라이드 넘김, 햅틱 진동 피드백(`navigator.vibrate`), 실시간 네트워크 상태 뱃지(`🟢 맥북 무선 연동됨`).

7. **프리젠터 파일 대본(Speaker Notes) 고도화 생성 표준**:
   * **형식 (완결된 액션 큐 & 블릿 기호)**:
     - 미완성 어절(`~속에서.`, `~현실.`, `~소개.` ❌) 절대 금지.
     - 발표자가 즉시 스피치할 수 있는 **완결된 행동 지침(Actionable Cues)**​ 작성:
       1) **청중 공감/오프닝 큐**: 공감 질문, 현장 문제의식, 톤 조절
       2) **핵심 메시지 (Key Message)**: 슬라이드가 전하고자 하는 본질적 주장과 세부 논거
       3) **다음 슬라이드 브릿지 (Transition)**: 자연스러운 전환 멘트
   * **서체 (고딕체 / Sans-serif)**: `Pretendard`, `Noto Sans KR`, system-ui 등 명쾌하고 가독성 높은 고딕 서체 적용.
   * **문단형식 (내어쓰기 / Hanging Indent)**: `text-indent: -1.35em; padding-left: 1.35em;` 적용으로 줄바꿈 시 블릿 기호 뒷부분으로 깔끔하게 수직 정렬.
   * **영상 내레이션 (`narration`)**: Audio Studio TTS 및 MP4 영상 자막용으로 30~80단어의 자연스러운 구어체 완성형 문장으로 별도 작성.
