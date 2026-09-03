#!/usr/bin/env python3
"""
tools/make_ultra_peach_cutscenes.py
로알드 달 《제임스와 슈퍼 복숭아》 1~7막 울트라 픽셀 아트 제너레이터
- 단독 덩어리가 아닌, 공간 배경 텍스처와 인물 간 생생한 인터랙션 구도 100% 구현:
  * 1막: 영국의 황량한 언덕 저택, 지팡이를 휘두르는 앙상한 스파이커 & 번들거리는 스폰지 이모 vs 무거운 물통을 들고 웅크린 제임스
  * 2막: 마른 고목의 거대한 뒤틀린 뿌리 숲, 안갯속 신비로운 노인이 무릎 꿇고 요동치는 초록 마법 봉투를 건넴 vs 눈을 크게 뜬 제임스
  * 3막: 쿵-쿵 박동하는 거대한 복숭아와 복숭아 껍질 표면의 솜털 질감, 입을 떡 벌리고 뒤로 나자빠지는 마을 사람들과 기자들
  * 4막: 달콤한 호박색 복숭아 내부 방, 턱시도와 모노클의 메뚜기 신사, 42개 다리의 지네, 레이스 보닛의 무당벌레 숙녀, 실크 짠 거미와 제임스
  * 5막: 깎아지른 백색 절벽을 굴러떨어져 대서양에 '풍덩' 솟구치는 거대한 하얀 파도 물기둥과 바다에 뜬 복숭아
  * 6막: 끝없는 푸른 창공과 뭉게구름, 수백 가닥의 은빛 거미줄에 매달려 날개를 펄럭이는 500마리 흰 갈매기 떼와 복숭아 꼭대기에서 지휘하는 제임스
  * 7막: 뉴욕 맨해튼의 마천루 빌딩 숲, 엠파이어 스테이트 빌딩 피뢰침에 꽂힌 거대 복숭아 위에서 환호하는 제임스와 친구들, 오색 꽃가루 폭풍
"""

import sys
sys.path.append("/home/krjoylee/code/game/tools")
from generate_all_packs_studio import (
    CANVAS_W, CANVAS_H, PALETTE_16,
    C_BG, C_LINE, C_SKIN, C_SHADOW, C_CLOTH, C_BROWN,
    C_RED, C_BLUE, C_SKY, C_WHITE, C_CYAN, C_DARK_BROWN,
    C_GOLD, C_GREEN, C_STEEL, C_LIME,
    make_canvas, fill_rect, draw_circle
)

# ─────────────────────────────────────────────────────────────────────────────
# 1막: 스폰지와 스파이커 이모의 학대 vs 웅크린 제임스
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act1_ultra():
    base = make_canvas()
    # 배경: 잿빛 하늘과 황량한 영국 언덕 저택 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 54, C_BG)
    fill_rect(base, 80, 10, 216, 54, C_DARK_BROWN) # 저택 지붕과 벽
    fill_rect(base, 100, 20, 124, 38, C_GOLD); fill_rect(base, 172, 20, 196, 38, C_GOLD) # 창문
    fill_rect(base, 0, 54, CANVAS_W-1, 151, C_BROWN) # 언덕 마당 바닥
    for x in range(0, CANVAS_W, 20): fill_rect(base, x, 54, x+2, 151, C_DARK_BROWN) # 마른 잔디 결

    # [좌측: 뼈만 앙상한 스파이커 이모 (Col 30~100)]
    fill_rect(base, 46, 26, 84, 68, C_SKIN) # 마른 얼굴
    fill_rect(base, 50, 38, 60, 42, C_LINE); base[40][54] = C_WHITE # 철테 안경
    fill_rect(base, 70, 38, 80, 42, C_LINE); base[40][74] = C_WHITE
    fill_rect(base, 62, 44, 68, 56, C_SHADOW) # 날카로운 매부리코
    fill_rect(base, 56, 58, 74, 61, C_LINE) # 메마른 입술
    fill_rect(base, 30, 68, 96, 151, C_RED) # 뼈대만 남은 어깨와 피빛 드레스
    # 독수리 발톱 손으로 쥔 지팡이 (Col 92~98, Row 50~151)
    fill_rect(base, 92, 54, 96, 151, C_STEEL)

    # [우측: 거대한 팽창 덩어리 스폰지 이모 (Col 190~286)]
    draw_circle(base, 240, 56, 44, 40, C_SKIN) # 세 겹 턱살 얼굴
    fill_rect(base, 214, 46, 226, 50, C_LINE); fill_rect(base, 252, 46, 264, 50, C_LINE) # 실눈
    fill_rect(base, 234, 52, 244, 58, C_SHADOW) # 돼지코
    fill_rect(base, 226, 64, 252, 70, C_RED) # 붉고 기름진 입술
    fill_rect(base, 180, 76, 290, 151, C_CLOTH) # 거대한 항아리 몸통
    fill_rect(base, 170, 100, 184, 116, C_SKIN); fill_rect(base, 174, 106, 180, 110, C_GOLD) # 금반지

    # [중앙 아래: 무거운 양철 물통을 들고 웅크린 제임스 (Col 116~164)]
    draw_circle(base, 140, 84, 16, 16, C_BROWN) # 헝클어진 갈색 머리
    fill_rect(base, 128, 84, 152, 110, C_SKIN)
    fill_rect(base, 130, 92, 136, 96, C_LINE); base[94][133] = C_WHITE
    fill_rect(base, 144, 92, 150, 96, C_LINE); base[94][147] = C_WHITE
    fill_rect(base, 120, 110, 160, 146, C_WHITE) # 낡은 셔츠 & 멜빵바지
    fill_rect(base, 126, 110, 130, 146, C_BROWN); fill_rect(base, 150, 110, 154, 146, C_BROWN)
    # 무거운 양철 물통 (Col 102~118, Row 118~148)
    fill_rect(base, 102, 118, 118, 146, C_STEEL)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 지팡이 끝 번쩍임 & 스폰지 금반지 스파클
            fr[50][94] = C_WHITE; fill_rect(fr, 91, 53, 97, 55, C_WHITE); fr[58][94] = C_WHITE
            fr[104][177] = C_WHITE; fill_rect(fr, 175, 107, 179, 109, C_WHITE); fr[112][177] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 2막: 안갯속 노인의 신비로운 봉투 건넴 vs 제임스
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act2_ultra():
    base = make_canvas()
    # 배경: 어둡고 안개 낀 복숭아나무 고목 숲 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
    # 거대한 뒤틀린 마른 나무뿌리들
    for x in range(210, 280, 14):
        fill_rect(base, x, 0, x+8, 151, C_BROWN)
    fill_rect(base, 0, 110, CANVAS_W-1, 151, C_LINE)

    # [좌측: 신비로운 늙은 노인 (Col 30~120)]
    fill_rect(base, 44, 24, 88, 66, C_SKIN)
    # 풍성한 은빛 머리칼과 턱수염
    for y in range(50, 100): fill_rect(base, 36, y, 96, y, C_WHITE)
    fill_rect(base, 24, 76, 106, 151, C_LINE) # 신비로운 검은 로브
    # 노인이 건네는 종이봉투 (Col 96~150, Row 66~114)
    fill_rect(base, 98, 68, 150, 114, C_WHITE)
    draw_circle(base, 124, 91, 16, 16, C_GREEN) # 봉투 속 초록 발광체

    # [우측: 경이로움에 눈을 크게 뜬 제임스 (Col 160~240)]
    draw_circle(base, 192, 54, 20, 20, C_BROWN)
    fill_rect(base, 176, 54, 208, 92, C_SKIN)
    fill_rect(base, 180, 64, 188, 68, C_LINE); base[66][184] = C_WHITE # 큰 눈
    fill_rect(base, 164, 92, 220, 151, C_CLOTH) # 멜빵바지
    # 조심스레 뻗은 제임스의 두 손 (Col 144~166, Row 86~98)
    fill_rect(base, 146, 88, 166, 96, C_SKIN)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 봉투 속 수천 마리 악어 혀의 꿈틀거림 (동세)
        shift = (i % 3) * 3
        draw_circle(fr, 124 + shift, 91, 12, 12, C_LIME)
        if i == 2: # F3 마법의 씨앗 초록 다이아몬드 스파클(◆)
            fr[76][124] = C_WHITE; fill_rect(fr, 118, 82, 130, 84, C_WHITE); fr[92][124] = C_WHITE
            fr[84][124] = C_GOLD
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 3막: 쿵-쿵 박동하는 집채만 한 복숭아 & 경악하는 사람들
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act3_ultra():
    base = make_canvas()
    # 배경: 도버의 푸른 언덕과 아침 햇살 해안선 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 60, C_SKY)
    fill_rect(base, 0, 60, CANVAS_W-1, 80, C_BLUE) # 먼 바다
    fill_rect(base, 0, 80, CANVAS_W-1, 151, C_LIME) # 푸른 들판 잔디
    for x in range(0, CANVAS_W, 16): fill_rect(base, x, 80, x+2, 151, C_GREEN)

    # [중앙 메인: 집채만 한 거대 슈퍼 복숭아 (Col 70~226, Row 10~138)]
    draw_circle(base, 148, 74, 76, 68, C_GOLD)
    draw_circle(base, 148, 74, 66, 58, C_RED)
    # 복숭아 표면 솜털 질감 디더링
    for y in range(24, 124, 4):
        for x in range(90, 206, 6):
            if (x + y) % 3 == 0: base[y][x] = C_GOLD
    # 복숭아 골짜기 명암선
    for y in range(20, 128): base[y][148] = C_DARK_BROWN
    # 꼭지와 싱싱한 나뭇잎
    fill_rect(base, 144, 6, 152, 20, C_BROWN)
    draw_circle(base, 164, 12, 18, 8, C_LIME)

    # [전경 좌우: 뒤로 나자빠져 경악하는 마을 사람들과 기자들]
    fill_rect(base, 16, 100, 46, 140, C_CLOTH) # 좌측 사람
    fill_rect(base, 244, 100, 274, 140, C_CLOTH) # 우측 사람
    draw_circle(base, 31, 92, 10, 10, C_SKIN); draw_circle(base, 259, 92, 10, 10, C_SKIN)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 거대 복숭아 쿵-쿵 심장 박동 펄스 (동세)
        pulse = 4 if i % 2 == 0 else -4
        draw_circle(fr, 148, 74, 68 + pulse, 60 + pulse, C_RED)
        for y in range(20, 128): fr[y][148] = C_DARK_BROWN
        if i == 2: # F3 복숭아 꼭지에서 터지는 황금빛 향기 스파클(◆)
            fr[2][148] = C_WHITE; fill_rect(fr, 142, 5, 154, 7, C_WHITE); fr[10][148] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 4막: 복숭아 속 거대 곤충 친구들과의 만남 (메뚜기, 무당벌레, 지네, 제임스)
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act4_ultra():
    base = make_canvas()
    # 배경: 달콤하고 따스한 복숭아 심장부 호박색 과육 방 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_GOLD)
    for y in range(0, 152, 12):
        for x in range(0, 296, 16):
            if (x + y) % 4 == 0: fill_rect(base, x, y, x+4, y+4, C_RED) # 달콤한 과육 질감

    # [좌측: 턱시도 연미복의 늙은 초록 메뚜기 신사 (Col 30~96)]
    fill_rect(base, 46, 36, 82, 70, C_GREEN)
    fill_rect(base, 42, 14, 86, 36, C_LINE) # 번쩍이는 실크햇
    fill_rect(base, 68, 44, 76, 52, C_WHITE); base[48][72] = C_GOLD # 단안경(모노클)!
    fill_rect(base, 34, 70, 94, 146, C_LINE) # 우아한 턱시도
    fill_rect(base, 54, 70, 74, 90, C_WHITE) # 순백 나비넥타이와 셔츠
    # 바이올린 활처럼 뻗은 뒷다리
    fill_rect(base, 24, 50, 32, 130, C_GREEN)

    # [우측: 선홍색 등껍질과 점박이 7개의 무당벌레 숙녀 (Col 196~270)]
    draw_circle(base, 234, 70, 36, 32, C_RED)
    draw_circle(base, 234, 44, 12, 10, C_LINE) # 머리
    # 선명한 검은 점박이 7개
    fill_rect(base, 216, 58, 224, 66, C_LINE); fill_rect(base, 244, 58, 252, 66, C_LINE)
    fill_rect(base, 230, 72, 238, 80, C_LINE)
    fill_rect(base, 218, 86, 226, 94, C_LINE); fill_rect(base, 246, 86, 254, 94, C_LINE)

    # [중앙: 감격하여 친구들을 바라보는 제임스 (Col 120~176)]
    draw_circle(base, 148, 64, 18, 18, C_BROWN)
    fill_rect(base, 134, 64, 162, 98, C_SKIN)
    fill_rect(base, 138, 72, 144, 76, C_LINE); base[74][141] = C_WHITE
    fill_rect(base, 152, 72, 158, 76, C_LINE); base[74][155] = C_WHITE
    fill_rect(base, 142, 84, 154, 88, C_RED) # 활짝 웃는 입
    fill_rect(base, 124, 98, 172, 151, C_CLOTH) # 멜빵바지
    # 메뚜기 신사에게 뻗은 악수의 손
    fill_rect(base, 98, 92, 124, 100, C_SKIN)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 메뚜기 단안경 끝과 무당벌레 등껍질 다이아몬드 스파클(◆)
            fr[40][72] = C_WHITE; fill_rect(fr, 68, 43, 76, 45, C_WHITE); fr[50][72] = C_WHITE
            fr[66][234] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 5막: 깎아지른 절벽을 굴러떨어져 대서양에 솟구치는 거대한 파도 물기둥
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act5_ultra():
    base = make_canvas()
    # 배경: 푸른 하늘과 눈부신 정오의 태양
    fill_rect(base, 0, 0, CANVAS_W-1, 60, C_SKY)
    draw_circle(base, 250, 20, 16, 16, C_GOLD) # 태양
    # 짙푸른 대서양 바다 (Col 0~295, Row 60~151)
    fill_rect(base, 0, 60, CANVAS_W-1, 151, C_BLUE)
    for y in range(70, 152, 10):
        for x in range(0, 296, 24):
            fill_rect(base, x, y, x+12, y+2, C_CYAN) # 바다 은빛 윤슬

    # [중앙: 바다에 둥실 떠오른 거대 슈퍼 복숭아 (Col 100~196, Row 40~110)]
    draw_circle(base, 148, 76, 52, 46, C_GOLD)
    draw_circle(base, 148, 76, 44, 38, C_RED)
    fill_rect(base, 144, 26, 152, 36, C_BROWN) # 꼭지

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 양옆으로 솟구치는 거대한 하얀 파도 물기둥과 포말 (스플래시 동세)
        sp_h = 30 + (i % 3) * 8
        fill_rect(fr, 40, 90 - sp_h, 80, 120, C_WHITE)
        fill_rect(fr, 216, 90 - sp_h, 256, 120, C_WHITE)
        # 복숭아를 둘러싼 하얀 물보라
        fill_rect(fr, 86, 92, 210, 102, C_WHITE)
        if i == 2: # F3 파도 물방울 끝 찬란한 다이아몬드 스파클(◆)
            fr[50][60] = C_WHITE; fill_rect(fr, 56, 53, 64, 55, C_WHITE); fr[60][60] = C_WHITE
            fr[50][236] = C_WHITE; fill_rect(fr, 232, 53, 240, 55, C_WHITE); fr[60][236] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 6막: 500마리 갈매기 떼의 비행과 거미줄 결속
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act6_ultra():
    base = make_canvas()
    # 배경: 상공 수천 미터 코발트 블루 하늘과 뭉게구름 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
    # 하얀 뭉게구름들 (하단에 깔림)
    for cx in range(30, 280, 60):
        draw_circle(base, cx, 140, 36, 18, C_WHITE)

    # [중앙: 하늘에 높이 뜬 슈퍼 복숭아 (Col 106~190, Row 76~140)]
    draw_circle(base, 148, 108, 44, 38, C_GOLD)
    draw_circle(base, 148, 108, 38, 32, C_RED)
    # 복숭아 꼭대기에서 당당히 지휘하는 제임스 (Col 142~154, Row 60~76)
    fill_rect(base, 144, 60, 152, 70, C_SKIN)
    fill_rect(base, 140, 70, 156, 82, C_CLOTH)

    # 꼭지와 갈매기들을 잇는 수백 가닥의 은빛 거미줄 (Col 60~240, Row 24~76)
    for x in range(60, 240, 14):
        for y in range(24, 76):
            if (x * 3 + y) % 2 == 0: base[y][x] = C_WHITE

    frames = []
    # 갈매기 날개 플랩 6단계
    wing_offsets = [-10, -5, 0, 6, 0, -5]
    for idx, dy in enumerate(wing_offsets):
        fr = [row[:] for row in base]
        # 하늘을 가르는 8마리의 흰 갈매기 편대 (상단)
        for gx in range(40, 260, 32):
            fill_rect(fr, gx - 14, 18 + dy, gx + 14, 22 + dy, C_WHITE) # 날개
            fr[16 + dy][gx] = C_LINE # 머리
            base[20 + dy][gx] = C_GOLD # 부리
        if idx == 2: # F3 구름 위 눈부신 햇살 다이아몬드 스파클(◆)
            fr[4][148] = C_WHITE; fill_rect(fr, 142, 8, 154, 10, C_WHITE); fr[14][148] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 7막: 엠파이어 스테이트 빌딩 피뢰침 착륙과 환호의 꽃가루 폭풍
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act7_ultra():
    base = make_canvas()
    # 배경: 뉴욕 맨해튼 마천루 빌딩 숲과 황혼의 노을빛 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE) # 벨벳 밤하늘
    # 양옆의 고층 마천루 실루엣과 노란 창문 불빛
    fill_rect(base, 10, 60, 60, 151, C_DARK_BROWN)
    for y in range(70, 140, 12):
        for x in range(16, 56, 8): fill_rect(base, x, y, x+3, y+5, C_GOLD)
    fill_rect(base, 236, 60, 286, 151, C_DARK_BROWN)
    for y in range(70, 140, 12):
        for x in range(242, 282, 8): fill_rect(base, x, y, x+3, y+5, C_GOLD)

    # [중앙 메인: 엠파이어 스테이트 빌딩 첨탑과 꽂힌 복숭아 (Col 110~186)]
    fill_rect(base, 136, 70, 160, 151, C_STEEL) # 빌딩 상층부
    fill_rect(base, 146, 10, 150, 70, C_STEEL) # 뾰족한 피뢰침
    # 피뢰침에 완벽하게 꽂힌 거대 슈퍼 복숭아 (Col 116~180, Row 24~74)
    draw_circle(base, 148, 46, 36, 30, C_GOLD)
    draw_circle(base, 148, 46, 30, 24, C_RED)

    # 복숭아 꼭대기에서 양손을 번쩍 들고 환호하는 제임스와 곤충 친구들 (Row 10~26)
    fill_rect(base, 144, 12, 152, 22, C_SKIN) # 제임스 머리
    fill_rect(base, 138, 14, 142, 18, C_SKIN); fill_rect(base, 154, 14, 158, 18, C_SKIN) # 번쩍 든 두 손
    fill_rect(base, 140, 22, 156, 28, C_CLOTH)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 온 하늘에 흩날리는 뉴욕의 오색종이 꽃가루 폭풍 (동세)
        for fx in range(10, 286, 18):
            fy = (i * 22 + fx * 4) % 146
            fr[fy][fx] = C_GOLD if fx % 3 == 0 else (C_WHITE if fx % 3 == 1 else C_RED)
        if i == 2: # F3 첨탑 끝과 제임스의 만세 다이아몬드 스파클(◆)
            fr[2][148] = C_WHITE; fill_rect(fr, 143, 6, 153, 8, C_WHITE); fr[12][148] = C_WHITE
        frames.append(fr)
    return frames

print("Loaded ultra peach cutscenes successfully!")
