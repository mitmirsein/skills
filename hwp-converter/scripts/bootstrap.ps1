# HWP Converter Zero-Config Bootstrap Script for Windows (PowerShell)
# 윈도우 초심자를 위한 환경 자동 구축 스크립트

$ErrorActionPreference = "Stop"

# 스킬 루트 디렉터리로 이동 (uv sync가 pyproject.toml을 찾을 수 있도록)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillRoot = Split-Path -Parent $ScriptDir
Set-Location $SkillRoot

Write-Host "🚀 Windows 환경에서 HWP 변환 설정을 시작합니다..." -ForegroundColor Cyan
Write-Host "   스킬 루트: $SkillRoot"

# 1. winget 존재 여부 확인 (Windows 10 구버전에는 없을 수 있음)
if (!(Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️ winget이 설치되어 있지 않습니다." -ForegroundColor Yellow
    Write-Host "   Microsoft Store에서 'App Installer'를 설치하거나,"
    Write-Host "   https://aka.ms/getwinget 에서 직접 다운로드하세요."
    Write-Host "   winget 설치 후 이 스크립트를 다시 실행해 주세요."
    exit 1
}

# 2. uv (Python 관리자) 설치
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "🔍 uv가 없습니다. 설치를 시작합니다..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    # uv 설치 후 PATH를 현재 세션에 즉시 반영합니다.
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
} else {
    Write-Host "✅ uv 확인됨"
}

# 3. Pandoc 설치
if (!(Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Pandoc 설치 중..."
    winget install JohnMacFarlane.Pandoc --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
} else {
    Write-Host "✅ Pandoc 확인됨"
}

# 4. Go & hwp2md 설치
if (!(Get-Command go -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Go 설치 중..."
    winget install GoLang.Go --silent --accept-package-agreements --accept-source-agreements
    # winget 설치 후 PATH를 현재 세션에 강제 갱신합니다.
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Go 바이너리 경로를 현재 세션 PATH에 추가
$GoBinPath = "$env:USERPROFILE\go\bin"
if ($env:Path -notlike "*$GoBinPath*") {
    $env:Path += ";$GoBinPath"
}

if (!(Get-Command hwp2md -ErrorAction SilentlyContinue)) {
    if (Get-Command go -ErrorAction SilentlyContinue) {
        Write-Host "📦 hwp2md 엔진 설치 중..."
        go install github.com/roboco-io/hwp2md@latest
    } else {
        Write-Host "⚠️ Go 설치 후 터미널을 껐다 켠 뒤 다시 이 스크립트를 실행해 주세요." -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✅ hwp2md 확인됨"
}

# 5. Python 의존성 설치 (이미 스킬 루트에 cd한 상태)
Write-Host "🔍 Python 라이브러리 동기화 중..."
uv sync

Write-Host ""
Write-Host "✨ 모든 준비가 끝났습니다! 윈도우에서도 HWP 변환이 가능합니다." -ForegroundColor Green
Write-Host "   사용법: uv run $SkillRoot\scripts\convert_hwp.py `"변환할파일.hwp`""
Write-Host "⚠️ 설치 후 명령어가 인식되지 않으면 터미널을 껐다 켜주세요."
