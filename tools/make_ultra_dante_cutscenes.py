#!/usr/bin/env python3
"""
tools/make_ultra_dante_cutscenes.py
단테 알리기에리 《신곡: 지옥편》 1~7막 정밀 픽셀 아트 제너레이터
- 단독 덩어리가 아닌 지옥의 층별 깊이감과 두 시인(단테 & 베르길리우스)의 드라마틱한 인터랙션 구도 100% 구현
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
# 1막: 어두운 숲, 가시덤불, 으르렁거리는 맹수들 & 베르길리우스의 구원
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act1_ultra():
    base = make_canvas()
    # 배경: 빛 한 점 없는 메마른 고목 숲 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_BG)
    for x in range(0, CANVAS_W, 14):
        fill_rect(base, x, 0, x+2, 110, C_LINE)
    fill_rect(base, 0, 110, CANVAS_W-1, 151, C_BROWN)

    # [좌측: 공포에 질려 주저앉은 단테 (Col 30~96)]
    fill_rect(base, 46, 36, 88, 70, C_RED) # 진홍빛 학자 두건
    fill_rect(base, 54, 46, 82, 82, C_SKIN) # 고뇌의 마른 얼굴
    fill_rect(base, 58, 54, 66, 57, C_LINE); base[55][62] = C_WHITE
    fill_rect(base, 72, 54, 80, 57, C_LINE); base[55][76] = C_WHITE
    fill_rect(base, 66, 58, 72, 70, C_SHADOW) # 날카로운 매부리코
    fill_rect(base, 36, 72, 98, 151, C_RED) # 진홍색 롱 로브

    # [중앙 아래: 으르렁거리는 늑대/표범 실루엣 (Col 110~154)]
    fill_rect(base, 116, 110, 154, 140, C_LINE)
    base[118][124] = C_RED; base[118][132] = C_RED # 번뜩이는 맹수의 붉은 눈

    # [우측: 성스러운 월계관과 지팡이의 스승 베르길리우스 (Col 176~250)]
    fill_rect(base, 186, 36, 224, 76, C_SKIN)
    fill_rect(base, 180, 28, 230, 42, C_WHITE) # 은빛 머리칼
    draw_circle(base, 205, 30, 18, 6, C_LIME) # 푸른 월계관!
    fill_rect(base, 192, 48, 200, 51, C_LINE); fill_rect(base, 210, 48, 218, 51, C_LINE) # 온화한 눈매
    fill_rect(base, 172, 72, 238, 151, C_WHITE) # 고대 로마 순백 토가
    # 맹수들을 가로막는 목자의 긴 지팡이 (Col 160~166, Row 40~151)
    fill_rect(base, 162, 40, 166, 151, C_BROWN)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 월계관 잎새 끝과 지팡이 다이아몬드 스파클(◆)
            fr[22][205] = C_WHITE; fill_rect(fr, 200, 28, 210, 30, C_WHITE); fr[34][205] = C_WHITE
            fr[34][164] = C_WHITE; fill_rect(fr, 160, 38, 168, 40, C_WHITE); fr[44][164] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 2막: 아케론 강, 카론의 핏빛 숯불 눈과 위압적인 노질 vs 나룻배의 단테
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act2_ultra():
    base = make_canvas()
    # 배경: 핏빛 붉은 안개와 피안의 절벽 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 70, C_LINE)
    fill_rect(base, 0, 70, CANVAS_W-1, 151, C_RED) # 끓는 아케론 강
    # 나룻배 (Col 30~260, Row 96~136)
    fill_rect(base, 30, 100, 260, 134, C_DARK_BROWN)

    # [좌측: 배 위에 탄 단테와 베르길리우스 (Col 40~110)]
    fill_rect(base, 50, 70, 76, 100, C_RED) # 단테
    fill_rect(base, 80, 56, 106, 100, C_WHITE) # 베르길리우스
    draw_circle(base, 93, 54, 10, 4, C_LIME)

    # [우측: 거인 늙은 뱃사공 카론 (Col 140~230)]
    fill_rect(base, 156, 26, 200, 70, C_SKIN)
    fill_rect(base, 150, 20, 206, 32, C_STEEL) # 산발한 잿빛 머리
    for y in range(66, 90): fill_rect(base, 164, y, 192, y, C_STEEL) # 턱수염
    # 이글거리는 붉은 숯불 눈!
    base[42][168] = C_RED; base[43][168] = C_RED
    base[42][184] = C_RED; base[43][184] = C_RED
    fill_rect(base, 140, 70, 216, 120, C_DARK_BROWN) # 누더기 가죽

    # 망령들을 위협하는 거대한 무쇠 노 (Col 110~130, Row 30~140)
    fill_rect(base, 120, 30, 126, 140, C_STEEL)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 무쇠 노를 치켜들고 내리치는 역동적 동세
        oar_x = 114 + (i % 3) * 8
        fill_rect(fr, oar_x, 30, oar_x + 6, 140, C_STEEL)
        if i == 2: # F3 카론의 두 눈에서 뿜어지는 핏빛 다이아몬드 스파클(◆)
            fr[38][168] = C_WHITE; fr[38][184] = C_WHITE
            fr[42][164] = C_RED; fr[42][188] = C_RED
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 4막: 불타는 석관 속에서 단테를 쏘아보는 오만한 파리나타
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act4_ultra():
    base = make_canvas()
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
    # [우측: 붉게 달아오른 돌 석관 (Col 110~260, Row 66~140)]
    fill_rect(base, 110, 70, 260, 140, C_STEEL)
    fill_rect(base, 120, 76, 250, 84, C_RED) # 석관 틈새 화염
    # 석관 속에서 허리를 꼿꼿이 세운 파리나타 장군 (Col 150~210, Row 20~76)
    fill_rect(base, 162, 22, 198, 64, C_SKIN)
    fill_rect(base, 168, 34, 176, 37, C_LINE); fill_rect(base, 184, 34, 192, 37, C_LINE) # 매서운 눈
    fill_rect(base, 176, 38, 184, 48, C_SHADOW)
    fill_rect(base, 146, 64, 214, 110, C_DARK_BROWN) # 갑주와 팔짱 낀 자세

    # [좌측: 석관을 바라보며 경의를 표하는 단테와 베르길리우스 (Col 30~90)]
    fill_rect(base, 36, 60, 64, 94, C_RED) # 단테
    fill_rect(base, 68, 50, 94, 94, C_WHITE) # 베르길리우스

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 석관 바닥에서 치솟는 불꽃들
        for x in range(120, 250, 12):
            fy = 46 + ((x + i * 8) % 20)
            fill_rect(fr, x, fy, x+6, 76, C_GOLD)
        if i == 2: # F3 파리나타 검자루 끝 불꽃 스파클(◆)
            fr[18][180] = C_WHITE; fill_rect(fr, 175, 22, 185, 24, C_WHITE); fr[28][180] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 5막: 펄펄 끓는 피의 강 플레게톤과 활을 당긴 켄타우로스 네소스
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act5_ultra():
    base = make_canvas()
    fill_rect(base, 0, 0, CANVAS_W-1, 60, C_LINE)
    # 펄펄 끓는 선홍색 핏빛 강물 (Row 60~151)
    fill_rect(base, 0, 60, CANVAS_W-1, 151, C_RED)
    for y in range(70, 152, 12):
        for x in range(0, 296, 20): fill_rect(base, x, y, x+8, y+2, C_GOLD) # 끓는 포말

    # 피의 강 속에서 절규하며 허우적대는 폭군들의 손들 (Col 20~140)
    for x in range(30, 130, 24):
        fill_rect(base, x, 84, x+4, 110, C_SHADOW)

    # [우측: 강둑에서 활시위를 팽팽히 당긴 반인반마 켄타우로스 네소스 (Col 160~270)]
    fill_rect(base, 190, 20, 230, 66, C_SKIN) # 인간 상반신
    fill_rect(base, 170, 66, 270, 126, C_BROWN) # 말의 몸통과 네 다리
    # 팽팽하게 당겨진 거대한 활 (Col 140~200, Row 24~60)
    fill_rect(base, 144, 24, 148, 64, C_STEEL) # 활대
    fill_rect(base, 148, 42, 196, 44, C_STEEL) # 화살

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 시위를 당긴 화살촉 끝 다이아몬드 스파클(◆)
            fr[36][144] = C_WHITE; fill_rect(fr, 140, 41, 148, 43, C_WHITE); fr[48][144] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 6막: 말레볼제 구덩이, 죄인을 칭칭 감고 물어뜯는 거대한 지옥 뱀
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act6_ultra():
    base = make_canvas()
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
    # [중앙: 고통에 몸부림치는 죄인과 거대한 청록색 지옥 뱀 (Col 110~190)]
    fill_rect(base, 134, 36, 168, 114, C_SKIN) # 죄인
    # 죄인을 칭칭 감은 거대한 뱀의 몸통 코일
    draw_circle(base, 150, 74, 38, 48, C_GREEN)
    draw_circle(base, 150, 74, 28, 38, C_LINE) # 뱀 비늘 명암
    # 뱀의 머리와 날카로운 독니 (Row 30~50, Col 160~184)
    draw_circle(base, 172, 38, 14, 12, C_GREEN)
    base[36][168] = C_RED # 붉은 뱀 눈
    fill_rect(base, 176, 42, 180, 48, C_WHITE) # 독니

    # [좌측: 절벽 위에서 직시하는 단테와 베르길리우스 (Col 20~76)]
    fill_rect(base, 24, 70, 48, 100, C_RED)
    fill_rect(base, 50, 60, 74, 100, C_WHITE)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        shift = 4 if i % 2 == 0 else -4
        draw_circle(fr, 150 + shift, 74, 40, 50, C_GREEN)
        if i == 2: # F3 뱀의 독니와 붉은 눈 다이아몬드 스파클(◆)
            fr[30][172] = C_WHITE; fill_rect(fr, 166, 35, 176, 37, C_WHITE); fr[42][172] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 7막: 얼음 지옥 코키토스 탈출과 밤하늘 은하수 & 별들의 찬가
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act7_ultra():
    base = make_canvas()
    # 배경: 벨벳 같은 칠흑의 밤하늘과 은하수 (Row 0~100)
    fill_rect(base, 0, 0, CANVAS_W-1, 100, C_LINE)
    # 총총히 박힌 수많은 별무리
    for sx in range(16, 286, 20):
        sy = (sx * 7) % 86
        base[sy][sx] = C_GOLD if sx % 2 == 0 else C_WHITE

    # 하단: 얼음 구멍을 빠져나온 지상 언덕 (Row 100~151)
    fill_rect(base, 0, 100, CANVAS_W-1, 151, C_DARK_BROWN)
    # 얼음 호수 코키토스의 푸른 균열
    for x in range(20, 280, 30): fill_rect(base, x, 130, x+8, 134, C_SKY)

    # [중앙: 밤하늘 별들을 우러러보는 두 시인의 벅찬 뒷모습 (Col 110~186)]
    # 단테 (진홍빛 두건과 로브 뒷모습)
    fill_rect(base, 120, 66, 146, 110, C_RED)
    fill_rect(base, 126, 56, 140, 66, C_RED)
    # 베르길리우스 (순백 토가와 푸른 월계관 뒷모습)
    fill_rect(base, 150, 58, 178, 110, C_WHITE)
    fill_rect(base, 156, 48, 172, 58, C_WHITE)
    draw_circle(base, 164, 48, 10, 4, C_LIME) # 월계관

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 북극성과 은하수 별빛 깜빡임
        for sx in range(16, 286, 40):
            sy = (sx * 7) % 86
            fr[sy][sx] = C_WHITE if (sx + i) % 2 == 0 else C_GOLD
        if i == 2: # F3 가장 찬란한 북극성 다이아몬드 스파클(◆)
            fr[10][210] = C_WHITE; fill_rect(fr, 204, 15, 216, 17, C_WHITE); fr[22][210] = C_WHITE
        frames.append(fr)
    return frames

print("Loaded ultra dante cutscenes successfully!")

# ─────────────────────────────────────────────────────────────────────────────
# 3막: 애욕의 폭풍 속 부유하는 파올로와 프란체스카 vs 단테
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act3_ultra():
    base = make_canvas()
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
    # [좌측: 지켜보는 단테와 베르길리우스]
    fill_rect(base, 20, 60, 50, 94, C_RED) # 단테 두건
    fill_rect(base, 24, 70, 46, 100, C_SKIN)
    fill_rect(base, 10, 94, 60, 151, C_RED)
    # 베르길리우스 토가와 월계관
    fill_rect(base, 50, 44, 80, 80, C_WHITE)
    draw_circle(base, 65, 42, 12, 5, C_LIME)
    fill_rect(base, 44, 80, 90, 151, C_WHITE)

    # [중앙-우측: 소용돌이 암흑 폭풍 속에서 서로를 껴안고 허공을 부유하는 두 연인]
    # 프란체스카 (순백의 얇은 옷)
    draw_circle(base, 160, 60, 16, 20, C_WHITE)
    draw_circle(base, 160, 46, 12, 12, C_SKIN)
    for y in range(40, 70): base[y][154] = C_DARK_BROWN # 흩날리는 긴 머리칼
    # 파올로 (푸른 옷으로 프란체스카를 감싸 안음)
    draw_circle(base, 180, 66, 18, 22, C_BLUE)
    draw_circle(base, 178, 50, 12, 12, C_SKIN)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 회오리바람 검은 선과 영혼들의 부유
        for y in range(20, 140, 18):
            bx = (y * 4 + i * 16) % CANVAS_W
            fill_rect(fr, bx, y, bx + 30, y + 2, C_SHADOW)
        if i == 2: # F3 연인의 눈물과 단테의 비탄 스파클
            fr[54][160] = C_WHITE; fill_rect(fr, 155, 57, 165, 59, C_WHITE); fr[64][160] = C_WHITE
            fr[72][46] = C_WHITE
        frames.append(fr)
    return frames
