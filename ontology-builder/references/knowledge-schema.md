# Ontology Builder: Knowledge Schema (Entity, Relation, Aporia)

지식 그래프를 구성하는 3대 요소의 데이터 구조 및 명세입니다.

## 🟢 Entity (Node)
| 필드 | 설명 | 예시 |
|:---|:---|:---|
| `id` | 고유 ID (PascalCase) | `Barth_Karl`, `Trinity_Doctrine` |
| `type` | 유형 | `Person`, `Concept`, `Work`, `Event`, `Other` |
| `names` | 별칭(Alias) 목록 | `["Karl Barth", "바르트"]` |
| `key_chunks` | 증거 청크 ID (필수) | `["KD_1_1:0012_01"]` |

## 🔵 Relation (Edge)
| 필드 | 설명 | 예시 |
|:---|:---|:---|
| `source` | 출발 Entity ID | `Barth_Karl` |
| `target` | 도착 Entity ID | `Natural_Theology` |
| `relation` | 술어 (Predicate) | `critiques`, `isA`, `partOf` |
| `evidence` | 증거 청크 ID (필수) | `KD_1_1:0123_01` |

## 🔴 Aporia (Negative Ontology)
분해에 저항하는 신학적 신비나 역설을 기록합니다.
- **Resistance Types**: `identity_paradox`, `self_dissolution`, `mutual_indwelling`, `temporal_transcendence`, `linguistic_limit`.
- **Fields**: `id`, `description`, `attempted_decomposition` (시도된 분해), `what_is_lost` (상실되는 가치).
