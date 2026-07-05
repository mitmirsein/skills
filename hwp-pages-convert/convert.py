#!/usr/bin/env python3
import os
import sys
import re
import glob
import subprocess
import tempfile
from dochan import Dochan

def clean_markdown(text):
    # 1. Pandoc 변환 시 유입되는 Pages 특유의 RTL 태그 및 구두점 괄호 정규화
    # 예: ["]{dir="rtl"} -> ", [']{dir="rtl"} -> '
    text = re.sub(r'\[(.*?)\]\{\s*dir="rtl"\s*\}', r'\1', text)
    text = re.sub(r'\{\s*dir="rtl"\s*\}', '', text)

    # 2. 이탤릭체(*text* 또는 _text_)를 볼드체(**text**)로 변환 (볼드 강조 규정 준수)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'**\1**', text)
    text = re.sub(r'(?<!_)_(?!_)(.*?)(?<!_)_(?!_)', r'**\1**', text)

    # 3. 볼드 기호(**) 바로 뒤에 한국어 조사나 영숫자가 오면 Zero-Width Space(U+200B) 삽입
    text = re.sub(r'\*\*(.*?)\*\*([a-zA-Z0-9가-힣])', r'**\1**' + '\u200b' + r'\2', text)
    
    # 4. 연속된 공백 라인 정제 (가독성 향상)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def convert_hwp(input_path, output_md_path):
    print(f"HWP 변환 시작: {os.path.basename(input_path)}...")
    doc = Dochan(input_path)
    markdown_content = doc.to_markdown()
    cleaned_content = clean_markdown(markdown_content)
    
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
    print(f"✅ HWP 변환 완료: {output_md_path}")
    return True

def convert_pages(input_path, output_md_path):
    print(f"Pages 변환 시작: {os.path.basename(input_path)}...")
    abs_pages_path = os.path.abspath(input_path)
    abs_md_path = os.path.abspath(output_md_path)
    
    # 임시 docx 파일 생성
    temp_docx = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    temp_docx.close()
    abs_docx_path = temp_docx.name

    try:
        # AppleScript를 사용하여 Pages 앱을 통해 docx로 내보내기.
        # 경로는 f-string 삽입이 아니라 osascript 인자(on run argv)로 전달한다 —
        # 경로에 큰따옴표가 포함돼도 스크립트가 깨지거나 임의 AppleScript가 주입되지 않도록(B4-20).
        applescript_code = '''
        on run argv
            set posixPagesPath to item 1 of argv
            set posixDocxPath to item 2 of argv
            set pagesFile to POSIX file posixPagesPath as alias
            set docxFile to POSIX file posixDocxPath

            tell application "Pages"
                set myDoc to open pagesFile
                export myDoc to docxFile as Microsoft Word
                close myDoc saving no
            end tell
        end run
        '''

        result = subprocess.run(
            ["osascript", "-e", applescript_code, abs_pages_path, abs_docx_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"AppleScript 실행 실패: {result.stderr.strip()}")
            
        # Pandoc을 사용하여 DOCX를 Markdown으로 변환
        subprocess.run([
            "pandoc",
            "--wrap=none",
            abs_docx_path,
            "-o",
            abs_md_path
        ], check=True)
        
        # 마크다운 스타일 보정
        with open(abs_md_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        cleaned_content = clean_markdown(content)
        
        with open(abs_md_path, "w", encoding="utf-8") as f:
            f.write(cleaned_content)
            
        print(f"✅ Pages 변환 완료: {abs_md_path}")
        return True
        
    except Exception as e:
        print(f"❌ Pages 변환 실패 ({os.path.basename(abs_pages_path)}): {e}")
        return False
        
    finally:
        # 임시 docx 파일 삭제
        if os.path.exists(abs_docx_path):
            os.remove(abs_docx_path)

def convert_file(input_path, output_dir=None):
    if not os.path.exists(input_path):
        print(f"Error: 파일이 존재하지 않습니다: {input_path}")
        return False
        
    # 출력 경로 설정
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.splitext(os.path.basename(input_path))[0] + ".md"
        output_md_path = os.path.join(output_dir, filename)
    else:
        output_md_path = os.path.splitext(input_path)[0] + ".md"
        
    ext = os.path.splitext(input_path.lower())[1]
    
    try:
        if ext in ('.hwp', '.hwpx'):
            return convert_hwp(input_path, output_md_path)
        elif ext == '.pages':
            return convert_pages(input_path, output_md_path)
        else:
            print(f"Error: 지원하지 않는 확장자입니다 ({ext}): {input_path}")
            return False
    except Exception as e:
        print(f"❌ 변환 오류 ({os.path.basename(input_path)}): {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python convert.py <입력_파일_또는_디렉토리> [<출력_디렉토리>]")
        sys.exit(1)
        
    target_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if os.path.isdir(target_path) and not target_path.endswith(".pages"):
        # 디렉토리 일괄 변환 (단, 패키지형 .pages는 제외)
        files = (
            glob.glob(os.path.join(target_path, "*.hwp")) + 
            glob.glob(os.path.join(target_path, "*.hwpx")) + 
            glob.glob(os.path.join(target_path, "*.pages"))
        )
        if not files:
            print(f"디렉토리 내에 변환 가능한 파일(HWP/HWPX/Pages)이 없습니다: {target_path}")
            sys.exit(1)
            
        print(f"총 {len(files)}개의 문서를 변환합니다...")
        success_count = 0
        for f in files:
            if convert_file(f, output_dir):
                success_count += 1
        print(f"\n🎉 전체 작업 완료: {success_count}/{len(files)} 성공")
    else:
        # 단일 파일 변환 (패키지형 .pages 포함)
        convert_file(target_path, output_dir)

if __name__ == "__main__":
    main()
