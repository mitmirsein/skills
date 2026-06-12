# Mole Manager 알려진 함정 및 에러 대응

## ⚠️ 명령어 네이밍 함정

### `mole` vs `mo`
- Homebrew로 설치하면 바이너리는 `/opt/homebrew/bin/mole`이지만, **실제 CLI 명령어는 `mo`**입니다.
- `mole clean` → ❌ 작동 안 함
- `mo clean` → ✅ 올바른 명령어

```bash
# 설치 확인
which mo          # /opt/homebrew/bin/mo
mo --version      # 버전 확인
```

---

## 🔴 삭제 불가 케이스

| 상황 | 증상 | 대응 |
|------|------|------|
| 시스템 앱 삭제 시도 | Mole이 자동 필터링 후 건너뜀 | 정상 동작, 시스템 앱은 제거 대상에서 제외됨 |
| 앱 실행 중 uninstall | 일부 파일 잠금으로 제거 실패 | 앱 먼저 종료 후 재시도 |
| SIP 보호 경로 | `/System/`, `/usr/` 등 수정 불가 | Mole이 자동 스킵 |

---

## 🟡 성능 관련 함정

### Xcode 캐시 삭제 후
- Derived Data 재생성으로 다음 빌드가 매우 느려짐.
- 대형 프로젝트 빌드 직전에는 `mo clean`에서 Xcode 항목 화이트리스트 권장.

### Spotlight 재인덱싱
- `mo optimize` 후 Spotlight 재인덱싱이 수십 분 소요될 수 있음.
- 인덱싱 중 CPU 사용량 급증 → 정상 동작.

### npm/pnpm 캐시 삭제
- 글로벌 패키지 캐시 삭제 후 다음 `npm install`이 느려짐.
- 오프라인 환경에서 삭제 금지.

---

## 🟡 Syncthing 환경 특이사항

현재 환경은 M1 MacBook Air + Intel iMac이 Syncthing으로 연결된 구성입니다.

- **`.venv` 경로**: Syncthing 동기화 경로에 있는 가상환경은 `mo purge` 스캔 대상이 될 수 있음.  
  → purge 전 스캔 경로 확인: `mo purge --paths`  
  → `.venv-m1`, `.venv-intel` 등 `.stignore` 처리된 경로만 정리 권장.
- **`node_modules.nosync`**: `.nosync` 확장자가 있어도 purge 스캔에 포함될 수 있으니 dry-run으로 먼저 확인.

---

## 🟡 Docker 관련

- `mo clean`이 Docker 이미지를 정리 대상으로 포함할 수 있음.
- 필요한 이미지가 있다면 `--whitelist`로 보호하거나, Docker Desktop을 종료한 상태에서 실행.

---

## 🟢 자주 묻는 에러

### "permission denied"
```bash
sudo mo clean    # 일부 시스템 경로는 sudo 필요
```

### "command not found: mo"
```bash
brew install mole   # 재설치
# 또는
export PATH="/opt/homebrew/bin:$PATH"  # PATH 확인
```

### 업데이트 실패
```bash
mo update --force   # 강제 재설치
# 또는
brew upgrade mole   # Homebrew로 업데이트
```
