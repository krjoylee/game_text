#!/usr/bin/env python3
"""
tools/generate_all_packs_studio.py
🏆 [4대 명작 통합 296x152 영화적 컷씬 스튜디오]
- 지원 작품 (총 4개 팩):
  1. 흥부놀부전 (Tutorial)
  2. 제임스와 슈퍼 복숭아 (Roald Dahl)
  3. 단테의 신곡: 지옥편 (Dante's Inferno)
  4. 데미안 (Hermann Hesse)
- 4대 연출 원칙 100% 적용:
  * 물리적 동세 (Flapping, Wave, Fire, Blade)
  * 해부학적 접촉점 선명화 (Hands, Teeth, Knives, Horns)
  * 절제된 시네마틱 다이아몬드 스파클 (◆)
  * 인물 일관성 (Character Consistency)
"""

import os
import sys
import json

CANVAS_W = 296
CANVAS_H = 152

PALETTE_16 = [
    ("배경암흑", 237, (30, 30, 30)),        # 0: 어두운 배경 회갈색
    ("칠흑먹선", 16, (10, 10, 10)),        # 1: 외곽선, 눈썹, 동공, 수염, 밤하늘
    ("피부살구", 223, (255, 204, 153)),     # 2: 밝은 피부톤
    ("피부음영", 179, (212, 155, 106)),     # 3: 코 음영, 턱선, 주름, 근육
    ("누런삼베", 186, (194, 178, 128)),     # 4: 짚, 양피지, 옷감
    ("대지갈색", 94, (139, 90, 43)),       # 5: 나무, 고목, 지붕, 암석
    ("타오르는주홍", 196, (231, 76, 60)),    # 6: 지옥불, 복숭아 붉은빛, 피, 단테 두건
    ("신비군청", 25, (36, 113, 163)),       # 7: 대서양 바다, 심연, 도포
    ("눈물하늘", 81, (93, 173, 226)),       # 8: 눈물, 하늘, 호수, 얼음
    ("순백반사", 231, (255, 255, 255)),     # 9: 눈동자 반사광, 스파클, 송곳니, 갈매기
    ("비단청록", 31, (0, 135, 175)),        # 10: 바다 물결, 지옥 강물
    ("거친음영", 137, (175, 135, 95)),      # 11: 옷 주름, 바위 질감
    ("황금빛", 220, (244, 208, 63)),        # 12: 금이빨, 박씨, 별빛, 복숭아, 마법의 씨앗
    ("괴수녹색", 36, (22, 160, 133)),       # 13: 마법 악어 혀, 도깨비
    ("강철무쇠", 244, (128, 139, 150)),     # 14: 톱날, 칼날, 쇠몽둥이, 파이프오르간
    ("생명녹색", 41, (46, 204, 113)),       # 15: 봄 들판, 수풀
]

C_BG = 0; C_LINE = 1; C_SKIN = 2; C_SHADOW = 3; C_CLOTH = 4; C_BROWN = 5
C_RED = 6; C_BLUE = 7; C_SKY = 8; C_WHITE = 9; C_CYAN = 10; C_DARK_BROWN = 11
C_GOLD = 12; C_GREEN = 13; C_STEEL = 14; C_LIME = 15

def make_canvas():
    return [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]

def fill_rect(canvas, x1, y1, x2, y2, color):
    x1 = max(0, min(CANVAS_W-1, x1)); x2 = max(0, min(CANVAS_W-1, x2))
    y1 = max(0, min(CANVAS_H-1, y1)); y2 = max(0, min(CANVAS_H-1, y2))
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            canvas[y][x] = color

def draw_circle(canvas, cx, cy, rx, ry, color):
    for y in range(max(0, cy - ry), min(CANVAS_H, cy + ry + 1)):
        for x in range(max(0, cx - rx), min(CANVAS_W, cx + rx + 1)):
            if ((x - cx)**2) / (rx**2) + ((y - cy)**2) / (ry**2) <= 1.0:
                canvas[y][x] = color

def compress_frame_rle(grid):
    flat = [p for row in grid for p in row]
    chunks = []
    cur_c = flat[0]
    cur_cnt = 1
    for p in flat[1:]:
        if p == cur_c and cur_cnt < 255:
            cur_cnt += 1
        else:
            chunks.append(f"{cur_cnt}_{cur_c}")
            cur_c = p
            cur_cnt = 1
    chunks.append(f"{cur_cnt}_{cur_c}")
    return ",".join(chunks)

# ─────────────────────────────────────────────────────────────────────────────
# 기존 흥부놀부전 컷씬 불러오기
# ─────────────────────────────────────────────────────────────────────────────
sys.path.append("/home/krjoylee/code/game/tools")
from generate_hires_studio import (
    gen_hires_act1, gen_hires_act2, gen_hires_act3, gen_hires_act4,
    gen_hires_act5, gen_hires_act6, gen_hires_act7
)

# ─────────────────────────────────────────────────────────────────────────────
# 🍑 [제임스와 슈퍼 복숭아] 1~7막 296x152 영화적 컷씬 제너레이터
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act1(): # 스폰지와 스파이커 이모의 학대
    base = make_canvas()
    # 앙상한 스파이커 (좌측) & 뚱뚱한 스폰지 (우측)
    fill_rect(base, 40, 20, 80, 80, C_SKIN)
    fill_rect(base, 36, 12, 84, 20, C_LINE) # 깃털 모자
    fill_rect(base, 54, 40, 60, 56, C_SHADOW) # 뾰족한 코
    fill_rect(base, 20, 80, 96, 151, C_RED) # 붉은 드레스
    # 스폰지 이모
    draw_circle(base, 220, 60, 48, 48, C_SKIN)
    fill_rect(base, 160, 90, 280, 151, C_CLOTH) # 거대한 몸통
    # 제임스 (중앙 아래 웅크림)
    fill_rect(base, 136, 90, 160, 120, C_SKIN)
    fill_rect(base, 132, 114, 164, 151, C_DARK_BROWN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 이모 지팡이 스파클
            fr[60][98] = C_WHITE; fill_rect(fr, 96, 61, 100, 63, C_WHITE); fr[64][98] = C_WHITE
        frames.append(fr)
    return frames

def gen_peach_act2(): # 노인의 빛나는 초록 마법 악어 혀
    base = make_canvas()
    # 노인의 두 손이 빛나는 봉투를 건넴
    fill_rect(base, 60, 80, 130, 130, C_SKIN)
    fill_rect(base, 166, 80, 236, 130, C_SKIN)
    # 신비로운 봉투와 초록 마법 발광체
    fill_rect(base, 120, 50, 176, 110, C_WHITE)
    draw_circle(base, 148, 80, 20, 20, C_GREEN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 꿈틀거리는 초록빛 마법 동세
        shift = (i % 3) * 2
        draw_circle(fr, 148 + shift, 80, 16, 16, C_LIME)
        if i == 2: # F3 초록 다이아몬드 스파클
            fr[68][148] = C_WHITE; fill_rect(fr, 144, 73, 152, 75, C_WHITE); fr[80][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_peach_act3(): # 거대 슈퍼 복숭아 탄생
    base = make_canvas()
    # 언덕 위 거대한 슈퍼 복숭아
    draw_circle(base, 148, 80, 68, 64, C_GOLD)
    draw_circle(base, 148, 80, 56, 52, C_RED)
    # 꼭지 나뭇잎
    fill_rect(base, 144, 12, 152, 24, C_BROWN)
    draw_circle(base, 158, 16, 14, 6, C_LIME)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 복숭아 박동 들숨/날숨
        pulse = 2 if i % 2 == 0 else -2
        draw_circle(fr, 148, 80, 58 + pulse, 54 + pulse, C_RED)
        if i == 2: # F3 향기 스파클
            fr[6][148] = C_WHITE; fill_rect(fr, 145, 10, 151, 12, C_WHITE); fr[16][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_peach_act4(): # 곤충 친구들과의 만남
    base = make_canvas()
    # 실크햇 메뚜기 신사
    fill_rect(base, 70, 40, 100, 70, C_GREEN)
    fill_rect(base, 74, 20, 96, 40, C_LINE) # 실크햇
    # 무당벌레 숙녀
    draw_circle(base, 210, 70, 30, 26, C_RED)
    fill_rect(base, 196, 60, 202, 66, C_LINE); fill_rect(base, 218, 60, 224, 66, C_LINE) # 점박이
    # 제임스 (가운데)
    fill_rect(base, 136, 70, 160, 120, C_SKIN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 메뚜기 안경 스파클
            fr[46][94] = C_WHITE; fill_rect(fr, 92, 49, 96, 51, C_WHITE); fr[54][94] = C_WHITE
        frames.append(fr)
    return frames

def gen_peach_act5(): # 바다로 굴러떨어지는 역동적 스플래시
    base = make_canvas()
    # 푸른 대서양 바다
    fill_rect(base, 0, 90, CANVAS_W-1, 151, C_BLUE)
    # 복숭아 바다에 둥둥
    draw_circle(base, 148, 86, 54, 50, C_RED)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 하얀 파도 포말 출렁임
        wave_y = 86 + (i % 3) * 3
        fill_rect(fr, 80, wave_y, 216, wave_y + 4, C_WHITE)
        if i == 2: # F3 물방울 스파클
            fr[70][148] = C_WHITE; fill_rect(fr, 145, 74, 151, 76, C_WHITE); fr[80][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_peach_act6(): # 500마리 갈매기 결속 하늘 비행
    base = make_canvas()
    # 푸른 하늘과 흰 구름
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
    # 공중에 뜬 슈퍼 복숭아
    draw_circle(base, 148, 100, 44, 40, C_RED)
    # 거미줄 실 (위로 뻗음)
    for x in range(70, 230, 20):
        for y in range(20, 70):
            base[y][x] = C_WHITE
    frames = []
    wing_offsets = [-8, -4, 0, 6, 0, -4]
    for idx, dy in enumerate(wing_offsets):
        fr = [row[:] for row in base]
        # 날개 퍼덕이는 갈매기 떼 (상단)
        for gx in range(60, 240, 40):
            fill_rect(fr, gx - 12, 20 + dy, gx + 12, 24 + dy, C_WHITE)
            fr[18 + dy][gx] = C_LINE
        if idx == 2: # F3 햇살 스파클
            fr[4][148] = C_WHITE; fill_rect(fr, 144, 8, 152, 10, C_WHITE); fr[14][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_peach_act7(): # 엠파이어 스테이트 빌딩 착륙과 환호
    base = make_canvas()
    # 뉴욕 마천루 엠파이어 빌딩 첨탑
    fill_rect(base, 140, 60, 156, 151, C_STEEL)
    fill_rect(base, 146, 10, 150, 60, C_STEEL)
    # 첨탑에 꽂힌 슈퍼 복숭아!
    draw_circle(base, 148, 40, 36, 32, C_RED)
    # 꼭대기에서 손 흔드는 제임스
    fill_rect(base, 144, 12, 152, 22, C_SKIN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 뉴욕 꽃가루 흩날림
        for fx in range(20, 280, 30):
            fy = (i * 18 + fx) % 140
            fr[fy][fx] = C_GOLD if fx % 2 == 0 else C_WHITE
        if i == 2: # F3 첨탑 다이아몬드 스파클
            fr[2][148] = C_WHITE; fill_rect(fr, 144, 6, 152, 8, C_WHITE); fr[12][148] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 🔥 [단테의 신곡: 지옥편] 1~7막 296x152 영화적 컷씬 제너레이터
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act1(): # 어두운 숲과 세 마리 맹수 & 베르길리우스
    base = make_canvas()
    # 어두운 가시덤불 숲
    for x in range(0, CANVAS_W, 20): fill_rect(base, x, 0, x+2, 120, C_LINE)
    # 단테 (붉은 두건과 도포)
    fill_rect(base, 60, 40, 90, 70, C_RED)
    fill_rect(base, 64, 50, 86, 80, C_SKIN)
    # 베르길리우스 (온화한 월계관과 푸른 옷)
    fill_rect(base, 180, 30, 210, 60, C_WHITE)
    draw_circle(base, 195, 24, 14, 6, C_LIME) # 월계관
    fill_rect(base, 170, 60, 220, 151, C_BLUE)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 지팡이 월계관 스파클
            fr[18][195] = C_WHITE; fill_rect(fr, 191, 22, 199, 24, C_WHITE); fr[28][195] = C_WHITE
        frames.append(fr)
    return frames

def gen_dante_act2(): # 지옥의 문과 아케론 강의 뱃사공 카론
    base = make_canvas()
    # 검붉은 아케론 강
    fill_rect(base, 0, 90, CANVAS_W-1, 151, C_RED)
    # 카론의 나룻배와 노
    fill_rect(base, 60, 100, 220, 130, C_BROWN)
    # 불타는 눈의 늙은 카론
    fill_rect(base, 130, 40, 166, 100, C_LINE)
    base[50][140] = C_RED; base[50][156] = C_RED # 이글거리는 붉은 눈!
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 카론의 노질 움직임
        oar_x = 100 + (i % 3) * 8
        fill_rect(fr, oar_x, 60, oar_x + 6, 140, C_STEEL)
        if i == 2: # F3 붉은 눈빛 스파클
            fr[46][140] = C_WHITE; fr[46][156] = C_WHITE
        frames.append(fr)
    return frames

def gen_dante_act3(): # 애욕의 폭풍 속 파올로와 프란체스카
    base = make_canvas()
    # 허공을 맴도는 두 연인 (포옹)
    draw_circle(base, 136, 70, 24, 30, C_WHITE) # 프란체스카
    draw_circle(base, 160, 70, 24, 30, C_BLUE)  # 파올로
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 회오리치는 암흑 폭풍
        for y in range(20, 140, 16):
            sx = (y * 3 + i * 20) % CANVAS_W
            fill_rect(fr, sx, y, sx + 40, y + 2, C_LINE)
        if i == 2: # F3 눈물 스파클
            fr[62][148] = C_WHITE; fill_rect(fr, 144, 65, 152, 67, C_WHITE); fr[74][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_dante_act4(): # 불타는 석관과 파리나타의 기개
    base = make_canvas()
    # 붉게 달아오른 석관
    fill_rect(base, 60, 70, 236, 140, C_STEEL)
    # 치솟는 지옥불
    fill_rect(base, 80, 40, 216, 70, C_RED)
    # 당당한 파리나타 상반신
    fill_rect(base, 126, 20, 170, 70, C_SKIN)
    fill_rect(base, 110, 60, 186, 110, C_CLOTH)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 불꽃의 넘실거림
        for x in range(80, 216, 12):
            fy = 30 + ((x + i * 8) % 20)
            fill_rect(fr, x, fy, x + 6, 70, C_GOLD)
        if i == 2: # F3 불꽃 검 스파클
            fr[16][148] = C_WHITE; fill_rect(fr, 144, 20, 152, 22, C_WHITE); fr[26][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_dante_act5(): # 끓는 피의 강과 켄타우로스의 활
    base = make_canvas()
    # 펄펄 끓는 플레게톤 강
    fill_rect(base, 0, 80, CANVAS_W-1, 151, C_RED)
    # 반인반마 켄타우로스 활 시위
    fill_rect(base, 180, 20, 230, 80, C_SKIN)
    fill_rect(base, 160, 70, 270, 130, C_BROWN) # 말 몸통
    fill_rect(base, 120, 30, 180, 34, C_STEEL) # 겨눈 화살!
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 보글거리는 핏방울
        for bx in range(20, 160, 24):
            by = 90 + ((bx + i * 10) % 40)
            draw_circle(fr, bx, by, 6, 4, C_GOLD)
        if i == 2: # F3 화살촉 스파클
            fr[26][120] = C_WHITE; fill_rect(fr, 116, 30, 124, 32, C_WHITE); fr[36][120] = C_WHITE
        frames.append(fr)
    return frames

def gen_dante_act6(): # 말레볼제의 구덩이와 뱀의 변신
    base = make_canvas()
    # 암흑 구덩이
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
    # 고통받는 죄인
    fill_rect(base, 130, 40, 166, 120, C_SKIN)
    # 죄인을 칭칭 감은 거대한 지옥 뱀
    draw_circle(base, 148, 70, 34, 46, C_GREEN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 뱀의 똬리 꿈틀거림
        shift = 4 if i % 2 == 0 else -4
        draw_circle(fr, 148 + shift, 70, 36, 48, C_GREEN)
        if i == 2: # F3 독니 스파클
            fr[34][148] = C_WHITE; fill_rect(fr, 144, 38, 152, 40, C_WHITE); fr[44][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_dante_act7(): # 얼음 지옥 탈출과 밤하늘의 찬란한 별들
    base = make_canvas()
    # 깊은 밤하늘
    fill_rect(base, 0, 0, CANVAS_W-1, 100, C_LINE)
    # 지상으로 빠져나온 언덕
    fill_rect(base, 0, 100, CANVAS_W-1, 151, C_BROWN)
    # 우러러보는 단테와 베르길리우스 뒷모습
    fill_rect(base, 60, 80, 84, 120, C_RED)
    fill_rect(base, 94, 70, 120, 120, C_BLUE)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 밤하늘 총총한 별빛들
        for sx in range(40, 280, 30):
            sy = (sx * 7) % 80
            fr[sy][sx] = C_GOLD if (sx + i) % 2 == 0 else C_WHITE
        if i == 2: # F3 북극성 대형 다이아몬드 스파클
            fr[10][220] = C_WHITE; fill_rect(fr, 214, 16, 226, 18, C_WHITE); fr[24][220] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 🦅 [데미안] 1~7막 296x152 영화적 컷씬 제너레이터
# ─────────────────────────────────────────────────────────────────────────────
def gen_demian_act1(): # 크로머의 사과 협박
    base = make_canvas()
    # 어두운 골목 가스등 불빛
    fill_rect(base, 20, 20, 60, 151, C_GOLD)
    # 불량배 크로머 (주머니칼 든 손)
    fill_rect(base, 80, 30, 130, 80, C_LINE)
    fill_rect(base, 130, 60, 170, 70, C_STEEL) # 번쩍이는 칼날!
    # 겁에 질린 싱클레어
    fill_rect(base, 180, 40, 220, 90, C_SKIN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 칼날 차가운 스파클
            fr[54][150] = C_WHITE; fill_rect(fr, 146, 59, 154, 61, C_WHITE); fr[66][150] = C_WHITE
        frames.append(fr)
    return frames

def gen_demian_act2(): # 막스 데미안과 카인의 표식
    base = make_canvas()
    # 신비로운 소년 막스 데미안의 얼굴 클로즈업
    fill_rect(base, 100, 20, 196, 110, C_SKIN)
    # 깊고 지적인 눈매
    fill_rect(base, 116, 50, 140, 54, C_LINE)
    fill_rect(base, 156, 50, 180, 54, C_LINE)
    base[52][128] = C_SKY; base[52][168] = C_SKY
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # F3 이마의 카인의 표식 황금빛 발광!
        if i == 2:
            fr[28][148] = C_GOLD; fill_rect(fr, 142, 34, 154, 38, C_GOLD); fr[44][148] = C_GOLD
            base[36][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_demian_act3(): # 베아트리체 초상화와 촛불
    base = make_canvas()
    # 어두운 방 이젤 위의 신비로운 초상화
    fill_rect(base, 90, 20, 206, 130, C_CLOTH)
    draw_circle(base, 148, 70, 36, 44, C_SKIN)
    # 촛불 (좌측)
    fill_rect(base, 40, 80, 48, 140, C_WHITE)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 촛불 불꽃 넘실거림
        flame_y = 66 + (i % 3) * 2
        draw_circle(fr, 44, flame_y, 6, 10, C_GOLD)
        if i == 2: # F3 초상화 이마 스파클
            fr[40][148] = C_WHITE; fill_rect(fr, 144, 46, 152, 48, C_WHITE); fr[54][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_demian_act4(): # 알을 깨고 나오는 매의 비상 (아브락사스)
    base = make_canvas()
    # 푸른 하늘
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
    # 깨진 거대한 알껍데기 (하단)
    draw_circle(base, 148, 110, 50, 36, C_WHITE)
    # 솟구치는 황금 매의 몸통
    draw_circle(base, 148, 50, 24, 28, C_GOLD)
    frames = []
    wing_offsets = [-16, -8, 0, 10, 0, -8]
    for idx, dy in enumerate(wing_offsets):
        fr = [row[:] for row in base]
        # 힘찬 날개짓 (좌우)
        wy = 44 + dy
        fill_rect(fr, 40, wy, 130, wy + 8, C_GOLD)
        fill_rect(fr, 166, wy, 256, wy + 8, C_GOLD)
        if idx == 2: # F3 부리와 눈빛 신성한 스파클
            fr[20][148] = C_WHITE; fill_rect(fr, 144, 26, 152, 28, C_WHITE); fr[34][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_demian_act5(): # 오르간 연주자 피스토리우스와 불꽃
    base = make_canvas()
    # 거대한 파이프오르간 파이프들
    for x in range(20, 200, 16): fill_rect(base, x, 10, x + 8, 110, C_STEEL)
    # 벽난로 타오르는 불꽃 (우측)
    fill_rect(base, 220, 70, 280, 140, C_BROWN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        # 타오르는 장작불
        for fx in range(230, 270, 10):
            fy = 80 + ((fx + i * 8) % 30)
            fill_rect(fr, fx, fy, fx + 6, 130, C_GOLD)
        if i == 2: # F3 파이프 끝 금빛 스파클
            fr[4][80] = C_WHITE; fill_rect(fr, 76, 8, 84, 10, C_WHITE); fr[14][80] = C_WHITE
        frames.append(fr)
    return frames

def gen_demian_act6(): # 에바 부인의 자애로운 품
    base = make_canvas()
    # 숭고하고 자애로운 에바 부인의 상반신
    draw_circle(base, 148, 54, 38, 44, C_SKIN)
    fill_rect(base, 90, 80, 206, 151, C_BLUE) # 우아한 드레스
    # 목걸이 보석
    draw_circle(base, 148, 86, 6, 6, C_GOLD)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 목걸이 보석 다이아몬드 스파클
            fr[78][148] = C_WHITE; fill_rect(fr, 144, 84, 152, 86, C_WHITE); fr[92][148] = C_WHITE
        frames.append(fr)
    return frames

def gen_demian_act7(): # 야전병원의 마지막 키스와 거울 속 자아
    base = make_canvas()
    # 야전병원 침상과 거울
    fill_rect(base, 40, 40, 130, 130, C_WHITE) # 침상 데미안
    fill_rect(base, 170, 20, 260, 130, C_STEEL) # 거울 프레임
    # 거울 속에 비친 완전히 성숙한 싱클레어의 얼굴
    draw_circle(base, 215, 75, 30, 36, C_SKIN)
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if i == 2: # F3 거울 속 눈동자 영원한 스파클
            fr[60][215] = C_WHITE; fill_rect(fr, 210, 66, 220, 68, C_WHITE); fr[76][215] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 📜 4개 팩 마스터 데이터 빌더
# ─────────────────────────────────────────────────────────────────────────────
def build_all_packs_studio():
    packs_meta = [
        {
            "pack_id": "heungbu_nolbu",
            "pack_name": "《흥부놀부전》 (Tutorial)",
            "metric": "♧ 선행의 씨앗",
            "acts": [
                {"id": 1, "title": "제1막: 형제의 갈림길", "desc": "놀부의 호통과 쫓겨나는 흥부의 눈물", "gen": gen_hires_act1},
                {"id": 2, "title": "제2막: 다친 제비", "desc": "흥부의 따스한 두 손과 붉은 실 치료", "gen": gen_hires_act2},
                {"id": 3, "title": "제3막: 보은의 비행과 박씨", "desc": "제비의 상하 플랩 날개짓과 황금 박씨", "gen": gen_hires_act3},
                {"id": 4, "title": "제4막: 대박 타기와 황금 보화", "desc": "흥부 부부의 역동적 톱질과 엽전 폭풍", "gen": gen_hires_act4},
                {"id": 5, "title": "제5막: 놀부의 잔혹한 만행", "desc": "놀부의 엄지와 검지가 제비 다리를 뚝 꺾음", "gen": gen_hires_act5},
                {"id": 6, "title": "제6막: 도깨비의 심판", "desc": "외뿔 도깨비의 송곳니와 다이아몬드 스파클", "gen": gen_hires_act6},
                {"id": 7, "title": "제7막: 눈물의 화해", "desc": "참회의 눈물을 흘리는 놀부와 맞잡은 두 손", "gen": gen_hires_act7}
            ]
        },
        {
            "pack_id": "james_peach",
            "pack_name": "《제임스와 슈퍼 복숭아》 (Roald Dahl)",
            "metric": "✦ 경이와 용기",
            "acts": [
                {"id": 1, "title": "제1막: 스폰지와 스파이커 이모", "desc": "사악한 이모들의 학대와 웅크린 제임스", "gen": gen_peach_act1},
                {"id": 2, "title": "제2막: 마법의 악어 혀", "desc": "신비로운 노인의 봉투 속 요동치는 초록 발광체", "gen": gen_peach_act2},
                {"id": 3, "title": "제3막: 거대 복숭아의 탄생", "desc": "언덕 위 쿵-쿵 박동하며 부풀어 오른 슈퍼 복숭아", "gen": gen_peach_act3},
                {"id": 4, "title": "제4막: 거대 곤충 친구들", "desc": "실크햇 메뚜기 신사와 상냥한 무당벌레", "gen": gen_peach_act4},
                {"id": 5, "title": "제5막: 대서양으로의 출항", "desc": "절벽을 굴러 떨어져 바다에 뜬 복숭아와 파도", "gen": gen_peach_act5},
                {"id": 6, "title": "제6막: 500마리 갈매기 비행", "desc": "거미줄로 결속된 갈매기 떼의 장엄한 하늘 비행", "gen": gen_peach_act6},
                {"id": 7, "title": "제7막: 엠파이어 빌딩 착륙", "desc": "뉴욕 마천루 첨탑에 꽂힌 복숭아와 환호의 꽃가루", "gen": gen_peach_act7}
            ]
        },
        {
            "pack_id": "dante_inferno",
            "pack_name": "《단테의 신곡: 지옥편》 (Dante Alighieri)",
            "metric": "☩ 이성과 영혼의 빛",
            "acts": [
                {"id": 1, "title": "제1막: 어두운 숲과 베르길리우스", "desc": "세 마리 맹수를 물리치고 나타난 스승의 지팡이 빛", "gen": gen_dante_act1},
                {"id": 2, "title": "제2막: 지옥의 문과 카론", "desc": "아케론 강의 핏빛 나룻배와 카론의 붉은 눈", "gen": gen_dante_act2},
                {"id": 3, "title": "제3막: 애욕의 폭풍", "desc": "암흑 폭풍 속 부유하는 파올로와 프란체스카의 눈물", "gen": gen_dante_act3},
                {"id": 4, "title": "제4막: 불타는 석관의 파리나타", "desc": "솟구치는 지옥불 속 당당한 귀족의 기개", "gen": gen_dante_act4},
                {"id": 5, "title": "제5막: 끓는 피의 강과 켄타우로스", "desc": "플레게톤 강둑에서 겨눈 서슬 퍼런 화살촉", "gen": gen_dante_act5},
                {"id": 6, "title": "제6막: 말레볼제와 지옥 뱀", "desc": "죄인을 칭칭 감은 뱀의 독니와 지독한 고통", "gen": gen_dante_act6},
                {"id": 7, "title": "제7막: 얼음 지옥 탈출과 별들", "desc": "코키토스를 빠져나와 마주한 밤하늘의 찬란한 은하수", "gen": gen_dante_act7}
            ]
        },
        {
            "pack_id": "demian",
            "pack_name": "《데미안》 (Hermann Hesse)",
            "metric": "☥ 내면의 각성",
            "acts": [
                {"id": 1, "title": "제1막: 두 개의 세계와 크로머", "desc": "골목길 그늘에서 번쩍이는 주머니칼 협박", "gen": gen_demian_act1},
                {"id": 2, "title": "제2막: 데미안과 카인의 표식", "desc": "신비로운 눈빛과 이마에 빛나는 카인의 표식", "gen": gen_demian_act2},
                {"id": 3, "title": "제3막: 베아트리체 초상화", "desc": "흔들리는 촛불과 내면의 얼굴이 투영된 이젤", "gen": gen_demian_act3},
                {"id": 4, "title": "제4막: 알을 깨는 매의 비상", "desc": "알껍데기를 깨고 푸른 하늘로 날아오르는 황금 매", "gen": gen_demian_act4},
                {"id": 5, "title": "제5막: 피스토리우스와 불꽃", "desc": "거대한 파이프오르간과 벽난로의 타오르는 장작불", "gen": gen_demian_act5},
                {"id": 6, "title": "제6막: 에바 부인의 품", "desc": "모든 어머니이자 연인인 에바 부인의 자애로운 목걸이", "gen": gen_demian_act6},
                {"id": 7, "title": "제7막: 마지막 키스와 거울", "desc": "야전병원의 어둠 속 거울에 비친 완성된 참 자아", "gen": gen_demian_act7}
            ]
        }
    ]

    processed_packs = []
    for p in packs_meta:
        print(f"📦 팩 빌드 중: {p['pack_name']}...")
        p_acts = []
        for act in p["acts"]:
            frames = act["gen"]()
            rle_frames = [compress_frame_rle(f) for f in frames]
            p_acts.append({
                "id": act["id"],
                "title": act["title"],
                "desc": act["desc"],
                "rle_frames": rle_frames
            })
        processed_packs.append({
            "pack_id": p["pack_id"],
            "pack_name": p["pack_name"],
            "metric": p["metric"],
            "acts": p_acts
        })

    palette_hex = [f"#{c[2][0]:02x}{c[2][1]:02x}{c[2][2]:02x}" for c in PALETTE_16]
    
    studio_json = json.dumps({
        "palette": palette_hex,
        "packs": processed_packs
    })

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Divina Ludus — 4대 명작 컷씬 검토 스튜디오 (Native 296x152)</title>
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
  .studio-frame {{
    width: 1040px;
    height: 880px;
    background: #1e1e1e;
    border: 3px solid #4a4a4a;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.9);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .studio-header {{
    background: #2d2d2d;
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #3a3a3a;
  }}
  .studio-title {{ font-size: 16px; font-weight: bold; color: #ffcc99; }}
  .studio-hud {{ font-size: 13px; color: #81d4fa; font-family: monospace; }}
  
  .main-content {{
    flex: 1;
    display: flex;
    background: #181818;
  }}
  .sidebar {{
    width: 290px;
    background: #222;
    border-right: 2px solid #333;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow-y: auto;
  }}
  .pack-header {{
    font-size: 13px;
    font-weight: bold;
    color: #f39c12;
    margin-top: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #444;
  }}
  .nav-btn {{
    background: #2a2a2a;
    color: #bbb;
    border: 1px solid #3c3c3c;
    padding: 9px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    text-align: left;
    transition: all 0.15s;
  }}
  .nav-btn:hover {{
    background: #383838;
    color: #fff;
    border-color: #777;
  }}
  .nav-btn.active {{
    background: #2c3e50;
    color: #f1c40f;
    border-color: #f39c12;
    font-weight: bold;
  }}
  
  .display-area {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 16px 20px;
    gap: 14px;
  }}
  .canvas-wrapper {{
    background: #0a0a0a;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
    border-radius: 6px;
    border: 2px solid #333;
  }}
  canvas {{
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    width: 680px;
    height: 350px;
    background: #252525;
    box-shadow: 0 4px 15px rgba(0,0,0,0.7);
  }}
  
  .info-card {{
    background: #222;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .info-title {{ font-size: 16px; font-weight: bold; color: #f4d03f; }}
  .info-desc {{ font-size: 14px; color: #ccc; line-height: 1.5; }}
  
  .footer-bar {{
    background: #252525;
    padding: 10px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 2px solid #3a3a3a;
    font-size: 13px;
    color: #aaa;
  }}
  .key-hint {{
    color: #81d4fa;
    font-family: monospace;
    font-weight: bold;
  }}
</style>
</head>
<body>

<div class="studio-frame">
  <div class="studio-header">
    <div class="studio-title" id="mainHeader">🎬 Divina Ludus — 컷씬 검토 스튜디오</div>
    <div class="studio-hud" id="hudText">[Native 296x152 60FPS]</div>
  </div>

  <div class="main-content">
    <div class="sidebar" id="sidebar"></div>

    <div class="display-area">
      <div class="canvas-wrapper">
        <canvas id="retroCanvas" width="296" height="152"></canvas>
      </div>

      <div class="info-card">
        <div class="info-title" id="cardTitle">제목</div>
        <div class="info-desc" id="cardDesc">설명</div>
      </div>
    </div>
  </div>

  <div class="footer-bar">
    <div>조작: <span class="key-hint">[1~7] 숫자키</span>로 씬 이동 | <span class="key-hint">[Tab]</span> 팩 전환 | 마우스 클릭 가능</div>
    <div style="color: #2ecc71;">● 네이티브 296x152 영화적 4X 도트 렌더러</div>
  </div>
</div>

<script>
  const data = {studio_json};
  const canvas = document.getElementById('retroCanvas');
  const ctx = canvas.getContext('2d');
  
  let curPackIdx = 1; // 기본: 제임스와 슈퍼 복숭아부터 검토!
  let curActIdx = 0;
  let curFrame = 0;
  let isPaused = false;
  
  const sidebar = document.getElementById('sidebar');
  
  function renderSidebar() {{
    sidebar.innerHTML = '';
    data.packs.forEach((pack, pIdx) => {{
      const pHead = document.createElement('div');
      pHead.className = 'pack-header';
      pHead.innerText = pack.pack_name;
      sidebar.appendChild(pHead);
      
      pack.acts.forEach((act, aIdx) => {{
        const btn = document.createElement('button');
        btn.className = 'nav-btn' + (pIdx === curPackIdx && aIdx === curActIdx ? ' active' : '');
        btn.innerText = `[${{aIdx+1}}] ${{act.title}}`;
        btn.onclick = () => selectScene(pIdx, aIdx);
        sidebar.appendChild(btn);
      }});
    }});
  }}
  
  function selectScene(pIdx, aIdx) {{
    curPackIdx = pIdx;
    curActIdx = aIdx;
    curFrame = 0;
    
    renderSidebar();
    
    const pack = data.packs[curPackIdx];
    const act = pack.acts[curActIdx];
    
    document.getElementById('mainHeader').innerText = `🎬 Divina Ludus — ${{pack.pack_name}}`;
    document.getElementById('cardTitle').innerText = `${{pack.pack_name}} · ${{act.title}}`;
    document.getElementById('cardDesc').innerText = act.desc;
    document.getElementById('hudText').innerText = `[${{act.title}} | F1/6 Native 296x152]`;
    
    renderCurrentFrame();
  }}
  
  function renderCurrentFrame() {{
    const pack = data.packs[curPackIdx];
    const act = pack.acts[curActIdx];
    const rleStr = act.rle_frames[curFrame];
    const imgData = ctx.createImageData(296, 152);
    
    const chunks = rleStr.split(',');
    let pIdx = 0;
    for (let i = 0; i < chunks.length; i++) {{
      const parts = chunks[i].split('_');
      const count = parseInt(parts[0]);
      const colorIdx = parseInt(parts[1]);
      
      const hex = data.palette[colorIdx];
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      
      for (let c = 0; c < count; c++) {{
        imgData.data[pIdx] = r;
        imgData.data[pIdx + 1] = g;
        imgData.data[pIdx + 2] = b;
        imgData.data[pIdx + 3] = 255;
        pIdx += 4;
      }}
    }}
    ctx.putImageData(imgData, 0, 0);
    
    const hud = document.getElementById('hudText');
    if (curFrame === 2) {{
      hud.innerText = `[${{act.title}} | ★ F3 다이아몬드 스파클 ★]`;
      hud.style.color = "#f4d03f";
    }} else {{
      hud.innerText = `[${{act.title}} | F${{curFrame+1}}/6 Native 296x152]`;
      hud.style.color = "#81d4fa";
    }}
  }}
  
  setInterval(() => {{
    if (isPaused) return;
    const pack = data.packs[curPackIdx];
    const act = pack.acts[curActIdx];
    curFrame = (curFrame + 1) % act.rle_frames.length;
    renderCurrentFrame();
  }}, 750);
  
  selectScene(1, 0); // 제임스와 슈퍼 복숭아 1막 자동 로드
  
  window.addEventListener('keydown', (e) => {{
    const num = parseInt(e.key);
    const pack = data.packs[curPackIdx];
    if (num >= 1 && num <= pack.acts.length) {{
      selectScene(curPackIdx, num - 1);
    }} else if (e.code === 'Tab') {{
      e.preventDefault();
      curPackIdx = (curPackIdx + 1) % data.packs.length;
      selectScene(curPackIdx, 0);
    }} else if (e.code === 'Space') {{
      isPaused = !isPaused;
    }}
  }});
  
  window.addEventListener('wheel', (e) => e.preventDefault(), {{ passive: false }});
</script>

</body>
</html>
"""
    studio_path = "/mnt/d/game/images/studio.html"
    with open(studio_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 4대 명작 통합 검토 스튜디오 배포 완료: {studio_path}")

if __name__ == "__main__":
    build_all_packs_studio()
