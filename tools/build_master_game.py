#!/usr/bin/env python3
"""
tools/build_master_game.py
Divina Ludus — 4대 명작 마스터 게임 엔진 (서사·대화 완벽 복원 & 힌트 시스템 & 울트라 픽셀 컷씬)
- 단독 대사 탈피: 싱클레어와 크로머, 데미안, 피스토리우스, 에바 부인의 생생한 티키타카 문답 대화 복원
- 조작계 개편:
  * [*] 키 (또는 Q/ESC): 서재/메인 메뉴로 나가기 (0번에서 분리)
  * [0] 키: 현 상황의 문맥과 원작 철학을 짚어주는 [지혜의 힌트 / 사색 노트] 시스템 신설!
  * [1~5] 키: 선택지 및 다음 페이지 전용
- 울트라 픽셀 아트: 1막 놀부/흥부 수준으로 배경 디더링과 두 인물의 맞대면 구도 완벽 렌더링
"""

import os
import sys
import json
import gzip

sys.path.append("/home/krjoylee/code/game/tools")
from generate_hires_studio import (
    gen_hires_act1, gen_hires_act2, gen_hires_act3, gen_hires_act4,
    gen_hires_act5, gen_hires_act6, gen_hires_act7
)
from generate_all_packs_studio import PALETTE_16, compress_frame_rle
from make_ultra_peach_cutscenes import (
    gen_peach_act1_ultra, gen_peach_act2_ultra, gen_peach_act3_ultra,
    gen_peach_act4_ultra, gen_peach_act5_ultra, gen_peach_act6_ultra,
    gen_peach_act7_ultra
)
from make_ultra_dante_cutscenes import (
    gen_dante_act1_ultra, gen_dante_act2_ultra, gen_dante_act3_ultra,
    gen_dante_act4_ultra, gen_dante_act5_ultra, gen_dante_act6_ultra,
    gen_dante_act7_ultra
)
from make_ultra_demian_cutscenes import (
    gen_demian_act1_ultra, gen_demian_act2_ultra, gen_demian_act3_ultra,
    gen_demian_act4_ultra, gen_demian_act5_ultra, gen_demian_act6_ultra,
    gen_demian_act7_ultra
)
from make_ultra_james_dante_cutscenes import (
    gen_peach_act2_ultra, gen_dante_act3_ultra
)

def build_master_system():
    print("🎨 4대 명작 28개 씬 울트라 픽셀 컷씬 렌더링 및 RLE 압축 중...")
    
    # 1. 흥부놀부전
    heungbu_acts = [
        gen_hires_act1(), gen_hires_act2(), gen_hires_act3(), gen_hires_act4(),
        gen_hires_act5(), gen_hires_act6(), gen_hires_act7()
    ]
    act_rle_heungbu = [[compress_frame_rle(f) for f in a] for a in heungbu_acts]

    # 2. 제임스와 슈퍼 복숭아 (전 7막 울트라 픽셀 컷씬)
    peach_acts = [
        gen_peach_act1_ultra(), gen_peach_act2_ultra(), gen_peach_act3_ultra(),
        gen_peach_act4_ultra(), gen_peach_act5_ultra(), gen_peach_act6_ultra(),
        gen_peach_act7_ultra()
    ]
    act_rle_peach = [[compress_frame_rle(f) for f in a] for a in peach_acts]

    # 3. 단테의 신곡: 지옥편 (전 7막 울트라 픽셀 컷씬)
    dante_acts = [
        gen_dante_act1_ultra(), gen_dante_act2_ultra(), gen_dante_act3_ultra(),
        gen_dante_act4_ultra(), gen_dante_act5_ultra(), gen_dante_act6_ultra(),
        gen_dante_act7_ultra()
    ]
    act_rle_dante = [[compress_frame_rle(f) for f in a] for a in dante_acts]

    # 4. 데미안 (전 1~7막 울트라 픽셀 교체)
    demian_acts = [
        gen_demian_act1_ultra(), gen_demian_act2_ultra(), gen_demian_act3_ultra(),
        gen_demian_act4_ultra(), gen_demian_act5_ultra(), gen_demian_act6_ultra(),
        gen_demian_act7_ultra()
    ]
    act_rle_demian = [[compress_frame_rle(f) for f in a] for a in demian_acts]

    packs_data = [
        {
            "id": "heungbu",
            "title": "흥부놀부전",
            "tag": "Tutorial · 한국 고전",
            "metric_name": "선행의 씨앗",
            "metric_icon": "♧",
            "scenes": [
                {
                    "act": 1, "title": "형제의 갈림길", "speaker": "놀부와 흥부",
                    "text": "놀부: '네 이놈 흥부야! 내 집에 더는 쌀 한 톨 축낼 생각 마라! 처자식 데리고 썩 꺼지지 못할까!'\n흥부: '형님... 눈밭에 어린것들을 데리고 어디로 가란 말씀입니까... 제발 자비를 베풀어 주십시오...'",
                    "hint": "부모의 유훈과 혈육의 도리를 생각할 것인가, 부당한 핍박에 즉각 분노를 터뜨릴 것인가? 당장의 설움보다 더 큰 덕을 바라보십시오.",
                    "rle": act_rle_heungbu[0], "is_transition": False,
                    "choices": [
                        {"text": "부모님 말씀을 떠올리며 눈물을 삼키고 조용히 돌아선다", "delta": 1, "feedback": "흥부는 눈물을 삼키며 빈손으로 형의 집을 나섰습니다. 가슴은 미어졌으나 형을 원망하지 않았습니다."},
                        {"text": "억울함에 복받쳐 형에게 소리치며 맞서본다", "delta": -1, "feedback": "놀부가 몽둥이를 치켜들며 호통쳤습니다! '이놈이 어디서 감히 눈을 부라려?!'"}
                    ]
                },
                {
                    "act": 2, "title": "다친 제비", "speaker": "아내와 흥부",
                    "text": "아내: '여보! 저 처마 밑 제비 좀 보세요! 구렁이에 놀라 떨어져 다리가 부러졌어요! 피를 흘리며 가련하게 짹짹 울어요!'\n흥부: '쯧쯧, 미물이라도 어찌 목숨이 귀하지 않겠소. 당장 명주실과 부목을 가져오시오!'",
                    "hint": "스스로 먹을 양식조차 없는 극한의 가난 속에서도, 나보다 약한 작은 생명을 향해 손을 내미는 것이 진정한 자비입니다.",
                    "rle": act_rle_heungbu[1], "is_transition": False,
                    "choices": [
                        {"text": "하얀 부목을 대고 붉은 명주실로 정성껏 묶어 치료한다", "delta": 2, "feedback": "흥부는 떨리는 손으로 새끼 제비 다리에 부목을 대고 붉은 실로 감아주었습니다. 치유의 온기가 감돌았습니다."},
                        {"text": "우리 식구 먹을 것도 없는데... 못 본 척 돌아선다", "delta": -2, "feedback": "흥부는 한숨을 쉬며 발길을 돌렸습니다. 처마 밑엔 새끼 제비의 슬픈 울음소리만 흩어졌습니다."}
                    ]
                },
                {
                    "act": 3, "title": "박씨를 물고 온 제비", "speaker": "제비와 흥부",
                    "text": "제비: '(창공을 선회하며 흥부의 머리맡에 눈부신 황금 박씨를 툭 떨어뜨린다)'\n흥부: '아니! 작년에 다리를 고쳐 날아간 그 제비로구나! 입에 물고 온 이 씨앗은 무엇인고?'",
                    "hint": "은혜를 잊지 않는 미물의 마음에 감사하며, 대지의 품에 씨앗을 맡기십시오.",
                    "rle": act_rle_heungbu[2], "is_transition": True, "button_text": "박씨를 마당 양지바른 곳에 정성껏 심는다"
                },
                {
                    "act": 4, "title": "흥부의 대박 타기", "speaker": "흥부 내외",
                    "text": "흥부: '여보, 지붕 위 보름달만 한 대박을 탑시다! 슬근슬근 톱질하세!'\n아내: '엉차, 엉차! 박이 타지면 속이라도 끓여 굶주린 아이들 배를 채웁시다!'",
                    "hint": "뜻밖의 거대한 행운과 재물이 쏟아질 때, 참된 군자는 독점하지 않고 궁핍한 이웃을 돌아봅니다.",
                    "rle": act_rle_heungbu[3], "is_transition": False,
                    "choices": [
                        {"text": "쏟아지는 금은보화와 쌀을 가난한 이웃들에게 고루 나눈다", "delta": 2, "feedback": "박이 쩍 갈라지며 번쩍이는 엽전과 쌀이 폭포수처럼 쏟아졌습니다! 흥부는 온 마을에 양식을 베풀었습니다."},
                        {"text": "다시 가난해질까 두려워 곳간 깊숙이 금괴를 숨겨둔다", "delta": 0, "feedback": "산더미 같은 재물을 얻었으나, 흥부는 문을 걸어 잠그고 가슴을 졸였습니다."}
                    ]
                },
                {
                    "act": 5, "title": "놀부의 탐욕", "speaker": "놀부와 제비",
                    "text": "놀부: '멀쩡한 제비 다리를 뚝 분질러서 나도 벼락부자가 될 테다!'\n제비: '(처절하게 비명을 지르며 공포에 질려 퍼덕인다)'",
                    "hint": "남의 복을 시기하여 억지로 흉내 내는 악행은 스스로를 파멸의 구렁텅이로 몰아넣습니다.",
                    "rle": act_rle_heungbu[4], "is_transition": True, "button_text": "인과응보의 시간이 다가옵니다"
                },
                {
                    "act": 6, "title": "도깨비의 응징", "speaker": "도깨비와 놀부",
                    "text": "도깨비: '놀부야! 죄 없는 생명을 해치고 탐욕을 부린 죗값을 받아라! 쇠몽둥이 맛을 보아라!'\n놀부: '으악! 사람 살려! 내 돈, 내 패물 다 가져가고 제발 목숨만 살려주시오!'",
                    "hint": "파멸을 겪고 알거지가 된 자에게 남은 유일한 길은 진실한 참회뿐입니다.",
                    "rle": act_rle_heungbu[5], "is_transition": True, "button_text": "알거지가 되어 길바닥에 쫓겨난 놀부"
                },
                {
                    "act": 7, "title": "눈물의 화해", "speaker": "놀부와 흥부",
                    "text": "놀부: '흥부야... 내가 천하의 몹쓸 놈이다... 네 복을 시기하다 패가망신했구나... 나를 패 죽여다오...'\n흥부: '형님! 어찌 그런 말씀을 하십니까! 우리는 한 부모의 피를 나눈 형제입니다. 제 집으로 가시지요!'",
                    "hint": "진정한 용서는 원수를 굴복시키는 것이 아니라, 무조건적인 사랑으로 품어 상처를 치유하는 것입니다.",
                    "rle": act_rle_heungbu[6], "is_transition": False,
                    "choices": [
                        {"text": "엎드린 형을 부둥켜안고 눈물을 흘리며 지난 원망을 씻어낸다", "delta": 3, "feedback": "흥부는 형을 품에 안고 통곡했습니다. 두 형제의 눈물이 얼어붙은 땅을 녹이고 봄풀을 틔웠습니다."},
                        {"text": "거처와 양식은 내주되, 다시는 욕심부리지 말라 엄히 타이른다", "delta": 1, "feedback": "놀부는 고개를 숙이고 지난날의 악행을 뼈저리게 뉘우쳤습니다."}
                    ]
                }
            ],
            "endings": [
                {"min": 8, "title": "성인군자의 반열 (최고 선행)", "desc": "지극한 자비와 형제애로 가난과 멸시를 이겨내고 온 나라에 덕망을 떨친 성인의 반열에 올랐습니다."},
                {"min": 5, "title": "의좋은 형제 (정석 해피엔딩)", "desc": "미물을 아끼고 혈육의 정을 되살려, 부귀영화와 화목한 가정을 모두 지켜냈습니다."},
                {"min": -99, "title": "깨달음의 길 (고난 극복)", "desc": "가혹한 시련을 거쳐 물질보다 소중한 양심과 진정한 형제애의 가치를 깨달았습니다."}
            ]
        },
        {
            "id": "demian",
            "title": "데미안",
            "tag": "Hermann Hesse · 자아 실현",
            "metric_name": "내면의 각성",
            "metric_icon": "☥",
            "scenes": [
                {
                    "act": 1, "title": "두 개의 세계와 크로머", "speaker": "크로머와 싱클레어",
                    "text": "크로머: '사과를 훔쳤다고 으스대더니 겁쟁이 녀석! 내일까지 2마르크를 가져오지 않으면 네 아비와 경찰에 다 까발릴 테다, 알겠냐?'\n싱클레어: '프란츠, 제발... 우리 집엔 그런 큰돈이 없어... 한 번만 용서해 줘...'",
                    "hint": "밝고 따스한 부모님의 세계 뒤편에 도사린 어둠의 세계. 거짓말로 시작된 굴레를 어떻게 끊어낼 것인가? 두려움에 굴복할수록 악마의 손아귀는 깊어집니다.",
                    "rle": act_rle_demian[0], "is_transition": False,
                    "choices": [
                        {"text": "양심의 가책을 느끼며 더 이상 거짓과 협박에 휘둘리지 않기로 결심한다", "delta": 2, "feedback": "싱클레어는 떨리는 가슴을 쥐며 어둠의 굴레에서 벗어나려 몸부림쳤습니다. 영혼의 눈이 떠지기 시작했습니다."},
                        {"text": "공포에 질려 부모님의 서랍에서 돈을 훔쳐 갖다주려 한다", "delta": -2, "feedback": "크로머의 잔인한 휘파람 소리가 귓가에 맴돌며, 싱클레어는 죄악의 심연으로 끌려 들어갔습니다."}
                    ]
                },
                {
                    "act": 2, "title": "막스 데미안과 카인의 표식", "speaker": "데미안과 싱클레어",
                    "text": "데미안: '싱클레어, 카인은 비열한 살인자가 아니야. 그는 남들이 감히 갖지 못한 비범한 정신과 용기를 지녔기에 특별한 표식을 갖게 된 거란다.'\n싱클레어: '하지만 성경에는... 하나님이 그를 저주하셨다고 쓰여 있잖아?'\n데미안: '대부분의 사람들은 스스로 생각하기를 두려워하거든. 너는 어때?'",
                    "hint": "남들이 정해준 맹목적인 도덕과 교리를 넘어서, 내면의 독립적인 이성으로 세상을 직시하는 자만이 '카인의 표식'을 지닙니다.",
                    "rle": act_rle_demian[1], "is_transition": False,
                    "choices": [
                        {"text": "그의 대담하고 신비로운 통찰에 깊이 공명하며 귀를 기울인다", "delta": 2, "feedback": "데미안의 이마에서 은은한 황금빛 후광이 번지며, 싱클레어는 기존 세계의 껍질이 금 가는 것을 느꼈습니다."},
                        {"text": "기존 교회의 가르침과 다르다며 두려워 귀를 닫으려 한다", "delta": -1, "feedback": "데미안은 서글프고도 그윽한 눈빛으로 싱클레어를 바라보며 조용히 침묵했습니다."}
                    ]
                },
                {
                    "act": 3, "title": "베아트리체 초상화", "speaker": "싱클레어의 독백",
                    "text": "싱클레어: '이젤 앞에 홀린 듯 붓을 놀려 그린 이 얼굴... 거리에서 마주친 소녀 베아트리체인 줄 알았으나, 데미안의 얼굴이며, 동시에 내 영혼 깊은 곳의 참된 나 자신의 얼굴이로구나!'",
                    "hint": "외부의 대상을 향한 동경은 결국 자기 내면의 신성을 발견하기 위한 거울에 불과합니다.",
                    "rle": act_rle_demian[2], "is_transition": True, "button_text": "초상화에 불을 붙여 태우며 데미안에게 영혼의 전언을 띄운다"
                },
                {
                    "act": 4, "title": "알을 깨는 매의 비상", "speaker": "아브락사스와 싱클레어",
                    "text": "데미안의 편지: '새는 알에서 나오려고 투쟁한다. 알은 세계다. 태어나려는 자는 하나의 세계를 깨뜨려야 한다. 신의 이름은 아브락사스다.'\n싱클레어: '아브락사스... 신적이면서 동시에 악마적인, 빛과 어둠을 모두 품은 절대자여!'",
                    "hint": "선(善)만을 강요하는 반쪽짜리 세계를 부수지 않고서는 온전한 인간으로 다시 태어날 수 없습니다.",
                    "rle": act_rle_demian[3], "is_transition": False,
                    "choices": [
                        {"text": "기존의 세계를 과감히 부수고 참된 자아를 향해 날아오른다", "delta": 3, "feedback": "황금빛 매가 껍질을 박차고 솟구쳐 창공을 향해 포효했습니다! 영혼의 비상이 시작되었습니다."},
                        {"text": "안온하고 익숙했던 유년의 보호막 속에 머물며 망설인다", "delta": -2, "feedback": "내면의 알껍데기가 삐걱거리며 성장통의 지독한 어둠이 엄습했습니다."}
                    ]
                },
                {
                    "act": 5, "title": "피스토리우스와 불꽃", "speaker": "피스토리우스와 싱클레어",
                    "text": "피스토리우스: '(오르간 건반에서 손을 떼며) 싱클레어, 타오르는 불꽃 속을 응시하게. 그대가 꿈꾸는 모든 신비는 외부가 아닌 그대 가슴속에 이미 살아있네!'\n싱클레어: '선생님, 하지만 홀로 서는 것은 너무나 두렵고 고독합니다...'\n피스토리우스: '고독이야말로 자연이 인간을 성숙시키는 유일한 도가니라네.'",
                    "hint": "스승의 가르침조차 딛고 넘어서야 비로소 온전한 홀로서기가 완성됩니다.",
                    "rle": act_rle_demian[4], "is_transition": True, "button_text": "불꽃 속에서 내면의 불멸하는 소리에 귀를 기울인다"
                },
                {
                    "act": 6, "title": "에바 부인의 품", "speaker": "에바 부인과 싱클레어",
                    "text": "에바 부인: '싱클레어, 그대는 먼 길을 돌아 마침내 나를 찾아왔군요. 사랑은 애원하는 것이 아니라, 스스로의 내부에서 확신에 차오르는 것이랍니다.'\n싱클레어: '어머니... 당신은 제 모든 꿈의 종착역이자 운명입니다.'",
                    "hint": "모성적인 대지이자 영혼의 고향. 참된 사랑은 구걸하는 것이 아니라 확신으로 이끄는 힘입니다.",
                    "rle": act_rle_demian[5], "is_transition": True, "button_text": "대모신의 자애로운 손길을 느끼며 참 자아를 각성한다"
                },
                {
                    "act": 7, "title": "마지막 키스와 거울 속 자아", "speaker": "데미안과 싱클레어",
                    "text": "데미안: '(야전병원 침대에서 희미하게 미소 지으며) 어린 싱클레어... 이제 내가 없더라도 네 안의 소리에 귀를 기울여 봐. 언젠가 네가 나를 부를 때... 거울을 보면 내 모습이 바로 너 자신 안에 보일 거야.'\n싱클레어: '(데미안의 이마에 입맞춤을 받고 조용히 거울을 마주한다)'",
                    "hint": "스승과 친구는 떠나갔으나, 그가 일깨운 빛은 영원히 내 영혼의 일부가 되었습니다.",
                    "rle": act_rle_demian[6], "is_transition": False,
                    "choices": [
                        {"text": "거울 속에 비친 완전히 성숙해진 나 자신을 직시하며 미소 짓는다", "delta": 3, "feedback": "거울 속에 비친 싱클레어의 눈동자는 완전히 데미안과 하나가 되어 있었습니다. 순례는 완성되었습니다."},
                        {"text": "떠나간 친구의 빈자리를 슬퍼하며 뜨거운 눈물로 작별을 고한다", "delta": 1, "feedback": "데미안의 키스는 지워지지 않는 영원한 표식이 되어 싱클레어의 가슴에 아로새겨졌습니다."}
                    ]
                }
            ],
            "endings": [
                {"min": 8, "title": "아브락사스에 도달한 자", "desc": "빛과 어둠의 세계를 모두 통합하고, 알을 깨고 나와 온전한 참 자아를 실현했습니다."},
                {"min": 5, "title": "표식을 지닌 자 (카인의 후예)", "desc": "세상의 규율에 굴복하지 않고 내면의 부름을 따르는 고결한 영혼의 소유자가 되었습니다."},
                {"min": -99, "title": "알을 깨는 순례자", "desc": "수많은 방황과 고통 끝에 마침내 스스로의 삶을 대면할 용기를 얻었습니다."}
            ]
        },
        {
            "id": "peach",
            "title": "제임스와 슈퍼 복숭아",
            "tag": "Roald Dahl · 환상 모험",
            "metric_name": "경이와 용기",
            "metric_icon": "✦",
            "scenes": [
                {
                    "act": 1, "title": "스폰지와 스파이커 이모", "speaker": "이모들과 제임스",
                    "text": "스파이커: '게으른 녀석! 장작을 더 패지 못해?! 지팡이로 뼈마디를 두들겨 맞아야 정신을 차릴 테냐!'\n스폰지: '오호호, 밥도 주지 마 얘! 굶겨 죽여야 고분고분해지지!'\n제임스: '이모, 하루 종일 물 한 모금 못 마셨어요... 숨이 턱턱 막혀요...'",
                    "hint": "가혹한 학대와 억압 속에서도 영혼의 순수함과 자유를 향한 불씨를 결코 꺼뜨리지 마십시오.",
                    "rle": act_rle_peach[0], "is_transition": False,
                    "choices": [
                        {"text": "입술을 깨물며 묵묵히 도끼를 쥐고 자유의 날을 기다린다", "delta": 1, "feedback": "제임스는 눈물을 삼키며 장작을 팼습니다. 언젠가 푸른 바다 너머로 탈출하겠다는 꿈을 품었습니다."},
                        {"text": "억울함에 복받쳐 이모들에게 반항의 눈빛을 쏘아본다", "delta": -1, "feedback": "스파이커 이모가 앙상한 손으로 지팡이를 내리쳤습니다! '이놈이 어디서 눈을 똑바로 떠?!'"}
                    ]
                },
                {
                    "act": 2, "title": "마법의 초록 악어 혀", "speaker": "신비로운 노인과 제임스",
                    "text": "노인: '얘야, 이 봉투를 받거라. 이 안에는 수천 마리 악어의 혀로 빚어낸 거대한 마법이 꿈틀대고 있단다. 절대 흘리지 마라!'\n제임스: '할아버지, 봉투 안에서 빛이 뿜어져 나와요! 손가락 끝이 찌릿찌릿해요!'\n노인: '이 씨앗이 닿는 곳마다 세상에서 가장 경이로운 일이 일어날 게다!'",
                    "hint": "미지의 기적을 마주했을 때 의심과 두려움 대신, 순수한 호기심과 용기로 두 손을 내미십시오.",
                    "rle": act_rle_peach[1], "is_transition": False,
                    "choices": [
                        {"text": "소중히 품에 안고 마른 복숭아나무 뿌리를 향해 전력으로 달린다", "delta": 2, "feedback": "초록빛 발광체들이 나무뿌리로 스며들자, 말라죽었던 복숭아나무가 쿵쿵 심장처럼 고동치기 시작했습니다!"},
                        {"text": "의심하며 노인에게 무슨 속셈인지 캐묻는다", "delta": 0, "feedback": "노인은 기괴한 미소를 지으며 순식간에 안갯속으로 사라져 버렸습니다."}
                    ]
                },
                {
                    "act": 3, "title": "거대 복숭아의 탄생", "speaker": "마을 사람들과 제임스",
                    "text": "마을 사람들: '저게 뭐야?! 복숭아가 집채만 하게 부풀어 오르고 있어! 심장처럼 쿵-쿵 박동하잖아!'\n스파이커 이모: '입장료를 받아야 해! 사람당 1실링씩 내고 구경해라!'\n제임스: '달콤한 복숭아 향기가 온 언덕을 뒤덮고 있어요... 복숭아 옆구리에 기어 들어갈 구멍이 보여요!'",
                    "hint": "탐욕스러운 어른들의 소란을 피해, 미지의 세계로 통하는 비밀스러운 입구로 뛰어드십시오.",
                    "rle": act_rle_peach[2], "is_transition": True, "button_text": "박동하는 복숭아의 달콤한 과육 터널 속으로 기어 들어간다"
                },
                {
                    "act": 4, "title": "거대 곤충 친구들", "speaker": "메뚜기, 무당벌레, 제임스",
                    "text": "메뚜기 신사: '어서 오십시오, 어린 신사여! 두려워 마세요. 우리는 당신을 기다려 온 복숭아의 친구들이랍니다!'\n지네: '어이 꼬마! 구두끈 묶는 것 좀 도와줘! 내 발이 마흔두 개나 되거든!'\n무당벌레 숙녀: '아가, 이모들에게 괴롭힘당하느라 뺨이 핼쑥하구나. 이리 오렴!'\n제임스: '거대 벌레들이 말을 하다니... 하지만 이모들보다 수천 배는 다정해요!'",
                    "hint": "겉모습의 기괴함 너머에 있는 진실한 영혼을 꿰뚫어 보고, 따스한 벗들과 연대하십시오.",
                    "rle": act_rle_peach[3], "is_transition": False,
                    "choices": [
                        {"text": "두려움을 떨치고 정중히 메뚜기 신사와 친구들에게 악수를 청한다", "delta": 2, "feedback": "곤충 친구들이 환호하며 제임스를 둘러싸고 따스하게 반겨주었습니다. 제임스는 평생 처음으로 가족의 온기를 느꼈습니다."},
                        {"text": "거대한 벌레들의 꿈틀거림에 비명을 지르며 벽으로 물러선다", "delta": -1, "feedback": "지네가 서운한 표정으로 수십 개의 다리를 긁적였습니다. '우릴 무서워하다니 섭섭한걸...?'"}
                    ]
                },
                {
                    "act": 5, "title": "대서양으로의 출항", "speaker": "지네와 제임스",
                    "text": "지네: '꼭지를 끊었다! 굴러간다, 굴러가!! 언덕을 박차고 절벽을 넘는다!'\n제임스: '풍덩!! 바다다! 푸른 대서양 바다 위에 복숭아가 배처럼 둥실 떠올랐어요!'\n무당벌레 숙녀: '우리가 이모들의 학대에서 벗어나 마침내 자유의 바다로 나왔어!'",
                    "hint": "익숙했던 학대의 땅을 떠나 거친 망망대해로 나아가는 것은 위대한 자유의 시작입니다.",
                    "rle": act_rle_peach[4], "is_transition": True, "button_text": "상어 떼의 습격에 맞서 갈매기 낚아챌 실크 거미줄을 준비한다"
                },
                {
                    "act": 6, "title": "500마리 갈매기 비행", "speaker": "제임스와 친구들",
                    "text": "제임스: '거미 누나, 누에 아저씨, 실을 더 빨리 뽑아주세요! 지네 아저씨, 갈매기 목에 올가미를 거세요!'\n지네: '잡았다! 갈매기들이 날개를 퍼덕인다! 복숭아가 뜬다, 하늘로!!'\n메뚜기 신사: '놀랍군요, 제임스! 상어들의 주둥이를 벗어나 구름 위를 날고 있어요!'",
                    "hint": "지혜와 협동심이야말로 절체절명의 위기를 극복하고 창공으로 날아오르는 가장 강인한 날개입니다.",
                    "rle": act_rle_peach[5], "is_transition": False,
                    "choices": [
                        {"text": "지혜를 발휘해 500마리 갈매기 편대를 일사불란하게 지휘한다", "delta": 2, "feedback": "흰 갈매기들이 거대한 날갯짓으로 복숭아를 성층권까지 들어 올렸습니다! 눈부신 태양광이 쏟아져 내렸습니다."},
                        {"text": "상어 떼의 이빨과 거센 바람에 겁에 질려 눈을 감아버린다", "delta": -1, "feedback": "친구들의 격려 속에 제임스는 떨리는 손으로 가까스로 중심을 잡았습니다."}
                    ]
                },
                {
                    "act": 7, "title": "엠파이어 빌딩 착륙", "speaker": "뉴욕 시장과 제임스",
                    "text": "뉴욕 시민들: '하늘을 봐! 거대한 복숭아가 엠파이어 스테이트 빌딩 첨탑에 사뿐히 내려앉았어! 만세!!'\n뉴욕 시장: '용감한 소년이여, 그대와 신비로운 벗들을 뉴욕에 환영하오!'\n제임스: '달콤한 복숭아 살을 온 도시의 배고픈 아이들에게 전부 나누어 줄게요!'",
                    "hint": "고난 끝에 얻은 경이로운 풍요를 세상의 가난하고 소외된 이웃들과 나눌 때 삶은 완성됩니다.",
                    "rle": act_rle_peach[6], "is_transition": False,
                    "choices": [
                        {"text": "달콤한 슈퍼 복숭아를 뉴욕의 모든 가난한 아이들에게 선물한다", "delta": 3, "feedback": "수만 명의 아이들이 환호하며 달콤한 복숭아를 나누어 먹었습니다! 제임스는 센트럴파크 복숭아 씨앗 궁전에서 영원히 행복했습니다."},
                        {"text": "복숭아를 영구 보존하며 박물관을 세우고 친구들과 안식처를 꾸린다", "delta": 1, "feedback": "제임스와 곤충 친구들은 평생 가장 진실한 우정을 나누며 평화롭게 살았습니다."}
                    ]
                }
            ],
            "endings": [
                {"min": 8, "title": "경이의 위대한 선장", "desc": "가혹한 학대를 지혜와 용기로 이겨내고, 대서양을 건너 세상 모든 아이들에게 꿈을 선물했습니다."},
                {"min": 5, "title": "용감한 하늘의 비행사", "desc": "친구들과 힘을 합쳐 상어와 절망을 이겨내고 뉴욕에 새로운 보금자리를 개척했습니다."},
                {"min": -99, "title": "자유를 찾은 영혼", "desc": "어두운 언덕을 탈출하여 마침내 스스로의 삶을 살아갈 용기를 얻었습니다."}
            ]
        },
        {
            "id": "dante",
            "title": "단테의 신곡: 지옥편",
            "tag": "Dante · 대서사시",
            "metric_name": "이성과 영혼의 빛",
            "metric_icon": "☩",
            "scenes": [
                {
                    "act": 1, "title": "어두운 숲과 베르길리우스", "speaker": "베르길리우스와 단테",
                    "text": "단테: '길을 잃었습니다, 스승이여... 표범과 사자와 늑대가 길을 가로막고 으르렁거립니다...'\n베르길리우스: '방황하는 시인이여, 두려워 마라. 내가 그대를 지옥의 심연을 지나 천국으로 인도하리라.'",
                    "hint": "삶의 반환점에서 길을 잃었을 때, 참된 이성과 지혜의 목소리에 영혼을 맡기십시오.",
                    "rle": act_rle_dante[0], "is_transition": False,
                    "choices": [
                        {"text": "스승의 손을 잡고 지옥의 문으로 굳건히 발을 딛는다", "delta": 2, "feedback": "스승의 월계관이 어두운 숲속에서 성스러운 빛을 뿜어냈습니다. 단테의 발걸음에 힘이 실렸습니다."},
                        {"text": "세 마리 맹수의 포효에 뒷걸음질 치며 주저앉는다", "delta": -1, "feedback": "베르길리우스가 지팡이를 들어 맹수들을 쫓아내며 타이르고 이끌었습니다."}
                    ]
                },
                {
                    "act": 2, "title": "지옥의 문과 뱃사공 카론", "speaker": "카론과 베르길리우스",
                    "text": "카론: '이곳에 들어오는 자, 모든 희망을 버려라! 살아있는 자여, 썩 물러가라! 아케론 강 건너 영원한 암흑 속으로 떠날지니!'\n베르길리우스: '카론이여, 분노를 거두라. 이것은 하늘에서 뜻하신 바니 더 이상 묻지 말라!'",
                    "hint": "공포와 절망 앞에서도 하늘의 뜻과 이성의 인도하심을 믿으십시오.",
                    "rle": act_rle_dante[1], "is_transition": False,
                    "choices": [
                        {"text": "스승의 가르침을 믿고 당당히 핏빛 나룻배에 오른다", "delta": 2, "feedback": "거구의 카론도 위엄 있는 스승의 일갈에 뱃머리를 돌려 두 시인을 태웠습니다."},
                        {"text": "망령들의 비명 소리에 공포에 질려 기절하고 만다", "delta": -2, "feedback": "단테는 핏빛 강물 앞에서 전율하며 정신을 잃고 말았습니다."}
                    ]
                },
                {
                    "act": 3, "title": "제2옥: 애욕의 암흑 폭풍", "speaker": "프란체스카와 단테",
                    "text": "프란체스카: '오 자비로운 시인이여, 책을 읽다 사랑에 빠져 비극을 맞이한 우리를 가엾게 여겨 주소서... 영원한 암흑 폭풍 속에서도 우리는 서로를 놓지 못합니다...'\n단테: '오 프란체스카여, 그대의 고통에 가슴이 찢어지는 듯하오...'",
                    "hint": "인간적인 연민과 신의 엄정한 정의 사이에서 영혼의 고뇌를 통찰하십시오.",
                    "rle": act_rle_dante[2], "is_transition": False,
                    "choices": [
                        {"text": "두 연인의 애달픈 비극에 깊이 탄식하며 눈물을 흘린다", "delta": 2, "feedback": "단테는 지극한 연민과 슬픔으로 가슴이 찢어지며 바닥에 엎드렸습니다. 참된 자비가 싹텄습니다."},
                        {"text": "죄는 죗값일 뿐이라며 냉정하게 고개를 돌린다", "delta": -1, "feedback": "베르길리우스가 침묵 속에서 단테의 차가운 눈빛을 응시했습니다."}
                    ]
                },
                {
                    "act": 4, "title": "제6옥: 불타는 석관의 파리나타", "speaker": "파리나타와 단테",
                    "text": "파리나타: '그대 피렌체의 말을 쓰는 나그네여! 지옥의 화염이 내 몸을 태울지라도, 내 조국 피렌체의 운명은 어떻게 되었는가!'\n단테: '조국을 향한 그대의 오만과 기개는 지옥불 속에서도 꺾이지 않는구려.'",
                    "hint": "지옥의 형벌 속에서도 굴복하지 않는 인간 정신의 거대한 기개.",
                    "rle": act_rle_dante[3], "is_transition": True, "button_text": "오만한 귀족의 숭고한 기개에 경의를 표한다"
                },
                {
                    "act": 5, "title": "제7옥: 끓는 피의 강 플레게톤", "speaker": "해설",
                    "text": "이웃을 해친 폭군들이 펄펄 끓는 핏빛 강물 속에서 울부짖고, 강둑에서는 반인반마 켄타우로스들이 활시위를 팽팽히 당기고 있습니다!",
                    "hint": "타인에게 가한 폭력은 반드시 피의 강물이 되어 돌아옵니다.",
                    "rle": act_rle_dante[4], "is_transition": True, "button_text": "침착하게 네소스의 등에 올라 피의 강을 건넌다"
                },
                {
                    "act": 6, "title": "제8옥: 말레볼제의 구덩이", "speaker": "해설",
                    "text": "거대한 지옥 뱀들이 도둑들의 몸을 칭칭 감고 물어뜯습니다. 물린 육신이 재로 타들어 갔다가 다시 인간으로 부활하는 지독한 고통이 끝없이 반복됩니다!",
                    "hint": "죄악의 실체를 피하지 않고 직시하는 것만이 정화의 첫걸음입니다.",
                    "rle": act_rle_dante[5], "is_transition": True, "button_text": "죄악의 끔찍한 실체를 직시하며 심연으로 내려간다"
                },
                {
                    "act": 7, "title": "얼음 지옥 탈출과 별들의 찬가", "speaker": "단테와 베르길리우스",
                    "text": "단테: '스승이여! 거대한 얼음 호수 코키토스를 지나 마침내 지옥의 구멍을 빠져나왔습니다!'\n베르길리우스: '보라, 단테여. 머리 위로 밤하늘의 찬란한 별들이 쏟아져 내리는구나!'",
                    "hint": "심연의 어둠을 통과한 자만이 밤하늘의 진정한 별빛을 우러러볼 수 있습니다.",
                    "rle": act_rle_dante[6], "is_transition": False,
                    "choices": [
                        {"text": "'그리고 우리는 밖으로 나와 다시 별들을 보았다' 구원의 찬가를 부른다", "delta": 3, "feedback": "칠흑 같은 어둠을 뚫고 나온 단테의 눈에 눈부신 은하수가 가득 차올랐습니다!"},
                        {"text": "지옥의 끔찍한 고통을 잊지 않겠다 다짐하며 무릎 꿇는다", "delta": 1, "feedback": "베르길리우스가 단테의 어깨를 짚으며 자애롭게 미소 지었습니다."}
                    ]
                }
            ],
            "endings": [
                {"min": 8, "title": "신성한 구원의 대시인", "desc": "지옥의 모든 죄악과 고통을 이성과 연민으로 통찰하고, 별들이 빛나는 구원의 길로 나아갔습니다."},
                {"min": 5, "title": "깨어난 순례자", "desc": "공포와 절망을 극복하고 스승의 인도를 따라 지옥의 심연을 무사히 통과했습니다."},
                {"min": -99, "title": "심연을 목격한 자", "desc": "지옥의 끔찍한 형벌을 뼈에 새기며 지상에서의 새로운 삶을 성찰했습니다."}
            ]
        }
    ]

    palette_hex = [f"#{c[2][0]:02x}{c[2][1]:02x}{c[2][2]:02x}" for c in PALETTE_16]
    master_payload = {
        "palette": palette_hex,
        "packs": packs_data
    }

    json_str = json.dumps(master_payload)
    
    html_engine = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Divina Ludus — Literature Master Console</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; }}
  html, body {{
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #0d0d0d;
    color: #e0e0e0;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  .console-frame {{
    width: 860px;
    height: 730px;
    background: #181818;
    border: 3px solid #383838;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.95);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .console-header {{
    background: #222222;
    padding: 8px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #2e2e2e;
  }}
  .console-title {{ font-size: 15px; font-weight: bold; color: #ffcc99; }}
  .console-hud {{ font-size: 13px; color: #81d4fa; font-family: monospace; }}
  
  .canvas-container {{
    background: #000000;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 6px;
    border-bottom: 2px solid #282828;
  }}
  canvas {{
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    width: 640px;
    height: 328px;
    background: #151515;
    border: 2px solid #333333;
    box-shadow: 0 4px 15px rgba(0,0,0,0.8);
  }}
  
  .bottom-panel {{
    flex: 1;
    display: flex;
    padding: 10px 18px;
    gap: 14px;
    background: #141414;
  }}
  .dialogue-box {{
    flex: 65;
    background: #1e1e1e;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .speaker {{
    font-size: 15px;
    font-weight: bold;
    color: #f4d03f;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .speaker::before {{ content: "◈"; color: #e74c3c; }}
  .dialogue-text {{
    font-size: 14px;
    line-height: 1.55;
    color: #ffffff;
    word-break: keep-all;
    white-space: pre-line;
    min-height: 44px;
  }}
  
  .system-box {{
    flex: 35;
    background: #1e1e1e;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .metric-label {{
    font-size: 13px;
    color: #bbb;
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-weight: bold;
  }}
  .metric-track {{
    height: 10px;
    background: #2c2c2c;
    border-radius: 5px;
    overflow: hidden;
    border: 1px solid #404040;
  }}
  .metric-fill {{
    height: 100%;
    width: 30%;
    background: linear-gradient(90deg, #27ae60, #2ecc71);
    transition: width 0.35s ease;
  }}
  
  .choice-container {{
    padding: 0 18px 10px 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    background: #141414;
  }}
  .choice-btn {{
    background: #22313f;
    color: #f0f3f4;
    border: 1px solid #2c3e50;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    transition: all 0.15s;
  }}
  .choice-btn:hover {{
    background: #2c3e50;
    border-color: #f39c12;
    color: #f1c40f;
    transform: translateX(4px);
  }}

  /* 힌트 모달 / 박스 */
  .hint-box {{
    background: #2a2415;
    border: 1px solid #d4ac0d;
    color: #f9e79f;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 12.5px;
    line-height: 1.4;
    margin-top: 6px;
    display: none;
  }}
</style>
</head>
<body>

<div class="console-frame">
  <div class="console-header">
    <div class="console-title" id="headerTitle">◆ Divina Ludus · 고전문학 서재 ◆</div>
    <div class="console-hud" id="hudText">[Ultra 296x152 Engine]</div>
  </div>

  <div class="canvas-container">
    <canvas id="retroCanvas" width="296" height="152"></canvas>
  </div>

  <div class="bottom-panel">
    <div class="dialogue-box">
      <div>
        <div class="speaker" id="speakerName">사서</div>
        <div class="dialogue-text" id="dialogueText">환영합니다, 순례자여. 서재의 책을 펼쳐 여정을 시작하십시오.</div>
        <div class="hint-box" id="hintBox"></div>
      </div>
      <div style="font-size: 12px; color: #888;" id="feedbackText">키보드 [1], [2] 키를 눌러 선택할 수 있습니다.</div>
    </div>
    <div class="system-box">
      <div>
        <div class="metric-label">
          <span id="metricName">♧ 선행의 씨앗</span>
          <span id="metricVal">3 / 10</span>
        </div>
        <div class="metric-track">
          <div class="metric-fill" id="metricBar" style="width: 30%;"></div>
        </div>
      </div>
      <div style="font-size: 11.5px; color: #888; line-height: 1.45;" id="sysInfo">
        ◈ [1~5]: 선택 / 다음페이지<br>
        ◈ [0]: 💡 지혜의 사색 힌트<br>
        ◈ [* / Q / ESC]: 서재 나가기
      </div>
    </div>
  </div>

  <div class="choice-container" id="choiceBox"></div>
</div>

<script>
  const masterData = {json_str};
  const canvas = document.getElementById('retroCanvas');
  const ctx = canvas.getContext('2d');
  
  // Game States: 'TITLE' | 'LIBRARY' | 'IN_GAME' | 'ENDING'
  let gameState = 'TITLE';
  let curPack = null;
  let curSceneIdx = 0;
  let curFrame = 0;
  let metricValue = 3;
  let hintVisible = false;
  
  // 서재 페이지네이션 (1페이지당 최대 3작품, 5번은 다음 페이지)
  let libraryPage = 0;
  const ITEMS_PER_PAGE = 3;

  function showTitleScreen() {{
    gameState = 'TITLE';
    curPack = null;
    hideHint();
    document.getElementById('headerTitle').innerText = "◆ Divina Ludus · 고전문학 서재 ◆";
    document.getElementById('speakerName').innerText = "안내 사서";
    document.getElementById('dialogueText').innerText = "환영합니다, 순례자여.\\n[1]번을 눌러 조작법을 익히는 '기본 튜토리얼'을 시작하거나,\\n[2]번을 눌러 '정식 문학 서재'로 입장하십시오.";
    document.getElementById('feedbackText').innerText = "키보드 [1] 또는 [2] 키를 누르세요.";
    document.getElementById('metricName').innerText = "◈ 모드 안내";
    document.getElementById('metricVal').innerText = "준비 완료";
    document.getElementById('metricBar').style.width = "100%";
    document.getElementById('sysInfo').innerHTML = "◈ [1] 기본 튜토리얼<br>◈ [2] 정식 문학 서재<br>◈ 1MB 무설치 단일 엔진";

    const box = document.getElementById('choiceBox');
    box.innerHTML = `
      <button class="choice-btn" onclick="startTutorial()">[1] 기본 튜토리얼 시작: 《흥부놀부전》 (초심자 추천)</button>
      <button class="choice-btn" onclick="showLibraryScreen(0)">[2] 정식 문학 서재 입장 (제임스 복숭아, 단테 지옥편, 데미안)</button>
    `;
    
    renderStaticFrame(masterData.packs[0].scenes[0].rle[0]);
  }}

  function showLibraryScreen(page = 0) {{
    gameState = 'LIBRARY';
    libraryPage = page;
    hideHint();
    
    const literaturePacks = masterData.packs.slice(1);
    const totalPages = Math.ceil(literaturePacks.length / ITEMS_PER_PAGE);
    const startIdx = libraryPage * ITEMS_PER_PAGE;
    const pageItems = literaturePacks.slice(startIdx, startIdx + ITEMS_PER_PAGE);

    document.getElementById('headerTitle').innerText = `◆ 정식 문학 서재 (Page ${{libraryPage + 1}} / ${{totalPages}}) ◆`;
    document.getElementById('speakerName').innerText = "서재의 문지기";
    document.getElementById('dialogueText').innerText = "어떤 영혼의 여정을 탐험하시겠습니까?\\n플레이하고자 하는 명작의 번호[1~3]를 선택하십시오. [*] 키로 메인 타이틀로 돌아갑니다.";
    document.getElementById('feedbackText').innerText = "키보드 숫자키 [1~3], [5] 다음페이지, [*] 타이틀";

    let buttonsHtml = '';
    pageItems.forEach((pack, i) => {{
      buttonsHtml += `<button class="choice-btn" onclick="loadPackById('${{pack.id}}')">[${{i + 1}}] ${{pack.title}} (${{pack.tag}} · ${{pack.metric_icon}} ${{pack.metric_name}})</button>`;
    }});

    if (totalPages > 1) {{
      const nextPage = (libraryPage + 1) % totalPages;
      buttonsHtml += `<button class="choice-btn" style="color:#f39c12;" onclick="showLibraryScreen(${{nextPage}})">[5] 다음 페이지 서재 목록 보기 (Page ${{nextPage + 1}}/${{totalPages}})</button>`;
    }}

    buttonsHtml += `<button class="choice-btn" style="background:#282828;" onclick="showTitleScreen()">[*] 메인 메뉴로 돌아가기 (ESC / Q)</button>`;
    
    document.getElementById('choiceBox').innerHTML = buttonsHtml;
    
    renderStaticFrame(pageItems[0].scenes[1].rle[0]);
  }}

  function startTutorial() {{
    loadPackById('heungbu');
  }}

  function loadPackById(packId) {{
    curPack = masterData.packs.find(p => p.id === packId);
    gameState = 'IN_GAME';
    curSceneIdx = 0;
    curFrame = 0;
    metricValue = 3;
    hideHint();
    
    document.getElementById('metricName').innerText = `${{curPack.metric_icon}} ${{curPack.metric_name}}`;
    document.getElementById('sysInfo').innerHTML = `◈ 작품: ${{curPack.title}}<br>◈ [0] 💡 지혜의 사색 힌트<br>◈ [*] 서재로 나가기`;
    
    loadScene(0);
  }}

  function loadScene(idx) {{
    curSceneIdx = idx;
    curFrame = 0;
    hideHint();
    const scene = curPack.scenes[curSceneIdx];
    
    document.getElementById('headerTitle').innerText = `◆ ${{curPack.title}} · 제${{scene.act}}막: ${{scene.title}} ◆`;
    document.getElementById('speakerName').innerText = scene.speaker;
    document.getElementById('dialogueText').innerText = scene.text;
    document.getElementById('feedbackText').innerText = scene.is_transition ? "진행: [Enter] / 사색 힌트: [0] / 서재 나가기: [*]" : "선택: [1], [2] / 사색 힌트: [0] / 서재 나가기: [*]";
    
    updateMetricUI();
    
    const box = document.getElementById('choiceBox');
    box.innerHTML = '';
    
    if (scene.is_transition) {{
      const btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.innerText = `▶ ${{scene.button_text}} [Enter]`;
      btn.onclick = () => advanceScene(0);
      box.appendChild(btn);
    }} else {{
      scene.choices.forEach((c, i) => {{
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.innerText = `[${{i+1}}] ${{c.text}} (${{c.delta >= 0 ? '+' + c.delta : c.delta}})`;
        btn.onclick = () => {{
          document.getElementById('dialogueText').innerText = c.feedback;
          setTimeout(() => advanceScene(c.delta), 850);
        }};
        box.appendChild(btn);
      }});
    }}

    // 하단 힌트 버튼 추가
    const hintBtn = document.createElement('button');
    hintBtn.className = 'choice-btn';
    hintBtn.style.background = '#282315';
    hintBtn.style.borderColor = '#7d6608';
    hintBtn.style.color = '#f9e79f';
    hintBtn.innerText = `[0] 💡 지혜의 사색 힌트 열기/닫기`;
    hintBtn.onclick = toggleHint;
    box.appendChild(hintBtn);
  }}

  function toggleHint() {{
    if (gameState !== 'IN_GAME') return;
    const scene = curPack.scenes[curSceneIdx];
    const hb = document.getElementById('hintBox');
    hintVisible = !hintVisible;
    if (hintVisible && scene.hint) {{
      hb.innerText = "💡 [원작 사색 노트] " + scene.hint;
      hb.style.display = 'block';
    }} else {{
      hb.style.display = 'none';
    }}
  }}

  function hideHint() {{
    hintVisible = false;
    const hb = document.getElementById('hintBox');
    if (hb) hb.style.display = 'none';
  }}

  function advanceScene(delta) {{
    metricValue = Math.max(0, Math.min(10, metricValue + delta));
    updateMetricUI();
    
    if (curSceneIdx + 1 >= curPack.scenes.length) {{
      showEnding();
    }} else {{
      loadScene(curSceneIdx + 1);
    }}
  }}

  function updateMetricUI() {{
    document.getElementById('metricVal').innerText = `${{metricValue}} / 10`;
    document.getElementById('metricBar').style.width = `${{metricValue * 10}}%`;
  }}

  function showEnding() {{
    gameState = 'ENDING';
    hideHint();
    let matched = curPack.endings[curPack.endings.length - 1];
    for (let end of curPack.endings) {{
      if (metricValue >= end.min) {{
        matched = end;
        break;
      }}
    }}
    
    document.getElementById('headerTitle').innerText = `◆ ${{curPack.title}} 완결 · 여정의 끝 ◆`;
    document.getElementById('speakerName').innerText = "달성 칭호: " + matched.title;
    document.getElementById('dialogueText').innerText = matched.desc;
    document.getElementById('feedbackText').innerText = `최종 ${{curPack.metric_name}}: ${{metricValue}}/10 — 플레이해주셔서 감사합니다!`;
    
    const box = document.getElementById('choiceBox');
    box.innerHTML = `
      <button class="choice-btn" onclick="showLibraryScreen(0)">[1] 다른 명작 스토리 선택하기 (서재로)</button>
      <button class="choice-btn" onclick="showTitleScreen()">[2] 처음 메인 타이틀로 (R)</button>
    `;
  }}

  function renderStaticFrame(rleStr) {{
    const imgData = ctx.createImageData(296, 152);
    const chunks = rleStr.split(',');
    let pIdx = 0;
    for (let i = 0; i < chunks.length; i++) {{
      const parts = chunks[i].split('_');
      const count = parseInt(parts[0]);
      const colorIdx = parseInt(parts[1]);
      const hex = masterData.palette[colorIdx];
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      for (let c = 0; c < count; c++) {{
        imgData.data[pIdx] = r; imgData.data[pIdx+1] = g; imgData.data[pIdx+2] = b; imgData.data[pIdx+3] = 255;
        pIdx += 4;
      }}
    }}
    ctx.putImageData(imgData, 0, 0);
  }}

  function renderFrame() {{
    if (gameState !== 'IN_GAME') return;
    const scene = curPack.scenes[curSceneIdx];
    const rleStr = scene.rle[curFrame];
    renderStaticFrame(rleStr);
    
    const hud = document.getElementById('hudText');
    if (curFrame === 2) {{
      hud.innerText = `[제${{scene.act}}막 | ★ F3 핵심 감정/스파클 ★]`;
      hud.style.color = "#f4d03f";
    }} else {{
      hud.innerText = `[제${{scene.act}}막 | F${{curFrame+1}}/6 Ultra 296x152]`;
      hud.style.color = "#81d4fa";
    }}
  }}

  setInterval(() => {{
    if (gameState === 'IN_GAME') {{
      const scene = curPack.scenes[curSceneIdx];
      curFrame = (curFrame + 1) % scene.rle.length;
      renderFrame();
    }}
  }}, 750);

  // 키보드 조작계:
  // [1~5]: 선택지 및 다음페이지
  // [0]: 💡 힌트 토글
  // [*, Q, ESC]: 서재 / 뒤로가기
  window.addEventListener('keydown', (e) => {{
    if (gameState === 'TITLE') {{
      if (e.key === '1') startTutorial();
      else if (e.key === '2') showLibraryScreen(0);
    }} else if (gameState === 'LIBRARY') {{
      const literaturePacks = masterData.packs.slice(1);
      const startIdx = libraryPage * ITEMS_PER_PAGE;
      const pageItems = literaturePacks.slice(startIdx, startIdx + ITEMS_PER_PAGE);
      
      if (e.key === '1' && pageItems[0]) loadPackById(pageItems[0].id);
      else if (e.key === '2' && pageItems[1]) loadPackById(pageItems[1].id);
      else if (e.key === '3' && pageItems[2]) loadPackById(pageItems[2].id);
      else if (e.key === '5') {{
        const totalPages = Math.ceil(literaturePacks.length / ITEMS_PER_PAGE);
        showLibraryScreen((libraryPage + 1) % totalPages);
      }}
      else if (e.key === '*' || e.key === 'q' || e.key === 'Q' || e.key === 'Escape') showTitleScreen();
    }} else if (gameState === 'IN_GAME') {{
      const scene = curPack.scenes[curSceneIdx];
      if (e.key === '*' || e.key === 'q' || e.key === 'Q' || e.key === 'Escape') {{
        showLibraryScreen(0);
        return;
      }}
      if (e.key === '0') {{
        toggleHint();
        return;
      }}
      if (scene.is_transition) {{
        if (e.key === 'Enter' || e.code === 'Space') advanceScene(0);
      }} else {{
        if (e.key === '1') {{
          const c = scene.choices[0];
          document.getElementById('dialogueText').innerText = c.feedback;
          setTimeout(() => advanceScene(c.delta), 650);
        }} else if (e.key === '2' && scene.choices.length > 1) {{
          const c = scene.choices[1];
          document.getElementById('dialogueText').innerText = c.feedback;
          setTimeout(() => advanceScene(c.delta), 650);
        }}
      }}
    }} else if (gameState === 'ENDING') {{
      if (e.key === '1') showLibraryScreen(0);
      else if (e.key === '2' || e.key === 'r' || e.key === 'R') showTitleScreen();
    }}
  }});

  window.addEventListener('wheel', (e) => e.preventDefault(), {{ passive: false }});

  // 시작
  showTitleScreen();
</script>

</body>
</html>
"""

    html_path = "/mnt/d/game/Divina_Console.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_engine)
    print(f"✅ HTML 마스터 콘솔 작성 완료: {html_path} ({os.path.getsize(html_path)/1024:.1f} KB)")

    # Gzip 압축: game.html.gz 생성!
    with open(html_path, "rb") as f:
        raw_b = f.read()
    gz_b = gzip.compress(raw_b, 9)
    gz_path = "/mnt/d/game/game.html.gz"
    with open(gz_path, "wb") as f:
        f.write(gz_b)
    print(f"📦 Gzip 초압축 완료: {gz_path} ({len(gz_b)/1024:.1f} KB) — 1MB 한도 완전 수호!")

if __name__ == "__main__":
    build_master_system()
