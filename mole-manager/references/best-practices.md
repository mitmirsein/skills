# Mole Manager 운영 수칙

## 🔑 핵심 원칙

### 1. Dry-Run 필수 원칙
**파괴적 작업(clean, uninstall, optimize, purge, installer, remove)은 반드시 `--dry-run`으로 먼저 미리보기 후 사용자 명시적 승인을 받아야 합니다.**

```bash
# 올바른 순서
mo clean --dry-run   # Step 1: 미리보기
# → 사용자 확인 후
mo clean             # Step 2: 실행
```

> `mo status`, `mo analyze`는 읽기 전용이므로 즉시 실행 가능.

---

## 🎯 작업별 수칙

### mo clean
- Xcode, Docker 캐시는 재생성에 시간이 걸리므로 삭제 전 필요성 확인.
- `--whitelist`로 중요한 캐시(예: brew 다운로드 캐시)를 보호 목록에 추가.
- 개발 환경에서는 npm/pnpm 글로벌 캐시 삭제 후 인터넷 연결 필요.

### mo uninstall
- 시스템 앱(Safari, Mail 등)은 제거 불가. Mole이 자동으로 필터링함.
- iCloud 연동 앱 제거 시 데이터 백업 여부 먼저 확인.
- 앱 실행 중 uninstall 시도 시 먼저 종료 요청.

### mo optimize
- 시스템 서비스 재시작으로 잠시 성능 저하가 발생할 수 있음.
- Spotlight 재인덱싱은 시간이 걸리므로 유휴 시간에 실행 권장.
- `--whitelist`로 자주 사용하는 서비스를 보호 목록에 추가.

### mo purge
- `node_modules` 제거 시 `package-lock.json`이 있는지 먼저 확인.
- `.venv` 제거 시 이 머신에서 재생성 가능한지 확인 (Python 버전, 의존성).
- Syncthing 동기화 경로에 있는 `.venv`는 삭제 전 특별 주의 (AGENTS.md 수칙).
- `mo purge --paths`로 스캔 경로를 MS_Dev, MS_Library, MS_Thoughts 특화 설정 권장.

### mo analyze
- 외장 드라이브 포함: `mo analyze /Volumes`
- 대용량 디렉터리 발견 시 직접 삭제 전 purge 또는 별도 확인 절차 진행.

---

## ⚡ 추천 워크플로우

### 월간 시스템 정리 루틴
```bash
mo status              # 현재 상태 파악
mo analyze             # 대용량 파일 식별
mo clean --dry-run     # 청소 대상 확인
mo clean               # 실행
mo purge --dry-run     # 프로젝트 정크 확인
mo purge               # 실행
mo optimize --dry-run  # 최적화 대상 확인
mo optimize            # 실행
```

### 앱 삭제 루틴
```bash
mo uninstall --dry-run  # 제거될 파일 목록 확인
mo uninstall            # 실행
```

---

## ⚠️ 주의사항

- `mo remove`는 Mole 자체를 제거하는 명령. 일반 청소 작업에 사용 금지.
- `mo update --nightly`는 미검증 빌드이므로 안정적 환경에서는 사용 자제.
- MS_Library 및 MS_Thoughts 볼트 내 `node_modules.nosync` 등 Syncthing 제외 경로는 purge 스캔에서 제외 권장.
