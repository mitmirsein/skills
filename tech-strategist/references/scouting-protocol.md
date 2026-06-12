# Tech Scout: Repository Infiltration Protocol

외부 GitHub 저장소를 분석하여 MS_Dev 생태계에 이식 가능한 가치 있는 지성(Loot)을 추출하기 위한 5단계 작전 지침입니다.

## 🎯 Objective
- 코드의 단순 복제가 아닌, 외부 프로젝트의 **프롬프트, 워크플로우, 아키텍처 패턴** 등 '적응 가능한 지능(Adaptable Intelligence)'을 식별하고 제안하는 것입니다.

## 🚀 The Scouting Lifecycle (5-Phase)

### 1. Infiltration (잠입)
- **Landing Zone**: 루트에 `temp_scout_<repo_name>` 임시 디렉토리를 생성합니다.
- **Clone**: `git clone`을 통해 타겟 저장소를 로컬로 가져옵니다.

### 2. Reconnaissance (정찰)
- **README Analysis**: 프로젝트의 핵심 제안 가치를 파악합니다.
- **Terrain Mapping**: `ls -R` 또는 `tree`를 사용하여 파일 구조를 시각화합니다.
- **Identify Assets**: `prompts/`, `workflows/`, `utils/`, 혹은 행동을 정의하는 `yaml/json` 설정 파일을 고가치 타겟(Loot)으로 식별합니다.

### 3. Intelligence Report (보고)
- 식별된 자산과 이식 가능한 스킬/취향(Instincts)을 요약하여 **Scouting Report**를 발행합니다.

### 4. Wait for Command (대기)
- **절대 즉시 추출하지 마십시오.** 사용자의 최종 '강탈(Exfiltrate)' 명령을 기다립니다.

### 5. Exfiltration (강탈 및 탈출)
- 승인된 자산의 내용을 캡처하고 MS_Dev 규격의 새로운 `SKILL.md`로 변환하여 이식합니다.
- 작업 완료 후 임시 디렉토리를 완전히 삭제(`rm -rf`)하여 흔적을 지웁니다.
