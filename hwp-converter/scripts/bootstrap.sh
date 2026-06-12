#!/bin/bash
set -e

# HWP Converter Zero-Config Bootstrap Script
# 초심자를 위한 환경 자동 구축 스크립트 (macOS / Linux)

# 스킬 루트 디렉터리로 이동 (uv sync가 pyproject.toml을 찾을 수 있도록)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SKILL_ROOT"

echo "🚀 HWP 변환을 위한 환경 점검 및 설치를 시작합니다..."
echo "   스킬 루트: $SKILL_ROOT"

# 1. Homebrew 체크 및 설치
if ! command -v brew &> /dev/null; then
    echo "🔍 Homebrew가 없습니다. 설치를 시도합니다..."
    # NONINTERACTIVE=1: 에이전트 환경에서 "Press RETURN" 프롬프트를 건너뜁니다.
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Apple Silicon Mac에서는 /opt/homebrew/bin이 PATH에 없을 수 있습니다.
    if [ -f /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew 확인됨"
fi

# 2. uv (Python 관리자) 체크 및 설치
if ! command -v uv &> /dev/null; then
    echo "🔍 uv가 없습니다. 설치를 시작합니다..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # uv는 ~/.local/bin에 설치됩니다. 현재 세션에 PATH를 즉시 반영합니다.
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✅ uv 확인됨"
fi

# 3. Pandoc 설치
if ! command -v pandoc &> /dev/null; then
    echo "🔍 Pandoc 설치 중..."
    brew install pandoc
else
    echo "✅ Pandoc 확인됨"
fi

# 4. Go & hwp2md 설치
export PATH="$HOME/go/bin:$PATH"  # go install 결과물 경로를 미리 PATH에 추가

if ! command -v hwp2md &> /dev/null; then
    echo "🔍 Go 기반 변환 엔진(hwp2md) 설치 중..."
    if ! command -v go &> /dev/null; then
        brew install go
    fi
    go install github.com/roboco-io/hwp2md@latest
else
    echo "✅ hwp2md 확인됨"
fi

# 5. Python 의존성 설치 (이미 스킬 루트에 cd한 상태)
echo "🔍 Python 라이브러리 동기화 중..."
uv sync

echo ""
echo "✨ 모든 준비가 끝났습니다! 이제 HWP 파일을 마크다운으로 변환할 수 있습니다."
echo "   사용법: uv run $SKILL_ROOT/scripts/convert_hwp.py \"변환할파일.hwp\""
