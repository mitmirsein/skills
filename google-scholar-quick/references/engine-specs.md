# Google Scholar Quick: CDP Engine Specs

Google Scholar에서 저비용, 고속으로 논문 리스트를 확보하기 위한 기술 명세입니다.

## ⚡ CDP (Chrome DevTools Protocol) 가속
- **Engine**: Playwright CLI (Headless Mode).
- **Efficiency**: `browser_subagent` 대비 약 99%의 토큰을 절약합니다 (평균 500 토큰 소모).
- **Scope**: 논문의 제목, 저자, 연도, URL 및 단순 인용 횟수 데이터만 정밀 타격하여 수집합니다.

## 🚀 CLI Usage
```bash
zsh google_scholar_quick_search.sh "<query>"
```

## 🛡️ Usage Policy
- **Low-Cost Research**: 대규모 문헌 탐색의 첫 단계(Filtering)에서 사용을 권장합니다.
- **Detailed Analysis**: 논문 초록이나 본문에 대한 심층 분석이 필요한 경우 `google-scholar-semantic`으로 전환하십시오.
