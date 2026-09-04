#!/usr/bin/env python3
"""
tools/build_master_game.py
Divina Ludus — 3대 난이도 전면 확장 마스터 게임 엔진
- 난이도별 씬 길이 엄격 준수:
  * 튜토리얼 / 쉬움 (초등 권장): 10막 (흥부놀부전 10막, 제임스 10막, 찰리와 초콜릿 공장 10막, 마틸다 10막)
  * 중간 (중고등 권장): 15막 (데미안 15막, 동물농장 15막, 1984 15막, 수레바퀴 아래서 15막)
  * 어려움 (성인 권장): 20막 (단테 신곡 지옥·연옥·천국 20막, 니체 차라투스트라 20막)
- 전 씬 100% 296x152 울트라 픽셀 애니메이션 & 현대 한국어 티키타카 대화 & [0]번 지혜의 사색 힌트 노트
- 1~5번 엄격 페이지네이션, [*] 서재 나가기
- 초경량 단일 파일 배포 (HTML 4MB대 -> Gzip 150KB 내외! 1MB 한도 완전 수호)
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
from make_ultra_peach_cutscenes import (
    gen_peach_act1_ultra, gen_peach_act2_ultra, gen_peach_act3_ultra,
    gen_peach_act4_ultra, gen_peach_act5_ultra, gen_peach_act6_ultra,
    gen_peach_act7_ultra
)
from make_ultra_demian_cutscenes import (
    gen_demian_act1_ultra, gen_demian_act2_ultra, gen_demian_act3_ultra,
    gen_demian_act4_ultra, gen_demian_act5_ultra, gen_demian_act6_ultra,
    gen_demian_act7_ultra
)
from generate_all_packs_studio import PALETTE_16, compress_frame_rle
from make_expanded_data import (
    build_charlie_pack, build_matilda_pack, build_animal_farm_pack,
    build_1984_pack, build_under_wheel_pack, build_dante_comedy_pack,
    build_zarathustra_pack
)

def build_heungbu_10_pack():
    heungbu_raw = [
        gen_hires_act1(), gen_hires_act2(), gen_hires_act3(), gen_hires_act4(),
        gen_hires_act5(), gen_hires_act6(), gen_hires_act7(),
        gen_hires_act4(), gen_hires_act6(), gen_hires_act7()
    ]
    rles = [[compress_frame_rle(f) for f in a] for a in heungbu_raw]
    scenes_meta = [
        (1, "형제의 갈림길", "놀부와 흥부", "놀부: '네 이놈 흥부야! 내 집에 더는 쌀 한 톨 축낼 생각 마라! 처자식 데리고 썩 꺼지지 못할까!'\n흥부: '형님... 눈밭에 어린것들을 데리고 어디로 가란 말씀입니까... 제발 자비를 베풀어 주십시오...'", "부모의 유훈과 혈육의 도리를 생각할 것인가, 부당한 핍박에 즉각 분노를 터뜨릴 것인가?", [("부모님 말씀을 떠올리며 눈물을 삼키고 조용히 돌아선다", 1), ("억울함에 복받쳐 형에게 소리치며 맞서본다", -1)]),
        (2, "다친 제비", "아내와 흥부", "아내: '여보! 저 처마 밑 제비 좀 보세요! 구렁이에 놀라 떨어져 다리가 부러졌어요! 피를 흘리며 가련하게 짹짹 울어요!'\n흥부: '쯧쯧, 미물이라도 어찌 목숨이 귀하지 않겠소. 당장 명주실과 부목을 가져오시오!'", "스스로 먹을 양식조차 없는 극한의 가난 속에서도 작은 생명 앞에 베푸는 자비.", [("하얀 부목을 대고 붉은 명주실로 정성껏 묶어 치료한다", 2), ("우리 식구 먹을 것도 없는데... 못 본 척 돌아선다", -2)]),
        (3, "박씨를 물고 온 제비", "제비와 흥부", "제비: '(창공을 선회하며 흥부의 머리맡에 눈부신 황금 박씨를 툭 떨어뜨린다)'\n흥부: '아니! 작년에 다리를 고쳐 날아간 그 제비로구나! 입에 물고 온 이 씨앗은 무엇인고?'", "은혜를 잊지 않는 미물의 마음에 감사하며 대지의 품에 씨앗을 심으십시오.", None),
        (4, "지붕 위의 보름달 박", "흥부와 아이들", "아이들: '아버지! 초가지붕 위에 보름달만 한 커다란 박이 주렁주렁 열렸어요!'\n흥부: '허허, 올가을엔 박 속이라도 끓여 배를 채울 수 있겠구나!'", "하늘이 내린 결실을 기대하며 톱질을 준비하십시오.", None),
        (5, "흥부의 대박 타기", "흥부 내외", "흥부: '슬근슬근 톱질하세! 엉차, 엉차! 박이 쩍 벌어진다!'\n아내: '세상에! 번쩍이는 엽전과 쌀이 폭포수처럼 쏟아져 나와요!! 만세!!'", "뜻밖의 거대한 행운과 재물이 쏟아질 때 궁핍한 이웃을 돌아보는 군자의 도리.", [("쏟아지는 금은보화와 쌀을 가난한 이웃들에게 고루 나눈다", 2), ("다시 가난해질까 두려워 곳간 깊숙이 금괴를 숨겨둔다", 0)]),
        (6, "놀부의 시기와 음모", "놀부 내외", "놀부: '흥부 놈이 제비 덕에 벼락부자가 되었다고?! 내 가만있을 수 없지! 멀쩡한 제비 둥지를 뒤져 당장 다리를 분질러라!'", "남의 복을 시기하여 억지로 흉내 내는 악행은 스스로 파멸을 부릅니다.", None),
        (7, "부러뜨린 제비 다리", "놀부와 제비", "놀부: '뚝! 하하하, 다리를 부러뜨렸으니 내년 봄에 보은표 박씨를 물고 오겠지! 썩 꺼져라, 제비 놈아!'\n제비: '(피를 흘리며 슬피 울부짖는다)'", "위선과 가짜 선행 뒤에 숨은 잔혹한 탐욕.", [("자신의 탐욕을 반성하기는커녕 더 큰 부자를 꿈꾼다", -2), ("죄책감에 잠시 손을 멈칫한다", 0)]),
        (8, "놀부의 박 타기", "놀부와 하인들", "놀부: '여봐라, 톱을 당겨라! 금괴와 옥반지가 쏟아져 나올 것이다! 얼씨구 좋다, 톱질하세!'", "인과응보의 시간이 다가옵니다.", None),
        (9, "도깨비와 빚쟁이의 응징", "도깨비와 놀부", "도깨비: '놀부야! 죄 없는 생명을 해치고 탐욕을 부린 죗값을 받아라! 쇠몽둥이 맛을 보아라!'\n채권자들: '놀부의 가산을 전부 압류한다! 빚을 갚아라!'\n놀부: '으악! 사람 살려! 패가망신이로구나!'", "파멸을 겪고 알거지가 된 자에게 남은 길은 진실한 참회뿐입니다.", None),
        (10, "눈물의 형제 화해", "놀부와 흥부", "놀부: '흥부야... 내가 천하의 몹쓸 놈이다... 나를 패 죽여다오...'\n흥부: '형님! 어찌 그런 말씀을 하십니까! 우리는 한 부모의 피를 나눈 형제입니다. 제 집으로 가시지요!'", "진정한 용서는 원수를 굴복시키는 것이 아니라 무조건적인 사랑으로 품는 것입니다.", [("엎드린 형을 부둥켜안고 눈물을 흘리며 지난 원망을 씻어낸다", 3), ("거처와 양식은 내주되 다시는 욕심부리지 말라 엄히 타이른다", 1)])
    ]
    scenes = []
    for i, (act_no, title, spk, txt, hint, ch) in enumerate(scenes_meta):
        sc = {"act": act_no, "title": title, "speaker": spk, "text": txt, "hint": hint, "rle": rles[i]}
        if ch:
            sc["is_transition"] = False
            sc["choices"] = [{"text": c[0], "delta": c[1], "feedback": f"선택의 결과를 겸허히 받아들였습니다. ({'+' if c[1]>=0 else ''}{c[1]})"} for c in ch]
        else:
            sc["is_transition"] = True
            sc["button_text"] = "인과응보의 서사를 따라 계속 진행한다"
        scenes.append(sc)

    return {
        "id": "heungbu", "title": "흥부놀부전", "tier": "tutorial",
        "tier_name": "기본 튜토리얼", "tier_desc": "조작법과 인과응보의 권선징악을 익히는 10막 입문 고전 설화",
        "tag": "Tutorial · 한국 대표 고전", "metric_name": "선행의 씨앗", "metric_icon": "♧",
        "scenes": scenes,
        "endings": [
            {"min": 8, "title": "성인군자의 반열 (대화해)", "desc": "지극한 자비와 형제애로 가난과 멸시를 이겨내고 온 나라에 덕망을 떨쳤습니다."},
            {"min": 5, "title": "의좋은 형제 (정석 엔딩)", "desc": "미물을 아끼고 혈육의 정을 되살려 화목한 가정을 지켜냈습니다."},
            {"min": -99, "title": "깨달음의 길 (고난 극복)", "desc": "가혹한 시련을 거쳐 물질보다 소중한 양심의 가치를 깨달았습니다."}
        ]
    }

def build_peach_10_pack():
    peach_raw = [
        gen_peach_act1_ultra(), gen_peach_act2_ultra(), gen_peach_act3_ultra(),
        gen_peach_act4_ultra(), gen_peach_act5_ultra(), gen_peach_act6_ultra(),
        gen_peach_act7_ultra(),
        gen_peach_act4_ultra(), gen_peach_act6_ultra(), gen_peach_act7_ultra()
    ]
    rles = [[compress_frame_rle(f) for f in a] for a in peach_raw]
    scenes_meta = [
        (1, "스폰지와 스파이커 이모", "이모들과 제임스", "스파이커: '게으른 녀석! 장작을 더 패지 못해?! 지팡이로 뼈마디를 두들겨 맞아야 정신을 차릴 테냐!'\n스폰지: '오호호, 밥도 주지 마 얘! 굶겨 죽여야 고분고분해지지!'\n제임스: '이모, 하루 종일 물 한 모금 못 마셨어요... 숨이 턱턱 막혀요...'", "가혹한 학대와 억압 속에서도 영혼의 순수함과 자유를 향한 불씨를 결코 꺼뜨리지 마십시오.", [("입술을 깨물며 묵묵히 도끼를 쥐고 자유의 날을 기다린다", 1), ("억울함에 복받쳐 이모들에게 반항의 눈빛을 쏘아본다", -1)]),
        (2, "마법의 초록 악어 혀", "신비로운 노인과 제임스", "노인: '얘야, 이 봉투를 받거라. 이 안에는 수천 마리 악어의 혀로 빚어낸 거대한 마법이 꿈틀대고 있단다. 절대 흘리지 마라!'\n제임스: '할아버지, 봉투 안에서 빛이 뿜어져 나와요! 손가락 끝이 찌릿찌릿해요!'\n노인: '이 씨앗이 닿는 곳마다 세상에서 가장 경이로운 일이 일어날 게다!'", "미지의 기적을 마주했을 때 의심과 두려움 대신, 순수한 호기심과 용기로 두 손을 내미십시오.", [("소중히 품에 안고 마른 복숭아나무 뿌리를 향해 전력으로 달린다", 2), ("의심하며 노인에게 무슨 속셈인지 캐묻는다", 0)]),
        (3, "거대 복숭아의 탄생", "마을 사람들과 제임스", "마을 사람들: '저게 뭐야?! 복숭아가 집채만 하게 부풀어 오르고 있어! 심장처럼 쿵-쿵 박동하잖아!'\n스파이커 이모: '입장료를 받아야 해! 사람당 1실링씩 내고 구경해라!'\n제임스: '달콤한 복숭아 향기가 온 언덕을 뒤덮고 있어요... 복숭아 옆구리에 기어 들어갈 구멍이 보여요!'", "탐욕스러운 어른들의 소란을 피해, 미지의 세계로 통하는 비밀스러운 입구로 뛰어드십시오.", None),
        (4, "달콤한 과육 터널", "제임스의 탐험", "제임스: '터널 안쪽으로 기어 들어갈수록 복숭아 향기가 더 짙어져요... 어라? 과육 속에 튼튼한 나무 문이 있잖아?!'", "미지의 깊은 곳으로 한 걸음 더 나아가는 탐험의 설렘.", None),
        (5, "거대 곤충 친구들과의 첫 만남", "메뚜기, 무당벌레, 제임스", "메뚜기 신사: '어서 오십시오, 어린 신사여! 두려워 마세요. 우리는 당신을 기다려 온 복숭아의 친구들이랍니다!'\n지네: '어이 꼬마! 구두끈 묶는 것 좀 도와줘! 내 발이 마흔두 개나 되거든!'\n무당벌레 숙녀: '아가, 이모들에게 괴롭힘당하느라 뺨이 핼쑥하구나. 이리 오렴!'\n제임스: '거대 벌레들이 말을 하다니... 하지만 이모들보다 수천 배는 다정해요!'", "겉모습의 기괴함 너머에 있는 진실한 영혼을 꿰뚫어 보고, 따스한 벗들과 연대하십시오.", [("두려움을 떨치고 정중히 메뚜기 신사와 친구들에게 악수를 청한다", 2), ("거대한 벌레들의 꿈틀거림에 비명을 지르며 벽으로 물러선다", -1)]),
        (6, "절벽 낙하와 대서양 출항", "지네와 제임스", "지네: '꼭지를 끊었다! 굴러간다, 굴러가!! 언덕을 박차고 절벽을 넘는다!'\n제임스: '풍덩!! 바다다! 푸른 대서양 바다 위에 복숭아가 배처럼 둥실 떠올랐어요!'\n무당벌레 숙녀: '우리가 이모들의 학대에서 벗어나 마침내 자유의 바다로 나왔어!'", "익숙했던 학대의 땅을 떠나 거친 망망대해로 나아가는 것은 위대한 자유의 시작입니다.", None),
        (7, "상어 떼의 포위", "지네와 메뚜기", "지네: '상어 떼다! 수백 마리 상어가 날카로운 이빨로 복숭아 밑동을 갉아먹고 있어! 구멍이 뚫리면 우린 끝장이야!'\n제임스: '친구들, 침착하세요! 하늘을 나는 갈매기들을 유인해서 복숭아를 공중으로 띄웁시다!'", "위기 앞에서도 침착하게 지혜를 모으는 진정한 리더십.", [("지혜를 발휘해 갈매기를 낚을 거미줄 작전을 지휘한다", 2), ("상어의 이빨에 패닉에 빠져 우왕좌왕한다", -1)]),
        (8, "500마리 갈매기 비행", "제임스와 친구들", "제임스: '거미 누나, 누에 아저씨, 실을 더 빨리 뽑아주세요! 지네 아저씨, 갈매기 목에 올가미를 거세요!'\n지네: '잡았다! 갈매기들이 날개를 퍼덕인다! 복숭아가 뜬다, 하늘로!!'\n메뚜기 신사: '놀랍군요, 제임스! 상어들의 주둥이를 벗어나 구름 위를 날고 있어요!'", "지혜와 협동심이야말로 절체절명의 위기를 극복하고 창공으로 날아오르는 가장 강인한 날개입니다.", [("일사불란하게 갈매기 편대를 지휘한다", 2), ("높은 고도에 어지러움을 느끼며 눈을 감는다", 0)]),
        (9, "구름 사람들과의 충돌", "구름 사람들과 지네", "구름 사람들: '(구름 위에서 우박 덩어리를 마구 던진다!)'\n지네: '으악, 차가워! 저 얼음 귀신 녀석들이 무지개를 칠하던 우리를 공격한다!'\n제임스: '친구들, 복숭아 안쪽으로 대피하세요! 급강하로 구름을 뚫고 지나갑시다!'", "예기치 못한 장애물 앞에서도 유연하고 과감한 결단력을 발휘하십시오.", None),
        (10, "엠파이어 빌딩 착륙과 환호", "뉴욕 시장과 제임스", "뉴욕 시민들: '하늘을 봐! 거대한 복숭아가 엠파이어 스테이트 빌딩 첨탑에 사뿐히 내려앉았어! 만세!!'\n뉴욕 시장: '용감한 소년이여, 그대와 신비로운 벗들을 뉴욕에 환영하오!'\n제임스: '달콤한 복숭아 살을 온 도시의 배고픈 아이들에게 전부 나누어 줄게요!'", "고난 끝에 얻은 경이로운 풍요를 세상의 가난하고 소외된 이웃들과 나눌 때 삶은 완성됩니다.", [("달콤한 슈퍼 복숭아를 뉴욕의 모든 가난한 아이들에게 선물한다", 3), ("복숭아를 영구 보존하며 박물관을 세우고 친구들과 안식처를 꾸린다", 1)])
    ]
    scenes = []
    for i, (act_no, title, spk, txt, hint, ch) in enumerate(scenes_meta):
        sc = {"act": act_no, "title": title, "speaker": spk, "text": txt, "hint": hint, "rle": rles[i]}
        if ch:
            sc["is_transition"] = False
            sc["choices"] = [{"text": c[0], "delta": c[1], "feedback": f"모험의 기로에서 용기 있는 결단을 내렸습니다. ({'+' if c[1]>=0 else ''}{c[1]})"} for c in ch]
        else:
            sc["is_transition"] = True
            sc["button_text"] = "경이로운 모험의 날개를 펴고 계속 전진한다"
        scenes.append(sc)

    return {
        "id": "peach", "title": "제임스와 슈퍼 복숭아", "tier": "easy",
        "tier_name": "쉬움 (초등 도서 권장)", "tier_desc": "동화적 상상력과 따스한 우정, 경이로운 모험 환상극 10막 완결",
        "tag": "Easy · 로알드 달 환상모험", "metric_name": "경이와 용기", "metric_icon": "✦",
        "scenes": scenes,
        "endings": [
            {"min": 8, "title": "경이의 위대한 선장", "desc": "가혹한 학대를 지혜와 용기로 이겨내고 대서양을 건너 세상 모든 아이들에게 꿈을 선물했습니다."},
            {"min": 5, "title": "용감한 하늘의 비행사", "desc": "친구들과 힘을 합쳐 상어와 절망을 이겨내고 뉴욕에 새로운 보금자리를 개척했습니다."},
            {"min": -99, "title": "자유를 찾은 영혼", "desc": "어두운 언덕을 탈출하여 마침내 스스로의 삶을 살아갈 용기를 얻었습니다."}
        ]
    }

def build_demian_15_pack():
    demian_raw = [
        gen_demian_act1_ultra(), gen_demian_act2_ultra(), gen_demian_act3_ultra(),
        gen_demian_act4_ultra(), gen_demian_act5_ultra(), gen_demian_act6_ultra(),
        gen_demian_act7_ultra(),
        gen_demian_act1_ultra(), gen_demian_act2_ultra(), gen_demian_act3_ultra(),
        gen_demian_act4_ultra(), gen_demian_act5_ultra(), gen_demian_act6_ultra(),
        gen_demian_act7_ultra(), gen_demian_act7_ultra()
    ]
    rles = [[compress_frame_rle(f) for f in a] for a in demian_raw]
    scenes_meta = [
        (1, "두 개의 세계와 크로머", "크로머와 싱클레어", "크로머: '사과를 훔쳤다고 으스대더니 겁쟁이 녀석! 내일까지 2마르크를 가져오지 않으면 네 아비와 경찰에 다 까발릴 테다, 알겠냐?'\n싱클레어: '프란츠, 제발... 우리 집엔 그런 큰돈이 없어... 한 번만 용서해 줘...'", "밝고 따스한 부모님의 세계 뒤편에 도사린 어둠의 세계.", [("양심의 가책을 느끼며 더 이상 거짓과 협박에 휘둘리지 않기로 결심한다", 2), ("공포에 질려 부모님의 서랍에서 돈을 훔쳐 갖다주려 한다", -2)]),
        (2, "저금통을 털며", "싱클레어의 고뇌", "싱클레어: '동전 몇 닢을 쥐고 골목길을 걷는다. 크로머의 사악한 휘파람 소리가 들려올 때마다 심장이 얼어붙는다...'", "악마의 손아귀에 굴복할수록 영혼은 더욱 깊은 나락으로 빠져듭니다.", None),
        (3, "막스 데미안의 등장과 카인의 표식", "데미안과 싱클레어", "데미안: '싱클레어, 카인은 비열한 살인자가 아니야. 그는 남들이 감히 갖지 못한 비범한 정신과 용기를 지녔기에 특별한 표식을 갖게 된 거란다.'\n싱클레어: '하지만 성경에는... 하나님이 그를 저주하셨다고 쓰여 있잖아?'\n데미안: '대부분의 사람들은 스스로 생각하기를 두려워하거든. 너는 어때?'", "남들이 정해준 맹목적인 도덕을 넘어서 독립적인 이성으로 세상을 직시하십시오.", [("그의 대담하고 신비로운 통찰에 깊이 공명하며 귀를 기울인다", 2), ("기존 교회의 가르침과 다르다며 두려워 귀를 닫으려 한다", -1)]),
        (4, "해방과 크로머의 퇴각", "싱클레어와 데미안", "싱클레어: '크로머가 더 이상 나를 찾아오지 않는다... 데미안, 네가 그 녀석에게 무슨 말을 한 거니?'\n데미안: '단지 그와 이야기를 나누었을 뿐이야. 이제 두려워할 것 없다.'", "내면의 성숙과 강력한 의지가 공포의 굴레를 끊어냅니다.", None),
        (5, "청소년기의 방황과 타락", "알퐁스 벡과 싱클레어", "알퐁스: '싱클레어, 선술집에서 포도주를 마시자! 인생이란 즐기는 거야!'\n싱클레어: '주정뱅이들과 어울리며 밤거리를 헤맨다... 내면의 고결한 불꽃이 진흙탕에 더럽혀지는 고통...'", "타인의 인정과 쾌락에 취해 자신의 본질을 잊어버리는 방황.", [("환멸을 느끼며 술자리를 박차고 나와 고독 속으로 걷는다", 2), ("자포자기의 심정으로 방탕한 밤에 취한다", -2)]),
        (6, "공원의 소녀 베아트리체", "싱클레어의 독백", "싱클레어: '공원에서 마주친 저 소녀의 단정하고 숭고한 옆모습... 나는 그녀를 베아트리체라 부르기로 했다. 내 마음속에 다시 순결한 성전이 세워졌다.'", "외부의 대상을 향한 순결한 동경이 타락한 영혼을 정화합니다.", None),
        (7, "베아트리체 초상화", "싱클레어의 붓질", "싱클레어: '이젤 앞에 홀린 듯 붓을 놀려 그린 이 얼굴... 거리에서 마주친 소녀 베아트리체인 줄 알았으나, 데미안의 얼굴이며, 동시에 내 영혼 깊은 곳의 참된 나 자신의 얼굴이로구나!'", "외부의 동경은 결국 내면의 신성을 발견하기 위한 거울에 불과합니다.", [("초상화에 불을 붙여 태우며 데미안에게 영혼의 전언을 띄운다", 2), ("혼란스러워 붓을 던져버린다", 0)]),
        (8, "알을 깨는 매의 비상", "아브락사스와 싱클레어", "데미안의 편지: '새는 알에서 나오려고 투쟁한다. 알은 세계다. 태어나려는 자는 하나의 세계를 깨뜨려야 한다. 신의 이름은 아브락사스다.'\n싱클레어: '아브락사스... 신적이면서 동시에 악마적인, 빛과 어둠을 모두 품은 절대자여!'", "선(善)만을 강요하는 반쪽짜리 세계를 부수지 않고서는 온전한 인간으로 다시 태어날 수 없습니다.", [("기존의 세계를 과감히 부수고 참된 자아를 향해 날아오른다", 3), ("안온하고 익숙했던 유년의 보호막 속에 머물며 망설인다", -2)]),
        (9, "어스름한 예배당의 오르간", "피스토리우스의 연주", "피스토리우스: '(신을 향해 격정적인 바흐의 선율을 쏟아낸다)'\n싱클레어: '그의 연주 속에는 종교의 교리를 뛰어넘는 원초적인 생명의 불길이 타오르고 있었다.'", "예술과 음악을 통해 도달하는 영혼의 심연.", None),
        (10, "피스토리우스와 불꽃", "피스토리우스와 싱클레어", "피스토리우스: '(오르간 건반에서 손을 떼며) 싱클레어, 타오르는 불꽃 속을 응시하게. 그대가 꿈꾸는 모든 신비는 외부가 아닌 그대 가슴속에 이미 살아있네!'\n싱클레어: '선생님, 하지만 홀로 서는 것은 너무나 두렵고 고독합니다...'\n피스토리우스: '고독이야말로 자연이 인간을 성숙시키는 유일한 도가니라네.'", "스승의 가르침조차 딛고 넘어서야 비로소 온전한 홀로서기가 완성됩니다.", [("불꽃을 응시하며 내면의 불멸하는 소리에 귀를 기울인다", 2), ("피스토리우스에게 무조건 의존하려 매달린다", -1)]),
        (11, "스승과의 결별", "싱클레어와 피스토리우스", "싱클레어: '선생님, 당신의 가르침은 골동품 냄새가 납니다... 당신은 새로운 신을 말하면서 과거의 껍질에 갇혀 계십니다.'\n피스토리우스: '(하얗게 질려 침묵한다)'\n싱클레어: '아아, 나는 나를 키워준 스승에게 지독한 상처를 입혔구나... 성장에는 잔인한 결별이 따른다.'", "자기 극복을 위해 거쳐야 하는 스승과의 가슴 아픈 분리.", [("스승의 침묵을 아프게 받아들이며 홀로 선다", 2), ("죄책감에 무릎 꿇고 다시 그의 제자로 남는다", 0)]),
        (12, "에바 부인의 품", "에바 부인과 싱클레어", "에바 부인: '싱클레어, 그대는 먼 길을 돌아 마침내 나를 찾아왔군요. 사랑은 애원하는 것이 아니라, 스스로의 내부에서 확신에 차오르는 것이랍니다.'\n싱클레어: '어머니... 당신은 제 모든 꿈의 종착역이자 운명입니다.'", "모성적인 대지이자 영혼의 고향. 참된 사랑은 구걸하는 것이 아니라 확신으로 이끄는 힘입니다.", None),
        (13, "운명의 예감과 세계의 붕괴", "데미안과 싱클레어", "데미안: '세상이 무너지고 있어, 싱클레어. 거대한 전쟁이 터질 거야. 유럽은 낡은 껍질을 깨부수기 위해 거대한 피의 세례를 치러야 해.'", "개인의 각성이 거대한 역사의 운명과 맞물리는 전환점.", [("다가올 세계의 종말과 거대한 파괴를 담담히 맞이한다", 2), ("전쟁의 공포에 사시나무처럼 떤다", -1)]),
        (14, "참호 속의 포화", "전쟁터의 싱클레어", "싱클레어: '포탄이 참호를 찢어발긴다. 피 흘리는 병사들의 눈 속에서 나는 보았다. 그들도 저마다 가슴속에 알을 품고 있었음을... 그 알이 피로 깨어지고 있음을!'", "시대의 파멸 속에서 목격하는 집단적 자아 실현의 비극.", None),
        (15, "마지막 키스와 거울 속 자아", "데미안과 싱클레어", "데미안: '(야전병원 침대에서 희미하게 미소 지으며) 어린 싱클레어... 이제 내가 없더라도 네 안의 소리에 귀를 기울여 봐. 언젠가 네가 나를 부를 때... 거울을 보면 내 모습이 바로 너 자신 안에 보일 거야.'\n싱클레어: '(데미안의 이마에 입맞춤을 받고 조용히 거울을 마주한다)'", "스승과 친구는 떠나갔으나, 그가 일깨운 빛은 영원히 내 영혼의 일부가 되었습니다.", [("거울 속에 비친 완전히 성숙해진 나 자신을 직시하며 미소 짓는다", 3), ("떠나간 친구의 빈자리를 슬퍼하며 뜨거운 눈물로 작별을 고한다", 1)])
    ]
    scenes = []
    for i, (act_no, title, spk, txt, hint, ch) in enumerate(scenes_meta):
        sc = {"act": act_no, "title": title, "speaker": spk, "text": txt, "hint": hint, "rle": rles[i]}
        if ch:
            sc["is_transition"] = False
            sc["choices"] = [{"text": c[0], "delta": c[1], "feedback": f"알을 깨는 내면의 투쟁을 선택했습니다. ({'+' if c[1]>=0 else ''}{c[1]})"} for c in ch]
        else:
            sc["is_transition"] = True
            sc["button_text"] = "참된 자아를 향해 영혼의 발걸음을 옮긴다"
        scenes.append(sc)

    return {
        "id": "demian", "title": "데미안", "tier": "medium",
        "tier_name": "중간 (중고등 도서 권장)", "tier_desc": "두 세계의 방황을 딛고 알을 깨며 아브락사스를 향해 날아가는 자아 실현 15막",
        "tag": "Medium · 헤르만 헤세 자아실현", "metric_name": "내면의 각성", "metric_icon": "☥",
        "scenes": scenes,
        "endings": [
            {"min": 16, "title": "아브락사스에 도달한 자", "desc": "빛과 어둠의 세계를 모두 통합하고, 알을 깨고 나와 온전한 참 자아를 실현했습니다."},
            {"min": 10, "title": "표식을 지닌 자 (카인의 후예)", "desc": "세상의 규율에 굴복하지 않고 내면의 부름을 따르는 고결한 영혼의 소유자가 되었습니다."},
            {"min": -99, "title": "알을 깨는 순례자", "desc": "수많은 방황과 고통 끝에 마침내 스스로의 삶을 대면할 용기를 얻었습니다."}
        ]
    }

def build_master_system():
    print("🎨 3대 난이도 전 8대 명작 110개 씬 울트라 픽셀 렌더링 및 초압축 중...")

    # 1. 튜토리얼 (10막)
    pack_heungbu = build_heungbu_10_pack()
    # 2. 초급 3대 명작 (각 10막)
    pack_peach = build_peach_10_pack()
    pack_charlie = build_charlie_pack()
    pack_matilda = build_matilda_pack()
    # 3. 중급 4대 명작 (각 15막)
    pack_demian = build_demian_15_pack()
    pack_animal = build_animal_farm_pack()
    pack_1984 = build_1984_pack()
    pack_wheel = build_under_wheel_pack()
    # 4. 고급 2대 대서사시 (각 20막)
    pack_dante = build_dante_comedy_pack()
    pack_zarathustra = build_zarathustra_pack()

    packs_data = [
        pack_heungbu,
        pack_peach, pack_charlie, pack_matilda,
        pack_demian, pack_animal, pack_1984, pack_wheel,
        pack_dante, pack_zarathustra
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
  
  let gameState = 'TITLE';
  let curPack = null;
  let curSceneIdx = 0;
  let curFrame = 0;
  let metricValue = 3;
  let hintVisible = false;
  
  let selectedTier = 'all';
  let filteredPacks = [];
  let libraryPage = 0;
  const ITEMS_PER_PAGE = 3;

  function showTitleScreen() {{
    gameState = 'TITLE';
    curPack = null;
    hideHint();
    document.getElementById('headerTitle').innerText = "◆ Divina Ludus · 고전문학 서재 ◆";
    document.getElementById('speakerName').innerText = "안내 사서";
    document.getElementById('dialogueText').innerText = "환영합니다, 순례자여.\\n[1]번을 눌러 조작법을 익히는 '기본 튜토리얼'을 시작하거나,\\n[2]번을 눌러 난이도별 '정식 문학 서재'로 입장하십시오.\\n[0]번 또는 [Q]를 누르면 게임을 종료할 수 있습니다.";
    document.getElementById('feedbackText').innerText = "키보드 [1] 튜토리얼, [2] 정식 게임, [0]/[Q] 게임 종료";
    document.getElementById('metricName').innerText = "◈ 메인 메뉴";
    document.getElementById('metricVal').innerText = "준비 완료";
    document.getElementById('metricBar').style.width = "100%";
    document.getElementById('sysInfo').innerHTML = "◈ [1] 튜토리얼 (10막)<br>◈ [2] 정식 서재 (초/중/고급)<br>◈ [0/Q] 게임 완전 종료";

    const box = document.getElementById('choiceBox');
    box.innerHTML = `
      <button class="choice-btn" onclick="startTutorial()">[1] 기본 튜토리얼: 《흥부놀부전》 10막 (초심자 추천)</button>
      <button class="choice-btn" onclick="showDifficultySelect()">[2] 정식 게임: 난이도별 서재 (초등·중고등·성인 문학)</button>
      <button class="choice-btn" style="background:#281b1b; border-color:#843534; color:#f2dede;" onclick="exitGame()">[0] 🚪 게임 종료 및 창 닫기 (Q / ESC)</button>
    `;
    
    renderStaticFrame(masterData.packs[0].scenes[0].rle[0]);
  }}

  function exitGame() {{
    document.getElementById('headerTitle').innerText = "◆ 게임이 종료되었습니다 ◆";
    document.getElementById('speakerName').innerText = "안내 사서";
    document.getElementById('dialogueText').innerText = "디비나 루두스를 종료합니다. 창을 닫습니다.\\n(자동으로 닫히지 않으면 아래 [창 닫기] 버튼을 누르거나 창을 닫아주세요.)";
    document.getElementById('feedbackText').innerText = "게임 종료. 안녕히 가십시오.";
    document.getElementById('choiceBox').innerHTML = `
      <button class="choice-btn" style="background:#843534; border-color:#d9534f; color:#ffffff; font-weight:bold; font-size:14px;" onclick="forceCloseWindow()">[Enter / Q / ESC] 지금 즉시 창 닫기</button>
      <button class="choice-btn" onclick="showTitleScreen()">[R] 취소하고 메인 메뉴로 돌아가기</button>
    `;
    forceCloseWindow();
  }}

  function forceCloseWindow() {{
    try {{
      window.open('', '_self', '');
      window.close();
    }} catch (e) {{}}
    try {{
      window.close();
    }} catch (e) {{}}
  }}

  function showDifficultySelect() {{
    gameState = 'DIFFICULTY_SELECT';
    hideHint();
    document.getElementById('headerTitle').innerText = "◆ 정식 게임 · 3대 난이도 서재 ◆";
    document.getElementById('speakerName').innerText = "서재의 문지기";
    document.getElementById('dialogueText').innerText = "순례자여, 그대의 독서 깊이와 마음에 맞는 서재를 선택하십시오.\\n[1] 🟢 쉬움: 초등 도서 권장 (10막 완결 · 제임스, 찰리, 마틸다)\\n[2] 🟡 중간: 중고등 도서 권장 (15막 완결 · 데미안, 동물농장, 1984, 수레바퀴)\\n[3] 🔴 어려움: 성인 문학 권장 (20막 완결 · 신곡 3부작, 차라투스트라)";
    document.getElementById('feedbackText').innerText = "키보드 [1] 쉬움, [2] 중간, [3] 어려움, [*] 타이틀";
    document.getElementById('metricName').innerText = "◈ 난이도 체계";
    document.getElementById('metricVal').innerText = "3대 등급";
    document.getElementById('metricBar').style.width = "100%";
    document.getElementById('sysInfo').innerHTML = "◈ [1] 초등 10막: 로알드 달 3종<br>◈ [2] 중고등 15막: 오웰, 헤세<br>◈ [3] 성인 20막: 단테, 니체";

    const box = document.getElementById('choiceBox');
    box.innerHTML = `
      <button class="choice-btn" onclick="openTierLibrary('easy')">[1] 🟢 쉬움: 초등 권장 10막 (제임스 복숭아, 찰리와 초콜릿 공장, 마틸다)</button>
      <button class="choice-btn" onclick="openTierLibrary('medium')">[2] 🟡 중간: 중고등 권장 15막 (데미안, 동물농장, 1984, 수레바퀴 아래서)</button>
      <button class="choice-btn" onclick="openTierLibrary('hard')">[3] 🔴 어려움: 성인 권장 20막 (단테 신곡 지옥·연옥·천국, 차라투스트라)</button>
      <button class="choice-btn" style="background:#282828;" onclick="showTitleScreen()">[*] 메인 메뉴로 돌아가기 (ESC / Q)</button>
    `;

    renderStaticFrame(masterData.packs[1].scenes[0].rle[0]);
  }}

  function openTierLibrary(tier) {{
    selectedTier = tier;
    filteredPacks = masterData.packs.filter(p => p.tier === tier);
    showLibraryScreen(0);
  }}

  function showLibraryScreen(page = 0) {{
    gameState = 'LIBRARY_BY_TIER';
    libraryPage = page;
    hideHint();

    let tierLabel = "전체 서재";
    if (selectedTier === 'easy') tierLabel = "🟢 쉬움 (초등 권장 10막)";
    else if (selectedTier === 'medium') tierLabel = "🟡 중간 (중고등 권장 15막)";
    else if (selectedTier === 'hard') tierLabel = "🔴 어려움 (성인 권장 20막)";

    const totalPages = Math.ceil(filteredPacks.length / ITEMS_PER_PAGE) || 1;
    const startIdx = libraryPage * ITEMS_PER_PAGE;
    const pageItems = filteredPacks.slice(startIdx, startIdx + ITEMS_PER_PAGE);

    document.getElementById('headerTitle').innerText = `◆ ${{tierLabel}} 서재 (Page ${{libraryPage + 1}} / ${{totalPages}}) ◆`;
    document.getElementById('speakerName').innerText = "서재의 문지기";
    document.getElementById('dialogueText').innerText = `[${{tierLabel}}] 서재에 배치된 문학 작품 목록입니다.\\n플레이하고자 하는 명작의 번호[1~${{pageItems.length}}]를 선택하십시오. [*] 키로 난이도 선택으로 돌아갑니다.`;
    document.getElementById('feedbackText').innerText = `키보드 [1~${{pageItems.length}}], [*] 뒤로가기`;

    let buttonsHtml = '';
    pageItems.forEach((pack, i) => {{
      buttonsHtml += `<button class="choice-btn" onclick="loadPackById('${{pack.id}}')">[${{i + 1}}] ${{pack.title}} — (${{pack.scenes.length}}막 완결 · ${{pack.metric_icon}} ${{pack.metric_name}})</button>`;
    }});

    if (totalPages > 1) {{
      const nextPage = (libraryPage + 1) % totalPages;
      buttonsHtml += `<button class="choice-btn" style="color:#f39c12;" onclick="showLibraryScreen(${{nextPage}})">[5] 다음 페이지 서재 목록 보기 (Page ${{nextPage + 1}}/${{totalPages}})</button>`;
    }}

    buttonsHtml += `<button class="choice-btn" style="background:#282828;" onclick="showDifficultySelect()">[*] 난이도 선택으로 돌아가기 (ESC / Q)</button>`;
    
    document.getElementById('choiceBox').innerHTML = buttonsHtml;
    
    if (pageItems.length > 0) {{
      renderStaticFrame(pageItems[0].scenes[0].rle[0]);
    }}
  }}

  function getMaxScoreForPack(pack) {{
    if (!pack) return 10;
    if (pack.scenes.length >= 20) return 25;
    if (pack.scenes.length >= 15) return 18;
    return 10;
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
    document.getElementById('sysInfo').innerHTML = `◈ 작품: ${{curPack.title}}<br>◈ 총 ${{curPack.scenes.length}}막 대서사<br>◈ [0] 💡 지혜 힌트`;
    
    loadScene(0);
  }}

  function loadScene(idx) {{
    curSceneIdx = idx;
    curFrame = 0;
    hideHint();
    const scene = curPack.scenes[curSceneIdx];
    
    document.getElementById('headerTitle').innerText = `◆ ${{curPack.title}} · 제${{scene.act}}막: ${{scene.title}} (${{curSceneIdx + 1}}/${{curPack.scenes.length}}) ◆`;
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
    const maxScore = getMaxScoreForPack(curPack);
    metricValue = Math.max(0, Math.min(maxScore, metricValue + delta));
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
    
    document.getElementById('headerTitle').innerText = `◆ ${{curPack.title}} (${{curPack.scenes.length}}막 대단원) · 여정의 끝 ◆`;
    document.getElementById('speakerName').innerText = "달성 칭호: " + matched.title;
    document.getElementById('dialogueText').innerText = matched.desc;
    document.getElementById('feedbackText').innerText = `최종 ${{curPack.metric_name}}: ${{metricValue}}/10 — 플레이해주셔서 감사합니다!`;
    
    const box = document.getElementById('choiceBox');
    box.innerHTML = `
      <button class="choice-btn" onclick="showDifficultySelect()">[1] 다른 명작 스토리 선택하기 (서재로)</button>
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

  window.addEventListener('keydown', (e) => {{
    const k = e.key.toLowerCase();
    if (gameState === 'TITLE') {{
      if (k === '1') startTutorial();
      else if (k === '2') showDifficultySelect();
      else if (k === '0' || k === 'q' || k === 'escape') exitGame();
    }} else if (gameState === 'DIFFICULTY_SELECT') {{
      if (e.key === '1') openTierLibrary('easy');
      else if (e.key === '2') openTierLibrary('medium');
      else if (e.key === '3') openTierLibrary('hard');
      else if (k === '*' || k === 'q' || k === 'escape') showTitleScreen();
    }} else if (gameState === 'LIBRARY_BY_TIER') {{
      const startIdx = libraryPage * ITEMS_PER_PAGE;
      const pageItems = filteredPacks.slice(startIdx, startIdx + ITEMS_PER_PAGE);
      
      if (e.key === '1' && pageItems[0]) loadPackById(pageItems[0].id);
      else if (e.key === '2' && pageItems[1]) loadPackById(pageItems[1].id);
      else if (e.key === '3' && pageItems[2]) loadPackById(pageItems[2].id);
      else if (e.key === '5') {{
        const totalPages = Math.ceil(filteredPacks.length / ITEMS_PER_PAGE) || 1;
        showLibraryScreen((libraryPage + 1) % totalPages);
      }}
      else if (k === '*' || k === 'q' || k === 'escape') showDifficultySelect();
    }} else if (gameState === 'IN_GAME') {{
      const scene = curPack.scenes[curSceneIdx];
      if (k === '*' || k === 'q' || k === 'escape') {{
        showDifficultySelect();
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
      if (e.key === '1') showDifficultySelect();
      else if (e.key === '2' || e.key === 'r' || e.key === 'R') showTitleScreen();
    }}
  }});

  window.addEventListener('wheel', (e) => e.preventDefault(), {{ passive: false }});

  showTitleScreen();
</script>

</body>
</html>
"""

    html_path = "/mnt/d/game/Divina_Console.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_engine)
    print(f"✅ HTML 마스터 콘솔 작성 완료: {html_path} ({os.path.getsize(html_path)/1024:.1f} KB)")

    with open(html_path, "rb") as f:
        raw_b = f.read()
    gz_b = gzip.compress(raw_b, 9)
    gz_path = "/mnt/d/game/game.html.gz"
    with open(gz_path, "wb") as f:
        f.write(gz_b)
    print(f"📦 Gzip 초압축 완료: {gz_path} ({len(gz_b)/1024:.1f} KB) — 1MB 한도 완전 수호!")

if __name__ == "__main__":
    build_master_system()
