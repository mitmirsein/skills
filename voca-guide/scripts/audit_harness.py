#!/usr/bin/env python3
import json
import os
import re
import sys

# 품질 감사 기준 상수 정의
MAX_LOGIC_DESC_LEN = 150
MAX_REAL_TIP_LEN = 200
MAX_SENTENCE_LEN = 100
MAX_QUESTION_LEN = 100

# 금지어 패턴 (정규식 객체 리스트)
FORBIDDEN_KEYWORDS = [
    re.compile(r"\bminkyoo_cho\b", re.IGNORECASE),
    re.compile(r"\bminkyoo\b", re.IGNORECASE),
    re.compile(r"\bcho\b", re.IGNORECASE),
    re.compile(r"조민규"),
    re.compile(r"대치동"),
    re.compile(r"개별맞춤")
]

# 딱딱한 격식체 종결어미 패턴 (설명문용)
# 입니다, 했습니다, 합니다, 됩니다, 습니다, 예요, 에요 등
FORMAL_TONE_PATTERNS = [
    r"입니다\b", r"했습니다\b", r"합니다\b", r"됩니다\b", r"습니다\b",
    r"입니다\.", r"했습니다\.", r"합니다\.", r"됩니다\.", r"습니다\.",
    r"입니다\s", r"했습니다\s", r"합니다\s", r"됩니다\s", r"습니다\s"
]

# 어원 접두사 표기 규격 패턴
# L., Gk., OE. 등 약어 명시 여부
ETYMOLOGY_LANG_PATTERN = re.compile(r"\b(L\.|Gk\.|OE\.|OF\.|PGmc\.)")


def audit_vocab_data(json_path):
    if not os.path.exists(json_path):
        print(f"[ERROR] 파일이 존재하지 않습니다: {json_path}")
        return False, {"errors": [f"파일 없음: {json_path}"], "warnings": []}

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 디코딩 실패: {e}")
        return False, {"errors": [f"JSON 파싱 에러: {e}"], "warnings": []}

    if not isinstance(data, list):
        return False, {"errors": ["데이터의 최상위 노드는 반드시 리스트 형식이어야 합니다."], "warnings": []}

    errors = []
    warnings = []
    
    print(f"\n===== Voca Guide 품질 감사 시작 (대상 어휘 수: {len(data)}) =====")

    for idx, item in enumerate(data):
        word = item.get("word", f"Unknown_Word_{idx}")
        prefix = f"[{word}]"

        # ----------------------------------------------------
        # 1. Schema & Completeness (정합성 검사)
        # ----------------------------------------------------
        required_fields = [
            "word", "pronunciation", "meaning1", "meaning2", "intro",
            "etymology", "examples1", "transition_question", "logic_flow",
            "logic_desc", "examples2", "feeling", "real_tip", "summary_flow", "quiz"
        ]
        
        for field in required_fields:
            if field not in item:
                errors.append(f"{prefix} 필수 필드 '{field}'가 누락되었습니다.")
                continue

        # etymology 하위 구조 검사
        etym = item.get("etymology", {})
        if isinstance(etym, dict):
            if "root1" not in etym or "root2" not in etym or "flow" not in etym:
                errors.append(f"{prefix} 'etymology' 필드 하위에 'root1', 'root2', 'flow'가 모두 존재해야 합니다.")
        else:
            errors.append(f"{prefix} 'etymology' 필드는 dict 타입이어야 합니다.")

        # examples1, examples2 구조 검사
        for ex_field in ["examples1", "examples2"]:
            ex_list = item.get(ex_field, [])
            if not isinstance(ex_list, list) or len(ex_list) != 2:
                errors.append(f"{prefix} '{ex_field}'는 반드시 원소 2개를 가진 리스트여야 합니다.")
            else:
                for ex_idx, ex in enumerate(ex_list):
                    if not isinstance(ex, dict) or "en" not in ex or "ko" not in ex:
                        errors.append(f"{prefix} '{ex_field}'의 {ex_idx+1}번째 원소에 'en' 혹은 'ko' 키가 누락되었습니다.")

        # quiz 구조 검사
        quiz_list = item.get("quiz", [])
        if not isinstance(quiz_list, list) or len(quiz_list) != 2:
            errors.append(f"{prefix} 'quiz'는 반드시 원소 2개를 가진 리스트여야 합니다.")
        else:
            for q_idx, q in enumerate(quiz_list):
                if not isinstance(q, dict) or "question" not in q or "translation" not in q or "answer" not in q:
                    errors.append(f"{prefix} 'quiz'의 {q_idx+1}번째 문항에 'question', 'translation', 'answer' 중 누락된 키가 있습니다.")

        # ----------------------------------------------------
        # 2. Pedagogical Style & Tone (학습 친화성 및 문체)
        # ----------------------------------------------------
        # 한글 설명 필드에서 격식체 검사 (intro, logic_desc, feeling, real_tip)
        checked_korean_fields = {
            "intro": item.get("intro", ""),
            "logic_desc": item.get("logic_desc", ""),
            "feeling": item.get("feeling", ""),
            "real_tip": item.get("real_tip", "")
        }

        for f_name, f_val in checked_korean_fields.items():
            if not isinstance(f_val, str):
                continue
            for pattern in FORMAL_TONE_PATTERNS:
                if re.search(pattern, f_val):
                    warnings.append(
                        f"{prefix} 설명문 '{f_name}'에서 격식체 단어(종결어미)가 발견되었습니다: \"{f_val}\". "
                        f"학생 친화적인 구어체 반말(~이지, ~했어, ~잖아 등)로 수정하십시오."
                    )
                    break

        # 어원 접두사 표기 검사 (접사는 예외로 처리)
        if isinstance(etym, dict):
            for root_key in ["root1", "root2"]:
                root_val = etym.get(root_key, "")
                is_suffix = root_val and ("suffix" in root_val.lower() or "접사" in root_val or "접미사" in root_val or root_val.strip().startswith("-") or "plural" in root_val.lower() or "명사" in root_val or "형용사" in root_val or "동사" in root_val)
                if root_val and not is_suffix and not ETYMOLOGY_LANG_PATTERN.search(root_val):
                    warnings.append(
                        f"{prefix} 어원 '{root_key}'에 라틴어(L.), 그리스어(Gk.), 고대영어(OE.) 등의 언어 기호가 명시되지 않았습니다: \"{root_val}\"."
                    )

        # 퀴즈 정답 검합성 검사 (answer가 word의 기본형 혹은 일부 변형인지)
        base_word = item.get("word", "").lower()
        for q_idx, q in enumerate(quiz_list):
            if not isinstance(q, dict):
                continue
            ans = q.get("answer", "").lower()
            if not ans:
                continue
            
            # answer가 word와 정확히 일치하거나, word의 처음 몇 글자가 일치하는지 러프하게 확인
            # (예: compromise -> compromised / incident -> incidents)
            match_len = min(len(base_word), 5)
            if not (base_word in ans or ans[:match_len] == base_word[:match_len]):
                warnings.append(
                    f"{prefix} {q_idx+1}번째 퀴즈의 정답 '{ans}'이 표제어 '{base_word}'와 일치하지 않거나 관련 없는 단어일 가능성이 높습니다."
                )

        # ----------------------------------------------------
        # 3. Privacy & Security (개인정보 및 보안)
        # ----------------------------------------------------
        full_text = json.dumps(item, ensure_ascii=False).lower()
        for forbidden in FORBIDDEN_KEYWORDS:
            if forbidden.search(full_text):
                errors.append(f"{prefix} 금지된 개인정보 또는 학원명 키워드가 발견되었습니다: '{forbidden.pattern}'")

        # ----------------------------------------------------
        # 4. Layout & Overflow Guard (레이아웃 오버플로우 방지)
        # ----------------------------------------------------
        logic_desc = item.get("logic_desc", "")
        if isinstance(logic_desc, str) and len(logic_desc) > MAX_LOGIC_DESC_LEN:
            warnings.append(
                f"{prefix} 'logic_desc' 글자 수가 {len(logic_desc)}자입니다. "
                f"최대 글자 수 {MAX_LOGIC_DESC_LEN}자를 초과하여 A4 오버플로우 위험이 있습니다."
            )

        real_tip = item.get("real_tip", "")
        if isinstance(real_tip, str) and len(real_tip) > MAX_REAL_TIP_LEN:
            warnings.append(
                f"{prefix} 'real_tip' 글자 수가 {len(real_tip)}자입니다. "
                f"최대 글자 수 {MAX_REAL_TIP_LEN}자를 초과하여 A4 오버플로우 위험이 있습니다."
            )

        intro = item.get("intro", "")
        if isinstance(intro, str) and len(intro) > MAX_QUESTION_LEN:
            warnings.append(f"{prefix} 'intro' 글자 수가 {len(intro)}자입니다. {MAX_QUESTION_LEN}자 이하 권장.")

        trans_q = item.get("transition_question", "")
        if isinstance(trans_q, str) and len(trans_q) > MAX_QUESTION_LEN:
            warnings.append(f"{prefix} 'transition_question' 글자 수가 {len(trans_q)}자입니다. {MAX_QUESTION_LEN}자 이하 권장.")

        # 예문 길이 검사
        for ex_field in ["examples1", "examples2"]:
            ex_list = item.get(ex_field, [])
            if not isinstance(ex_list, list):
                continue
            for ex_idx, ex in enumerate(ex_list):
                if not isinstance(ex, dict):
                    continue
                en_len = len(ex.get("en", ""))
                ko_len = len(ex.get("ko", ""))
                if en_len > MAX_SENTENCE_LEN:
                    warnings.append(f"{prefix} '{ex_field}' {ex_idx+1}번째 영문 예문이 {en_len}자로 너무 깁니다. {MAX_SENTENCE_LEN}자 이하 권장.")
                if ko_len > MAX_SENTENCE_LEN:
                    warnings.append(f"{prefix} '{ex_field}' {ex_idx+1}번째 국문 번역이 {ko_len}자로 너무 깁니다. {MAX_SENTENCE_LEN}자 이하 권장.")

    print(f"품질 감사 완료: 에러 {len(errors)}개, 경고 {len(warnings)}개 검출")
    print("========================================================\n")

    # 콘솔 상세 리포팅
    if errors:
        print("❌ [CRITICAL ERRORS]")
        for err in errors:
            print(f"  - {err}")
        print()
        
    if warnings:
        print("⚠️ [WARNINGS]")
        for warn in warnings:
            print(f"  - {warn}")
        print()

    base_name = os.path.splitext(os.path.basename(json_path))[0]
    report_path = os.path.join(os.path.dirname(json_path), f"{base_name}_audit_report.txt")
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(f"=== Voca Guide Quality Audit Report ===\n")
        rf.write(f"Target file: {json_path}\n")
        rf.write(f"Total words: {len(data)}\n")
        rf.write(f"Errors: {len(errors)}, Warnings: {len(warnings)}\n\n")
        
        if errors:
            rf.write("--- CRITICAL ERRORS ---\n")
            for err in errors:
                rf.write(f"x {err}\n")
            rf.write("\n")
            
        if warnings:
            rf.write("--- WARNINGS ---\n")
            for warn in warnings:
                rf.write(f"! {warn}\n")
            rf.write("\n")
            
    print(f"상세 감사 진단서가 저장되었습니다: {report_path}")

    # 크리티컬 에러가 없으면 합격으로 판정 (경고는 빌드를 중단하진 않음)
    is_success = len(errors) == 0
    return is_success, {"errors": errors, "warnings": warnings}


if __name__ == "__main__":
    target = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/vocab_data.json")
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    success, _ = audit_vocab_data(target)
    sys.exit(0 if success else 1)
