import json
import os

vocab_list = [
    {
        "word": "enormously",
        "pronunciation": "i-NAWR-muhs-lee",
        "meaning1": "거대하게 (물리적)",
        "meaning2": "엄청나게, 매우 (추상적)",
        "intro": "이 단어는 덩치 큰 느낌과 강조하는 느낌이 동시에 있어요. 왜 그럴까요?",
        "etymology": {
            "root1": "e- : out of (벗어남)",
            "root2": "norm : rule, standard (규격, 기준)",
            "flow": ["기준(규격)을 벗어남", "일반적인 한계를 초과함", "물리적으로 거대하게", "추상적으로 엄청나게, 매우"]
        },
        "examples1": [
            {"en": "The building was enormously constructed.", "ko": "그 건물은 거대하게 건설되었다."},
            {"en": "She was enormously successful.", "ko": "그녀는 엄청나게 성공했다."}
        ],
        "transition_question": "그런데 왜 추상적인 \"매우\"라는 뜻으로 더 자주 쓰일까요?",
        "logic_flow": ["물리적 규격을 넘어선 큰 크기", "↓", "인간의 인지적 한계를 뛰어넘음", "↓", "매우 강조하는 부사로 전이", "↓", "엄청나게, 극도로"],
        "logic_desc": "규격을 벗어난 거대한 크기가 마음의 감탄(매우, 엄청나게)으로 확장된 것입니다.",
        "examples2": [
            {"en": "This habit is enormously useful.", "ko": "이 습관은 엄청나게 유용하다."},
            {"en": "They enjoyed the concert enormously.", "ko": "그들은 그 콘서트를 매우 즐겼다."}
        ],
        "feeling": "enormously = 규격 외의 크기 = 상상을 초월하는 = 엄청나게",
        "real_tip": "실제 수능이나 내신 시험에서는 '매우(extremely)'의 동의어로 훨씬 자주 출제됩니다.",
        "summary_flow": ["norm 기준", "enormous 기준을 벗어난 거대한", "enormously 거대하게", "추상화", "엄청나게, 매우"],
        "quiz": [
            {"question": "Both sides benefited __________ from the partnership.", "translation": "양측은 그 파트너십으로부터 엄청나게 혜택을 입었다.", "answer": "enormously"},
            {"question": "The task was __________ difficult.", "translation": "그 작업은 대단히 어려웠다.", "answer": "enormously"}
        ]
    },
    {
        "word": "episode",
        "pronunciation": "EP-uh-sohd",
        "meaning1": "일화, 사건 (일상적 해프닝)",
        "meaning2": "방송 회차 (에피소드)",
        "intro": "드라마의 1화, 2화할 때의 에피소드가 왜 일상 속 '사건'도 되는 걸까요?",
        "etymology": {
            "root1": "epi- : in addition (곁에, 덧붙여)",
            "root2": "eis-hodos : entry, way (들어오는 길, 입구)",
            "flow": ["본 길 옆으로 들어오는 곁길", "연극 중 노래 사이에 덧붙여진 말", "본 줄거리 밖의 짧은 토막 이야기", "일상의 일화 / 드라마의 한 회차"]
        },
        "examples1": [
            {"en": "It was a funny episode in my childhood.", "ko": "그것은 내 어린 시절의 재미있는 일화였다."},
            {"en": "This episode taught me a great lesson.", "ko": "이 사건은 나에게 큰 교훈을 주었다."}
        ],
        "transition_question": "곁다리 이야기가 어떻게 \"드라마 1회분\"이 되었을까요?",
        "logic_flow": ["그리스 연극 중 코러스 사이에 들어가는 배우의 연기", "↓", "본 줄거리 곁에 덧붙여진 독립된 토막 이야기", "↓", "연속극에서 전체 테마 중 하나를 다루는 독립된 방송분", "↓", "드라마 1회차 에피소드"],
        "logic_desc": "전체 큰 흐름에서 쪼개져 나온 '독립된 이야기 한 토막'이라는 개념에서 출발했습니다.",
        "examples2": [
            {"en": "Did you watch the final episode of the show?", "ko": "그 쇼의 마지막 에피소드(마지막 회)를 봤니?"},
            {"en": "This is the most popular episode.", "ko": "이것이 가장 인기 있는 회차이다."}
        ],
        "feeling": "episode = 전체 흐름에서 곁가지로 뻗어 나온 = 독립된 이야기 한 토막 = 일화 / 방송의 회차",
        "real_tip": "뉴스에서 '우울증 삽화(depressive episode)'처럼 의학적으로 특정 증상이 나타나는 '기간, 시기'를 뜻하기도 합니다.",
        "summary_flow": ["hodos 길", "eishodos 들어가는 길", "episode 곁다리로 들어간 이야기", "일화(해프닝)", "독립된 방송 회차"],
        "quiz": [
            {"question": "That was a painful __________ in my life.", "translation": "그것은 내 인생에서 고통스러운 사건이었다.", "answer": "episode"},
            {"question": "I can't wait for the next __________ of the series.", "translation": "그 시리즈의 다음 회차가 너무 기다려진다.", "answer": "episode"}
        ]
    },
    {
        "word": "subscribers",
        "pronunciation": "suhb-SKRY-berz",
        "meaning1": "기부자, 찬성 서명자",
        "meaning2": "구독자들 (유튜브, 신문 등)",
        "intro": "유튜브 '구독자'를 뜻하는 이 단어에 왜 '기부자, 서명자'라는 어려운 뜻이 숨어 있을까요?",
        "etymology": {
            "root1": "sub- : under (아래에)",
            "root2": "scribe : write (적다, 쓰다)",
            "flow": ["계약서 아래에 이름을 적다", "조항에 서명하여 동의하다", "정기 후원이나 대금 지불을 동의하다", "정기구독자, 기부자"]
        },
        "examples1": [
            {"en": "The subscribers to the charter signed below.", "ko": "헌장에 동의한 서명자들이 아래에 서명했다."},
            {"en": "The charity has many loyal subscribers.", "ko": "그 자선단체는 많은 충실한 기부자들을 두고 있다."}
        ],
        "transition_question": "서명하고 기부하는 행위가 어떻게 \"유튜브 구독\"으로 이어졌을까요?",
        "logic_flow": ["계약서나 지지 선언서 아래(sub)에 이름 서명(scribe)하기", "↓", "이 단체나 주장에 찬성하여 정기적으로 돈을 내기로 서명함", "↓", "신문이나 잡지를 정기적으로 돈 내고 받아보는 구독자로 확장", "↓", "유튜브나 OTT 등 채널을 정기적으로 받아보는 구독자"],
        "logic_desc": "단순한 시청이 아니라 '내가 이 채널(혹은 매체)에 서명하여 지지하고 받아보겠다'는 약속이 내포되어 있습니다.",
        "examples2": [
            {"en": "The magazine lost thousands of subscribers.", "ko": "그 잡지는 수천 명의 구독자를 잃었다."},
            {"en": "Subscribers can access exclusive content.", "ko": "구독자들은 독점 콘텐츠에 접근할 수 있다."}
        ],
        "feeling": "subscribers = 문서 아래에 서명하여 동의한 사람들 = 지지 정기 후원자 = 정기 구독자",
        "real_tip": "계약서 아래에 서명하는 주체를 뜻하므로, 주식 청약자(subscribers of shares)라는 경영 용어로도 쓰입니다.",
        "summary_flow": ["scribe 쓰다", "subscribe 아래에 서명하다", "subscriber 서명자, 동의자", "정기 결제 구독자", "유튜브/매체 구독자"],
        "quiz": [
            {"question": "The newly launched channel gained 10,000 __________ in a day.", "translation": "새로 개설된 채널은 하루 만에 만 명의 구독자를 모았다.", "answer": "subscribers"},
            {"question": "The list of __________ to the fund was published.", "translation": "기금 서명 기부자 명단이 공개되었다.", "answer": "subscribers"}
        ]
    },
    {
        "word": "concept",
        "pronunciation": "KAHN-sept",
        "meaning1": "기본 구상, 초안",
        "meaning2": "개념, 정의 (추상적 이론)",
        "intro": "미술이나 비즈니스에서 말하는 '컨셉'과 수학이나 과학의 '개념'이 어떻게 같은 단어일까요?",
        "etymology": {
            "root1": "con- : together (함께, 완전히)",
            "root2": "cept : take, hold (취하다, 쥐다)",
            "flow": ["흩어진 생각들을 마음속에 함께 모아 쥐다", "마음속에 어떤 아이디어를 품어 내다", "설계의 뼈대가 되는 기본 구상", "이론적인 추상적 개념"]
        },
        "examples1": [
            {"en": "She introduced the basic concept of the design.", "ko": "그녀는 그 디자인의 기본 구상을 소개해 주었다."},
            {"en": "The concept car was shown at the exhibition.", "ko": "그 컨셉트 카(개발 초안 차량)가 전시회에 나타났다."}
        ],
        "transition_question": "마음속에 품은 설계 초안이 어떻게 학술적인 \"개념\"이 되었을까요?",
        "logic_flow": ["머릿속에 떠도는 복잡한 생각들을 하나로 모아서(con) 쥐어(cept)봄", "↓", "하나의 뼈대 구상이 마음속에 잉태됨 (구상, 컨셉)", "↓", "이 구상을 단어로 명확하게 규정하여 모든 이가 공유할 수 있게 만듦", "↓", "학술적 이론의 개념 정의"],
        "logic_desc": "머릿속으로 완전히 파악하여 쥐고 있는 핵심적인 정의를 나타냅니다.",
        "examples2": [
            {"en": "It is a difficult concept to explain to children.", "ko": "그것은 아이들에게 설명하기 어려운 개념이다."},
            {"en": "He failed to grasp the concept of gravity.", "ko": "그는 중력의 개념을 이해하지 못했다."}
        ],
        "feeling": "concept = 함께 모아 마음속에 쥔 생각 = 뼈대가 되는 구상 = 정의된 개념",
        "real_tip": "동사형 conceive(품다, 생각하다)와 명사형 conception(개념, 임신)도 같은 어원에서 나온 세트 단어입니다.",
        "summary_flow": ["cept 잡다", "conceive 마음속에 품다", "concept 마음속에 모아 쥔 뼈대", "개발 기본 구상", "정의된 학술 개념"],
        "quiz": [
            {"question": "The new marketing __________ is focused on eco-friendly packaging.", "translation": "새로운 마케팅 구상은 친환경 포장에 초점을 맞추고 있다.", "answer": "concept"},
            {"question": "We need to define the key __________ of this research.", "translation": "우리는 이 연구의 핵심 개념을 정의해야 한다.", "answer": "concept"}
        ]
    },
    {
        "word": "originally",
        "pronunciation": "uh-RIJ-uh-nuhl-ee",
        "meaning1": "원래, 본래 (기원상)",
        "meaning2": "독창적으로 (새롭게)",
        "intro": "과거를 뜻하는 '원래'와 새로움을 뜻하는 '독창적으로'가 왜 한 단어에 뭉쳐 있을까요?",
        "etymology": {
            "root1": "origin : source, rise (시작점, 기원)",
            "root2": "-ally : 부사 접사",
            "flow": ["가장 처음의 기원에서부터 시작하여", "원래, 본래 상태로", "다른 이의 모방이 아닌 최초 시작점 그대로의 독특함", "독창적으로"]
        },
        "examples1": [
            {"en": "The house was originally a school.", "ko": "그 집은 원래 학교였다."},
            {"en": "Originally, we planned to go to the beach.", "ko": "원래 우리는 해변에 가기로 계획했었다."}
        ],
        "transition_question": "옛날을 가리키는 시작점이 어떻게 \"독창적인\"으로 바뀌었을까요?",
        "logic_flow": ["세상의 모든 것이 시작된 최초의 시작점(origin)", "↓", "시간의 출발선에 서서 원래 상태로 (본래)", "↓", "그 출발점의 독창적이고 순수한 특징을 지님", "↓", "남을 따라 하지 않고 기원 그대로의 독자성을 뽐냄", "↓", "독창적으로"],
        "logic_desc": "남을 흉내 내지 않고, 최초의 소스(Origin) 자체에서 직접 끌어온 듯이 생각하고 표현하는 모습을 가리킵니다.",
        "examples2": [
            {"en": "She thinks very originally.", "ko": "그녀는 아주 독창적으로 생각한다."},
            {"en": "The artist interpreted the theme quite originally.", "ko": "그 예술가는 그 주제를 꽤 독창적으로 해석했다."}
        ],
        "feeling": "originally = 기원인 최초의 시점부터 = 원래 = 모방이 없는 기원 본연의 = 독창적으로",
        "real_tip": "originate(유래하다, 시작되다)와 originality(독창성) 또한 수능 어휘 단골 출제 세트입니다.",
        "summary_flow": ["origin 기원, 시작", "original 최초의 / 독창적인", "originally 기원상 원래", "의미의 진화", "독창적으로"],
        "quiz": [
            {"question": "This novel was __________ written in Korean.", "translation": "이 소설은 원래 한국어로 쓰였다.", "answer": "originally"},
            {"question": "He has a rare ability to solve problems __________.", "translation": "그는 문제를 독창적으로 해결하는 흔치 않은 능력을 가졌다.", "answer": "originally"}
        ]
    },
    {
        "word": "creativity",
        "pronunciation": "kree-ey-TIV-i-tee",
        "meaning1": "창의력, 독창성 (능력)",
        "meaning2": "창작성, 창작물 (결과)",
        "intro": "머릿속의 아이디어인 '창의력'과 밖으로 표현된 '창작물'이 어떻게 한 단어로 호환될까요?",
        "etymology": {
            "root1": "cre- : grow, make (자라나게 하다, 창조하다)",
            "root2": "-tivity : 성질, 능력을 뜻하는 명사 접사",
            "flow": ["무에서 유를 자라나게 하는 성질", "새로운 아이디어를 낳는 정신적 창의력", "실제 현실에 그 능력을 발현하는 것", "창작적 결과물"]
        },
        "examples1": [
            {"en": "Art helps to develop children's creativity.", "ko": "미술은 아이들의 창의력을 발달시키는 데 도움이 된다."},
            {"en": "We need more creativity in our marketing.", "ko": "우리는 마케팅에서 더 많은 창조성이 필요하다."}
        ],
        "transition_question": "추상적 능력이 어떻게 실제 \"창작물\"의 느낌으로 쓰이게 되었을까요?",
        "logic_flow": ["생각 속에서 무언가를 만들어 자라나게(cre) 하는 힘", "↓", "남들이 생각지 못한 방식으로 생각하는 창의력", "↓", "그 능력이 외부로 발현되어 특수한 결과물을 이룸", "↓", "작품이나 제품 등에서 보여주는 구체화된 독창성(창작적 행위)"],
        "logic_desc": "머릿속에 머무는 생각의 힘에 그치지 않고, 실제로 무언가를 만들어내어 입증하는 생산적인 역량을 통칭합니다.",
        "examples2": [
            {"en": "The film was praised for its artistic creativity.", "ko": "그 영화는 예술적 창작성으로 극찬을 받았다."},
            {"en": "Technological innovation requires both creativity and execution.", "ko": "기술 혁신은 창조성과 실행력 둘 다를 요구한다."}
        ],
        "feeling": "creativity = 무에서 유를 기르는 힘 = 창의력 = 겉으로 입증된 창작적 독창성",
        "real_tip": "recreate는 '재창조하다' 외에도 '기분 전환을 하다(휴양하다 - recreation)'라는 중요한 뜻이 있습니다.",
        "summary_flow": ["creare 창조하다", "creative 창조적인", "creativity 창조하는 힘(창의력)", "외부적 실현", "예술적 창작성"],
        "quiz": [
            {"question": "The team's __________ led to a breakthrough in the project.", "translation": "그 팀의 창의력이 프로젝트의 돌파구를 열었다.", "answer": "creativity"},
            {"question": "He expressed his __________ through music.", "translation": "그는 음악을 통해 자신의 창작성(창조력)을 표현했다.", "answer": "creativity"}
        ]
    },
    {
        "word": "cleansing",
        "pronunciation": "KLEN-zing",
        "meaning1": "세안, 피부 씻어내기 (물리적)",
        "meaning2": "두뇌 정화, 죄의 정화 (정신적)",
        "intro": "클렌징 폼할 때의 '세안'이 어떻게 마음이나 머릿속을 비워내는 '정화'가 될까요?",
        "etymology": {
            "root1": "clean : free from dirt (깨끗한)",
            "root2": "-sing : 행동을 나타내는 동사/명사 변형",
            "flow": ["더러운 것을 닦아내 깨끗하게 함", "얼굴이나 몸의 먼지를 씻어내는 세안", "머릿속이나 마음에 쌓인 찌꺼기를 깨끗하게 함", "죄나 오염을 씻어내는 영적 정화"]
        },
        "examples1": [
            {"en": "She bought a new cleansing oil.", "ko": "그녀는 새로운 세안용 클렌징 오일을 샀다."},
            {"en": "A deep cleansing is necessary for oily skin.", "ko": "지성 피부에는 딥 클렌징(세안)이 필수적이다."}
        ],
        "transition_question": "피부를 씻는 세척이 어떻게 마음에 적용되어 \"정화\"가 되었을까요?",
        "logic_flow": ["표면에 붙어 있는 물리적인 먼지와 기름때를 깨끗이 제거함", "↓", "머릿속을 어지럽히는 복잡한 생각, 쓰레기 정보들을 털어냄", "↓", "일명 '브레인 클렌징(두뇌 정화)'", "↓", "내면의 상처나 영적인 죄의 씻김으로 고도화"],
        "logic_desc": "더러운 불순물을 제거하여 본연의 깨끗한 상태로 되돌리는 모든 행위를 아우릅니다.",
        "examples2": [
            {"en": "Morning pages are meant to be a brain cleansing.", "ko": "모닝페이지는 두뇌 정화(머릿속 비워내기)를 위한 것이다."},
            {"en": "The ritual was performed for spiritual cleansing.", "ko": "그 의식은 영적인 정화를 위해 거행되었다."}
        ],
        "feeling": "cleansing = 더러운 때를 씻음 = 피부 세안 = 내면의 찌꺼기를 비워냄 = 두뇌/영적 정화",
        "real_tip": "정치사에서 특정 집단을 몰아내는 부정적 단어로 '인종 청소(ethnic cleansing)'라고 쓰기도 합니다.",
        "summary_flow": ["clean 깨끗한", "cleanse 깨끗하게 하다", "cleansing 피부 세안", "추상적 확장", "두뇌/정신적 정화"],
        "quiz": [
            {"question": "Writing down worries helps with mental __________.", "translation": "걱정거리를 적는 것은 정신적 정화(비워내기)에 도움을 준다.", "answer": "cleansing"},
            {"question": "Apply the __________ cream to your face gently.", "translation": "세안용 크림을 얼굴에 부드럽게 바르세요.", "answer": "cleansing"}
        ]
    },
    {
        "word": "private",
        "pronunciation": "PRY-vit",
        "meaning1": "비공개인, 사적인 (개인적인)",
        "meaning2": "이등병, 최말단 병사 (군사)",
        "intro": "비공개를 뜻하는 '사적인' 단어가 왜 군대에서는 '이등병'을 가리킬까요?",
        "etymology": {
            "root1": "priv : deprived, single (박탈된, 분리된)",
            "root2": "-ate : 형용사/명사 접사",
            "flow": ["공적인 관직에서 분리되어 단독으로 있다", "대중에게 공개되지 않는 사적인 공간", "공식 관직이나 지위가 없는 개인 신분", "군대에서 직책이 없는 말단 이등병"]
        },
        "examples1": [
            {"en": "Keep your morning pages completely private.", "ko": "당신의 모닝페이지를 완전히 비공개로 유지하세요."},
            {"en": "This is a private conversation, please leave.", "ko": "이것은 사적인 대화이니 자리를 비워 주세요."}
        ],
        "transition_question": "나만의 비밀이 어떻게 최하위 군인인 \"이등병\"이 되었을까요?",
        "logic_flow": ["국가나 왕실 등 공공(Public) 영역에서 떨어져 나와 분리됨(priv)", "↓", "나만의 고유한 영역인 '사적인, 비공개의'", "↓", "공식 지위나 임명장이 없는 평범한 '일반 개인 시민'", "↓", "군대에서 아무런 지휘권이나 특별 계급이 없는 일반 사병", "↓", "가장 기저의 최말단 계급인 이등병"],
        "logic_desc": "공식적인 관직이나 지휘권이 없이, 단독(private citizen)으로 군복무를 시작하는 신분을 뜻합니다.",
        "examples2": [
            {"en": "Private Kim was assigned to our unit.", "ko": "김 이등병이 우리 부대로 배치되었다."},
            {"en": "He entered the army as a private.", "ko": "그는 이등병으로 육군에 입대했다."}
        ],
        "feeling": "private = 공적 영역에서 분리된 = 사적인 / 비공개의 = 계급이 없는 개인 병사 = 이등병",
        "real_tip": "privilege(특권)는 private(사적인) + lex(법)가 합쳐져 '특정 개인에게만 적용되는 사적인 법'에서 유래했습니다.",
        "summary_flow": ["priv 분리시키다", "private 공공과 분리된 사적인", "private citizen 일반 시민", "군대 적용", "이등병, 일반 사병"],
        "quiz": [
            {"question": "The document contains __________ information.", "translation": "그 문서에는 비공개(사적인) 정보가 포함되어 있다.", "answer": "private"},
            {"question": "He was promoted from __________ to corporal.", "translation": "그는 이등병에서 상병으로 진급했다.", "answer": "private"}
        ]
    },
    {
        "word": "honestly",
        "pronunciation": "AHN-ist-lee",
        "meaning1": "솔직하게, 가식 없이 (정직하게)",
        "meaning2": "정말로, 참으로 (강조 부사)",
        "intro": "'솔직하게 말해서'라고 할 때의 부사가 왜 '정말로 모르겠다'처럼 부정문을 강조할까요?",
        "etymology": {
            "root1": "honor : honor, dignity (명예, 고결함)",
            "root2": "-ly : 부사 접사",
            "flow": ["명예를 지키며 떳떳하게 행동하여", "추호의 거짓 없이 솔직하고 정직하게", "자신의 말에 한 점의 가식도 없음을 강변함", "참으로, 진짜로 (강조)"]
        },
        "examples1": [
            {"en": "It is important for you to write honestly.", "ko": "당신이 솔직하게 글을 쓰는 것이 중요합니다."},
            {"en": "She honestly answered all the questions.", "ko": "그녀는 모든 질문에 솔직하게 답변했다."}
        ],
        "transition_question": "정직함이 어떻게 의미를 세게 밀어붙이는 \"정말로\"가 되었을까요?",
        "logic_flow": ["명예로운(honor) 선비처럼 양심을 지키는 태도", "↓", "남을 속이지 않고 떳떳하게 정직하게", "↓", "자신의 진심을 하소연하며 문장 앞에 붙임", "↓", "내 말에 진짜 거짓이 없다는 서약적 강조", "↓", "정말로, 진짜로 (강조)"],
        "logic_desc": "자기 발언의 참됨을 걸고 말함으로써 문장 전체의 진실성을 강화하는 어법입니다.",
        "examples2": [
            {"en": "I honestly don't know what to do next.", "ko": "나는 다음엔 무엇을 해야 할지 정말로 모르겠다."},
            {"en": "Honestly, that was the best meal I've ever had.", "ko": "정말로, 그것은 내가 먹어본 것 중 최고의 식사였다."}
        ],
        "feeling": "honestly = 명예롭게 거짓 없이 = 솔직하게 = 나의 양심을 걸고 강조건대 = 정말로 / 진짜로",
        "real_tip": "구어체에서 'Honestly!'라고 단독으로 외치면 상대의 어이없는 행동에 대한 '정말 기가 막히네!'라는 짜증 섞인 표현이 됩니다.",
        "summary_flow": ["honor 명예", "honest 정직한", "honestly 정직하게", "구어적 강조", "정말로, 참으로"],
        "quiz": [
            {"question": "Speak __________ about your feelings.", "translation": "당신의 감정에 대해 솔직하게 이야기해 보세요.", "answer": "honestly"},
            {"question": "I __________ believe this is our only option.", "translation": "나는 정말로 이것이 우리의 유일한 선택이라고 믿는다.", "answer": "honestly"}
        ]
    },
    {
        "word": "complaints",
        "pronunciation": "kuhm-PLAYNTS",
        "meaning1": "불평들, 불만 사항 (항의)",
        "meaning2": "질환들, 육체적 통증 (의학)",
        "intro": "고객 센터에 접수되는 '불평'이 어떻게 병원에 호소하는 '통증, 질환'과 같은 단어일까요?",
        "etymology": {
            "root1": "com- : intensive (강하게)",
            "root2": "plaint : beat the breast (가슴을 치며 슬퍼하다)",
            "flow": ["슬픔과 고통으로 가슴을 강하게 치다", "자신이 겪는 억울함이나 손해를 하소연함", "불평, 불만 토로", "몸이 아파 괴로워하는 신체적 통증/질환"]
        },
        "examples1": [
            {"en": "I wrote a lot of complaints about my hard life.", "ko": "나는 내 힘든 삶에 대한 불평을 많이 적었다."},
            {"en": "The manager handled all the customer complaints.", "ko": "그 매니저는 모든 고객 불만 사항들을 처리했다."}
        ],
        "transition_question": "하소연하는 불평이 어떻게 의학적 \"질병, 통증\"이 되었을까요?",
        "logic_flow": ["몸이나 마음이 너무 아파서 가슴을 부여잡고 끙끙 앓음", "↓", "자신을 아프게 만드는 요인에 대해 거세게 호소함 (불평, 불만)", "↓", "의사에게 내 몸 어디가 쑤시고 아픈지 증상을 호소함 (통증)", "↓", "그 통증을 유발하는 고질적인 질병 자체"],
        "logic_desc": "고통스럽고 불편한 상태를 외부로 표현하고 호소하는 대상(Complaint)이라는 점에서 통일됩니다.",
        "examples2": [
            {"en": "Most back complaints can be treated without surgery.", "ko": "대부분의 등 통증(허리 질환)은 수술 없이 치료될 수 있다."},
            {"en": "He went to the doctor with chest complaints.", "ko": "그는 가슴 통증(흉부 질환)을 호소하며 의사를 찾아갔다."}
        ],
        "feeling": "complaints = 아파서 가슴 치는 비명 = 삶에 대한 불평/불만 = 몸이 아픈 통증/질환",
        "real_tip": "plaintiff는 '고통을 호소하는 사람'이라는 뜻에서 유래하여 법률 용어로 '원고(소송을 제기한 사람)'를 뜻합니다.",
        "summary_flow": ["plangere 슬피 울다", "complain 불평하다 / 통증을 호소하다", "complaint 불평, 불만", "의학적 의미 전이", "통증, 질환"],
        "quiz": [
            {"question": "We received several __________ about the noise.", "translation": "우리는 소음에 관한 여러 건의 불평(민원)을 접수했다.", "answer": "complaints"},
            {"question": "He has been suffering from chronic stomach __________.", "translation": "그는 만성적인 위장 질환(통증)으로 고통받아 왔다.", "answer": "complaints"}
        ]
    },
    {
        "word": "productive",
        "pronunciation": "pruh-DUHK-tiv",
        "meaning1": "생산적인, 효율이 높은",
        "meaning2": "다작하는, 결실이 풍부한",
        "intro": "일 처리가 빠를 때 쓰는 '생산적인'이 왜 예술가에게는 '다작하는'이라는 뜻으로 연결될까요?",
        "etymology": {
            "root1": "pro- : forward (앞으로)",
            "root2": "duct : lead, pull (이끌다, 당기다)",
            "flow": ["결과물을 앞으로 이끌어 내다", "노력 대비 얻어내는 아웃풋이 많음", "생산적인, 효율적인", "수많은 작품이나 열매를 풍성하게 생산하는"]
        },
        "examples1": [
            {"en": "Nowadays, I feel less stressed and more productive.", "ko": "요즘 나는 스트레스도 덜 받고 더 생산적이다."},
            {"en": "We had a highly productive meeting today.", "ko": "우리는 오늘 매우 생산적인 회의를 가졌다."}
        ],
        "transition_question": "결과물을 잘 만드는 특성이 창작자에게 어떻게 적용될까요?",
        "logic_flow": ["무언가를 밖으로 끌어내는(duct) 강력한 힘", "↓", "시간을 낭비하지 않고 가치 있는 아웃풋을 뽑아내는 '생산적인'", "↓", "화가나 작가가 작품을 끊임없이 뽑아내는 '다작의'", "↓", "식물이 풍성한 열매를 많이 맺는 '결실이 풍부한'"],
        "logic_desc": "결과물(Product)을 활발하게 밀어내고 이끌어내는 성질을 가집니다.",
        "examples2": [
            {"en": "He was a productive writer who published 50 books.", "ko": "그는 50권의 책을 출판한 다작하는(생산적인) 작가였다."},
            {"en": "The valley has a productive soil.", "ko": "그 계곡은 결실이 풍부한(비옥한) 토양을 가지고 있다."}
        ],
        "feeling": "productive = 앞으로 끌어당겨 내는 = 효율성 있는 = 열매를 많이 맺는 = 다작하는",
        "real_tip": "반대말인 unproductive(비생산적인)와 명사형 productivity(생산성)도 함께 외워두세요.",
        "summary_flow": ["duc lead", "produce 생산하다", "productive 생산적인", "창작에 적용", "다작하는, 결실이 많은"],
        "quiz": [
            {"question": "How can I make my study time more __________?", "translation": "내 공부 시간을 어떻게 더 생산적으로 만들 수 있을까?", "answer": "productive"},
            {"question": "A __________ orchard provides fresh fruits every autumn.", "translation": "결실이 풍부한 과수원은 매년 가을 신선한 과일을 제공한다.", "answer": "productive"}
        ]
    },
    {
        "word": "random",
        "pronunciation": "RAN-duhm",
        "meaning1": "무작위의, 마구잡이의",
        "meaning2": "엉뚱한, 뜻밖의 (구어체)",
        "intro": "질서가 없음을 뜻하는 '무작위'가 일상 대화에서는 왜 '엉뚱하다'라는 뉘앙스로 바뀔까요?",
        "etymology": {
            "root1": "rand : force, speed (강한 힘, 질주)",
            "root2": "at random : 고삐 풀려 제멋대로 내달리는",
            "flow": ["방향을 정하지 않고 거세게 달리는", "규칙이나 목표 없이 내딛는", "마구잡이의, 무작위의", "논리 맥락을 벗어나 엉뚱한"]
        },
        "examples1": [
            {"en": "I simply wrote random thoughts in my notebook.", "ko": "나는 공책에 마구잡이로 떠오르는 생각들을 적었다."},
            {"en": "The numbers were chosen in a random order.", "ko": "그 숫자들은 무작위 순서로 선택되었다."},
        ],
        "transition_question": "규칙이 없다는 단어가 어떻게 \"엉뚱한\"으로 쓰이게 되었을까요?",
        "logic_flow": ["통제를 벗어나 고삐 풀린 말이 제멋대로 날뜀", "↓", "아무런 인과관계나 체계가 없음 (무작위)", "↓", "현재 나누는 대화의 흐름과 전혀 상관없는 뜬금없는 말", "↓", "엉뚱한, 뜻밖의"],
        "logic_desc": "일정한 흐름이나 통제 계획에 따르지 않고, 우연히 툭 튀어나온 상태를 뜻합니다.",
        "examples2": [
            {"en": "Some random guy came up to me on the street.", "ko": "어떤 엉뚱한(뜬금없는) 사람이 길에서 내게 다가왔다."},
            {"en": "That was a very random comment.", "ko": "그것은 정말 뜬금없는(엉뚱한) 발언이었다."}
        ],
        "feeling": "random = 제멋대로 내달려 질서가 없는 = 마구잡이의 = 맥락을 벗어난 = 뜬금없는 / 엉뚱한",
        "real_tip": "통계학 용어인 '무작위 추출(random sampling)' 등 학술적으로도 널리 쓰이는 기본 단어입니다.",
        "summary_flow": ["ran 질주하다", "at random 제멋대로 질주하는", "random 무작위의, 마구잡이의", "구어체 적용", "뜬금없는, 엉뚱한"],
        "quiz": [
            {"question": "The computer generates a __________ password every time.", "translation": "컴퓨터는 매번 무작위의 비밀번호를 생성한다.", "answer": "random"},
            {"question": "It was just a __________ thought, don't take it seriously.", "translation": "그것은 그저 뜬금없는(마구잡이의) 생각이었으니 진지하게 받아들이지 마라.", "answer": "random"}
        ]
    },
    {
        "word": "assignment",
        "pronunciation": "uh-SYN-muhnt",
        "meaning1": "과제, 임무",
        "meaning2": "배정, 할당 (권리 이전)",
        "intro": "학생들이 가장 싫어하는 '숙제(과제)'가 왜 비즈니스나 법률에서는 '배정, 양도'가 될까요?",
        "etymology": {
            "root1": "ad- : to (~에게)",
            "root2": "sign : mark, seal (표시하다, 서명하다)",
            "flow": ["특정인에게 대상을 표시하여 넘겨주다", "할 일을 지정해서 맡기다", "숙제, 과제, 임무", "돈이나 권리를 특정 몫으로 할당/배정해 줌"]
        },
        "examples1": [
            {"en": "I need to finish the math assignment today.", "ko": "나는 오늘 수학 과제를 끝내야 한다."},
            {"en": "Her next assignment is to run the branch office.", "ko": "그녀의 다음 임무는 지점을 운영하는 것이다."}
        ],
        "transition_question": "나에게 할당된 숙제가 어떻게 권리적 \"배정\"으로 이어질까요?",
        "logic_flow": ["특정 대상의 이름을 콕 짚어 표시(sign)하여 일을 넘겨줌", "↓", "개인에게 부과된 '할 일(과제)'", "↓", "회사의 자원이나 부서 배치를 각 사람의 몫으로 짚어줌", "↓", "자산이나 방의 '배정(할당)', 혹은 특허권 등의 '양도(소유권 이전)'"],
        "logic_desc": "주체가 대상을 지정하여(sign to) 특정 몫이나 의무를 건네주는 행위를 일컫습니다.",
        "examples2": [
            {"en": "The assignment of rooms was done alphabetically.", "ko": "방 배정은 알파벳 순으로 이루어졌다."},
            {"en": "They signed the assignment of patent rights.", "ko": "그들은 특허권 양도 계약서에 서명했다."}
        ],
        "feeling": "assignment = 특정인에게 표시하여 넘겨준 것 = 과제 = 권리나 자원의 배정 / 양도",
        "real_tip": "동사형 assign(배정하다, 부과하다)과 어사인(Assign)이라는 한글 비즈니스 용어도 자주 사용됩니다.",
        "summary_flow": ["sign 표시하다", "assign 지정하여 나누다", "assignment 부과된 과제", "자원 분배", "배정, 양도"],
        "quiz": [
            {"question": "He failed to submit his writing __________ on time.", "translation": "그는 글쓰기 과제를 제시간에 제출하지 못했다.", "answer": "assignment"},
            {"question": "The __________ of responsibilities was clear to everyone.", "translation": "책임의 배정(분담)은 모두에게 명확했다.", "answer": "assignment"}
        ]
    },
    {
        "word": "normally",
        "pronunciation": "NAWR-muhl-ee",
        "meaning1": "정상적으로, 규칙대로",
        "meaning2": "보통, 주로, 대개",
        "intro": "규칙을 뜻하는 '정상적으로'가 왜 일상에서는 단순히 '보통은'이라는 뜻으로 쓰일까요?",
        "etymology": {
            "root1": "norm : rule, standard (규칙, 기준)",
            "root2": "-ally : 부사 접사",
            "flow": ["정해진 기준과 규칙에 딱 맞추어", "이상 없이 정상적으로 작동하여", "일반적인 상황의 척도에 따라", "보통, 대개"]
        },
        "examples1": [
            {"en": "The machine is now operating normally.", "ko": "그 기계는 이제 정상적으로 작동하고 있다."},
            {"en": "Treat people normally and they will respond well.", "ko": "사람들을 평범하고 규칙대로 대하면 그들도 잘 반응할 것이다."}
        ],
        "transition_question": "정상적인 상태가 어떻게 일상의 빈도를 뜻하는 \"보통\"이 되었을까요?",
        "logic_flow": ["사회가 정해놓은 규칙과 잣대(norm)", "↓", "비정상이 아닌 궤도 위의 '정상적으로'", "↓", "기준치에서 벗어나지 않은 평범한 상태", "↓", "특별한 일이 없는 10번 중 8~9번의 일반적 조건", "↓", "보통, 대개"],
        "logic_desc": "일반적인 규칙이나 궤도(Norm)에서 벗어나지 않은 보편적 상황을 지칭합니다.",
        "examples2": [
            {"en": "I normally start by writing about today's tasks.", "ko": "나는 보통 오늘 해야 할 일을 적는 것으로 시작한다."},
            {"en": "Normally, we don't allow pets in this building.", "ko": "대개는 이 건물에 반려동물 동반을 허용하지 않는다."}
        ],
        "feeling": "normally = 기준에 맞아 엇나감이 없는 = 정상적으로 = 대다수의 보편적 조건인 = 보통 / 대개",
        "real_tip": "형용사형 normal(보통의, 정상적인)의 반대말은 abnormal(비정상적인)입니다.",
        "summary_flow": ["norm 기준", "normal 정상의, 평범한", "normally 정상적으로", "빈도수 적용", "보통, 주로"],
        "quiz": [
            {"question": "We should check if the engine is running __________.", "translation": "우리는 엔진이 정상적으로 작동하고 있는지 확인해야 한다.", "answer": "normally"},
            {"question": "I __________ wake up at 6 AM on weekdays.", "translation": "나는 보통 평일에는 아침 6시에 일어난다.", "answer": "normally"}
        ]
    },
    {
        "word": "purpose",
        "pronunciation": "PUR-puhs",
        "meaning1": "목적, 조준 (의도적 목표)",
        "meaning2": "결단력, 굳은 의지",
        "intro": "나아갈 방향을 뜻하는 '목적'에 어떻게 사람의 성격인 '결단력'이라는 뜻이 공존할까요?",
        "etymology": {
            "root1": "pro- : forward (앞에)",
            "root2": "pose : place, put (두다, 놓다)",
            "flow": ["내 시선 앞쪽에 목표물을 놓아두다", "달성하고자 하는 목적/의도", "의도를 향해 한 치의 흔들림 없이 나아가는 상태", "결단력, 의지"]
        },
        "examples1": [
            {"en": "What is the main purpose of your visit?", "ko": "당신이 방문한 주요 목적은 무엇입니까?"},
            {"en": "I have a clear sense of purpose to start the day.", "ko": "나는 하루를 시작할 명확한 목적의식을 갖고 있다."}
        ],
        "transition_question": "눈앞에 놓아둔 목표가 어떻게 사람의 내적 \"의지\"로 해석될까요?",
        "logic_flow": ["내 눈앞(pro)에 표적처럼 과녁을 가져다 놓음(pose)", "↓", "마음속으로 지향하는 최종 과녁인 '목적'", "↓", "목적이 뚜렷하여 다른 곳으로 한눈을 팔지 않는 태도", "↓", "목적의식에서 우러나오는 굳은 의지와 결단력"],
        "logic_desc": "의도와 표적이 확실하여 헛되이 흩어지지 않는 강인한 집중력을 보여줍니다.",
        "examples2": [
            {"en": "He walked with a sense of purpose.", "ko": "그는 결단력(목적의식) 있는 걸음걸이로 걸어갔다."},
            {"en": "A man of purpose never gives up easily.", "ko": "굳은 의지(결단력)를 가진 사람은 쉽게 포기하지 않는다."}
        ],
        "feeling": "purpose = 시선 앞에 놓은 표적 = 달성할 목적 = 과녁을 향해 나아가는 단호함 = 결단력 / 의지",
        "real_tip": "부사구 'on purpose'는 '고의로, 의도적으로(deliberately)'라는 매우 중요한 시험 빈출 표현입니다.",
        "summary_flow": ["pro 앞에", "pose 두다", "purpose 앞에 놓은 과녁(목적)", "목적의식에 충실함", "결단력, 굳은 의지"],
        "quiz": [
            {"question": "The board discussed the __________ of the new regulation.", "translation": "이사회는 새로운 규정의 목적에 대해 논의했다.", "answer": "purpose"},
            {"question": "She set out with __________, determined to succeed.", "translation": "그녀는 성공하겠다는 굳은 의지(결단력)를 가지고 출발했다.", "answer": "purpose"}
        ]
    },
    {
        "word": "relate to",
        "pronunciation": "ri-LEYT too",
        "meaning1": "~와 관련되다 (연관성)",
        "meaning2": "~에 공감하다, 이해하다",
        "intro": "A와 B를 엮는 '관련되다'가 어떻게 상대의 감정에 동요하는 '공감하다'로 쓰일까요?",
        "etymology": {
            "root1": "re- : back, again (다시)",
            "root2": "late : bring, carry (가져오다)",
            "flow": ["두 대상을 다시 가져와 서로 이어 붙이다", "서로 물리적/논리적으로 연관되다", "상대의 고통이나 이야기를 내 상황으로 끌고 와 대입하다", "~에 공감하다"]
        },
        "examples1": [
            {"en": "These data relate to the climate change.", "ko": "이 데이터들은 기후 변화와 관련이 있다."},
            {"en": "How do these two ideas relate to each other?", "ko": "이 두 아이디어는 서로 어떻게 관련되어 있습니까?"}
        ],
        "transition_question": "논리적 관련이 어떻게 감정의 통로인 \"공감\"이 되었을까요?",
        "logic_flow": ["공식(re)적으로 멀리 떨어진 두 값을 내 편으로 가져와(late) 엮음", "↓", "~와 연계하다 (관련되다)", "↓", "다른 이가 겪는 슬픔을 내 감정의 궤도로 대입해 봄", "↓", "상대의 처지가 내 일처럼 다가와 전적으로 공감함"],
        "logic_desc": "타인의 고난이나 서사를 나(Relation)의 일부분으로 끌어안아 느끼는 마음입니다.",
        "examples2": [
            {"en": "I can totally relate to these two people.", "ko": "나는 이 두 사람에게 전적으로 공감할 수 있다."},
            {"en": "Many teens relate to the main character in the movie.", "ko": "많은 십 대들이 그 영화 속 주인공에게 공감한다."}
        ],
        "feeling": "relate to = 대상을 내 쪽으로 끌어와 엮음 = 연관되다 = 남의 상황을 나와 이어붙임 = 공감하다",
        "real_tip": "명사형 relation(관계, 친척)과 relative(친척, 상대적인)도 '이어져 있는 혈연'이라는 의미 맥락입니다.",
        "summary_flow": ["late 가져오다", "relate 다시 연결하다", "relate to ~와 연관되다", "감정적 대입", "공감하다, 이해하다"],
        "quiz": [
            {"question": "The police are looking for clues that __________ the suspect.", "translation": "경찰은 용의자와 관련된 단서들을 찾고 있다.", "answer": "relate to"},
            {"question": "I can __________ your frustration; I've been there too.", "translation": "네 좌절감에 정말 공감해. 나도 그런 적이 있거든.", "answer": "relate to"}
        ]
    },
    {
        "word": "concentrate",
        "pronunciation": "KAHN-suhn-treyt",
        "meaning1": "집중하다, 주의를 모으다",
        "meaning2": "농축시키다 (액체 등)",
        "intro": "시험 볼 때의 '집중하다'와 주스 병에 써진 '농축액'이 어떻게 같은 뿌리에서 나왔을까요?",
        "etymology": {
            "root1": "con- : together (함께, 한곳에)",
            "root2": "center : center (중심점)",
            "flow": ["모든 요소를 하나의 중심점에 모아 두다", "주의와 신경을 한 초점에 쏟다 (집중하다)", "액체 속의 성분들을 중심부로 조밀하게 뭉쳐 모으다 (농축하다)"]
        },
        "examples1": [
            {"en": "It wasn't easy for me to concentrate on studying.", "ko": "나는 공부에 집중하는 것이 쉽지 않았다."},
            {"en": "You need to concentrate your mind.", "ko": "너는 정신을 집중해야 한다."}
        ],
        "transition_question": "정신을 모으는 행위가 화학적으로 어떻게 \"농축\"이 될까요?",
        "logic_flow": ["사방으로 분산되어 흩어지는 에너지를 중심(center)으로 모음(con)", "↓", "정신을 흩뜨리지 않고 과녁에 명중시키듯이 '집중함'", "↓", "화학 용액에서 물기를 빼고 유효 성분들을 중심으로 똘똘 뭉치게 함", "↓", "농도를 높이다, 농축하다"],
        "logic_desc": "밀도를 극대화하여 핵심(Center)에 모아놓은 응축 상태를 의미합니다.",
        "examples2": [
            {"en": "Orange juice can be sold as concentrate.", "ko": "오렌지 주스는 농축액 형태로 판매될 수 있다."},
            {"en": "The chemical was concentrated in the tissue.", "ko": "그 화학 물질은 조직 내에 농축되었다(밀집되었다)."}
        ],
        "feeling": "concentrate = 사방의 에너지를 한 중심으로 모음 = 집중하다 = 성분을 조밀하게 응축함 = 농축하다",
        "real_tip": "반대말처럼 쓰이는 '분산시키다, 흩뿌리다'는 disperse나 distract(주의를 돌리다)를 씁니다.",
        "summary_flow": ["center 중심", "concentrate 한 중심으로 모으다", "정신력 모으기 (집중하다)", "물질적 밀도 모으기", "농축시키다"],
        "quiz": [
            {"question": "Please quiet down; I can't __________.", "translation": "조용히 해 줘. 집중할 수가 없어.", "answer": "concentrate"},
            {"question": "This soup is too salty; they used a __________ broth.", "translation": "이 스프는 너무 짜다. 그들이 농축된 육수를 썼나 봐.", "answer": "concentrate"}
        ]
    },
    {
        "word": "emotional",
        "pronunciation": "i-MOH-shuh-nuhl",
        "meaning1": "감정의, 정서적인 (이성의 반대)",
        "meaning2": "감정이 격해진, 감상적인",
        "intro": "단순한 '정서적'이라는 말과 '너 왜 이렇게 감정적이니?'라고 화낼 때의 뜻 차이를 구별해 볼까요?",
        "etymology": {
            "root1": "e- : out (밖으로)",
            "root2": "motion : move (움직임, 요동)",
            "flow": ["내면의 고요함이 깨져 밖으로 요동치며 나오다", "마음의 정서 및 감정 상태의", "감정이 파도처럼 크게 밖으로 솟구친 상태", "감정 과잉의, 격앙된"]
        },
        "examples1": [
            {"en": "Writing helped relieve my emotional tension.", "ko": "글쓰기는 나의 정서적(감정적) 긴장을 완화하는 데 도움을 주었다."},
            {"en": "Music has a strong emotional impact on us.", "ko": "음악은 우리에게 강한 정서적 영향을 미친다."}
        ],
        "transition_question": "순수한 마음의 상태가 어떻게 \"감정 격앙\"이라는 뜻으로 쓰일까요?",
        "logic_flow": ["가만히 있던 마음이 요동쳐 밖(e)으로 거세게 움직임(motion)", "↓", "뇌와 가슴의 작동인 '정서적인'", "↓", "그 움직임의 진폭이 너무 커져 통제력을 잃음", "↓", "이성적 제어를 벗어나 쉽게 울컥하고 격해지는 '감정적인' 상태"],
        "logic_desc": "잔잔한 이성의 물결에 감정의 큰 에너지가 유입되어 출렁이는 기폭을 뜻합니다.",
        "examples2": [
            {"en": "She became emotional when talking about her dog.", "ko": "그녀는 반려견에 대해 이야기할 때 감정이 격해졌다."},
            {"en": "Don't make emotional decisions in anger.", "ko": "화가 났을 때 감정적인 결정을 내리지 마라."}
        ],
        "feeling": "emotional = 마음이 흔들려 밖으로 요동치는 = 정서의 = 통제를 잃어 크게 출렁이는 = 감상적인 / 격앙된",
        "real_tip": "명사형 emotion(감정)과 이성을 뜻하는 reason(이성), rational(이성적인)을 대비하여 공부하면 유익합니다.",
        "summary_flow": ["move 움직이다", "emotion 마음이 요동침", "emotional 정서적인", "요동이 지나침", "격앙된, 감상적인"],
        "quiz": [
            {"question": "He needs some __________ support during this tough time.", "translation": "그는 이 힘든 시기에 약간의 정서적인 지지가 필요하다.", "answer": "emotional"},
            {"question": "The actor gave a highly __________ performance.", "translation": "그 배우는 매우 감정이 격해진(감상적인) 연기를 선보였다.", "answer": "emotional"}
        ]
    },
    {
        "word": "tension",
        "pronunciation": "TEN-shuhn",
        "meaning1": "긴장, 팽팽함 (심리/물리)",
        "meaning2": "전압, 전기적 압력 (물리)",
        "intro": "마음이 조여오는 '긴장'이 왜 물리학이나 공학에서는 '전기적 압력(전압)'이 될까요?",
        "etymology": {
            "root1": "tens- : stretch (팽팽하게 당기다)",
            "root2": "-ion : 상태를 뜻하는 명사 접사",
            "flow": ["끈이나 밧줄을 양쪽에서 세게 잡아당긴 상태", "마음의 끈이 팽팽하게 조여지는 긴장", "전선 내부에서 전자를 강하게 밀어당기는 힘", "전기 전압"]
        },
        "examples1": [
            {"en": "Writing is good for relieving mental tension.", "ko": "글쓰기는 정신적 긴장을 완화하는 데 좋다."},
            {"en": "There is a growing tension between the two countries.", "ko": "두 나라 사이에 팽팽한 긴장감이 고조되고 있다."}
        ],
        "transition_question": "팽팽하게 조이는 고무줄의 힘이 어떻게 \"전압\"이 될까요?",
        "logic_flow": ["양끝을 붙잡고 부러지거나 끊어지기 직전까지 쭉 잡아당김(tens)", "↓", "줄이 팽팽히 서 있어 에너지가 실린 상태 (장력, 팽팽함)", "↓", "마음의 신경망이 바짝 서 있어 조마조마한 '긴장'", "↓", "전자를 당겨 전기를 흐르게 하는 전기적 팽팽함의 세기 (전압/High tension)"],
        "logic_desc": "모든 에너지가 극도로 당겨져 조여진 팽팽한 한계 상태를 묘사합니다.",
        "examples2": [
            {"en": "High-tension cables carry electricity over long distances.", "ko": "고압선(높은 전압 케이블)은 전기를 장거리 송전한다."},
            {"en": "The structural engineer measured the tension of the wire.", "ko": "구조 엔지니어는 와이어의 장력(팽팽함)을 측정했다."}
        ],
        "feeling": "tension = 고무줄을 팽팽하게 당김 = 장력 = 마음이 조여드는 = 긴장 = 전자를 세게 당기는 = 전압",
        "real_tip": "인간관계의 갈등이나 대립 구도를 표현할 때 'racial tension(인종 갈등/긴장)'처럼 널리 응용됩니다.",
        "summary_flow": ["tendere 당기다", "tens 팽팽한 상태", "tension 장력 / 마음의 긴장", "전력 적용", "전압(High-tension)"],
        "quiz": [
            {"question": "He laughed to break the __________ in the room.", "translation": "그는 방 안의 긴장감을 깨기 위해 웃었다.", "answer": "tension"},
            {"question": "We must ensure the wire __________ is perfectly balanced.", "translation": "우리는 와이어의 장력(팽팽함)이 완벽하게 균형을 이루도록 해야 한다.", "answer": "tension"}
        ]
    },
    {
        "word": "performance",
        "pronunciation": "per-FAWR-muhns",
        "meaning1": "공연, 연주 (무대 예술)",
        "meaning2": "수행, 성적, 성능 (일의 결과)",
        "intro": "음악가의 '공연'과 학생의 '학업 성적(수행)', 기계의 '성능'이 어떻게 같은 단어일까요?",
        "etymology": {
            "root1": "per- : thoroughly (완전히, 끝까지)",
            "root2": "form : shape, carry out (형태를 갖추다, 완성하다)",
            "flow": ["요청받은 명령이나 설계를 완전히 형태를 갖추어 끝마치다", "약속된 책임을 완수해 낸 결과물", "성적, 수행력, 기계 성능", "무대 위에서 예술적 완성을 직접 행하여 보여줌", "공연, 연주"]
        },
        "examples1": [
            {"en": "I watched a live music performance last night.", "ko": "나는 어젯밤 라이브 음악 공연을 관람했다."},
            {"en": "The actor's performance was outstanding.", "ko": "그 배우의 연기(공연)는 뛰어났다."}
        ],
        "transition_question": "무대 위의 연기가 어떻게 나의 \"학업 성적\"이나 컴퓨터 \"성능\"이 될까요?",
        "logic_flow": ["주어진 기획이나 명령을 완전하게(per) 형태(form)를 지어 끝냄", "↓", "의무를 완성하는 것 (수행, 이행)", "↓", "학생이 공부를 해낸 최종 완성도 (학업 성적, 학업 수행)", "↓", "컴퓨터나 자동차가 스펙대로 완전히 일을 해내는 퀄리티 (성능)"],
        "logic_desc": "머릿속 계획이나 설계를 실제 결과(Form)로 온전히 구현해 낸 종합적인 지표를 가리킵니다.",
        "examples2": [
            {"en": "Her schoolwork performance has improved.", "ko": "그녀의 학업 성적(수행력)이 향상되었다."},
            {"en": "We need to test the performance of the new software.", "ko": "우리는 새로운 소프트웨어의 성능을 테스트해야 한다."}
        ],
        "feeling": "performance = 완벽하게 형태를 갖춰 이행함 = 수행 / 실적 = 무대 위에서 이행해 보임 = 연주 / 공연",
        "real_tip": "내신 평가에서 흔히 말하는 '수행평가'의 정식 영어 표현이 바로 'performance assessment'입니다.",
        "summary_flow": ["form 형태", "perform 끝까지 형태를 만들다(이행하다)", "performance 수행 / 연주", "학업 및 제품 적용", "성적, 성능"],
        "quiz": [
            {"question": "The company's financial __________ was excellent this year.", "translation": "올해 그 회사의 재무적 실적(성적)은 훌륭했다.", "answer": "performance"},
            {"question": "The audience applauded after the dance __________.", "translation": "관객들은 무용 공연이 끝난 후 박수를 보냈다.", "answer": "performance"}
        ]
    },
    {
        "word": "vague",
        "pronunciation": "veyg",
        "meaning1": "희미한, 막연한 (추상적)",
        "meaning2": "방랑하는, 정처 없는 (정신적)",
        "intro": "기억이 흐릿할 때 쓰는 '막연한'에 왜 정처 없이 방황한다는 뉘앙스가 있을까요?",
        "etymology": {
            "root1": "vag- : wander (정처 없이 헤매다, 방랑하다)",
            "root2": "-ue : 형용사 접사",
            "flow": ["한곳에 고정되지 않고 정처 없이 돌아다니다", "초점이 고정되지 않고 공중에 흩어지다", "희미한, 막연한", "논리가 방랑하여 모호한"]
        },
        "examples1": [
            {"en": "Gradually, vague ideas became clear plans.", "ko": "점차 막연한 아이디어들은 명확한 계획이 되었다."},
            {"en": "I have a vague memory of that place.", "ko": "나는 그곳에 대한 희미한 기억이 있다."}
        ],
        "transition_question": "방랑하는 헤맴이 어떻게 \"흐릿함\"이 되었을까요?",
        "logic_flow": ["초점이 맞춰지지 않고 사방으로 헤매며 떠돎(vag)", "↓", "형체가 뚜렷하지 않고 공중에 흩어진 '희미한'", "↓", "생각이나 목표가 구체적이지 않고 공중에 붕 뜬 '막연한'", "↓", "의견이 방황하여 갈피를 못 잡음"],
        "logic_desc": "한 점에 머물러 정의되지 못하고 주변을 맴도는 모호한 상태를 뜻합니다.",
        "examples2": [
            {"en": "She gave a vague answer to my question.", "ko": "그녀는 내 질문에 애매모호한(막연한) 답변을 했다."},
            {"en": "He had a vague feeling that something was wrong.", "ko": "그는 무언가 잘못되었다는 모호한 느낌을 받았다."}
        ],
        "feeling": "vague = 고정되지 않고 방랑하여 떠도는 = 희미한 = 모호한 / 막연한",
        "real_tip": "방랑하는 사람을 뜻하는 vagabond(방랑자)나 vagrant(부랑자)도 같은 vag-(떠돌다) 어원에서 나왔습니다.",
        "summary_flow": ["vagus 방랑하는", "vague 헤매는, 흐릿한", "vague memory 희미한 기억", "추상적 구체성 부족", "막연한 계획"],
        "quiz": [
            {"question": "The candidate's promises were too __________ to be trusted.", "translation": "그 후보의 공약들은 신뢰하기에 너무 막연했다.", "answer": "vague"},
            {"question": "I only have a __________ outline of the project so far.", "translation": "나는 아직 그 프로젝트에 대한 막연한(대략적인) 개요만 가지고 있다.", "answer": "vague"}
        ]
    },
    {
        "word": "drive",
        "pronunciation": "dryv",
        "meaning1": "운전하다, 몰아가다 (물리적)",
        "meaning2": "추진력, 강한 충동 (정신적)",
        "intro": "자동차 '드라이브'라는 단어에 왜 내 안을 뒤흔드는 '추진력'이라는 강한 힘의 뜻이 있을까요?",
        "etymology": {
            "root1": "drive : push, force to move (세게 밀어대다, 쫓아내다)",
            "root2": "noun / verb : 명사/동사 공통",
            "flow": ["가축이나 차를 앞으로 세게 몰아가다", "운전하다, 몰다", "마음속에서 무언가를 성취하라고 등을 떠미는 내적 엔진", "추진력, 욕구, 충동"]
        },
        "examples1": [
            {"en": "She learned to drive a car last year.", "ko": "그녀는 작년에 운전하는 법을 배웠다."},
            {"en": "The wind will drive the clouds away.", "ko": "바람이 구름을 몰아낼 것이다."}
        ],
        "transition_question": "몰아붙이는 운전이 어떻게 내면의 \"추진력\"이 될까요?",
        "logic_flow": ["앞에 있는 대상을 세게 채찍질하여 밖으로 몰아붙임(drive)", "↓", "마차를 몰고 나아가는 '운전하다'", "↓", "목표를 향해 나를 가만두지 않고 채찍질하여 몰아가는 내적 힘", "↓", "포기하지 않게 등을 떠미는 의지(추진력, 충동)"],
        "logic_desc": "행동을 개시하도록 뒤에서 강하게 밀어붙이는 에너지(Drive)를 말합니다.",
        "examples2": [
            {"en": "My morning pages have given me the drive to achieve these aims.", "ko": "나의 모닝페이지는 나에게 이런 목표들을 달성할 추진력을 주었다."},
            {"en": "Hunger is a basic survival drive.", "ko": "식욕은 기본적인 생존 충동(욕구)이다."}
        ],
        "feeling": "drive = 앞으로 세게 몰아댐 = 운전하다 = 목표를 향해 나를 등 떠미는 힘 = 추진력 / 욕구",
        "real_tip": "비즈니스에서는 '판매 촉진 캠페인'을 'sales drive'라고 표현하기도 합니다.",
        "summary_flow": ["drive 몰다", "driver 운전사", "driving force 추진력(동력)", "심리적 내재화", "욕구, 추진력"],
        "quiz": [
            {"question": "You need to find a new __________ to keep going.", "translation": "계속 전진하려면 새로운 추진력(동기)을 찾아야 한다.", "answer": "drive"},
            {"question": "He has a strong __________ to succeed in business.", "translation": "그는 사업에서 성공하고자 하는 강한 추진력(의지)을 갖고 있다.", "answer": "drive"}
        ]
    },
    {
        "word": "achieve",
        "pronunciation": "uh-CHEEV",
        "meaning1": "성취하다, 달성하다",
        "meaning2": "정상에 도달하다, 해내다",
        "intro": "꿈을 '성취하다'라는 단어의 어원 속에 '머리(꼭대기)'라는 개념이 들어있는 사실을 아시나요?",
        "etymology": {
            "root1": "a- (ad-) : to (~로, 향하여)",
            "root2": "chieve (chef) : head, top (우두머리, 머리, 꼭대기)",
            "flow": ["일의 꼭대기(머리)를 향해 올라가다", "정상에 도달하여 마침표를 찍다", "성취하다, 달성하다", "성공적으로 끝맺다"]
        },
        "examples1": [
            {"en": "Morning pages gave me the ideas to achieve these aims.", "ko": "모닝페이지는 나에게 이런 목표들을 달성할 아이디어를 주었다."},
            {"en": "You can achieve anything if you work hard.", "ko": "열심히 노력하면 무엇이든 성취할 수 있다."}
        ],
        "transition_question": "머리에 닿는 것이 어떻게 \"성취\"가 되었을까요?",
        "logic_flow": ["어떤 임무나 산의 맨 꼭대기(chef/chieve)를 향해(ad) 감", "↓", "끝단인 머리에 발을 디뎌 정상 정복에 성공함", "↓", "목표의 최종 결승선에 도달하여 승리를 얻어냄", "↓", "성취하다, 완수하다"],
        "logic_desc": "일의 꼭대기(머리)를 완성하여 마침내 정상을 밟았음을 의미합니다.",
        "examples2": [
            {"en": "The mountain climbers finally achieved the summit.", "ko": "등반가들은 마침내 정상 정복을 이루어 냈다(도달했다)."},
            {"en": "He achieved notoriety for his wild behavior.", "ko": "그는 난폭한 행동으로 악명(정점)을 얻었다."}
        ],
        "feeling": "achieve = 끝단(머리)을 향해 감 = 정상에 도달함 = 목표를 성취하다 / 완수하다",
        "real_tip": "프랑스 요리사인 '셰프(chef)'도 주방의 '머리(우두머리)'를 가리키는 동일한 어원입니다.",
        "summary_flow": ["chef 머리, 우두머리", "achieve 끝머리에 도달하다", "정상을 밟다", "목표 달성", "성취하다"],
        "quiz": [
            {"question": "How did you manage to __________ such high sales?", "translation": "어떻게 그렇게 높은 매출을 달성해 내셨나요?", "answer": "achieve"},
            {"question": "They worked together to __________ their common goals.", "translation": "그들은 공동의 목표를 달성하기 위해 함께 노력했다.", "answer": "achieve"}
        ]
    },
    {
        "word": "ultimate",
        "pronunciation": "UHL-tuh-mit",
        "meaning1": "궁극적인, 최종의 (본질적)",
        "meaning2": "최고의, 극치의 (끝판왕)",
        "intro": "마지막을 뜻하는 '최종'이 어떻게 '최고의(끝판왕)'라는 뜻으로 격상되었을까요?",
        "etymology": {
            "root1": "ultim- : last, extreme (가장 먼, 마지막, 극단의)",
            "root2": "-ate : 형용사 접사",
            "flow": ["가장 끝단에 위치하여 더 나아갈 수 없는", "마지막 단계의, 최종의", "모든 표면 아래에 숨어있는 본질적인 (궁극의)", "최고의 (끝판왕)"]
        },
        "examples1": [
            {"en": "The ultimate aim is to improve your mental health.", "ko": "궁극적인 목표는 당신의 정신 건강을 개선하는 것이다."},
            {"en": "Death is the ultimate reality for everyone.", "ko": "죽음은 모두에게 최종적인(최후의) 현실이다."}
        ],
        "transition_question": "마지막 한계의 단어가 어떻게 \"최고\"라는 극찬의 뜻이 될까요?",
        "logic_flow": ["더 이상 뒤로 갈 수 없는 가장 멀고 마지막(ultim) 지점", "↓", "과정의 마침표인 '최종의'", "↓", "질적으로 가치의 가장 최상단 끝에 올라서 있음", "↓", "더 이상 높은 수준이 없는 '최고의, 끝판왕'"],
        "logic_desc": "마지막 끝판 단계에 서서 더 나아갈 여지 없이 완결된 상태를 보여줍니다.",
        "examples2": [
            {"en": "This car is the ultimate driving machine.", "ko": "이 차는 최고의(극치의) 주행용 머신이다."},
            {"en": "She achieved the ultimate success in her career.", "ko": "그녀는 커리어에서 최고의 성공을 거두었다."}
        ],
        "feeling": "ultimate = 가장 마지막인 = 최종의 = 더 올라갈 수 없는 정상의 = 궁극의 / 최고의",
        "real_tip": "마지막 경고나 최종 제안서를 뜻할 때 'ultimatum(최후통첩)'이라는 단어로 사용합니다.",
        "summary_flow": ["ultra 저 멀리", "ultim 가장 먼 최후의", "ultimate 최종적인 / 궁극적인", "가치 극대화", "최고의(끝판왕)"],
        "quiz": [
            {"question": "We must discover the __________ truth behind this mystery.", "translation": "우리는 이 미스터리 배후의 궁극적인 진실을 발견해야 한다.", "answer": "ultimate"},
            {"question": "This luxury hotel is the __________ in comfort.", "translation": "이 고급 호텔은 안락함의 극치(최고봉)를 선사한다.", "answer": "ultimate"}
        ]
    },
    {
        "word": "repetition",
        "pronunciation": "rep-uh-TISH-uhn",
        "meaning1": "반복, 되풀이 (행동)",
        "meaning2": "암송, 모방 (기억)",
        "intro": "같은 행동의 '반복'이 왜 머릿속으로 외워 읊조리는 '암송'으로 이어질까요?",
        "etymology": {
            "root1": "re- : again (다시)",
            "root2": "pet- : seek, attack (구하다, 달려가다, 청하다)",
            "flow": ["목표를 향해 다시 나아가 달려가다", "같은 행동을 몇 번이고 되풀이하여 구하다", "반복", "머리로 다시 가기 위해 읊조림", "암송"]
        },
        "examples1": [
            {"en": "A habit is formed through repetition.", "ko": "습관은 반복을 통해 형성된다."},
            {"en": "The job was boring due to constant repetition.", "ko": "그 일은 끊임없는 반복 때문에 지루했다."}
        ],
        "transition_question": "행동의 반복이 어떻게 머리 쓰는 \"암송\"이 되었을까요?",
        "logic_flow": ["원점으로 다시(re) 돌아가 목표를 세게 추구함(pet)", "↓", "같은 패턴을 여러 차례 되풀이하는 '반복'", "↓", "텍스트를 암기하기 위해 입으로 계속 다시 찾아내는 행위", "↓", "시나 구절을 큰 소리로 외우는 '암송'"],
        "logic_desc": "동일한 지점을 다시 시도하여 뇌나 손에 각인시키는 행위를 가리킵니다.",
        "examples2": [
            {"en": "She learned the poem by simple repetition.", "ko": "그녀는 단순한 암송(되풀이 읽기)을 통해 그 시를 외웠다."},
            {"en": "We want to avoid a repetition of past mistakes.", "ko": "우리는 과거 실수의 되풀이(반복)를 피하고 싶다."}
        ],
        "feeling": "repetition = 다시 향해 나아감 = 반복 = 기억을 되찾으려 되풀이함 = 암송 / 복습",
        "real_tip": "동사형 repeat(반복하다)와 형용사형 repetitive(반복적인, 지루한)도 꼭 암기해 두어야 할 필수 단어입니다.",
        "summary_flow": ["petere 나아가다, 청하다", "repeat 다시 요구하다/되풀이하다", "repetition 행동의 반복", "기억 훈련 적용", "암송, 되풀이"],
        "quiz": [
            {"question": "Learning a language requires continuous __________.", "translation": "언어를 배우는 것은 지속적인 반복을 요구한다.", "answer": "repetition"},
            {"question": "He gave a perfect __________ of the script.", "translation": "그는 대본을 한 치의 오차 없이 완벽하게 암송(재현)했다.", "answer": "repetition"}
        ]
    },
    {
        "word": "specific",
        "pronunciation": "spi-SIF-ik",
        "meaning1": "구체적인, 명확한 (자세한)",
        "meaning2": "고유한, 특유의 (특수한)",
        "intro": "자세하게 적는 '구체적인'에 왜 특정인에게만 속한다는 '고유한'의 뜻이 들어있을까요?",
        "etymology": {
            "root1": "speci : kind, look (종류, 분류, 외관)",
            "root2": "fic : make (만들다, 규정하다)",
            "flow": ["외형을 구별해 콕 짚어 종류로 만들다", "흐리멍덩하지 않고 또렷하게 구분 짓다", "구체적인, 명확한", "특정 분류에만 딱 적용되는 고유한/특유의"]
        },
        "examples1": [
            {"en": "Make your goal specific and clear.", "ko": "당신의 목표를 구체적이고 명확하게 만드세요."},
            {"en": "Can you be more specific about the plan?", "ko": "그 계획에 대해 좀 더 구체적으로 말씀해 주시겠습니까?"}
        ],
        "transition_question": "구분 지어 명확한 것이 어떻게 \"고유함\"으로 연결될까요?",
        "logic_flow": ["사물의 외관상 종류(speci)를 정확하게 따로 떼어 만듦(fic)", "↓", "포괄적이지 않고 콕 짚어서 지시함 (구체적인)", "↓", "그 특정 종류에만 배타적으로 해당되는 고유한 성질", "↓", "이 지역이나 생물 특유의 '고유한'"],
        "logic_desc": "다른 대다수와 구분되도록 고유한 외관의 틀을 부여하여 특정화했음을 뜻합니다.",
        "examples2": [
            {"en": "This disease is specific to tropical areas.", "ko": "이 질병은 열대 지방에만 고유하게(특유하게) 나타난다."},
            {"en": "Every species has its own specific behavior.", "ko": "모든 종은 자신만의 특유한 행동을 가지고 있다."}
        ],
        "feeling": "specific = 종류별로 칼같이 나눠 만든 = 구체적인 = 그 종류에만 딱 할당된 = 고유한 / 특유의",
        "real_tip": "명사형 species는 '생물학적 종'을 뜻하며, specify는 '명문화하다, 명시하다'라는 동사입니다.",
        "summary_flow": ["specere 보다", "species 눈에 보이는 종류", "specific 종류별로 콕 집어 만든", "구체적인", "해당 종류 고유의"],
        "quiz": [
            {"question": "I need __________ instructions on how to install this.", "translation": "이것을 설치하는 방법에 대한 구체적인 설명이 필요하다.", "answer": "specific"},
            {"question": "The smell is __________ to this chemical reaction.", "translation": "그 냄새는 이 화학 반응 특유의(고유의) 것이다.", "answer": "specific"}
        ]
    },
    {
        "word": "meditate",
        "pronunciation": "MED-i-teyt",
        "meaning1": "명상하다, 묵상하다 (종교/마음)",
        "meaning2": "계획을 꾀하다, 계획하다 (비즈니스)",
        "intro": "조용히 눈 감고 하는 '명상하다'가 옛 영어와 격식체에서는 어떻게 '일의 성공을 꾀하다'가 될까요?",
        "etymology": {
            "root1": "med- : measure, consider (척도를 재다, 깊이 생각하다)",
            "root2": "-ate : 동사 접사",
            "flow": ["마음속으로 깊이 치수와 척도를 재어 보다", "고요히 내면을 들여다보며 명상하다", "어떤 일을 머릿속으로 깊이 저울질하며 준비하다", "계획을 꾀하다"]
        },
        "examples1": [
            {"en": "I'll meditate for five minutes each day.", "ko": "나는 매일 5분씩 명상할 것이다."},
            {"en": "She likes to meditate in a quiet room.", "ko": "그녀는 조용한 방에서 명상하는 것을 좋아한다."}
        ],
        "transition_question": "조용히 생각하는 것이 어떻게 머리 굴리는 \"꾀하다\"가 되었을까요?",
        "logic_flow": ["일의 깊이와 모양을 마음의 자로 가만히 재어(med) 봄", "↓", "자아 성찰을 위해 차분히 뇌파를 내리는 '명상하다'", "↓", "어떤 구상이나 큰 음모를 마음속으로 깊이 저울질하며 설계함", "↓", "성공을 꾀하다, 기획하다 (ex. meditate a revenge - 복수를 꾀하다)"],
        "logic_desc": "충동적으로 하지 않고, 마음속 자로 치수를 깊게 재어가며 시뮬레이션함을 의미합니다.",
        "examples2": [
            {"en": "They meditated a quick takeover of the rival company.", "ko": "그들은 경쟁사의 신속한 인수를 꾀했다(머릿속으로 계획했다)."},
            {"en": "He meditated on his past mistakes before deciding.", "ko": "그는 결정하기 전에 자신의 지난 실수를 깊이 묵상했다(저울질했다)."}
        ],
        "feeling": "meditate = 내면의 깊이를 재어 봄 = 명상하다 = 설계 치수를 꼼꼼히 재어 봄 = 계획하다 / 꾀하다",
        "real_tip": "의학을 뜻하는 medicine도 '몸의 척도를 재어 균형을 맞춰주는 것'에서 나온 동일 어원 패밀리입니다.",
        "summary_flow": ["med 척도를 재다", "meditate 자로 깊이 재다", "마음 재기 (명상하다)", "비즈니스 기획 재기", "계획을 꾀하다"],
        "quiz": [
            {"question": "He spent years in the temple to learn how to __________.", "translation": "그는 명상하는 법을 배우기 위해 사원에서 수년을 보냈다.", "answer": "meditate"},
            {"question": "They are __________ a new expansion project.", "translation": "그들은 새로운 확장 프로젝트를 계획하고 있다(꾀하고 있다).", "answer": "meditating"}
        ]
    },
    {
        "word": "combine",
        "pronunciation": "kuhm-BYN",
        "meaning1": "결합하다, 병합하다 (동사)",
        "meaning2": "콤바인 (수확용 농기계, 명사)",
        "intro": "화학적 '결합'을 뜻하는 단어가 농촌에서 타고 다니는 커다란 '콤바인' 기계와 어떻게 연결될까요?",
        "etymology": {
            "root1": "com- : together (함께)",
            "root2": "bin : two by two (둘씩, 쌍으로)",
            "flow": ["둘(two)을 하나로 함께 묶다", "여러 요소를 섞어 하나로 결합하다", "추수와 탈곡 두 가지 작업을 하나로 합쳐서 하는 기계", "콤바인"]
        },
        "examples1": [
            {"en": "This works better if you combine your habits.", "ko": "이것은 당신의 습관들을 결합하면 훨씬 더 효과가 있다."},
            {"en": "Hydrogen and oxygen combine to form water.", "ko": "수소와 산소는 결합하여 물을 형성한다."}
        ],
        "transition_question": "두 개의 결합이 어떻게 시골의 거대한 \"농기계\" 이름이 되었을까요?",
        "logic_flow": ["흩어져 있는 두 개(bin)를 붙잡아 하나로 함께(com) 엮음", "↓", "화학적, 물리적으로 융합하는 '결합하다'", "↓", "과거에는 분리되어 수많은 일손이 필요했던 '곡식 베기'와 '낟알 털기(탈곡)'", "↓", "이 두 가지 핵심 노동을 결합하여 한 대로 해내는 다목적 수확기", "↓", "농기계 콤바인"],
        "logic_desc": "두 개 이상의 기능이나 물질을 묶어 시너지를 창출하는 개념입니다.",
        "examples2": [
            {"en": "The farmer drove the combine through the wheat field.", "ko": "농부는 밀밭을 가로질러 콤바인(수확기)을 몰았다."},
            {"en": "A combine harvester cut down the crops rapidly.", "ko": "콤바인 수확기가 작물을 빠르게 베어냈다."}
        ],
        "feeling": "combine = 둘을 함께 묶어 하나로 = 결합하다 = 베기와 털기를 결합한 기계 = 콤바인",
        "real_tip": "숫자 2를 뜻하는 binary(이진법의, 두 개로 이루어진)도 bin-(둘) 어원에서 파생되었습니다.",
        "summary_flow": ["bin 둘", "combine 둘을 함께 묶다", "결합하다", "농업 다기능 결합", "농기계 콤바인"],
        "quiz": [
            {"question": "We need to __________ our resources to win the contract.", "translation": "우리는 계약을 따내기 위해 자원을 결합해야 한다.", "answer": "combine"},
            {"question": "He serviced the __________ before the harvest season.", "translation": "그는 수확기가 시작되기 전에 콤바인을 정비했다.", "answer": "combine"}
        ]
    },
    {
        "word": "cue",
        "pronunciation": "kyoo",
        "meaning1": "무대 시작 신호 (연극/방송)",
        "meaning2": "당구 큐대 / 머리 땋은 꽁지깃",
        "intro": "신호를 뜻하는 '큐 사인을 주다'가 어떻게 당구장의 '당구 큐대'와 동음이의어일까요?",
        "etymology": {
            "root1": "cue : tail, q-sign (꼬리 / 연극 큐 사인의 약자 Q)",
            "root2": "noun : 명사",
            "flow": ["배우에게 들어올 차례를 알려주는 대본 끝자락의 꼬리표 신호", "행동을 개시하게 하는 신호, 큐", "동물의 긴 꼬리처럼 길쭉하게 뻗은 나뭇가지", "당구 큐대"]
        },
        "examples1": [
            {"en": "When your habit becomes a cue for action, it sticks.", "ko": "당신의 습관이 행동의 신호(큐)가 되면, 그것은 몸에 밴다."},
            {"en": "The actor missed his cue and stood silent.", "ko": "그 배우는 자신의 큐 사인(시작 신호)을 놓쳐 가만히 서 있었다."}
        ],
        "transition_question": "연극 시작 신호가 어떻게 당구장의 \"나무 막대기\"가 되었을까요?",
        "logic_flow": ["대본 뒷단에 꼬리(tail)처럼 붙어있는 시작 타이밍 알림 표시 Q", "↓", "행동을 유발하는 트리거인 '신호, 단서'", "↓", "동물의 꼬리(queue)처럼 얇고 길게 잘 뻗은 나무 꼬챙이", "↓", "당구공을 치는 길쭉한 막대인 '당구 큐대'"],
        "logic_desc": "길게 꼬리처럼 뒤를 잇는 표식이나 물체라는 공통의 시각적 형태에서 나왔습니다.",
        "examples2": [
            {"en": "He chalked the tip of his billiard cue.", "ko": "그는 당구 큐대 끝에 초크를 칠했다."},
            {"en": "She took a cue from her mother's style.", "ko": "그녀는 어머니의 스타일에서 힌트(실마리)를 얻었다."}
        ],
        "feeling": "cue = 꼬리표로 달아둔 알림 = 신호 / 단서 = 꼬리처럼 길쭉한 나뭇가지 = 당구 큐대",
        "real_tip": "줄을 서서 기다리는 사람들의 대기 열차를 뜻하는 queue(큐, 줄)도 같은 어원 출신입니다.",
        "summary_flow": ["queue 꼬리", "Q(quando) 언제? 타이밍 신호", "cue 무대 시작 신호", "꼬리 같은 나무 막대", "당구 큐대"],
        "quiz": [
            {"question": "The visual __________ helped the kids remember the vocabulary.", "translation": "시각적 신호(단서)는 아이들이 어휘를 기억하는 데 도움을 주었다.", "answer": "cue"},
            {"question": "He owns a custom-made 당구 __________.", "translation": "그는 주문 제작한 당구 큐대를 소유하고 있다. (힌트: cue)", "answer": "cue"}
        ]
    },
    {
        "word": "attractive",
        "pronunciation": "uh-TRAK-tiv",
        "meaning1": "매력적인, 호감이 가는 (심리)",
        "meaning2": "인력을 지닌, 잡아당기는 (물리)",
        "intro": "외모가 '매력적'이라는 말이 어떻게 물리 교과서의 '인력(당기는 힘)'과 한 단어일까요?",
        "etymology": {
            "root1": "ad- : toward (~쪽으로)",
            "root2": "tract : pull, drag (당기다, 끌다)",
            "flow": ["중심을 향해 힘껏 자기 쪽으로 끌어당기다", "물체를 잡아당기는 인력의", "사람의 눈길과 호기심을 세게 끌어당기는", "매력적인, 매혹적인"]
        },
        "examples1": [
            {"en": "Make your new habit attractive to stick to it.", "ko": "당신의 새로운 습관을 매력적으로 만들어야 몸에 붙는다."},
            {"en": "The offer was very attractive, so I accepted.", "ko": "그 제안은 매우 매력적이었기에 나는 수락했다."}
        ],
        "transition_question": "자석이 쇠를 당기는 것이 어떻게 사람이 예쁘다는 뜻이 되었을까요?",
        "logic_flow": ["대상을 내 몸 쪽(ad)으로 힘을 주어 강력하게 끌어당김(tract)", "↓", "자석이나 지구가 물체를 끌어당기는 '인력을 가진'", "↓", "이성이나 관객의 눈동자를 자석처럼 착 끌어당기는 성질", "↓", "호감이 가고 마음을 사로잡는 '매력적인'"],
        "logic_desc": "상대의 의지와 상관없이 시선과 관심을 자석(Tractor)처럼 강제로 잡아 끄는 유인력을 뜻합니다.",
        "examples2": [
            {"en": "There is an attractive force between opposite charges.", "ko": "서로 반대되는 전하 사이에는 인력(잡아당기는 힘)이 존재한다."},
            {"en": "He has an attractive personality.", "ko": "그는 매력적인 성격을 가지고 있다."}
        ],
        "feeling": "attractive = 내 쪽으로 힘껏 잡아당기는 = 인력의 = 시선을 착 끌어당기는 = 매력적인",
        "real_tip": "농촌에서 무거운 짐을 끌어당기는 트랙터(tractor)와 정신을 딴 데로 잡아당겨 흩뜨리는 산만함(distraction)도 형제 단어입니다.",
        "summary_flow": ["tract 당기다", "attract 끌어당기다", "attractive 끌어당기는 성질의", "물리적 적용(인력의)", "심리적 적용(매력적인)"],
        "quiz": [
            {"question": "She wore an __________ dress to the dinner.", "translation": "그녀는 저녁 식사 자리에 매력적인 드레스를 입고 왔다.", "answer": "attractive"},
            {"question": "Gravity is the __________ force of the earth.", "translation": "중력은 지구의 인력(잡아당기는 힘)이다.", "answer": "attractive"}
        ]
    },
    {
        "word": "useful",
        "pronunciation": "YOOS-fuhl",
        "meaning1": "유용한, 쓸모가 있는 (사물)",
        "meaning2": "유능한, 도움이 되는 (사람)",
        "intro": "도구가 '유용하다'라는 단어가 왜 직원을 칭찬할 때는 '유능한(능력 있는)'이라는 뜻이 될까요?",
        "etymology": {
            "root1": "use : use, perform (사용하다, 부리다)",
            "root2": "-ful : full of (~로 가득 찬)",
            "flow": ["사용할 수 있는 용도로 가득 차다", "쓸모가 많아 유용하다", "함께 일할 때 손이 많이 가고 쓸데가 많아 유능하다", "도움이 되는, 유능한"]
        },
        "examples1": [
            {"en": "I find the morning pages enormously useful.", "ko": "나는 모닝페이지가 엄청나게 유용하다는 것을 알게 되었다."},
            {"en": "Here is some useful information for travelers.", "ko": "여기 여행객들을 위한 몇 가지 유용한 정보가 있다."}
        ],
        "transition_question": "도구의 쓸모가 어떻게 사람의 \"유능함\"으로 이어질까요?",
        "logic_flow": ["필요할 때 언제든 손에 쥐고 사용(use)할 가치로 가득(ful)함", "↓", "버릴 데가 없이 쓰임새가 뛰어난 '유용한'", "↓", "팀원으로서 역할을 적재적소에 잘 소화해 내는 사람", "↓", "부려먹기(쓰기)에 매우 편하고 능력 있는 '유능한, 도움이 되는'"],
        "logic_desc": "제 기능과 가치를 아낌없이 발휘하여 유의미한 가치를 창출하는 성향입니다.",
        "examples2": [
            {"en": "He is a very useful member of our research team.", "ko": "그는 우리 연구팀의 매우 유능한(도움이 되는) 일원이다."},
            {"en": "She made herself useful by cleaning the kitchen.", "ko": "그녀는 주방을 청소함으로써 스스로 쓸모 있는(도움이 되는) 사람이 되었다."}
        ],
        "feeling": "useful = 쓸 수 있는 쓰임새로 가득 찬 = 유용한 = 쓰기에 참 기특하고 든든한 = 유능한 / 도움이 되는",
        "real_tip": "use(사용)와 관련된 유용한 파생어로 usability(사용 편의성), utility(공공설비, 수도가스 등)가 있습니다.",
        "summary_flow": ["use 쓰다", "useful 쓸모가 가득 찬", "유용한 정보", "인물에 적용", "유능한, 도움 되는"],
        "quiz": [
            {"question": "Computers are __________ tools for learning.", "translation": "컴퓨터는 학습에 매우 유용한 도구이다.", "answer": "useful"},
            {"question": "Try to make yourself __________ around the office.", "translation": "사무실에서 네가 도움 되는(유능한) 사람이 되도록 노력해라.", "answer": "useful"}
        ]
    },
    {
        "word": "host",
        "pronunciation": "hohst",
        "meaning1": "주인, 진행자 (팟캐스트/파티)",
        "meaning2": "다수, 군대, 무리 (많은 수)",
        "intro": "진행자를 뜻하는 '호스트'가 왜 영어 성경이나 문학에서는 '군대, 다수'를 뜻하는 대량의 수가 될까요?",
        "etymology": {
            "root1": "host (hospes) : guest-host, stranger (손님을 대접하는 주인 / 혹은 군대, 적의 무리 hostis)",
            "root2": "noun : 명사",
            "flow": ["손님을 내 집에 모셔와 정성껏 대접하는 주인", "파티나 팟캐스트를 이끌어가는 진행자, 사회자", "대량으로 쳐들어온 외부 이방인 군대", "하늘의 수많은 군사, 다수, 무리"]
        },
        "examples1": [
            {"en": "Welcome, this is Regan, your podcast host.", "ko": "환영합니다, 저는 여러분의 팟캐스트 진행자 Regan입니다."},
            {"en": "The host greeted the guests warmly.", "ko": "주인은 손님들을 따뜻하게 맞이했다."}
        ],
        "transition_question": "대접하는 주인이 어떻게 \"무리, 군대\"가 되었을까요?",
        "logic_flow": ["손님(hospes)을 맞이하는 '주인' (호스트)", "↓", "행사나 방송을 총괄하고 안내하는 '진행자'", "↓", "역사적으로 라틴어 hostis(이방인, 적군)라는 다른 단어와 철자가 합쳐짐", "↓", "떼를 지어 몰려오는 외적의 거대한 군대", "↓", "하늘의 수많은 천사 무리(a host of angels) 및 수많은 다수"],
        "logic_desc": "두 가지 별개의 어원(환대하는 주인과 무장한 적군)이 역사적 과정을 통해 한 단어로 통합되었습니다.",
        "examples2": [
            {"en": "A host of angels appeared in the sky.", "ko": "수많은 천사 무리(군대)가 하늘에 나타났다."},
            {"en": "The project faced a host of unexpected problems.", "ko": "그 프로젝트는 수많은 예기치 못한 문제들에 직면했다."}
        ],
        "feeling": "host = 손님을 맞이하는 주인 = 사회자 / 진행자 = 떼를 지어 쳐들어온 무리 = 군대 / 다수",
        "real_tip": "a host of + 복수명사는 '수많은 ~'라는 중요한 수어로 독해 시험에 단골 출제됩니다.",
        "summary_flow": ["hospes 주인 / hostis 적군", "host 팟캐스트 진행자", "적군의 집단", "종교/문학적 확장", "수많은 무리, 군대"],
        "quiz": [
            {"question": "She is going to __________ the national talk show next week.", "translation": "그녀는 다음 주에 전국 토크쇼를 진행할(사회 볼) 예정이다.", "answer": "host"},
            {"question": "There are a __________ of reasons why we should reject this.", "translation": "우리가 이것을 거절해야 할 수많은 이유들이 있다.", "answer": "host"}
        ]
    },
    {
        "word": "overcome",
        "pronunciation": "oh-ver-KUHM",
        "meaning1": "극복하다, 이겨내다",
        "meaning2": "압도당하다, 질식당하다 (수동태)",
        "intro": "장벽을 넘어서는 '극복하다'가 왜 감정과 연계되면 '눈물이 앞을 가려 압도당하다'가 될까요?",
        "etymology": {
            "root1": "over- : above, across (장벽의 위를 건너)",
            "root2": "come : come, arrive (도달하다)",
            "flow": ["장애물의 정수리 위를 훌쩍 타고 넘어오다", "역경과 한계를 무찌르고 이겨내다, 극복하다", "거대한 감정이나 가스가 위에서 나를 덮치다", "압도당하다, 질식하다"]
        },
        "examples1": [
            {"en": "The technique was developed to help artists overcome a loss of creativity.", "ko": "이 기법은 예술가들이 창조성 상실을 극복하도록 돕기 위해 개발되었다."},
            {"en": "We must overcome our fear to win.", "ko": "우리는 승리하기 위해 두려움을 극복해야만 한다."}
        ],
        "transition_question": "내가 장벽 위를 넘어가던 주체가 어떻게 슬픔에 \"압도당할\" 수 있을까요?",
        "logic_flow": ["내 앞에 버티고 서 있는 거대한 바위산 위로(over) 훌쩍 넘어(come) 감", "↓", "난관을 누르고 지배하여 '극복하다'", "↓", "역으로 너무 큰 슬픔, 충격, 가스가 내 머리 위(over)로 쏟아져 들어옴(come)", "↓", "내 온몸이 고통이나 슬픔에 짓눌려 '압도당하다' (be overcome by)"],
        "logic_desc": "주도권이 누구에게 있느냐에 따라, 내가 장애물 위에 서면 '극복', 장애물이 내 위에 서면 '압도'가 됩니다.",
        "examples2": [
            {"en": "She was overcome with grief when she heard the news.", "ko": "그녀는 그 소식을 들었을 때 슬픔에 완전히 압도당했다(가슴이 미어졌다)."},
            {"en": "Two firefighters were overcome by thick smoke.", "ko": "소방관 두 명이 자욱한 연기에 질식당했다(압도당했다)."}
        ],
        "feeling": "overcome = 장애물 위를 뛰어넘어 밟음 = 극복하다 = 슬픔의 파도가 내 위를 덮쳐 밟음 = 압도당하다 / 질식하다",
        "real_tip": "be overcome by/with ~ 의 형태로 수동태로 쓰이면 99% '압도당하다'로 번역하면 자연스럽습니다.",
        "summary_flow": ["over 머리 위로", "come 와서 지배하다", "장애물 지배 (극복하다)", "감정이 나를 지배", "압도당하다, 질식하다"],
        "quiz": [
            {"question": "He managed to __________ his physical handicap and won the race.", "translation": "그는 신체적 장애를 극복하고 경주에서 우승했다.", "answer": "overcome"},
            {"question": "The children were __________ by curiosity.", "translation": "아이들은 호기심에 완전히 압도당했다(사로잡혔다).", "answer": "overcome"}
        ]
    },
    {
        "word": "correctly",
        "pronunciation": "kuh-REKT-lee",
        "meaning1": "올바르게, 문법적으로 정확하게",
        "meaning2": "예의 바르게, 정중하게",
        "intro": "시험 정답을 맞출 때의 '올바르게'가 왜 태도를 지적할 때는 '예의 바르게'가 될까요?",
        "etymology": {
            "root1": "con- : completely (완전히)",
            "root2": "rect : straight, right (곧게 세운, 똑바른)",
            "flow": ["굽은 곳이나 엇나감 없이 완전히 똑바르게 만들다", "틀린 부분 없이 정확하고 올바르게", "사회 규범과 법도에 똑바르게 처신하다", "예의 바르게, 단정하게"]
        },
        "examples1": [
            {"en": "Don't worry about writing correctly in the beginning.", "ko": "처음에는 올바르게(맞춤법에 맞게) 쓰는 것에 대해 걱정하지 마라."},
            {"en": "Did I pronounce your name correctly?", "ko": "내가 당신의 이름을 정확하게 발음했나요?"}
        ],
        "transition_question": "정확한 팩트가 어떻게 사람의 \"매너\"로 확장될까요?",
        "logic_flow": ["삐딱하지 않고 수직으로 하늘을 향해 완전히(con) 똑바로(rect) 세움", "↓", "왜곡이나 틀림이 없는 수학적인 '정확하게'", "↓", "행동거지나 마음가짐이 굽어 있지 않고 도덕적으로 올곧음", "↓", "어른들 앞에서 단정하고 예의 바르게 행동하는 모습"],
        "logic_desc": "도덕적, 규칙적 비뚤어짐이 전혀 없이 규범의 직선상에 서 있음을 묘사합니다.",
        "examples2": [
            {"en": "He behaved very correctly during the formal dinner.", "ko": "그는 공식 만찬 동안 매우 예의 바르게(단정하게) 행동했다."},
            {"en": "If you act correctly, no one will criticize you.", "ko": "네가 법도에 맞게(예의 바르게) 행동한다면 아무도 널 비판하지 않을 것이다."}
        ],
        "feeling": "correctly = 구부러짐 없이 똑바르게 = 정확하고 올바르게 = 행동을 바르게 처신하여 = 예의 바르게",
        "real_tip": "정치적으로 바른 말을 하는 사회 풍조를 가리켜 'PC(Political Correctness - 정치적 올바름)'라고 부릅니다.",
        "summary_flow": ["rect 똑바른", "correct 바로잡다 / 정확한", "correctly 정확하게", "행동 규범 적용", "예의 바르게, 단정하게"],
        "quiz": [
            {"question": "Please make sure the form is filled out __________.", "translation": "양식이 정확하게 작성되었는지 확인해 주세요.", "answer": "correctly"},
            {"question": "She was raised to speak and act __________ in public.", "translation": "그녀는 공공장소에서 예의 바르게 말하고 행동하도록 양육되었다.", "answer": "correctly"}
        ]
    },
    {
        "word": "exploring",
        "pronunciation": "ik-SPLAWR-ing",
        "meaning1": "탐구하는, 탐험하는 (미지 발견)",
        "meaning2": "진찰하는, 환부를 진단하는 (의학)",
        "intro": "우주나 정글을 헤매는 '탐험'이 병원에서는 어떻게 의사가 환부를 찔러 '진단'하는 행위가 될까요?",
        "etymology": {
            "root1": "ex- : out (밖으로)",
            "root2": "plor : cry out, weep (외치다, 눈물 흘리다)",
            "flow": ["소리를 질러(plor) 숲속 짐승들을 밖으로(ex) 몰아내다", "사냥터나 미지의 정글을 구석구석 뒤져 사냥하다", "미지의 영역을 샅샅이 탐험/탐구하다", "의사가 상처 속을 도구로 샅샅이 뒤져 진단하다"]
        },
        "examples1": [
            {"en": "You don't know your creative energy until you start exploring.", "ko": "당신이 탐구를 시작하기 전에는 자신의 창조적 에너지를 결코 알 수 없다."},
            {"en": "They spent the day exploring the ancient forest.", "ko": "그들은 고대 숲을 탐험하며 하루를 보냈다."}
        ],
        "transition_question": "정글의 수색이 어떻게 병원 수술실에서 사용될까요?",
        "logic_flow": ["소리를 꽥꽥 질러 숲속 구석구석의 덤불을 뒤집어 헤집음", "↓", "안 가본 미지의 땅을 샅샅이 수색하고 뒤지는 '탐험하다'", "↓", "의사가 환자의 뱃속이나 상처 구멍 안을 도구로 샅샅이 찔러보며 조사함", "↓", "환부를 면밀히 진찰함, 촉진(觸診)함"],
        "logic_desc": "보이지 않는 어두운 장소의 실체를 알아내기 위해 숨겨진 속을 샅샅이 파헤치는 행위입니다.",
        "examples2": [
            {"en": "The surgeon is exploring the wound for any metal pieces.", "ko": "외과의는 금속 파편이 있는지 상처 부위를 찔러보며 진찰(탐사)하고 있다."},
            {"en": "Exploring the internal organs was necessary before the surgery.", "ko": "수술 전 장기 내부를 정밀 진찰하는 것이 필요했다."}
        ],
        "feeling": "exploring = 소리쳐 헤집어 뒤짐 = 미지를 탐험/탐구함 = 상처 내부를 샅샅이 살펴봄 = 진찰 / 진단함",
        "real_tip": "implore는 안으로(im) 눈물을 흘리며 외치다(plore)라는 뜻에서 '애원하다, 탄원하다'라는 강력한 뜻이 됩니다.",
        "summary_flow": ["plor 소리치다", "explore 소리쳐 헤집다 (탐험하다)", "미지 탐구", "의학 수색 적용", "환부 진찰/진단"],
        "quiz": [
            {"question": "He has a passion for __________ new cultures.", "translation": "그는 새로운 문화를 탐구하는(배우는) 데 열정이 있다.", "answer": "exploring"},
            {"question": "The medical tool is used for __________ deep cavities.", "translation": "그 의료 도구는 신체의 깊은 공동(구멍)을 진찰하는 데 사용된다.", "answer": "exploring"}
        ]
    },
    {
        "word": "sticks",
        "pronunciation": "stiks",
        "meaning1": "달라붙다, 몸에 배다 (동사)",
        "meaning2": "나뭇가지, 막대기 (명사)",
        "intro": "바닥에 굴러다니는 '나뭇가지(막대기)'가 왜 동사가 되면 '달라붙다'가 될까요?",
        "etymology": {
            "root1": "stick : sharp point, pierce (뾰족한 끝, 콕 찌르다)",
            "root2": "noun / verb : 명사/동사 공통",
            "flow": ["뾰족하고 얇은 나무 막대기, 나뭇가지", "뾰족한 끝으로 찔러 벽에 고정하다", "접착제처럼 착 달라붙다, 고수하다", "습관이 끈질기게 몸에 배다"]
        },
        "examples1": [
            {"en": "Here are five ways to start a habit that really sticks.", "ko": "여기에 실제로 몸에 배는(착 달라붙는) 습관을 만드는 다섯 가지 방법이 있다."},
            {"en": "We collected dry sticks to make a campfire.", "ko": "우리는 캠프파이어를 만들기 위해 마른 나뭇가지들을 모았다."}
        ],
        "transition_question": "막대기가 어떻게 접착제처럼 \"달라붙는\" 뜻이 되었을까요?",
        "logic_flow": ["뾰족한 나뭇가지(stick) 끝으로 종이를 벽에 콕 찔러서 고정함", "↓", "고정되어 덜렁이지 않고 자리에 착 '달라붙어 있음'", "↓", "어떤 약속이나 규칙을 바꾸지 않고 끝까지 달라붙어 지킴 (고수하다)", "↓", "행동 패턴이 뇌와 몸에 착 달라붙어 떨어지지 않음 (몸에 배다)"],
        "logic_desc": "뾰족한 핀으로 찔러 박아놓은 것처럼, 자리를 이탈하지 않고 고정되어 밀착된 모습을 가리킵니다.",
        "examples2": [
            {"en": "The wet shirt sticks to his back.", "ko": "젖은 셔츠가 그의 등에 착 달라붙는다."},
            {"en": "He always sticks to his promise.", "ko": "그는 항상 자신의 약속을 고수한다(끝까지 지킨다)."}
        ],
        "feeling": "sticks = 뾰족한 막대기 = 찔러 박아 고정함 = 달라붙다 = 약속을 끝까지 지키다 = 몸에 배다",
        "real_tip": "스티커(sticker)는 뒤에 접착력이 있어 벽에 '착 달라붙는 종이'를 의미하는 가장 직관적인 단어입니다.",
        "summary_flow": ["stigo 찌르다", "stick 뾰족한 나뭇가지", "콕 찔러 박다", "달라붙다 / 약속을 고수하다", "습관이 몸에 배다"],
        "quiz": [
            {"question": "Use a calendar to make sure your routine __________.", "translation": "당신의 일과가 완전히 몸에 배도록(달라붙도록) 달력을 사용해라.", "answer": "sticks"},
            {"question": "The dog ran after the __________ I threw.", "translation": "그 개는 내가 던진 막대기(나뭇가지)를 향해 달려갔다.", "answer": "stick"}
        ]
    },
    {
        "word": "progress",
        "pronunciation": "PRAH-gres",
        "meaning1": "진행, 진전, 발전 (명사)",
        "meaning2": "전진하다, 나아가다 (동사)",
        "intro": "시간이 '흘러간다'라는 단순한 진행이 왜 사회나 학업의 '발전'이라는 뜻으로 연결될까요?",
        "etymology": {
            "root1": "pro- : forward (앞으로)",
            "root2": "gress : go, step (걷다, 한 걸음 내딛다)",
            "flow": ["앞을 향해 발걸음을 내딛다", "물리적으로 앞으로 전진하다", "시간이 지나 일의 단계가 깊어지는 진행/진전", "질적으로 개선되어가는 발전"]
        },
        "examples1": [
            {"en": "Seeing the progress gives you a sense of achievement.", "ko": "진행 상황(진전)을 보는 것은 당신에게 성취감을 준다."},
            {"en": "We are making great progress in our negotiations.", "ko": "우리는 협상에서 큰 진전(발전)을 이루고 있다."}
        ],
        "transition_question": "앞으로 걷는 행위가 어떻게 가치적 \"발전\"이 되었을까요?",
        "logic_flow": ["시선을 앞으로(pro) 두고 한 발짝 한 발짝 걸어(gress) 나감", "↓", "물리적인 전진", "↓", "프로젝트나 업무가 멈춰있지 않고 진행되어 감 (진전)", "↓", "어제보다 오늘 지식과 환경이 더 나아짐 (학업/기술의 발전)"],
        "logic_desc": "정체되지 않고 계속해서 앞 방향(Forward)을 향해 궤적을 갱신해 나가는 성질입니다.",
        "examples2": [
            {"en": "The disease is starting to progress rapidly.", "ko": "그 질병이 빠르게 진행되기(악화되기) 시작하고 있다."},
            {"en": "As the class progressed, the students grew quieter.", "ko": "수업이 진행됨에 따라 학생들은 더 차분해졌다."}
        ],
        "feeling": "progress = 앞으로 한 걸음 전진함 = 일의 진행 상황 = 질적인 향상과 발전",
        "real_tip": "반대말은 뒤로(retro) 후퇴하는 regress와 밑으로(de) 떨어지는 퇴보인 degress입니다.",
        "summary_flow": ["gradi 걷다", "pro-gress 앞으로 걸어감", "물리적 전진", "일의 단계별 진행", "기술과 문명의 발전"],
        "quiz": [
            {"question": "She is pleased with the __________ of her students.", "translation": "그녀는 학생들의 진전(학업 발전)에 흡족해한다.", "answer": "progress"},
            {"question": "Work on the new bridge is __________ slowly.", "translation": "새 교량 건설 작업은 천천히 진행되고(나아가고) 있다.", "answer": "progressing"}
        ]
    },
    {
        "word": "achievement",
        "pronunciation": "uh-CHEEV-muhnt",
        "meaning1": "업적, 성취 (객관적 도달)",
        "meaning2": "성취감 (주관적 기쁨)",
        "intro": "내가 이룩한 역사적인 '업적'과 내 가슴이 벅차오르는 '성취감'은 어떻게 한 단어로 묶일까요?",
        "etymology": {
            "root1": "achieve : reach the head (정상 꼭대기에 도달하다)",
            "root2": "-ment : 상태나 결과를 뜻하는 명사 접사",
            "flow": ["정상에 도달하여 마침표를 찍은 상태", "노력의 끝에 달성한 객관적 업적/성취", "그 도달점에 우뚝 섰을 때 내면에서 샘솟는 감정", "성취감"]
        },
        "examples1": [
            {"en": "Winning the gold medal was a great achievement.", "ko": "금메달을 딴 것은 위대한 업적(성취)이었다."},
            {"en": "This award recognizes his lifetime achievements.", "ko": "이 상은 그의 평생의 업적들을 기리는 것이다."}
        ],
        "transition_question": "눈에 보이는 결과물인 업적이 어떻게 내면의 \"성취감\"이라는 기쁨이 될까요?",
        "logic_flow": ["오랜 등반 끝에 산의 꼭대기(chef) 정상을 밟아냄", "↓", "세상 사람들이 인정하는 객관적인 성공의 열매 (성취, 업적)", "↓", "정상에 서서 아래를 굽어보며 땀방울을 씻을 때 느끼는 주관적 보람", "↓", "가슴 깊이 벅차오르는 성취감 (a sense of achievement)"],
        "logic_desc": "정점 정복의 사실(Achievement)과 그로 인해 유발되는 인간의 자부심(Sense of Achievement)을 포괄합니다.",
        "examples2": [
            {"en": "Seeing the progress gives you a sense of achievement.", "ko": "진전 상황을 보는 것은 당신에게 성취감을 준다."},
            {"en": "Completing the marathon gave him a huge feeling of achievement.", "ko": "마라톤을 완주한 것은 그에게 거대한 성취감을 안겨주었다."}
        ],
        "feeling": "achievement = 정상에 선 결실 = 성취 / 위대한 업적 = 정상 정복 시 우러나는 뿌듯함 = 성취감",
        "real_tip": "의무 교육이나 교육학에서 다루는 '학업성취도 평가'를 영어로 'achievement test'라고 부릅니다.",
        "summary_flow": ["achieve 정상에 닿다", "achievement 도달된 결과(성취)", "객관적 역사적 업적", "주관적 감정 전이", "성취감 (Sense of ~)"],
        "quiz": [
            {"question": "The new invention was a remarkable __________ in science.", "translation": "그 새로운 발명품은 과학계의 놀라운 업적(성취)이었다.", "answer": "achievement"},
            {"question": "Helping others gives me a deep sense of __________.", "translation": "타인을 돕는 것은 나에게 깊은 성취감을 준다.", "answer": "achievement"}
        ]
    },
    {
        "word": "flexible",
        "pronunciation": "FLEK-suh-buhl",
        "meaning1": "유연한, 잘 휘어지는 (물리)",
        "meaning2": "융통성 있는, 가변적인 (정신/조건)",
        "intro": "플라스틱이 잘 휘어지는 '유연함'이 왜 사람의 태도나 약속에서는 '융통성 있다'가 될까요?",
        "etymology": {
            "root1": "flex- : bend (구부리다, 꺾다)",
            "root2": "-ible : able to be (할 수 있는)",
            "flow": ["뚝 부러지지 않고 부드럽게 잘 구부릴 수 있는", "유연한, 잘 휘어지는", "원칙에 뻣뻣하게 굳어 있지 않고 생각을 잘 조율하는", "융통성 있는, 조절 가능한"]
        },
        "examples1": [
            {"en": "Rubber is a highly flexible material.", "ko": "고무는 매우 유연한(잘 휘어지는) 재질이다."},
            {"en": "You need a flexible spine to avoid injury.", "ko": "부상을 피하려면 유연한 척추가 필요하다."}
        ],
        "transition_question": "물리적 구부러짐이 어떻게 생각의 \"융통성\"이 되었을까요?",
        "logic_flow": ["강한 힘을 가해도 꺾여 부러지지 않고 유연하게 휘어짐(flex)", "↓", "부드럽고 유연함", "↓", "상황의 변화가 닥쳤을 때 고집 피우지 않고 계획을 잘 굽힘", "↓", "규정이나 약속 시간을 유연하게 조율하는 '융통성 있는, 가변적인'"],
        "logic_desc": "외부의 충격이나 상황적 압박에 부러지거나 붕괴하지 않고 부드럽게 형태를 바꾸어 적응하는 성향입니다.",
        "examples2": [
            {"en": "We need to be flexible about our travel plans.", "ko": "우리는 여행 계획에 대해 융통성을 가질(유연해질) 필요가 있다."},
            {"en": "My working hours are very flexible.", "ko": "내 근무 시간은 매우 유연하다(융통성 있게 가변적이다)."}
        ],
        "feeling": "flexible = 부러지지 않고 잘 굽혀지는 = 유연한 = 고집부리지 않고 잘 절충하는 = 융통성 있는",
        "real_tip": "반대말인 inflexible은 '뻣뻣한, 고집 센, 변경할 수 없는'이라는 강경한 뜻이 됩니다.",
        "summary_flow": ["flectere 구부리다", "flexible 휠 수 있는", "물리적 유연함", "심리적 적응성", "융통성 있는, 가변적인"],
        "quiz": [
            {"question": "The hose is made of __________ plastic.", "translation": "그 호스는 잘 휘어지는(유연한) 플라스틱으로 만들어졌다.", "answer": "flexible"},
            {"question": "A __________ approach is required when negotiating with them.", "translation": "그들과 협상할 때는 융통성 있는(유연한) 접근이 필요하다.", "answer": "flexible"}
        ]
    },
    {
        "word": "left",
        "pronunciation": "left",
        "meaning1": "왼쪽의 (방향)",
        "meaning2": "중단한, 손을 뗀 (leave off의 과거/과거분사)",
        "intro": "단순한 '왼쪽'인 이 단어가 왜 구동사 'leave off'와 만나면 '중단했다'라는 뜻이 될까요?",
        "etymology": {
            "root1": "left / leave : weak side / depart, hand over (약한 쪽 / 떠나다, 남겨두다)",
            "root2": "leave off : stop doing something (하던 행동을 떼어놓고 떠나다)",
            "flow": ["오른손에 비해 힘이 빠진 왼쪽", "물건을 제자리에 둔 채 몸만 떠나다", "하던 일에서 손을 완전히 떼다", "중단하다 -> 과거형 left off (중단했다)"]
        },
        "examples1": [
            {"en": "Take a left turn at the next corner.", "ko": "다음 모퉁이에서 좌회전(왼쪽으로 돌기)을 하세요."},
            {"en": "He writes with his left hand.", "ko": "그는 왼손으로 글을 쓴다."}
        ],
        "transition_question": "방향인 단어가 어떻게 일의 \"중단\"과 연계되어 사용될까요?",
        "logic_flow": ["원래 '약하고 무력한 쪽'을 뜻하던 고대어에서 유래한 '왼쪽(left)'", "↓", "전혀 다른 단어인 leave(남겨두다, 떠나다)의 과거형 'left'", "↓", "여기에 off(분리)를 합쳐 '하던 작업에서 완전히 손을 떼고 멀어짐' (leave off)", "↓", "잠시 중단한 지점이나 끝마친 시점", "↓", "past left off (중단했던 지점)"],
        "logic_desc": "leave(남기다)와 off(분리)가 융합된 구동사의 과거 시제 표현으로, 가던 길을 멈추고 멈춰선 자리를 뜻합니다.",
        "examples2": [
            {"en": "Just pick up where you left off.", "ko": "그저 당신이 중단했던(멈췄던) 지점부터 다시 시작하세요."},
            {"en": "We left off at page 50 last week.", "ko": "우리는 지난주에 50페이지에서 공부를 중단했다(멈췄다)."}
        ],
        "feeling": "left = 약한 방향인 왼쪽 = 떠나고 남겨둔 = 하던 일에서 완전히 떨어져 손을 뗀 = 중단한 / 멈춘",
        "real_tip": "시험과 회화에서 'pick up where we left off'는 '이전에 멈췄던 부분부터 이어서 계속하다'라는 100% 빈출 수어입니다.",
        "summary_flow": ["leave 떠나다/남겨두다", "leave off 하던 일에서 손을 떼다", "left off 손을 뗐다(중단했다)", "pick up 다시 집어들다", "중단했던 지점부터 이어서 하다"],
        "quiz": [
            {"question": "Let's start today's lesson from where we __________ last class.", "translation": "지난 수업 시간에 우리가 중단했던(left off) 부분부터 오늘 수업을 시작합시다.", "answer": "left off"},
            {"question": "She had only a few dollars __________ in her purse.", "translation": "그녀는 지갑에 단 몇 달러만 남겨져(left) 있었다.", "answer": "left"}
        ]
    }
]

output_path = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/vocab_data.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(vocab_list, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(vocab_list)} vocabulary data points and saved to {output_path}")
