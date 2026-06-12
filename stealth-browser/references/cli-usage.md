# Stealth Browser: CLI Commands & Usage

`agents/stealth_browser.py`를 터미널에서 제어하기 위한 명령어와 옵션입니다.

## 🛠️ CLI Patterns

### 1. Basic Stealth Browsing
```bash
/stealth https://www.google.com
```

### 2. Local Profile
로컬 격리 프로필 이름을 지정하여 브라우징합니다.
```bash
/stealth https://www.notion.so --profile research
```

### 3. Parallel Sessions (병렬 브라우징)
각기 다른 전용 프로필(`Worker_N`)로 여러 웹페이지를 동시에 엽니다.
```bash
/stealth-parallel https://google.com https://naver.com https://daum.net
```

### 4. Multi-Provider & 우회 전략
기본 로컬 브라우저 외에 클라우드 브라우저(`lightpanda`, `browserbase`, `kernel`)를 호출하여 안티봇 환경을 회피할 수 있습니다.
```bash
python agents/stealth_browser.py https://kernel.sh --provider kernel
```
*(호출 시 `BROWSERBASE_API_KEY`, `KERNEL_API_KEY` 등의 환경변수가 필요합니다)*

### 5. CLI Wrapper (순간 텍스트 추출 모드)
에이전트 단기 작업을 위해 DOM 전체 텍스트만 추출하고 창을 닫습니다. `stealth-browser`를 단순 쉘 명령처럼 사용할 때 매우 효율적입니다.
```bash
python agents/stealth_browser.py https://example.com --provider lightpanda --extract
```

## ⚠️ Operation Warning
- **Session Isolation**: 기본 프로필은 `~/.msdev-browser/profiles/` 아래에 생성됩니다.
- **Login Required Sites**: 로그인 세션 공유/복제는 지원하지 않습니다. 필요한 경우 수동 로그인 후 해당 격리 프로필을 재사용합니다.
