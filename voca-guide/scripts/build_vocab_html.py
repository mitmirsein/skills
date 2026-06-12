import json
import os
import asyncio
from playwright.async_api import async_playwright

latin_etymologies = {
    "enormously": {
        "root1": "e- (L. ex- : out of / 벗어남)",
        "root2": "norm (L. norma : rule, standard / 규격, 기준)",
        "flow": "기준(규격)을 벗어남 &rarr; 일반적인 한계를 초과함 &rarr; 물리적으로 거대하게 &rarr; 추상적으로 엄청나게"
    },
    "episode": {
        "root1": "epi- (Gk. epi- : in addition / 곁에, 덧붙여)",
        "root2": "sode (Gk. eis-hodos : entry, way / 들어오는 길)",
        "flow": "본 길 옆으로 들어오는 곁길 &rarr; 연극 중 덧붙여진 짧은 이야기 &rarr; 방송의 독립된 회차"
    },
    "subscribers": {
        "root1": "sub- (L. sub- : under / 아래에)",
        "root2": "scribe (L. scribere : write / 적다, 쓰다)",
        "flow": "계약서 아래에 이름을 적다 &rarr; 정기 후원/대금 지불 동의 &rarr; 유튜브/매체 정기구독자"
    },
    "concept": {
        "root1": "con- (L. com- : together / 함께, 완전히)",
        "root2": "cept (L. capere : take, hold / 취하다, 쥐다)",
        "flow": "생각들을 완전히 모아 쥐다 &rarr; 기본 구상 설계 초안 &rarr; 정의된 학술 개념"
    },
    "originally": {
        "root1": "origin (L. oriri : to rise, begin / 솟아나다, 시작점)",
        "root2": "-ally (Suffix : 부사 접사)",
        "flow": "가장 처음의 기원에서 시작하여 &rarr; 원래, 본래 &rarr; 기원 그대로의 독자성 &rarr; 독창적으로"
    },
    "creativity": {
        "root1": "cre- (L. creare : to make, grow / 창조하다, 자라나게 하다)",
        "root2": "-tivity (Suffix : 성질, 능력을 뜻하는 명사 접사)",
        "flow": "무에서 유를 자라나게 하는 성질 &rarr; 머릿속의 창의력 &rarr; 구체화된 예술적 창작성"
    },
    "cleansing": {
        "root1": "clean (OE. clænsian : to clear / 깨끗하게 씻어내다)",
        "root2": "-sing (Suffix : 행동 명사 접사)",
        "flow": "더러운 것을 닦아 깨끗하게 함 &rarr; 얼굴 피부 세안 &rarr; 마음과 두뇌의 찌꺼기 정화"
    },
    "private": {
        "root1": "priv- (L. privare : to deprive, separate / 박탈하다, 분리하다)",
        "root2": "-ate (Suffix : 형용사/명사 접사)",
        "flow": "공공 영역에서 분리되어 단독으로 있다 &rarr; 사적인, 비공개의 &rarr; 직책 없는 사병 &rarr; 이등병"
    },
    "honestly": {
        "root1": "honest (L. honestus < honor : honorable / 명예로운, 고결한)",
        "root2": "-ly (Suffix : 부사 접사)",
        "flow": "명예를 지키며 떳떳하게 행동하여 &rarr; 솔직하게 &rarr; 진심을 담은 강조 &rarr; 정말로, 참으로"
    },
    "complaints": {
        "root1": "com- (L. com- : intensive / 강하게)",
        "root2": "plaint (L. plangere : to beat the breast / 가슴을 치며 슬퍼하다)",
        "flow": "가슴을 치며 고통을 하소연하다 &rarr; 고객 민원/불평 &rarr; 아파서 지르는 비명 &rarr; 통증, 질환"
    },
    "productive": {
        "root1": "pro- (L. pro- : forward / 앞으로)",
        "root2": "duct (L. ducere : to lead, pull / 이끌다, 당기다)",
        "flow": "결과를 앞으로 이끌어 내다 &rarr; 효율성 높은 생산적인 &rarr; 쉼 없이 작품을 생산하는 &rarr; 다작하는"
    },
    "random": {
        "root1": "rand (OF. randon : force, speed / 질주, 강한 힘)",
        "root2": "-dom (Suffix : 상태 접사)",
        "flow": "고삐 풀린 말이 제멋대로 내달림 &rarr; 규칙 없는 마구잡이의 &rarr; 맥락 없는 뜬금없는 &rarr; 엉뚱한"
    },
    "assignment": {
        "root1": "ad- (L. ad- : to / ~에게)",
        "root2": "sign (L. signare : to mark / 표시하다, 서명하다)",
        "flow": "지정해서 특정인에게 넘겨주다 &rarr; 부과된 임무/과제 &rarr; 몫을 지정하여 나누어 줌 &rarr; 배정, 양도"
    },
    "normally": {
        "root1": "norm (L. norma : rule, standard / 규칙, 기준)",
        "root2": "-ally (Suffix : 부사 접사)",
        "flow": "기준과 규칙에 맞추어 &rarr; 정상적으로 작동하여 &rarr; 일반적인 척도에 따라 &rarr; 보통, 대개"
    },
    "purpose": {
        "root1": "pro- (L. pro- : forward / 앞에)",
        "root2": "pose (L. ponere : to place, put / 두다, 놓다)",
        "flow": "내 눈앞에 표적을 가져다 놓다 &rarr; 달성할 의도/목적 &rarr; 목적을 향한 흔들림 없는 태도 &rarr; 결단력, 의지"
    },
    "relate to": {
        "root1": "re- (L. re- : back, again / 다시)",
        "root2": "late (L. latus < ferre : to carry, bring / 가져오다)",
        "flow": "두 대상을 다시 가져와 엮다 &rarr; ~와 관련되다 &rarr; 상대 상황을 내 궤도에 대입 &rarr; 공감하다"
    },
    "concentrate": {
        "root1": "con- (L. com- : together / 함께, 한곳에)",
        "root2": "center (L. centrum < Gk. kentron : center / 중심점)",
        "flow": "모든 요소를 한 중심에 모아 두다 &rarr; 주의를 모으다(집중하다) &rarr; 성분을 중심에 조밀하게 뭉침 &rarr; 농축하다"
    },
    "emotional": {
        "root1": "e- (L. ex- : out / 밖으로)",
        "root2": "mot (L. movere : to move / 움직이다)",
        "flow": "마음의 움직임이 밖으로 뿜어져 나옴 &rarr; 감정적인 &rarr; 마음이 세게 흔들려 울컥함 &rarr; 격해진, 감동한"
    },
    "tension": {
        "root1": "tens (L. tendere : to stretch / 잡아당기다, 팽팽하게 하다)",
        "root2": "-ion (Suffix : 명사 접사)",
        "flow": "양쪽에서 팽팽하게 잡아당김 &rarr; 물리적 장력 &rarr; 마음이 팽팽히 조여 드는 상태 &rarr; 긴장, 갈등"
    },
    "performance": {
        "root1": "per- (L. per- : thoroughly / 완전히, 끝까지)",
        "root2": "form (L. formare : to shape, do / 형성하다, 수행하다)",
        "flow": "설계된 모양대로 끝까지 완수하다 &rarr; 기계의 성능/작동 &rarr; 관객 앞에서 임무를 해내다 &rarr; 공연, 연주"
    },
    "vague": {
        "root1": "vague (L. vagus : wandering, aimless / 방랑하는, 정처 없는)",
        "root2": "-ue (Suffix : 형용사 접사)",
        "flow": "방향을 잡지 못하고 이리저리 헤맴 &rarr; 형태가 흐릿하고 모호한 &rarr; 생각이나 어조가 얼버무리는 &rarr; 애매한"
    },
    "drive": {
        "root1": "drive (OE. drīfan : to push, drive / 몰다, 밀어붙이다)",
        "root2": "verb (동사/명사 공통)",
        "flow": "가축이나 차를 앞으로 세게 몰다 &rarr; 운전하다/구동하다 &rarr; 목표를 향해 강하게 밀어붙임 &rarr; 충동, 추진력"
    },
    "achieve": {
        "root1": "a- (L. ad- : to / ~에게)",
        "root2": "chieve (L. caput : head / 우두머리, 머리, 정상)",
        "flow": "산의 정상 꼭대기에 도달하다 &rarr; 목표에 도달하여 완수하다 &rarr; 성취하다, 업적을 남기다"
    },
    "ultimate": {
        "root1": "ultim (L. ultimus : farthest, last / 가장 먼, 마지막의)",
        "root2": "-ate (Suffix : 형용사 접사)",
        "flow": "가장 끝자락 극단까지 가 닿은 &rarr; 궁극적인, 최종의 &rarr; 근본을 건드리는 가장 단순한 &rarr; 극한의"
    },
    "repetition": {
        "root1": "re- (L. re- : again / 다시)",
        "root2": "petit (L. petere : to seek, aim at / 추구하다, 달려가다)",
        "flow": "원하는 목표를 향해 다시 달리기 &rarr; 반복 &rarr; 똑같은 행동을 되풀이하여 구사함 &rarr; 되풀이, 재연"
    },
    "specific": {
        "root1": "speci (L. species : appearance, kind / 외형, 종류)",
        "root2": "fic (L. facere : to make / 만들다, 하다)",
        "flow": "어떤 종류의 외형적 특징을 명확히 함 &rarr; 구체적인 &rarr; 약재가 특정 부위에 효능을 보임 &rarr; 특효가 있는"
    },
    "meditate": {
        "root1": "med (L. meditari : to measure, ponder / 치수를 가만히 재어보다)",
        "root2": "-ate (Suffix : 동사 접사)",
        "flow": "마음속 자로 가만히 모양을 재어 봄 &rarr; 성찰을 위한 명상하다 &rarr; 음모나 기획을 깊이 저울질함 &rarr; 계획하다, 꾀하다"
    },
    "combine": {
        "root1": "com- (L. com- : together / 함께)",
        "root2": "bin (L. bini : two by two / 둘씩, 쌍으로)",
        "flow": "흩어진 둘을 하나로 함께 묶다 &rarr; 결합하다 &rarr; 베기와 탈곡 두 작업을 합쳐서 하는 기계 &rarr; 농기계 콤바인"
    },
    "cue": {
        "root1": "cue (L. cauda : tail / 동물의 꼬리)",
        "root2": "Q-sign (L. quando : when / 연극 시작 타이밍 알림)",
        "flow": "대본 끝자락에 달아둔 꼬리표 신호 &rarr; 연극 시작 신호, 단서 &rarr; 동물의 꼬리처럼 긴 나무 &rarr; 당구 큐대"
    },
    "attractive": {
        "root1": "ad- (L. ad- : toward / ~쪽으로)",
        "root2": "tract (L. trahere : to pull, drag / 끌어당기다)",
        "flow": "힘을 주어 자기 중심 쪽으로 끌어당김 &rarr; 자석의 인력을 지닌 &rarr; 상대의 마음과 눈길을 착 잡아당김 &rarr; 매력적인"
    },
    "useful": {
        "root1": "use (L. uti : to use / 사용하다, 부리다)",
        "root2": "-ful (Suffix : full of / 가득 찬)",
        "flow": "쓸모가 있는 성질로 가득 차다 &rarr; 도구의 유용한 &rarr; 팀원으로서 쓸모가 많아 기특한 &rarr; 유능한, 도움 되는"
    },
    "host": {
        "root1": "hostis (L. hostis : stranger, enemy / 이방인, 적군)",
        "root2": "hospes (L. hospes : guest-host / 손님을 맞는 주인)",
        "flow": "손님을 집으로 환대하는 주인 &rarr; 사회자 &rarr; 떼를 지어 쳐들어온 적군의 무리 &rarr; 천사 군대 &rarr; 수많은 무리/다수"
    },
    "overcome": {
        "root1": "over (OE. ofer : above, across / 장벽의 위를 넘어)",
        "root2": "come (OE. cuman : to arrive / 도달하다)",
        "flow": "내 앞의 장벽 위를 훌쩍 넘어 밟음 &rarr; 극복하다 &rarr; 슬픔의 파도가 내 머리 위로 쏟아져 덮침 &rarr; 압도당하다"
    },
    "correctly": {
        "root1": "con- (L. com- : completely / 완전히)",
        "root2": "rect (L. regere < rectus : to make straight / 똑바로 세우다)",
        "flow": "굽은 곳 없이 완전히 똑바로 세움 &rarr; 수학적 올바르게 &rarr; 규범의 직선에 서서 곧게 행동함 &rarr; 예의 바르게"
    },
    "exploring": {
        "root1": "ex- (L. ex- : out / 밖으로)",
        "root2": "plor (L. plorare : to cry out, weep / 외치다, 울부짖다)",
        "flow": "소리를 질러 덤불 속 짐승을 몰아냄 &rarr; 미지의 정글 수색(탐험) &rarr; 상처 속을 도구로 찔러 조사함 &rarr; 진찰/진단"
    },
    "sticks": {
        "root1": "stick (OE. sticca : rod, pin / 뾰족한 나무 막대)",
        "root2": "stick (OE. stician : to pierce / 콕 찔러 고정하다)",
        "flow": "뾰족한 나무 꼬챙이 &rarr; 핀으로 찔러 벽에 박아 고정하다 &rarr; 접착제처럼 착 달라붙다 &rarr; 루틴이 뇌에 몸에 뱀"
    },
    "progress": {
        "root1": "pro- (L. pro- : forward / 앞으로)",
        "root2": "gress (L. gradi : to walk, step / 걷다, 걸음 내딛다)",
        "flow": "시선을 앞을 향해 두고 한 발짝 걷기 &rarr; 물리적 전진 &rarr; 멈추지 않는 일의 진행 &rarr; 어제보다 더 나은 발전"
    },
    "achievement": {
        "root1": "a- (L. ad- : to / ~에게)",
        "root2": "chef (L. caput : head, top / 우두머리, 머리, 정상)",
        "flow": "오랜 등반 끝에 산의 꼭대기에 다다름 &rarr; 이룩해낸 성취/업적 &rarr; 정상에서 땀 닦을 때 샘솟는 뿌듯함 &rarr; 성취감"
    },
    "flexible": {
        "root1": "flex (L. flectere : to bend / 구부리다, 꺾다)",
        "root2": "-ible (Suffix : able to be / ~할 수 있는)",
        "flow": "힘을 주어도 뚝 부러지지 않고 휘어짐 &rarr; 유연한 &rarr; 상황에 맞춰 내 고집이나 계획을 구부림 &rarr; 융통성 있는"
    },
    "left": {
        "root1": "left (OE. lyft : weak / 약한 쪽, 왼쪽)",
        "root2": "leave (OE. læfan : to depart / 떠나다, 남겨두다)",
        "flow": "약하고 무력한 손인 왼쪽 &rarr; 하던 작업에서 완전히 손 떼고 분리됨(leave off) &rarr; 공부를 중단한/멈춘 지점"
    }
}

def build_html():
    json_path = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/vocab_data.json")
    html_path = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/Lesson4_Vocabulary_CardNews_40.html")
    
    with open(json_path, "r", encoding="utf-8") as f:
        vocab_list = json.load(f)
        
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>수능·내신 고득점 단어 카드뉴스 교재</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Gmarket+Sans:wght@300;500;700&family=Inter:wght@300;400;600;700;800&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        @page {
            size: A4;
            margin: 0;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #f7f6f3;
            color: #1e293b;
            font-family: 'Inter', 'Noto Sans KR', sans-serif;
            -webkit-print-color-adjust: exact;
        }
        .page {
            width: 210mm;
            height: 297mm;
            padding: 10mm 12mm;
            position: relative;
            page-break-after: always;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: radial-gradient(circle at 50% 30%, #fdfdfd 0%, #f4f2ee 100%);
            overflow: hidden;
        }
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid rgba(2, 132, 199, 0.15);
            padding-bottom: 6px;
            margin-bottom: 8px;
        }
        .page-header .brand {
            font-family: 'Gmarket Sans', sans-serif;
            font-weight: 700;
            font-size: 13px;
            color: #0284c7;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .page-header .brand span {
            background: linear-gradient(90deg, #0284c7, #4f46e5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .page-header .brand-sub {
            font-size: 10px;
            color: #64748b;
            font-weight: 500;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: 68px repeat(4, 1fr);
            gap: 8px;
            flex-grow: 1;
            height: calc(100% - 45px);
        }
        .card {
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(0, 0, 0, 0.06);
            border-radius: 10px;
            padding: 8px 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(148, 163, 184, 0.12);
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2.5px;
            background: linear-gradient(90deg, #0284c7, #4f46e5);
        }
        /* 카드 종류별 테두리 및 색상 강조 */
        .card-q {
            border: 1px solid rgba(245, 158, 11, 0.3);
            background: rgba(245, 158, 11, 0.04);
        }
        .card-q::before {
            background: linear-gradient(90deg, #f59e0b, #d97706);
        }
        .card-word {
            border: 1px solid rgba(2, 132, 199, 0.3);
            background: rgba(2, 132, 199, 0.04);
        }
        .card-word::before {
            background: linear-gradient(90deg, #0284c7, #4f46e5);
        }
        .card-quiz {
            border: 1px solid rgba(219, 39, 119, 0.3);
            background: rgba(219, 39, 119, 0.03);
        }
        .card-quiz::before {
            background: linear-gradient(90deg, #db2777, #7c3aed);
        }
        /* 인스타 포스트 헤더 */
        .insta-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            padding-bottom: 4px;
            margin-bottom: 4px;
            height: 20px;
        }
        .insta-profile {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .profile-pic {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
            padding: 1px;
        }
        .profile-pic-inner {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 6px;
            color: #e1306c;
            font-weight: bold;
        }
        .profile-info {
            display: flex;
            flex-direction: column;
            line-height: 1;
        }
        .profile-username {
            font-size: 8px;
            font-weight: 700;
            color: #0f172a;
        }
        .profile-subtext {
            font-size: 6.5px;
            color: #64748b;
        }
        .insta-badge {
            font-size: 7.5px;
            font-weight: 700;
            color: #475569;
            background: rgba(0, 0, 0, 0.05);
            padding: 1px 5px;
            border-radius: 10px;
        }
        .card-body {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 2px 0;
        }
        /* 콘텐츠 레이아웃 스타일 */
        .q-text {
            font-size: 11px;
            font-weight: 700;
            color: #b45309;
            line-height: 1.35;
        }
        .intro-text {
            font-size: 10px;
            color: #475569;
            line-height: 1.4;
            font-style: italic;
        }
        .word-title {
            font-family: 'Gmarket Sans', sans-serif;
            font-weight: 700;
            font-size: 18px;
            color: #0284c7;
            text-align: center;
            letter-spacing: -0.02em;
        }
        .word-pron {
            font-size: 9px;
            color: #64748b;
            text-align: center;
            margin-bottom: 4px;
        }
        .word-meanings {
            font-size: 9.5px;
            color: #334155;
            display: flex;
            flex-direction: column;
            gap: 2px;
            padding-left: 4px;
        }
        .word-meanings div {
            display: flex;
            gap: 4px;
        }
        .mean-num {
            color: #0284c7;
            font-weight: bold;
        }
        .etym-box {
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .etym-item {
            font-size: 8.5px;
            background: rgba(0, 0, 0, 0.02);
            padding: 2px 5px;
            border-radius: 4px;
            border-left: 2px solid #4f46e5;
            color: #1e293b;
        }
        .etym-flow {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 3px;
            margin-top: 2px;
            font-size: 8px;
            color: #64748b;
        }
        .etym-flow-step {
            background: rgba(79, 70, 229, 0.06);
            padding: 1px 4px;
            border-radius: 3px;
            color: #4f46e5;
            font-weight: 500;
        }
        .example-list {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .example-item {
            border-left: 2px solid #0284c7;
            padding-left: 5px;
            line-height: 1.3;
        }
        .example-item-ko {
            border-left: 2px solid #059669;
            padding-left: 5px;
            line-height: 1.3;
        }
        .ex-en {
            font-size: 9.5px;
            font-weight: 600;
            color: #1e293b;
        }
        .ex-ko {
            font-size: 8.5px;
            color: #64748b;
        }
        .trans-question {
            font-size: 11px;
            font-weight: 700;
            color: #e11d48;
            text-align: center;
            line-height: 1.4;
        }
        .logic-flow-box {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
            gap: 2px;
            margin-bottom: 4px;
        }
        .logic-step {
            font-size: 8.5px;
            background: rgba(0, 0, 0, 0.03);
            padding: 2px 4px;
            border-radius: 4px;
            color: #334155;
            font-weight: 500;
        }
        .logic-arrow {
            font-size: 8px;
            color: #64748b;
        }
        .logic-desc {
            font-size: 9px;
            color: #475569;
            line-height: 1.35;
            text-align: center;
            background: rgba(2, 132, 199, 0.05);
            padding: 3px;
            border-radius: 4px;
        }
        .meaning2-title {
            font-size: 9px;
            color: #db2777;
            font-weight: bold;
            margin-bottom: 2px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .meaning2-box {
            font-size: 12px;
            font-weight: 700;
            color: #db2777;
            text-align: center;
            background: rgba(219, 39, 119, 0.06);
            padding: 6px;
            border-radius: 6px;
            border: 1px dashed rgba(219, 39, 119, 0.25);
        }
        .feeling-box {
            background: rgba(5, 150, 105, 0.06);
            border-left: 3px solid #059669;
            padding: 5px;
            border-radius: 0 6px 6px 0;
        }
        .feeling-title {
            font-size: 8.5px;
            font-weight: bold;
            color: #059669;
            margin-bottom: 2px;
        }
        .feeling-text {
            font-size: 9.5px;
            color: #1e293b;
            line-height: 1.35;
            font-weight: 600;
        }
        .tip-box {
            font-size: 9px;
            color: #334155;
            line-height: 1.4;
            border-left: 2px solid #e11d48;
            padding-left: 6px;
        }
        .tip-title {
            font-weight: bold;
            color: #e11d48;
            margin-bottom: 2px;
            font-size: 8.5px;
        }
        .summary-sequence {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
            gap: 3px;
            font-size: 8px;
        }
        .summary-node {
            background: rgba(0, 0, 0, 0.03);
            padding: 2px 5px;
            border-radius: 4px;
            color: #475569;
        }
        .summary-node.highlight {
            background: rgba(2, 132, 199, 0.1);
            color: #0284c7;
            font-weight: 700;
        }
        .summary-arrow {
            color: #94a3b8;
        }
        .quiz-container {
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 8px;
        }
        .quiz-item {
            background: rgba(0, 0, 0, 0.01);
            padding: 3px;
            border-radius: 4px;
            border: 1px solid rgba(0, 0, 0, 0.02);
        }
        .quiz-q {
            color: #1e293b;
            font-weight: 600;
            line-height: 1.25;
            margin-bottom: 1px;
        }
        .quiz-t {
            color: #64748b;
            line-height: 1.2;
        }
        .quiz-answer {
            font-size: 7px;
            color: rgba(219, 39, 119, 0.7);
            text-align: right;
            margin-top: 1px;
            font-weight: bold;
        }
        .page-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(0, 0, 0, 0.06);
            padding-top: 4px;
            font-size: 9px;
            color: #64748b;
            margin-top: 6px;
        }
        .page-footer .instalink {
            color: #475569;
            font-weight: 600;
        }
    </style>
</head>
<body>
"""

    for i, vocab in enumerate(vocab_list):
        word = vocab["word"]
        pronunciation = vocab["pronunciation"]
        meaning1 = vocab["meaning1"]
        meaning2 = vocab["meaning2"]
        intro = vocab["intro"]
        etymology = vocab["etymology"]
        examples1 = vocab["examples1"]
        transition_question = vocab["transition_question"]
        logic_flow = vocab["logic_flow"]
        logic_desc = vocab["logic_desc"]
        examples2 = vocab["examples2"]
        feeling = vocab["feeling"]
        real_tip = vocab["real_tip"]
        summary_flow = vocab["summary_flow"]
        quiz = vocab["quiz"]
        
        page_num = i + 1
        
        # 라틴어 어원 데이터가 있는 경우 대입
        if word in latin_etymologies:
            etym_data = latin_etymologies[word]
            root1_str = etym_data["root1"]
            root2_str = etym_data["root2"]
            flow_steps = etym_data["flow"].split(" &rarr; ")
        else:
            root1_str = etymology['root1']
            root2_str = etymology['root2']
            if isinstance(etymology['flow'], list):
                flow_steps = etymology['flow']
            else:
                flow_steps = etymology['flow'].split(" &rarr; ")
            
        # 13개 카드 렌더링
        html_content += f"""
    <div class="page">
        <!-- 상단 헤더 -->
        <div class="page-header">
            <div class="brand">
                <span>Voca Guide</span> <span class="brand-sub">수능·내신 필수 어휘 • 40Q 완성 교재</span>
            </div>
            <div class="brand-sub" style="font-weight: 700; color: #0284c7; font-family: 'Noto Sans KR', sans-serif;">고등 영어1 (YBM 박준언) Lesson 4</div>
        </div>
        
        <!-- 그리드 본문 -->
        <div class="grid-container">
            <!-- 1. Q&A 질문 (2칸 차지) -->
            <div class="card card-q" style="grid-column: span 2;">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">Q</div></div>
                        <div class="profile-info">
                            <span class="profile-username">student_q</span>
                            <span class="profile-subtext">질문 게시판</span>
                        </div>
                    </div>
                    <span class="insta-badge" style="color: #b45309;">1 / 13</span>
                </div>
                <div class="card-body">
                    <p class="q-text">Q. 선생님, {word}는 '{meaning1.split('(')[0].strip()}' 인데요. 왜 '{meaning2.split('(')[0].strip()}' 라는 뜻도 있는 건가요??? 🤔</p>
                </div>
            </div>
            
            <!-- 2. 인사말 (1칸 차지) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">어휘 특강</span>
                        </div>
                    </div>
                    <span class="insta-badge">2 / 13</span>
                </div>
                <div class="card-body">
                    <p class="intro-text">"이 질문도 꽤 많이 다룬 핵심 질문입니다. 다시 한번 핵심을 파헤쳐 볼까요? 😉"</p>
                </div>
            </div>
            
            <!-- 3. 메인 단어 카드 (1칸) -->
            <div class="card card-word">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">어휘 특강</span>
                        </div>
                    </div>
                    <span class="insta-badge" style="color: #0284c7;">3 / 13</span>
                </div>
                <div class="card-body" style="justify-content: flex-start; padding-top: 4px;">
                    <h2 class="word-title">{word}</h2>
                    <div class="word-pron">/{pronunciation}/</div>
                    <div class="word-meanings">
                        <div><span class="mean-num">①</span> <span>{meaning1}</span></div>
                        <div><span class="mean-num">②</span> <span>{meaning2}</span></div>
                    </div>
                </div>
            </div>
            
            <!-- 4. 어원 분석 카드 (1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">어원 분석</span>
                        </div>
                    </div>
                    <span class="insta-badge">4 / 13</span>
                </div>
                <div class="card-body">
                    <div class="etym-box">
                        <div class="etym-item"><strong>어근 1</strong>: {root1_str}</div>
                        <div class="etym-item"><strong>어근 2</strong>: {root2_str}</div>
                        <div class="etym-flow">
                            {" &rarr; ".join([f'<span class="etym-flow-step">{step}</span>' for step in flow_steps])}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 5. 예문 1 카드 (1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">예문 학습 ①</span>
                        </div>
                    </div>
                    <span class="insta-badge">5 / 13</span>
                </div>
                <div class="card-body">
                    <div class="example-list">
                        <div class="example-item">
                            <p class="ex-en">{examples1[0]['en']}</p>
                            <p class="ex-ko">{examples1[0]['ko']}</p>
                        </div>
                        <div class="example-item">
                            <p class="ex-en">{examples1[1]['en']}</p>
                            <p class="ex-ko">{examples1[1]['ko']}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 6. 전환 질문 카드 (1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">의미의 확장</span>
                        </div>
                    </div>
                    <span class="insta-badge">6 / 13</span>
                </div>
                <div class="card-body">
                    <p class="trans-question">"{transition_question}"</p>
                </div>
            </div>
            
            <!-- 7. 핵심 연결 논리 카드 (2칸 차지) -->
            <div class="card" style="grid-column: span 2;">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">논리 연계 스토리</span>
                        </div>
                    </div>
                    <span class="insta-badge">7 / 13</span>
                </div>
                <div class="card-body">
                    <div class="logic-flow-box">
                        {f' <span class="logic-arrow">&darr;</span> '.join([f'<span class="logic-step">{step}</span>' for step in logic_flow if step != '↓'])}
                    </div>
                    <p class="logic-desc">💡 {logic_desc}</p>
                </div>
            </div>
            
            <!-- 8. 뜻 2 소개 카드 (1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">추상적 정의</span>
                        </div>
                    </div>
                    <span class="insta-badge">8 / 13</span>
                </div>
                <div class="card-body">
                    <div class="meaning2-title">Second Meaning</div>
                    <div class="meaning2-box">"{meaning2.split('(')[0].strip()}"</div>
                </div>
            </div>
            
            <!-- 9. 예문 2 카드 (1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">예문 학습 ②</span>
                        </div>
                    </div>
                    <span class="insta-badge">9 / 13</span>
                </div>
                <div class="card-body">
                    <div class="example-list">
                        <div class="example-item-ko">
                            <p class="ex-en">{examples2[0]['en']}</p>
                            <p class="ex-ko">{examples2[0]['ko']}</p>
                        </div>
                        <div class="example-item-ko">
                            <p class="ex-en">{examples2[1]['en']}</p>
                            <p class="ex-ko">{examples2[1]['ko']}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 10. 뉘앙스 정리 카드 (10 / 13, 1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">뉘앙스 느낌</span>
                        </div>
                    </div>
                    <span class="insta-badge">10 / 13</span>
                </div>
                <div class="card-body">
                    <div class="feeling-box">
                        <div class="feeling-title">Core Image</div>
                        <div class="feeling-text">{feeling.replace(f'{word} = ', '')}</div>
                    </div>
                </div>
            </div>
            
            <!-- 11. 실제 꿀팁 카드 (11 / 13, 1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">실전 꿀팁</span>
                        </div>
                    </div>
                    <span class="insta-badge">11 / 13</span>
                </div>
                <div class="card-body">
                    <div class="tip-box">
                        <div class="tip-title">Test / Focus</div>
                        <div>{real_tip}</div>
                    </div>
                </div>
            </div>
            
            <!-- 12. 요약 흐름 카드 (12 / 13, 1칸) -->
            <div class="card">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">요약 시퀀스</span>
                        </div>
                    </div>
                    <span class="insta-badge">12 / 13</span>
                </div>
                <div class="card-body">
                    <div class="summary-sequence">
                        {" &rarr; ".join([f'<span class="summary-node {"highlight" if node == word or node in meaning2 else ""}" >{node}</span>' for node in summary_flow])}
                    </div>
                </div>
            </div>
            
            <!-- 13. 퀴즈 테스트 카드 (13 / 13, 1칸) -->
            <div class="card card-quiz">
                <div class="insta-header">
                    <div class="insta-profile">
                        <div class="profile-pic"><div class="profile-pic-inner">V</div></div>
                        <div class="profile-info">
                            <span class="profile-username">voca_guide</span>
                            <span class="profile-subtext">데일리 퀴즈</span>
                        </div>
                    </div>
                    <span class="insta-badge" style="color: #db2777;">13 / 13</span>
                </div>
                <div class="card-body">
                    <div class="quiz-container">
                        <div class="quiz-item">
                            <p class="quiz-q">(1) {quiz[0]['question']}</p>
                            <p class="quiz-t">{quiz[0]['translation']}</p>
                        </div>
                        <div class="quiz-item">
                            <p class="quiz-q">(2) {quiz[1]['question']}</p>
                            <p class="quiz-t">{quiz[1]['translation']}</p>
                        </div>
                        <div class="quiz-answer">
                            정답: (1) {quiz[0]['answer']} / (2) {quiz[1]['answer']}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 하단 푸터 -->
        <div class="page-footer">
            <span class="instalink">Essential Vocabulary Guide Book</span>
            <span>{page_num:02d} / 40</span>
        </div>
    </div>
"""

    html_content += """
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated HTML file at {html_path}")

async def render_pdf():
    html_path = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/Lesson4_Vocabulary_CardNews_40.html")
    pdf_path = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/Lesson4_Vocabulary_CardNews_40.pdf")
    
    print(f"Rendering {html_path} to {pdf_path} using Playwright...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # HTML 로드
        await page.goto(f"file://{html_path}")
        
        # 폰트 및 리소스 로딩 대기
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)  # 폰트 렌더링을 위해 조금 넉넉히 대기
        
        # PDF 출력
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        
        await browser.close()
    print("PDF Generation Completed successfully.")

if __name__ == "__main__":
    build_html()
    asyncio.run(render_pdf())
