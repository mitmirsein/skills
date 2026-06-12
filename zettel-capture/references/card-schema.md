# 🗃️ Zettel Card Schema (3단계 노트 유형별 규격)

제텔카스텐의 3가지 노트 유형에 따른 카드 템플릿 규격입니다.

---

## 1. 노트 유형 분류 기준

| 유형 | 아이콘 | 판별 기준 | 대표 시나리오 |
|:---|:---|:---|:---|
| **Fleeting** | 💭 | 출처 불명확, 가공 안 된 즉흥적 생각 | "일단 적어놔", 산책 중 떠오른 아이디어 |
| **Literature** | 📖 | 특정 출처 + 자기 말로의 해석이 결합 | "이 문장 메모해줘 + 내 생각은..." |
| **Permanent** | 💎 | 출처에서 독립된 원자적 명제, 재사용 가능 | 성숙 큐에서 승격된 완성된 지식 단위 |

### 판별 순서도
```
입력에 특정 출처가 있는가?
├─ Yes → 대장의 고유 사유가 포함되어 있는가?
│        ├─ Yes → 📖 Literature
│        └─ No  → 📖 Literature (사유 촉발 옵션 확인)
└─ No  → 독립적 명제인가?
         ├─ Yes → 💎 Permanent (드문 경우, 대장에게 확인)
         └─ No  → 💭 Fleeting
```

---

## 2. 공통 메타데이터 (YAML Frontmatter)

모든 카드 유형에 공통으로 적용되는 YAML 규격입니다.

```yaml
---
zettel_id: "YYYYMMDD-NNN"    # 날짜 + 일련번호 (예: 20260325-001)
type: literature              # literature | fleeting | permanent
maturity: "seed"              # seed | growth | mature
source:
  title: ""                   # 출처 제목 (필수)
  author: ""                  # 저자
  locator: ""                 # 페이지, 타임스탬프, 챕터, §번호 등
  url: ""                     # URL (웹/영상 출처일 경우)
tags: []                      # 핵심 키워드 태그
# aporia_hint: 이 생각에 내포된 '반대 주장'이나 긴장을 한 줄로.
# 예) "은혜가 전부라면, 왜 바울은 순종을 명하는가?"
# 이 필드가 성숙 후 사전 표제어의 tensions.pole_b 씨앗이 됩니다.
aporia_hint: ""
related: []                   # [[wikilink]] 형태의 관련 카드
created: YYYY-MM-DD           # 생성일
---
```

### 필드별 규칙
- `zettel_id`: `YYYYMMDD` 부분은 생성일, `NNN`은 당일 일련번호(001부터). 기존 카드와 중복 방지 필수.
- `type`: 대장의 승인 후 확정. 에이전트가 임의 변경 금지.
- `maturity`: 신규 생성 시 항상 seed. 승격은 `/zettel review`를 통해서만.
- `source.locator`: 유연한 필드. 도서는 "p.346", 영상은 "12:34", 논문은 "§3.2" 등.

---

## 3. 유형별 본문 규격

### 💭 Fleeting Note
가장 가볍고 빠른 형태. 형식에 자유도가 높음.

```markdown
## 💭 Memo
[대장의 즉흥적 생각을 그대로 기록]
```

- Quote 섹션 **생략 가능**
- Source 메타데이터 **선택적** (없으면 비워둠)
- 목표: 30초 이내에 포착 완료

### 📖 Literature Note
대장의 핵심 유즈케이스. 출처의 원문 + 나의 사유 결합.

```markdown
## 💬 Quote (원문)
> "[출처에서 발췌한 원문을 정확히 보존]"

## 🧠 Zettel (나의 사유)
[대장이 기입하는 고유한 해석, 반응, 연결]

## 🔗 Connections
- [[관련 카드 또는 노트]]
```

- Quote는 **반드시 원문 그대로** (번역이 필요하면 별도 표기)
- Zettel 섹션은 **대장만** 작성 가능 (에이전트 대필 금지)
- Connections는 에이전트가 **제안**하되, 대장이 **확정**

### 💎 Permanent Note
출처에서 독립된, 재사용 가능한 원자적 지식 단위.

```markdown
## 💎 Thesis (명제)
[하나의 독립적이고 원자적인 지식 명제]

## 📐 Argument (논증)
[명제를 뒷받침하는 논증 또는 근거]

## 🔗 Connections
- [[관련 permanent note]]
- [[원본 literature note]]
```

- 새로 포착할 때 바로 Permanent로 생성하는 것은 **극히 드묾** (대장에게 확인 필수)
- 대부분 `/zettel review`를 통해 Literature → Permanent로 **승격**됨
- 반드시 **최소 1개 이상의 Connection**이 존재해야 Permanent 자격

---

## 4. Zettel ID 관리 규칙

1. **일련번호 채번**: 동일 날짜의 기존 카드를 `config.json`의 `zettel_dir`에서 스캔하여 다음 번호 부여.
2. **중복 방지**: 같은 ID가 이미 존재하면 NNN을 +1 증가.
3. **파일명 규칙**: `{zettel_id}_{짧은_제목}.md` (예: `20260325-001_신적_자유.md`)

---
*Created by MS_Dev Third Gen Standard*
