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
