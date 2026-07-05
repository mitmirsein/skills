---
name: grafeo-connector
description: >
  Connects the msn_th_db corpus and TOSK ontology for fused search — BM25
  text axis with chunk-level provenance plus a graph axis (entity match,
  shortest-path relation inference). Runs on a built-in lightweight
  file-based backend (swappable for GrafeoDB later). Use when the user asks
  for grafeo sync, hybrid search, or theological relation analysis.
  키워드: 그라페오, 융합 검색, 관계 추론, 지식 그래프 검색
version: 1.1.0
codename: Third Gen
author: MS_Dev
triggers:
  - "grafeo sync"
  - "grafeo search [query]"
  - "신학적 관계 분석해줘"
  - "#grafeo"
capabilities:
  - knowledge_graph_synchronization
  - hybrid_vector_text_search
  - cross_domain_inference_bridge
  - topological_relation_mapping
  - mmr_diversified_retrieval
status: active
---

# 🕸️ Grafeo Connector 1.0

## 1. 개요 (Overview)
`msn_th_db`의 방대한 텍스트 서고와 `TOSK`의 정교한 온톨로지 구조를 GrafeoDB의 고성능 그래프-벡터 엔진 위에서 통합합니다. 단순 검색을 넘어 신학적 개념들의 '위상적 관계'를 추론하고 대규모 데이터에서의 시맨틱 검색 속도를 혁신합니다.

## 2. 핵심 워크플로우 (Dynamic Workflow)

### Phase 1: Ingest & Sync (데이터 동기화)
- `msn_th_db`의 JSONL 청크 데이터와 `TOSK`의 `entities.jsonl`, `relations.jsonl`을 읽어 Grafeo의 LPG(Labeled Property Graph)로 변환합니다.
- 텍스트 청크는 `Vector` 타입으로 변환되어 HNSW 인덱스에 저장됩니다.

### Phase 2: Hybrid Search (융합 검색)
- 사용자의 질문을 3개국어로 확장한 후, Grafeo의 BM25(텍스트)와 Cosine Similarity(벡터) 엔진을 동시에 가동합니다.
- RRF(Reciprocal Rank Fusion) 알고리즘을 통해 최적화된 결과 순위를 도출합니다.

### Phase 3: Relation Inference (추론)
- 검색된 노드들 사이의 최단 경로(Shortest Path)나 연결성(Centrality)을 분석하여, 표면적으로 드러나지 않은 신학적 동맹이나 대립 관계를 시각화 보고합니다.

## 3. 주요 명령어 및 도구 (Tools)

> **백엔드 주석 (2026-06-12 구현)**: 현재 구현은 GrafeoDB 엔진이 아니라 **경량 내장
> 백엔드**(stdlib 전용, 파일 기반 LPG + 단일 패스 BM25)다. 벡터 코사인·HNSW·RRF는
> GrafeoDB 도입 시 `scripts/grafeo_lite.py`만 교체해 활성화한다. 인터페이스 계약과
> 품질 게이트(G1/G3)는 동일하게 충족된다.

- `python3 scripts/sync.py`: TOSK 그래프 + 코퍼스 매니페스트 동기화 (G1 카운트 보고)
- `python3 scripts/search.py --query "..." [--limit 5] [--json]`: 융합 검색
  (텍스트 축 BM25 + 그래프 축 엔티티, 청크 좌표 provenance 유지)
- `python3 scripts/analyze_rel.py --nodes "A,B"`: 최단 경로·연결도 분석
  (경로 없음 = 잠재 연구 간극으로 보고)
- 데이터 원천 재지정: 환경변수 `MSN_TH_DB_CHUNKS`, `TOSK_DATA`

## 4. 품질 게이트 (Quality Gates)
- **G1 (Sync Integrity)**: 동기화 후 소스 데이터와 노드/에지 카운트 일치 확인 — sync.py가 자동 보고.
- **G2 (Recall & Precision)**: 검색 상위 결과의 질의어 실제 포함 여부를 표본 검증.
  (코사인 임계치 검증은 GrafeoDB 벡터 축 도입 시 복원)
- **G3 (Provenance)**: 모든 검색 결과에 `msn_th_db`의 원본 좌표(printed_page, global_chunk_id) 유지.

---
*Created by MS_Dev, Third Gen Standard*
