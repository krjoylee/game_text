#!/usr/bin/env python3
"""
tools/make_ultra_james_dante_cutscenes.py
《제임스와 슈퍼 복숭아》 & 《단테의 신곡: 지옥편》 정밀 픽셀 아트 제너레이터
- 단독 덩어리가 아닌 인물 간 대화/상황 인터랙션 구도 완벽 구현
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
# 🍑 [제임스와 슈퍼 복숭아]
# ─────────────────────────────────────────────────────────────────────────────
def gen_peach_act2_ultra(): # 2막: 안갯속 노인의 신비로운 봉투 건넴 vs 제임스
    base = make_canvas()
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
    # 고목 나무의 거대한 뿌리
    fill_rect(base, 200, 0, 260, 151, C_BROWN)
    # 노인 (좌측): 하얀 수염, 로브, 빛나는 봉투를 앞으로 내밈
    fill_rect(base, 40, 30, 84, 80, C_SKIN)
    for y in range(60, 110): fill_rect(base, 34, y, 90, y, C_WHITE) # 풍성한 하얀 수염
    fill_rect(base, 20, 80, 100, 151, C_LINE)
    # 노인이 건네는 하얀 종이봉투와 초록 마법체 (Col 90~144, Row 70~110)
    fill_rect(base, 92, 70, 144, 114, C_WHITE)
    draw_circle(base, 118, 92, 14, 14, C_GREEN)
    # 제임스 (우측): 눈을 크게 뜨고 조심스레 두 손을 뻗음
    draw_circle(base, 186, 60, 18, 18, C_BROWN)
    fill_rect(base, 172, 60, 200, 94, C_SKIN)
    fill_rect(base, 174, 68, 182, 72, C_LINE); base[70][178] = C_WHITE
    fill_rect(base, 156, 90, 214, 151, C_CLOTH) # 멜빵
    fill_rect(base, 140, 88, 160, 98, C_SKIN) # 뻗은 두 손
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        shift = (i % 3) * 2
        draw_circle(fr, 118 + shift, 92, 10, 10, C_LIME)
        if i == 2:
            fr[78][118] = C_WHITE; fill_rect(fr, 112, 84, 124, 86, C_WHITE); fr[92][118] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 🔥 [단테의 신곡: 지옥편]
# ─────────────────────────────────────────────────────────────────────────────
def gen_dante_act3_ultra(): # 3막: 애욕의 폭풍 속 부유하는 파올로와 프란체스카 vs 단테
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

print("Loaded ultra james & dante cutscenes!")
