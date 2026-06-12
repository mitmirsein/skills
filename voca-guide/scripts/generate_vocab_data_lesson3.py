import json
import os

vocab_list = [
    {
        "word": "react",
        "pronunciation": "ree-AKT",
        "meaning1": "반응하다 (물리적 작용에 대한 반작용)",
        "meaning2": "반발하다, 대항하다 (추상적 반대 의사)",
        "intro": "물리적인 '반작용'이 어떻게 마음의 '반발과 대항'이라는 의미로 확장될까요?",
        "etymology": {
            "root1": "re- (L. re- : back, again / 뒤로, 다시)",
            "root2": "act (L. agere : to do, drive / 행동하다, 구동하다)",
            "flow": ["뒤로 다시 행동하다", "가해진 작용에 대해 맞받아 행동함", "물리적으로 반응하다", "심리적/사회적으로 거부감을 갖고 반발하다"]
        },
        "examples1": [
            {"en": "How would you react if you saw a robot?", "ko": "만약 당신이 로봇을 본다면 어떻게 반응하겠습니까?"},
            {"en": "Iron reacts with oxygen to form rust.", "ko": "철은 산소와 반응하여 녹을 형성한다."}
        ],
        "transition_question": "물질이나 신체의 반응이 어떻게 사회적인 \"반발\"이 되었을까요?",
        "logic_flow": ["외부의 자극이 주어짐", "↓", "그에 대응하여 반대 방향으로 힘을 보냄 (반작용)", "↓", "외부의 지시나 변화에 대해 심리적 거부감을 드러냄", "↓", "반발하다, 대항하다"],
        "logic_desc": "외부의 작용(action)에 대해 반대(re-)로 되받아치는 물리적 힘의 원리가 사람의 태도나 사회적 반발로 확장된 것입니다.",
        "examples2": [
            {"en": "Voters reacted against the tax increase.", "ko": "유권자들은 세금 인상에 대해 반발했다."},
            {"en": "She reacted strongly to the criticism.", "ko": "그녀는 비판에 대해 강하게 반발했다."}
        ],
        "feeling": "react = 다시(re-) 행동하다(act) = 맞받아 반응함 = 거부하고 반발함",
        "real_tip": "react는 자동사이므로 전치사 to(~에 반응하다) 또는 against(~에 반발하다)와 짝꿍으로 자주 쓰입니다.",
        "summary_flow": ["agere 행동하다", "react 맞받아 행동하다", "물리적 반응", "심리적 반대", "반발/대항"],
        "quiz": [
            {"question": "The public will __________ negatively to the news.", "translation": "대중은 그 소식에 부정적으로 반응할 것이다.", "answer": "react"},
            {"question": "Local communities are starting to __________ against the construction.", "translation": "지역 공동체들이 그 건설에 반발하기 시작하고 있다.", "answer": "react"}
        ]
    },
    {
        "word": "probably",
        "pronunciation": "PRAH-buh-blee",
        "meaning1": "아마도 (추측)",
        "meaning2": "십중팔구, 그럴듯하게 (논리적 개연성)",
        "intro": "'증명할 수 있다'는 단단한 의미가 왜 불확실한 추측인 '아마도'가 되었을까요?",
        "etymology": {
            "root1": "prob (L. probare : to test, prove / 시험하다, 증명하다)",
            "root2": "-able (Suffix : 할 수 있는) + -ly (Adverb Suffix)",
            "flow": ["시험을 거쳐 증명할 수 있게", "참이 될 가능성이 매우 높게", "어떤 일이 일어날 개연성이 큰", "아마도, 십중팔구"]
        },
        "examples1": [
            {"en": "You would probably look around the front of your car.", "ko": "당신은 아마도 당신의 차 앞을 둘러볼 것이다."},
            {"en": "They will probably arrive before dinner.", "ko": "그들은 아마도 저녁 식사 전에 도착할 것이다."}
        ],
        "transition_question": "증명 가능하다는 단어가 어떻게 높은 수준의 개연성인 \"십중팔구\"가 되었을까요?",
        "logic_flow": ["실험과 시험을 거쳐 증명해 냄 (prove)", "↓", "검증을 통과하여 참으로 믿을 만함", "↓", "논리적 근거로 보아 실현 가능성이 80% 이상임", "↓", "십중팔구, 그럴듯하게"],
        "logic_desc": "검증이나 증명(prove)을 견뎌낼 수 있을 만큼 타당성이 높다는 뜻에서 '확률이 매우 높은 추측'으로 변모했습니다.",
        "examples2": [
            {"en": "He is probably the best candidate for the job.", "ko": "그는 십중팔구 그 자리에 가장 적합한 후보자다."},
            {"en": "This is probably where the rumor started.", "ko": "이곳이 십중팔구 소문이 시작된 곳일 것이다."}
        ],
        "feeling": "probably = 증명될 수 있는(probable) = 높은 확률로 참인 = 아마도 / 십중팔구",
        "real_tip": "부사 probably는 maybe보다 확신의 정도(약 80%)가 훨씬 높습니다. 독해 시 화자의 강한 확신을 나타냅니다.",
        "summary_flow": ["probare 증명하다", "probable 증명 가능한", "probably 증명 가능하게", "추상적 개연성", "아마도, 십중팔구"],
        "quiz": [
            {"question": "It will __________ rain tomorrow, so bring an umbrella.", "translation": "내일은 아마도 비가 올 것이니 우산을 챙기세요.", "answer": "probably"},
            {"question": "She was __________ the most talented writer of her time.", "translation": "그녀는 십중팔구 당대 가장 재능 있는 작가였을 것이다.", "answer": "probably"}
        ]
    },
    {
        "word": "momentarily",
        "pronunciation": "moh-muhn-TER-uh-lee",
        "meaning1": "순간적으로, 잠깐 (시간적 찰나)",
        "meaning2": "곧, 금방 (미래의 즉각성)",
        "intro": "'아주 잠깐'을 뜻하는 부사가 어떻게 '곧, 금방'이라는 미래의 즉각성으로 연결될까요?",
        "etymology": {
            "root1": "moment (L. momentum : movement, moving power / 순간, 물리적 추진력)",
            "root2": "-ary (Suffix : ~에 관한) + -ly (Adverb Suffix)",
            "flow": ["저울을 움직이는 미세한 추진력", "눈 깜짝할 순간의 찰나", "순간적으로, 일시적으로", "바로 이 순간에 이어서 '곧, 금방'"]
        },
        "examples1": [
            {"en": "You would be confused momentarily, but laugh soon.", "ko": "당신은 잠깐 동안 혼란스럽겠지만 이내 웃을 것이다."},
            {"en": "The power went out momentarily during the storm.", "ko": "폭풍우 동안 전기가 일시적으로(잠깐) 나갔다."}
        ],
        "transition_question": "눈 깜짝할 찰나가 어떻게 미래의 \"곧, 금방\"이라는 시점으로 변할까요?",
        "logic_flow": ["저울 바늘을 기울게 만드는 찰나의 움직임 (momentum)", "↓", "매우 짧은 순간 동안만 지속됨 (순간적으로)", "↓", "현재 지점에서 다음 행동이 시작되는 시간 간격의 극소화", "↓", "기다릴 필요 없이 '곧, 금방'"],
        "logic_desc": "시간의 지속 길이가 극도로 짧다는 의미(잠깐)에서, 현재 시간과 사건 발생 시점 사이의 간격이 극도로 짧음(곧, 금방)으로 전이되었습니다.",
        "examples2": [
            {"en": "The plane will be landing momentarily.", "ko": "비행기가 곧 착륙할 것입니다."},
            {"en": "She will be with you momentarily.", "ko": "그녀가 곧 당신에게 갈 것입니다."}
        ],
        "feeling": "momentarily = 아주 미세한 순간 = 찰나의 시간 동안 = 간격이 없는 = 곧 / 금방",
        "real_tip": "영국 영어에서는 주로 '잠깐 동안'으로 쓰이고, 미국 영어에서는 '곧(soon)'의 의미로 공항 안내 방송 등에 매우 많이 쓰입니다.",
        "summary_flow": ["movere 움직이다", "momentum 저울을 움직이는 추진력/찰나", "momentary 순간의", "momentarily 순간적으로", "곧, 금방"],
        "quiz": [
            {"question": "The screen flickered __________ before turning off.", "translation": "화면이 꺼지기 전에 잠깐 깜빡였다.", "answer": "momentarily"},
            {"question": "The doctor will see you __________.", "translation": "의사 선생님이 곧 당신을 진찰하실 겁니다.", "answer": "momentarily"}
        ]
    },
    {
        "word": "term",
        "pronunciation": "turm",
        "meaning1": "용어, 말 (의미의 울타리)",
        "meaning2": "기간, 임기, 조건 (시간/행동의 경계선)",
        "intro": "영토의 '경계선'을 가리키던 단어가 왜 우리가 공부하는 '용어'와 '계약 조건'이 되었을까요?",
        "etymology": {
            "root1": "term (L. terminus : boundary, limit / 경계, 한계, 끝)",
            "root2": "noun (명사)",
            "flow": ["경계선, 영토의 경계", "개념의 한계를 정하여 규정한 말 (용어)", "시간적 한계와 규정 (기간/임기)", "서로 합의된 선 (계약 조건)"]
        },
        "examples1": [
            {"en": "The term 'robot' means 'traffic light' in South Africa.", "ko": "'robot'이라는 용어는 남아프리카 공화국에서 '신호등'을 의미한다."},
            {"en": "Medical terms are often difficult to understand.", "ko": "의학 용어들은 종종 이해하기 어렵다."}
        ],
        "transition_question": "한계를 그어둔 선이 어떻게 계약의 \"조건\"이나 \"학기, 임기\"가 되었을까요?",
        "logic_flow": ["땅의 시작과 끝을 나누는 경계비 (terminus)", "↓", "개념의 테두리를 그어서 규정한 구체적인 어휘 (용어)", "↓", "시간의 시작과 끝을 그어 놓은 구간 (학기/임기/기간)", "↓", "합의된 약속의 선을 넘지 않기로 규정한 조항들 (조건)"],
        "logic_desc": "의미의 울타리를 쳐서 단어를 규정하면 '용어'가 되고, 시간의 울타리를 치면 '기간'이 되며, 약속의 울타리를 치면 '조건'이 되는 경계(Terminus)의 일관된 원리입니다.",
        "examples2": [
            {"en": "He was elected for a four-year term.", "ko": "그는 4년 임기로 선출되었다."},
            {"en": "Under the terms of the contract, we must pay now.", "ko": "계약 조건에 따라 우리는 지금 지불해야 한다."}
        ],
        "feeling": "term = 딱 한계를 지어 놓은 경계선 = 용어 = 한정된 기간 = 지켜야 할 계약 조건",
        "real_tip": "in terms of(~의 면에서)는 수능에 매년 출제되는 단골 표현이며, 복수형 terms는 '조건, 관점, 관계' 등의 뜻이 있습니다.",
        "summary_flow": ["terminus 경계/한계", "term 경계를 지은 것", "개념 경계: 용어", "시간 경계: 기간/학기", "약속 경계: 조건"],
        "quiz": [
            {"question": "He explained the concept in simple __________.", "translation": "그는 그 개념을 쉬운 용어로 설명했다.", "answer": "terms"},
            {"question": "The payment __________ must be negotiated.", "translation": "지불 조건이 협상되어야 한다.", "answer": "terms"}
        ]
    },
    {
        "word": "unique",
        "pronunciation": "yoo-NEEK",
        "meaning1": "유일무이한, 독특한 (물리적 단 하나)",
        "meaning2": "뛰어난, 특별한 (추상적 고유 가치)",
        "intro": "숫자 '1'에서 탄생한 단어가 어떻게 '특별하고 독특한' 가치를 나타내게 되었을까요?",
        "etymology": {
            "root1": "uni- (L. unus : one / 하나)",
            "root2": "-que (Suffix : 형용사 접사)",
            "flow": ["단 하나뿐인, 오직 하나인", "비슷한 비교군이 없는", "독특한, 고유한 특징을 지닌", "매우 특별하고 뛰어난"]
        },
        "examples1": [
            {"en": "The unique usage of this word might cause confusion.", "ko": "이 단어의 독특한 사용법은 혼란을 초래할 수도 있다."},
            {"en": "Each person has a unique DNA pattern.", "ko": "사람마다 고유한(유일한) DNA 패턴을 가지고 있다."}
        ],
        "transition_question": "오직 하나뿐이라는 사실이 어떻게 \"뛰어난, 특별한\" 가치 평가로 이어질까요?",
        "logic_flow": ["숫자 1(unus)처럼 전 우주에 단 하나만 존재함", "↓", "대체할 수 있는 다른 물건이 없음", "↓", "그것만이 가진 독특하고 고유한 특성", "↓", "흉내 낼 수 없을 만큼 뛰어난, 특별한"],
        "logic_desc": "대체 불가능한 '유일성(One)'의 성질이, 사물의 독창성과 고유의 훌륭함(특별함)을 나타내는 가치 평가로 변모했습니다.",
        "examples2": [
            {"en": "She has a unique talent for design.", "ko": "그녀는 디자인에 뛰어난(독보적인) 재능을 가지고 있다."},
            {"en": "This museum offers a unique experience.", "ko": "이 박물관은 특별한 경험을 제공한다."}
        ],
        "feeling": "unique = 오직 하나(uni)뿐인 = 대체 불가능한 = 고유한 = 특별하고 뛰어난",
        "real_tip": "unique는 원칙적으로 절대적 개념(유일무이)이어서 very나 more의 수식을 받지 않는 것이 어법 원칙이지만, 구어에서는 흔히 쓰입니다.",
        "summary_flow": ["unus 하나", "unicus 하나뿐인", "unique 유일무이한", "고유의 독특한", "특별히 뛰어난"],
        "quiz": [
            {"question": "The island is home to several __________ species.", "translation": "그 섬은 몇몇 독특한(고유한) 종들의 서식지이다.", "answer": "unique"},
            {"question": "He has a __________ opportunity to study abroad.", "translation": "그는 해외에서 공부할 특별한 기회를 얻었다.", "answer": "unique"}
        ]
    },
    {
        "word": "usage",
        "pronunciation": "YOO-sij",
        "meaning1": "사용법, 용례 (물리적 사용 행위)",
        "meaning2": "관습, 관례 (사회적으로 고착화된 관행)",
        "intro": "도구를 '사용하는 행동'이 어떻게 사회의 단단한 '관습과 법적 효력'이 될까요?",
        "etymology": {
            "root1": "us (L. uti : to use / 사용하다)",
            "root2": "-age (Suffix : 행위, 상태, 집합)",
            "flow": ["사용하는 행위와 방법", "언어나 도구의 실제 사용례", "사회에서 반복적으로 사용하여 굳어짐", "사회적 관습, 관례, 법률상의 관행"]
        },
        "examples1": [
            {"en": "The unique usage of this word might cause misunderstanding.", "ko": "이 단어의 독특한 사용법(용례)은 오해를 유발할 수 있다."},
            {"en": "This dictionary illustrates the modern usage of terms.", "ko": "이 사전은 용어들의 현대적 용례를 보여준다."}
        ],
        "transition_question": "단어나 도구를 쓰는 법이 어떻게 사회를 규정하는 \"관습\"이 될까요?",
        "logic_flow": ["무언가를 필요에 따라 이용함 (use)", "↓", "그 이용 방식이 널리 공유된 행동 양식 (사용법, 용례)", "↓", "시간이 흐르면서 특정 집단 안에서 오랜 기간 되풀이됨", "↓", "행동을 규율하는 사회적 규칙이나 관습(custom)"],
        "logic_desc": "시간의 축 위에서 '쓰임새(usage)'가 축적되어 다수가 정당하다고 인정하게 되면서, 구속력을 지닌 사회적 관습이나 관례로 뜻이 확장되었습니다.",
        "examples2": [
            {"en": "The law is based on long-established commercial usage.", "ko": "그 법은 오랫동안 확립된 상업적 관습(관례)에 기반을 두고 있다."},
            {"en": "It is contrary to social usage.", "ko": "그것은 사회적 관례에 어긋난다."}
        ],
        "feeling": "usage = 실제로 사용함 = 단어의 쓰임새/용례 = 세대를 거치며 굳어진 관습",
        "real_tip": "use는 일상적인 '사용'을, usage는 오랜 역사 속에서 고착화된 '사용법'이나 '관습'을 가리킬 때 구분하여 씁니다.",
        "summary_flow": ["uti 사용하다", "usus 사용", "usage 실제 사용법", "반복된 행위", "사회적 관습/관례"],
        "quiz": [
            {"question": "He was criticized for his improper __________ of language.", "translation": "그는 부적절한 언어 사용법(용례) 때문에 비판을 받았다.", "answer": "usage"},
            {"question": "Local __________ dictated that the land belonged to the community.", "translation": "지역의 관습(관례)에 따라 그 땅은 공동체의 소유로 정해졌다.", "answer": "usage"}
        ]
    },
    {
        "word": "diversity",
        "pronunciation": "dih-VUR-si-tee",
        "meaning1": "다양성, 다채로움 (여러 갈래로 흩어짐)",
        "meaning2": "갈등, 불일치 (의견이 서로 엇갈림)",
        "intro": "풍요로운 '다양성' 속에 왜 의견이 나뉘는 '갈등'의 씨앗이 내포되어 있을까요?",
        "etymology": {
            "root1": "di- (L. dis- : apart, aside / 갈라져, 사방으로)",
            "root2": "vers (L. vertere : to turn / 돌리다)",
            "flow": ["사방으로 길을 흩어 돌리다", "한곳으로 뭉치지 않고 제각각 다름", "다양성, 다채로운 상태", "방향이 일치하지 않아 생기는 의견 불일치, 갈등"]
        },
        "examples1": [
            {"en": "It highlights the diversity of World Englishes.", "ko": "이것은 세계 영어들의 다양성을 강조한다."},
            {"en": "The diversity of species makes the forest healthy.", "ko": "종의 다양성은 숲을 건강하게 만든다."}
        ],
        "transition_question": "서로 방향이 흩어지는 성질이 어떻게 \"의견 대립과 갈등\"이 될까요?",
        "logic_flow": ["하나의 초점이 여러 갈래(di)로 쪼개짐", "↓", "각 요소가 다른 방향(vertere)으로 몸을 돎", "↓", "서로 다른 개성을 지녀서 다채로움 (다양성)", "↓", "일관된 합의점을 찾지 못하고 사방으로 찢어짐", "↓", "의견 불일치, 대립, 갈등"],
        "logic_desc": "한 방향으로 획일화되지 않고 제각기 방향을 틀고(diverse) 있는 다름의 속성에서 다양성(풍요로움)과 대립(갈등)이라는 두 갈래 의미가 다 파생했습니다.",
        "examples2": [
            {"en": "The diversity of opinions within the team caused a delay.", "ko": "팀 내 의견의 불일치(갈등/다양성)가 지연을 초래했다."},
            {"en": "They had to resolve the diversity between their interests.", "ko": "그들은 그들의 이해관계 간의 불일치(갈등)를 해결해야 했다."}
        ],
        "feeling": "diversity = 사방(di)으로 꺾어 돌려(vers) 놓은 상태 = 다채로움 = 엇갈리는 의견 / 갈등",
        "real_tip": "동사형인 diversify는 '다각화하다, 투자를 분산하다'로 시험에 출제되니 함께 암기해야 합니다.",
        "summary_flow": ["vertere 돌리다", "divertere 갈라져서 돌다", "diversity 갈라져 흩어진 상태", "다양성/다채로움", "의견의 불일치/갈등"],
        "quiz": [
            {"question": "We should promote __________ and inclusion in the office.", "translation": "우리는 사무실 내의 다양성과 포용성을 증진해야 한다.", "answer": "diversity"},
            {"question": "A great __________ of views was expressed during the meeting.", "translation": "회의 중에 매우 다양한(상이한) 의견들이 개진되었다.", "answer": "diversity"}
        ]
    },
    {
        "word": "extensive",
        "pronunciation": "ik-STEN-siv",
        "meaning1": "넓은, 광범위한 (물리적 공간)",
        "meaning2": "해박한, 폭넓은 (추상적 지식/영향력)",
        "intro": "밖으로 팽팽하게 뻗어나가는 힘이 어떻게 지식이 '해박한'이라는 뜻으로 연결될까요?",
        "etymology": {
            "root1": "ex- (L. ex- : out / 밖으로)",
            "root2": "tens (L. tendere : to stretch / 펼치다, 늘이다)",
            "flow": ["바깥으로 쭉 뻗쳐 펼치다", "물리적 공간이나 영역이 넓은", "범위와 내용이 풍성하고 대규모인", "지식이나 조사가 깊고 해박한"]
        },
        "examples1": [
            {"en": "English has become widely used due to its extensive usage.", "ko": "영어는 그것의 광범위한 사용으로 인해 널리 사용되게 되었다."},
            {"en": "The farm has extensive fields of wheat.", "ko": "그 농장은 광범위한 밀밭을 가지고 있다."}
        ],
        "transition_question": "물리적 넓이가 어떻게 지식이나 학습의 깊이인 \"해박함\"이 될까요?",
        "logic_flow": ["안에 머물지 않고 사방 바깥(ex)으로 뻗어감(tendere)", "↓", "차지하는 영토나 면적이 커서 광활한", "↓", "영향이 가 닿는 정보의 범위가 넓은", "↓", "자료 조사나 독서량이 몹시 넓고 해박한"],
        "logic_desc": "물리적 팽창선(extension)이 무형의 데이터 영역으로 투영되어, 탐색한 폭이 몹시 넓고 체계적임을 뜻하게 되었습니다.",
        "examples2": [
            {"en": "The professor is famous for his extensive knowledge.", "ko": "그 교수는 해박한 지식으로 유명하다."},
            {"en": "They conducted an extensive search for the lost dog.", "ko": "그들은 잃어버린 개를 찾기 위해 광범위한 수색을 실시했다."}
        ],
        "feeling": "extensive = 밖으로(ex) 뻗어나간(tens) = 광범위한 = 깊고 해박한",
        "real_tip": "반대말인 intensive는 '집중적인'이며, 두 단어의 접두사 차이(ex: 밖으로 vs in: 안으로)를 대조하는 문항이 출제됩니다.",
        "summary_flow": ["tendere 뻗다", "extendere 밖으로 뻗다", "extensive 밖으로 뻗어나간", "광범위한 영토", "해박한/폭넓은 지식"],
        "quiz": [
            {"question": "The storm caused __________ damage to the coastal area.", "translation": "폭풍우는 해안 지역에 광범위한 피해를 입혔다.", "answer": "extensive"},
            {"question": "She has had __________ training in classical music.", "translation": "그녀는 고전 음악에서 폭넓은 훈련을 받았다.", "answer": "extensive"}
        ]
    },
    {
        "word": "adoption",
        "pronunciation": "uh-DAHP-shuhn",
        "meaning1": "입양 (가족으로 받아들임)",
        "meaning2": "채택, 차용 (새로운 아이디어/제도의 도입)",
        "intro": "아이를 가족으로 삼는 '입양'과 제도를 도입하는 '채택'은 어떻게 머릿속에서 한 몸이 되었을까요?",
        "etymology": {
            "root1": "ad- (L. ad- : to, toward / ~쪽으로)",
            "root2": "opt (L. optare : to choose / 선택하다, 고르다)",
            "flow": ["내 쪽으로 끌어당겨 선택하다", "혈연관계가 없는 아이를 내 자식으로 선택하다 (입양)", "새로운 의견이나 문화를 선택해 수용하다", "채택, 차용, 수용"]
        },
        "examples1": [
            {"en": "They decided to choose adoption to build their family.", "ko": "그들은 가족을 이루기 위해 입양을 선택하기로 결정했다."},
            {"en": "The adoption of orphan children increased.", "ko": "고아 아동들의 입양이 증가했다."}
        ],
        "transition_question": "가족 구성원을 들이는 것에서 어떻게 문물이나 언어의 \"채택\"으로 번졌을까요?",
        "logic_flow": ["수많은 선택지 중에서 나에게 유익한 것을 고름 (opt)", "↓", "내 울타리 안(ad)으로 소중히 들여와 정착시킴", "↓", "부모가 없는 아이를 내 아이로 품음 (입양)", "↓", "외부에 존재하는 훌륭한 법률, 기술, 단어를 골라 도입함 (채택, 차용)"],
        "logic_desc": "주체가 강한 의지를 갖고 가치 있는 대상을 내 품(가족, 자국 문화) 안으로 껴안아(optare) 내재화하는 공통 메커니즘을 가지고 있습니다.",
        "examples2": [
            {"en": "The adoption of the new law was welcomed by citizens.", "ko": "새로운 법률의 채택(통과)은 시민들의 환영을 받았다."},
            {"en": "We saw the rapid adoption of smartphone technology.", "ko": "우리는 스마트폰 기술의 빠른 채택(수용)을 목격했다."}
        ],
        "feeling": "adoption = 마음 쪽으로(ad) 선택하여(opt) 내 것으로 만듦 = 입양 = 제도/언어의 채택",
        "real_tip": "동사형 adopt(입양하다, 채택하다)와 헷갈리기 쉬운 adapt(적응하다, 개조하다)를 구별하는 문제는 어휘 단골 기출입니다.",
        "summary_flow": ["optare 고르다", "adoptare 골라 가지다", "adoption 내 것으로 삼음", "아이의 입양", "법안/기술의 채택"],
        "quiz": [
            {"question": "The committee recommended the __________ of the new curriculum.", "translation": "위원회는 새로운 교육과정의 채택을 권고했다.", "answer": "adoption"},
            {"question": "She was raised by her aunt after her __________.", "translation": "그녀는 입양된 후 그녀의 이모 밑에서 자랐다.", "answer": "adoption"}
        ]
    },
    {
        "word": "individuals",
        "pronunciation": "in-dih-VIJ-oo-uhlz",
        "meaning1": "개인들, 개별 존재들 (더는 나눌 수 없는 단위)",
        "meaning2": "개성 있는 사람들 (독자적 주체)",
        "intro": "'더는 나눌 수 없다'는 부정적인 원리가 어떻게 우리 하나하나를 가리키는 '개인'이 되었을까요?",
        "etymology": {
            "root1": "in- (L. not / 아님)",
            "root2": "dividu (L. dividere : to divide / 나누다)",
            "flow": ["나눌 수 없는 상태의", "사회를 쪼갤 때 나오는 최소 생명 단위", "단체와 구별되는 개개의 사람", "개인들, 개별체들"]
        },
        "examples1": [
            {"en": "This allows individuals who speak different languages to communicate.", "ko": "이것은 서로 다른 모국어를 사용하는 개인들이 소통할 수 있게 한다."},
            {"en": "We must treat them as separate individuals.", "ko": "우리는 그들을 별개의 개인들로 취급해야 한다."}
        ],
        "transition_question": "쪼갤 수 없는 최소 입자가 어떻게 사회에서 \"독자적 주체\"를 칭하는 말이 될까요?",
        "logic_flow": ["칼로 자르고 나누어 분리함 (divide)", "↓", "더 자르면 파괴되어 기능하지 못하는 최소 단위 (in-dividu)", "↓", "국가나 사회 집단이라는 거대한 덩어리와 대비되는 낱개의 한 사람", "↓", "자기만의 성향을 지닌 개성 있는 인간 주체"],
        "logic_desc": "더 이상 나눌 수 없다는 속성(individual)이 물리적 쪼개기에서 시작해, 사회적 속에서 가치를 독립적으로 보유하는 최종 인간 주체(개인)로 철학화되었습니다.",
        "examples2": [
            {"en": "Creative individuals drive societal progress.", "ko": "창의적인 개인들이 사회적 발전을 추진한다."},
            {"en": "The tax cuts will benefit high-income individuals.", "ko": "감세는 고소득 개인들에게 혜택을 줄 것이다."}
        ],
        "feeling": "individuals = 더 쪼갤 수 없는(individuus) 최소 단위 = 사회 속 낱개의 한 사람 = 개인들",
        "real_tip": "individual은 형용사로 '개인의, 독특한'이라는 뜻도 있으며, 복수형은 사회 전체(society)의 대조군으로 독해에 자주 나옵니다.",
        "summary_flow": ["dividere 나누다", "individuus 나눌 수 없는", "individual 개별적인 인간 하나", "복수화", "개인들"],
        "quiz": [
            {"question": "The charity helps __________ in need.", "translation": "그 자선단체는 곤경에 처한 개인들을 돕는다.", "answer": "individuals"},
            {"question": "Every person has __________ rights that must be protected.", "translation": "모든 사람은 보호받아야 할 개별적인(개인의) 권리가 있다.", "answer": "individual"}
        ]
    },
    {
        "word": "demand",
        "pronunciation": "dih-MAND",
        "meaning1": "요구하다, 요구 (강력한 의사 표시)",
        "meaning2": "수요 (시장의 강력한 필요)",
        "intro": "명령조로 강력하게 '요구하는 행위'가 경제학에서는 왜 '수요'라는 중립적인 뜻이 되었을까요?",
        "etymology": {
            "root1": "de- (L. de- : formally, away / 공식적으로, 아래로)",
            "root2": "mand (L. mandare : to order, entrust / 명령하다, 맡기다)",
            "flow": ["공식적으로 명령하여 요구하다", "강하게 달라고 요구하는 행위", "상품을 구매하고자 하는 소비자들의 요구", "수요 / 필요 사항"]
        },
        "examples1": [
            {"en": "There was a high demand of English in critical fields.", "ko": "중요한 분야들에서 영어에 대한 높은 수요(요구)가 있었다."},
            {"en": "Workers demand a wage increase and better conditions.", "ko": "노동자들은 임금 인상과 더 나은 조건을 요구한다."}
        ],
        "transition_question": "주권자의 명령과 요구가 어떻게 시장 경제의 \"수요\"라는 물리량이 되었을까요?",
        "logic_flow": ["공식적으로 권리를 주장하며 달라고 압박함 (demand)", "↓", "반드시 충족시켜야 하는 필수 요구 사항", "↓", "시장에서 특정 재화를 사고 싶어 하는 소비자들의 집단적 욕구", "↓", "수요 (Supply와 대칭점)"],
        "logic_desc": "주체가 대상을 향해 가지겠다고 강하게 외치며 요구(mandare)하는 행위가, 경제 구도 내의 총합 수요(demand)로 정착되었습니다.",
        "examples2": [
            {"en": "The demand for electric cars is rising rapidly.", "ko": "전기차에 대한 수요가 빠르게 늘고 있다."},
            {"en": "The job demands high concentration and skill.", "ko": "그 일은 높은 집중력과 기술을 요구한다(필요로 한다)."}
        ],
        "feeling": "demand = 힘주어(de) 명령하다(mand) = 요구하다 = 반드시 필요함 = 시장의 수요",
        "real_tip": "demanding은 형용사로 '요구가 많은, 힘든, 까다로운'이라는 뜻으로 변별력 문제에 출제됩니다.",
        "summary_flow": ["mandare 위임하다/명령하다", "demandare 요구하다", "demand 권리를 주장하며 요구함", "요구사항", "시장의 수요"],
        "quiz": [
            {"question": "Supply should balance with __________ in a market economy.", "translation": "시장 경제에서 공급은 수요와 균형을 이루어야 한다.", "answer": "demand"},
            {"question": "The protesters __________ the release of the prisoners.", "translation": "시위자들은 수감자들의 석방을 요구했다.", "answer": "demand"}
        ]
    },
    {
        "word": "critical",
        "pronunciation": "KRIT-i-kuhl",
        "meaning1": "비판적인 (판단하고 지적함)",
        "meaning2": "결정적인, 중대한, 위독한 (판단이 필요한 경계선)",
        "intro": "남의 꼬투리를 잡는 '비판적인' 단어가 왜 환자의 목숨을 다룰 때는 '위독한'이 되는 것일까요?",
        "etymology": {
            "root1": "crit (Gk. krinein : to decide, judge / 판단하다, 비판하다)",
            "root2": "-ical (Suffix : 형용사화 접사)",
            "flow": ["옳고 그름을 칼같이 판단하는", "허점을 날카롭게 분석하여 비판하는", "운명을 판단해야 하는 중대 국면의", "대단히 중요한 / 위독한"]
        },
        "examples1": [
            {"en": "She wrote a critical review of the book.", "ko": "그녀는 그 책에 대한 비판적인 평론을 썼다."},
            {"en": "Stop being so critical of everything I do.", "ko": "내가 하는 모든 일에 그렇게 비판적으로 굴지 마라."}
        ],
        "transition_question": "지적질하는 마음이 어떻게 삶과 죽음의 경계인 \"위독함, 결정적 중요성\"이 될까요?",
        "logic_flow": ["진위를 나누는 날카로운 판단 (judge)", "↓", "오류와 단점을 분석적으로 가려냄 (비판적인)", "↓", "성패나 생사가 판가름 나는 아슬아슬한 분기점 (critical point)", "↓", "대단히 중대하고 결정적인 / 생명이 위독한"],
        "logic_desc": "이쪽인지 저쪽인지 확실하게 선을 긋는 매서운 '판단(Krinein)'에서, 생사가 갈리는 시점의 엄혹함(위독한)과 결과에 지대한 영향을 미침(중요한)이 유도되었습니다.",
        "examples2": [
            {"en": "We need English in critical fields like science and technology.", "ko": "우리는 과학과 기술 같은 중요한(결정적인) 분야에서 영어가 필요하다."},
            {"en": "The patient is in a critical condition.", "ko": "그 환자는 위독한(위태로운) 상태이다."}
        ],
        "feeling": "critical = 정밀하게 깎아 판단하는 = 꼬투리 잡는 비판적 = 결단이 필요한 = 중대한/위독한",
        "real_tip": "수능 독해 필자의 태도 묻기 문항에서 'critical(비판적인)'은 매우 자주 등장하는 빈출 선지 단어입니다.",
        "summary_flow": ["krinein 판단하다/가르다", "criticus 비판가/중요 분기점", "critical 비판적인", "운명을 가르는 중대한", "생사가 걸린 위독한"],
        "quiz": [
            {"question": "The first 24 hours after the surgery are __________.", "translation": "수술 후 첫 24시간이 결정적이다(위태로운 고비다).", "answer": "critical"},
            {"question": "He is highly __________ of the government's economic policy.", "translation": "그는 정부의 경제 정책을 매우 비판적으로 바라본다.", "answer": "critical"}
        ]
    },
    {
        "word": "era",
        "pronunciation": "EER-uh",
        "meaning1": "시대, 연대 (역사적 구분)",
        "meaning2": "획기적인 시기, 새 시대 (질적인 큰 변화)",
        "intro": "주판계산용 '주사위'나 '숫자'를 뜻하던 라틴어가 어떻게 거대한 역사의 '시대'가 되었을까요?",
        "etymology": {
            "root1": "era (L. aera : counters for calculation, markers / 계산용 주사위, 동전, 기준점)",
            "root2": "noun (명사)",
            "flow": ["계산의 기준이 되는 눈금/숫자", "새로운 역법 계산의 시작 연도", "그 시작점부터 지속되는 특정한 연대", "새로운 가치가 지배하는 장엄한 시대"]
        },
        "examples1": [
            {"en": "Moreover, in the digital era, online information is vast.", "ko": "게다가 디지털 시대에 온라인 정보는 방대하다."},
            {"en": "The fall of the wall marked the end of an era.", "ko": "장벽의 붕괴는 한 시대의 종말을 알렸다."}
        ],
        "transition_question": "기준점이 되는 숫자가 어떻게 문화 전체를 아우르는 \"새 시대\"로 숙성되었을까요?",
        "logic_flow": ["주판에서 셈을 세는 계산용 말판 (aera)", "↓", "기념비적 사건이 일어난 해를 0년으로 두는 기원 기준점", "↓", "그 기준점으로부터 새롭게 셈을 이어가는 년수 단위", "↓", "기성 세대와 뚜렷이 구별되는 양상으로 가득 찬 문명사적 시대"],
        "logic_desc": "달력 계산의 '기준 좌표(Aera)'가 되는 해로부터 출발하여, 사회적·기술적으로 독자적인 성격을 지닌 역사의 한 장(Era)을 가리키게 되었습니다.",
        "examples2": [
            {"en": "We are entering a new era of space exploration.", "ko": "우리는 우주 탐사의 새로운 시대에 진입하고 있다."},
            {"en": "The Victorian era was a time of rapid growth in Britain.", "ko": "빅토리아 시대는 영국이 급속도로 성장하던 때였다."}
        ],
        "feeling": "era = 계산의 새로운 기준점 = 뚜렷하게 나뉘는 획기적 역사 단위 = 시대",
        "real_tip": "시대나 시기를 뜻하는 period(단순 구간), age(역사적 대구분), epoch(획기적 사건 위주)와 뉘앙스를 비교할 수 있습니다.",
        "summary_flow": ["aera 구리 주사위/계산의 원점", "era 연대 측정 기점", "특정한 기준 연도", "역사적 연대", "디지털/새 시대"],
        "quiz": [
            {"question": "The industrial revolution ushered in a new __________.", "translation": "산업 혁명은 새로운 시대를 열었다.", "answer": "era"},
            {"question": "Dinosaurs ruled the Earth during a previous geologic __________.", "translation": "공룡은 이전 지질 시대에 지구를 지배했다.", "answer": "era"}
        ]
    },
    {
        "word": "exposed",
        "pronunciation": "ik-SPOHZD",
        "meaning1": "노출된, 드러난 (물리적 겉면)",
        "meaning2": "무방비의, 위험에 취약한 (추상적 방어 해제)",
        "intro": "물건을 그냥 '밖에 던져놓은' 상태가 어떻게 위험에 '무방비로 취약한' 뜻이 될까요?",
        "etymology": {
            "root1": "ex- (L. ex- : out / 밖으로)",
            "root2": "posed (L. ponere : to place / 두다, 놓다)",
            "flow": ["바깥에 꺼내어 드러내 놓다", "가림막 없이 외부에 노출시키다", "햇볕이나 추위에 무방비로 버려지다", "위험이나 질병에 취약한, 무방비의"]
        },
        "examples1": [
            {"en": "People are exposed to a vast amount of online information.", "ko": "사람들은 방대한 양의 온라인 정보에 노출되어 있다."},
            {"en": "Keep the exposed skin covered in winter.", "ko": "겨울에는 노출된 피부를 가린 상태로 유지하라."}
        ],
        "transition_question": "안전지대 밖으로 놓인 상태가 어떻게 정신적인 \"취약함\"으로 번져갔을까요?",
        "logic_flow": ["상자 안에 숨기지 않고 밖(ex)으로 꺼내 놓음(ponere)", "↓", "장벽과 지붕이라는 보호 장치가 완전히 소멸함", "↓", "바람, 자외선, 방사능 등 외부 에너지를 고스란히 맞음", "↓", "사기, 비판, 폭력의 충격을 여과 없이 흡수하는 무방비 상태"],
        "logic_desc": "외부의 작용으로부터 보호받지 못하고 '밖에 그대로 던져져 배치된(Expose)' 물리적 상태가, 위험 요인에 정면으로 뚫려 있는 무방비함(Vulnerability)으로 전이된 형세입니다.",
        "examples2": [
            {"en": "The campers were exposed to severe cold overnight.", "ko": "캠핑객들은 밤새 극심한 추위에 노출되었다(무방비로 취약해졌다)."},
            {"en": "If you don't wear a mask, you are exposed to the virus.", "ko": "마스크를 쓰지 않으면 바이러스에 노출된다."},
            {"en": "This made the octopuses more exposed to predators.", "ko": "이것은 문어들을 포식자들에게 더 노출되게(무방비하게) 만들었다."}
        ],
        "feeling": "exposed = 보호막 없이 밖에(ex) 둔(pose) = 껍질이 벗겨진 = 취약하고 무방비인",
        "real_tip": "be exposed to (~에 노출되다) 구문으로 수동태 형태로 수능 독해 지문에 빈출됩니다.",
        "summary_flow": ["ponere 놓다", "exponere 밖에 내놓다", "exposed 노출된", "물리적 드러남", "위험에 취약한/무방비의"],
        "quiz": [
            {"question": "His skin was severely sunburned after being __________ to the sun.", "translation": "태양에 노출된 후 그의 피부는 심하게 그을렸다.", "answer": "exposed"},
            {"question": "Without passwords, your personal data is __________ to hackers.", "translation": "비밀번호가 없으면 당신의 개인 정보는 해커들에게 노출된다(취약하다).", "answer": "exposed"}
        ]
    },
    {
        "word": "vast",
        "pronunciation": "vast",
        "meaning1": "방대한, 광활한 (물리적으로 텅 비어 엄청나게 넓은)",
        "meaning2": "막대한, 엄청난 (추상적 수량이나 영향력)",
        "intro": "'텅 비어서 황량하다'는 황폐한 어원의 단어가 왜 부러움을 사는 '엄청나게 방대한' 뜻이 되었을까요?",
        "etymology": {
            "root1": "vast (L. vastus : empty, desolate, waste / 텅 빈, 황량한, 파괴된)",
            "root2": "adjective (형용사)",
            "flow": ["아무도 살지 않아 광활하고 황폐한", "눈을 씻고 봐도 끝이 보이지 않는 광대함", "부피와 면적이 엄청나게 방대한", "양과 강도가 대단히 막대한"]
        },
        "examples1": [
            {"en": "They are exposed to a vast amount of online information.", "ko": "사람들은 방대한 양의 온라인 정보에 노출되어 있다."},
            {"en": "We looked out over the vast desert.", "ko": "우리는 광활한 사막을 바라보았다."}
        ],
        "transition_question": "황량한 사막의 텅 빔이 어떻게 다량의 지식이나 돈의 \"막대함\"으로 연결될까요?",
        "logic_flow": ["인공물이 없는 텅 빈(vastus) 황무지", "↓", "시선이 끝닿지 않는 아득한 지평선", "↓", "면적이나 물리적 그릇의 엄청난 방대함", "↓", "추상적 개념(자금, 정보, 가능성)의 크기가 거대함", "↓", "막대한, 엄청난"],
        "logic_desc": "경계선이나 가로막음이 없어 아득하고 텅 빈 지평선(Vastus)의 광대함이 현대에 이르러 지식이나 재산의 '방대한 수치'라는 긍정적 역동으로 재탄생했습니다.",
        "examples2": [
            {"en": "The project cost a vast sum of money.", "ko": "그 프로젝트는 막대한 액수의 돈이 들었다."},
            {"en": "The vast majority of students passed the exam.", "ko": "학생들의 절대다수(막대한 다수)가 시험에 합격했다."}
        ],
        "feeling": "vast = 끝이 없이 텅 비어 뚫린 = 광활하고 방대한 = 척도가 어마어마하게 막대한",
        "real_tip": "vast majority는 단골 숙어로 '압도적 다수, 절대다수'를 뜻하여 주제문 추론에 결정적 역할을 합니다.",
        "summary_flow": ["vastus 황량한/텅 빈", "vast 광활하게 열린", "물리적 광대한", "추상적 수량", "방대한, 막대한"],
        "quiz": [
            {"question": "He has a __________ experience in international trade.", "translation": "그는 국제 무역 분야에서 방대한(풍부한) 경험을 갖고 있다.", "answer": "vast"},
            {"question": "The stars in the __________ universe are uncountable.", "translation": "광대하고 무한한 우주 속의 별들은 셀 수 없다.", "answer": "vast"}
        ]
    },
    {
        "word": "consistently",
        "pronunciation": "kuhn-SIS-tuhnt-lee",
        "meaning1": "일관되게, 시종일관 (모든 요소가 함께 꿋꿋이 서서)",
        "meaning2": "항상, 지속적으로 (추상적 안정성)",
        "intro": "'다 같이 한자리에 똑바로 서 있다'는 행동이 어떻게 든든한 '일관성'의 상징이 되었을까요?",
        "etymology": {
            "root1": "con- (L. com- : together / 함께, 다 같이)",
            "root2": "sist (L. sistere : to stand / 서다, 세우다) + -ently (Adverb Suffix)",
            "flow": ["모든 부분이 흩어지지 않고 다 함께 서서", "흔들리거나 무너지지 않고 정합을 이룸", "앞과 뒤가 다르지 않고 시종일관되게", "변치 않고 항상, 지속적으로"]
        },
        "examples1": [
            {"en": "These factors have consistently contributed to the widespread use of English.", "ko": "이러한 요인들이 영어의 광범위한 사용에 지속적으로 기여해왔다."},
            {"en": "She consistently performs at the highest level.", "ko": "그녀는 항상(일관되게) 최고 수준의 기량을 발휘한다."}
        ],
        "transition_question": "흐트러짐 없이 서 있는 자세가 어떻게 시간적으로 \"항상\"이라는 신뢰의 부사가 되었을까요?",
        "logic_flow": ["첫 기둥과 마지막 기둥이 나란히(con) 꼿꼿이 서 있음(sistere)", "↓", "시간의 경과나 외부 압박에도 붕괴되거나 일그러지지 않음", "↓", "말과 행동의 전후가 조화를 이루며 유지됨 (일관되게)", "↓", "어김없이 매번 똑같은 궤도를 달림 (지속적으로, 항상)"],
        "logic_desc": "여러 구성원이나 시간대의 단편들이 한 대형으로 나란히 정렬하여 서 있는(Consist) 굳건함에서, 신뢰할 만한 일관된(consistent) 궤적이 파생되었습니다.",
        "examples2": [
            {"en": "The player is consistently good throughout the season.", "ko": "그 선수는 시즌 내내 일관되게 훌륭한 활약을 펼친다."},
            {"en": "He consistently arrived late for the class.", "ko": "그는 한결같이(어김없이) 수업에 늦게 도착했다."}
        ],
        "feeling": "consistently = 함께(con) 똑바로 선(sist) 채 흔들리지 않는 = 한결같이 = 지속적으로",
        "real_tip": "consistent(일관된)와 반대어인 inconsistent(모순된, 변덕스러운)도 문맥 파악 독해에 빈출되니 꼭 외워야 합니다.",
        "summary_flow": ["sistere 서다", "consistere 함께 단단히 서다", "consistent 흔들림 없이 한결같은", "consistently 일관되게", "항상/지속적으로"],
        "quiz": [
            {"question": "The company __________ produces high-quality products.", "translation": "그 회사는 지속적으로(일관되게) 고품질의 제품을 생산한다.", "answer": "consistently"},
            {"question": "To achieve your goal, you must study __________.", "translation": "목표를 이루려면 일관되게 공부해야 한다.", "answer": "consistently"}
        ]
    },
    {
        "word": "contributed",
        "pronunciation": "kuhn-TRIB-yoo-tid",
        "meaning1": "기여했다, 기부했다 (몫을 보태어 바치다)",
        "meaning2": "원인이 되었다 (추상적 영향 초래)",
        "intro": "세금을 납부하듯 내 몫을 떼어 '바치는' 행위가 왜 어떤 사건의 '원인이 되다'로 쓰일까요?",
        "etymology": {
            "root1": "con- (L. com- : together / 함께, 다 같이)",
            "root2": "tribute (L. tribuere : to assign, give / 몫을 나누어 주다, 바치다)",
            "flow": ["다 같이 자기 몫을 쪼개어 모아 바치다", "공동의 목적을 위해 기여/기부하다", "어떤 결과를 초래하는 데 힘을 보태다", "~의 주된 원인이 되다"]
        },
        "examples1": [
            {"en": "These factors have contributed to the widespread use of English.", "ko": "이러한 요인들이 영어의 광범위한 사용에 기여해왔다."},
            {"en": "He contributed a large sum of money to the hospital.", "ko": "그는 병원에 거액의 돈을 기부(기여)했다."}
        ],
        "transition_question": "금전이나 노동력을 바치는 선행이 어떻게 사건의 \"원인이 되다\"로 의미가 번졌을까요?",
        "logic_flow": ["개별 집단이 세금과 공물(tribute)을 한곳에(con) 모아 냄", "↓", "공동 프로젝트의 완수를 위해 힘과 몫을 보탬 (기여함)", "↓", "특정 현상을 발발시키는 데 내 몫의 영향력을 던져 넣음", "↓", "그 일의 발발 요인이자 원인이 됨"],
        "logic_desc": "결과물이라는 큰 더미를 완성하기 위해, 한 요인으로서 자기 지분을 던져 넣어 보탬을 준(tribuere) 인과 흐름을 담고 있습니다.",
        "examples2": [
            {"en": "Smoking contributed to his lung disease.", "ko": "흡연이 그의 폐 질환의 원인이 되었다(기여했다)."},
            {"en": "The heavy rain contributed to the car accident.", "ko": "폭우가 그 교통사고의 한 원인이 되었다."}
        ],
        "feeling": "contributed = 몫을 모아서(con) 바쳤다(tribut) = 기여했다 = 힘을 보태어 원인이 되었다",
        "real_tip": "contribute to의 to는 전치사이므로 뒤에 명사나 동명사(-ing)가 오며, '원인이 되다'라는 인과 독해의 핵심 축입니다.",
        "summary_flow": ["tribuere 나누어 주다/바치다", "contribuere 함께 힘을 바치다", "contribute 기여하다", "과거/과거분사형", "기여했다/원인이 되었다"],
        "quiz": [
            {"question": "Many volunteers __________ to the success of the Olympic games.", "translation": "많은 자원봉사자들이 올림픽 대회의 성공에 기여했다.", "answer": "contributed"},
            {"question": "Lack of sleep __________ to his poor memory.", "translation": "수면 부족이 그의 기억력 저하의 원인이 되었다.", "answer": "contributed"}
        ]
    },
    {
        "word": "influence",
        "pronunciation": "IN-floo-uhns",
        "meaning1": "영향력 (마음속에 스며 흐르는 힘)",
        "meaning2": "세력, 지배력 (사회적 권세)",
        "intro": "물이나 점성 액체가 '속으로 흘러드는' 물리 현상이 어떻게 거대한 '영향력'이 되었을까요?",
        "etymology": {
            "root1": "in- (L. in- : into / 안으로)",
            "root2": "flu (L. fluere : to flow / 흐르다) + -ence (Suffix : 명사화)",
            "flow": ["액체가 스며들어 안으로 흐름", "별의 정기가 인간의 운명 속으로 쏟아져 들어옴", "보이지 않게 마음과 생각을 지배해 흘러가는 힘 (영향력)", "사회적 위세와 세력"]
        },
        "examples1": [
            {"en": "These factors contributed to the global influence of English.", "ko": "이러한 요인들이 영어의 전 세계적인 영향력에 기여했다."},
            {"en": "The media has a powerful influence on public opinion.", "ko": "미디어는 여론에 강력한 영향력을 미친다."}
        ],
        "transition_question": "보이지 않게 유입되는 흐름이 어떻게 사회를 흔드는 \"지배 세력\"이 되었을까요?",
        "logic_flow": ["경계선을 뚫고 내부 깊숙이(in) 흘러(fluere) 유입됨", "↓", "자각하지 못하는 사이에 상태와 형태를 바꾸어 놓음 (영향력)", "↓", "주변 사람들을 내 의도대로 조종할 수 있는 물리력 축적", "↓", "권세를 틀어쥔 실질적 세력, 지배력"],
        "logic_desc": "점령군처럼 깃발을 꽂지 않고, 강물이 대지를 적시듯 조용히 내면으로 흘러들어(influence) 주도권을 쥐는 스며듦의 힘입니다.",
        "examples2": [
            {"en": "He used his political influence to pass the reform.", "ko": "그는 개혁안을 통과시키기 위해 자신의 정치적 영향력(세력)을 사용했다."},
            {"en": "Under the influence of alcohol, he couldn't drive.", "ko": "알코올의 영향 아래(술 취한 상태)에서 그는 운전할 수 없었다."}
        ],
        "feeling": "influence = 안으로(in) 서서히 흘러드는(flu) 기운 = 보이지 않게 장악하는 영향력 = 권세/세력",
        "real_tip": "have an influence on (~에 영향을 주다)은 수능 작문과 빈칸 문제의 매우 강력한 고정 패턴입니다.",
        "summary_flow": ["fluere 흐르다", "influere 안으로 흐르다", "influentia 천체의 기운이 흘러듦", "영향력", "지배 세력/권세"],
        "quiz": [
            {"question": "Peer __________ can shape teenagers' behaviors.", "translation": "또래 집단의 영향력은 십 대들의 행동을 형성할 수 있다.", "answer": "influence"},
            {"question": "He was a man of great __________ in the banking industry.", "translation": "그는 금융업계에서 대단한 영향력(세력)을 지닌 사람이었다.", "answer": "influence"}
        ]
    },
    {
        "word": "emerged",
        "pronunciation": "ih-MURJD",
        "meaning1": "떠올랐다, 나타났다 (수면 아래서 위로 솟아오름)",
        "meaning2": "알려졌다, 부상했다 (추상적 가치나 사실 폭로)",
        "intro": "물속에 푹 잠겨있던 것이 '물 위로 솟는 것'이 어떻게 가치나 비밀의 '부상과 출현'이 될까요?",
        "etymology": {
            "root1": "e- (L. ex- : out / 밖으로)",
            "root2": "merged (L. mergere : to dip, plunge / 물에 담그다, 잠기다)",
            "flow": ["물속에 깊이 잠겼던 상태에서 밖으로 나오다", "수면 위로 고개를 들이밀며 나타나다", "숨겨져 있던 비밀이나 신인이 세상에 드러나다", "두각을 나타내며 주역으로 부상했다"]
        },
        "examples1": [
            {"en": "Various English varieties have emerged worldwide.", "ko": "다양한 영어 종류들이 전 세계적으로 출현했다(등장했다)."},
            {"en": "The submarine emerged from the deep sea.", "ko": "그 잠수함은 심해로부터 수면 위로 떠올랐다."}
        ],
        "transition_question": "눈에 보이게 떠오른 야수가 어떻게 숨은 인물의 \"부상\"이나 비밀의 \"폭로\"가 될까요?",
        "logic_flow": ["어두컴컴한 물속(merge)에 짓눌려 숨겨져 있음", "↓", "부력을 얻어 장벽을 뚫고 바깥(ex)으로 튀어나옴 (솟아오름)", "↓", "모두가 관찰할 수 있게 존재를 만천하에 드러냄 (등장하다)", "↓", "무명이었던 세력이 중심 무대의 권력으로 떠오름 (부상했다)"],
        "logic_desc": "어둠(물속)에 잠겨(mergere) 보이지 않던 대상이 빛(바깥) 속으로 밀고 나와(ex-) 윤곽을 확연히 드러내는 해방의 시각 이미지입니다.",
        "examples2": [
            {"en": "It emerged that the company had lied about the budget.", "ko": "그 회사가 예산에 대해 거짓말을 했다는 사실이 드러났다(밝혀졌다).", "word_origin": "emerged"},
            {"en": "A new leader emerged from the crisis.", "ko": "위기 속에서 새로운 지도자가 부상했다(등장했다)."}
        ],
        "feeling": "emerged = 물속에 잠겨(merge) 있다가 밖으로(e-) 솟아올랐다 = 나타났다 = 드러나 부상했다",
        "real_tip": "It emerged that ~ 구문은 '대리 주어(It)'와 호응하여 '~라는 사실이 뒤늦게 밝혀졌다'는 의미로 자주 출제됩니다.",
        "summary_flow": ["mergere 물에 잠기다", "emergere 물 밖으로 솟다", "emerge 나타나다", "과거/과거분사형", "솟아올랐다/세상에 등장했다"],
        "quiz": [
            {"question": "The sun __________ from behind the thick clouds.", "translation": "태양이 두꺼운 구름 뒤에서 나타났다(솟아올랐다).", "answer": "emerged"},
            {"question": "New evidence has __________ during the investigation.", "translation": "수사 과정에서 새로운 증거가 드러났다(나타났다).", "answer": "emerged"}
        ]
    },
    {
        "word": "standard",
        "pronunciation": "STAN-derd",
        "meaning1": "표준, 기준 (전쟁터 한복판에 세운 대형 군기)",
        "meaning2": "일반적인, 기성의, 표준적인 (보편적 수용 모델)",
        "intro": "전쟁터의 매서운 칼바람 속에 꼿꼿이 세워둔 '대형 깃발'이 어떻게 매일 쓰는 '표준'이 되었을까요?",
        "etymology": {
            "root1": "stand (L. extendere : to stretch out / 깃발을 넓게 펼쳐 뻗다, 혹은 stand : 서다)",
            "root2": "-ard (Suffix : 특성, 사람)",
            "flow": ["전투 시 군사들이 헤매지 않게 넓게 펼친 군기", "군사들이 모여 정렬해야 하는 중심 기준점", "사물의 품질이나 척도를 비교하는 공인된 기준 (표준)", "보편적으로 채택된 흔한 모델"]
        },
        "examples1": [
            {"en": "British English and American English were considered standard models.", "ko": "영국 영어와 미국 영어는 표준 모델로 여겨졌다."},
            {"en": "The military standard was raised high in the battle.", "ko": "전투 중에 군대의 대형 깃발(기준 군기)이 높이 올려졌다."}
        ],
        "transition_question": "군대가 정렬해야 하는 깃발이 어떻게 제품이나 등급의 \"보편적 기준\"이 될까요?",
        "logic_flow": ["치열한 전투로 시야가 흐려진 백병전 상황", "↓", "아군이 퇴각하거나 헤매지 않도록 굳건하게 세워둔(stand) 큰 깃발", "↓", "이 선을 넘거나 대열을 이탈하면 안 되는 중심 약속선", "↓", "사물의 질을 등급 매기는 합의된 절대적 척도 (기준, 표준)", "↓", "특수 사양이 아닌 가장 보편적이고 기성인 (표준의)"],
        "logic_desc": "바람에 흔들려 꺾이지 않는 전쟁터의 '대형 표지 깃발(Estandart)'에서, 인간 행동과 공학의 공인 규격인 '표준(Standard)'이 수립되었습니다.",
        "examples2": [
            {"en": "You must meet the safety standards.", "ko": "당신은 안전 기준(표준)을 충족해야 한다."},
            {"en": "The standard version of the app is free.", "ko": "그 앱의 기본(표준) 버전은 무료이다."}
        ],
        "feeling": "standard = 전쟁터 중심에 꼿꼿이 세워둔 큰 깃발 = 대열의 중심선 = 행동의 표준 = 기본 규격",
        "real_tip": "standardize는 '표준화하다'이며, double standard(이중 잣대)는 현대 사회 비판 문제의 빈출 어휘입니다.",
        "summary_flow": ["extendere 펼치다/세우다", "estandart 전투 기준 깃발", "standard 기준 군기", "공식 표준", "보편적인 기성 모델"],
        "quiz": [
            {"question": "There is no __________ procedure for this task.", "translation": "이 작업을 위한 표준 절차는 존재하지 않는다.", "answer": "standard"},
            {"question": "The hotel rooms are of a very high __________.", "translation": "그 호텔 방들은 매우 높은 기준(수준)을 갖추고 있다.", "answer": "standard"}
        ]
    },
    {
        "word": "initially",
        "pronunciation": "ih-NISH-uh-lee",
        "meaning1": "처음에, 시초에 (문턱을 걸어 들어가기 시작하며)",
        "meaning2": "원래는, 초기에는 (가정과 초기 상태 확인)",
        "intro": "'문턱 안으로 걸어 들어가기 시작한다'는 어원이 어떻게 '처음에는'이라는 시간 부사가 되었을까요?",
        "etymology": {
            "root1": "in- (L. in- : into, upon / 안으로, 문턱에)",
            "root2": "it (L. ire : to go / 걸어가다, 진입하다) + -ially (Adverb Suffix)",
            "flow": ["문턱을 밟고 안으로 걸어 들어가기 시작하여", "모든 일의 시발점에 선 채로", "처음에, 시초에", "나중에 변화가 오기 전 '원래는'"]
        },
        "examples1": [
            {"en": "American English was initially seen as a regional variation.", "ko": "미국 영어는 초기에는 지역적 변이로 여겨졌다."},
            {"en": "Initially, we planned to stay home.", "ko": "처음에 우리는 집에 머물 계획이었다."}
        ],
        "transition_question": "입구로 들어가는 첫걸음이 어떻게 \"나중에 바뀐 현실\"과 대조를 이루는 \"원래는\"이 될까요?",
        "logic_flow": ["방의 경계선을 건너 안으로(in) 걸음을 뗌(ire)", "↓", "작업의 진도표 중 0%인 가장 첫 구간 (시작)", "↓", "이후에 여러 사건과 반전이 몰아닥치기 직전의 고요한 원점", "↓", "초기에는, 원래는 (나중엔 양상이 변경됨을 암시)"],
        "logic_desc": "진입의 첫 발걸음(initial)을 뗀 상황을 가리키며, 독해 지문에서는 기승전결의 '기(시작)'에서 훗날의 변화와 대조하기 위해 주로 쓰입니다.",
        "examples2": [
            {"en": "The project was initially funded by a charity.", "ko": "그 프로젝트는 처음에 한 자선단체에 의해 자금이 지원되었다."},
            {"en": "I was initially surprised by his decision.", "ko": "나는 처음에는 그의 결정에 놀랐다."}
        ],
        "feeling": "initially = 문을 열고 속으로(in) 들어가는(it) 첫 지점 = 시초에 = 원래는(나중엔 바뀜)",
        "real_tip": "initially가 문두에 나오면 '처음에는 (그랬으나 나중에는 다른 사건이 발생했다)'라는 반전의 흐름을 대비해야 합니다.",
        "summary_flow": ["ire 가다", "initium 들어가는 시작점", "initial 처음의", "initially 처음에", "원래는/초기에는"],
        "quiz": [
            {"question": "__________ he denied the rumors, but later admitted them.", "translation": "처음에 그는 소문을 부인했으나, 나중에 인정했다.", "answer": "Initially"},
            {"question": "The software was __________ designed for military use.", "translation": "그 소프트웨어는 원래(초기에) 군사용으로 설계되었다.", "answer": "initially"}
        ]
    },
    {
        "word": "variation",
        "pronunciation": "vair-ee-EY-shuhn",
        "meaning1": "변형, 변이 (알록달록하게 엇갈린 문양)",
        "meaning2": "차이, 편차 (수치적 오차와 흔들림)",
        "intro": "알록달록한 얼룩무늬에서 유래한 단어가 어떻게 생물의 '변이'와 수학의 '편차'가 되었을까요?",
        "etymology": {
            "root1": "vary (L. varius : diverse, speckled / 얼룩덜룩한, 다양한)",
            "root2": "-ation (Suffix : 명사화 접사)",
            "flow": ["알록달록하게 점들이 박혀 다양함", "규격에서 약간 빗겨 나간 다른 무늬", "표준 모델에서 갈라져 나온 다채로운 변형/변이", "수치상 발생하는 흔들림과 편차"]
        },
        "examples1": [
            {"en": "American English was seen as a regional variation.", "ko": "미국 영어는 지역적 변이(변형)로 여겨졌다."},
            {"en": "There is a minor variation in the recipe.", "ko": "그 레시피에는 약간의 변형이 있다."}
        ],
        "transition_question": "알록달록한 모양의 다름이 어떻게 과학의 정교한 \"오차와 편차\"가 되었을까요?",
        "logic_flow": ["점박이 표범 가죽처럼 무늬가 불규칙함 (varius)", "↓", "한 선으로 균일하게 가지 않고 굴곡이 생김", "↓", "원형(prototype)에서 개량되어 튀어나온 다른 형태 (변이, 변형)", "↓", "기준선 위아래로 춤을 추듯 벌어지는 수학적 차이 (편차, 변동)"],
        "logic_desc": "일정하게 정해진 무늬가 아니라 알록달록 무질서하게 점이 박힌 상태(Varius)처럼, 일정선에서 벗어난 변동이나 개조된 양상(variation)을 뜻합니다.",
        "examples2": [
            {"en": "We observed a wide variation in temperatures.", "ko": "우리는 기온의 큰 편차(변화)를 관찰했다."},
            {"en": "This genetic variation makes them immune to the disease.", "ko": "이 유전적 변이는 그들에게 그 질병에 대한 면역력을 제공한다."}
        ],
        "feeling": "variation = 단색이 아닌 얼룩덜룩함 = 표준에서 비틀어 낸 변형/변이 = 위아래의 흔들림 편차",
        "real_tip": "음악에서는 주제 멜로디를 꾸며 바꾸는 '변주곡'을 variation이라고 부릅니다.",
        "summary_flow": ["varius 알록달록한", "variare 바꾸다", "variation 달라진 모습", "지역적 변종/변형", "기온/수치의 편차"],
        "quiz": [
            {"question": "The experiment showed too much __________ in results.", "translation": "그 실험은 결과에서 너무 많은 편차(변동)를 보였다.", "answer": "variation"},
            {"question": "This dialect is a __________ of Southern English.", "translation": "이 방언은 남부 영어의 하나의 변형(변이)이다.", "answer": "variation"}
        ]
    },
    {
        "word": "evolves",
        "pronunciation": "ih-VAHLVZ",
        "meaning1": "진화하다 (두루마리를 바깥으로 풀다)",
        "meaning2": "서서히 발달하다, 변화하다 (단순에서 복잡으로)",
        "intro": "돌돌 말린 책인 '두루마리를 푸는' 동작이 어떻게 우주의 장엄한 '진화'가 되었을까요?",
        "etymology": {
            "root1": "e- (L. ex- : out / 밖으로)",
            "root2": "volves (L. volvere : to roll / 구르다, 돌다, 감다)",
            "flow": ["돌돌 말린 두루마리를 밖으로 풀다", "접혀 있던 속의 내용을 하나씩 꺼내 보여주다", "생물이 세대를 거치며 환경에 맞춰 형태를 바꾸다 (진화하다)", "서서히 양적으로 질적으로 발전하다"]
        },
        "examples1": [
            {"en": "A language evolves to accurately reflect daily realities.", "ko": "언어는 일상의 현실을 정확하게 반영하기 위해 진화한다(변화한다)."},
            {"en": "The species evolves over millions of years.", "ko": "그 종은 수백만 년에 걸쳐 진화한다."}
        ],
        "transition_question": "양장본 책을 펼치는 그림이 어떻게 문명이나 우주의 \"점진적 발달\"이 되었을까요?",
        "logic_flow": ["안에 말려(volvere) 보이지 않던 두루마리 양장본", "↓", "바깥(ex)으로 슬슬 굴려 글씨를 노출시킴", "↓", "안에 잠재되어 있던 유전정보나 역량이 활짝 개화함", "↓", "원시적인 모습에서 고도화된 형태로 오랜 세월을 거쳐 진화함", "↓", "점진적으로 발달하고 개조됨"],
        "logic_desc": "꽁꽁 숨겨져 뭉쳐 있던 두루마리(Volvere)의 가닥이 밖으로(ex-) 매끄럽게 전개되어 풀려나가는 장기적인 자기 발현 과정(evolution)을 묘사합니다.",
        "examples2": [
            {"en": "The business model evolves to meet new demands.", "ko": "그 비즈니스 모델은 새로운 수요를 맞추기 위해 서서히 발달한다(변한다)."},
            {"en": "Her style evolves with each new album.", "ko": "그녀의 스타일은 새로운 앨범이 나올 때마다 진화한다(발달한다)."}
        ],
        "feeling": "evolves = 두루마리를 밖으로(e-) 굴려(volv) 펼친다 = 잠재력을 개화하다 = 진화하다 = 서서히 발달하다",
        "real_tip": "혁명적인 급격한 변화를 뜻하는 revolve/revolution과 달리, evolve/evolution은 '점진적이고 평화적인 진화'를 가리킵니다.",
        "summary_flow": ["volvere 구르다/말다", "evolvere 밖으로 풀어 굴리다", "evolve 서서히 풀려 전개되다", "단수형 적용 evolves", "진화하다/발달하다"],
        "quiz": [
            {"question": "The technology __________ rapidly to adapt to the market.", "translation": "기술은 시장에 적응하기 위해 빠르게 진화한다(발달한다).", "answer": "evolves"},
            {"question": "How a caterpillar __________ into a butterfly is amazing.", "translation": "애벌레가 어떻게 나비로 진화하는(변하는)지는 놀랍다. (단수형: evolves)", "answer": "evolves"}
        ]
    },
    {
        "word": "specific",
        "pronunciation": "spih-SIF-ik",
        "meaning1": "특정한, 구체적인 (종류를 명확히 구분함)",
        "meaning2": "독특한, 고유한 (특정 카테고리에만 국한됨)",
        "intro": "사물의 '종류와 겉모양'을 뜻하는 단어에서 어떻게 '구체적이고 명확한'이라는 뜻이 나왔을까요?",
        "etymology": {
            "root1": "speci (L. species : appearance, kind / 꼴, 외견, 종류)",
            "root2": "fic (L. facere : to make / 만들다, 행동하다)",
            "flow": ["특정한 종류의 겉모양을 정확히 규정하여 만들다", "애매하게 얼버무리지 않고 콕 짚어 명확히 한", "특정한 범위에만 속하는 구체적인", "대상 고유의, 독특한"]
        },
        "examples1": [
            {"en": "When a language is adopted in a specific region, it changes.", "ko": "한 언어가 특정 지역에 채택되면, 그것은 변화한다."},
            {"en": "We need to set a specific date for the next meeting.", "ko": "우리는 다음 회의를 위해 구체적인 날짜를 정해야 한다."}
        ],
        "transition_question": "종류를 명확히 나누는 행동이 어떻게 \"이 대상만의 고유함\"으로 연결될까요?",
        "logic_flow": ["두루뭉술하게 섞지 않고 겉모양(species)을 대조함", "↓", "각 물건을 별개의 종류로 확실하게 갈라놓음(facere)", "↓", "타겟을 명확하게 조준하여 지목한 '구체적인/특정한'", "↓", "오직 그 분류군에서만 관찰되는 다른 곳엔 없는 '독특한/고유한'"],
        "logic_desc": "애매함의 안개를 걷어내고, 사물의 꼴(Species)을 명확하게 깎아 규정하는(facere) 이지적인 조준 상태를 가리킵니다.",
        "examples2": [
            {"en": "This treatment is specific to this type of cancer.", "ko": "이 치료법은 이 종류의 암에만 국한된(고유한) 것이다."},
            {"en": "The symptoms are not specific to the disease.", "ko": "그 증상들은 그 질병에만 나타나는 독특한(특이한) 것은 아니다."}
        ],
        "feeling": "specific = 종류의 꼴(speci)을 명확히 만든(fic) = 콕 집어 지명한 특정한 = 명확하고 구체적인",
        "real_tip": "명사형인 specification은 제품의 구체적인 '사양, 스펙'을 의미하는 비즈니스 핵심 어휘로 응용됩니다.",
        "summary_flow": ["species 겉보기 꼴/종류", "specificus 종류를 가르는", "specific 구체적인/특정한", "대상의 고유한", "스펙/상세 명세"],
        "quiz": [
            {"question": "Could you be more __________ about your request?", "translation": "당신의 요청에 대해 조금 더 구체적으로 말씀해 주시겠어요?", "answer": "specific"},
            {"question": "This behavior is __________ to this species of birds.", "translation": "이 행동은 이 조류 종에게만 나타나는 고유한(특정한) 것이다.", "answer": "specific"}
        ]
    },
    {
        "word": "utilize",
        "pronunciation": "YOO-tuh-lyz",
        "meaning1": "이용하다, 활용하다 (목적 달성을 위해 효과적으로 쓰다)",
        "meaning2": "수단화하다, 이용(악용)하다 (추상적 대상 조종)",
        "intro": "단순히 물건을 그냥 '쓰는(use)' 것과 '활용하는(utilize)' 것은 어떤 학술적 어원의 차이가 있을까요?",
        "etymology": {
            "root1": "util (L. uti : to use / 사용하다, 유용하다)",
            "root2": "-ize (Suffix : ~화하다, 동사화)",
            "flow": ["물건의 잠재 가치를 유용한 상태로 전환하다", "필요한 목적에 부합하도록 영리하게 이용하다", "이용하다, 활용하다", "타인이나 제도를 나를 위한 도구로 쓰다 (악용/수단화)"]
        },
        "examples1": [
            {"en": "The local people utilize the language to reflect their realities.", "ko": "지역 사람들은 자신들의 현실을 반영하기 위해 그 언어를 활용한다."},
            {"en": "We must utilize all available resources.", "ko": "우리는 이용 가능한 모든 자원을 활용해야 한다."}
        ],
        "transition_question": "도구의 쓸모를 100% 뿜어내게 하는 활용이 어떻게 사람을 \"수단화\"하게 되었을까요?",
        "logic_flow": ["쓸모없어 방치되던 요소의 가치를 발견함 (uti)", "↓", "가공을 통해 내 목적에 부합하게끔 체계화시킴 (utilize)", "↓", "효과와 효율성을 대폭 높여 영리하게 활용함", "↓", "순수한 가치를 훼손하고 나만의 사리사욕의 징검다리로 삼음 (수단화)"],
        "logic_desc": "물건의 내재된 '유용성(Utility)'을 극대화하여 도구화시키는 적극적 활용에서, 대상을 영악하게 나의 수단으로 조종하는 부정적 이용으로 의미가 수렴됩니다.",
        "examples2": [
            {"en": "She knew how to utilize her networking skills.", "ko": "그녀는 자신의 인맥 구축 기술을 어떻게 활용하는지 알고 있었다."},
            {"en": "The politician tried to utilize the crisis for his campaign.", "ko": "그 정치인은 캠페인을 위해 그 위기를 활용하려고(이용해 먹으려고) 시도했다."}
        ],
        "feeling": "utilize = 유용하게(util) 만들다(-ize) = 잠재력을 끌어내다 = 효과적으로 활용하다 = 수단화하다",
        "real_tip": "use는 일상 전반의 '사용'을, utilize는 방치되던 자원의 효율성을 극대화하여 '활용'할 때 주로 씁니다.",
        "summary_flow": ["uti 사용하다", "utilis 유용한", "utilize 유용하게 기능시키다", "도구적 활용", "수단화/악용"],
        "quiz": [
            {"question": "How do you __________ the solar energy in this building?", "translation": "이 건물에서 태양 에너지를 어떻게 활용합니까?", "answer": "utilize"},
            {"question": "They will __________ this loophole to avoid taxes.", "translation": "그들은 세금을 피하기 위해 이 법적 허점을 이용할(악용할) 것이다.", "answer": "utilize"}
        ]
    },
    {
        "word": "accurately",
        "pronunciation": "AK-yer-it-lee",
        "meaning1": "정확하게 (지극한 정성을 쏟아 과녁에 맞닿게)",
        "meaning2": "빈틈없이, 정밀하게 (추상적 정보 오류 제로)",
        "intro": "'정성을 기울여 걱정한다'는 뜻의 어근이 왜 수학적이고 과학적인 '정확하게'가 되었을까요?",
        "etymology": {
            "root1": "ac- (L. ad- : to / ~에, 맞닿아)",
            "root2": "cur (L. cura : care, attention / 정성, 주의, 보살핌) + -ately (Adverb Suffix)",
            "flow": ["정성을 다해 목표물 쪽에 밀착시키다", "정성이 깃들어 실수와 흠이 하나도 없는", "정확하게, 정밀하게", "한 치의 오차도 없이 빈틈없는"]
        },
        "examples1": [
            {"en": "The language is utilized to more accurately reflect their realities.", "ko": "그 언어는 그들의 현실을 더 정확하게 반영하기 위해 활용된다."},
            {"en": "The clock was set to tell the time accurately.", "ko": "그 시계는 시간을 정확하게 가리키도록 설정되었다."}
        ],
        "transition_question": "정성을 쏟아 관리하는 태도가 어떻게 정보의 \"정밀함, 오차 없음\"이 될까요?",
        "logic_flow": ["주의와 정성(cura)을 다해 대상을 정밀 조율함", "↓", "목표 기준선에 한 치의 틈도 없이 딱 밀착(ad)시킴", "↓", "대충 얼버무리지 않고 꼼꼼히 검증하여 오차를 제로로 만듦", "↓", "정보나 수치가 빈틈없이 정확하고 정밀한"],
        "logic_desc": "조금의 태만도 없이 꼼꼼하게 정성(cura)을 쏟아 부어, 오차의 불순물이 끼어들 틈을 원천 봉쇄한 장인의 완성 상태(accurate)를 일컫습니다.",
        "examples2": [
            {"en": "It is difficult to predict the future accurately.", "ko": "미래를 정확하게 예측하는 것은 어렵다."},
            {"en": "We must measure the chemicals accurately.", "ko": "우리는 화학 물질들을 정밀하게(빈틈없이) 측정해야 한다."}
        ],
        "feeling": "accurately = 정성(cur)을 쏟아 기준에 딱(ac) 달라붙게 = 오차 없이 = 정확하게 = 정밀하게",
        "real_tip": "형용사형 accurate(정확한)와 명사형 accuracy(정확도)도 수능 독해 데이터 해석 지문에 단골로 등장합니다.",
        "summary_flow": ["cura 정성/돌봄", "accurare 정성스레 행하다", "accurate 정성을 다해 빈틈없는", "accurately 정확하게", "정밀하게"],
        "quiz": [
            {"question": "The software can __________ translate complex sentences.", "translation": "그 소프트웨어는 복잡한 문장들을 정확하게 번역할 수 있다.", "answer": "accurately"},
            {"question": "He described the crime scene __________ to the police.", "translation": "그는 경찰에게 범죄 현장을 정확하게(세밀하게) 설명했다.", "answer": "accurately"}
        ]
    },
    {
        "word": "reflect",
        "pronunciation": "rih-FLEKT",
        "meaning1": "반사하다, 비추다 (물결이나 빛을 뒤로 꺾어 보내다)",
        "meaning2": "반영하다, 숙고하다 (거울처럼 모습을 드러내거나 생각을 곱씹다)",
        "intro": "빛을 '뒤로 꺾어서 돌려보내는' 물리 현상이 어떻게 생각을 깊이 하는 '반성(성찰)'이 되었을까요?",
        "etymology": {
            "root1": "re- (L. re- : back / 뒤로, 다시)",
            "root2": "flect (L. flectere : to bend / 꺾다, 구부리다)",
            "flow": ["뒤를 향해 꺾어 구부리다", "날아오는 빛이나 에너지를 반대 방향으로 반사하다", "상태나 성질을 거울처럼 고스란히 반영하여 보여주다", "내 생각을 뒤로 꺾어 과거를 차분히 숙고하다 (반성하다)"]
        },
        "examples1": [
            {"en": "The language is used to reflect their daily realities.", "ko": "그 언어는 그들의 일상의 현실을 반영하기 위해 사용된다."},
            {"en": "The mirror reflects the light into the dark room.", "ko": "그 거울은 어두운 방 안으로 빛을 반사한다."}
        ],
        "transition_question": "광선의 반사가 어떻게 마음을 들여다보는 \"성찰과 숙고\"가 될까요?",
        "logic_flow": ["앞으로 나아가던 선이 장벽을 만나 뒤로(re) 꺾임(flectere)", "↓", "외부 대상을 표면에 똑같은 형상으로 비추어 냄 (반사/반영)", "↓", "바깥을 향해 뻗어가던 내 시선을 꺾어 내 내면의 영혼을 비춤", "↓", "지나온 행동의 과오를 차분히 뜯어보며 곱씹음 (반성, 숙고)"],
        "logic_desc": "외부로 직진하던 시선의 각도를 180도 뒤로 구부려(flectere) 자신의 자아와 역사를 들여다보는 내면적 꺾임(reflection)의 철학을 보여줍니다.",
        "examples2": [
            {"en": "The manager needs time to reflect on the failure.", "ko": "그 매니저는 실패에 대해 숙고할(반성할) 시간이 필요하다."},
            {"en": "Her eyes reflect her inner happiness.", "ko": "그녀의 눈은 그녀의 내면의 행복을 반영한다(비춘다)."}
        ],
        "feeling": "reflect = 뒤로(re) 꺾다(flect) = 빛을 반사함 = 실체를 반영함 = 생각을 꺾어 성찰함",
        "real_tip": "reflect on은 '~에 대해 깊이 생각하다, 성찰하다'라는 뜻으로 내신과 수능 시험에 매우 중요하게 출제됩니다.",
        "summary_flow": ["flectere 구부리다", "reflectere 뒤로 구부리다", "reflect 반사하다", "현상을 반영하다", "의견을 숙고/성찰하다"],
        "quiz": [
            {"question": "The calm water __________ the surrounding trees like a mirror.", "translation": "잔잔한 물이 주변 나무들을 거울처럼 비춘다(반사한다).", "answer": "reflects"},
            {"question": "Take a moment to __________ on what you have learned today.", "translation": "오늘 당신이 배운 것에 대해 잠시 성찰하는(숙고하는) 시간을 가지세요.", "answer": "reflect"}
        ]
    },
    {
        "word": "modifications",
        "pronunciation": "mah-dih-fih-KEY-shuhnz",
        "meaning1": "수정, 변경들 (알맞은 척도에 맞추어 고침)",
        "meaning2": "완화, 조절 (한계선 내로 다듬기)",
        "intro": "알맞은 규격이나 분수를 뜻하는 단어가 어떻게 사물의 '수정과 변경들'이 되었을까요?",
        "etymology": {
            "root1": "mod (L. modus : measure, manner, limit / 척도, 분수, 방식)",
            "root2": "fic (L. facere : to make / 만들다) + -ation + -s (Plural)",
            "flow": ["알맞은 척도에 부합하도록 다듬어 만들다", "어긋난 부분을 다듬어서 올바르게 바꿈", "원형을 살린 채 부분적으로 고친 수정 사항들", "강도를 줄이거나 조절함"]
        },
        "examples1": [
            {"en": "It is natural for a language to undergo modifications.", "ko": "한 언어가 변형(수정)을 겪는 것은 자연스럽다."},
            {"en": "They made some modifications to the original plan.", "ko": "그들은 원래 계획에 몇 가지 수정(변경)을 가했다."}
        ],
        "transition_question": "척도에 맞게 다듬는 행동이 어떻게 법안이나 계획의 \"완화나 조절\"이 될까요?",
        "logic_flow": ["넘치지도 모자라지도 않은 알맞은 선(modus)을 그림", "↓", "선을 이탈한 삐죽한 불순물을 칼로 깎아 정돈함(facere)", "↓", "기성 설계도의 치명적 에러를 척도에 맞게 고침 (수정, 변형)", "↓", "지나치게 날카로운 법안을 둥글게 깎아 한계 내로 단속함 (완화)"],
        "logic_desc": "적절한 한계와 척도(Modus)를 잣대로 삼아, 과도하거나 잘못된 부위를 부드럽게 고쳐서 맞추어 놓은(modification) 흔적들입니다.",
        "examples2": [
            {"en": "We had to request modifications to our contract terms.", "ko": "우리는 계약 조건에 대한 수정을 요청해야 했다."},
            {"en": "The modifications of the rules made the game safer.", "ko": "규칙의 완화(조정/수정)가 게임을 더 안전하게 만들었다."}
        ],
        "feeling": "modifications = 척도(mod)에 맞춤 = 다듬어서 조금씩 고친 사항들 = 변형/수정안 = 강도 완화",
        "real_tip": "modify(수정하다)는 change와 비슷하지만, '틀은 두고 일부를 개선한다'는 미세한 결이 있습니다.",
        "summary_flow": ["modus 방법/척도", "modificare 척도에 맞게 다듬다", "modification 수정/개량", "복수화", "수정 및 변형들"],
        "quiz": [
            {"question": "The engine required minor __________ to run smoothly.", "translation": "그 엔진은 부드럽게 작동하기 위해 소폭의 수정(개조)이 필요했다.", "answer": "modifications"},
            {"question": "The architect proposed several __________ to the blueprint.", "translation": "건축가는 청사진에 대한 몇 가지 수정 사항을 제안했다.", "answer": "modifications"}
        ]
    },
    {
        "word": "noticeable",
        "pronunciation": "NOH-tis-uh-buhl",
        "meaning1": "눈에 띄는, 두드러진 (인지할 수 있는)",
        "meaning2": "주목할 만한, 중요한 (가치가 확연히 드러나는)",
        "intro": "'알아채다'라는 동사에서 어떻게 모두의 시선을 착 잡아끄는 '눈에 띄는'이라는 단어가 나왔을까요?",
        "etymology": {
            "root1": "not (L. noscere : to know / 알다, 마음에 담다)",
            "root2": "notice (인지하다, 알림) + -able (Suffix : 할 수 있는)",
            "flow": ["쉽게 머릿속으로 파악하고 알 수 있는", "가만히 있어도 감각에 와 닿아 느껴지는", "눈에 띄는, 확연히 두드러진", "무시할 수 없이 몹시 중요하고 주목할 만한"]
        },
        "examples1": [
            {"en": "The change is particularly noticeable in vocabulary.", "ko": "그 변화는 특히 어휘에서 눈에 띄게 두드러진다."},
            {"en": "There was a noticeable increase in temperature.", "ko": "기온의 눈에 띄는 상승이 있었다."}
        ],
        "transition_question": "쉽게 감지할 수 있다는 속성이 어떻게 가치의 \"중요성\"으로 전이되었을까요?",
        "logic_flow": ["내면의 지식 창고에 정보가 꽂혀 알게 됨 (noscere)", "↓", "의도적으로 찾으려 하지 않아도 뇌리에 포착됨 (notice)", "↓", "윤곽과 경계선이 뚜렷하여 눈동자를 잡아끄는 (눈에 띄는)", "↓", "절대 흘려보낼 수 없을 만큼 영향력이 큼 (주목할 만한, 중요한)"],
        "logic_desc": "주체가 대상을 쉽게 알아차리고(notice) 감각할 수 있을 만큼, 대상이 뿜어내는 색깔이나 윤곽이 명확하고 두드러진(noticeable) 상태를 뜻합니다.",
        "examples2": [
            {"en": "She showed a noticeable improvement in her English speaking.", "ko": "그녀는 영어 말하기에서 눈에 띄는(주목할 만한) 향상을 보였다."},
            {"en": "His absence was noticeable during the meeting.", "ko": "회의 중에 그의 부재가 눈에 띄었다(확연히 드러났다)."}
        ],
        "feeling": "noticeable = 알아챌(notice) 수 있는(-able) = 시선이 꽂히는 = 두드러진 = 주목할 만한",
        "real_tip": "부사형인 noticeably(두드러지게)도 그래프나 지표 변화를 설명하는 도표 독해 지문에 빈출됩니다.",
        "summary_flow": ["noscere 알다", "notitia 알림/지식", "notice 인지하다", "noticeable 인지할 수 있는", "눈에 띄는 / 주목할 만한"],
        "quiz": [
            {"question": "The scar on his face became less __________ over time.", "translation": "시간이 흐르면서 그의 얼굴에 있는 흉터는 덜 눈에 띄게 되었다.", "answer": "noticeable"},
            {"question": "There is a __________ difference between the two products.", "translation": "두 제품 사이에는 눈에 띄는 차이가 존재한다.", "answer": "noticeable"}
        ]
    },
    {
        "word": "coined",
        "pronunciation": "koynd",
        "meaning1": "주조했다, 화폐를 찍어냈다 (쐐기 도장으로 쾅 누르다)",
        "meaning2": "(신조어를) 만들어냈다, 주조했다 (새로운 말을 발명하다)",
        "intro": "주머니 속의 '동전(coin)'이 어떻게 새로운 단어를 '만들어내다'라는 움직임으로 변했을까요?",
        "etymology": {
            "root1": "coin (L. cuneus : wedge, corner / 쐐기, 화폐 인쇄용 금형 쐐기)",
            "root2": "-ed (Suffix : 과거형/과거분사)",
            "flow": ["쐐기 모양의 강철 도장으로 금속판을 누르다", "금속을 찍어 정식 화폐를 주조했다", "금형 도장으로 찍어내듯 세상에 없던 새 어휘를 발명했다", "신조어가 만들어졌다"]
        },
        "examples1": [
            {"en": "In Indian English, the term 'prepone' was coined.", "ko": "인도 영어에서 'prepone'이라는 용어가 새로 만들어졌다."},
            {"en": "The king coined silver coins to boost trade.", "ko": "왕은 무역을 활성화하기 위해 은화를 주조했다."}
        ],
        "transition_question": "쇠붙이를 쾅 내리쳐 동전을 찍어내던 행동이 어떻게 언어의 \"발명\"이 될까요?",
        "logic_flow": ["쐐기 도장(cuneus)을 쇠망치로 때려 문양을 고정함", "↓", "그 나라에서 통용되는 공인 화폐를 제조함 (주조하다)", "↓", "혼란스럽던 개념들에 기표(외형)를 딱 때려 박아 공인시킴", "↓", "세상에 없던 새로운 신조어를 처음으로 깎아 만듦 (창조/발명함)"],
        "logic_desc": "말랑한 금속판에 강철 도장을 찍어 단단한 화폐(coin)를 완성하듯, 형태 없는 생각 위에 새로운 음운의 이름표를 쾅 찍어서 언어(coined)로 공인해 낸 지적 작업입니다.",
        "examples2": [
            {"en": "The phrase 'cyberpunk' was coined in the 1980s.", "ko": "'cyberpunk'라는 문구는 1980년대에 만들어졌다(창조되었다)."},
            {"en": "Who coined this famous expression?", "ko": "누가 이 유명한 표현을 만들어 냈습니까?"}
        ],
        "feeling": "coined = 쐐기 도장으로 쾅 눌러 찍었다 = 고착화시켰다 = 단어를 주조했다 = 신조어를 만들었다",
        "real_tip": "coin a word/phrase는 '단어/문구를 신조하다'라는 고난도 영어 관용구로 수능 어휘 시험에 매우 자주 나옵니다.",
        "summary_flow": ["cuneus 쐐기", "coigne 모퉁이 쐐기돌", "coin 화폐를 찍다", "신조어를 만들다", "과거분사형 coined"],
        "quiz": [
            {"question": "Many new IT terms were __________ in Silicon Valley.", "translation": "많은 새로운 IT 용어들이 실리콘 밸리에서 만들어졌다.", "answer": "coined"},
            {"question": "The currency was __________ and distributed nationwide.", "translation": "그 화폐는 주조되어 전국에 유통되었다.", "answer": "coined"}
        ]
    },
    {
        "word": "opposite",
        "pronunciation": "AHP-uh-zit",
        "meaning1": "정반대의, 맞은편의 (반대 방향을 마주보게 놓아둔)",
        "meaning2": "상반되는 것, 반대 세력 (추상적 대립 개념/사람)",
        "intro": "서로 '마주 보게 놓여 있는' 물리적 배치가 어떻게 논리적 '정반대'와 '대립 세력'이 될까요?",
        "etymology": {
            "root1": "op- (L. ob- : against, in front of / 마주보고, 반대하여)",
            "root2": "pos (L. ponere : to place, put / 두다, 놓다) + -ite (Suffix)",
            "flow": ["반대 방향으로 마주 보게 서로를 놓다", "길 건너편에 마주 서 있는", "성질이나 방향이 완전하게 등진 정반대의", "상반되는 대립 개념 / 반대의 것"]
        },
        "examples1": [
            {"en": "The term 'prepone' was coined as the opposite of 'postpone'.", "ko": "'prepone'이라는 용어는 'postpone'의 정반대(반의어)로 만들어졌다."},
            {"en": "They live on the opposite side of the street.", "ko": "그들은 길 맞은편(반대편)에 산다."}
        ],
        "transition_question": "눈앞에 마주 놓인 공간 구도가 어떻게 논리의 \"상반된 모순\"이 될까요?",
        "logic_flow": ["눈동자를 교차하며 상대와 직면(ob)하는 각도를 잡음", "↓", "서로 다른 영역에 대상을 배치하여 놓아둠(ponere)", "↓", "맞은편에 적으로 마주 선 (건너편의)", "↓", "성격과 논리가 모순되어 하나로 합쳐질 수 없는 (정반대의)", "↓", "정반대의 개념이나 반대의 색깔"],
        "logic_desc": "시선이 정면충돌하는 길 건너편 마주 보기(ob-ponere)의 구도가, 논리학으로 들어와 서로 양립할 수 없는 상반되는 모순(opposite)의 형세로 정교화되었습니다.",
        "examples2": [
            {"en": "Love is not the opposite of hate; it is indifference.", "ko": "사랑은 미움의 정반대(상반되는 것)가 아니다. 그것은 무관심이다."},
            {"en": "The two brothers held opposite views on politics.", "ko": "두 형제는 정치에 대해 상반되는(정반대의) 견해를 가졌다."}
        ],
        "feeling": "opposite = 맞은편에 마주보게(ob) 놓아둔(pose) = 건너편의 = 상반된 = 정반대인 것",
        "real_tip": "the opposite of는 '~의 반대말'을 가리키며, 빈칸 완성에서 단서의 역접(반의어) 논리를 잡는 키워드입니다.",
        "summary_flow": ["ponere 두다", "opponere 반대하여 두다", "oppositus 맞은편에 대립된", "opposite 정반대의", "반대의 것/반의어"],
        "quiz": [
            {"question": "White is the __________ of black.", "translation": "흰색은 검은색의 정반대이다.", "answer": "opposite"},
            {"question": "He ran in the __________ direction to escape.", "translation": "그는 탈출하기 위해 정반대 방향으로 달렸다.", "answer": "opposite"}
        ]
    },
    {
        "word": "postpone",
        "pronunciation": "pohst-POHN",
        "meaning1": "미루다, 연기하다 (일정을 시간축의 뒤에 놓아두다)",
        "meaning2": "경시하다, 후순위로 두다 (가치 평가의 뒤로 배치함)",
        "intro": "달력의 빈 칸을 '뒤로 배치하는' 행위가 어떻게 우리가 매일 외우는 '연기하다'가 되었을까요?",
        "etymology": {
            "root1": "post- (L. post- : after, behind / 뒤에, 나중에)",
            "root2": "pone (L. ponere : to place, put / 놓다, 두다)",
            "flow": ["일정이나 물건을 기준선보다 뒤에 가져다 놓다", "약속 날짜를 미래의 뒤 시점으로 배치하다", "뒤로 미루다, 연기하다", "중요도를 뒤로 밀어 경시하다"]
        },
        "examples1": [
            {"en": "We had to postpone the meeting due to the storm.", "ko": "우리는 폭풍우 때문에 회의를 연기해야(미뤄야) 했다."},
            {"en": "Do not postpone what you can do today.", "ko": "당신이 오늘 할 수 있는 일을 뒤로 미루지 마라."}
        ],
        "transition_question": "시간표를 뒤로 옮겨 잡는 것이 어떻게 가치관에서 중요도를 \"경시하다\"가 될까요?",
        "logic_flow": ["오늘 처리해야 할 항목을 들어 올림", "↓", "현재 타임라인 밖의 미래의 저편(post)에다가 올려놓음(ponere)", "↓", "약속이나 일정을 연기함 (미루다)", "↓", "가장 중요하게 처리해야 할 리스트에서 후순위로 던져버림", "↓", "중요치 않게 취급해 경시하다"],
        "logic_desc": "시간 선(timeline)상의 뒤쪽에 약속을 던져 두는(ponere) 물리적 행위가, 가치관의 우선순위 선반에서 맨 뒤 칸으로 밀어내는 경시(postponement)로 개념 전이되었습니다.",
        "examples2": [
            {"en": "They had to postpone their career plans for their children.", "ko": "그들은 아이들을 위해 그들의 커리어 계획을 후순위로 미뤄야(경시해야) 했다."},
            {"en": "The decision was postponed until further analysis.", "ko": "그 결정은 추가 분석이 있을 때까지 연기되었다."}
        ],
        "feeling": "postpone = 나중에(post) 하도록 놓아두다(pone) = 미루다 = 후순위로 미뤄 경시하다",
        "real_tip": "put off, delay, hold over 등과 동의어 세트로 묶이며, 'postpone A until B' 구문으로 독해에 다수 기입됩니다.",
        "summary_flow": ["ponere 놓다", "postponere 뒤에 놓다", "postpone 미루다", "일정 연기", "중요성을 뒤로 두다/경시하다"],
        "quiz": [
            {"question": "We had to __________ the outdoor concert because of rain.", "translation": "우리는 비 때문에 야외 콘서트를 연기해야 했다.", "answer": "postpone"},
            {"question": "It is unwise to __________ decisions of such importance.", "translation": "그렇게 중요한 결정들을 후순위로 미루는(경시하는) 것은 현명하지 못하다.", "answer": "postpone"}
        ]
    },
    {
        "word": "encouragement",
        "pronunciation": "in-KUR-ij-muhnt",
        "meaning1": "격려, 위로 (타인의 심장 속에 용기를 불어넣음)",
        "meaning2": "조장, 권장, 장려 (행동을 부추겨 확산시킴)",
        "intro": "사람의 가슴속에 '심장(용기)'을 쑤셔 박아주는 행동이 어떻게 비즈니스의 '장려와 권장'이 되었을까요?",
        "etymology": {
            "root1": "en- (L. in- : into, make / 안으로, 만들다)",
            "root2": "cour (L. cor : heart / 심장, 용기, 마음) + -age + -ment (Suffix : 명사화)",
            "flow": ["가슴속에 심장(cor)을 들이받아 주입하다", "두려움을 몰아내고 용기를 만들어주다", "위로하고 힘을 돋우는 격려", "특정 행동을 활성화시키는 권장, 장려"]
        },
        "examples1": [
            {"en": "They shout 'add oil' to show encouragement or support.", "ko": "그들은 격려나 지지를 보여주기 위해 'add oil'을 외친다."},
            {"en": "The teacher's words gave great encouragement to the student.", "ko": "선생님의 말씀은 그 학생에게 큰 격려(용기)가 되었다."}
        ],
        "transition_question": "심리적 용기를 심어주는 격려가 어떻게 시장 제도의 \"장려와 조장\"이 될까요?",
        "logic_flow": ["두려움으로 얼어붙어 멈춰 선 타인에게 다가감", "↓", "그의 가슴 안(en)에 불타는 심장(cor)을 이식해 줌", "↓", "다시 달릴 수 있도록 기를 불어넣음 (격려)", "↓", "소비나 출산을 머뭇거리는 대중에게 혜택을 주어 발동을 검", "↓", "제도적 권장, 행동의 장려"],
        "logic_desc": "주저하는 사람의 내면 깊숙이 뜨거운 심장(cor)을 던져 넣어서(en-) 앞으로 전진하게 시동을 걸어주는 모든 동력 전달(encouragement) 행위입니다.",
        "examples2": [
            {"en": "Government policies offer encouragement for small businesses.", "ko": "정부 정책은 중소기업들에게 권장(장려 혜택)을 제공한다."},
            {"en": "There was little financial encouragement to complete the project.", "ko": "그 프로젝트를 완료하기 위한 재정적 장려책(유인)이 거의 없었다."}
        ],
        "feeling": "encouragement = 심장(cour)을 가슴 안에(en) 이식함 = 용기를 북돋움 = 격려 = 행동 장려책",
        "real_tip": "동사형인 encourage는 대표적인 5형식 동사로, 'encourage + 목적어 + to부정사' 구조를 뇌에 박아두어야 어법을 맞춥니다.",
        "summary_flow": ["cor 심장/마음", "encourage 용기를 주다", "encouraging 힘을 주는", "encouragement 격려", "행동 유도/장려책"],
        "quiz": [
            {"question": "He needed some __________ to speak up during the debate.", "translation": "그는 토론 중에 당당히 말할 수 있도록 약간의 격려(용기)가 필요했다.", "answer": "encouragement"},
            {"question": "The tax cuts provided __________ for foreign investment.", "translation": "감세 조치는 외국인 투자를 위한 장려(유도책)를 제공했다.", "answer": "encouragement"}
        ]
    },
    {
        "word": "translation",
        "pronunciation": "trans-LEY-shuhn",
        "meaning1": "번역, 해석 (의미를 다른 강 건너로 실어 나름)",
        "meaning2": "변환, 상태 전이 (차원이나 양식의 변경)",
        "intro": "짐짝을 '강 건너 저편으로 실어 나르는' 노역이 어떻게 인류 최고의 지적 행동인 '번역'이 되었을까요?",
        "etymology": {
            "root1": "trans- (L. trans- : across / 건너서, 저편으로)",
            "root2": "lat (L. latus < ferre : to carry, bear / 실어 나르다, 가져가다) + -ion (Suffix)",
            "flow": ["강 건너 저쪽으로 물건을 실어 나르다", "한 언어의 뜻을 다른 언어의 땅으로 그대로 옮기다", "번역, 해석", "에너지나 물질의 상태를 다른 차원으로 바꿈 (변환)"]
        },
        "examples1": [
            {"en": "This expression is a direct translation from a Chinese expression.", "ko": "이 표현은 중국어 표현에서 그대로 직역(직접 번역)한 것이다."},
            {"en": "The translation of the bible took several years.", "ko": "성경의 번역은 수년이 걸렸다."}
        ],
        "transition_question": "경계를 넘어 의미를 운반하는 번역이 어떻게 형태를 바꾸는 \"변환과 이동\"이 될까요?",
        "logic_flow": ["이쪽 강기슭에 있던 정보 뭉치를 배에 선적함", "↓", "국경선 강줄기 너머(trans) 반대편 기슭으로 가로질러 감", "↓", "반대편 부두에 짐을 하역하여(latus) 동일하게 조립해 냄 (번역)", "↓", "디지털 신호나 에너지를 물리적 움직임으로 바꿔놓음 (변환, 전이)"],
        "logic_desc": "어떤 기호를 경계선 너머(trans-)로 고스란히 이송하여, 저편의 문법에 맞게 재구성해 주는 의미 수송 작업(translation)을 의미합니다.",
        "examples2": [
            {"en": "We need the translation of theoretical concepts into practical actions.", "ko": "우리는 이론적 개념을 실제적인 행동으로 변환하는(바꾸는) 것이 필요하다."},
            {"en": "The motor handles the translation of electrical energy into motion.", "ko": "그 모터는 전기 에너지를 운동 에너지로 변환(전이)하는 것을 처리한다."}
        ],
        "feeling": "translation = 경계 건너편으로(trans) 실어 나름(lat) = 문맥을 바꿈 = 번역 = 차원의 변환",
        "real_tip": "simultaneous translation은 '동시 통역'을 의미하며, translate A into B는 'A를 B로 번역/변환하다'로 출제됩니다.",
        "summary_flow": ["ferre 나르다", "transferre 가로질러 옮기다", "translatus 옮겨진", "translation 언어의 번역", "추상적 상태 변환/전이"],
        "quiz": [
            {"question": "The French __________ of the novel was excellent.", "translation": "그 소설의 프랑스어 번역본은 훌륭했다.", "answer": "translation"},
            {"question": "We observed the __________ of genes into active proteins.", "translation": "우리는 유전자가 활성 단백질로 변환(발현)되는 것을 관찰했다.", "answer": "translation"}
        ]
    },
    {
        "word": "inject",
        "pronunciation": "in-JEKT",
        "meaning1": "주입하다, 주사하다 (안으로 세차게 쏘아 던지다)",
        "meaning2": "도입하다, 불어넣다 (대화나 자금에 활력을 밀어 넣음)",
        "intro": "속으로 '무언가를 던져 넣는' 힘이 어떻게 병원에서의 '주사'와 분위기의 '활력 불어넣기'가 되었을까요?",
        "etymology": {
            "root1": "in- (L. in- : into / 안으로)",
            "root2": "ject (L. jacere : to throw / 던지다, 쏘다)",
            "flow": ["안쪽 깊은 곳으로 던져 밀어 넣다", "주사기를 통해 몸 안으로 약물을 쏘다 (주입/주사하다)", "자금이나 에너지를 시장이나 프로젝트에 강제로 집어넣다", "대화 속에 활력이나 농담을 획기적으로 불어넣다"]
        },
        "examples1": [
            {"en": "They shout 'add oil', originally meaning to inject more gasoline.", "ko": "그들은 원래 휘발유를 더 주입하라는 의미였던 'add oil'을 외친다."},
            {"en": "The nurse will inject the medicine into your arm.", "ko": "간호사가 당신의 팔에 약을 주사(주입)할 것입니다."}
        ],
        "transition_question": "신체에 약물을 쏘는 행위가 어떻게 침체된 조직에 \"활력을 불어넣는\" 일로 변모했을까요?",
        "logic_flow": ["굳게 잠긴 경계 벽면을 확인하고 조준함", "↓", "벽 내부의 깊숙한 곳(in)을 향해 이물질을 힘껏 던짐(jacere)", "↓", "관이나 바늘을 타고 액체가 침투함 (주입하다, 주사하다)", "↓", "자본이나 신선한 아이디어를 침체된 조직에 투입해 판을 뒤흔듦", "↓", "새로운 바람을 불어넣다, 도입하다"],
        "logic_desc": "밀폐된 공간 내부(in)로 이물질을 뚫고 들어가 투척하는(jacere) 강력한 에너지 투사 동작에서 수혈과 도입(injection)의 뜻이 나왔습니다.",
        "examples2": [
            {"en": "We need to inject some humor into this boring meeting.", "ko": "우리는 이 지루한 회의에 유머를 좀 불어넣을(도입할) 필요가 있다."},
            {"en": "The government decided to inject capital into banks.", "ko": "정부는 은행들에 자금을 주입하기(투입하기)로 결정했다."}
        ],
        "feeling": "inject = 내부로(in) 힘껏 던져 넣다(ject) = 약물을 주사하다 = 자금/활력을 불어넣다",
        "real_tip": "reject(거부하다-밖으로 던짐), project(투사하다-앞으로 던짐), eject(배출하다-바깥으로 던짐) 등 ject 어근 패밀리는 100% 시험에 나옵니다.",
        "summary_flow": ["jacere 던지다", "injicere 안으로 던져 넣다", "inject 주입하다", "주사기를 통해 투약하다", "새로운 활력을 도입하다/불어넣다"],
        "quiz": [
            {"question": "They want to __________ new life into the dying project.", "translation": "그들은 죽어가는 프로젝트에 새로운 생명력을 불어넣고(주입하고) 싶어 한다.", "answer": "inject"},
            {"question": "Do not __________ gasoline unless the engine is completely cool.", "translation": "엔진이 완전히 식지 않았다면 가솔린을 주입하지 마라.", "answer": "inject"}
        ]
    },
    {
        "word": "avoid",
        "pronunciation": "uh-VOYD",
        "meaning1": "피하다, 모면하다 (방을 텅 비워두고 사라지다)",
        "meaning2": "무효로 하다, 무위로 돌리다 (법률적 효력을 텅 비게 만듦)",
        "intro": "공간을 '텅 비우는 것'이 어떻게 나쁜 상황을 요리조리 '피하는' 행동이 되었을까요?",
        "etymology": {
            "root1": "a- (L. ex- : out of / 비우다, 떠나다)",
            "root2": "void (L. vacuus : empty / 텅 빈)",
            "flow": ["자리나 집을 완전히 텅 비우고 나가다", "방해물이나 위험에 닿지 않도록 거리를 비우다", "나쁜 접촉을 피해 도망치다, 모면하다", "계약이나 문서의 가치를 텅 비게 하여 무효로 하다"]
        },
        "examples1": [
            {"en": "Kitchens outside the home help avoid trapping heat.", "ko": "집 밖에 있는 부엌들은 열기를 가두는 것을 피하도록 도와준다."},
            {"en": "You should avoid eating too much sugar.", "ko": "당신은 설탕을 너무 많이 먹는 것을 피해야 한다."}
        ],
        "transition_question": "위험을 피하는 일상 행동이 어떻게 법정에서 조항을 \"무효화\"하는 철퇴가 되었을까요?",
        "logic_flow": ["내 눈앞에 유해한 장벽이나 타격을 주는 충돌체가 날아옴", "↓", "접촉 면적을 0으로 만들어 공간을 텅 비게(vacuus) 이탈함", "↓", "부딪히지 않고 무사히 스쳐 감 (피하다, 모면하다)", "↓", "작성된 문장 내부의 논리를 공허하게 지워 비워버림", "↓", "약속이나 계약을 법률적으로 무효로 하다"],
        "logic_desc": "대상이 자리하고 있어야 할 좌표를 텅 빈 상태(void)로 비워버려, 무(無)로 돌리고 피하는(avoid) 회피과 공허의 메커니즘입니다.",
        "examples2": [
            {"en": "Any violation will avoid the warranty automatically.", "ko": "어떤 위반 사항이든 보증을 자동적으로 무효로 만들(비워버릴) 것이다."},
            {"en": "He drove carefully to avoid an accident.", "ko": "그는 사고를 피하기 위해 조심스럽게 운전했다."}
        ],
        "feeling": "avoid = 공간을 비워서(void) 안 부딪히게 하다 = 피하다 = 법률적 효력을 비워 무효화하다",
        "real_tip": "avoid는 목적어로 무조건 동명사(-ing)만을 취합니다. to부정사가 오면 어법 문제에서 틀린 것으로 골라야 합니다.",
        "summary_flow": ["vacuus 텅 빈", "evuidier 텅 비우다", "avoid 피하다/모면하다", "접촉을 회피하다", "계약을 무효로 하다"],
        "quiz": [
            {"question": "Try to __________ making hasty decisions.", "translation": "성급한 결정을 내리는 것을 피하도록 노력하세요.", "answer": "avoid"},
            {"question": "The court can __________ the contract if fraud is proven.", "translation": "사기가 입증된다면 법원은 그 계약을 무효로 할(피할) 수 있다.", "answer": "avoid"}
        ]
    },
    {
        "word": "trapping",
        "pronunciation": "TRAP-ing",
        "meaning1": "가두기, 함정에 빠뜨리기 (덫에 걸리게 하는 행위)",
        "meaning2": "장식, 겉치레, 장신구 (말의 안장 겉을 씌우는 것 - 주로 복수형 trappings)",
        "intro": "짐승을 잡는 '덫(trap)'이 어떻게 귀족들의 화려한 '겉치레 장식'이라는 뜻이 되었을까요?",
        "etymology": {
            "root1": "trap (OE. treppe : snare, trap / 덫, 함정)",
            "root2": "-ing (Suffix : 동명사/현재분사)",
            "flow": ["덫을 놓아 가두기", "열이나 냄새를 밖으로 못 나가게 포획함", "말의 등 뒤에 안장을 고정하기 위해 단단히 씌우는 띠", "겉으로 보이는 신분의 장식물, 겉치레"]
        },
        "examples1": [
            {"en": "They cook outside to avoid trapping heat inside the house.", "ko": "그들은 집안에 열기를 가두는 것을 피하기 위해 밖에서 요리한다."},
            {"en": "The police were successful in trapping the thief.", "ko": "경찰은 도둑을 가두는(생포하는) 데 성공했다."}
        ],
        "transition_question": "짐승을 포획하는 덫이 어떻게 사람을 꾸미는 \"장신구와 겉치레\"가 되었을까요?",
        "logic_flow": ["짐승의 목을 조여 가두는 나무 틀과 올가미 (trap)", "↓", "통제선 밖으로 열이나 냄새, 생물이 탈출하지 못하게 포획하여 결박함", "↓", "말의 등을 단단히 옥죄어 감싸 덮는 마구와 담요 장식", "↓", "공식 직위나 권력을 가진 사람의 겉모양을 화려하게 옭아매서 꾸미는 장신구, 겉치레 (trappings)"],
        "logic_desc": "달아나지 못하도록 '옭아매어 감싸 가두는 것(trapping)'에서 시작하여, 신분을 규정하기 위해 화려하게 몸을 감싸 안는 지위의 포장지(trappings)로 전이되었습니다.",
        "examples2": [
            {"en": "He had all the trappings of power but no real authority.", "ko": "그는 권력의 온갖 겉치레(장식)를 가졌으나 실권은 없었다.", "word_origin": "trappings"},
            {"en": "We must recognize the trapping of energy by greenhouse gases.", "ko": "우리는 온실가스에 의한 에너지의 가두기(축적)를 인지해야 한다."}
        ],
        "feeling": "trapping = 덫을 놓아 가둠 = 탈출 차단하기 = 말의 몸을 고정해 감싼 장식물 = 겉치레 장식",
        "real_tip": "시험에 동명사로 '가두기(trapping)'가 출제될 때, avoid 뒤의 동명사 목적으로 쓰여 trapping 형태로 변형되는 것을 주의해야 합니다.",
        "summary_flow": ["treppe 덫/올가미", "trap 덫으로 가두다", "trapping 가둠 / 덫으로 잡기", "복수화 trappings", "신분 장신구 / 겉치레"],
        "quiz": [
            {"question": "Greenhouse effect is caused by the __________ of infrared radiation.", "translation": "온실효과는 적외선 복사열을 가두는 것(포착)에 의해 유발된다.", "answer": "trapping"},
            {"question": "He enjoyed the luxury and all the __________ of wealth.", "translation": "그는 사치와 부유함의 온갖 겉치레(장식물)들을 즐겼다. (힌트: 복수형)", "answer": "trappings"}
        ]
    },
    {
        "word": "expansion",
        "pronunciation": "ik-SPAN-shuhn",
        "meaning1": "확장, 팽창 (날개를 바깥으로 넓게 펼침)",
        "meaning2": "부연, 상세한 설명 (논리에 살을 붙여 펼침)",
        "intro": "접혀있던 날개를 '밖으로 활짝 펴는' 동작이 어떻게 회사 매출의 '확장'과 논리의 '부연'이 될까요?",
        "etymology": {
            "root1": "ex- (L. ex- : out / 밖으로)",
            "root2": "pans (L. pandere : to spread, stretch / 펼치다, 넓히다) + -ion (Suffix)",
            "flow": ["접힌 자락을 바깥으로 활짝 펼쳐놓다", "영토나 부피가 물리적으로 커짐 (확장, 팽창)", "사업이나 어휘의 영역이 넓어짐", "말의 뼈대에 상세한 살을 붙임 (부연 설명)"]
        },
        "examples1": [
            {"en": "These expressions contribute to the expansion of vocabulary.", "ko": "이러한 표현들은 어휘의 확장에 기여한다."},
            {"en": "The expansion of the universe is still ongoing.", "ko": "우주의 팽창(확장)은 여전히 진행 중이다."}
        ],
        "transition_question": "공간적인 영토 확장이 어떻게 말글의 \"상세한 부연 설명\"이 될까요?",
        "logic_flow": ["안쪽으로 조밀하게 압축되어 감춰진 덩어리", "↓", "경계 막을 허물고 밖(ex)으로 날개를 쫙 뻗침(pandere)", "↓", "차지하는 점유 면적의 급격한 늘어남 (확장, 팽창)", "↓", "요약본 문서에 논리적 데이터 살을 듬뿍 붙여 늘여 놓음", "↓", "상세한 설명, 부연"],
        "logic_desc": "바깥(ex)을 향해 팽팽하게 펼치는(pandere) 역동에서 부피의 확장(expansion)과 글자 수의 증폭(부연 설명)이 나란히 도출되었습니다.",
        "examples2": [
            {"en": "This essay is an expansion of a short article he wrote.", "ko": "이 에세이는 그가 쓴 짧은 글의 부연(상세한 확장본)이다."},
            {"en": "The company planned a rapid global expansion.", "ko": "그 회사는 빠른 전 세계적 확장을 계획했다."}
        ],
        "feeling": "expansion = 바깥으로(ex) 펼친(pan) 결과 = 부피가 늘어남 = 확장/팽창 = 부연 설명",
        "real_tip": "동사형인 expand(확장하다)는 expend(돈/시간을 소비하다)와 모음이 달라 어휘 시험에 매우 단골로 비교 출제됩니다.",
        "summary_flow": ["pandere 펼치다", "expandere 밖으로 넓게 펴다", "expansio 팽창", "expansion 물리적 확장", "학술적 부연 설명"],
        "quiz": [
            {"question": "The city underwent a rapid __________ during the 1990s.", "translation": "그 도시는 1990년대 동안 급격한 확장을 겪었다.", "answer": "expansion"},
            {"question": "Her new book is an __________ of her doctoral thesis.", "translation": "그녀의 새 책은 그녀의 박사 학위 논문의 부연(상세한 확장본)이다.", "answer": "expansion"}
        ]
    },
    {
        "word": "diversification",
        "pronunciation": "dih-vur-sih-fih-KEY-shuhn",
        "meaning1": "다양화, 다각화 (여러 갈래로 쪼개어 돌려 만듦)",
        "meaning2": "분산 투자 (위험 회피를 위해 쪼개어 나누기)",
        "intro": "한 길로 걷던 흐름을 '여러 갈래로 돌려놓는 것'이 왜 금융 시장의 '분산 투자'가 될까요?",
        "etymology": {
            "root1": "di- (L. dis- : apart / 갈라져, 따로)",
            "root2": "vers (L. vertere : to turn / 돌리다) + fic (facere : to make) + -ation",
            "flow": ["따로 갈라져서 돌게 만들다", "한곳으로 쏠리지 않게 다양하게 가닥을 쪼개다", "다양성 증대, 다양화, 다각화", "돈을 여러 바구니에 나누어 담는 분산 투자"]
        },
        "examples1": [
            {"en": "These expressions contribute to the diversification of the English vocabulary.", "ko": "이러한 표현들은 영어 어휘의 다양화(다각화)에 기여한다."},
            {"en": "The diversification of crops saved the farmers from famine.", "ko": "작물의 다양화(다각화)가 농부들을 기근으로부터 구했다."}
        ],
        "transition_question": "품목을 여러 개로 쪼개는 다양화가 어떻게 재정적인 \"분산 투자\"가 될까요?",
        "logic_flow": ["한 바구니에 모든 계란을 쏠리게 담아둠 (위험)", "↓", "바구니를 여러 방향(dis-vertere)으로 분할함", "↓", "구조나 형태가 다채로워짐 (다양화, 다각화)", "↓", "자산을 여러 투자처로 쪼개어 배치해 충격을 흡수하게 함", "↓", "재정적 분산 투자"],
        "logic_desc": "한 갈래에만 기대지 않고 쪼개어 각각 다르게 돌려놓음(diversify)으로써, 풍요로움을 얻고 위험을 분산하는(diversification) 지혜입니다.",
        "examples2": [
            {"en": "Portfolio diversification reduces investment risks.", "ko": "포트폴리오 분산 투자는 투자 위험을 감소시킨다."},
            {"en": "The company decided on the diversification of its product line.", "ko": "그 회사는 제품 라인의 다각화(다양화)를 결정했다."}
        ],
        "feeling": "diversification = 갈라져 돌게(diverse) 만듦(fic) = 획일화 방지 = 다양화 = 자산 분산 투자",
        "real_tip": "경영/경제 독해 지문에서 'don't put all your eggs in one basket' 속담과 함께 분산 투자(diversification)로 단골 등장합니다.",
        "summary_flow": ["vertere 돌리다", "divertere 갈라져 돌다", "diversify 다양화하다", "diversification 다양화", "분산 투자"],
        "quiz": [
            {"question": "The region needs economic __________ to create new jobs.", "translation": "그 지역은 새로운 일자리를 창출하기 위해 경제적 다각화(다양화)가 필요하다.", "answer": "diversification"},
            {"question": "We recommend the __________ of your stocks.", "translation": "우리는 당신 주식의 분산 투자를 권장합니다.", "answer": "diversification"}
        ]
    },
    {
        "word": "incorporated",
        "pronunciation": "in-KAWR-puh-rey-tid",
        "meaning1": "포함된, 편입된 (하나의 큰 몸뚱이 안으로 집어넣은)",
        "meaning2": "법인 조직의, 주식회사의 (법적 육체를 부여받은 - 약어 Inc.)",
        "intro": "보이지 않는 추상적 요소를 큰 '몸통(육체)' 안으로 우겨넣는 행위가 왜 '주식회사'가 될까요?",
        "etymology": {
            "root1": "in- (L. in- : into, make / 안으로, 만들다)",
            "root2": "corpor (L. corpus : body / 몸, 신체, 육체) + -ate + -ed (Suffix)",
            "flow": ["하나의 거대한 몸통 안으로 집어넣다", "보이지 않는 시스템을 눈에 보이는 신체로 엮어 포함시키다", "포함된, 편입된", "법적 실물 몸뚱아리 자격을 취득한 법인 주식회사의"]
        },
        "examples1": [
            {"en": "English dictionaries have incorporated words borrowed from foreign languages.", "ko": "영어 사전들은 외국어에서 차용된 단어들을 포함해왔다(편입시켜왔다)."},
            {"en": "The new features were incorporated into the design.", "ko": "새로운 기능들이 디자인에 포함되었다(통합되었다)."}
        ],
        "transition_question": "몸통 안에 편입되는 것이 어떻게 법을 입은 유한회사 \"주식회사\"가 되었을까요?",
        "logic_flow": ["영혼만 존재하던 개념 덩어리", "↓", "물리적인 실물 육체(corpus)의 형상을 갖추게 만듦(in)", "↓", "기성 조직의 뼈대 장기 세포 속으로 합쳐 묶음 (포함된, 편입된)", "↓", "법률이 인정한 독립적 신체 자격을 획득함 (법인격 취득)", "↓", "유한 책임의 주식회사 (Incorporated, Inc.)"],
        "logic_desc": "실체가 없던 것들을 하나로 모아 영양분이 가득한 유기적 몸뚱이(Corpus) 안으로 집어넣어(incorporate) 하나로 결합하고 법적 실체를 주는 일입니다.",
        "examples2": [
            {"en": "He works for Apple Incorporated.", "ko": "그는 애플 주식회사(법인)에서 일한다."},
            {"en": "The design incorporated suggestions from users.", "ko": "그 디자인은 사용자들의 제안을 반영했다(포함했다)."}
        ],
        "feeling": "incorporated = 몸통(corpor) 안으로(in) 밀어 넣었다 = 뼈대에 편입된 = 법적 신체를 입은 주식회사",
        "real_tip": "회사명 뒤에 붙는 'Inc.'가 바로 'Incorporated'의 약어이며, 독해 시 주식회사라는 뜻과 포함되었다는 뜻을 다 아셔야 합니다.",
        "summary_flow": ["corpus 몸/육체", "incorporare 몸 안으로 흡수하다", "incorporate 포함하다", "과거분사형", "포함된 / 주식회사의"],
        "quiz": [
            {"question": "The university __________ the local college into its system.", "translation": "그 대학교는 지역 대학을 자교 시스템으로 편입시켰다(통합시켰다). (힌트: 과거형)", "answer": "incorporated"},
            {"question": "He was hired by Microsoft __________.", "translation": "그는 마이크로소프트 주식회사에 고용되었다.", "answer": "Incorporated"}
        ]
    }
]

# JSON 파일 저장
json_path = os.path.expanduser("~/Desktop/MS_Dev.nosync/cts/vocab_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(vocab_list, f, ensure_ascii=False, indent=4)

print(f"Lesson 3 Vocab Data generation complete. Saved at {json_path}")
