# TAWP Phase Gate & Execution Manual (v2.3-local)

이 문서는 자연어 연구 주제로부터 시작하여 저널급 신학 에세이/논문 원고, Claim Ledger, 로컬 PDF 검수 산출물까지 완성하기 위한 TAWP의 8개 Phase별 행동 강령과 개별 스킬 매핑을 규정합니다.

---

## 🏛️ TAWP 8대 Phase 및 개별 스킬 매핑

### Phase 1: 아이데이션 (Ideation)
* **목적**: 사용자가 제안한 자연어 연구 아이디어(예: *"칼 바르트의 칭의 이해에 대해 에세이 쓰고 싶어"*)를 학술적 문제제기와 핵심 질문으로 구조화합니다.
* **동원 스킬**: `research-mentor`
* **에이전트 행동**:
  1. 연구 대상이 되는 신학적 주제의 역사적/교리적 배경을 검토합니다.
  2. 연구의 목적을 담은 1~2개의 **핵심 가설(Hypothesis)**과 문제제기 목록을 작성합니다.
* **종료 조건**: 사용자가 아이데이션 결과 및 방향성에 동의하거나 수정을 지시합니다.

### Phase 2: 검색 및 리서치 (Research)
* **목적**: 제안된 가설을 지지하거나 논쟁할 선행 학술 연구 문헌들을 탐색하고 메타데이터를 수집합니다.
* **3개 언어 쿼리 규칙 (한·영·독)**: 
  - 신학 연구의 깊이를 온전히 확보하고 유럽 및 서구 신학의 핵심 문헌을 빠짐없이 수집하기 위해, 검색어는 반드시 **한국어(KO), 영어(EN), 독일어(DE)** 3개 언어로 자동 번역 및 확장하여 교차 생성해야 합니다.
  - **언어별 번역 및 확장 원칙**:
    - **한국어**: 국내 신학 트렌드 및 학위논문을 타겟팅하여 주요 학술 개념과 국문 번역 키워드를 조합합니다.
    - **영어**: 글로벌 학계의 연구 성과를 확보하기 위해 SBL 표준 및 주요 저널 키워드로 확장합니다.
    - **독일어**: 조직신학(Dogmatics)이나 성서학(Biblical Studies) 등 원전 및 독일어권 학술 담론의 중요성을 고려하여, 핵심 개념의 독일어 신학 전문 용어를 매핑합니다.
    - 예: "칭의와 종말론" ➔ (한) 칭의 종말론, (영) justification eschatology, (독) Rechtfertigung Eschatologie
* **동원 스킬**: 
  - **한국어 검색**: `kci-api-searcher` (임시 OpenAPI 검색), `riss-searcher`
  - **LOD 식별자 연계**: `nlk-interlinker` (국립중앙도서관/Wikidata 연계)
  - **영어 및 글로벌 검색**: `google-scholar-quick`, `crossref-journal-searcher`
  - **독일어 및 유럽권 검색**: `ixtheo-searcher` (Index Theologicus 연동), `google-scholar-quick`
  - **선택 심화 검색**: `google-scholar-semantic` (설치된 경우에만 Scholar 맥락·인용 네트워크 수집)
* **에이전트 행동**:
  1. **쿼리 생성 단계**: Phase 1에서 제안된 가설 및 핵심 질문을 기반으로 한국어, 영어, 독일어 3개 언어로 대응되는 검색 키워드 맵(Trilingual Query Map)을 작성합니다.
  2. **검색 수행 단계**: 생성된 3개 언어 쿼리별로 대응하는 DB(KCI, RISS, Scholar, IxTheo 등)를 정찰하여 원시 리소스(Raw Resources)를 최대한 폭넓게 확보합니다. 독일어 신학 문헌은 특히 IxTheo API(`ixtheo-searcher`)를 우선적으로 활용합니다.
  3. **에이전트 자체 정제 및 추천 단계 (🔴 신설 의무 단계)**: 수집된 원시 리소스(Raw Resources) 전체를 그대로 사용자에게 넘기지 않는다. 에이전트는 다음 기준으로 스스로 1차 필터링하여 **"정제된 추천 리소스 리스트(Recommended Evidence Pack)"**를 구성해야 한다.
     - **포함 기준**: (1) Phase 1의 가설 및 핵심 논증과 직접적 연관성이 있는 문헌, (2) 지지/논박/비교 대상으로서 온톨로지 명제에 명확히 귀속될 수 있는 문헌, (3) 저자 및 서지 정보가 확인된 학술 권위 문헌.
     - **제외 기준**: 논증 주제와 간접적으로 연관되거나 관련성이 미약한 문헌, 저자 미상 자료, 각주 인용 가능성이 없는 배경 참고 자료.
  4. **문헌 정리 단계**: 정제된 추천 리소스를 언어별(한·영·독)로 구분하여 저자, 연도, 제목, 학술지명 및 해당 문헌이 어느 논증 명제를 지지하는지를 명기합니다.
  5. **LOD 식별자 매핑 단계**: 확정된 신학자 및 핵심 단행본 노드에 대해 `nlk-interlinker`를 기동하여 Wikidata, LoC, DNB URI를 조회하고, 매핑된 식별자들을 해당 로컬 마크다운 노트의 프론트매터(YAML)에 자동으로 보완합니다.
* **종료 조건 (🔲 HITL 필수)**: 에이전트가 자체 정제한 **"추천 리소스 리스트(Recommended Evidence Pack)"**를 사용자에게 제안합니다. 사용자는 이를 검토하여 불필요한 문헌을 솎아내고 온톨로지 및 집필에 활용할 **"최종 확정 문헌 팩(Confirmed Evidence Pack)"**을 승인합니다. 이 승인이 완료되어야만 Phase 3으로 진입합니다.

### Phase 3: 소스 인제스트 (Source Ingest)
* **목적**: 사용자가 제공한 논문 PDF, 단행본 발췌, 스캔 자료, 원전 자료를 집필 가능한 Markdown/Text와 page map으로 전처리합니다.
* **동원 스킬**: `pdf-extractor` (선택)
* **에이전트 행동**:
  1. `pdf-extractor`가 설치되어 있으면 PDF 입력을 Markdown/Text로 추출하고, 가능한 경우 원문 페이지와 추출 텍스트의 page map을 생성합니다.
  2. PDF 추출은 근거 확보를 위한 전처리입니다. 최종 PDF 렌더링/조판은 Phase 8의 로컬 `theology-pdf` 검수 흐름에서만 다룹니다.
  3. `pdf-extractor`가 없거나 PDF 입력이 없으면 사용자가 제공한 Markdown/Text 자료를 EvidencePack 입력으로 사용합니다.
  4. 추출물에서 핵심 주장 후보, 인용 후보, 페이지 근거를 표시하여 Phase 4의 온톨로지 설계와 Phase 7의 Claim Ledger가 참조할 수 있게 합니다.
* **종료 조건**: 원자료가 Markdown/Text 또는 page map이 있는 추출물 형태로 준비됩니다.

### Phase 4: 분석, 최소 온톨로지 및 집필 설계 (Analysis, Ontology & Outline Design)
* **목적**: 라이팅이 시작되기 **이전에**, Phase 2에서 사용자가 확정한 정제 문헌 팩과 1차 텍스트만을 대상으로 핵심 개념·학자 노선 대립·타협 불가능한 신학적 긴장(Aporia)을 명제망으로 정리하여, 집필 전체를 안내하는 지적 내비게이션을 수립합니다.
* **🔴 온톨로지 분석 대상 범위 (핵심 원칙)**: 온톨로지 명제망의 입력 자료는 오직 **Phase 2에서 사용자가 승인한 "최종 확정 문헌 팩(Confirmed Evidence Pack)"과 Phase 3에서 준비된 1차 텍스트/추출물**로만 제한한다. 라이팅 이후의 최종 에세이를 사후 분석하거나, 승인되지 않은 원시 검색 결과를 온톨로지 명제의 근거로 사용하는 것을 금지한다.
* **동원 스킬**: `ontology-builder`, `theology-discourse-mapper`
* **에이전트 행동**:
  1. **사전(Pre-Writing) 온톨로지 명제 설계**: 확정 문헌 팩과 1차 텍스트를 기반으로, 에세이에서 다룰 핵심 명제(Subject-Predicate-Object)와 아포리아(Aporia) 명제를 RDF Triples 형태로 설계합니다. 각 명제에는 반드시 근거 문헌을 1:1로 명기합니다.
  2. **라이팅 TOC 및 개요 설계**: 수립된 온톨로지 명제들을 서사적 흐름으로 번역하여 에세이의 **장/절 목차(TOC)와 각 섹션별 상세 개요(Outline)**를 작성합니다. 개요에는 각 섹션이 입증할 온톨로지 명제와 배정될 문헌 인용처를 반드시 명시합니다.
* **종료 조건 (🔲 HITL 필수)**: 설계된 **최소 온톨로지 명제망, 라이팅 TOC 및 상세 개요**를 사용자에게 일괄 제시하고 최종 승인(HITL)을 얻습니다. 이 승인이 완료되면 Phase 5 적대적 검증 단계로 진입합니다.

### Phase 5: 적대적 레드팀 검증 (Adversarial Red-Team Audit)
* **목적**: 집필 진입 전, 개요와 온톨로지가 품고 있는 역사적/교리적 갭과 아전인수적 사료 인용(Vibe-interpretation)을 난폭하게 공격하여 개요 설계의 학술적 완성도를 극대화합니다.
* **동원 스킬**: `theology-redteam`
* **에이전트 행동**:
  1. Phase 4에서 완성된 최소 온톨로지와 개요에 대해 `theology-redteam`을 가동하여 적대적 비평 리포트를 출력합니다.
  2. 리포트의 `[Leap-Alert]` 및 `[Evidence-Check]` 경보를 바탕으로, 지목된 갭을 채우기 위한 추가 표적 리서치를 수행합니다.
  3. 리포트의 `[Gap-Filling Directives]` 가이드를 따라 개요(TOC) 내에 가교(Bridge) 단락 및 보완 레퍼런스를 수정한 고도화된 개요 개정안을 작성합니다.
* **종료 조건 (🔲 HITL 필수)**: 레드팀의 공격 지점을 완벽하게 보완한 **"개정된 최종 개요 및 갭 보완 보고서"**를 사용자에게 제시하여 최종 승인을 획득합니다. 이 승인이 완료되어야만 Phase 6 집필을 개시할 수 있습니다.

### Phase 6: SBL 라이팅 & 린팅 (SBL Writing & Citation Linting)
* **목적**: 설계된 온톨로지 뼈대를 엄격히 따라 흐트러짐 없이 논지를 전개하며 SBL 규격 에세이를 작성하고, 인용 관계를 정상화합니다.
* **동원 스킬**: `theology-citation-linker`
* **에이전트 행동**:
  1. 최소 온톨로지의 명제 관계를 본문의 각 문단과 섹션 구조에 1:1로 매핑하여 논지를 잃지 않고 서술합니다.
  2. 서술 시 모든 문장은 한국어 평서문(`~한다`, `~이다`)을 사용합니다.
  3. `theology-citation-linker`를 기동하여 본문 임시 앵커 `[Ref: ...]`를 SBL 2nd Edition 표준 각주 및 참고문헌(한국어 문헌은 겹화살괄호 『 』, 홑화살괄호 「 」 적용)으로 린팅 및 복원합니다.
* **종료 조건**: SBL 규격 에세이 초안 완성.

### Phase 7: Claim Ledger
* **목적**: 본문 핵심 주장마다 근거 문헌, 페이지, 반대 근거, 신뢰도 상태를 추적하여 저널급 주장-근거 정합성을 확보합니다.
* **동원 스킬**: 공유용 프로젝트의 `claim-ledger` CLI, `theology-citation-linker`, `theology-reviewer`
* **에이전트 행동**:
  1. 로컬 `.skills`에 별도 `claim-ledger` 스킬이 없어도 `~/Desktop/MS_Dev.nosync/projects/tawp/skills/claim-ledger/scripts/claim_ledger.py`를 직접 호출합니다.
  2. 본문 핵심 주장마다 `claim_id`를 부여합니다.
  3. 각 claim을 EvidencePack의 `source_id`, 각주, 페이지 범위 또는 page map과 연결합니다.
  4. `support_type`을 `direct`, `indirect`, `contextual`, `contested`로 분류합니다.
  5. 논쟁적 주장에는 `counterevidence`를 요구하고, 누락 시 제출 전 hard gate로 처리합니다.
  6. `confidence`가 `unsupported` 또는 `weak`인 주장은 본문에서 보강하거나 철회합니다.
* **기본 명령**:
```bash
python3 ~/Desktop/MS_Dev.nosync/projects/tawp/skills/claim-ledger/scripts/claim_ledger.py build \
  --file [FileName].md \
  --output [FileName]_ClaimLedger.json

python3 ~/Desktop/MS_Dev.nosync/projects/tawp/skills/claim-ledger/scripts/claim_ledger.py audit \
  --file [FileName].md \
  --ledger [FileName]_ClaimLedger.json \
  --evidence EvidencePack.json \
  --report [FileName]_ClaimLedger_Audit.md \
  --fail-on-unsupported \
  --fail-on-missing-counterevidence
```
* **종료 조건**: 모든 핵심 주장이 Claim Ledger에서 `pass` 또는 검토 가능한 `warn` 상태로 분류됩니다.

### Phase 8: 최종 감사 및 로컬 PDF 검수 (Final Audit)
* **목적**: 에세이의 논증 타당성, Claim Ledger 정합성, 전문 용어 일관성, 각주 구조, PDF 조판 위험을 검사하며, AI 스스로의 지적 허세를 필터링합니다.
* **동원 스킬**: `theology-reviewer`, `theology-terminology-linter`, `theology-citation-linker`, `theology-pdf`, `slash-criticalthink` (자가 검열)
* **에이전트 행동**:
  1. `theology-terminology-linter`를 돌려 `tre_terms.csv`에 어긋나거나 혼용된 용어(예: "성찬" vs "성만찬" 등)를 검출하여 감사 보고서를 작성합니다.
  2. `theology-citation-linker --audit-footnotes --fail-on-footnote-issues`를 실행하여 같은 위치의 연속 각주, 다른 위치의 반복 각주, 본문 호출/하단 정의 불일치를 PDF 전 단계에서 차단합니다.
  3. Claim Ledger와 본문 각주, EvidencePack의 정합성을 대조하여 미근거 핵심 주장과 반대 근거 누락을 검출합니다.
  4. `tawp_quality_gate.py --halt-on-fail`을 실행하여 원고에 Thai/Cyrillic 등 비허용 문자권이 섞였는지, 라틴 문자 음역어가 백틱 코드로 감싸져 PDF에서 모노스페이스로 렌더링될 위험이 있는지 검사합니다.
  5. 로컬 산출이 필요할 때만 `theology-pdf` 컴파일을 실행하고, 폰트 내장·누락 글자·레이아웃 경고 감사가 100점 또는 최소 PASS 기준을 충족하는지 확인합니다.
  6. `#criticalthink`를 통해 논리적 비약이나 인용의 임의 변형(블러핑)이 없는지 최종 자가 진단합니다.
* **종료 조건 (🔲 HITL 필수)**: 감사 보고서를 제시하고, 사용자에게 최종 에세이 완성물 승인을 받습니다.

#### Phase 8.1 Pre-PDF Unicode & Typography Gate

PDF 조판 직전에는 다음 명령을 필수로 실행합니다.

```bash
python3 ~/Desktop/MS_Dev.nosync/.skills/tawp/scripts/tawp_quality_gate.py \
  --file [FileName].md \
  --halt-on-fail
```

차단 규칙:
- 한국어 신학 원고의 허용 문자권은 기본적으로 한글, 라틴 문자, 그리스어, 히브리어, 일반 문장부호로 제한합니다.
- Thai/Cyrillic/Lao/Myanmar/Khmer 문자가 발견되면 OCR 또는 입력기 혼입으로 보고 중단합니다. `στεναγμός`처럼 그리스어 단어 안에 다른 문자권이 섞인 사례는 반드시 교정해야 합니다.
- 라틴 문자 음역어를 백틱 코드로 감싸지 않습니다. `` `peirasmos` ``, `` `pneuma` ``, `` `christon` ``처럼 백틱 처리된 음역어는 PDF에서 `Courier New` 계열 모노스페이스로 렌더링되어 학술 조판을 훼손합니다. 음역어는 plain text 또는 이탤릭(`*peirasmos*`)으로 표기합니다.

---

## 🚨 에이전트 서술 헌법 (Korean Academic Register)
1. **모든 신학 분석 보고서, 에세이 및 담론 보고서의 텍스트는 한국어 평서문(~한다, ~이다)으로 작성한다.**
2. 학술적 권위와 신학적 무게감을 잃지 않는 어조를 유지하며, 문맥을 흐리는 미사여구는 배제한다.
3. 신학적 긴장을 해소하거나 평탄화하려 하지 말고, 온톨로지 단계에서 설계한 아포리아를 본문 논증 안에서 끝까지 긴장감 있게 유지한다.
4. **최종 에세이 문서의 학술적 순수성 보존**:
   - 최종 완성되는 에세이 파일(`[FileName].md`)은 오직 본문 텍스트, SBL 각주, 그리고 실제 본문에 인용된 문헌들만 정렬된 참고문헌(Bibliography) 섹션으로만 구성되어야 합니다.
   - 리서치 과정에서 얻은 전체 선행 연구 서지 링크 리스트(`Appendix: Research Inventory`)는 본문에서 제외하여 별도의 파일 `[FileName]_inventory.md`로 분리 생성해야 합니다.
   - 파이프라인 작동 이력이나 린터 검증 데이터(`Forensic Audit Log`) 역시 본문 하단에 적는 것을 금지하며, 독자적인 감사 파일 `[FileName]_audit_log.md`로 밀어내야 합니다. 이 규격은 `theology-citation-linker`와 같은 검수 엔진 작동 시 자동으로 감지 및 분리(Split & Clean-up) 처리됩니다.
