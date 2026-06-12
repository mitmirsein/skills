import json
import os

vocab_list = [
    {
        "word": "incident",
        "pronunciation": "IN-suh-duhnt",
        "meaning1": "사건, 일어난 일 (물리적으로 발생한 우발적 해프닝)",
        "meaning2": "갈등, 부차적 마찰 (추상적 분쟁과 대립)",
        "intro": "하늘에서 뚝 '떨어지는' 이미지가 어떻게 우리 삶을 흔드는 '사건'과 '갈등'이 되었을까요?",
        "etymology": {
            "root1": "in- (L. in- : upon / 위에, 안으로)",
            "root2": "cid (L. cadere : to fall / 떨어지다)",
            "flow": ["하늘에서 위로 뚝 떨어지다", "예상치 못하게 돌발적으로 마주치다", "물리적 사건, 해프닝", "부차적인 외교적/심리적 갈등과 마찰"]
        },
        "examples1": [
            {"en": "On March 13, 2016, an incident occurred that thrilled art scene.", "ko": "2016년 3월 13일, 미술계를 뒤흔든 사건이 발생했다."},
            {"en": "She reported the incident to the local police.", "ko": "그녀는 그 사건을 현지 경찰에 신고했다."}
        ],
        "transition_question": "돌발적인 돌멩이가 떨어지는 현상이 어떻게 국가 간의 \"갈등/마찰\"이 될까요?",
        "logic_flow": ["일정한 궤도 위로 무언가 뚝 떨어짐(cadere)", "↓", "평온하던 질서가 깨어지며 발생한 돌발적 일 (사건)", "↓", "인간관계나 국제 정치에서 튀어나온 돌출 요소", "↓", "심각한 대립이나 부차적 분쟁(갈등)"],
        "logic_desc": "질서 있는 평지에 갑자기 돌이 떨어져(cadere) 파문이 일듯, 일상에 돌발적으로 터진 사건과 그로 인한 마찰을 의미합니다.",
        "examples2": [
            {"en": "The border incident almost caused a war between the nations.", "ko": "그 국경 마찰(사건)은 두 나라 간의 전쟁을 초래할 뻔했다."},
            {"en": "He wanted to avoid any further domestic incidents.", "ko": "그는 더 이상의 가정 내 마찰(소동)을 피하고 싶었다."}
        ],
        "feeling": "incident = 머리 위로 갑자기 뚝(in) 떨어진(cid) 일 = 우발적 사건 = 부차적 분쟁/갈등",
        "real_tip": "accident는 '우연한 사고'를 뜻하지만, incident는 '의도적이거나 특정한 맥락을 가진 사건/마찰'에 가깝습니다.",
        "summary_flow": ["cadere 떨어지다", "incidere 위로 떨어지다", "incident 우발적인 일", "일상적 사건", "외교적/가정 내 마찰"],
        "quiz": [
            {"question": "The minor __________ was resolved without any injuries.", "translation": "그 경미한 사건은 부상자 없이 해결되었다.", "answer": "incident"},
            {"question": "A serious border __________ has strained relations between the countries.", "translation": "심각한 국경 갈등(마찰)이 국가 간의 관계를 긴장시켰다.", "answer": "incident"}
        ]
    },
    {
        "word": "contemporary",
        "pronunciation": "kuhn-TEM-puh-rer-ee",
        "meaning1": "현대의, 동시대의 (같은 시간대를 공유하는)",
        "meaning2": "최신 유행의, 현대적인 (시간의 앞단에 서서 트렌디한)",
        "intro": "시간(time)이라는 단어에서 나온 이 단어가 어떻게 '동시대'와 '현대적 미술'의 의미를 동시에 갖게 되었을까요?",
        "etymology": {
            "root1": "con- (L. com- : together / 함께, 다 같이)",
            "root2": "tempor (L. tempus : time / 시간)",
            "flow": ["동일한 시간(tempus)을 함께(con) 나누다", "같은 시대에 살아가는", "동시대의 / 현대의", "당대의 트렌디하고 현대적인"]
        },
        "examples1": [
            {"en": "The incident thrilled the contemporary art scene.", "ko": "그 사건은 현대 미술계를 감격시켰다(뒤흔들었다)."},
            {"en": "He was a contemporary of Shakespeare.", "ko": "그는 셰익스피어와 동시대 사람이었다."}
        ],
        "transition_question": "시간을 같이 보낸다는 개념이 어떻게 미술이나 건축의 \"현대적 유행\"이 되었을까요?",
        "logic_flow": ["역사의 타임라인 속에서 같은 지점(tempus)을 공유함", "↓", "과거가 아닌 우리가 함께(con) 발을 딛고 선 시대 (동시대의)", "↓", "현재 살아 움직이는 작가들의 최신 경향 (현대의)", "↓", "가장 세련되고 감각적인 최신 유행의"],
        "logic_desc": "고전(classic)과 대비되는, '지금 이 시점(tempus)에 우리와 호흡을 함께(con) 하는 최신 예술과 문물'을 의미합니다.",
        "examples2": [
            {"en": "She prefers contemporary dance to classical ballet.", "ko": "그녀는 고전 발레보다 현대 무용을 선호한다."},
            {"en": "The building has a very contemporary design.", "ko": "그 건물은 매우 현대적인 디자인을 가지고 있다."}
        ],
        "feeling": "contemporary = 시간(temp)을 함께(con) 보내는 = 동시대의 = 고전과 대조되는 현대적인",
        "real_tip": "명사로 쓰이면 '동시대 사람'을 뜻하며, 독해 지문에서는 문맥에 따라 '동시대의'인지 '현대의(modern)'인지 정확히 분별해야 합니다.",
        "summary_flow": ["tempus 시간", "temporarius 일시적인", "contemporary 함께하는 시간의", "동시대의", "현대적인/최신 유행의"],
        "quiz": [
            {"question": "We must study both ancient and __________ history.", "translation": "우리는 고대사와 현대사 모두를 공부해야 한다.", "answer": "contemporary"},
            {"question": "He was one of the greatest __________ composers.", "translation": "그는 당대(동시대)의 가장 위대한 작곡가 중 한 명이었다.", "answer": "contemporary"}
        ]
    },
    {
        "word": "portrait",
        "pronunciation": "PAWR-trit",
        "meaning1": "초상화, 인물화 (얼굴 선을 밖으로 그려 냄)",
        "meaning2": "상세한 묘사, 재현 (글로 쓴 생생한 기록)",
        "intro": "붓을 대고 선을 '앞으로 길게 긋는' 행동이 어떻게 인간의 영혼을 담는 '초상화'가 되었을까요?",
        "etymology": {
            "root1": "por- (L. pro- : forward / 앞으로, 밖에)",
            "root2": "trait (L. trahere : to draw, pull / 선을 긋다, 끌어당기다)",
            "flow": ["얼굴의 외곽 선을 앞으로 쭉 뻗어 그리다", "얼굴 생김새를 도화지 위에 모사하다", "인물 초상화, 초상", "성격이나 인격의 생생한 묘사/재현"]
        },
        "examples1": [
            {"en": "Rembrandt experts gathered to view this portrait of a man.", "ko": "렘브란트 전문가들이 한 남성의 초상화를 보기 위해 모였다."},
            {"en": "The museum has a gallery dedicated to royal portraits.", "ko": "그 미술관은 왕실 초상화 전용 전시실을 가지고 있다."}
        ],
        "transition_question": "붓으로 그린 얼굴 그림이 어떻게 소설이나 전기 속의 \"생생한 묘사\"가 되었을까요?",
        "logic_flow": ["얼굴의 미세한 굴곡과 특징을 앞으로(pro) 끄집어냄", "↓", "펜이나 붓으로 그 특징적인 선을 그림(trahere)", "↓", "인물의 외견을 닮게 만든 시각 예술품 (초상화)", "↓", "글을 통해 한 인물의 성격과 일생을 입체적으로 그려 냄", "↓", "생생한 묘사 / 재현"],
        "logic_desc": "도화지 위에 외곽 선(trait)을 잡아당겨 그려 겉모습을 완성하듯, 인간의 고유 성품과 특징을 시각적으로나 텍스트로 '끌어내어 재현(portray)'한 결과물입니다.",
        "examples2": [
            {"en": "The book provides a vivid portrait of a young doctor.", "ko": "그 책은 젊은 의사의 생생한 초상(묘사)을 제공한다."},
            {"en": "Her novel is a psychological portrait of a killer.", "ko": "그녀의 소설은 한 살인마에 대한 심리적 묘사이다."}
        ],
        "feeling": "portrait = 밖으로(pro) 끄집어낸 선(trait) = 인물 초상화 = 인물상 / 생생한 성격 묘사",
        "real_tip": "스마트폰 카메라의 '인물 사진 모드'가 바로 Portrait mode이며, 가로 출력(Landscape)과 반대되는 '세로 방향'을 뜻하기도 합니다.",
        "summary_flow": ["trahere 끌다/그리다", "protrahere 앞으로 끌어내다", "portrait 밖으로 묘사된 것", "초상화", "전기 속 인물 묘사"],
        "quiz": [
            {"question": "He commissioned a famous artist to paint his __________.", "translation": "그는 자신의 초상화를 그리기 위해 유명한 화가를 고용했다.", "answer": "portrait"},
            {"question": "The documentary presents a dark __________ of the modern society.", "translation": "그 다큐멘터리는 현대 사회의 어두운 초상(묘사)을 보여준다.", "answer": "portrait"}
        ]
    },
    {
        "word": "thoroughly",
        "pronunciation": "THUR-oh-lee",
        "meaning1": "철저하게, 구석구석 (처음부터 끝까지 완전히 관통하여)",
        "meaning2": "대단히, 완전히 (추상적인 완벽한 상태)",
        "intro": "터널을 끝까지 '통과한다'는 방향성이 어떻게 '철저하고 완전하다'는 부사가 되었을까요?",
        "etymology": {
            "root1": "thorough (OE. thurh : through / 꿰뚫어, 통과하여)",
            "root2": "-ly (Suffix : 부사 접사)",
            "flow": ["장벽의 이쪽에서 저쪽으로 뚫고 나가며", "어느 한 구석도 건너뛰지 않고 꼼꼼히", "철저하게, 정밀하게", "완전히, 100% 온전하게"]
        },
        "examples1": [
            {"en": "They thoroughly examined the painting to make sure.", "ko": "그들은 확실하게 하려고 그림을 철저히 조사했다."},
            {"en": "The room was thoroughly cleaned before guests arrived.", "ko": "손님들이 도착하기 전에 방이 구석구석 철저히 청소되었다."}
        ],
        "transition_question": "장벽을 관통하는 꼼꼼함이 어떻게 감정이나 태도의 \"완전히, 대단히\"가 되었을까요?",
        "logic_flow": ["장애물의 내부 중심을 정면으로 통과(through)하여 이탈함", "↓", "대강 수박 겉핥기 하지 않고 바닥 끝까지 파헤침", "↓", "행동을 구석구석 꼼꼼히 완수함 (철저하게)", "↓", "어떠한 흠집이나 의문도 남기지 않은 상태", "↓", "완전히, 대단히 (강조)"],
        "logic_desc": "처음부터 끝까지 뚫고 나아가는(through) 시선으로, 중간에 멈춤 없이 100% 밀도를 가득 채워 행동을 완수(thoroughly)하는 상태입니다.",
        "examples2": [
            {"en": "We thoroughly enjoyed the concert last night.", "ko": "우리는 어젯밤 콘서트를 완전히(대단히) 즐겼다."},
            {"en": "She was thoroughly confused by the instructions.", "ko": "그녀는 그 지시사항 때문에 완전히 혼란스러웠다."}
        ],
        "feeling": "thoroughly = 처음부터 끝까지 뚫어(through) 구석구석 = 철저하게 = 완전하게/대단히",
        "real_tip": "through(~를 통과하여), though(비록 ~일지라도), thorough(철저한)는 철자가 매우 비슷하여 어휘 시험 오답률이 극도로 높으니 주의해야 합니다.",
        "summary_flow": ["thurh 통과하여", "thorough 관통하는/철저한", "thoroughly 철저히 관통하여", "구석구석 꼼꼼하게", "완전히/대단히"],
        "quiz": [
            {"question": "The police __________ investigated the crime scene.", "translation": "경찰은 범죄 현장을 철저하게 수사했다.", "answer": "thoroughly"},
            {"question": "I am __________ convinced of his innocence.", "translation": "나는 그의 무죄를 완전히 확신한다.", "answer": "thoroughly"}
        ]
    },
    {
        "word": "extraordinary",
        "pronunciation": "ik-STRAWR-duh-ner-ee",
        "meaning1": "비범한, 놀라운 (평범한 일상 질서의 바깥에 놓인)",
        "meaning2": "이상한, 기이한 (상식의 궤도를 벗어난 독특함)",
        "intro": "일상의 '질서'를 뜻하는 단어 앞에 '바깥'이라는 접두사가 붙어 어떻게 '비범하고 특별한' 뜻이 될까요?",
        "etymology": {
            "root1": "extra- (L. extra- : outside, beyond / 벗어남, 바깥에)",
            "root2": "ordinary (L. ordo : order, rule / 질서, 일반적 일상)",
            "flow": ["일반적인 질서와 상식선 바깥에 있는", "보통의 규격에서 아득히 멀어진", "비범한, 뛰어난, 놀라운", "상식을 넘어서 묘하고 기이한"]
        },
        "examples1": [
            {"en": "How wonderful to greet a new work of this extraordinary artist!", "ko": "이 비범한 예술가의 신작을 맞이하게 되다니 얼마나 경이로운가!"},
            {"en": "She has an extraordinary talent for mathematics.", "ko": "그녀는 수학에 비범한(놀라운) 재능을 가지고 있다."}
        ],
        "transition_question": "규격을 초월한 뛰어남이 어떻게 사물에 붙으면 \"기이하고 이상한\" 뉘앙스가 될까요?",
        "logic_flow": ["규정된 행동 질서와 타임라인 (ordo)", "↓", "그 질서의 울타리를 뚫고 바깥(extra)으로 탈출함", "↓", "평범한 수준을 아득히 뛰어넘어 찬탄을 자아냄 (비범한, 놀라운)", "↓", "설명하기 힘들 만큼 이례적이고 독특함", "↓", "이상한, 기이한"],
        "logic_desc": "평범하고 뻔한 질서의 궤도(Ordo) 바깥에(Extra) 홀로 빛나는 지표나 사물을 지칭하여, 대단한 찬사(비범함)와 기묘함(이상함)을 공유합니다.",
        "examples2": [
            {"en": "An extraordinary light was seen in the night sky.", "ko": "밤하늘에 기이한(놀라운) 불빛이 보였다."},
            {"en": "It is extraordinary that they resolved the problem so fast.", "ko": "그들이 그 문제를 그렇게 빨리 해결했다는 것은 기이한(놀라운) 일이다."}
        ],
        "feeling": "extraordinary = 질서(ordinary) 바깥에(extra) 있는 = 평범하지 않은 = 비범한/놀라운 = 기이한",
        "real_tip": "보통 ordinary(평범한)의 반대말로 쓰이며, 인물 묘사나 과학적 업적을 극찬할 때 독해 지문의 핵심 단어로 기여합니다.",
        "summary_flow": ["ordo 질서", "ordinarius 일반적인 질서의", "extra-ordinarius 질서 밖의", "extraordinary 비범한/대단한", "기이한/이상한"],
        "quiz": [
            {"question": "His performance was __________ and received a standing ovation.", "translation": "그의 공연은 비범했고(대단했고) 기립박수를 받았다.", "answer": "extraordinary"},
            {"question": "There was nothing __________ about the case; it was simple.", "translation": "그 사건에는 전혀 기이한(특별한) 점이 없었다. 그것은 단순했다.", "answer": "extraordinary"}
        ]
    },
    {
        "word": "evidence",
        "pronunciation": "EV-i-duhns",
        "meaning1": "증거, 근거 (내부의 진실을 밖으로 보여주는 것)",
        "meaning2": "흔적, 징후 (추상적인 증명 단서)",
        "intro": "눈으로 '확인하여 보다'라는 어근에서 어떻게 법정에서 죄를 밝히는 '증거'가 나왔을까요?",
        "etymology": {
            "root1": "e- (L. ex- : out / 밖으로)",
            "root2": "vid (L. videre : to see / 보다)",
            "flow": ["장막 속에 감춰진 진실을 밖으로 꺼내 보게 하다", "확실히 볼 수 있게 만드는 명백함", "주장을 논리적으로 뒷받침하는 물리적 증거(물)", "진실을 보여주는 뚜렷한 흔적/징후"]
        },
        "examples1": [
            {"en": "The experts asked them to offer some evidence.", "ko": "전문가들은 그들에게 몇 가지 증거를 제공해달라고 요청했다."},
            {"en": "There is no scientific evidence to support this claim.", "ko": "이 주장을 뒷받침할 과학적 증거는 없다."}
        ],
        "transition_question": "눈에 보이는 물질적 입증이 어떻게 추상적 질병의 \"징후/흔적\"으로 연결될까요?",
        "logic_flow": ["의혹이라는 장막 너머에 진실이 숨어 있음", "↓", "장막을 찢고 밖(ex)으로 실물을 꺼내어 직접 보게 함(videre)", "↓", "부인할 수 없는 절대적인 근거 (증거)", "↓", "어떤 사건이나 현상이 존재했었음을 지시하는 흔적", "↓", "흔적, 징후"],
        "logic_desc": "눈앞에 명백히 보여줌(evident)으로써 상대의 마음속 의혹을 강제로 해소해 주는 굳건한 입증의 실체(evidence)입니다.",
        "examples2": [
            {"en": "The police found evidence of a struggle in the room.", "ko": "경찰은 방 안에서 싸운 흔적(증거)을 발견했다."},
            {"en": "His pale face was clear evidence of his illness.", "ko": "그의 창백한 얼굴은 그의 병에 대한 확실한 징후(증거)였다."}
        ],
        "feeling": "evidence = 밖으로(e) 꺼내어 눈앞에 보여주는(vid) 것 = 입증 자료 = 흔적/징후",
        "real_tip": "evidence는 셀 수 없는 명사(uncountable)로 취급되므로, 앞에 a를 붙이거나 복수형 evidences로 잘 쓰지 않고 주로 information처럼 단수 취급합니다.",
        "summary_flow": ["videre 보다", "evidens 밖으로 훤히 보이는", "evidence 눈앞에 보여주는 것", "입증 증거", "추상적 흔적/징후"],
        "quiz": [
            {"question": "We need to gather more __________ before making a decision.", "translation": "우리는 결정을 내리기 전에 더 많은 증거를 수집해야 한다.", "answer": "evidence"},
            {"question": "There was no __________ that he had been in the building.", "translation": "그가 건물 안에 있었다는 흔적(증거)이 전혀 없었다.", "answer": "evidence"}
        ]
    },
    {
        "word": "provoked",
        "pronunciation": "pruh-VOHKT",
        "meaning1": "촉발했다, 자아냈다 (상대의 반응을 소리쳐 끌어내다)",
        "meaning2": "화나게 했다, 성질을 돋웠다 (도발하여 화를 유도함)",
        "intro": "상대의 목소리를 '밖으로 소환하는' 행동이 어떻게 감정을 불같이 일어나게 만드는 '도발'과 '촉발'이 되었을까요?",
        "etymology": {
            "root1": "pro- (L. pro- : forward, out / 앞으로, 바깥으로)",
            "root2": "vok (L. vocare : to call / 부르다, 소리치다) + -ed",
            "flow": ["상대를 성벽 앞으로 나오라고 소리쳐 부르다", "싸움을 도발하다, 상대를 격분시켜 화나게 했다", "추상적인 반응이나 토론, 의문을 자아냈다", "질문이나 사건을 촉발했다"]
        },
        "examples1": [
            {"en": "This was one of the events that provoked the question.", "ko": "이것은 그 질문(의문)을 촉발한(자아낸) 사건들 중 하나였다."},
            {"en": "His rude remarks provoked a violent response.", "ko": "그의 무례한 발언은 격렬한 반응을 자아냈다(촉발했다)."}
        ],
        "transition_question": "물리적 도발이 어떻게 논쟁의 \"의문을 자아냈다\"라는 유연한 지적 작용이 되었을까요?",
        "logic_flow": ["상대방을 앞으로(pro) 나오라고 큰소리로 부름(vocare)", "↓", "평온한 마음의 평정을 흔들어 화를 돋움 (화나게 했다)", "↓", "외부에서 주입된 충격이 마음에 잠재된 반응을 툭 쳐서 꺼냄", "↓", "의문이나 활발한 토론의 물꼬를 엶 (자아냈다, 촉발했다)"],
        "logic_desc": "숨어 있던 생각이나 억눌린 감정을 밖으로(pro) 끄집어내게끔 자극을 던져 불러일으키는(vocare) 도발적 기제입니다.",
        "examples2": [
            {"en": "The new book provoked a nationwide debate on safety.", "ko": "그 새 책은 안전에 대한 전국적인 토론을 촉발했다(자아냈다)."},
            {"en": "She was provoked by his constant teasing.", "ko": "그녀는 그가 지속적으로 놀려대자 화가 났다(도발당했다)."}
        ],
        "feeling": "provoked = 앞으로(pro) 불러내다(vok) = 자극하여 화를 돋웠다 = 의문/반응을 촉발했다",
        "real_tip": "provoke는 'provoke A to B' (A를 자극해 B하게 하다) 구문으로 쓰이거나, 명사형 provocation(도발, 자극)과 함께 출제됩니다.",
        "summary_flow": ["vocare 부르다", "provocare 앞으로 불러내다", "provoke 감정을 부추기다", "과거/과거분사형 적용", "촉발했다/자아냈다"],
        "quiz": [
            {"question": "The decision __________ a storm of protests among citizens.", "translation": "그 결정은 시민들 사이에 거센 항의의 폭풍을 촉발했다.", "answer": "provoked"},
            {"question": "He was easily __________ to anger by small criticisms.", "translation": "그는 작은 비판에도 쉽게 자극을 받아 분노했다(화가 났다).", "answer": "provoked"}
        ]
    },
    {
        "word": "unresolved",
        "pronunciation": "uhn-rih-ZAHLVD",
        "meaning1": "해결되지 않은, 미해결의 (단단히 엉킨 매듭을 끝내 풀지 못한)",
        "meaning2": "우유부단한, 결단이 서지 않은 (추상적 마음에 매듭을 짓지 못한)",
        "intro": "단단한 고체를 '녹여서 해체하는' 화학적 어원의 단어가 왜 풀리지 않은 '의문'이 되었을까요?",
        "etymology": {
            "root1": "un- (L. not / 아님)",
            "root2": "re- (L. intensive / 강하게) + solv (L. solvere : to loosen / 풀다, 용해하다) + -ed",
            "flow": ["단단하게 고착된 것을 부드럽게 풀지 못한", "문제를 명쾌하게 해결하지 못한", "해결되지 않은, 미해결의", "마음에 방향을 정하지 못하고 망설이는"]
        },
        "examples1": [
            {"en": "This question is unresolved, but critics see it as art.", "ko": "이 질문은 아직 해결되지 않았으나, 비평가들은 이것을 예술로 본다."},
            {"en": "They left several unresolved issues after the meeting.", "ko": "그들은 회의 후에 몇 가지 해결되지 않은 문제들을 남겨두었다."}
        ],
        "transition_question": "수학식이나 의문이 풀리지 않은 상태가 어떻게 사람의 \"망설임\"이 되었을까요?",
        "logic_flow": ["꽁꽁 묶이거나(solvere) 굳어버린 물질", "↓", "부드럽게 녹여서 액체로 해체해야 해결(resolve)이 됨", "↓", "아직 그 매듭이 그대로 남아 있어 해결되지 못함 (미해결의)", "↓", "내적 생각의 가치 정리가 확실히 마무리되지 않음", "↓", "결단을 내리지 못하고 망설이는"],
        "logic_desc": "단단하게 엉켜 응고된 매듭을 말끔하게 풀어내지(solvere) 못한 채 방치되어 공중에 떠 있는 찜찜한 상태를 가리킵니다.",
        "examples2": [
            {"en": "She remained unresolved about whether to accept the job.", "ko": "그녀는 그 일자리를 수용할지 여부에 대해 망설였다(결단하지 못했다)."},
            {"en": "The mystery of his disappearance is still unresolved.", "ko": "그가 사라진 미스터리는 여전히 풀리지 않았다(해결되지 않았다)."}
        ],
        "feeling": "unresolved = 풀리지(solve) 않은(un) = 단단히 매여 있는 = 미해결의 = 결단 못 하고 망설이는",
        "real_tip": "동사형 resolve는 '해결하다, 결심하다, 분해하다'라는 상반되어 보이는 세 뜻을 지니고 있어 빈출도가 매우 높습니다.",
        "summary_flow": ["solvere 풀다/느슨하게 하다", "resolvere 완전히 풀다/분해하다", "resolved 해결된/결심이 단단한", "unresolved 해결 안 된", "미해결의 / 망설이는"],
        "quiz": [
            {"question": "Many questions about the incident remain __________.", "translation": "그 사건에 대한 많은 질문들이 여전히 해결되지 않은 상태로 남아 있다.", "answer": "unresolved"},
            {"question": "He was __________ to the end, unable to make a choice.", "translation": "그는 결국 선택을 내리지 못한 채 마지막까지 망설였다(결단하지 못했다).", "answer": "unresolved"}
        ]
    },
    {
        "word": "critics",
        "pronunciation": "KRIT-iks",
        "meaning1": "비평가들, 평론가들 (작품의 질을 정밀하게 가려내는 사람)",
        "meaning2": "혹평가들, 깎아내리는 세력 (부정적 의견을 투사하는 주체)",
        "intro": "진짜와 가짜를 이지적으로 '판단하는' 사람이 왜 예술 영역에서는 무서운 '비평가'가 되었을까요?",
        "etymology": {
            "root1": "crit (Gk. krinein : to decide, judge / 판단하다, 가르다)",
            "root2": "-ic (Suffix : 학문, 주체) + -s (Plural)",
            "flow": ["옳고 그름, 가치 있고 없음을 이지적으로 판정하는 자", "예술이나 책의 완성도를 전문적으로 감정하는 사람", "비평가들, 평론가들", "늘 단점을 들추며 가혹하게 혹평하는 세력"]
        },
        "examples1": [
            {"en": "More and more art critics see AI art as a new field.", "ko": "점점 더 많은 미술 비평가들이 AI 예술을 새로운 분야로 보고 있다."},
            {"en": "The film received high praise from contemporary critics.", "ko": "그 영화는 당대의 평론가들로부터 높은 찬사를 받았다."}
        ],
        "transition_question": "이지적 잣대를 지닌 감정사가 어떻게 대상을 헐뜯는 \"혹평가들\"이 되었을까요?",
        "logic_flow": ["옥석을 가려내기 위해 칼을 대어 분별함(krinein)", "↓", "작품의 결함이나 우수성을 분석하여 지면에 기재함 (비평가)", "↓", "분석적 태도가 부정적인 방향으로 극대화됨", "↓", "꼬투리를 잡아 흠집을 대중에게 퍼뜨리는 비토 세력 (혹평가들)"],
        "logic_desc": "대상의 완성도를 정밀하게 저울질하여 가르는(krinein) 지적 필터를 쥐고 있는 주체(critics)로, 공적 평가단과 흠집 잡는 세력의 두 얼굴을 지닙니다.",
        "examples2": [
            {"en": "The politician's critics accused him of corruption.", "ko": "그 정치인의 혹평가들(반대 세력)은 그를 부패 혐의로 고발했다."},
            {"en": "She ignored her critics and kept writing her novel.", "ko": "그녀는 비평가들(혹평가들)을 무시하고 소설을 계속 썼다."}
        ],
        "feeling": "critics = 잣대를 대고 정밀하게 가르는(crit) 사람들 = 평론가들 = 흠집을 파고드는 반대파들",
        "real_tip": "critical(비판적인/중요한), criticize(비판하다), criticism(비평/비판) 등 파생어 전체가 단골 출제됩니다.",
        "summary_flow": ["krinein 가르다/판단하다", "krites 재판관/판단하는 자", "criticus 비평가", "복수화", "비평가들 / 반대파들"],
        "quiz": [
            {"question": "Art __________ were not impressed by the new style of painting.", "translation": "미술 비평가들은 새로운 스타일의 그림에 감명받지 않았다.", "answer": "critics"},
            {"question": "He has silenced his __________ by winning the championship.", "translation": "그는 챔피언십을 우승함으로써 자신을 깎아내리던 혹평가들(비판자들)을 침묵시켰다.", "answer": "critics"}
        ]
    },
    {
        "word": "photography",
        "pronunciation": "fuh-TAHG-ruh-fee",
        "meaning1": "사진술, 사진 예술 (빛의 화학 작용을 통해 기록하는 물리적 방식)",
        "meaning2": "사진 (인화된 인쇄물)",
        "intro": "그리스어로 '빛'과 '그림 그리기'가 만나 탄생한 이 단어가 어떻게 기술을 넘어 '예술'이 되었을까요?",
        "etymology": {
            "root1": "photo (Gk. phos : light / 빛)",
            "root2": "graph (Gk. graphein : to write, draw / 적다, 그리다, 기록하다) + -y",
            "flow": ["감광제 위에 빛(phos)의 화학 작용으로 이미지를 고정하다", "렌즈를 통해 들어온 기하학적 형상을 기록하는 방식 (사진술)", "기술에서 하나의 독자적인 미학으로 진화함", "사진 예술 / 사진"]
        },
        "examples1": [
            {"en": "Photography came to be seen as art rather than technology.", "ko": "사진이 기술이라기보다 예술로 여겨지게 되었다."},
            {"en": "She fell in love with landscape photography during her trip.", "ko": "그녀는 여행 동안 풍경 사진 예술에 매료되었다."}
        ],
        "transition_question": "빛으로 기록하는 기술 방식이 어떻게 우리 집 벽에 걸어두는 \"실물 사진 한 장\"이 될까요?",
        "logic_flow": ["카메라 옵스큐라 어두운 방 내부에 구멍을 뚫음", "↓", "빛(phos)의 직진을 이용해 필름 위에 화학적 자국을 새김(graphein)", "↓", "대상의 실상을 완전무결하게 기계적으로 기록해 내는 기술 (사진술)", "↓", "작가의 시각적 영감이 투사된 예술적 소장품 (사진)"],
        "logic_desc": "인위적인 붓질 대신, 자연의 본질인 빛(phos)을 도구로 삼아 찰나를 새겨(graphein) 영구 보존하는 미학적 도구입니다.",
        "examples2": [
            {"en": "Digital photography has made taking pictures very easy.", "ko": "디지털 사진술은 사진 촬영을 매우 쉽게 만들었다."},
            {"en": "He collected old black-and-white photographs of the city.", "ko": "그는 그 도시의 옛 흑백 사진들을 수집했다."}
        ],
        "feeling": "photography = 빛(photo)으로 기록한(graph) 것 = 물리적 사진 촬영 기술 = 사진 예술",
        "real_tip": "photograph(사진/동사로 사진 찍다), photographer(사진작가), photographic(사진의/기억력이 생생한)으로 변형 출제됩니다.",
        "summary_flow": ["phos 빛", "graphein 쓰다/그리다", "photograph 빛으로 그린 그림", "-y 접사 적용", "사진술 / 사진 예술"],
        "quiz": [
            {"question": "He decided to study __________ at the art institute.", "translation": "그는 예술 대학에서 사진술(사진 예술)을 공부하기로 결정했다.", "answer": "photography"},
            {"question": "The exhibition showcases the best of wildlife __________.", "translation": "그 전시회는 야생 동물 사진 예술의 정수를 보여준다.", "answer": "photography"}
        ]
    },
    {
        "word": "occurred",
        "pronunciation": "uh-KURD",
        "meaning1": "발생했다, 일어났다 (눈앞에 갑자기 마주하여 뛰어들다)",
        "meaning2": "(생각이) 머릿속에 떠올랐다 (뇌리에 스쳐 가다 - 주로 occurred to)",
        "intro": "나를 향해 마주하여 '달려오는' 이미지가 어떻게 '사건이 발생하다'가 되었을까요?",
        "etymology": {
            "root1": "oc- (L. ob- : against, toward / ~를 마주하여, 향해)",
            "root2": "cur (L. currere : to run / 달리다) + -ed (Suffix : 과거형)",
            "flow": ["눈앞에 가로막고 맞대어 달려 나오다", "길 모퉁이에서 갑자기 마주쳐 튀어나오다", "사건이나 일이 발생했다", "아이디어가 뇌 속 의식 표면으로 솟아올랐다"]
        },
        "examples1": [
            {"en": "An incident occurred that thrilled the contemporary art scene.", "ko": "현대 미술계를 뒤흔든 사건이 발생했다(일어났다)."},
            {"en": "The accident occurred at the intersection yesterday.", "ko": "그 사고는 어제 교차로에서 일어났다."}
        ],
        "transition_question": "바깥에서 마주친 사건이 어떻게 내 머릿속의 \"깨달음/생각의 떠오름\"이 되었을까요?",
        "logic_flow": ["평화롭게 걷던 중 눈앞(ob)으로 정면 마주쳐 돌진함", "↓", "예측하지 못한 돌출 현상이 실재화됨 (발생했다)", "↓", "외부 자극이 아니라 뇌 신경망의 한 아이디어가 의식 위로 달려옴", "↓", "생각이 나에게 불쑥 찾아왔다 (occurred to)"],
        "logic_desc": "나를 마주하고(ob) 달려오는(currere) 물리적 돌발 사건(occurrence)에서, 생각의 끈이 머릿속에 돌출하여 스치는 인지 작용으로 확장되었습니다.",
        "examples2": [
            {"en": "It suddenly occurred to me that I had left my keys behind.", "ko": "내가 열쇠를 두고 왔다는 생각이 갑자기 내 뇌리에 떠올랐다."},
            {"en": "No problems have occurred so far.", "ko": "지금까지는 아무런 문제도 발생하지 않았다."}
        ],
        "feeling": "occurred = 내 앞을 향해(ob) 달려왔다(cur) = 불쑥 터졌다 = 발생했다 = 생각이 떠올랐다",
        "real_tip": "자음 r이 하나 더 겹치는 스펠링 규칙(occur -> occurred)을 내신 주관식 서술형에서 자주 실수하니 암기해야 합니다.",
        "summary_flow": ["currere 달리다", "occurrere 맞닥뜨리다", "occur 발생하다", "r 중복 및 과거형", "발생했다/떠올랐다"],
        "quiz": [
            {"question": "A massive earthquake __________ in the Pacific ocean.", "translation": "태평양에서 거대한 지진이 발생했다.", "answer": "occurred"},
            {"question": "It never __________ to him that they were playing a prank.", "translation": "그들이 장난을 치고 있다는 생각이 그에게는 전혀 떠오르지 않았다.", "answer": "occurred"}
        ]
    },
    {
        "word": "genuine",
        "pronunciation": "JEN-yoo-in",
        "meaning1": "진짜의, 진품의 (혈통이 공인된 진짜배기)",
        "meaning2": "진심 어린, 솔직한 (거짓이 없는 순수한 태도)",
        "intro": "아버지의 '무릎'을 가리키던 라틴어가 어떻게 '진짜의'와 '진심 어린'이라는 뜻이 되었을까요?",
        "etymology": {
            "root1": "genu (L. genu : knee / 무릎)",
            "root2": "L. genuinus (진짜의, 가식 없는, 본래 타고난)",
            "flow": ["태어난 아기를 아버지 무릎에 얹고 가문의 자식으로 공인하다", "가짜가 아님이 명백히 증명된", "진짜의, 진품의", "속임수가 없이 진실하고 진심 어린"]
        },
        "examples1": [
            {"en": "Several hours later, they confirmed, 'This is a genuine Rembrandt.'", "ko": "몇 시간 뒤, 그들은 '이것은 진짜 렘브란트 작품입니다'라고 확인했다."},
            {"en": "The purse is made of genuine leather.", "ko": "그 지갑은 진짜 가죽(천연 가죽)으로 만들어졌다."}
        ],
        "transition_question": "가짜가 아닌 실물 물건의 진짜성이 어떻게 사람의 \"진심 어린 마음\"이 될까요?",
        "logic_flow": ["로마의 아버지가 무릎(genu)에 얹어 가문의 정통 혈통을 확증함", "↓", "가짜 유전자나 복제품이 섞이지 않은 본래 그대로의 실물 (진짜의)", "↓", "포장을 하거나 남을 속이기 위한 위선이 없음", "↓", "가식 없이 순수하게 다가오는 솔직함 (진심 어린)"],
        "logic_desc": "가문의 권위자(가부장)가 무릎 위에 앉혀 정통성을 입증해 준(genuinus) 신뢰성에서 출발하여, 가식의 불순물이 섞이지 않은 진짜배기 상태를 뜻합니다.",
        "examples2": [
            {"en": "He showed a genuine concern for the safety of children.", "ko": "그는 아이들의 안전에 대해 진심 어린(가식 없는) 염려를 보여주었다."},
            {"en": "She had a genuine interest in learning Korean history.", "ko": "그녀는 한국사를 공부하는 데 순수한(진짜) 관심을 가지고 있었다."}
        ],
        "feeling": "genuine = 무릎(genu) 위에 얹어 인정받은 정통 = 진짜의 = 위선 없는 진심 어린",
        "real_tip": "반대말인 fake(가짜의), artificial(인공의), insincere(불성실한) 등과 독해 반의어 관계를 형성합니다.",
        "summary_flow": ["genu 무릎", "genuinus 무릎에 얹어 인정한 적자", "genuine 정통의", "진짜의/진품의", "가식 없는 진심 어린"],
        "quiz": [
            {"question": "Is this painting a __________ Picasso or a copy?", "translation": "이 그림은 진짜 피카소 작품인가요, 아니면 모작인가요?", "answer": "genuine"},
            {"question": "He is a __________ friend who always helps me in need.", "translation": "그는 내가 곤경에 처할 때 항상 돕는 진심 어린(진정한) 친구이다.", "answer": "genuine"}
        ]
    },
    {
        "word": "mechanism",
        "pronunciation": "MEK-uh-niz-uhm",
        "meaning1": "기계 장치, 작동 원리 (부품이 맞물려 돌아가는 장치)",
        "meaning2": "기제, 방법, 대처 수단 (추상적 사회/심리적 작동법)",
        "intro": "차량의 '톱니바퀴 결합'이 어떻게 우리 마음의 스트레스 '방어 기제'가 되었을까요?",
        "etymology": {
            "root1": "mechan (Gk. mekhane : machine, tool / 도구, 기계, 수단)",
            "root2": "-ism (Suffix : 사상, 체계, 작동 형태)",
            "flow": ["도구를 조밀하게 결합하여 만든 기계", "부품들이 유기적으로 맞물려 굴러가는 작동 방식", "물리적인 기계 구조/원리", "정신적이나 사회적으로 작동하는 기제/수단"]
        },
        "examples1": [
            {"en": "Let us look at the mechanism of AI creativity.", "ko": "AI 창의성의 작동 원리(메커니즘)를 살펴보자."},
            {"en": "The clock's mechanism is incredibly delicate.", "ko": "그 시계의 작동 장치(원리)는 믿을 수 없을 정도로 정교하다."}
        ],
        "transition_question": "물리적인 기계 톱니바퀴의 원리가 어떻게 인간 내면의 \"방어 기제\"가 될까요?",
        "logic_flow": ["인간의 손을 편하게 돕는 도구적 설계 (mekhane)", "↓", "나사선과 축이 얽혀 일정한 결과를 뽑아냄 (작동 원리)", "↓", "자극이 들어왔을 때 뇌나 조직이 자동 반사적으로 출력함", "↓", "심리적 위기를 모면하기 위해 가동되는 방어 체계 (기제)"],
        "logic_desc": "입력값(input)이 들어가면 내부 기어들이 정해진 인과관계에 따라 굴러가 출력값(output)을 내놓는 기계(machine)의 질서정연한 계통을 뜻합니다.",
        "examples2": [
            {"en": "Laughter is a natural coping mechanism for stress.", "ko": "웃음은 스트레스에 대한 자연스러운 대처 기제(방법)이다."},
            {"en": "The body has a built-in defense mechanism against bacteria.", "ko": "신체는 박테리아에 대응하는 내장된 방어 기제(체계)를 가지고 있다."}
        ],
        "feeling": "mechanism = 톱니바퀴가 얽힌 기계(mechan) = 인과적 작동 원리 = 심리적 대처 기제",
        "real_tip": "coping mechanism(대처 기제), defense mechanism(방어 기제)은 수능 심리학 독해의 단골 킬러 소재입니다.",
        "summary_flow": ["mekhane 도구/기계", "mechanicus 기계학", "mechanismus 기계적 구조", "물리적 작동 원리", "심리적 대처 기제"],
        "quiz": [
            {"question": "Scientists studied the __________ of cell division.", "translation": "과학자들은 세포 분열의 작동 메커니즘(원리)을 연구했다.", "answer": "mechanism"},
            {"question": "Denial is a common defense __________ in psychological trauma.", "translation": "부인은 심리적 트라우마에서 흔히 나타나는 방어 기제이다.", "answer": "mechanism"}
        ]
    },
    {
        "word": "distinguish",
        "pronunciation": "dih-STING-gwish",
        "meaning1": "구별하다, 식별하다 (따로 찔러서 표시해 가르다)",
        "meaning2": "두각을 나타내다 (나를 특별하게 세상에 표시함)",
        "intro": "날카로운 바늘로 콕 '찔러 자국을 내는' 행위가 어떻게 '구별하다'와 '성공하다'가 되었을까요?",
        "etymology": {
            "root1": "di- (L. dis- : apart / 갈라져, 따로)",
            "root2": "sting (L. stinguere : to prick, stamp / 찌르다, 도장을 찍다)",
            "flow": ["여럿 중에서 따로 구별하여 찌르다", "각 부위에 낙인이나 자국을 남겨 가르다", "대상을 구별하다, 식별하다", "나를 무리 속에서 찔러 솟구치게 돋보이게 하다 (두각을 나타내다)"]
        },
        "examples1": [
            {"en": "It makes a machine think, distinguish, and create.", "ko": "그것은 기계가 생각하고, 구별하고, 창조하게 만든다."},
            {"en": "He can't distinguish red from green.", "ko": "그는 빨간색과 초록색을 구별하지 못한다."}
        ],
        "transition_question": "물건들을 분리해 낙인을 찍는 행위가 어떻게 인간이 사회적으로 \"두각을 나타내다\"가 될까요?",
        "logic_flow": ["무더기로 섞여 있는 대상들의 뭉텅이", "↓", "각각 따로(dis) 날카로운 핀으로 찔러서(stinguere) 구멍을 냄", "↓", "시각적 표식에 기반하여 다름을 가려냄 (구별하다)", "↓", "나의 가치와 성과를 평범한 군중들 밖으로 끄집어내어 돋보이게 함", "↓", "두각을 나타내다 (distinguish oneself)"],
        "logic_desc": "섞여 있는 무리들 중에서 콕 찔러서(stinguere) 따로(dis) 분류 기호를 매기듯, 대상을 뚜렷하게 분리하여 식별하는 이지적 단속입니다.",
        "examples2": [
            {"en": "She distinguished herself as an excellent lawyer.", "ko": "그녀는 훌륭한 변호사로 두각을 나타냈다(자신을 돋보이게 했다)."},
            {"en": "The double lines distinguish this breed from others.", "ko": "두 개의 선이 이 품종을 다른 품종들과 구별해 준다."}
        ],
        "feeling": "distinguish = 따로(dis) 찔러(sting) 표시하다 = 식별하다/구별하다 = 두각을 나타내다",
        "real_tip": "distinguish A from B (A와 B를 구별하다) 또는 distinguish between A and B의 전치사 구조로 90% 이상 출제됩니다.",
        "summary_flow": ["stinguere 찌르다", "distinguere 따로 찔러 가르다", "distinguish 구별하다", "distinguished 훌륭한/두드러진", "distinguish oneself 두각을 나타내다"],
        "quiz": [
            {"question": "It is hard to __________ the twins from each other.", "translation": "그 쌍둥이를 서로 구별하기란 어렵다.", "answer": "distinguish"},
            {"question": "He managed to __________ himself in the physics department.", "translation": "그는 물리학과에서 가까스로 두각을 나타냈다.", "answer": "distinguish"}
        ]
    },
    {
        "word": "recognized",
        "pronunciation": "REK-uhg-nyzd",
        "meaning1": "알아보았다, 인지했다 (뇌 속 사전의 지식을 다시 확인해 알다)",
        "meaning2": "인정받았다, 공인되었다 (사회적 가치를 증명받음)",
        "intro": "'다시 머리를 굴려 안다'는 어원이 어떻게 길거리에서 지인을 '알아보다'와 사회적으로 '공인받다'가 될까요?",
        "etymology": {
            "root1": "re- (L. re- : again / 다시, 한번 더)",
            "root2": "cogn (L. cognoscere : to know / 인지하다, 알다) + -ized",
            "flow": ["과거의 기억을 바탕으로 다시 머릿속에서 알아채다", "익숙한 외모나 스타일을 보고 대조해 내다", "알아보았다, 식별했다", "사회의 합의를 거쳐 가치를 인정받았다"]
        },
        "examples1": [
            {"en": "They immediately recognized the artist's vivid style.", "ko": "그들은 그 작가의 생생한 스타일을 즉시 알아봤다."},
            {"en": "I recognized her voice instantly on the phone.", "ko": "나는 전화 통화에서 그녀의 목소리를 즉시 알아챘다."}
        ],
        "transition_question": "눈앞의 대상을 알아보는 개인적 인지가 어떻게 사회적 안보나 자격의 \"공인/인정\"이 될까요?",
        "logic_flow": ["예전에 취득한 정보의 데이터베이스", "↓", "새 자극을 마주했을 때 뇌 속 서랍을 뒤져 다시(re) 인지함(cognoscere)", "↓", "알아보고 대조 확인을 마침 (알아보았다)", "↓", "학위나 업적이 검증 기준에 맞물려 합당함을 정식 선언함", "↓", "공인받았다, 인정받았다"],
        "logic_desc": "두뇌 속에 있던 기성의 개념 지도(Cognize)를 대상 위에 다시(re-) 투영해 보아 정확히 부합함을 승인하는 인지 및 승인의 활동입니다.",
        "examples2": [
            {"en": "He was recognized as the rightful heir to the throne.", "ko": "그는 왕위의 정당한 상속자로 공인받았다(인정받았다)."},
            {"en": "The government recognized the independence of the colony.", "ko": "정부는 식민지의 독립을 정식 인정했다(승인했다)."}
        ],
        "feeling": "recognized = 머릿속에서 다시(re) 알게(cogn) 되었다 = 알아보았다 = 가치를 공인받았다",
        "real_tip": "recognition(인지, 인정), recognizable(알아볼 수 있는)도 함께 연계되며, 수동태 be recognized as(~로 인정받다)로도 빈출됩니다.",
        "summary_flow": ["cognoscere 알다/이해하다", "recognoscere 다시 알다/검토하다", "recognize 알아보았다", "사회적 가치 공인", "과거/과거분사형 적용"],
        "quiz": [
            {"question": "She __________ her old school friend in the crowd.", "translation": "그녀는 군중 속에서 그녀의 옛 학교 친구를 알아보았다.", "answer": "recognized"},
            {"question": "He was widely __________ for his contribution to science.", "translation": "그는 과학에 기여한 공로로 널리 인정받았다(표창받았다).", "answer": "recognized"}
        ]
    },
    {
        "word": "confirmed",
        "pronunciation": "kuhn-FURMD",
        "meaning1": "확인해 주었다, 확증했다 (뿌리를 완전히 단단하게 다짐)",
        "meaning2": "고질적인, 만성적인 (추상적 버릇이 철근처럼 단단해진)",
        "intro": "흔들리는 기둥 아래에 시멘트를 부어 '단단하게(firm)' 만드는 행위가 어떻게 '사실로 확인하다'가 되었을까요?",
        "etymology": {
            "root1": "con- (L. com- : completely / 완전히, 강하게)",
            "root2": "firm (L. firmus : strong, stable / 단단한, 확실한) + -ed",
            "flow": ["완전히 철근을 박아 단단하고 강하게 만들다", "불확실한 의혹을 단단한 사실로 고정하다", "확인해 주었다, 확증했다", "생각이나 버릇이 굳어져 고착된, 고질적인"]
        },
        "examples1": [
            {"en": "Several hours later, they confirmed, 'This is a genuine Rembrandt.'", "ko": "몇 시간 뒤, 그들은 '이것은 진짜 렘브란트입니다'라고 확인했다."},
            {"en": "The results confirmed our worst fears.", "ko": "그 결과는 우리의 가장 나쁜 두려움(우려)을 확인해 주었다(확증했다)."}
        ],
        "transition_question": "의혹을 사실로 굳히는 확증이 어떻게 사람의 기질이 굳어버린 \"만성적인\"이 될까요?",
        "logic_flow": ["뜬소문이나 가설이 공중에 날아다님", "↓", "검증을 통해 바닥에 완전히(con) 단단하게(firmus) 고착시킴", "↓", "진실임이 흔들림 없이 확인됨 (확증했다)", "↓", "의견이나 라이프스타일의 뿌리가 시멘트처럼 딱딱해짐", "↓", "만성적인, 굳어버린 (ex. confirmed bachelor : 골수 독신주의자)"],
        "logic_desc": "말이나 추측의 유동성을 차단하고, 튼튼한(firmus) 대지 위에 구조물을 굳건히 고정하여 확립해 주는(confirm) 힘의 상태입니다.",
        "examples2": [
            {"en": "He is a confirmed bachelor and will never marry.", "ko": "그는 골수(만성적) 독신주의자라 결코 결혼하지 않을 것이다."},
            {"en": "Her appointment was confirmed by the board of directors.", "ko": "그녀의 임명은 이사회에 의해 정식 승인되었다(확인되었다)."}
        ],
        "feeling": "confirmed = 완전히(con) 단단하게(firm) 고정했다 = 사실로 확인했다 = 습관이 굳어 고질적인",
        "real_tip": "confer(의논하다, 부여하다), conform(순응하다) 등 철자가 유사한 단어들과 헷갈리기 쉬우니 주의해야 합니다.",
        "summary_flow": ["firmus 단단한", "confirmare 튼튼하게 다지다", "confirm 사실로 고정하다", "확인/확증해주었다", "버릇이 굳어 고질적인"],
        "quiz": [
            {"question": "The laboratory __________ the diagnosis of the rare disease.", "translation": "실험실은 그 희귀 질병의 진단을 확인해 주었다.", "answer": "confirmed"},
            {"question": "She has a __________ habit of drinking coffee before bed.", "translation": "그녀는 잠자리에 들기 전 커피를 마시는 고질적인(굳어진) 버릇이 있다.", "answer": "confirmed"}
        ]
    },
    {
        "word": "typical",
        "pronunciation": "TIP-i-kuhl",
        "meaning1": "전형적인, 대표적인 (도장을 찍어 박은 틀 모양 그대로인)",
        "meaning2": "늘 그렇듯 뻔한, 보통의 (추상적 행동의 전형)",
        "intro": "금속을 강하게 때려 만든 '도장 틀(type)'에서 어떻게 '전형적인'이라는 성격이 탄생했을까요?",
        "etymology": {
            "root1": "typ (Gk. typos : blow, dent, impression, mold / 내리침, 찍어낸 자국, 틀)",
            "root2": "-ical (Suffix : 형용사 접사)",
            "flow": ["내리쳐 찍어 낸 기준 형판이나 주형 틀", "틀에 맞추어 찍어 낸 듯한 꼴의", "전형적인, 대표적인 성질의", "늘상 겪어 예상되는 뻔한, 보통의"]
        },
        "examples1": [
            {"en": "Their AI program learned to imitate Rembrandt's typical characteristics.", "ko": "그들의 AI 프로그램은 렘브란트의 전형적인 특징들을 모방하는 법을 배웠다."},
            {"en": "This is a typical example of gothic architecture.", "ko": "이것은 고딕 건축의 전형적인 사례이다."}
        ],
        "transition_question": "금형의 기준이 되는 성질이 어떻게 사람의 행동을 비꼴 때 쓰는 \"뻔하고 보통인\"이 될까요?",
        "logic_flow": ["쇠붙이 표면에 강타를 입혀 똑같은 무늬를 박아 넣음 (typos)", "↓", "각 개체가 그 문양 주형에서 하나씩 찍혀 나옴", "↓", "이 범주에 속한 모든 것들이 공유하는 보편적 꼴 (전형적인)", "↓", "특별할 것 없이 매번 반복되는 뻔한 행동 습성", "↓", "늘 그렇듯 뻔한, 보통의"],
        "logic_desc": "주물럭대서 만든 게 아니라, 주형 틀(typos)에 쇳물을 부어 찍어 낸 것처럼 가장 표준적이고 전형적인(typical) 속성입니다.",
        "examples2": [
            {"en": "It is typical of him to forget his wallet.", "ko": "지갑을 잊어버리는 것은 그 사람답다(늘 그렇듯 뻔한 짓이다)."},
            {"en": "The weather was typical for this time of the year.", "ko": "날씨는 연중 이맘때의 보통 날씨였다."}
        ],
        "feeling": "typical = 도장 틀(type)로 찍어 낸 = 규격 그대로인 = 전형적인 = 늘 그렇듯 뻔한",
        "real_tip": "It is typical of A to부정사 구문은 'A가 ~하는 것은 전형적인 행동이다(참 A답다)'라는 의미의 서술형 빈출 문장입니다.",
        "summary_flow": ["typos 찍어낸 자국/틀", "typicus 전형을 묘사하는", "typical 틀에 맞춘", "전형적인/대표적인", "늘 그렇듯 뻔한"],
        "quiz": [
            {"question": "A __________ workday starts at nine and ends at five.", "translation": "전형적인 근무일은 9시에 시작해서 5시에 끝난다.", "answer": "typical"},
            {"question": "It is __________ of her to arrive early for every event.", "translation": "모든 행사마다 일찍 도착하는 것은 그녀답다(그녀의 전형적인 모습이다).", "answer": "typical"}
        ]
    },
    {
        "word": "distinct",
        "pronunciation": "dih-STINGKT",
        "meaning1": "뚜렷한, 명확한 (찔러 표시해 둔 것처럼 눈에 훤한)",
        "meaning2": "별개의, 전혀 다른 (경계와 분류가 완전히 갈라선)",
        "intro": "바늘로 '찔러서 자국을 내는' 어원이 어떻게 눈에 잘 띄는 '뚜렷함'과 완전히 다른 '별개'를 뜻하게 되었을까요?",
        "etymology": {
            "root1": "di- (L. dis- : apart / 갈라져, 따로)",
            "root2": "stinct (L. stinguere : to prick, stamp / 찔러 표시하다)",
            "flow": ["하나씩 찔러서 고유한 자국을 남기다", "윤곽이 포착하기에 몹시 훤하고 뚜렷한", "뚜렷한, 명백한", "서로 표시가 달라 하나로 뭉칠 수 없는 별개의, 전혀 다른"]
        },
        "examples1": [
            {"en": "This learning process enables a machine to discover distinct patterns.", "ko": "이 학습 과정은 기계가 뚜렷한 패턴들을 발견하는 것을 가능하게 한다."},
            {"en": "There is a distinct smell of gas in the kitchen.", "ko": "부엌에서 가스 냄새가 뚜렷하게(확연하게) 난다."}
        ],
        "transition_question": "눈에 잘 띄는 명확함이 어떻게 서로 섞이지 않는 \"독자적이고 전혀 다른\"이 될까요?",
        "logic_flow": ["무더기 속의 요소들을 하나하나 따로(dis) 바늘로 찌름(stinguere)", "↓", "각각의 개체 표면에 선명한 구멍 표식이 남음", "↓", "멀리서 보아도 형태가 뭉개지지 않고 선명함 (뚜렷한)", "↓", "표식이 완전히 달라 겹치지 않는 독자 영역 구축", "↓", "서로 별개의, 전혀 다른"],
        "logic_desc": "따로(dis) 분류 도장 자국(stinguere)을 찍어 묶어두었기 때문에, 시각적으로 흐릿하지 않고 뚜렷하며(distinct) 범주가 다른 것들과 섞이지 않고 쪼개집니다.",
        "examples2": [
            {"en": "The two plants are distinct species.", "ko": "그 두 식물은 전혀 다른(별개의) 종이다."},
            {"en": "She had the distinct impression that she was being followed.", "ko": "그녀는 누군가 자신을 미행하고 있다는 뚜렷한 느낌을 받았다."}
        ],
        "feeling": "distinct = 따로(dis) 찔러서(stinct) 박아둔 = 형태가 뚜렷한 = 경계가 쪼개진 별개의",
        "real_tip": "distinct(뚜렷한, 별개의)와 distinctive(독특한, 차이를 만드는)의 미세한 뉘앙스 차이를 묻는 변별력 문제가 종종 출제됩니다.",
        "summary_flow": ["stinguere 찌르다", "distinguere 갈라 찌르다", "distinctus 분리 표식된", "시각적/감각적 뚜렷한", "완전히 다른 별개의"],
        "quiz": [
            {"question": "He has a __________ advantage over other runners due to his height.", "translation": "그는 그의 키 덕분에 다른 주자들에 비해 뚜렷한 우위를 점하고 있다.", "answer": "distinct"},
            {"question": "The project is divided into three __________ phases.", "translation": "그 프로젝트는 세 개의 서로 다른(별개의) 단계로 나뉜다.", "answer": "distinct"}
        ]
    },
    {
        "word": "numerous",
        "pronunciation": "NOO-muh-ruhs",
        "meaning1": "수많은, 다수의 (숫자가 가득 채워져 많은)",
        "meaning2": "운율적인, 음악적인 (숫자적 비례가 가득 차 조화로운 - 문학적)",
        "intro": "가치와 서열을 재는 '숫자'에서 탄생한 단어가 왜 '수없이 많음'을 뜻하는 일상의 단어가 되었을까요?",
        "etymology": {
            "root1": "numer (L. numerus : number / 숫자, 비례, 리듬)",
            "root2": "-ous (Suffix : ~이 가득 찬)",
            "flow": ["양이 많아 손가락 숫자로 가득 채우다", "헤아리기 힘들 만큼 양이 풍성한", "수많은, 다수의", "수학적 비례와 박자가 맞아 조화로운 (음악적)"]
        },
        "examples1": [
            {"en": "The machine discovers patterns from numerous data.", "ko": "그 기계는 수많은 데이터로부터 패턴을 발견한다."},
            {"en": "She has won numerous awards for her research.", "ko": "그녀는 그녀의 연구로 수많은 상을 받았다."}
        ],
        "transition_question": "단순한 숫자가 어째서 영시(poetry)나 클래식 음악의 \"조화롭고 운율적인\" 느낌이 되었을까요?",
        "logic_flow": ["양을 재기 위해 하나씩 세어 나가는 숫자 (numerus)", "↓", "자릿수가 가득 차서(ous) 쏟아질 정도로 부피가 큼", "↓", "수없이 많은, 다수의", "↓", "소절의 음절 숫자와 비례 박자가 정확히 맞아떨어짐", "↓", "운율이 아름답고 음악적인"],
        "logic_desc": "셀 수 있는 단위의 수치(numerus)가 무수하게 누적되어 가득 차(ous) 있는 양적 광대함과, 리듬의 정밀한 조화(박자)를 상징합니다.",
        "examples2": [
            {"en": "His prose was admired for its numerous cadence.", "ko": "그의 산문은 조화로운(운율적인) 가락으로 찬사를 받았다."},
            {"en": "Numerous studies have shown the benefits of exercise.", "ko": "수많은 연구가 운동의 이점을 보여주었다."}
        ],
        "feeling": "numerous = 자릿수(number)가 가득 찬(ous) = 헤아리기 벅찬 = 수많은 = 박자가 조화로운",
        "real_tip": "many보다 격식 있고 풍성한 뉘앙스를 주며, 'a number of'나 'innumerable'과 동의어로 출제됩니다.",
        "summary_flow": ["numerus 숫자/비례", "numerosus 숫자가 가득한/풍성한", "numerous 수많은", "양의 방대함", "조화로운/운율적인"],
        "quiz": [
            {"question": "Despite __________ attempts, he failed to pass the driving test.", "translation": "수많은 시도에도 불구하고, 그는 운전면허 시험 통과에 실패했다.", "answer": "numerous"},
            {"question": "There are __________ ways to solve this mathematical puzzle.", "translation": "이 수학 퍼즐을 풀 수 있는 수많은 방법이 존재한다.", "answer": "numerous"}
        ]
    },
    {
        "word": "eventually",
        "pronunciation": "ih-VEN-choo-uh-lee",
        "meaning1": "결국, 마침내 (우여곡절 끝에 밖으로 쏟아진 결과선)",
        "meaning2": "최종적으로, 궁극적으로 (논리적 종착지)",
        "intro": "사건들이 '밖으로 다 흘러나오는' 최종 상태가 어떻게 시간의 종점인 '마침내'가 되었을까요?",
        "etymology": {
            "root1": "event (L. e- : out / 바깥으로 + ven : venire : to come / 오다)",
            "root2": "-ual + -ly (Adverb Suffix)",
            "flow": ["일이 밖으로 다 흘러나와 정착하다", "발생한 사건(event)의 종점에 가 닿다", "우여곡절의 마침표를 찍으며 결국", "논리적 인과의 최종적 마감"]
        },
        "examples1": [
            {"en": "Photography eventually came to be seen as art.", "ko": "사진은 결국 예술로 여겨지게 되었다."},
            {"en": "Keep trying, and you will eventually succeed.", "ko": "계속 시도해라, 그러면 너는 결국 성공할 것이다."}
        ],
        "transition_question": "사건들의 흘러나옴이 어떻게 논쟁의 종지부인 \"최종적 귀결\"이 될까요?",
        "logic_flow": ["여러 시도와 원인들이 밖으로(ex) 흘러나옴(venire)", "↓", "각종 사건과 우여곡절이 연쇄적으로 발발함 (events)", "↓", "시간의 흐름이 마지막 종착 터미널에 당도함", "↓", "결국, 마침내 (긴 기다림의 마감)", "↓", "최종적이고 궁극적인 귀결"],
        "logic_desc": "시간의 터널 속에 갇혀 있던 사건의 결말들이 바깥으로(ex) 완전히 마중 나와(venire) 마침표를 찍는 마감(eventual)의 양상입니다.",
        "examples2": [
            {"en": "The dispute was eventually settled in court.", "ko": "그 분쟁은 결국 법정에서 해결되었다."},
            {"en": "This decision will eventually lead to the company's downfall.", "ko": "이 결정은 결국 회사의 몰락을 초래할 것이다."}
        ],
        "feeling": "eventually = 사건들(event)이 밖으로 다 솟아나온 끝에 = 마침내 = 최종적으로",
        "real_tip": "finally와 비슷하지만, eventually는 '중간에 수많은 사건과 지연이 있었고 그 오랜 끝에 마침내'라는 뉘앙스가 가미됩니다.",
        "summary_flow": ["venire 오다", "evenire 밖으로 오다/발생하다", "eventus 결과/사건", "eventual 최종 결과의", "eventually 결국, 마침내"],
        "quiz": [
            {"question": "He will __________ realize the truth of my words.", "translation": "그는 결국 내 말의 진실을 깨닫게 될 것이다.", "answer": "eventually"},
            {"question": "The old building was __________ demolished for safety.", "translation": "그 오래된 건물은 안전을 위해 결국 철거되었다.", "answer": "eventually"}
        ]
    },
    {
        "word": "imitate",
        "pronunciation": "IM-i-teyt",
        "meaning1": "모방하다, 흉내 내다 (외형과 동작을 그대로 베끼다)",
        "meaning2": "본받다, 모범으로 삼다 (추상적 품성과 정신의 계승)",
        "intro": "상대의 외형을 '본뜨는 것'이 어떻게 내면의 가치를 '본받다'라는 지고한 행동이 될까요?",
        "etymology": {
            "root1": "imi (L. imitari : to copy, portray / 따라하다, 본뜨다)",
            "root2": "-ate (Suffix : 동사 접사)",
            "flow": ["대상의 외형과 실루엣을 그대로 본뜨다", "동작이나 음성을 기계적으로 흉내 내다", "모방하다, 카피하다", "위대한 모델의 품성을 닮으려 본받다"]
        },
        "examples1": [
            {"en": "Their AI program learned to imitate Rembrandt's typical characteristics.", "ko": "그들의 AI 프로그램은 렘브란트의 전형적인 특징들을 모방하는 법을 배웠다."},
            {"en": "Parrots can imitate human speech.", "ko": "앵무새들은 인간의 말을 흉내 낼 수 있다."}
        ],
        "transition_question": "껍데기를 흉내 내는 카피가 어떻게 훌륭한 삶을 \"본받는\" 인격화가 될까요?",
        "logic_flow": ["원본의 실루엣 이미지(image)를 대조함", "↓", "내 행동 양식을 원본의 외형과 겹치게 고침 (imitari)", "↓", "작가의 기법이나 목소리를 복제함 (모방하다)", "↓", "인격적으로 존경하는 스승의 도덕적 양식을 따라 살아가려 애씀", "↓", "본받다, 모범으로 삼다"],
        "logic_desc": "거울(image)에 대상을 그대로 비추어 복사하듯(imitari), 겉보기 형태의 카피(모방)에서 내재적 자질의 학습(본받음)으로 개념의 층위가 깊어집니다.",
        "examples2": [
            {"en": "We should imitate the virtues of great leaders.", "ko": "우리는 위대한 지도자들의 덕목을 본받아야 한다."},
            {"en": "The child tried to imitate her father's walk.", "ko": "그 아이는 아빠의 걸음걸이를 흉내 내려고 노력했다."}
        ],
        "feeling": "imitate = 원본의 실루엣 이미지(imi)를 그대로 베끼다 = 흉내 내다 = 본받다",
        "real_tip": "명사형인 imitation은 '모방' 외에도 '인조의, 모조품(짝퉁)'이라는 명사/형용사로도 널리 쓰입니다.",
        "summary_flow": ["imago 모사/이미지", "imitari 따라하다", "imitate 모방하다", "흉내 내다", "인격을 본받다"],
        "quiz": [
            {"question": "Artists often __________ their masters in the early stages.", "translation": "예술가들은 종종 초기 단계에 그들의 스승을 모방한다.", "answer": "imitate"},
            {"question": "It is better to be original than to __________ others.", "translation": "다른 사람을 모방하는 것보다 독창적인 것이 낫다.", "answer": "imitate"}
        ]
    },
    {
        "word": "oppose",
        "pronunciation": "uh-POHZ",
        "meaning1": "반대하다 (맞은편에 벽을 세워 방해하다)",
        "meaning2": "대항하다, 대비시키다 (논리적 짝을 맞춰 대조함)",
        "intro": "상대의 눈앞에 '가로막고 놓는' 몸짓이 어떻게 정책을 반대하는 '대항'이 되었을까요?",
        "etymology": {
            "root1": "op- (L. ob- : against, in front of / 반대하여, 맞은편에)",
            "root2": "pose (L. ponere : to place, put / 놓다, 두다)",
            "flow": ["상대의 행동 경로 맞은편에 나를 두다", "나아가지 못하도록 굳건히 가로막다", "의견이나 결의안을 반대하다", "논리를 대치시켜 대비시키다"]
        },
        "examples1": [
            {"en": "Some people oppose AI art because it might steal data.", "ko": "어떤 사람들은 AI 예술이 데이터를 훔칠 수 있어서 반대한다."},
            {"en": "The citizens oppose the construction of the landfill.", "ko": "시민들은 쓰레기 매립지 건설을 반대한다."}
        ],
        "transition_question": "몸으로 길목을 막아서는 행동이 어떻게 이론을 \"대비/대치\"시키는 지적 대조가 될까요?",
        "logic_flow": ["공격자의 진군로 정면에(ob) 무거운 돌 장벽을 가져다 놓음(ponere)", "↓", "상대의 힘과 나의 힘이 충돌하여 멈춰 섬", "↓", "의견이나 정책에 찬성하지 않고 가로막음 (반대하다)", "↓", "두 개의 상반된 개념을 마주 보게 세워 대조함", "↓", "대비시키다, 대치하다"],
        "logic_desc": "상대의 의지와 정반대 방향(ob)으로 대칭점을 설정해 놓는(ponere) 거부의 구도로, 반대(opposition)와 대조(contrast)의 중심 원리입니다.",
        "examples2": [
            {"en": "The author prefers to oppose theory to practice.", "ko": "저자는 이론을 실제에 대비시키는(대조하는) 것을 선호한다."},
            {"en": "Most parents oppose the school's new dress code.", "ko": "대부분의 학부모는 학교의 새로운 복장 규정에 반대한다."}
        ],
        "feeling": "oppose = 가로막고 맞서(ob) 두다(pose) = 대열을 가로막다 = 반대하다 = 대비하다",
        "real_tip": "be opposed to(~에 반대하다) 구문은 to가 전치사여서 뒤에 동명사가 오며, oppose 자체는 타동사여서 목적어를 바로 취합니다.",
        "summary_flow": ["ponere 두다", "opponere 맞은편에 두다", "oppose 반대하다", "의견 저지", "대치/대비시키다"],
        "quiz": [
            {"question": "They strongly __________ the proposed law change.", "translation": "그들은 제안된 법률 개정에 강력히 반대한다.", "answer": "oppose"},
            {"question": "We must __________ these two ideas to understand their differences.", "translation": "우리는 그 둘의 차이를 이해하기 위해 이 두 아이디어를 대비시켜야(대치해야) 한다.", "answer": "oppose"}
        ]
    },
    {
        "word": "copyright",
        "pronunciation": "KAH-pee-ryt",
        "meaning1": "저작권, 판권 (창작물을 복제하여 퍼뜨릴 수 있는 합법적 독점 권리)",
        "meaning2": "저작권법의 보호를 받는 (형용사적 의미)",
        "intro": "복사를 뜻하는 'copy'와 올바름을 뜻하는 'right'가 만나 어떻게 현대 예술가들을 보호하는 '저작권'이 되었을까요?",
        "etymology": {
            "root1": "copy (L. copia : abundance, transcript / 풍요, 복제물)",
            "root2": "right (OE. riht : straight, rule / 곧음, 올바른 권리)",
            "flow": ["다량의 인쇄 복제물(copia)을 찍어 낼 수 있는", "법률이 보장하는 올바른 독점 권한(right)", "저작권, 판권", "저작권을 취득하다 (동사)"]
        },
        "examples1": [
            {"en": "AI can steal the data of human art without respecting copyright.", "ko": "AI는 저작권을 존중하지 않고 인간 예술의 데이터를 훔칠 수 있다."},
            {"en": "The author owns the copyright to this book.", "ko": "저자는 이 책에 대한 저작권을 소유하고 있다."}
        ],
        "transition_question": "인쇄 권리를 뜻하는 저작권이 어떻게 인터넷 시대의 \"지적 재산\"이 되었을까요?",
        "logic_flow": ["풍요롭게 복사하여 전파할 권리 (copy-right)", "↓", "인쇄 기술의 출현 이후 무단 복제를 단속할 법적 필요성", "↓", "창작자의 원본에 대한 인격적/재산적 권리 규정", "↓", "저작권, 지적 재산권"],
        "logic_desc": "책이나 예술품을 다량으로 복제(copy)하여 유통할 수 있는 올바른 독점 법적 권리(right)를 명문화한 단어입니다.",
        "examples2": [
            {"en": "The video was removed due to a copyright violation.", "ko": "그 비디오는 저작권 위반으로 인해 삭제되었다."},
            {"en": "All materials on this website are protected by copyright.", "ko": "이 웹사이트의 모든 자료는 저작권의 보호를 받는다."}
        ],
        "feeling": "copyright = 복제할(copy) 올바른 권리(right) = 원본 창작자 소유권 = 저작권",
        "real_tip": "copyleft(카피레프트)는 copyright의 반대로, '지적 재산을 공유하고 개방해야 한다'는 반대 운동을 지칭합니다.",
        "summary_flow": ["copia 풍요/복사", "riht 올곧음/권리", "copyright 복제 독점권", "무단 복제 방지", "지적 재산 보호 저작권"],
        "quiz": [
            {"question": "He was sued for __________ infringement after using the song.", "translation": "그는 그 노래를 사용한 후 저작권 침해로 소송을 당했다.", "answer": "copyright"},
            {"question": "Who holds the __________ for this film?", "translation": "이 영화의 저작권은 누가 쥐고 있습니까?", "answer": "copyright"}
        ]
    },
    {
        "word": "mimicking",
        "pronunciation": "MIM-ik-ing",
        "meaning1": "흉내 내기, 모방하기 (광대 연극처럼 외양을 똑같이 카피하는 것)",
        "meaning2": "모방하는, 흡사하게 만드는 (형용사/분사)",
        "intro": "그리스 무대의 '광대'를 가리키던 단어가 어떻게 컴퓨터 공학에서 스타일을 '모방하기'가 되었을까요?",
        "etymology": {
            "root1": "mimic (Gk. mimos : actor, mime / 무대 위 광대, 마임 배우)",
            "root2": "-ing (Suffix : 동명사 접사)",
            "flow": ["광대가 무대에서 우스꽝스럽게 얼굴을 베끼다", "대상의 특성을 장난치듯 따라 하다", "흉내 내기, 모방하기", "생물의 형태나 화학 성질을 똑같이 모사하는"]
        },
        "examples1": [
            {"en": "They trained themselves by learning and mimicking styles.", "ko": "그들은 스타일을 배우고 모방함으로써(흉내 냄으로써) 스스로를 훈련했다."},
            {"en": "The computer program is mimicking human handwriting.", "ko": "그 컴퓨터 프로그램은 인간의 필체를 흉내 내고(모방하고) 있다."}
        ],
        "transition_question": "광대의 익살스러운 흉내 내기가 어떻게 생물의 \"의태/모사\"라는 과학 용어가 되었을까요?",
        "logic_flow": ["무언가를 똑같이 카피하는 몸짓 광대 (mimos)", "↓", "희화화하여 표정과 언어를 그대로 재현함", "↓", "동작이나 스타일의 정교한 카피 (흉내 내기)", "↓", "생물이 천적을 속이기 위해 나뭇잎 색깔을 닮아감 (의태, 모사)"],
        "logic_desc": "마임 광대(mimos)가 원본 대상을 관찰하여 자신의 육체 위에 똑같이 포장해 복사(mimic)해 내는 카피 행위를 지칭합니다.",
        "examples2": [
            {"en": "The insects escape predators by mimicking twigs.", "ko": "그 곤충들은 나뭇가지를 흉내 냄(의태함)으로써 포식자들을 피한다."},
            {"en": "Her mimicking of the teacher's voice was perfect.", "ko": "선생님 목소리를 따라 한 그녀의 흉내 내기는 완벽했다."}
        ],
        "feeling": "mimicking = 마임 광대(mimic)가 그대로 따라 함 = 모방하기 = 위장과 의태",
        "real_tip": "mimic에 ing를 붙일 때 철자 규칙상 k가 삽입되어 mimicking(m-i-m-i-c-k-i-n-g)이 됨을 확실히 알아야 어형 시험을 맞춥니다.",
        "summary_flow": ["mimos 판토마임 배우", "mimicus 광대의/흉내 내는", "mimic 흉내 내다", "k 삽입 및 -ing 결합", "모방하기/흉내 내기"],
        "quiz": [
            {"question": "Some birds are famous for __________ other sounds.", "translation": "어떤 새들은 다른 소리들을 흉내 내는(모방하는) 것으로 유명하다.", "answer": "mimicking"},
            {"question": "The software is designed for __________ database activity.", "translation": "그 소프트웨어는 데이터베이스 활동을 모방하기(시뮬레이션하기) 위해 설계되었다.", "answer": "mimicking"}
        ]
    },
    {
        "word": "ethical",
        "pronunciation": "ETH-i-kuhl",
        "meaning1": "윤리적인, 도덕적인 (공동체 습속과 정품에 부합하는)",
        "meaning2": "정당한, 정직한 (사회적 행동 기준에 올바른)",
        "intro": "공동체가 오랜 세월 지켜온 '습관'을 뜻하는 단어가 어떻게 '윤리적인'이라는 무거운 뜻이 되었을까요?",
        "etymology": {
            "root1": "eth (Gk. ethos : custom, character, habit / 관습, 성품, 기질)",
            "root2": "-ical (Suffix : 형용사 접사)",
            "flow": ["공동체가 다 함께 오랫동안 지켜온 풍습과 관례", "사회의 안정과 질서를 위해 마땅히 지켜야 할 품성", "도덕적인, 윤리적인", "합당하고 정의로운"]
        },
        "examples1": [
            {"en": "AI raises ethical, social, or emotional questions.", "ko": "AI는 윤리적, 사회적, 또는 정서적 질문을 제기한다."},
            {"en": "Doctors must adhere to high ethical standards.", "ko": "의사들은 높은 윤리적 기준을 준수해야 한다."}
        ],
        "transition_question": "오랜 습속이 어떻게 비즈니스나 과학 연구의 \"올바르고 정당함\"의 잣대가 될까요?",
        "logic_flow": ["마을 구성원들이 함께 굳힌 행동 습관 (ethos)", "↓", "개인에게 내면화된 고결한 기질과 성품", "↓", "무엇이 옳고 그른지 분별하는 사회적 행동 규범 (도덕)", "↓", "양심에 부합하여 올바르고 정당한 (윤리적인)"],
        "logic_desc": "개인의 고립된 도덕이 아니라, 사회 공동체 전체가 합의해 온 올바른 습관(ethos)의 궤적에 부합하는 윤리(ethical)를 의미합니다.",
        "examples2": [
            {"en": "Is it ethical to keep animals in zoos?", "ko": "동물을 동물원에 가두어 두는 것이 윤리적인가?"},
            {"en": "The company won an award for ethical business practices.", "ko": "그 회사는 도덕적(윤리적)인 경영 행위로 상을 받았다."}
        ],
        "feeling": "ethical = 오랜 도덕적 습속(ethos)에 입각한 = 도덕적인 = 양심상 정당한",
        "real_tip": "ethnic(민족의)과 매우 철자가 흡사하여 어휘 선택 문제에 자주 짝꿍으로 묶여 출제됩니다.",
        "summary_flow": ["ethos 습속/성품", "ethicus 도덕에 관한", "ethical 규범에 맞는", "도덕적인", "정당한/윤리적인"],
        "quiz": [
            {"question": "Testing cosmetics on animals is not __________.", "translation": "화장품을 동물에 테스트하는 것은 윤리적이지 않다.", "answer": "ethical"},
            {"question": "He resigned due to an __________ dilemma.", "translation": "그는 윤리적인 딜레마(고민) 때문에 사임했다.", "answer": "ethical"}
        ]
    },
    {
        "word": "thrilled",
        "pronunciation": "thrild",
        "meaning1": "감격하게 했다, 전율케 했다 (송곳으로 뼈를 관통하듯 세차게 뚫다)",
        "meaning2": "아주 기쁘게 했다, 짜릿하게 했다 (추상적 대단한 만족감)",
        "intro": "뾰족한 송곳으로 구멍을 '뚫는' 아픈 행동이 어떻게 '대단히 감격하고 신나다'가 되었을까요?",
        "etymology": {
            "root1": "thrill (OE. thyrlean : to pierce, drill / 찌르다, 구멍을 뚫다)",
            "root2": "-ed (Suffix : 과거형/과거분사)",
            "flow": ["송곳이나 드릴로 찔러 구멍을 내 통과하다", "뼈나 내장을 관통하는 듯한 찌릿한 충격", "짜릿한 전율과 흥분감을 자아냈다", "감격하게 했다, 열광시켰다"]
        },
        "examples1": [
            {"en": "An incident occurred that thrilled the contemporary art scene.", "ko": "현대 미술계를 뒤흔든(전율케 한) 사건이 발생했다."},
            {"en": "The music thrilled the crowd and made them dance.", "ko": "그 음악은 대중을 전율케 했고(감격시켰고) 그들을 춤추게 했다."}
        ],
        "transition_question": "전율의 관통이 어떻게 일상에서 \"엄청 신나고 기분 좋다\"라는 뜻이 되었을까요?",
        "logic_flow": ["송곳으로 두꺼운 가죽이나 벽을 찌름 (pierce)", "↓", "감각 기관 전체에 구멍이 뚫린 듯한 강렬한 스파크", "↓", "온몸이 부르르 떨리는 짜릿한 전율 (thrill)", "↓", "의식이 완전히 매료되어 날아갈 듯 신남", "↓", "아주 기쁘게 했다, 감격하게 했다"],
        "logic_desc": "심장의 벽을 관통하는(thrill) 듯한 날카롭고 강렬한 지적/감각적 스파크(전율)를 안겨주어 감격(thrilled)시키는 행위입니다.",
        "examples2": [
            {"en": "She was thrilled to receive the invitation.", "ko": "그녀는 초대장을 받고 매우 기뻤다(감격했다)."},
            {"en": "He was thrilled by the prospect of traveling around the world.", "ko": "그는 세계 일주를 한다는 전망에 몹시 흥분했다(신이 났다)."}
        ],
        "feeling": "thrilled = 뼈를 관통하듯 세차게 찔린 = 전율을 느끼는 = 몹시 흥분되고 감격한",
        "real_tip": "감정 유발 동사의 과거분사형이므로, '사람이 주어로 쓰일 때' 몹시 신난 기분을 나타내기 위해 thrilled(p.p.)형태로 쓰입니다.",
        "summary_flow": ["thyril 구멍", "thyrelian 구멍을 뚫다", "thrill 관통하여 찌르다/전율시키다", "과거형 적용", "전율케 했다/감격시켰다"],
        "quiz": [
            {"question": "I was __________ to bits when I won the lottery.", "translation": "나는 복권에 당첨되었을 때 정말 뛸 듯이 기뻤다(감격했다).", "answer": "thrilled"},
            {"question": "The news __________ the fans of the football club.", "translation": "그 소식은 그 축구 클럽의 팬들을 열광시켰다(감격하게 했다).", "answer": "thrilled"}
        ]
    },
    {
        "word": "examined",
        "pronunciation": "ig-ZAM-ind",
        "meaning1": "조사했다, 검토했다 (저울 바늘을 보고 무게를 정밀하게 재다)",
        "meaning2": "시험했다, 진찰했다 (추상적 건강/실력을 가름)",
        "intro": "저울의 '바늘 눈금'을 보며 꼼꼼히 영점을 잡는 행위가 어떻게 '조사하고 시험하다'가 되었을까요?",
        "etymology": {
            "root1": "examin (L. examen : tongue of a balance / 저울대의 지시 바늘, 시험)",
            "root2": "-ed (Suffix : 과거형/과거분사)",
            "flow": ["저울 바늘의 미세한 흔들림을 유심히 지켜보다", "무게의 오차가 없는지 정밀하게 재다", "꼼꼼히 검토했다, 조사했다", "환자를 진찰하거나 학생을 시험했다"]
        },
        "examples1": [
            {"en": "They thoroughly examined the painting to make sure.", "ko": "그들은 확실히 하기 위해 그림을 철저히 조사했다(검토했다)."},
            {"en": "The customs officer examined the luggage closely.", "ko": "세관원이 수화물을 면밀히 조사했다."}
        ],
        "transition_question": "저울 바늘을 대조하는 검토가 어떻게 병원에서의 \"진찰\"과 학교의 \"시험\"이 되었을까요?",
        "logic_flow": ["좌우 수평이 정밀하게 맞아떨어지는지 저울 지시침(examen)을 봄", "↓", "의혹의 1g조차 허용하지 않겠다는 면밀한 태도", "↓", "흠결이 있는지 서류와 제품의 안팎을 대조함 (조사했다)", "↓", "사람의 내재된 질병이나 두뇌 역량의 눈금을 저울질함", "↓", "진찰했다, 시험했다"],
        "logic_desc": "저울(examen)에 대상을 얹어놓고 눈금 바늘이 가리키는 진실의 무게를 정밀 대조하여 가늠(examine)한 역사입니다.",
        "examples2": [
            {"en": "The doctor examined the patient's throat.", "ko": "의사가 환자의 목구멍을 진찰했다(검사했다)."},
            {"en": "Students were examined on their knowledge of chemistry.", "ko": "학생들은 화학 지식에 대해 시험을 치렀다(검증받았다)."}
        ],
        "feeling": "examined = 저울대 눈금(examin)을 보며 영점을 맞췄다 = 대조했다 = 철저히 검토/조사했다",
        "real_tip": "closely, carefully, thoroughly 등 '자세히'를 뜻하는 부사 수식어들과 한 짝으로 독해 지문에 빈출됩니다.",
        "summary_flow": ["exigere 몰아내다/측정하다", "examen 저울 눈금 바늘", "examinare 저울질하다", "examine 조사하다", "과거형 examined"],
        "quiz": [
            {"question": "The detective __________ the footprints left on the mud.", "translation": "그 형사는 진흙 위에 남겨진 발자국들을 조사했다.", "answer": "examined"},
            {"question": "Every candidate will be __________ by the panel.", "translation": "모든 지원자들은 면접 위원단에 의해 검토(시험)받을 것이다.", "answer": "examined"}
        ]
    },
    {
        "word": "characteristics",
        "pronunciation": "kair-ik-tuh-RIS-tiks",
        "meaning1": "특징들, 특성들 (도구로 깊이 새겨 굳힌 자국들)",
        "meaning2": "성격, 기질 (인물의 내면적 독특함)",
        "intro": "돌판이나 쇠붙이에 '글자를 새기다'라는 행동이 어떻게 인간 고유의 '특징'이 되었을까요?",
        "etymology": {
            "root1": "charact (Gk. kharassein : to engrave, sharp point / 예리한 칼끝으로 문양을 긁어 새기다)",
            "root2": "-istic (Suffix : 성질의) + -s (Plural)",
            "flow": ["예리한 도구로 돌이나 금속판 위에 지워지지 않게 깎아 판 무늬", "대상을 고유하게 구별해 주는 도장 낙인 자국", "고유 특징들, 특성들", "인격이나 기질"]
        },
        "examples1": [
            {"en": "Their AI program learned to imitate Rembrandt's typical characteristics.", "ko": "그들의 AI 프로그램은 렘브란트의 전형적인 특징들을 모방하는 법을 배웠다."},
            {"en": "What are the physical characteristics of the wolf?", "ko": "늑대의 신체적 특징들(특성들)은 무엇입니까?"}
        ],
        "transition_question": "단단한 판에 낙인을 새기는 것이 어떻게 사람의 눈에 안 보이는 \"성격/기질\"이 될까요?",
        "logic_flow": ["날카로운 칼끝으로 표면을 깊이 긁어(kharassein) 홈을 파냄", "↓", "바람이 불고 씻겨도 지워지지 않는 영구적 문양 (낙인)", "↓", "다른 사물과 즉각 구분되게 만드는 외형적 요소 (특징들)", "↓", "인생의 습관들이 뇌와 몸에 영구적으로 새겨진 내면의 꼴", "↓", "성격, 기질"],
        "logic_desc": "사물이나 사람의 가슴 위에 칼로 깎아 새겨 놓은(engrave) 것 같은, 지워지지 않는 고유의 식별선(characteristics)들을 지칭합니다.",
        "examples2": [
            {"en": "Generosity is one of her best characteristics.", "ko": "관대함은 그녀의 가장 좋은 성격(특성)들 중 하나이다."},
            {"en": "We must analyze the genetic characteristics of the plant.", "ko": "우리는 그 식물의 유전적 특성들을 분석해야 한다."}
        ],
        "feeling": "characteristics = 지워지지 않게 칼로 푹 파서 새겨(charact) 둔 고유 무늬 = 특징들 = 기질",
        "real_tip": "feature, trait, attribute, property 등 '특성'을 나타내는 동의어 군단과 함께 고등학교 어휘 시험의 단골 출제 어휘입니다.",
        "summary_flow": ["kharassein 새기다", "kharakter 새겨진 도장 문양/성격", "characteristic 특징적인", "복수화 characteristics", "고유 특성들/기질"],
        "quiz": [
            {"question": "The program can analyze the unique __________ of human voice.", "translation": "그 프로그램은 인간 목소리의 독특한 특징들을 분석할 수 있다.", "answer": "characteristics"},
            {"question": "The main __________ of this product is its durability.", "translation": "이 제품의 주요 특성은 내구성이다. (단수형: characteristic)", "answer": "characteristic"}
        ]
    },
    {
        "word": "creativity",
        "pronunciation": "kree-ey-TIV-i-tee",
        "meaning1": "창의성, 창조력 (무에서 유의 새로운 실체를 낳아 기르는 힘)",
        "meaning2": "창작성 (독창적으로 엮어내는 역량)",
        "intro": "생명이 '자라나게 만든다'는 어원이 어떻게 현대 디자인의 '창의성'이 되었을까요?",
        "etymology": {
            "root1": "creat (L. creare : to bring forth, make, grow / 낳다, 자라나게 하다)",
            "root2": "-ivity (Suffix : 성질, 작용력)",
            "flow": ["무에서 유의 생명을 낳고 양육하여 자라게 하다", "세상에 없던 새로운 형체와 질서를 부여하여 만들다", "창조적인 상태, 창조력", "예술적/지적 창의성, 독창성"]
        },
        "examples1": [
            {"en": "Let us look at the mechanism of AI creativity.", "ko": "AI 창의성(창조력)의 작동 원리를 살펴보자."},
            {"en": "Her creativity allows her to solve problems in unique ways.", "ko": "그녀의 창의성은 그녀가 독특한 방식으로 문제를 해결하도록 돕는다."}
        ],
        "transition_question": "생명을 출산하고 기르는 힘이 어떻게 비즈니스의 \"아이디어 발상(창의성)\"이 되었을까요?",
        "logic_flow": ["어머니가 태아를 잉태하고 세상 밖으로 낳음(creare)", "↓", "황무지에 식물의 씨앗을 심어 크게 기름", "↓", "정신계에서 기존 단서들을 조합해 세상에 없던 새 아이디어를 낳음", "↓", "예술과 공학을 수립하는 독창적인 힘 (창의성)"],
        "logic_desc": "아이를 낳고 나무를 키우듯(creare), 영혼의 무(無)의 상태에서 쓸모 있고 아름다운 유(有)의 가치를 낳아 자라게 하는 정신의 출산력(creativity)입니다.",
        "examples2": [
            {"en": "The project designed to foster children's creativity.", "ko": "그 프로젝트는 아이들의 창의성을 기르기 위해 설계되었다."},
            {"en": "Advertising requires a high degree of creativity.", "ko": "광고업은 높은 수준의 창의성을 요구한다."}
        ],
        "feeling": "creativity = 생명을 낳아(create) 기르는 성질 = 무에서 유를 조형함 = 창의성 = 창작력",
        "real_tip": "creative(창의적인), creation(창조물), creator(창조자) 등 다양한 파생어의 철자와 뜻을 함께 확인해야 합니다.",
        "summary_flow": ["creare 낳다/기르다", "creativus 창조적 효능의", "creative 창조적인", "-ity 결합", "창의성 / 창조력"],
        "quiz": [
            {"question": "AI lacks the emotional __________ of human artists.", "translation": "AI는 인간 예술가들이 가진 감정적 창의성이 결여되어 있다.", "answer": "creativity"},
            {"question": "Encouraging play can boost a child's __________.", "translation": "놀이를 장려하는 것은 아이의 창의성을 촉진할 수 있다.", "answer": "creativity"}
        ]
    },
    {
        "word": "inspiration",
        "pronunciation": "in-spuh-REY-shuhn",
        "meaning1": "영감, 직관 (신이 흙 인형에 생명의 숨결을 안으로 불어넣다)",
        "meaning2": "영감을 주는 존재/사물 (행동을 유발하는 자극제)",
        "intro": "공기를 '안으로 들이쉬는' 단순한 호흡이 어떻게 예술가의 번뜩이는 '영감'이 되었을까요?",
        "etymology": {
            "root1": "in- (L. in- : into / 안으로)",
            "root2": "spir (L. spirare : to breathe / 숨을 쉬다, 호흡하다) + -ation",
            "flow": ["몸속 내부 안으로 신선한 공기를 들이마시다", "신적인 기운이나 생명의 숨을 가슴속에 유입시키다", "번뜩이는 창조적 아이디어의 강림, 영감", "행동을 촉구하게 이끄는 훌륭한 자극제"]
        },
        "examples1": [
            {"en": "AI can be a powerful source of inspiration for artists.", "ko": "AI는 예술가들에게 강력한 영감의 원천이 될 수 있다."},
            {"en": "The poet found inspiration in the beauty of nature.", "ko": "그 시인은 대자연의 아름다움 속에서 영감을 찾았다."}
        ],
        "transition_question": "숨을 들이쉬는 생리 활동이 어떻게 사람의 행동을 고무하는 \"자극제\"가 되었을까요?",
        "logic_flow": ["밀폐된 내면의 공간에 바늘구멍을 뚫음", "↓", "바깥에 흐르던 산소 기운을 안으로(in) 세차게 빨아들임(spirare)", "↓", "차가운 바람이 머리에 닿아 번뜩이는 의식의 각성을 줌 (영감)", "↓", "게으른 심장을 강제로 박동하게 만듦", "↓", "행동을 자극하는 고마운 존재 / 자극제"],
        "logic_desc": "외부의 신선하고 거룩한 숨결(spirare)을 내 영혼 속으로(in-) 들이마셔, 의식을 깨우고 작품을 창작할 시동을 거는 번뜩임(inspiration)입니다.",
        "examples2": [
            {"en": "Her mother was a lifelong inspiration to her writing career.", "ko": "그녀의 어머니는 그녀의 집필 경력에 평생 동안 영감을 주는 존재(자극제)였다."},
            {"en": "The designer got his inspiration from traditional costumes.", "ko": "그 디자이너는 전통 의상으로부터 영감을 얻었다."}
        ],
        "feeling": "inspiration = 영혼 안으로(in) 들이쉬는 숨결(spir) = 지혜의 번뜩임 = 영감 = 자극제",
        "real_tip": "inspire(영감을 주다), conspiracy(음모-함께 숨 쉬며 수군거림), expire(만료되다-숨이 밖으로 나가 끊어짐) 등 spir 패밀리를 연계해 외웁니다.",
        "summary_flow": ["spirare 숨 쉬다", "inspirare 안으로 숨을 불어넣다", "inspiratio 신성한 숨결이 닿음", "영감", "자극제 / 영감을 주는 것"],
        "quiz": [
            {"question": "He needs a sudden spark of __________ to finish the song.", "translation": "그는 그 노래를 끝마치기 위해 갑작스러운 영감의 불꽃이 필요하다.", "answer": "inspiration"},
            {"question": "The museum is full of __________ for young painters.", "translation": "그 미술관은 젊은 화가들에게 영감을 주는 존재들(자극제)로 가득하다.", "answer": "inspiration"}
        ]
    },
    {
        "word": "valid",
        "pronunciation": "VAL-id",
        "meaning1": "유효한, 법적으로 힘이 있는 (힘이 세고 가치를 유지하는)",
        "meaning2": "타당한, 근거가 튼튼한 (논리적으로 반박 불가한 힘)",
        "intro": "'몸이 튼튼하고 건강하다'는 단어가 왜 법원에서는 '유효한 계약'이 되고 토론에서는 '타당하다'가 될까요?",
        "etymology": {
            "root1": "val (L. valere : to be strong, healthy / 힘이 세다, 가치 있다)",
            "root2": "-id (Suffix : 형용사 접사)",
            "flow": ["물리적 신체가 튼튼하고 쇠붙이가 강한", "법률적인 칼자루를 쥐어 구속력을 행사할 수 있는", "유효한, 효력이 있는", "논리적 근거가 정합하여 설득력 있는, 타당한"]
        },
        "examples1": [
            {"en": "Although our question is still valid, AI is helpful.", "ko": "비록 우리의 질문이 여전히 유효하지만(타당하지만), AI는 도움이 된다."},
            {"en": "Your ticket is no longer valid after the expiry date.", "ko": "당신의 티켓은 만료일 이후에는 더 이상 유효하지 않다."}
        ],
        "transition_question": "법적인 효력이 살아있음이 어떻게 논쟁에서의 \"타당하고 논리적인\" 뜻으로 쓰일까요?",
        "logic_flow": ["근육이 굵고 힘이 세어(valere) 상대를 제압함", "↓", "서류나 합의안이 깨지지 않고 굳건히 효력을 행사함 (유효한)", "↓", "논쟁에서 상대의 공격 칼날을 부러뜨리는 강도를 지님", "↓", "반론을 제기하기 어려운 탄탄하게 타당한"],
        "logic_desc": "흐물흐물해져서 버려지는(invalid) 상태가 아니라, 뼈대가 굵어 힘이 단단히 차 있는(valere) 상태여서 구속력과 논리력(valid)을 지니고 있음을 뜻합니다.",
        "examples2": [
            {"en": "You raised a valid point during the discussion.", "ko": "너는 토론 중에 타당한(논리적인) 지적을 제기했다."},
            {"en": "The contract is legally valid in this state.", "ko": "그 계약은 이 주에서 법적으로 유효하다."}
        ],
        "feeling": "valid = 힘이 세어(val) 깨지지 않는 = 유효한 = 논리가 탄탄하여 타당한",
        "real_tip": "반대말은 invalid이며, 명사형 validity(타당성/유효성), 동사형 validate(입증하다/비준하다)도 빈출 어휘입니다.",
        "summary_flow": ["valere 힘이 세다/가치 있다", "validus 강한/유효한", "valid 효력이 남아 있는", "법적 유효한", "논리적 타당한"],
        "quiz": [
            {"question": "Do you have a __________ reason for being absent?", "translation": "당신은 결석한 것에 대해 타당한(합당한) 이유가 있습니까?", "answer": "valid"},
            {"question": "A passport must be __________ for at least six months to travel.", "translation": "여행을 하려면 여권이 최소 6개월 동안은 유효해야 한다.", "answer": "valid"}
        ]
    },
    {
        "word": "authorship",
        "pronunciation": "AW-ther-ship",
        "meaning1": "원작자임, 저자 권한 (생각의 생명을 세상에 싹트게 한 시초자의 권위)",
        "meaning2": "저술 작업, 출처 (책의 근원 지분)",
        "intro": "자라나게 한다는 어원의 'author'에 자격을 뜻하는 '-ship'이 붙어 어떻게 '원작자의 지위'가 되었을까요?",
        "etymology": {
            "root1": "auth (L. augere : to increase, create / 자라나게 하다, 낳다, 창조하다)",
            "root2": "-ship (Suffix : 자격, 신분, 관계)",
            "flow": ["사상이나 이야기를 처음 세상에 낳아 싹 틔운 자 (author)", "그 사상을 기르고 관리할 권한을 지닌 주체의 자격 (-ship)", "원작자임, 저자 신분", "책이나 예술품의 기원/출처"]
        },
        "examples1": [
            {"en": "Artists usually sign their works to show authorship.", "ko": "예술가들은 대개 그들이 원작자임을 나타내기 위해 그들의 작품에 서명한다."},
            {"en": "The authorship of the anonymous letter is still debated.", "ko": "그 익명 편지의 원작자(누가 썼는지)는 여전히 논란 중이다."}
        ],
        "transition_question": "누가 창작했는지 밝히는 원작자 신분이 어떻게 문학의 \"저술 활동과 출처\"로 쓰일까요?",
        "logic_flow": ["머릿속 아이디어를 세상 밖으로 탄생시켜 키움 (augere)", "↓", "이 사상적 생명체의 주권을 쥔 아버지가 됨 (author)", "↓", "내가 처음 창작했다는 법적 독점 자격과 관계 수립 (-ship)", "↓", "원작자임 / 저작 권한", "↓", "이 텍스트가 누구의 붓끝에서 나왔는지의 출처"],
        "logic_desc": "문장이나 예술의 싹을 틔워 자라게(augere) 만든 시초자(author)의 법적 신분 및 기원성(authorship)을 일컫는 고난도 학술 개념입니다.",
        "examples2": [
            {"en": "We must verify the authorship of the medieval manuscript.", "ko": "우리는 그 중세 필사본의 원작자(출처)를 검증해야 한다."},
            {"en": "She claimed joint authorship of the research paper.", "ko": "그녀는 그 연구 논문의 공동 저자 자격(공동 저술권)을 주장했다."}
        ],
        "feeling": "authorship = 싹 틔워 자라게 한 자(author)의 자격(-ship) = 원작자임 = 글의 출처",
        "real_tip": "authority(권위/당국)와 author(저자)가 동일한 어근(augere : 키우다)에서 뻗어 나왔음을 연계해 인지하면 암기가 수월합니다.",
        "summary_flow": ["augere 기르다/창조하다", "auctor 창시자/저자", "author 저술가", "-ship 자격 접사 결합", "원작자임/저자 자격"],
        "quiz": [
            {"question": "The museum confirmed the __________ of the painting.", "translation": "그 미술관은 그 그림의 원작자(누구의 작품인지)를 확인했다.", "answer": "authorship"},
            {"question": "He was granted sole __________ of the software code.", "translation": "그는 그 소프트웨어 코드에 대한 단독 저자 권한을 부여받았다.", "answer": "authorship"}
        ]
    },
    {
        "word": "legal",
        "pronunciation": "LEE-guhl",
        "meaning1": "법적인, 사법상의 (사회적 룰인 법률의 테두리에 엮인)",
        "meaning2": "합법적인, 법률에 입각한 (위법이 없는 타당함)",
        "intro": "공동체가 꼿꼿이 세워둔 '법률(lex)'이 어떻게 우리의 정당함을 증명하는 '합법적인'이 될까요?",
        "etymology": {
            "root1": "leg (L. lex : law / 성문 법률, 사회적 규칙)",
            "root2": "-al (Suffix : 형용사 접사)",
            "flow": ["사법적 장치로 고정된 사회적 규약(lex)의", "법원과 재판 절차에 부합하는 (법적인)", "위법하여 처벌받지 않는 안전선 내부의 (합법적인)", "법률이 허용하는"]
        },
        "examples1": [
            {"en": "More companies ask for legal protection of the artworks.", "ko": "더 많은 기업들이 그 예술작품에 대한 법적 보호를 요청한다."},
            {"en": "They are seeking legal advice from a lawyer.", "ko": "그들은 변호사로부터 법적 조언을 구하고 있다."}
        ],
        "transition_question": "사법과 연관된다는 의미가 어떻게 행동의 \"합법성(올바름)\"으로 번졌을까요?",
        "logic_flow": ["시민 평의회가 굳건히 수립한 성문법 조항 (lex)", "↓", "개인 간의 마찰을 이 조항의 잣대로 끌고 가 판정함 (법적인)", "↓", "법의 그물망을 찢지 않고 규정을 완벽히 지킨 상태", "↓", "사법적 하자가 전혀 없는 (합법적인)"],
        "logic_desc": "임의의 판단이 아니라, 공식적으로 제정되어 세워진 성문법(lex)의 테두리 안에서 움직이는 규칙성(legal)을 의미합니다.",
        "examples2": [
            {"en": "Is it legal to record phone calls without consent?", "ko": "동의 없이 전화 통화를 녹음하는 것이 합법적인가?"},
            {"en": "The document has no legal force in this country.", "ko": "그 문서는 이 나라에서 어떠한 법적 효력도 지니지 않는다."}
        ],
        "feeling": "legal = 법률(lex)에 묶인 = 법원의 = 법을 잘 지킨 합법의",
        "real_tip": "illegal은 '불법의'로 반대말이며, legislate(입법하다), legitimate(합법적인/적법한)도 lex 어근에서 나온 일가족입니다.",
        "summary_flow": ["lex 법률", "legalis 법률에 정해진", "legal 사법의", "법적인 조치", "법이 허용한 합법의"],
        "quiz": [
            {"question": "They take __________ action against copyright violators.", "translation": "그들은 저작권 위반자들에 대해 법적인 조치를 취한다.", "answer": "legal"},
            {"question": "It is __________ to drive a car without a license.", "translation": "면허 없이 운전하는 것은 불법(illegal)이다.", "answer": "illegal"}
        ]
    },
    {
        "word": "undertook",
        "pronunciation": "uhn-der-TOOK",
        "meaning1": "착수했다, 떠맡았다 (무거운 과업 밑으로 들어가 손으로 받다)",
        "meaning2": "약속했다, 보증했다 (추상적 완수 계약을 짊어짐)",
        "intro": "영어 단어 'under(아래에)'와 'take(쥐다)'가 결합하여 어떻게 힘든 일에 '착수하다'가 되었을까요?",
        "etymology": {
            "root1": "under (OE. under : beneath, among / 밑에, 과업의 수렁 속에)",
            "root2": "took (OE. tacan : to take / 손으로 쥐다, 받다)",
            "flow": ["무거운 돌짐의 아래(under)로 기어들어가 양손으로 짊어지다(take)", "자신의 어깨에 책임을 얹고 일을 개시하다", "착수했다, 떠맡았다", "책임을 지고 이행할 것을 서약했다"]
        },
        "examples1": [
            {"en": "However, it is not clear who undertook the arrangements.", "ko": "그러나 누가 그 업무 조치(준비)들을 맡았는지는 명확하지 않다."},
            {"en": "She undertook the difficult task of organizing the festival.", "ko": "그녀는 축제를 조직하는 어려운 업무를 떠맡았다(착수했다)."}
        ],
        "transition_question": "짐을 떠맡는 육체 행동이 어떻게 계약서상의 \"보증하다, 서약하다\"가 되었을까요?",
        "logic_flow": ["수렁처럼 덮쳐오는 중압감의 아래(under) 영역", "↓", "피하지 않고 그 하중을 내 팔로 움켜잡아(take) 견딤", "↓", "공식적으로 책임을 가지고 일을 지휘하기 시작함 (착수했다)", "↓", "이 과업을 중간에 도망치지 않고 끝까지 해내겠다고 만인에게 언명함", "↓", "서약했다, 보증했다"],
        "logic_desc": "굴러떨어지는 무거운 통나무(과업)의 아랫방향(under)으로 기어 들어가, 자기 어깨로 그 통나무를 받아(take) 메고 걷기 시작하는 결단의 행동입니다.",
        "examples2": [
            {"en": "The doctor undertook to cure the patient.", "ko": "의사는 그 환자를 치료하겠다고 약속했다(서약했다)."},
            {"en": "We undertook a thorough review of the system.", "ko": "우리는 그 시스템에 대한 철저한 검토에 착수했다."}
        ],
        "feeling": "undertook = 짐의 아래로(under) 들어가 몸으로 받았다(take) = 책임을 맡았다 = 착수했다",
        "real_tip": "undertake의 과거형이며, 명사형인 undertaking은 '인수, 기업, 장례업'이라는 특수한 비즈니스 뜻을 가집니다.",
        "summary_flow": ["under 밑에", "tacan 쥐다/잡다", "undertake 책임을 맡다", "과거형 적용 undertook", "착수했다 / 보증했다"],
        "quiz": [
            {"question": "He __________ the responsibility of leading the team.", "translation": "그는 그 팀을 이끄는 책임을 떠맡았다(착수했다).", "answer": "undertook"},
            {"question": "They __________ to finish the construction within a year.", "translation": "그들은 1년 이내에 건설을 끝마치겠다고 약속했다(서약했다).", "answer": "undertook"}
        ]
    },
    {
        "word": "funded",
        "pronunciation": "FUHN-did",
        "meaning1": "자금을 지원했다 (사업의 바닥 기초 토대를 놓아주다)",
        "meaning2": "기금이 적립된, 적립 방식의 (금융적 의미)",
        "intro": "그릇의 '바닥'을 뜻하는 단어가 어떻게 프로젝트를 굴리는 '자금을 대주다'가 되었을까요?",
        "etymology": {
            "root1": "fund (L. fundus : bottom, base, foundation / 바닥, 기초, 토대)",
            "root2": "-ed (Suffix : 과거/과거분사 접사)",
            "flow": ["바닥 기초(fundus) 토대를 튼튼히 세우다", "사업이 주저앉지 않게 돈줄의 기초를 깔아주다", "자금을 대주었다, 재정 지원했다", "기금을 축적하여 준비한"]
        },
        "examples1": [
            {"en": "It could be the people who organized or funded the project.", "ko": "그것은 그 프로젝트를 조직하거나 자금을 지원한 사람일 수 있다."},
            {"en": "The research was funded by a government grant.", "ko": "그 연구는 정부 보조금에 의해 자금이 지원되었다."}
        ],
        "transition_question": "돈을 대는 재정 지원이 어떻게 연금 금융의 \"적립식 기금화\"가 될까요?",
        "logic_flow": ["빈 그릇의 맨 밑바닥(fundus)을 은화로 채워 넣음", "↓", "사업이 모래성처럼 주저앉지 않게 든든한 주춧돌을 세움", "↓", "필요한 모든 자재 비용을 대주다 (자금을 지원했다)", "↓", "미래에 찾아 쓸 수 있게 기금을 항아리 바닥에 계속 모아 둠", "↓", "기금이 적립된"],
        "logic_desc": "돈줄이 말라 공중분해 되지 않도록, 재정의 단단한 주춧돌 기초(fundus)를 현금으로 깔아 채워주는(funded) 인과입니다.",
        "examples2": [
            {"en": "The pension scheme is fully funded.", "ko": "그 연금 제도는 완전히 기금이 적립되어 있다(적립 방식이다)."},
            {"en": "They funded the new library building.", "ko": "그들은 새 도서관 건물의 자금을 대주었다(기부했다)."}
        ],
        "feeling": "funded = 바닥 토대(fund)를 든든하게 다져 주었다 = 돈을 대주었다 = 자금을 지원했다",
        "real_tip": "fund(기금/자금을 대다), fundamental(근본적인/바닥 기초의), refund(환불하다-돈을 바닥으로 돌려보냄)을 함께 묶어 공부합니다.",
        "summary_flow": ["fundus 바닥/기초", "fund 기금을 모으다/자금을 대다", "funded 자금 지원을 받은", "과거동사형", "자금을 지원했다 / 기금이 적립된"],
        "quiz": [
            {"question": "The study was __________ by a group of private investors.", "translation": "그 연구는 사적 투자자 집단에 의해 자금이 지원되었다.", "answer": "funded"},
            {"question": "Who __________ the construction of this bridge?", "translation": "이 다리의 건설 자금을 누가 대주었습니까(지원했습니까)?", "answer": "funded"}
        ]
    },
    {
        "word": "discovered",
        "pronunciation": "dih-SKUHV-erd",
        "meaning1": "발견되었다, 발견했다 (상자 뚜껑 가림막을 찢어 벗기다)",
        "meaning2": "깨닫게 되었다, 알게 되었다 (추상적 진실을 자각함)",
        "intro": "상자 위를 꽁꽁 싸맨 '덮개(cover)'를 '벗겨내는(dis)' 행동이 어떻게 과학과 보물선 '발견'이 되었을까요?",
        "etymology": {
            "root1": "dis- (L. dis- : un-, opposite / 반대, 떼어내다)",
            "root2": "covered (L. cooperire : to cover / 덮어씌운, 가려진) + -ed",
            "flow": ["유물을 덮고 있던 덮개(cover)를 찢어 버리다(dis)", "숨겨져 보이지 않던 보물이나 땅을 드러내다", "발견되었다, 찾아냈다", "숨은 자연의 진실이나 지식을 머리로 깨닫게 되었다"]
        },
        "examples1": [
            {"en": "An unknown painting had been discovered!", "ko": "정체불명의 그림이 발견되었다!"},
            {"en": "Columbus discovered America in 1492.", "ko": "콜럼버스는 1492년에 아메리카를 발견했다."}
        ],
        "transition_question": "유물을 찾아 덮개를 벗기는 눈의 발견이 어떻게 정신적인 \"깨달음/자각\"이 될까요?",
        "logic_flow": ["흙더미나 천막(cover) 속에 보물이 갇혀 보이지 않음", "↓", "장막을 거칠게 걷어내고(dis) 빛 아래 실물을 노출시킴", "↓", "인류 지도에 좌표를 정식 등록함 (발견하다)", "↓", "내 무지의 눈꺼풀 장막을 걷고 진실을 마주함", "↓", "머릿속으로 알게 되다, 깨닫다"],
        "logic_desc": "가려져 보이지 않던 대상 위에 덮인 장막(cover)을 걷어 던져서(dis-), 세상에 존재를 폭로하고 알아내는(discover) 행위입니다.",
        "examples2": [
            {"en": "He discovered that he had a talent for cooking.", "ko": "그는 자신에게 요리 재능이 있음을 깨달았다(알게 되었다)."},
            {"en": "Scientists discovered a new planet yesterday.", "ko": "과학자들은 어제 새로운 행성을 발견했다."}
        ],
        "feeling": "discovered = 덮개(cover)를 뜯어 젖혔다(dis) = 보물을 찾아냈다 = 발견했다 = 깨달았다",
        "real_tip": "invention은 없던 걸 만드는 '발명'이고, discovery는 원래 실재하던 가림막을 벗기는 '발견'으로 구별합니다.",
        "summary_flow": ["cooperire 덮다", "discooperire 덮개를 벗기다", "discover 발견하다", "과거/과거분사형", "발견되었다 / 깨달았다"],
        "quiz": [
            {"question": "Gold was __________ in California in 1848.", "translation": "1848년 캘리포니아에서 금이 발견되었다.", "answer": "discovered"},
            {"question": "I __________ that the shop was already closed.", "translation": "나는 그 상점이 이미 문을 닫았음을 깨달았다(알게 되었다).", "answer": "discovered"}
        ]
    },
    {
        "word": "presented",
        "pronunciation": "prih-ZEN-tid",
        "meaning1": "제시했다, 제출했다 (상대의 바로 앞에 존재를 갖다 놓다)",
        "meaning2": "발표했다, 선사했다 (선물을 정식 주다, 연극을 상연하다)",
        "intro": "상대의 눈동자 '바로 앞(pre)'에 물건을 '존재하게(sent)' 하는 행동이 어떻게 보고서 '제출'과 감동적인 '선물'이 되었을까요?",
        "etymology": {
            "root1": "pre- (L. prae- : before / 앞에, 마주하여)",
            "root2": "sent (L. esse : to be / 실재하다, 존재하다) + -ed",
            "flow": ["심사관 눈동자 바로 앞에(prae) 실물을 가져다 두다", "의견이나 보고서를 대면하여 내밀다", "제시했다, 제출했다", "선물을 선사하다 / 대중에게 연극을 보여주다"]
        },
        "examples1": [
            {"en": "They immediately presented a video showing the AI's process.", "ko": "그들은 즉시 AI의 제작 과정을 보여주는 비디오를 제시했다."},
            {"en": "The winner was presented with a gold medal.", "ko": "우승자에게 금메달이 선사되었다(제공되었다)."}
        ],
        "transition_question": "눈앞에 물건을 들이미는 제시가 어떻게 생일을 축하하는 \"선물(present)\"이 되었을까요?",
        "logic_flow": ["손수 준비한 진귀한 진상품", "↓", "왕이나 수장 바로 앞(prae)의 시선 아래 놓아 존재(esse)하게 함", "↓", "의견이나 데이터 기획안을 내놓음 (제시했다)", "↓", "정성껏 포장하여 타인에게 무상으로 건네줌 (선물하다)"],
        "logic_desc": "부재(absence)하던 대상을, 타인의 시야 정면(pre-)으로 끄집어내어 당당히 실재(presence)하게 가져다 놓는 적극적 대면(presentation)입니다.",
        "examples2": [
            {"en": "He presented his ID card at the security gate.", "ko": "그는 보안 게이트에서 자신의 신분증을 제시했다(보여주었다)."},
            {"en": "The theater group presented a new play last night.", "ko": "그 극단은 어젯밤 새 연극을 선보였다(상연했다)."}
        ],
        "feeling": "presented = 눈앞에(pre) 있게(sent) 만들었다 = 내밀어 보여주었다 = 제시했다 = 선사했다",
        "real_tip": "present는 동사로 '제시하다', 명사로 '선물/현재', 형용사로 '현재의/참석한'으로 다채롭게 쓰여 다의어 문제에 무조건 출제됩니다.",
        "summary_flow": ["esse 존재하다", "praesentare 마주 두다", "present 내놓다/선물하다", "과거/과거분사형", "제시했다/선사했다"],
        "quiz": [
            {"question": "She __________ her research findings at the conference.", "translation": "그녀는 컨퍼런스에서 자신의 연구 결과를 발표했다(제시했다).", "answer": "presented"},
            {"question": "The document must be __________ within ten days.", "translation": "그 문서는 10일 이내에 제출되어야(제시되어야) 한다.", "answer": "presented"}
        ]
    },
    {
        "word": "enables",
        "pronunciation": "ih-NEY-buhlz",
        "meaning1": "가능하게 하다, 작동하게 만들다 (할 수 있는 능력 상태로 조율함)",
        "meaning2": "승인하다, 자격을 주다 (법적/시스템적 기능 해제)",
        "intro": "능력이 '있다(able)'는 말 앞에 '만들다(en)'를 붙여 어떻게 프로그램이 '기능을 작동하다'가 되었을까요?",
        "etymology": {
            "root1": "en- (L. in- : make, put in / ~화하다, 채우다)",
            "root2": "able (L. habilis : handy, fit, able / 편리한, 할 수 있는) + -s",
            "flow": ["손에 맞춤해 다룰 능력이 있게 만들다", "불능 상태의 가림막을 걷어내다", "가능하게 하다, 촉진하다", "사용 승인하여 권한을 부여하다"]
        },
        "examples1": [
            {"en": "This learning process enables a machine to discover patterns.", "ko": "이 학습 과정은 기계가 패턴을 발견하는 것을 가능하게 한다."},
            {"en": "The new law enables citizens to vote online.", "ko": "그 새 법률은 시민들이 온라인으로 투표하는 것을 가능하게 한다."}
        ],
        "transition_question": "능력을 열어주는 가능케 함이 어떻게 IT 기기의 \"기능 활성화(enable)\"가 되었을까요?",
        "logic_flow": ["기술이나 힘이 없어 꽁꽁 잠겨 멈춰 선 개체", "↓", "자원과 자격을 공급해 할 수 있는(able) 상태로 밀어 올림(en)", "↓", "장벽을 돌파하고 주체가 실현하게 함 (가능하게 하다)", "↓", "잠금 설정된 메뉴의 스위치를 켜서 시스템을 기동함", "↓", "승인하다, 활성화하다"],
        "logic_desc": "주체가 한계를 뚫고 행동할 수 있는 합당한 성품이나 도구(habilis)를 갖추도록 강제로 세팅해(en-) 활로를 열어주는 동력 공급입니다.",
        "examples2": [
            {"en": "The setting enables the dark mode on your phone.", "ko": "그 설정은 당신의 휴대폰에서 다크 모드를 활성화한다(가능케 한다)."},
            {"en": "Microscopes enable scientists to observe tiny cells.", "ko": "현미경은 과학자들이 미세한 세포를 관찰하는 것을 가능하게 한다."}
        ],
        "feeling": "enables = 할 수 있게(able) 기동시킨다(en) = 잠금을 해제해 작동시킴 = 가능하게 하다",
        "real_tip": "enable은 5형식 동사 기출 1순위로, 'enable + 목적어 + to부정사' 구조를 취하여 '~가 ~하는 것을 가능케 하다'로 출제됩니다.",
        "summary_flow": ["habilis 손에 익은/유능한", "able 할 수 있는", "enable 할 수 있게 만들다", "단수형 적용 enables", "가능하게 하다/활성화하다"],
        "quiz": [
            {"question": "Wealth __________ him to travel wherever he wants.", "translation": "부는 그가 원하는 곳은 어디든 여행하는 것을 가능하게 한다.", "answer": "enables"},
            {"question": "This feature __________ users to back up data automatically.", "translation": "이 기능은 사용자들이 데이터를 자동으로 백업하는 것을 가능하게 한다.", "answer": "enables"}
        ]
    },
    {
        "word": "protection",
        "pronunciation": "pruh-TEK-shuhn",
        "meaning1": "보호, 방어 (위험이 날아오는 정면에 지붕 덮개를 씌움)",
        "meaning2": "보호 조치, 보호 무역 (추상적 사회 보호막)",
        "intro": "공격이 날아오는 '앞에(pro)' '지붕(tect)'을 얹는 물리적 방어가 어떻게 특허의 '법적 보호'가 되었을까요?",
        "etymology": {
            "root1": "pro- (L. pro- : in front of, forward / 앞에, 마주하여)",
            "root2": "tect (L. tegere : to cover / 지붕을 씌우다, 덮다) + -ion",
            "flow": ["공격이 날아오는 방향 정면에 가림막 지붕을 두다", "비바람이나 칼날의 타격이 몸에 닿지 않게 가리다", "물리적 보호, 방어", "지적 재산이나 자국 기업을 방어하는 법적 보호 조치"]
        },
        "examples1": [
            {"en": "More and more companies ask for legal protection of the artworks.", "ko": "점점 더 많은 기업들이 예술작품에 대한 법적 보호를 요청한다."},
            {"en": "The helmet provides protection for your head.", "ko": "헬멧은 당신의 머리에 대한 보호(방어)를 제공한다."},
            {"en": "More and more companies, developers, and artists ask for legal protection.", "ko": "더 많은 기업, 개발자, 예술가들이 법적 보호를 요구한다."}
        ],
        "transition_question": "물리적 방패를 세우는 방어가 어떻게 사법 제도의 \"특허 및 보호 무역\"이 될까요?",
        "logic_flow": ["위험물이나 자외선이 위에서 쏟아짐", "↓", "자극이 강타하는 지점의 바로 앞(pro)에 덮개(tegere)를 가로지름", "↓", "직접 타격을 차단해 내부 생명을 건짐 (보호)", "↓", "시장 경쟁이나 카피범의 침입을 법 조항의 울타리로 방어함", "↓", "특허권 보호 / 관세 장벽 (보호 조치)"],
        "logic_desc": "위험을 직면(pro)하여 머리 위에 튼튼한 지붕(tegere)을 올려, 아래의 연약한 실체를 무사히 수호해 주는 차단막(protection)입니다.",
        "examples2": [
            {"en": "Environmental protection is a key global issue.", "ko": "환경 보호는 핵심적인 글로벌 쟁점이다."},
            {"en": "Tariffs were introduced as a protection for domestic industries.", "ko": "관세는 국내 산업들을 위한 보호 조치로 도입되었다."}
        ],
        "feeling": "protection = 내 앞(pro)에 지붕(tect)을 얹은 것 = 장막 방어막 = 물리적 보호 = 법적 장치",
        "real_tip": "protect(보호하다), protective(보호하는), protectiveness(보호 성향) 등 파생어 명사 규격을 확인하십시오.",
        "summary_flow": ["tegere 덮다/지붕 씌우다", "protegere 정면에 덮개를 두다", "protects 보호하다", "명사화 접사 protection", "물리적 보호 / 법적 보호 조치"],
        "quiz": [
            {"question": "Wear sunscreen to provide __________ against UV rays.", "translation": "자외선에 대한 보호(차단)를 제공하기 위해 자외선 차단제를 바르세요.", "answer": "protection"},
            {"question": "The patent offers legal __________ to the inventor.", "translation": "그 특허는 발명가에게 법적 보호를 제공한다.", "answer": "protection"}
        ]
    },
    {
        "word": "organized",
        "pronunciation": "AWR-guh-nyzd",
        "meaning1": "조직했다, 구성했다 (도구와 신체 장기들을 하나로 묶다)",
        "meaning2": "체계적인, 정리된 (형용사로서 꼼꼼하고 규칙적인 상태)",
        "intro": "생명체의 '장기(organ)'나 '도구'를 뜻하는 단어가 어떻게 '조직했다'와 '체계적인'이 되었을까요?",
        "etymology": {
            "root1": "organ (Gk. organon : tool, instrument, bodily organ / 도구, 신체 장기)",
            "root2": "-ize + -ed (Suffix : 동사 과거형 / 형용사)",
            "flow": ["각각의 도구와 신체 장기들을 목적에 맞춰 배열하다", "제각기 흩어진 부품을 결합해 기능하게 조립하다", "조직했다, 결성했다", "체계가 조밀하게 정리된"]
        },
        "examples1": [
            {"en": "It could be the people who organized or funded the project.", "ko": "그것은 그 프로젝트를 조직하거나 자금을 지원한 사람일 수 있다."},
            {"en": "They organized a protest against the new policy.", "ko": "그들은 새로운 정책에 반대하는 시위를 조직(구성)했다."}
        ],
        "transition_question": "부품을 조립해 결성하는 조직화가 어떻게 사람의 성격이 \"꼼꼼하고 정리된\"이 될까요?",
        "logic_flow": ["제각각 노는 파편화된 도구(organon)들", "↓", "각 기기가 제 기능을 하도록 배치하여 파이프라인을 엮음", "↓", "하나의 공동 목적을 가진 거대한 생명체로 조립함 (조직했다)", "↓", "정신이나 책상 위가 서랍별로 흐트러짐 없이 정돈됨", "↓", "체계적인, 정리정돈이 잘 된"],
        "logic_desc": "따로 움직이면 찌꺼기일 뿐인 도구와 장기(organon)를, 생명 작동의 톱니바퀴처럼 일사불란하게 정렬하여 구성(organize)해 낸 결과물입니다.",
        "examples2": [
            {"en": "She is a very organized person who plans everything.", "ko": "그녀는 모든 것을 계획하는 매우 체계적인(정리정돈을 잘 하는) 사람이다."},
            {"en": "The charity organized a food drive for the homeless.", "ko": "그 자선단체는 노숙자들을 위한 음식 모으기 행사를 조직했다."}
        ],
        "feeling": "organized = 부품 장기(organ)들을 맞물려 결합했다 = 조직했다 = 정리정돈이 잘 된 체계적인",
        "real_tip": "organ(장기/오르간), organism(유기체/생물), organization(조직/기관)도 다 organon(도구)에서 파생된 한 집안 식구들입니다.",
        "summary_flow": ["organon 도구/신체 장기", "organisare 유기적으로 연결하다", "organize 조직하다", "과거동사형 organized", "조직했다 / 체계정리된"],
        "quiz": [
            {"question": "We __________ a surprise birthday party for our mom.", "translation": "우리는 엄마를 위해 깜짝 생일 파티를 준비했다(조직했다).", "answer": "organized"},
            {"question": "Keep your computer files __________ in folders.", "translation": "당신의 컴퓨터 파일들을 폴더별로 체계적으로 정리된(정돈된) 상태로 유지하세요.", "answer": "organized"}
        ]
    }
]

# JSON 파일 저장
json_path = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/vocab_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(vocab_list, f, ensure_ascii=False, indent=4)

print(f"Lesson 4 Vocab Data generation complete. Saved at {json_path}")
