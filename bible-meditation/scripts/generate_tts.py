#!/usr/bin/env python3
"""bible-meditation Phase 3 — 묵상글의 TTS 대본을 오디오 파일로 합성.

deps: stdlib only. 엔진: macOS 내장 `say`(+`afconvert`, 기본) 또는 edge-tts(설치 시).
실행: python3 generate_tts.py <묵상.md|대본.txt> [--voice Yuna] [--engine say|edge]
      [--out 출력.m4a] [--rate 175]

입력이 .md이면 `%%TTS-SCRIPT: ... %%` 블록을 추출해 합성하고,
그 외 파일은 전체 텍스트를 대본으로 사용한다.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TTS_BLOCK_RE = re.compile(r"%%TTS-SCRIPT:\s*(.*?)\s*%%", re.S)


def extract_script(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".md":
        m = TTS_BLOCK_RE.search(text)
        if not m:
            sys.exit("오류: %%TTS-SCRIPT: ... %% 블록을 찾을 수 없음 (phase3-tts-translation.md 형식 참조)")
        return m.group(1).strip()
    return text.strip()


def synth_say(script: str, out: Path, voice: str, rate: int) -> None:
    if not shutil.which("say"):
        sys.exit("오류: macOS `say` 명령이 없음 — --engine edge를 사용하거나 macOS에서 실행하십시오")
    voices = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout
    if voice not in voices:
        sys.exit(f"오류: 음성 '{voice}' 미설치. 설치된 한국어 음성 확인: say -v '?' | grep ko_KR")
    with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
        aiff = Path(tmp.name)
    try:
        subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(aiff), script], check=True)
        if out.suffix.lower() == ".aiff":
            shutil.move(str(aiff), out)
        else:
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", str(aiff), str(out)], check=True)
    finally:
        aiff.unlink(missing_ok=True)


def synth_edge(script: str, out: Path, voice: str) -> None:
    if not shutil.which("edge-tts"):
        sys.exit("오류: edge-tts 미설치 (uv tool install edge-tts) — 또는 기본 say 엔진 사용")
    edge_voice = voice if "-" in voice else "ko-KR-SunHiNeural"
    subprocess.run(["edge-tts", "--voice", edge_voice, "--text", script,
                    "--write-media", str(out)], check=True)


def main():
    ap = argparse.ArgumentParser(description="묵상 TTS 오디오 생성")
    ap.add_argument("input", help="묵상 .md (TTS 블록 포함) 또는 대본 .txt")
    ap.add_argument("--voice", default="Yuna", help="say 음성(기본 Yuna) 또는 edge-tts 음성명")
    ap.add_argument("--engine", choices=["say", "edge"], default="say")
    ap.add_argument("--out", help="출력 파일 (기본: <입력명>_tts.m4a)")
    ap.add_argument("--rate", type=int, default=175, help="say 발화 속도 wpm (기본 175)")
    args = ap.parse_args()

    src = Path(args.input).expanduser()
    if not src.is_file():
        sys.exit(f"오류: 입력 파일 없음 — {src}")
    out = Path(args.out).expanduser() if args.out else src.with_name(src.stem + "_tts.m4a")

    script = extract_script(src)
    print(f"대본 {len(script)}자 추출 → {args.engine} 엔진으로 합성 중...")
    if args.engine == "edge":
        synth_edge(script, out, args.voice)
    else:
        synth_say(script, out, args.voice, args.rate)

    size_kb = out.stat().st_size // 1024
    if size_kb == 0:
        sys.exit("오류: 출력 파일이 비어 있음")
    print(f"✅ 생성됨: {out} ({size_kb}KB)")


if __name__ == "__main__":
    main()
