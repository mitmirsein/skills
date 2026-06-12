---
name: hwp-converter
description: >
  Converts HWP/HWPX (Korean word processor) documents to Markdown on both
  macOS and Windows, with zero-config automatic environment bootstrap (uv,
  pandoc, hwp2md). Use when the user provides an HWP/HWPX file to convert
  or read. 키워드: 한글 문서 변환, HWP 변환, 아래아한글
version: 1.0.1
status: active
---

# 📝 HWP Converter Skill (Cross-Platform Zero-Config)

이 스킬은 한글(HWP/HWPX) 문서를 Markdown으로 변환합니다. **macOS와 Windows를 모두 지원**하며, 환경 설정이 전혀 되어 있지 않아도 에이전트가 스스로 환경을 구축합니다.

## 🆘 초심자 대응 및 저장 정책 (Policy)

### 1. 제로-컨피그 프로토콜
에이전트는 사용자의 운영체제를 확인한 후 도구(`uv`, `pandoc`, `hwp2md`)가 없다면 승인 후 자동 설치 스크립트를 실행합니다.
- **macOS**: `bash <이 스킬 폴더의 절대 경로>/scripts/bootstrap.sh`
- **Windows**: `powershell -ExecutionPolicy Bypass -File "<이 스킬 폴더의 절대 경로>\scripts\bootstrap.ps1"`

### 2. 저장 경로 정책 (Storage Policy)
**별도의 요청이 없다면, 변환 결과물(.md)은 반드시 원본 파일(.hwp)이 위치한 동일한 경로에 저장합니다.** 파일 이름은 원본과 동일하게 하되 확장자만 `.md`로 변경합니다.

## 🛠️ 주요 실행 방식

> **중요**: `scripts/convert_hwp.py`를 실행할 때는 반드시 **이 스킬 폴더 기준의 절대 경로**를 사용합니다. `uv run`은 스크립트 상단의 인라인 메타데이터(PEP 723)를 읽어 의존성을 자동 해결하므로, 어떤 cwd에서 실행해도 작동합니다.

### 1. 권장 방식 (uv 자동화 - 원본 경로 저장)
```bash
# 별도의 출력 경로 지정 없이 실행하면 원본 파일 옆에 .md가 생성됩니다.
uv run <이 스킬 폴더>/scripts/convert_hwp.py "변환할파일.hwp"
```

### 2. 고속 네이티브 방식
```bash
# macOS
~/go/bin/hwp2md convert "파일.hwp" -o "파일.md"

# Windows
%USERPROFILE%\go\bin\hwp2md.exe convert "파일.hwp" -o "파일.md"
```

## ⚙️ 실행 파이프라인 (Pipeline)

1.  **OS 인지 및 경로 확인**: 현재 OS와 원본 파일의 위치를 파악합니다.
2.  **엔진 가동**: `uv run` 모드를 기본으로 사용하며, 원본 경로에 파일을 생성합니다.
3.  **사후 검증**: 변환된 `.md` 파일이 원본 경로에 정상 생성되었는지 확인 후 사용자에게 보고합니다.

## 🛑 주의사항
- **윈도우 사용자**: PowerShell 환경에서 `winget`을 통해 도구를 설치합니다. `winget`이 없으면 에이전트가 설치 방법을 안내합니다.
- **macOS 사용자**: Homebrew가 없으면 자동 설치합니다 (비대화형 모드).
- **LibreOffice**: 구형 HWP(3.0 이하) 변환 실패 시 LibreOffice 설치를 권장하며, 에이전트가 친절히 안내합니다.
