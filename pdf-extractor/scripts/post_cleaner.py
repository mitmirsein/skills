"""PDF 추출 Markdown의 하이프네이션·문단·블록 구조를 정제합니다."""

import os
import re
import sys


# 문장 종결 부호 `.` 로 끝나도 문장이 끝난 게 아닌 약어들
# (이것들 뒤에서 문단을 flush 하면 신학 텍스트 문장이 중간에 잘림)
ABBREVIATIONS = {
    # 라틴/영어
    'cf', 'cf.', 'vgl', 'vgl.', 'ibid', 'op', 'cit', 'et', 'al', 'al.',
    'ed', 'ed.', 'eds', 'trans', 'tr', 'no', 'nr', 'vol', 'vols', 'pp',
    'esp', 'chap', 'ch', 'sec', 'fig', 'cap', 'col', 'fol', 'lit',
    'i.e', 'e.g', 'viz', 'approx', 'incl', 'St', 'Jr', 'Sr', 'Dr', 'Prof',
    # 독일어
    'z.B', 'u.a', 'd.h', 'usw', 'bzw', 'sog', 'Hrsg', 'Hg', 'Bd', 'Bde',
    'Sp', 'Aufl', 'Diss', 'Anm', 'ebd', 'a.a.O', 'f', 'ff', 'S',
    # 한국어 학술
    '참고', '참조', '이하', '재인용',
}

PAGE_MARKER_RE = re.compile(r'^={5}\s+p\.\d+\s+={5}$')
PROTECTED_TOKEN_RE = re.compile(r'^\ue000pdf-extractor-\d+\ue001$')
FENCE_START_RE = re.compile(r'^[ \t]{0,3}(`{3,}|~{3,})')
TABLE_ROW_RE = re.compile(r'^\s*(?:\|.*\||[^|\n]+\|[^|\n]+)\s*$')
LIST_ITEM_RE = re.compile(
    r'^\s*(?:[-+*]\s+|\d+[.)]\s+|[A-Za-z][.)]\s+|\([0-9A-Za-z]+\)\s+)'
)
HORIZONTAL_RULE_RE = re.compile(r'^\s*(?:\*\s*){3,}$|^\s*(?:-\s*){3,}$|^\s*(?:_\s*){3,}$')


def _new_protected_token(protected) -> str:
    token = f"\ue000pdf-extractor-{len(protected)}\ue001"
    protected[token] = ""
    return token


def _replace_protected_block(
    block: str,
    protected,
) -> str:
    """블록을 단일 토큰으로 치환하되 원래 줄 끝 여부는 보존합니다."""
    token = _new_protected_token(protected)
    if block.endswith("\r\n"):
        protected[token] = block[:-2]
        return token + "\r\n"
    if block.endswith(("\n", "\r")):
        protected[token] = block[:-1]
        return token + block[-1]
    protected[token] = block
    return token


def _protect_fenced_blocks(content: str, protected) -> str:
    """fenced code block을 후속 정규화에서 제외합니다."""
    lines = content.splitlines(keepends=True)
    output = []
    index = 0
    while index < len(lines):
        raw_line = lines[index].rstrip("\r\n")
        opening = FENCE_START_RE.match(raw_line)
        if not opening:
            output.append(lines[index])
            index += 1
            continue

        marker = opening.group(1)
        marker_char = marker[0]
        marker_length = len(marker)
        close_re = re.compile(
            rf'^[ \t]{{0,3}}{re.escape(marker_char)}{{{marker_length},}}[ \t]*$'
        )
        end = index + 1
        while end < len(lines):
            if close_re.match(lines[end].rstrip("\r\n")):
                end += 1
                break
            end += 1
        output.append(_replace_protected_block("".join(lines[index:end]), protected))
        index = end
    return "".join(output)


def _protect_html_comments(content: str, protected) -> str:
    """HTML 주석(특히 페이지 주석)의 내용과 줄바꿈을 보존합니다."""

    def replace(match) -> str:
        return _replace_protected_block(match.group(0), protected).rstrip("\n")

    return re.sub(r'<!--.*?-->', replace, content, flags=re.DOTALL)


def _is_indented_code_line(line: str) -> bool:
    return line.startswith("    ") or line.startswith("\t")


def _protect_indented_blocks(content: str, protected) -> str:
    """들여쓴 코드 블록을 전역 공백 정규화에서 제외합니다."""
    lines = content.splitlines(keepends=True)
    output = []
    index = 0
    while index < len(lines):
        if not _is_indented_code_line(lines[index]):
            output.append(lines[index])
            index += 1
            continue

        end = index + 1
        while end < len(lines):
            raw_line = lines[end].rstrip("\r\n")
            if _is_indented_code_line(raw_line) or not raw_line.strip():
                end += 1
                continue
            break
        output.append(_replace_protected_block("".join(lines[index:end]), protected))
        index = end
    return "".join(output)


def _protect_non_markdown_blocks(content: str):
    """코드·주석 블록을 보호하고 복원용 토큰 표를 반환합니다."""
    protected = {}
    content = _protect_fenced_blocks(content, protected)
    content = _protect_indented_blocks(content, protected)
    content = _protect_html_comments(content, protected)
    return content, protected


def _is_protected_line(stripped: str) -> bool:
    return bool(PROTECTED_TOKEN_RE.fullmatch(stripped))


def _is_markdown_structure_line(line: str) -> bool:
    """문단으로 합치면 안 되는 Markdown 블록 라인인지 판정합니다."""
    stripped = line.strip()
    if not stripped:
        return False
    if _is_protected_line(stripped) or PAGE_MARKER_RE.match(stripped):
        return True
    if re.match(r'^\s{0,3}#{1,6}(?:\s|$)', line):
        return True
    if re.match(r'^\s*>', line):
        return True
    if TABLE_ROW_RE.match(line) or LIST_ITEM_RE.match(line):
        return True
    return bool(HORIZONTAL_RULE_RE.match(line))


def _restore_protected_blocks(content: str, protected) -> str:
    for token, block in protected.items():
        content = content.replace(token, block)
    return content


def _is_abbrev_tail(stripped: str) -> bool:
    """줄이 약어/이니셜로 끝나 문장이 미완결인지 판정.

    - 마지막 토큰이 ABBREVIATIONS 에 속함 (vgl. z.B. Hrsg. 등)
    - 저자 이니셜 패턴으로 끝남 (`R.`, `R.F.`, `J.-P.`)
    """
    if not stripped.endswith('.'):
        return False
    # 저자 이니셜: 끝이 단일 대문자 + 마침표 (옵션 반복)
    if re.search(r'(?:\b[A-ZÄÖÜ]\.){1,4}$', stripped):
        return True
    last = stripped.split()[-1] if stripped.split() else ''
    return last.rstrip('.') in {a.rstrip('.') for a in ABBREVIATIONS}


def clean_markdown(file_path, output_path=None):
    """
    opendataloader 추출 결과의 마크다운을 신학 논문 규격에 맞게 정제합니다.
    
    기능:
    - OCR 노이즈 제거 (하이픈 잘림, 특수문자 오염)
    - Spalte(단 번호) 패턴 탐지 및 강조 표시
    - Literatur(참고문헌) 구역 구조화
    - 문단 결합 (번역 파이프라인 품질 최적화)
    - 공백 정규화

    Args:
        file_path (str): 정제할 .md 파일 경로
        output_path (str, optional): 출력 경로. None이면 _cleaned 접미어 사용
    
    Returns:
        str: 정제된 파일 경로
    """
    print(f"[*] 마크다운 정제 중: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 코드·HTML 주석은 하이프네이션과 공백 정규화의 대상이 아니다.
    content, protected_blocks = _protect_non_markdown_blocks(content)

    # 1. 하이픈/OCR 노이즈로 잘린 단어 복원
    # 1-a. 줄바꿈 하이프네이션: 라틴 문자 사이에서, 다음 줄이 소문자로
    #      이어질 때만 결합(유럽어 어절 분철). 대문자로 이어지면 고유
    #      합성어 하이픈일 수 있어 보존. 한글/숫자는 건드리지 않음.
    content = re.sub(
        r'([A-Za-zÀ-ÖØ-öø-ÿ]{2,})-\s*\n\s*([a-zà-öø-ÿ]+)',
        r'\1\2', content,
    )
    # 1-b. 단어 내부 물결표(~) OCR 노이즈 제거 — 라틴 문자 사이만.
    #      한국어 가운뎃점(·)은 정상 구분자(예: 북·동·서·남, 저자 나열)
    #      이므로 제거하지 않는다.
    content = re.sub(r'([A-Za-z])~([A-Za-z])', r'\1\2', content)

    # 2. Spalte(단 번호) 패턴 탐지 및 강조 (독일어 신학 사전 Sp. 표기)
    content = re.sub(r'(?:\[| )?Sp\.?\s*(\d+)(?:\]| )?', r'\n\n> [Sp. \1]\n\n', content)

    # 3. Literatur(참고문헌) 구역 구조화
    lines = content.split('\n')
    new_lines = []
    in_literatur = False
    for line in lines:
        if 'Literatur' in line and (line.startswith('###') or line.startswith('######')):
            in_literatur = True
            new_lines.append(f"\n{line}\n")
            continue
        if in_literatur:
            # 다음 헤딩이 나오면 Literatur 구역 종료
            if line.startswith('#'):
                in_literatur = False
                new_lines.append(line)
            elif line.strip():
                # 표·목록·코드·주석은 Literatur 안에서도 Markdown 구조를 보존한다.
                if _is_markdown_structure_line(line):
                    new_lines.append(line)
                else:
                    new_lines.append(f"> {line}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    content = '\n'.join(new_lines)

    # 4. 문단 결합 (번역 품질 최적화: 한 문단이 여러 줄에 걸쳐 있는 경우 병합)
    lines = content.split('\n')
    processed_lines = []
    temp_line = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if temp_line:
                processed_lines.append(temp_line)
                temp_line = ""
            processed_lines.append("")
            continue
        # 인용문, 헤딩, 페이지 마커는 그대로 유지
        if _is_markdown_structure_line(line):
            if temp_line:
                processed_lines.append(temp_line)
                temp_line = ""
            processed_lines.append(line)
            continue
        # 문장 병합
        normalized_line = re.sub(r' +', ' ', stripped)
        if temp_line:
            temp_line = temp_line + " " + normalized_line
        else:
            temp_line = normalized_line
        # 문장 종결 부호에서 flush — 단, 약어·이니셜로 끝나면 계속 누적
        # (vgl. / z.B. / Hrsg. / "R.F." 등에서 문장이 잘리는 것 방지)
        if normalized_line.endswith(('.', '!', '?', ':', ';', '"', ')')) \
                and not _is_abbrev_tail(normalized_line):
            processed_lines.append(temp_line)
            temp_line = ""
    if temp_line:
        processed_lines.append(temp_line)
    content = '\n'.join(processed_lines)

    # 5. 공백 정규화 — 일반 텍스트는 위에서 처리했고, 구조 블록은 보존한다.
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = _restore_protected_blocks(content, protected_blocks)

    # 출력 경로 결정
    if output_path is None:
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_cleaned{ext}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[+] 정제 완료 → {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python post_cleaner.py <md_파일_경로> [출력_경로]")
        sys.exit(1)
    target_md = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    if os.path.exists(target_md):
        clean_markdown(target_md, output_path=out_path)
    else:
        print(f"❌ 파일 없음: {target_md}")
        sys.exit(1)
