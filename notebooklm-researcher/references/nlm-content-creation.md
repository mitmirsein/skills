# 🎙️ NotebookLM 콘텐츠 생성 가이드 (오디오/슬라이드)

> **목적**: jacob-bd의 `notebooklm-mcp-cli`가 제공하는 콘텐츠 생성 기능  
> (팟캐스트 오디오, 스터디 가이드, 브리핑 문서, 슬라이드)을  
> 우리 연구 워크플로우에 통합하는 가이드.

---

## 1. 사용 가능한 콘텐츠 생성 도구

| 기능 | MCP 도구 | CLI 명령 | 설명 |
|:---|:---|:---|:---|
| 팟캐스트 오디오 | `mcp_notebooklm_studio_create` | `nlm audio create <notebook>` | AI 대화형 요약 오디오 생성 |
| 슬라이드 초안 | `mcp_notebooklm_studio_create` | `nlm slides create <notebook>` | 프레젠테이션 초안 |
| 슬라이드 수정 | `mcp_notebooklm_studio_revise` | `nlm slides revise <notebook>` | 슬라이드 내용 수정 |
| 아티팩트 다운로드 | `mcp_notebooklm_download_artifact` | `nlm download audio <notebook> <id>` | 생성된 파일 다운로드 |
| 공개 링크 | `mcp_notebooklm_notebook_share_*` | `nlm share public <notebook>` | 공유 링크 생성 |

---

## 2. 오디오 팟캐스트 생성 워크플로우

### 용도: 신학 연구 결과를 AI 대화형 팟캐스트로 변환

```
1. 노트북 소스 확인 (충분한 자료가 있어야 품질이 좋음)
   → mcp_notebooklm_notebook_get(notebook_id)

2. 오디오 생성 요청
   → mcp_notebooklm_studio_create(
        notebook_id=<id>,
        artifact_type="audio",
        customization="한국어로 대화해줘" (선택)
      )
   * 생성 시간: 약 2~5분

3. 상태 확인 (폴링)
   → mcp_notebooklm_studio_get(notebook_id, artifact_id)

4. 다운로드
   → mcp_notebooklm_download_artifact(notebook_id, artifact_id)
   또는 CLI: nlm download audio <notebook> <artifact-id>
```

### 활용 시나리오:
- 설교 준비: 묵상 노트를 팟캐스트로 변환 → 이동 중 청취
- 논문 요약: 여러 논문 소스 → 대화형 요약 오디오
- 강의 예습: 강의 자료 → 대화 형식 정리

---

## 3. 슬라이드 생성 워크플로우

### 용도: 연구/강의 자료를 슬라이드로 자동 변환

```
1. 슬라이드 생성
   → mcp_notebooklm_studio_create(
        notebook_id=<id>,
        artifact_type="slides"
      )

2. 슬라이드 수정 (필요 시)
   → mcp_notebooklm_studio_revise(
        notebook_id=<id>,
        artifact_id=<slide_id>,
        instruction="각 슬라이드에 성경 구절 인용 추가해줘"
      )

3. 다운로드 또는 공유 링크 생성
   → nlm download slides <notebook> <artifact-id>
   → nlm share public <notebook>
```

---

## 4. 빠른 CLI 사용법

```bash
# 전체 워크플로우 (CLI로 직접 실행)
nlm notebook list                           # 노트북 목록
nlm audio create "신학연구" --confirm       # 오디오 생성 (확인 후)
nlm download audio "신학연구" <artifact-id> # 다운로드
nlm share public "신학연구"                 # 공개 링크 생성

# 슬라이드
nlm studio create "신학연구" --type slides
nlm slides revise "신학연구" --instruction "한국어로 제목 수정"
```

---

## 5. 주의사항

| 항목 | 내용 |
|:---|:---|
| 생성 시간 | 오디오 2~5분, 슬라이드 1~3분 (비동기, 폴링 필요) |
| 언어 | 소스 언어 자동 감지. 한국어 소스 → 한국어 오디오 |
| 다운로드 경로 | 기본값: `~/Downloads/` |
| 재생성 | 같은 노트북에서 여러 번 생성 가능 (버전별 artifact_id) |

---

*NotebookLM Content Creation Guide | notebooklm-researcher v3.1 | MS_Dev*
