#!/usr/bin/env python3
"""
tools/make_ultra_demian_cutscenes.py
헤르만 헤세 《데미안》 1~7막 정밀 픽셀 아트 제너레이터
- 단독 덩어리가 아닌 원작 1:1 대화 구도:
  * 1막: 골목길 가스등, 크로머(사악한 뱁새눈, 주머니칼을 들이댐) vs 싱클레어(겁에 질려 눈물 흘리며 벽에 밀려남)
  * 2막: 학교 교정 플라타너스 나무, 데미안(석고상 마스크, 깊은 눈빛, 이마의 카인 표식 황금빛 발광)과 나란히 선 싱클레어
  * 3막: 촛불 밝힌 방, 이젤 위의 베아트리체 초상화(데미안과 싱클레어가 겹쳐진 기묘한 얼굴)를 바라보며 붓을 쥔 싱클레어
  * 4막: 거대한 알을 박차고 날아오르는 아브락사스(푸른 깃털과 황금빛 날개, 날카로운 눈, 튀어오르는 알껍데기)
  * 5막: 어두운 성당의 거대한 파이프오르간(금속 파이프 숲) 앞에서 격정적으로 연주하는 피스토리우스와 벽난로 불꽃을 응시하는 싱클레어
  * 6막: 따뜻한 벨벳 응접실, 자애로운 여신 에바 부인이 무릎 꿇은 싱클레어의 이마를 부드럽게 감싸 쥠 (푸른 사파이어 목걸이)
  * 7막: 1차 대전 야전병원, 피 묻은 침대에 나란히 누운 두 소년, 데미안이 싱클레어에게 속삭이며 거울 속 자아를 가리킴
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
# 1막: 크로머의 주머니칼 협박 vs 벽에 밀린 싱클레어
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act1_ultra():
    base = make_canvas()
    # 배경: 어두운 골목길 벽돌벽 디더링 (Col 0~295, Row 0~151)
    for y in range(0, 152, 8):
        for x in range(0, 296, 16):
            ox = 8 if (y//8)%2 == 1 else 0
            fill_rect(base, x+ox, y, x+ox+14, y+6, C_DARK_BROWN)
    # 가스등 기둥과 빛 (우측 상단)
    fill_rect(base, 250, 0, 254, 70, C_LINE)
    draw_circle(base, 252, 25, 16, 16, C_GOLD)
    draw_circle(base, 252, 25, 8, 8, C_WHITE)

    # [좌측: 불량배 프란츠 크로머 (Col 40~120)]
    # 삐딱한 헌팅캡 모자
    fill_rect(base, 50, 30, 110, 42, C_LINE)
    fill_rect(base, 42, 40, 118, 46, C_LINE)
    # 얼굴 윤곽 및 턱선
    fill_rect(base, 54, 44, 106, 92, C_SKIN)
    fill_rect(base, 54, 76, 62, 92, C_SHADOW); fill_rect(base, 98, 76, 106, 92, C_SHADOW)
    # 찢어진 뱁새눈 & 비열한 눈썹
    fill_rect(base, 62, 52, 74, 55, C_LINE); fill_rect(base, 86, 52, 98, 55, C_LINE)
    base[57][68] = C_LINE; base[57][92] = C_LINE
    # 삐뚤어진 코와 비열한 조소
    fill_rect(base, 76, 58, 82, 72, C_SHADOW)
    fill_rect(base, 70, 78, 92, 82, C_LINE); base[79][84] = C_WHITE # 뻐드렁니
    # 낡은 가죽 자켓
    fill_rect(base, 34, 92, 126, 151, C_LINE)
    # 뻗은 오른손과 주머니칼 (Col 100~160, Row 84~100)
    fill_rect(base, 104, 88, 128, 98, C_SKIN) # 손
    fill_rect(base, 128, 90, 142, 96, C_BROWN) # 손잡이
    fill_rect(base, 142, 92, 162, 95, C_STEEL) # 서슬 퍼런 칼날

    # [우측: 공포에 질려 벽에 밀린 어린 싱클레어 (Col 170~240)]
    # 부드러운 갈색 도련님 머리칼
    draw_circle(base, 205, 46, 26, 18, C_BROWN)
    # 하얗게 질린 얼굴
    fill_rect(base, 186, 48, 224, 94, C_SKIN)
    fill_rect(base, 186, 78, 192, 94, C_SHADOW); fill_rect(base, 218, 78, 224, 94, C_SHADOW)
    # 공포로 부릅뜬 큰 눈망울 & 처진 눈썹
    fill_rect(base, 190, 56, 198, 58, C_LINE); fill_rect(base, 212, 56, 220, 58, C_LINE)
    draw_circle(base, 194, 66, 4, 5, C_WHITE); base[66][194] = C_LINE
    draw_circle(base, 216, 66, 4, 5, C_WHITE); base[66][216] = C_LINE
    # 뺨을 타고 흐르는 식은땀과 눈물 (Col 218, Row 72~86)
    fill_rect(base, 218, 72, 220, 84, C_SKY); base[78][219] = C_WHITE
    # 바들바들 떠는 작은 입
    fill_rect(base, 200, 82, 210, 85, C_LINE)
    # 단정한 부르주아 소년 옷과 저금통 쥔 손
    fill_rect(base, 172, 94, 238, 151, C_BLUE) # 셔츠
    fill_rect(base, 184, 94, 226, 151, C_CLOTH) # 조끼
    fill_rect(base, 176, 110, 194, 128, C_SKIN) # 가슴 쥔 떨리는 손

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 크로머 칼날의 서늘한 떨림
        if i % 2 == 1:
            fill_rect(fr, 142, 91, 163, 94, C_WHITE)
        if i == 2: # F3 칼날 끝 번뜩임 & 싱클레어 눈물 스파클
            fr[88][162] = C_WHITE; fill_rect(fr, 159, 91, 165, 93, C_WHITE); fr[96][162] = C_WHITE
            fr[82][219] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 2막: 막스 데미안의 석고상 마스크 & 카인의 표식 vs 싱클레어
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act2_ultra():
    base = make_canvas()
    # 배경: 학교 교정의 등나무와 햇살 (밝은 녹음과 그늘)
    fill_rect(base, 0, 0, CANVAS_W-1, 60, C_LIME)
    for x in range(0, CANVAS_W, 30):
        fill_rect(base, x, 0, x+12, 80, C_GREEN)
    fill_rect(base, 0, 80, CANVAS_W-1, 151, C_BROWN) # 벤치와 흙길

    # [좌측: 신비로운 소년 막스 데미안 (Col 50~130)]
    # 단정하게 정돈된 흑갈색 머리칼
    fill_rect(base, 66, 24, 114, 40, C_LINE)
    # 고대 그리스 조각상 같은 서늘하고 완벽한 마스크
    fill_rect(base, 70, 36, 110, 88, C_SKIN)
    fill_rect(base, 70, 72, 76, 88, C_SHADOW); fill_rect(base, 104, 72, 110, 88, C_SHADOW)
    # 깊이를 알 수 없는 단호하고 지적인 눈
    fill_rect(base, 76, 50, 86, 52, C_LINE); fill_rect(base, 94, 50, 104, 52, C_LINE)
    fill_rect(base, 78, 54, 84, 58, C_WHITE); base[56][81] = C_CYAN
    fill_rect(base, 96, 54, 102, 58, C_WHITE); base[56][99] = C_CYAN
    # 오뚝하고 반듯한 콧대
    fill_rect(base, 88, 56, 92, 70, C_SHADOW)
    # 고요하고 차분한 입술
    fill_rect(base, 84, 76, 96, 78, C_SHADOW)
    # 단정한 검은 외투
    fill_rect(base, 50, 88, 130, 151, C_LINE)
    # 싱클레어의 어깨를 짚은 데미안의 손 (Col 140~160, Row 96~110)
    fill_rect(base, 130, 94, 156, 104, C_SKIN)

    # [우측: 깨달음을 얻고 눈을 뜬 싱클레어 (Col 160~240)]
    draw_circle(base, 200, 48, 24, 20, C_BROWN) # 머리
    fill_rect(base, 182, 48, 218, 92, C_SKIN)
    # 데미안을 바라보는 경이로운 눈빛
    fill_rect(base, 186, 56, 194, 60, C_WHITE); base[58][188] = C_LINE
    fill_rect(base, 204, 56, 212, 60, C_WHITE); base[58][206] = C_LINE
    fill_rect(base, 194, 76, 204, 79, C_LINE) # 감탄하는 입
    fill_rect(base, 160, 92, 230, 151, C_CLOTH) # 옷

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 데미안 이마의 [카인의 표식] 서서히 피어오르는 황금빛 후광 (Row 36~46, Col 86~94)
        if i >= 1:
            fr[40][90] = C_GOLD; fr[41][89] = C_GOLD; fr[41][91] = C_GOLD; fr[42][90] = C_GOLD
        if i == 2: # F3 카인의 표식 강렬한 다이아몬드 스파클(◆)
            fr[35][90] = C_WHITE; fill_rect(fr, 85, 39, 95, 41, C_WHITE); fr[45][90] = C_WHITE
            fr[40][90] = C_GOLD
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 3막: 촛불과 이젤 앞 베아트리체(데미안-자아) 초상화
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act3_ultra():
    base = make_canvas()
    # 배경: 어두운 하숙방 흑갈색 톤
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_BG)
    fill_rect(base, 20, 20, 70, 70, C_DARK_BROWN) # 창문과 비 내리는 밤

    # [좌측: 탁자 위 촛불 (Col 30~50, Row 80~140)]
    fill_rect(base, 26, 110, 54, 151, C_BROWN) # 탁자
    fill_rect(base, 36, 86, 44, 110, C_WHITE) # 양초
    fill_rect(base, 39, 80, 41, 86, C_LINE) # 심지

    # [중앙: 이젤과 초상화 (Col 90~190, Row 20~140)]
    # 나무 이젤 다리 3개
    fill_rect(base, 138, 10, 142, 151, C_DARK_BROWN)
    fill_rect(base, 80, 120, 84, 151, C_DARK_BROWN)
    fill_rect(base, 196, 120, 200, 151, C_DARK_BROWN)
    fill_rect(base, 86, 110, 194, 116, C_BROWN) # 받침대
    # 캔버스 (Col 96~184, Row 24~110)
    fill_rect(base, 96, 24, 184, 110, C_CLOTH)
    # 캔버스 속 초상화: 소년도 소녀도 아닌 신비로운 얼굴 (데미안과 싱클레어)
    draw_circle(base, 140, 60, 24, 28, C_SKIN)
    draw_circle(base, 140, 46, 26, 14, C_DARK_BROWN) # 신비로운 머리칼
    fill_rect(base, 128, 56, 136, 58, C_CYAN); fill_rect(base, 144, 56, 152, 58, C_CYAN) # 영롱한 눈
    fill_rect(base, 134, 74, 146, 76, C_RED) # 붉은 입술

    # [우측: 붓을 쥐고 응시하는 싱클레어의 뒷모습/옆모습 (Col 210~280)]
    fill_rect(base, 220, 50, 256, 90, C_SKIN) # 옆얼굴
    draw_circle(base, 230, 46, 22, 18, C_BROWN) # 헝클어진 머리
    fill_rect(base, 210, 90, 276, 151, C_LINE) # 어깨와 등
    # 오른손에 쥔 붓 (Col 180~216, Row 84~94)
    fill_rect(base, 196, 86, 216, 94, C_SKIN)
    fill_rect(base, 176, 88, 196, 90, C_GOLD) # 붓대

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 촛불 일렁임 모션
        fy = 72 + (i % 3) * 2
        draw_circle(fr, 40, fy, 6, 9, C_GOLD)
        draw_circle(fr, 40, fy, 3, 5, C_WHITE)
        if i == 2: # F3 초상화 눈동자와 촛불 다이아몬드 스파클
            fr[52][140] = C_WHITE; fill_rect(fr, 136, 55, 144, 57, C_WHITE); fr[60][140] = C_WHITE
            fr[68][40] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 4막: 알을 깨고 창공으로 솟구치는 아브락사스 (The Bird of Abraxas)
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act4_ultra():
    base = make_canvas()
    # 배경: 코발트 블루의 광활한 창공과 태양 광선
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
    for x in range(0, CANVAS_W, 20):
        fill_rect(base, x, 0, x+1, 151, C_WHITE) # 성스러운 빛살

    # 하단: 산산조각 나며 튀는 푸른 알껍데기 (Col 100~196, Row 110~148)
    draw_circle(base, 148, 126, 46, 24, C_WHITE)
    draw_circle(base, 148, 128, 42, 20, C_CYAN)
    # 파편 조각들
    fill_rect(base, 80, 114, 94, 124, C_WHITE)
    fill_rect(base, 202, 116, 216, 126, C_WHITE)
    fill_rect(base, 140, 100, 156, 108, C_CYAN)

    # [중앙: 알을 뚫고 솟구친 황금빛 매 (아브락사스)]
    # 매의 가슴과 몸통
    draw_circle(base, 148, 64, 20, 26, C_GOLD)
    # 머리와 깃털 볏
    draw_circle(base, 148, 40, 18, 18, C_GOLD)
    for y in range(20, 36): fill_rect(base, 144, y, 152, y, C_RED) # 붉은 불꽃 볏
    # 날카로운 맹금류의 눈과 부리
    draw_circle(base, 142, 38, 3, 3, C_LINE); base[38][142] = C_WHITE
    fill_rect(base, 152, 38, 166, 44, C_LINE) # 무쇠 갈고리 부리
    base[40][160] = C_GOLD

    frames = []
    # 웅장한 날개짓 6단계 (위로 솟구쳤다가 활짝 펴는 플랩 동세)
    wing_y = [-16, -8, 0, 8, 0, -8]
    for idx, dy in enumerate(wing_y):
        fr = [row[:] for row in base]
        # 좌측 날개 (Col 20~136)
        fill_rect(fr, 26, 46+dy, 136, 56+dy, C_GOLD)
        fill_rect(fr, 16, 38+dy, 80, 48+dy, C_CYAN) # 깃털 끝 푸른빛
        # 우측 날개 (Col 160~276)
        fill_rect(fr, 160, 46+dy, 270, 56+dy, C_GOLD)
        fill_rect(fr, 216, 38+dy, 280, 48+dy, C_CYAN)
        if idx == 2: # F3 매의 갈고리 부리와 눈동자 신성한 스파클(◆)
            fr[32][166] = C_WHITE; fill_rect(fr, 162, 37, 170, 39, C_WHITE); fr[42][166] = C_WHITE
            fr[34][142] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 5막: 파이프오르간 앞 피스토리우스와 불꽃을 응시하는 싱클레어
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act5_ultra():
    base = make_canvas()
    # 배경: 어스름한 석조 예배당 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_BG)
    # [좌측: 거대한 파이프오르간 숲 (Col 20~150, Row 10~110)]
    for idx, x in enumerate(range(20, 150, 10)):
        h = 30 + abs(x - 85)
        fill_rect(base, x, h, x+6, 110, C_STEEL)
        fill_rect(base, x+2, h+4, x+4, 108, C_WHITE) # 금속 광택
    # 오르간 건반과 의자
    fill_rect(base, 40, 110, 130, 120, C_DARK_BROWN)
    # 격정적으로 연주하는 피스토리우스의 뒷모습 (Col 60~110)
    draw_circle(base, 85, 94, 14, 14, C_BROWN) # 헝클어진 머리
    fill_rect(base, 66, 104, 104, 151, C_LINE) # 연주자 코트
    fill_rect(base, 50, 108, 120, 114, C_SKIN) # 건반 위의 두 손

    # [우측: 벽난로 장작불과 무릎 꿇고 응시하는 싱클레어 (Col 180~270)]
    # 벽난로 벽돌 틀
    fill_rect(base, 210, 60, 280, 140, C_DARK_BROWN)
    fill_rect(base, 224, 76, 266, 136, C_LINE) # 난로 속
    # 난로 앞 싱클레어
    draw_circle(base, 196, 92, 12, 12, C_BROWN)
    fill_rect(base, 190, 96, 202, 108, C_SKIN)
    fill_rect(base, 184, 108, 208, 151, C_BLUE)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 장작불 타오르는 불꽃 넘실거림
        for bx in range(228, 262, 8):
            by = 96 + ((bx + i * 12) % 24)
            fill_rect(fr, bx, by, bx+5, 132, C_GOLD)
            fill_rect(fr, bx+1, by+4, bx+4, 130, C_RED)
        if i == 2: # F3 오르간 파이프 반사광과 불꽃 스파클
            fr[40][85] = C_WHITE; fill_rect(fr, 81, 44, 89, 46, C_WHITE); fr[50][85] = C_WHITE
            fr[100][245] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 6막: 에바 부인의 자애로운 품과 거대한 사랑
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act6_ultra():
    base = make_canvas()
    # 배경: 따뜻하고 은은한 벨벳 서가와 사광 (Col 0~295, Row 0~151)
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
    # 창문으로 비쳐드는 렘브란트 황금빛 사광
    for y in range(0, 152):
        for x in range(0, 120):
            if (x + y) % 6 == 0: base[y][x] = C_GOLD

    # [중앙: 에바 부인 (Frau Eva · Col 110~190, Row 20~151)]
    # 틀어 올린 짙은 밤색 머리칼
    draw_circle(base, 148, 38, 24, 20, C_BROWN)
    # 성스러운 여신이자 어머니의 얼굴
    fill_rect(base, 130, 42, 166, 86, C_SKIN)
    fill_rect(base, 130, 70, 136, 86, C_SHADOW); fill_rect(base, 160, 70, 166, 86, C_SHADOW)
    # 깊고 온화한 눈매와 자애로운 미소
    fill_rect(base, 136, 52, 144, 55, C_LINE); fill_rect(base, 152, 52, 160, 55, C_LINE)
    base[56][140] = C_BLUE; base[56][156] = C_BLUE
    fill_rect(base, 142, 72, 154, 75, C_RED) # 온화한 미소
    # 푸른 사파이어 보석 목걸이 (Col 144~152, Row 88~96)
    fill_rect(base, 142, 86, 154, 89, C_GOLD) # 줄
    draw_circle(base, 148, 93, 4, 5, C_BLUE) # 보석
    # 품위 있는 군청색 드레스
    fill_rect(base, 106, 92, 190, 151, C_BLUE)

    # [우측 아래: 에바 부인 앞에 무릎 꿇은 싱클레어 (Col 180~250)]
    draw_circle(base, 196, 88, 16, 16, C_BROWN) # 고개 숙인 머리
    fill_rect(base, 186, 98, 204, 114, C_SKIN)
    fill_rect(base, 180, 114, 240, 151, C_CLOTH) # 옷
    # 에바 부인이 싱클레어의 이마를 부드럽게 감싸 쥔 따스한 손 (Col 172~192, Row 80~92)
    fill_rect(base, 170, 82, 192, 90, C_SKIN)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 에바 부인의 숨결에 따른 보석의 광채
        if i == 2: # F3 사파이어 목걸이와 부인의 눈빛 다이아몬드 스파클
            fr[87][148] = C_WHITE; fill_rect(fr, 143, 92, 153, 94, C_WHITE); fr[99][148] = C_WHITE
            fr[52][140] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 7막: 야전병원 마지막 키스와 거울 속 완성된 참 자아
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act7_ultra():
    base = make_canvas()
    # 배경: 포화가 번쩍이는 야전병원 병동 창문과 어두운 막사
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
    fill_rect(base, 120, 10, 180, 50, C_DARK_BROWN) # 창문
    fill_rect(base, 124, 14, 176, 46, C_RED) # 포화의 붉은 연기

    # [좌측 침대: 붕대를 감고 누운 데미안 (Col 30~120)]
    fill_rect(base, 20, 90, 126, 144, C_WHITE) # 침대 시트
    fill_rect(base, 40, 74, 86, 106, C_SKIN) # 데미안 얼굴
    fill_rect(base, 36, 68, 90, 78, C_WHITE) # 머리에 감은 하얀 붕대
    fill_rect(base, 48, 86, 56, 88, C_LINE); fill_rect(base, 70, 86, 78, 88, C_LINE) # 감긴 눈
    fill_rect(base, 56, 96, 68, 98, C_SHADOW) # 마지막 미소

    # [우측: 침대 곁에서 벽의 거울을 마주한 싱클레어 (Col 170~270)]
    # 벽에 걸린 작은 원형 거울 (Col 210~270, Row 30~90)
    draw_circle(base, 240, 60, 26, 26, C_STEEL) # 거울 테두리
    draw_circle(base, 240, 60, 22, 22, C_CYAN) # 거울 유리
    # 거울 속에 비친 얼굴: 이제는 데미안과 완전히 하나가 된 단호하고 성숙한 참 자아!
    fill_rect(base, 226, 46, 254, 76, C_SKIN)
    fill_rect(base, 230, 40, 250, 48, C_LINE) # 데미안을 닮은 단정한 머리
    fill_rect(base, 232, 54, 238, 56, C_LINE); fill_rect(base, 242, 54, 248, 56, C_LINE)
    base[55][235] = C_WHITE; base[55][245] = C_WHITE # 각성한 흔들림 없는 눈동자
    fill_rect(base, 236, 68, 244, 70, C_LINE) # 평온한 미소

    # 싱클레어의 상반신 (Col 160~220, Row 80~151)
    fill_rect(base, 160, 90, 220, 151, C_CLOTH)

    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 창밖의 간헐적 포화 섬광
        if i % 3 == 0:
            fill_rect(fr, 124, 14, 176, 46, C_GOLD)
        if i == 2: # F3 거울 속 눈동자에서 빛나는 영원한 각성의 스파클(◆)
            fr[50][240] = C_WHITE; fill_rect(fr, 235, 54, 245, 56, C_WHITE); fr[62][240] = C_WHITE
        frames.append(fr)
    return frames

print("Loaded ultra demian cutscenes!")
