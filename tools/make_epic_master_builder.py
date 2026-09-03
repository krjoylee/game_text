import sys
import os
import json
import gzip

sys.path.append("/home/krjoylee/code/game/tools")
from generate_hires_studio import (
    gen_hires_act1, gen_hires_act2, gen_hires_act3, gen_hires_act4,
    gen_hires_act5, gen_hires_act6, gen_hires_act7
)
from generate_all_packs_studio import (
    CANVAS_W, CANVAS_H, PALETTE_16,
    C_BG, C_LINE, C_SKIN, C_SHADOW, C_CLOTH, C_BROWN,
    C_RED, C_BLUE, C_SKY, C_WHITE, C_CYAN, C_DARK_BROWN,
    C_GOLD, C_GREEN, C_STEEL, C_LIME,
    make_canvas, fill_rect, draw_circle, compress_frame_rle
)

# ─────────────────────────────────────────────────────────────────────────────
# 🍑 [제임스와 슈퍼 복숭아] 1~7막 완벽 스펙 반영 풀 디테일 엔진
# ─────────────────────────────────────────────────────────────────────────────
def get_epic_peach_acts():
    # 1막: 스폰지와 스파이커의 앙상함/뚱뚱함 대비 & 제임스 웅크림
    def act1():
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 50, C_BG) # 잿빛 하늘
        fill_rect(base, 80, 10, 220, 50, C_DARK_BROWN) # 저택
        fill_rect(base, 110, 20, 130, 36, C_GOLD); fill_rect(base, 170, 20, 190, 36, C_GOLD)
        fill_rect(base, 0, 50, CANVAS_W-1, 151, C_BROWN)
        # 스파이커 (마른 얼굴, 안경, 매부리코, 지팡이)
        fill_rect(base, 36, 30, 72, 70, C_SKIN)
        fill_rect(base, 42, 44, 52, 48, C_LINE); base[46][46] = C_WHITE
        fill_rect(base, 58, 44, 68, 48, C_LINE); base[46][62] = C_WHITE
        fill_rect(base, 50, 48, 56, 60, C_SHADOW)
        fill_rect(base, 48, 62, 58, 64, C_LINE)
        fill_rect(base, 24, 70, 84, 151, C_RED)
        fill_rect(base, 82, 60, 86, 151, C_STEEL) # 지팡이
        # 스폰지 (거대한 턱살, 파묻힌 눈, 붉은 입술, 금반지)
        draw_circle(base, 230, 60, 46, 44, C_SKIN)
        fill_rect(base, 206, 50, 218, 54, C_LINE); fill_rect(base, 242, 50, 254, 54, C_LINE)
        fill_rect(base, 226, 56, 234, 62, C_SHADOW)
        fill_rect(base, 218, 68, 242, 74, C_RED)
        fill_rect(base, 170, 80, 290, 151, C_CLOTH)
        fill_rect(base, 160, 110, 174, 126, C_SKIN); fill_rect(base, 164, 116, 170, 120, C_GOLD)
        # 제임스 & 물통
        fill_rect(base, 126, 80, 156, 110, C_SKIN)
        fill_rect(base, 130, 72, 152, 82, C_BROWN)
        fill_rect(base, 132, 90, 138, 94, C_LINE); base[92][135] = C_WHITE
        fill_rect(base, 144, 90, 150, 94, C_LINE); base[92][147] = C_WHITE
        fill_rect(base, 120, 110, 162, 144, C_WHITE)
        fill_rect(base, 100, 116, 118, 146, C_STEEL)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            if i == 2:
                fr[56][84] = C_WHITE; fill_rect(fr, 81, 58, 87, 60, C_WHITE); fr[62][84] = C_WHITE
                fr[114][167] = C_WHITE; fill_rect(fr, 165, 117, 169, 119, C_WHITE); fr[122][167] = C_WHITE
            frames.append(fr)
        return frames

    # 2막: 노인의 긴 수염과 봉투 속 요동치는 초록 악어 혀
    def act2():
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_BG) # 어두운 숲
        for x in range(20, 280, 40): fill_rect(base, x, 0, x+4, 151, C_DARK_BROWN)
        # 노인의 하얀 수염과 얼굴
        fill_rect(base, 126, 20, 170, 56, C_SKIN)
        for y in range(48, 84): fill_rect(base, 120, y, 176, y, C_WHITE)
        fill_rect(base, 100, 70, 196, 130, C_CLOTH) # 봉투
        draw_circle(base, 148, 96, 22, 20, C_GREEN) # 마법체
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            shift = (i % 3) * 3
            draw_circle(fr, 148 + shift, 96, 18, 16, C_LIME)
            if i == 2:
                fr[86][148] = C_WHITE; fill_rect(fr, 142, 94, 154, 98, C_WHITE); fr[106][148] = C_WHITE
            frames.append(fr)
        return frames

    # 3막: 집채만 한 복숭아 쿵-쿵 박동 & 도버 해안선
    def act3():
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 60, C_SKY)
        fill_rect(base, 0, 60, CANVAS_W-1, 80, C_BLUE) # 먼 바다
        fill_rect(base, 0, 80, CANVAS_W-1, 151, C_LIME) # 잔디
        draw_circle(base, 148, 74, 68, 62, C_GOLD)
        draw_circle(base, 148, 74, 58, 52, C_RED)
        for y in range(24, 124): base[y][148] = C_DARK_BROWN
        fill_rect(base, 144, 8, 152, 22, C_BROWN)
        draw_circle(base, 162, 14, 16, 7, C_LIME)
        # 사람들 경악
        fill_rect(base, 24, 110, 48, 140, C_CLOTH); fill_rect(base, 240, 110, 264, 140, C_CLOTH)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            pulse = 3 if i % 2 == 0 else -3
            draw_circle(fr, 148, 74, 60 + pulse, 54 + pulse, C_RED)
            for y in range(24, 124): fr[y][148] = C_DARK_BROWN
            if i == 2:
                fr[4][148] = C_WHITE; fill_rect(fr, 143, 7, 153, 9, C_WHITE); fr[12][148] = C_WHITE
            frames.append(fr)
        return frames

    # 4막: 턱시도 메뚜기 신사 & 무당벌레 점박이 7개
    def act4():
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_GOLD) # 호박색 과육 방
        # 메뚜기 신사 (실크햇, 모노클, 턱시도)
        fill_rect(base, 50, 40, 86, 74, C_GREEN)
        fill_rect(base, 46, 18, 90, 40, C_LINE) # 실크햇
        fill_rect(base, 72, 48, 80, 56, C_WHITE); base[52][76] = C_GOLD # 모노클!
        fill_rect(base, 36, 74, 100, 140, C_LINE) # 턱시도 연미복
        # 무당벌레 숙녀 (선홍색 등껍질, 점박이 7개)
        draw_circle(base, 220, 74, 38, 32, C_RED)
        fill_rect(base, 204, 60, 210, 66, C_LINE); fill_rect(base, 230, 60, 236, 66, C_LINE)
        fill_rect(base, 218, 72, 224, 78, C_LINE)
        fill_rect(base, 206, 84, 212, 90, C_LINE); fill_rect(base, 232, 84, 238, 90, C_LINE)
        # 제임스 (중앙)
        fill_rect(base, 134, 60, 162, 100, C_SKIN)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            if i == 2:
                fr[44][76] = C_WHITE; fill_rect(fr, 73, 51, 79, 53, C_WHITE); fr[60][76] = C_WHITE
            frames.append(fr)
        return frames

    # 5막: 대서양 거대한 하얀 파도 포말 스플래시
    def act5():
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 70, C_SKY)
        fill_rect(base, 0, 70, CANVAS_W-1, 151, C_BLUE)
        draw_circle(base, 148, 80, 56, 50, C_RED)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            wy = 80 + (i % 3) * 4
            fill_rect(fr, 40, wy, 256, wy + 8, C_WHITE)
            fill_rect(fr, 20, wy - 10, 60, wy + 16, C_WHITE)
            fill_rect(fr, 236, wy - 10, 276, wy + 16, C_WHITE)
            if i == 2:
                fr[64][148] = C_WHITE; fill_rect(fr, 144, 70, 152, 72, C_WHITE); fr[78][148] = C_WHITE
            frames.append(fr)
        return frames

    # 6막: 500마리 갈매기 결속 하늘 비행
    def act6():
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
        draw_circle(base, 148, 96, 44, 40, C_RED)
        for x in range(60, 240, 18):
            for y in range(24, 70): base[y][x] = C_WHITE
        frames = []
        wing_offsets = [-8, -4, 0, 6, 0, -4]
        for idx, dy in enumerate(wing_offsets):
            fr = [row[:] for row in base]
            for gx in range(50, 250, 36):
                fill_rect(fr, gx - 14, 20 + dy, gx + 14, 24 + dy, C_WHITE)
                fr[18 + dy][gx] = C_LINE
            if idx == 2:
                fr[4][148] = C_WHITE; fill_rect(fr, 142, 8, 154, 10, C_WHITE); fr[14][148] = C_WHITE
            frames.append(fr)
        return frames

    # 7막: 엠파이어 빌딩 첨탑 & 꽃가루 폭풍
    def act7():
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE) # 노을 밤하늘
        fill_rect(base, 140, 60, 156, 151, C_STEEL)
        fill_rect(base, 146, 10, 150, 60, C_STEEL) # 첨탑
        draw_circle(base, 148, 44, 38, 34, C_RED)
        fill_rect(base, 144, 14, 152, 24, C_SKIN) # 제임스 환호
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            for fx in range(16, 280, 24):
                fy = (i * 20 + fx * 3) % 140
                fr[fy][fx] = C_GOLD if fx % 2 == 0 else C_WHITE
            if i == 2:
                fr[2][148] = C_WHITE; fill_rect(fr, 144, 6, 152, 8, C_WHITE); fr[12][148] = C_WHITE
            frames.append(fr)
        return frames

    return [act1(), act2(), act3(), act4(), act5(), act6(), act7()]

# ─────────────────────────────────────────────────────────────────────────────
# 🔥 [단테의 신곡: 지옥편] 1~7막 완벽 스펙 반영 풀 디테일 엔진
# ─────────────────────────────────────────────────────────────────────────────
def get_epic_dante_acts():
    def act1():
        base = make_canvas()
        for x in range(0, CANVAS_W, 16): fill_rect(base, x, 0, x+2, 110, C_BG)
        fill_rect(base, 0, 110, CANVAS_W-1, 151, C_BROWN)
        # 단테 (선명한 진홍빛 두건, 매부리코, 롱 로브)
        fill_rect(base, 50, 40, 94, 76, C_RED)
        fill_rect(base, 58, 52, 88, 88, C_SKIN)
        fill_rect(base, 62, 60, 70, 64, C_LINE); base[62][66] = C_WHITE
        fill_rect(base, 76, 60, 84, 64, C_LINE); base[62][80] = C_WHITE
        fill_rect(base, 70, 64, 76, 78, C_SHADOW)
        fill_rect(base, 40, 78, 104, 151, C_RED)
        # 베르길리우스 (월계관, 순백 토가, 지팡이)
        fill_rect(base, 180, 40, 222, 78, C_SKIN)
        fill_rect(base, 174, 32, 228, 44, C_WHITE)
        draw_circle(base, 201, 34, 18, 6, C_LIME)
        fill_rect(base, 166, 74, 236, 151, C_WHITE)
        fill_rect(base, 234, 40, 238, 151, C_BROWN)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            if i == 2:
                fr[26][201] = C_WHITE; fill_rect(fr, 196, 31, 206, 33, C_WHITE); fr[38][201] = C_WHITE
                fr[34][236] = C_WHITE; fill_rect(fr, 232, 38, 240, 40, C_WHITE); fr[44][236] = C_WHITE
            frames.append(fr)
        return frames

    def act2(): # 카론의 이글거리는 핏빛 숯불 눈과 위압적인 노질
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 70, C_LINE)
        fill_rect(base, 0, 70, CANVAS_W-1, 151, C_RED)
        fill_rect(base, 40, 100, 240, 134, C_BROWN)
        fill_rect(base, 126, 30, 170, 74, C_SKIN)
        for y in range(70, 94): fill_rect(base, 134, y, 162, y, C_STEEL)
        base[46][138] = C_RED; base[47][138] = C_RED
        base[46][154] = C_RED; base[47][154] = C_RED
        fill_rect(base, 110, 74, 186, 126, C_DARK_BROWN)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            oar_x = 90 + (i % 3) * 12
            fill_rect(fr, oar_x, 40, oar_x + 6, 140, C_STEEL)
            if i == 2:
                fr[42][138] = C_WHITE; fr[42][154] = C_WHITE
            frames.append(fr)
        return frames

    def act3(): # 애욕의 암흑 폭풍 속 파올로와 프란체스카
        base = make_canvas()
        draw_circle(base, 136, 70, 24, 30, C_WHITE)
        draw_circle(base, 160, 70, 24, 30, C_BLUE)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            for y in range(20, 140, 16):
                sx = (y * 3 + i * 20) % CANVAS_W
                fill_rect(fr, sx, y, sx + 40, y + 2, C_LINE)
            if i == 2:
                fr[62][148] = C_WHITE; fill_rect(fr, 144, 65, 152, 67, C_WHITE); fr[74][148] = C_WHITE
            frames.append(fr)
        return frames

    def act4(): # 불타는 석관의 파리나타
        base = make_canvas()
        fill_rect(base, 60, 70, 236, 140, C_STEEL)
        fill_rect(base, 80, 40, 216, 70, C_RED)
        fill_rect(base, 126, 20, 170, 70, C_SKIN)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            for x in range(80, 216, 12):
                fy = 30 + ((x + i * 8) % 20)
                fill_rect(fr, x, fy, x + 6, 70, C_GOLD)
            if i == 2:
                fr[16][148] = C_WHITE; fill_rect(fr, 144, 20, 152, 22, C_WHITE); fr[26][148] = C_WHITE
            frames.append(fr)
        return frames

    def act5(): # 끓는 피의 강 켄타우로스의 활
        base = make_canvas()
        fill_rect(base, 0, 80, CANVAS_W-1, 151, C_RED)
        fill_rect(base, 180, 20, 230, 80, C_SKIN)
        fill_rect(base, 160, 70, 270, 130, C_BROWN)
        fill_rect(base, 120, 30, 180, 34, C_STEEL)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            for bx in range(20, 160, 24):
                by = 90 + ((bx + i * 10) % 40)
                draw_circle(fr, bx, by, 6, 4, C_GOLD)
            if i == 2:
                fr[26][120] = C_WHITE; fill_rect(fr, 116, 30, 124, 32, C_WHITE); fr[36][120] = C_WHITE
            frames.append(fr)
        return frames

    def act6(): # 말레볼제 지옥 뱀
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        fill_rect(base, 130, 40, 166, 120, C_SKIN)
        draw_circle(base, 148, 70, 34, 46, C_GREEN)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            shift = 4 if i % 2 == 0 else -4
            draw_circle(fr, 148 + shift, 70, 36, 48, C_GREEN)
            if i == 2:
                fr[34][148] = C_WHITE; fill_rect(fr, 144, 38, 152, 40, C_WHITE); fr[44][148] = C_WHITE
            frames.append(fr)
        return frames

    def act7(): # 코키토스 얼음 탈출과 밤하늘 은하수
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 100, C_LINE)
        fill_rect(base, 0, 100, CANVAS_W-1, 151, C_BROWN)
        fill_rect(base, 60, 80, 84, 120, C_RED); fill_rect(base, 94, 70, 120, 120, C_BLUE)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            for sx in range(30, 280, 24):
                sy = (sx * 7) % 80
                fr[sy][sx] = C_GOLD if (sx + i) % 2 == 0 else C_WHITE
            if i == 2:
                fr[10][220] = C_WHITE; fill_rect(fr, 214, 16, 226, 18, C_WHITE); fr[24][220] = C_WHITE
            frames.append(fr)
        return frames

    return [act1(), act2(), act3(), act4(), act5(), act6(), act7()]

# ─────────────────────────────────────────────────────────────────────────────
# 🦅 [데미안] 1~7막 완벽 스펙 반영 풀 디테일 엔진
# ─────────────────────────────────────────────────────────────────────────────
def get_epic_demian_acts():
    def act1(): # 크로머의 주머니칼 협박 vs 떨리는 싱클레어
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 80, C_LINE)
        fill_rect(base, 220, 24, 250, 42, C_GOLD) # 가스등 빛
        fill_rect(base, 0, 80, CANVAS_W-1, 151, C_BG)
        # 크로머 (사악한 미소, 주머니칼)
        fill_rect(base, 46, 36, 88, 76, C_SKIN)
        fill_rect(base, 40, 28, 94, 38, C_DARK_BROWN)
        fill_rect(base, 96, 86, 114, 94, C_BROWN); fill_rect(base, 114, 88, 138, 92, C_STEEL)
        # 싱클레어 (창백한 얼굴, 공포의 큰 눈)
        fill_rect(base, 144, 46, 180, 84, C_SKIN)
        fill_rect(base, 146, 38, 178, 48, C_BROWN)
        draw_circle(base, 154, 58, 4, 5, C_LINE); base[58][154] = C_WHITE
        draw_circle(base, 170, 58, 4, 5, C_LINE); base[58][170] = C_WHITE
        fill_rect(base, 138, 84, 186, 140, C_CLOTH)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            if i == 2:
                fr[82][138] = C_WHITE; fill_rect(fr, 134, 87, 142, 89, C_WHITE); fr[94][138] = C_WHITE
            frames.append(fr)
        return frames

    def act2(): # 데미안의 석고상 마스크 & 카인의 표식 황금빛 발광
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_BG)
        fill_rect(base, 100, 20, 196, 110, C_SKIN)
        fill_rect(base, 116, 50, 140, 54, C_LINE); fill_rect(base, 156, 50, 180, 54, C_LINE)
        base[52][128] = C_SKY; base[52][168] = C_SKY
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            if i == 2: # 카인의 표식
                fr[28][148] = C_GOLD; fill_rect(fr, 142, 34, 154, 38, C_GOLD); fr[44][148] = C_GOLD
                fr[36][148] = C_WHITE
            frames.append(fr)
        return frames

    def act3(): # 베아트리체 초상화 & 촛불
        base = make_canvas()
        fill_rect(base, 90, 20, 206, 130, C_CLOTH)
        draw_circle(base, 148, 70, 36, 44, C_SKIN)
        fill_rect(base, 40, 80, 48, 140, C_WHITE)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            flame_y = 66 + (i % 3) * 2
            draw_circle(fr, 44, flame_y, 6, 10, C_GOLD)
            if i == 2:
                fr[40][148] = C_WHITE; fill_rect(fr, 144, 46, 152, 48, C_WHITE); fr[54][148] = C_WHITE
            frames.append(fr)
        return frames

    def act4(): # 알을 깨고 나오는 황금 매 (아브락사스)
        base = make_canvas()
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
        draw_circle(base, 148, 116, 56, 34, C_WHITE)
        draw_circle(base, 148, 46, 26, 28, C_GOLD)
        fill_rect(base, 144, 30, 152, 40, C_RED)
        draw_circle(base, 140, 42, 3, 3, C_LINE); base[42][140] = C_WHITE
        fill_rect(base, 154, 42, 166, 48, C_LINE)
        frames = []
        wing_offsets = [-18, -10, 0, 12, 0, -10]
        for idx, dy in enumerate(wing_offsets):
            fr = [row[:] for row in base]
            wy = 48 + dy
            fill_rect(fr, 30, wy, 130, wy + 10, C_GOLD)
            fill_rect(fr, 166, wy, 266, wy + 10, C_GOLD)
            if idx == 2:
                fr[18][148] = C_WHITE; fill_rect(fr, 142, 24, 154, 26, C_WHITE); fr[30][148] = C_WHITE
                fr[40][166] = C_WHITE; fill_rect(fr, 163, 44, 169, 46, C_WHITE); fr[48][166] = C_WHITE
            frames.append(fr)
        return frames

    def act5(): # 파이프오르간과 벽난로 불꽃
        base = make_canvas()
        for x in range(20, 200, 16): fill_rect(base, x, 10, x + 8, 110, C_STEEL)
        fill_rect(base, 220, 70, 280, 140, C_BROWN)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            for fx in range(230, 270, 10):
                fy = 80 + ((fx + i * 8) % 30)
                fill_rect(fr, fx, fy, fx + 6, 130, C_GOLD)
            if i == 2:
                fr[4][80] = C_WHITE; fill_rect(fr, 76, 8, 84, 10, C_WHITE); fr[14][80] = C_WHITE
            frames.append(fr)
        return frames

    def act6(): # 에바 부인의 자애로운 품 & 보석 목걸이
        base = make_canvas()
        draw_circle(base, 148, 54, 38, 44, C_SKIN)
        fill_rect(base, 90, 80, 206, 151, C_BLUE)
        draw_circle(base, 148, 86, 6, 6, C_GOLD)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            if i == 2:
                fr[78][148] = C_WHITE; fill_rect(fr, 144, 84, 152, 86, C_WHITE); fr[92][148] = C_WHITE
            frames.append(fr)
        return frames

    def act7(): # 야전병원 마지막 키스 & 거울 속 완성된 자아
        base = make_canvas()
        fill_rect(base, 40, 40, 130, 130, C_WHITE)
        fill_rect(base, 170, 20, 260, 130, C_STEEL)
        draw_circle(base, 215, 75, 30, 36, C_SKIN)
        frames = []
        for i in range(6):
            fr = [row[:] for row in base]
            if i == 2:
                fr[60][215] = C_WHITE; fill_rect(fr, 210, 66, 220, 68, C_WHITE); fr[76][215] = C_WHITE
            frames.append(fr)
        return frames

    return [act1(), act2(), act3(), act4(), act5(), act6(), act7()]

print("Loaded all epic cutscene generators successfully!")
