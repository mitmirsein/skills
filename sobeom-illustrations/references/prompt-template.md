# 이미지 생성 프롬프트 템플릿 (Prompt Template)

나노 바나나 프로(Nano Banana Pro / Gemini 3 Pro Image)에 전달할 개별 이미지 생성 프롬프트입니다. 아래 변수(`{}`)들을 실제 아티클 내용에 맞춰 치환하여 호출합니다.

```text
Generate one standalone 16:9 horizontal Korean article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse orange/blue/red handwritten Korean annotations. Clean, absurd, and witty sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring IP character required:
소범 (Sobeom), a minimalist Korean tiger with a round white face, tiny pointed tiger ears on top, a few simple wobbly hand-drawn black stripes on its cheeks and forehead, simple dot eyes with a deadpan expression, and very thin stick-like arms and legs. Sobeom is always wearing a traditional black Korean hat (Gat) slightly tilted on its head. Sobeom must perform the core conceptual action, not decorate the scene. Sobeom should look serious, deadpan, and slightly bizarre, not cute.

Theme:
{아티클 삽화 주제}

Structure type:
{구조 타입: Workflow / 시스템 분석 / 전후 대비 / 상태 변화 / 개념 은유 / 분기점 / 로드맵 / 카툰 분할}

Core idea:
{이 삽화가 전달하고자 하는 본질적인 개념}

Composition:
{화면 연출: 소범이가 무엇을 하고 있는지, 어떤 도구를 쥐고 있는지, 주황/빨강/파랑 포인트 컬러가 어디에 칠해지는지 구체적 기술}

Suggested elements:
{핵심 소품1} / {핵심 소품2} / {핵심 소품3}

Korean handwritten labels:
{한국어 주석단어1} / {한국어 주석단어2} / {한국어 주석단어3} (단어당 2~5글자 내외의 짧은 표현 권장)

Color use:
Black for main line art and Sobeom. Orange only for paths, flows, and directional arrows. Red only for errors, warnings, or blocking barriers. Blue only for secondary comments, thoughts, or internal system states. Keep color use extremely sparse and restrained.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 3-5 short handwritten Korean labels. Do not write a title in the top-left corner. Do not make it a formal diagram or slide. Do not copy prior templates; invent a fresh visual metaphor for this specific context.
```

---

## 이미지 수정/편집용 템플릿 (Editing & Iterating)

### 특정 타이틀이나 글자 영역 지우기
이미지 편집 시 특정 영역의 텍스트 오타나 타이틀을 지울 때 아래 프롬프트를 보강하여 덮어씌웁니다.

```text
Edit the provided image. Remove only the handwritten text "{지우고 싶은 한글}" and its underline from the image. Fill that area with the same clean, pure white background matching the surrounding blank paper. Preserve everything else exactly: Sobeom's appearance, Gat, brush lines, aspect ratio, and composition. Do not add any new elements.
```

### 소범이 묘사 수정 및 기묘함 강화
소범이가 단순히 서만 있거나 캐릭터가 흐릿하게 나왔을 때 캐릭터 액션을 중앙에 고정하도록 강제합니다.

```text
Regenerate this illustration. Make the character Sobeom (wearing Gat) the direct actor in the conceptual action. Sobeom should be physically holding, pulling, or interacting with the objects in the scene, rather than standing aside. Keep the line art clean, minimal, wobbly, and preserve 40% blank space.
```
