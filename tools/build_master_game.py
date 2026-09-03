#!/usr/bin/env python3
"""
tools/build_master_game.py
Divina Ludus — 4대 명작 마스터 게임 엔진 통합 빌더
- 메인 타이틀 화면:
  * [1] 튜토리얼: 흥부놀부전 시작
  * [2] 문학 서재: 명작 스토리 선택 (제임스 복숭아, 단테 지옥편, 데미안)
- 4대 명작 28개 씬 풀 스토리, 분기 선택지, 메트릭, 멀티 엔딩 완벽 연동
- 16색 인덱스 컬러 + 296x152 영화적 6프레임 모션 탑재
- Gzip 초압축 (1MB 이하 단일 파일 배포 및 divina.exe 자동 컴파일 지원)
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
from generate_all_packs_studio import (
    gen_peach_act1, gen_peach_act2, gen_peach_act3, gen_peach_act4,
    gen_peach_act5, gen_peach_act6, gen_peach_act7,
    gen_dante_act1, gen_dante_act2, gen_dante_act3, gen_dante_act4,
    gen_dante_act5, gen_dante_act6, gen_dante_act7,
    gen_demian_act1, gen_demian_act2, gen_demian_act3, gen_demian_act4,
    gen_demian_act5, gen_demian_act6, gen_demian_act7,
    PALETTE_16, compress_frame_rle
)

def build_master_system():
    print("🎨 4대 명작 28개 씬 296x152 컷씬 렌더링 및 RLE 압축 중...")
    
    # 1. 흥부놀부전 (Tutorial)
    act1_heungbu = [
        [compress_frame_rle(f) for f in gen_hires_act1()],
        [compress_frame_rle(f) for f in gen_hires_act2()],
        [compress_frame_rle(f) for f in gen_hires_act3()],
        [compress_frame_rle(f) for f in gen_hires_act4()],
        [compress_frame_rle(f) for f in gen_hires_act5()],
        [compress_frame_rle(f) for f in gen_hires_act6()],
        [compress_frame_rle(f) for f in gen_hires_act7()],
    ]

    # 2. 제임스와 슈퍼 복숭아
    act1_peach = [
        [compress_frame_rle(f) for f in gen_peach_act1()],
        [compress_frame_rle(f) for f in gen_peach_act2()],
        [compress_frame_rle(f) for f in gen_peach_act3()],
        [compress_frame_rle(f) for f in gen_peach_act4()],
        [compress_frame_rle(f) for f in gen_peach_act5()],
        [compress_frame_rle(f) for f in gen_peach_act6()],
        [compress_frame_rle(f) for f in gen_peach_act7()],
    ]

    # 3. 단테의 신곡: 지옥편
    act1_dante = [
        [compress_frame_rle(f) for f in gen_dante_act1()],
        [compress_frame_rle(f) for f in gen_dante_act2()],
        [compress_frame_rle(f) for f in gen_dante_act3()],
        [compress_frame_rle(f) for f in gen_dante_act4()],
        [compress_frame_rle(f) for f in gen_dante_act5()],
        [compress_frame_rle(f) for f in gen_dante_act6()],
        [compress_frame_rle(f) for f in gen_dante_act7()],
    ]

    # 4. 데미안
    act1_demian = [
        [compress_frame_rle(f) for f in gen_demian_act1()],
        [compress_frame_rle(f) for f in gen_demian_act2()],
        [compress_frame_rle(f) for f in gen_demian_act3()],
        [compress_frame_rle(f) for f in gen_demian_act4()],
        [compress_frame_rle(f) for f in gen_demian_act5()],
        [compress_frame_rle(f) for f in gen_demian_act6()],
        [compress_frame_rle(f) for f in gen_demian_act7()],
    ]

    packs_data = [
        {
            "id": "heungbu",
            "title": "흥부놀부전",
            "tag": "Tutorial · 한국 고전",
            "metric_name": "선행의 씨앗",
            "metric_icon": "♧",
            "scenes": [
                {
                    "act": 1, "title": "형제의 갈림길", "speaker": "놀부",
                    "text": "네 이놈 흥부야! 내 집에 더는 쌀 한 톨 축낼 생각 마라! 처자식 데리고 썩 꺼지지 못할까!",
                    "rle": act1_heungbu[0], "is_transition": False,
                    "choices": [
                        {"text": "부모님 말씀을 떠올리며 조용히 돌아선다", "delta": 1, "feedback": "흥부는 눈물을 삼키며 빈손으로 형의 집을 나섰습니다."},
                        {"text": "억울함에 형에게 맞서 따져본다", "delta": -1, "feedback": "놀부가 몽둥이를 치켜들며 호통쳤습니다! '이놈이 감히 눈을 부라려?!'"}
                    ]
                },
                {
                    "act": 2, "title": "다친 제비", "speaker": "흥부 아내",
                    "text": "여보! 저 처마 밑 제비 좀 보세요! 구렁이에 놀라 떨어져 다리가 부러졌어요! 짹짹 울며 피를 흘려요!",
                    "rle": act1_heungbu[1], "is_transition": False,
                    "choices": [
                        {"text": "정성껏 하얀 부목을 대고 붉은 실로 감아준다", "delta": 2, "feedback": "흥부는 떨리는 손으로 새끼 제비 다리에 부목을 대고 붉은 실로 감아주었습니다."},
                        {"text": "우리 먹을 것도 없는데... 모른 척 돌아선다", "delta": -2, "feedback": "흥부는 한숨을 쉬며 발길을 돌렸습니다. 처마 밑엔 슬픈 울음소리만 남았습니다."}
                    ]
                },
                {
                    "act": 3, "title": "박씨를 물고 온 제비", "speaker": "해설",
                    "text": "이듬해 봄, 은혜를 갚으러 돌아온 제비가 푸른 하늘을 가르며 날아왔습니다. 부리에는 눈부신 황금빛 박씨가 물려 있었습니다!",
                    "rle": act1_heungbu[2], "is_transition": True, "button_text": "박씨를 마당 양지바른 곳에 정성껏 심는다"
                },
                {
                    "act": 4, "title": "흥부의 대박 타기", "speaker": "흥부",
                    "text": "여보! 지붕 위에 커다란 박이 열렸소! 톱을 가져와 함께 당깁시다! 슬근슬근 톱질하세, 엉차! 엉차!",
                    "rle": act1_heungbu[3], "is_transition": False,
                    "choices": [
                        {"text": "쏟아지는 금은보화를 가난한 이웃들과 나눈다", "delta": 2, "feedback": "쩍 갈라진 박 속에서 번쩍이는 엽전과 쌀알이 폭포수처럼 쏟아졌습니다!"},
                        {"text": "혹시 모르니 곳간 깊숙이 잘 숨겨둔다", "delta": 0, "feedback": "산더미 같은 재물을 얻었으나, 흥부는 신중하게 문을 걸어 잠갔습니다."}
                    ]
                },
                {
                    "act": 5, "title": "놀부의 탐욕", "speaker": "놀부",
                    "text": "뭐라?! 그 알거지 놈이 박을 타서 벼락부자가 되었다고?! 멀쩡한 제비 놈을 잡아다가 다리를 뚝 분질러서 나도 대박을 타야겠다!",
                    "rle": act1_heungbu[4], "is_transition": True, "button_text": "인과응보의 시간이 다가옵니다"
                },
                {
                    "act": 6, "title": "도깨비의 응징", "speaker": "도깨비",
                    "text": "놀부 놀부 못된 놀부야! 죄 없는 미물을 해치고 탐욕을 부린 죗값을 받아라! 가시 쇠몽둥이 맛을 보아라, 철썩!!",
                    "rle": act1_heungbu[5], "is_transition": True, "button_text": "알거지가 되어 길바닥에 쫓겨난 놀부"
                },
                {
                    "act": 7, "title": "눈물의 화해", "speaker": "놀부",
                    "text": "흥부야... 내가 천하의 몹쓸 놈이다... 네게 죄를 짓고 하늘의 벌을 받아 알거지가 되었구나... 날 용서하지 마라...",
                    "rle": act1_heungbu[6], "is_transition": False,
                    "choices": [
                        {"text": "울며 형의 손을 굳게 잡고 품에 안아 용서한다", "delta": 3, "feedback": "흥부는 엎드린 형을 부둥켜안고 통곡했습니다. '형님, 우리는 한 피를 나눈 형제입니다!'"},
                        {"text": "집과 양식은 내주되, 다시는 욕심부리지 말라 타이른다", "delta": 1, "feedback": "놀부는 고개를 숙이고 참회의 눈물을 흘리며 지난날의 악행을 뉘우쳤습니다."}
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
            "id": "peach",
            "title": "제임스와 슈퍼 복숭아",
            "tag": "Roald Dahl · 환상 모험",
            "metric_name": "경이와 용기",
            "metric_icon": "✦",
            "scenes": [
                {
                    "act": 1, "title": "스폰지와 스파이커 이모", "speaker": "스파이커 이모",
                    "text": "게으른 녀석! 장작을 더 패지 못해?! 지팡이로 뼈마디를 두들겨 맞아야 정신을 차릴 테냐!",
                    "rle": act1_peach[0], "is_transition": False,
                    "choices": [
                        {"text": "고분고분 장작을 패며 언젠가 올 자유를 꿈꾼다", "delta": 1, "feedback": "제임스는 입술을 깨물며 묵묵히 도끼를 쥐었습니다. 희망을 잃지 않았습니다."},
                        {"text": "억울함에 이모들에게 반항의 눈빛을 쏘아본다", "delta": -1, "feedback": "스파이커 이모가 앙상한 손으로 지팡이를 내리쳤습니다! '눈을 똑바로 뜨다니!'"}
                    ]
                },
                {
                    "act": 2, "title": "마법의 초록 악어 혀", "speaker": "신비로운 노인",
                    "text": "얘야, 이 봉투를 받거라. 이 안에는 수천 마리 악어의 혀로 빚어낸 거대한 마법이 꿈틀대고 있단다. 절대 흘리지 마라!",
                    "rle": act1_peach[1], "is_transition": False,
                    "choices": [
                        {"text": "소중히 품에 안고 마른 복숭아나무 밑으로 달린다", "delta": 2, "feedback": "봉투 속 초록빛 발광체들이 나무뿌리로 스며들며 대지가 쿵쿵 진동했습니다!"},
                        {"text": "의심하며 노인에게 무슨 속셈인지 캐묻는다", "delta": 0, "feedback": "노인은 기괴한 미소를 지으며 순식간에 안갯속으로 사라져 버렸습니다."}
                    ]
                },
                {
                    "act": 3, "title": "거대 복숭아의 탄생", "speaker": "해설",
                    "text": "복숭아나무 꼭대기에 맺힌 작은 복숭아가 심장처럼 쿵-쿵 박동하며 부풀어 오르더니, 마침내 집채만 한 거대 복숭아가 되었습니다!",
                    "rle": act1_peach[2], "is_transition": True, "button_text": "박동하는 복숭아의 터널 속으로 기어 들어간다"
                },
                {
                    "act": 4, "title": "거대 곤충 친구들", "speaker": "메뚜기 신사",
                    "text": "어서 오십시오, 어린 신사여! 두려워 마세요. 우리는 당신을 기다려 온 복숭아의 친구들이랍니다!",
                    "rle": act1_peach[3], "is_transition": False,
                    "choices": [
                        {"text": "두려움을 떨치고 정중히 신사들에게 악수를 청한다", "delta": 2, "feedback": "무당벌레와 지네가 환호하며 제임스를 둘러싸고 따스하게 환영했습니다!"},
                        {"text": "기괴한 크기의 벌레들에 비명을 지르며 벽으로 물러선다", "delta": -1, "feedback": "지네가 서운한 표정으로 수십 개의 다리를 긁적였습니다."}
                    ]
                },
                {
                    "act": 5, "title": "대서양으로의 출항", "speaker": "해설",
                    "text": "꼭지를 끊은 슈퍼 복숭아가 언덕을 맹렬히 굴러 내려가 절벽을 넘어 드넓은 대서양 바다로 풍덩 빠졌습니다! 푸른 바다 위를 당당히 항해합니다!",
                    "rle": act1_peach[4], "is_transition": True, "button_text": "갈매기를 낚아챌 실크 거미줄을 준비한다"
                },
                {
                    "act": 6, "title": "500마리 갈매기 비행", "speaker": "제임스",
                    "text": "지네 아저씨, 거미 아가씨, 서두르세요! 갈매기 목에 실을 걸어 복숭아를 공중으로 띄웁시다! 날아오른다, 하늘로!!",
                    "rle": act1_peach[5], "is_transition": False,
                    "choices": [
                        {"text": "지혜를 발휘해 갈매기 떼를 일사불란하게 지휘한다", "delta": 2, "feedback": "500마리의 흰 갈매기들이 날개를 퍼덕이며 복숭아를 구름 위로 들어 올렸습니다!"},
                        {"text": "상어 떼의 습격에 겁에 질려 눈을 감아버린다", "delta": -1, "feedback": "친구들의 격려 속에 제임스는 가까스로 중심을 잡았습니다."}
                    ]
                },
                {
                    "act": 7, "title": "엠파이어 빌딩 착륙", "speaker": "해설",
                    "text": "대서양을 건너 뉴욕 맨해튼 상공에 도달한 거대 복숭아가 엠파이어 스테이트 빌딩 첨탑에 사뿐히 꽂혔습니다! 온 도시가 환호의 꽃가루로 뒤덮입니다!",
                    "rle": act1_peach[6], "is_transition": False,
                    "choices": [
                        {"text": "달콤한 복숭아 과육을 뉴욕의 가난한 아이들에게 선물한다", "delta": 3, "feedback": "수만 명의 아이들이 환호하며 달콤한 복숭아를 나누어 먹었습니다!"},
                        {"text": "복숭아 씨앗 속에 집을 짓고 영원한 자유를 누린다", "delta": 1, "feedback": "제임스는 평생 가장 진실한 친구들과 함께 자유롭고 행복하게 살았습니다."}
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
                    "act": 1, "title": "어두운 숲과 베르길리우스", "speaker": "베르길리우스",
                    "text": "인생의 반환점에서 길을 잃은 시인이여, 두려워 마라. 내가 그대를 지옥과 연옥의 심연을 지나 천국으로 인도하리라.",
                    "rle": act1_dante[0], "is_transition": False,
                    "choices": [
                        {"text": "스승의 손을 잡고 지옥의 문으로 굳건히 발을 딛는다", "delta": 2, "feedback": "스승의 월계관이 어두운 숲속에서 성스러운 빛을 뿜어냈습니다."},
                        {"text": "세 마리 맹수의 포효에 뒷걸음질 치며 주저앉는다", "delta": -1, "feedback": "베르길리우스가 지팡이를 들어 맹수들을 쫓아내며 타이르고 이끌었습니다."}
                    ]
                },
                {
                    "act": 2, "title": "지옥의 문과 뱃사공 카론", "speaker": "카론",
                    "text": "이곳에 들어오는 자, 모든 희망을 버려라! 살아있는 자여, 썩 물러가라! 아케론 강 건너 영원한 암흑 속으로 떠날지니!",
                    "rle": act1_dante[1], "is_transition": False,
                    "choices": [
                        {"text": "스승의 가르침을 믿고 당당히 핏빛 나룻배에 오른다", "delta": 2, "feedback": "베르길리우스가 외쳤습니다. '카론이여, 이것은 하늘의 뜻이니 분노를 거두라!'"},
                        {"text": "망령들의 비명 소리에 공포에 질려 기절하고 만다", "delta": -2, "feedback": "단테는 핏빛 강물 앞에서 전율하며 정신을 잃고 말았습니다."}
                    ]
                },
                {
                    "act": 3, "title": "제2옥: 애욕의 암흑 폭풍", "speaker": "프란체스카",
                    "text": "오 자비로운 시인이여, 책을 읽다 사랑에 빠져 비극을 맞이한 우리를 가엾게 여겨 주소서... 영원한 암흑 폭풍 속에서도 우리는 서로를 놓지 못합니다...",
                    "rle": act1_dante[2], "is_transition": False,
                    "choices": [
                        {"text": "두 연인의 애달픈 비극에 깊이 탄식하며 눈물을 흘린다", "delta": 2, "feedback": "단테는 지극한 연민과 슬픔으로 가슴이 찢어지며 바닥에 엎드렸습니다."},
                        {"text": "죄는 죗값일 뿐이라며 냉정하게 고개를 돌린다", "delta": -1, "feedback": "베르길리우스가 침묵 속에서 단테의 차가운 눈빛을 응시했습니다."}
                    ]
                },
                {
                    "act": 4, "title": "제6옥: 불타는 석관의 파리나타", "speaker": "파리나타",
                    "text": "그대 피렌체의 말을 쓰는 나그네여! 지옥의 화염이 내 몸을 태울지라도, 내 조국 피렌체의 운명은 어떻게 되었는가!",
                    "rle": act1_dante[3], "is_transition": True, "button_text": "오만한 귀족의 숭고한 기개에 경의를 표한다"
                },
                {
                    "act": 5, "title": "제7옥: 끓는 피의 강 플레게톤", "speaker": "해설",
                    "text": "이웃을 해친 폭군들이 펄펄 끓는 핏빛 강물 속에서 울부짖고, 강둑에서는 반인반마 켄타우로스들이 활시위를 팽팽히 당기고 있습니다!",
                    "rle": act1_dante[4], "is_transition": True, "button_text": "침착하게 네소스의 등에 올라 피의 강을 건넌다"
                },
                {
                    "act": 6, "title": "제8옥: 말레볼제의 구덩이", "speaker": "해설",
                    "text": "거대한 지옥 뱀들이 도둑들의 몸을 칭칭 감고 물어뜯습니다. 물린 육신이 재로 타들어 갔다가 다시 인간으로 부활하는 지독한 고통이 끝없이 반복됩니다!",
                    "rle": act1_dante[5], "is_transition": True, "button_text": "죄악의 끔찍한 실체를 직시하며 심연으로 내려간다"
                },
                {
                    "act": 7, "title": "얼음 지옥 탈출과 별들의 찬가", "speaker": "단테",
                    "text": "스승이여! 거대한 얼음 호수 코키토스를 지나 마침내 지옥의 구멍을 빠져나왔습니다! 머리 위로 밤하늘의 찬란한 별들이 쏟아져 내립니다!!",
                    "rle": act1_dante[6], "is_transition": False,
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
        },
        {
            "id": "demian",
            "title": "데미안",
            "tag": "Hermann Hesse · 자아 실현",
            "metric_name": "내면의 각성",
            "metric_icon": "☥",
            "scenes": [
                {
                    "act": 1, "title": "두 개의 세계와 크로머", "speaker": "프란츠 크로머",
                    "text": "사과를 훔쳤다고 떠벌리더니 겁쟁이 녀석! 내일까지 2마르크를 가져오지 않으면 경찰에 네 죄를 다 불어버릴 테다, 알겠냐?",
                    "rle": act1_demian[0], "is_transition": False,
                    "choices": [
                        {"text": "양심의 가책을 느끼며 더 이상 거짓에 휘둘리지 않기로 결심한다", "delta": 2, "feedback": "싱클레어는 떨리는 가슴을 쥐며 어둠의 굴레에서 벗어나려 몸부림쳤습니다."},
                        {"text": "공포에 질려 부모님의 서랍에서 돈을 훔치려 한다", "delta": -2, "feedback": "크로머의 휘파람 소리가 귓가에 맴돌며 영혼이 타락해 갔습니다."}
                    ]
                },
                {
                    "act": 2, "title": "막스 데미안과 카인의 표식", "speaker": "데미안",
                    "text": "싱클레어, 카인은 비열한 살인자가 아니야. 그는 남들이 감히 갖지 못한 고결한 힘과 용기를 지녔기에 '표식'을 지니게 된 거란다.",
                    "rle": act1_demian[1], "is_transition": False,
                    "choices": [
                        {"text": "그의 대담하고 신비로운 해석에 전율하며 귀를 기울인다", "delta": 2, "feedback": "데미안의 이마에서 은은한 황금빛 후광이 비치며 싱클레어의 닫힌 눈이 뜨였습니다."},
                        {"text": "기존 교회의 가르침과 다르다며 두려워 귀를 닫는다", "delta": -1, "feedback": "데미안은 그윽한 눈빛으로 싱클레어를 바라보며 조용히 미소 지었습니다."}
                    ]
                },
                {
                    "act": 3, "title": "베아트리체 초상화", "speaker": "싱클레어",
                    "text": "이젤 앞에 서서 홀린 듯 그린 이 얼굴... 소녀인 줄 알았으나 데미안이며, 동시에 내 영혼 깊은 곳의 참된 자아의 얼굴이로구나!",
                    "rle": act1_demian[2], "is_transition": True, "button_text": "초상화에 불을 붙여 태우며 영혼의 편지를 띄운다"
                },
                {
                    "act": 4, "title": "알을 깨는 매의 비상", "speaker": "아브락사스",
                    "text": "'새는 알에서 나오려고 투쟁한다. 알은 세계다. 태어나려는 자는 하나의 세계를 파괴해야 한다. 신의 이름은 아브락사스다.'",
                    "rle": act1_demian[3], "is_transition": False,
                    "choices": [
                        {"text": "기존의 세계를 부수고 알을 깨며 푸른 하늘로 날아오른다", "delta": 3, "feedback": "황금빛 매가 껍질을 박차고 솟구쳐 창공을 향해 포효했습니다!"},
                        {"text": "안온하고 익숙한 유년의 껍질 속에 머물고 싶어 망설인다", "delta": -2, "feedback": "내면의 알껍데기가 삐걱거리며 성장통의 괴로움이 엄습했습니다."}
                    ]
                },
                {
                    "act": 5, "title": "피스토리우스와 불꽃", "speaker": "피스토리우스",
                    "text": "싱클레어, 타오르는 불꽃 속을 응시하게. 그대가 꿈꾸는 모든 신비는 이미 그대의 가슴속에 살아 숨 쉬고 있네!",
                    "rle": act1_demian[4], "is_transition": True, "button_text": "파이프오르간의 장엄한 선율 속에서 자아를 응시한다"
                },
                {
                    "act": 6, "title": "에바 부인의 품", "speaker": "에바 부인",
                    "text": "싱클레어, 그대는 먼 길을 돌아 마침내 나를 찾아왔군요. 사랑은 애원하는 것이 아니라, 스스로의 내부에서 확신에 차오르는 것이랍니다.",
                    "rle": act1_demian[5], "is_transition": True, "button_text": "대모신의 자애로운 손길을 느끼며 눈물 흘린다"
                },
                {
                    "act": 7, "title": "마지막 키스와 거울 속 자아", "speaker": "데미안",
                    "text": "싱클레어, 네 안의 소리에 귀를 기울여 봐. 언젠가 네가 나를 부를 때... 이제 거울을 보면 내 모습이 바로 너 자신 안에 보일 거야.",
                    "rle": act1_demian[6], "is_transition": False,
                    "choices": [
                        {"text": "거울 속 완전히 성숙해진 나 자신을 직시하며 미소 짓는다", "delta": 3, "feedback": "거울 속에 비친 싱클레어의 눈동자는 완전히 데미안과 하나가 되어 있었습니다."},
                        {"text": "떠나간 친구의 빈자리에 눈물을 흘리며 작별을 고한다", "delta": 1, "feedback": "데미안의 키스는 영원한 표식이 되어 싱클레어의 영혼에 아로새겨졌습니다."}
                    ]
                }
            ],
            "endings": [
                {"min": 8, "title": "아브락사스에 도달한 자", "desc": "빛과 어둠의 세계를 모두 통합하고, 알을 깨고 나와 온전한 참 자아를 실현했습니다."},
                {"min": 5, "title": "표식을 지닌 자 (카인의 후예)", "desc": "세상의 규율에 굴복하지 않고 내면의 부름을 따르는 고결한 영혼의 소유자가 되었습니다."},
                {"min": -99, "title": "알을 깨는 순례자", "desc": "수많은 방황과 고통 끝에 마침내 스스로의 삶을 대면할 용기를 얻었습니다."}
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
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  .console-frame {{
    width: 880px;
    height: 840px;
    background: #1e1e1e;
    border: 3px solid #4a4a4a;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.9);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .console-header {{
    background: #2d2d2d;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #3a3a3a;
  }}
  .console-title {{ font-size: 15px; font-weight: bold; color: #ffcc99; }}
  .console-hud {{ font-size: 13px; color: #81d4fa; font-family: monospace; }}
  
  .canvas-container {{
    background: #0a0a0a;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
    border-bottom: 2px solid #333;
    position: relative;
  }}
  canvas {{
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    width: 820px;
    height: 420px;
    background: #252525;
    border: 2px solid #444;
    box-shadow: 0 4px 15px rgba(0,0,0,0.7);
  }}
  
  .bottom-panel {{
    flex: 1;
    display: flex;
    padding: 14px 20px;
    gap: 16px;
    background: #181818;
  }}
  .dialogue-box {{
    flex: 6;
    background: #222;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .speaker {{
    font-size: 15px;
    font-weight: bold;
    color: #f4d03f;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .speaker::before {{ content: "◈"; color: #e74c3c; }}
  .dialogue-text {{
    font-size: 14px;
    line-height: 1.6;
    color: #ffffff;
    word-break: keep-all;
    min-height: 50px;
  }}
  
  .system-box {{
    flex: 4;
    background: #222;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .metric-label {{
    font-size: 13px;
    color: #aaa;
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
  }}
  .metric-track {{
    height: 12px;
    background: #333;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #555;
  }}
  .metric-fill {{
    height: 100%;
    width: 30%;
    background: linear-gradient(90deg, #27ae60, #2ecc71);
    transition: width 0.4s ease;
  }}
  
  .choice-container {{
    padding: 0 20px 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: #181818;
  }}
  .choice-btn {{
    background: #2c3e50;
    color: #ecf0f1;
    border: 1px solid #34495e;
    padding: 11px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    transition: all 0.15s;
  }}
  .choice-btn:hover {{
    background: #34495e;
    border-color: #f39c12;
    color: #f1c40f;
    transform: translateX(4px);
  }}
</style>
</head>
<body>

<div class="console-frame">
  <div class="console-header">
    <div class="console-title" id="headerTitle">◆ Divina Ludus · 고전문학 서재 ◆</div>
    <div class="console-hud" id="hudText">[Native 296x152 4X Engine]</div>
  </div>

  <div class="canvas-container">
    <canvas id="retroCanvas" width="296" height="152"></canvas>
  </div>

  <div class="bottom-panel">
    <div class="dialogue-box">
      <div>
        <div class="speaker" id="speakerName">사서</div>
        <div class="dialogue-text" id="dialogueText">환영합니다, 순례자여. 서재의 책을 펼쳐 여정을 시작하십시오.</div>
      </div>
      <div style="font-size: 12px; color: #888;" id="feedbackText">키보드 [1], [2], [3], [4] 키를 눌러 선택할 수 있습니다.</div>
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
      <div style="font-size: 12px; color: #888; line-height: 1.4;" id="sysInfo">
        ◈ 모드: 메인 라이브러리<br>
        ◈ 1번: 기본 튜토리얼 (흥부놀부)<br>
        ◈ 2번: 정식 명작 서재 (3대 명작)
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
  
  function showTitleScreen() {{
    gameState = 'TITLE';
    curPack = null;
    document.getElementById('headerTitle').innerText = "◆ Divina Ludus · 고전문학 서재 ◆";
    document.getElementById('speakerName').innerText = "안내 사서";
    document.getElementById('dialogueText').innerText = "환영합니다, 순례자여. [1]번을 눌러 조작법과 룰을 익히는 '기본 튜토리얼'을 시작하거나, [2]번을 눌러 '정식 문학 서재'로 입장하십시오.";
    document.getElementById('feedbackText').innerText = "키보드 [1] 또는 [2] 키를 누르세요.";
    document.getElementById('metricName').innerText = "◈ 준비 상태";
    document.getElementById('metricVal').innerText = "대기 중";
    document.getElementById('metricBar').style.width = "100%";
    document.getElementById('sysInfo').innerHTML = "◈ [1] 기본 튜토리얼<br>◈ [2] 정식 문학 서재<br>◈ 1MB 무설치 단일 엔진";

    const box = document.getElementById('choiceBox');
    box.innerHTML = `
      <button class="choice-btn" onclick="startTutorial()">[1] 기본 튜토리얼 시작: 《흥부놀부전》 (초심자 추천)</button>
      <button class="choice-btn" onclick="showLibraryScreen()">[2] 정식 문학 서재 입장 (제임스 복숭아, 단테 지옥편, 데미안)</button>
    `;
    
    // 타이틀 컷씬: 흥부놀부 1막 프레임 렌더링
    renderStaticFrame(masterData.packs[0].scenes[0].rle[0]);
  }}

  function showLibraryScreen() {{
    gameState = 'LIBRARY';
    document.getElementById('headerTitle').innerText = "◆ 정식 문학 서재 · 작품 선택 ◆";
    document.getElementById('speakerName').innerText = "서재의 문지기";
    document.getElementById('dialogueText').innerText = "어떤 영혼의 여정을 탐험하시겠습니까? 플레이하고자 하는 명작의 번호를 선택하십시오.";
    document.getElementById('feedbackText').innerText = "키보드 [1], [2], [3] 키 또는 [0] 뒤로가기를 누르세요.";

    const box = document.getElementById('choiceBox');
    box.innerHTML = `
      <button class="choice-btn" onclick="loadPackById('peach')">[1] 《제임스와 슈퍼 복숭아》 (Roald Dahl · ✦ 경이와 용기)</button>
      <button class="choice-btn" onclick="loadPackById('dante')">[2] 《단테의 신곡: 지옥편》 (Dante · ☩ 이성과 영혼의 빛)</button>
      <button class="choice-btn" onclick="loadPackById('demian')">[3] 《데미안》 (Hermann Hesse · ☥ 내면의 각성)</button>
      <button class="choice-btn" style="background:#444;" onclick="showTitleScreen()">[0] 메인 메뉴로 돌아가기 (ESC)</button>
    `;
    
    // 서재 대표 컷씬: 제임스 복숭아 3막
    renderStaticFrame(masterData.packs[1].scenes[2].rle[0]);
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
    
    document.getElementById('metricName').innerText = `${{curPack.metric_icon}} ${{curPack.metric_name}}`;
    document.getElementById('sysInfo').innerHTML = `◈ 작품: ${{curPack.title}}<br>◈ 갈래: ${{curPack.tag}}<br>◈ [0] 서재로 나가기`;
    
    loadScene(0);
  }}

  function loadScene(idx) {{
    curSceneIdx = idx;
    curFrame = 0;
    const scene = curPack.scenes[curSceneIdx];
    
    document.getElementById('headerTitle').innerText = `◆ ${{curPack.title}} · 제${{scene.act}}막: ${{scene.title}} ◆`;
    document.getElementById('speakerName').innerText = scene.speaker;
    document.getElementById('dialogueText').innerText = scene.text;
    document.getElementById('feedbackText').innerText = scene.is_transition ? "진행하려면 [Enter] 키 또는 아래 버튼을 누르세요." : "키보드 [1], [2] 키로 선택하세요.";
    
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
          setTimeout(() => advanceScene(c.delta), 900);
        }};
        box.appendChild(btn);
      }});
    }}
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
      <button class="choice-btn" onclick="showLibraryScreen()">[1] 다른 명작 스토리 선택하기 (서재로)</button>
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
      hud.innerText = `[제${{scene.act}}막 | F${{curFrame+1}}/6 Native 296x152]`;
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

  // 키보드 마스터 조작계 (1, 2, 3, 0, Enter, Space, Escape)
  window.addEventListener('keydown', (e) => {{
    if (gameState === 'TITLE') {{
      if (e.key === '1') startTutorial();
      else if (e.key === '2') showLibraryScreen();
    }} else if (gameState === 'LIBRARY') {{
      if (e.key === '1') loadPackById('peach');
      else if (e.key === '2') loadPackById('dante');
      else if (e.key === '3') loadPackById('demian');
      else if (e.key === '0' || e.key === 'Escape') showTitleScreen();
    }} else if (gameState === 'IN_GAME') {{
      const scene = curPack.scenes[curSceneIdx];
      if (e.key === '0' || e.key === 'Escape') {{
        showLibraryScreen();
        return;
      }}
      if (scene.is_transition) {{
        if (e.key === 'Enter' || e.code === 'Space') advanceScene(0);
      }} else {{
        if (e.key === '1') {{
          const c = scene.choices[0];
          document.getElementById('dialogueText').innerText = c.feedback;
          setTimeout(() => advanceScene(c.delta), 700);
        }} else if (e.key === '2' && scene.choices.length > 1) {{
          const c = scene.choices[1];
          document.getElementById('dialogueText').innerText = c.feedback;
          setTimeout(() => advanceScene(c.delta), 700);
        }}
      }}
    }} else if (gameState === 'ENDING') {{
      if (e.key === '1') showLibraryScreen();
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
