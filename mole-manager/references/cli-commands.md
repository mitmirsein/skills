# Mole CLI 명령어 레퍼런스

> 이진파일 위치: `/opt/homebrew/bin/mole`  
> 실제 호출 명령어: **`mo`** (mole → mo alias)  
> GitHub: https://github.com/tw93/Mole

---

## 1. mo clean — 시스템 청소

```bash
mo clean              # 캐시·로그·임시파일·개발 정크 삭제 (대화형)
mo clean --dry-run    # ⚠️ 삭제 대상 미리보기 (파괴 없음)
mo clean --whitelist  # 화이트리스트(보호 캐시) 관리
```

**청소 대상 예시:**
- macOS 시스템 캐시 (`~/Library/Caches`)
- Xcode 파생 데이터, 시뮬레이터 캐시
- npm / pnpm / bun 캐시
- Docker 이미지·컨테이너 레이어
- 로그 파일 (`~/Library/Logs`)

---

## 2. mo uninstall — 앱 완전 제거

```bash
mo uninstall              # 앱 선택 후 완전 제거 (잔여 파일 포함)
mo uninstall --dry-run    # ⚠️ 제거 대상 미리보기
```

**제거 범위:**
- `/Applications/` 앱 본체
- `~/Library/Application Support/` 잔여 데이터
- `~/Library/Preferences/` 설정 파일
- `~/Library/Caches/` 앱 캐시

> AppCleaner 대체 도구로 사용.

---

## 3. mo optimize — 시스템 최적화

```bash
mo optimize             # 캐시 재구축·서비스 새로고침
mo optimize --dry-run   # ⚠️ 최적화 대상 미리보기
mo optimize --whitelist # 보호 항목 관리
```

**최적화 작업:**
- Spotlight 인덱스 재구축
- Launch Services 데이터베이스 재구축
- DNS 캐시 플러시
- 시스템 서비스 새로고침

---

## 4. mo analyze — 디스크 분석

```bash
mo analyze             # 현재 볼륨 디스크 점유율 시각화
mo analyze /Volumes    # 외장 드라이브 포함 분석
```

> DaisyDisk의 CLI 대체. 대용량 디렉터리를 트리 형식으로 시각화.

---

## 5. mo status — 실시간 시스템 모니터링

```bash
mo status    # CPU·GPU·메모리·디스크·네트워크 실시간 대시보드
```

> iStat Menus의 CLI 대체. 일회성 스냅샷 출력.

---

## 6. mo purge — 프로젝트 아티팩트 제거

```bash
mo purge              # 프로젝트 빌드 결과물·의존성 제거 (대화형)
mo purge --dry-run    # ⚠️ 제거 대상 미리보기
mo purge --paths      # 스캔 디렉터리 설정
```

**제거 대상 예시:**
- `node_modules/`, `.next/`, `dist/`, `build/`
- Python `__pycache__/`, `.venv/`
- Rust `target/`
- Java `.gradle/`, `target/`

---

## 7. mo installer — 설치 파일 정리

```bash
mo installer            # 다운로드된 .dmg·.pkg 설치 파일 탐색·제거
mo installer --dry-run  # ⚠️ 제거 대상 미리보기
```

---

## 8. mo touchid — Touch ID 설정

```bash
mo touchid enable             # sudo에 Touch ID 활성화
mo touchid enable --dry-run   # ⚠️ 변경사항 미리보기
```

---

## 9. 기타 유지보수 명령어

```bash
mo update           # 최신 안정 버전으로 업데이트
mo update --force   # 강제 재설치
mo update --nightly # 최신 개발 빌드 설치
mo completion       # 셸 탭 자동완성 설정
mo remove           # Mole 시스템에서 제거
mo --version        # 현재 버전 확인
```

---

## 10. 전역 플래그

| 플래그 | 설명 |
|--------|------|
| `--dry-run` | 실제 변경 없이 작업 대상 미리보기 |
| `--debug` | 상세 작업 로그 출력 |
| `--whitelist` | 보호 항목 관리 (clean, optimize) |
| `--paths` | 스캔 경로 설정 (purge) |
| `--help` | 도움말 출력 |
| `--version` | 버전 출력 |
