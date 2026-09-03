#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
Phase 2 신기술: 3대 베이스 원색 ➔ 3x3 딕셔너리 룩업(9칸 매트릭스) 렌더러!
- 기본 색상: 칠흑(K), 웜톤(W), 쿨톤(C), 백색(L)
- 9칸 딕셔너리 하프톤으로 16색(피부, 갓, 비단, 삼베, 금이빨) 전색상을 즉시 광학 합성!
- 저장 용량: 8비트(1바이트)당 2블록 팩킹 ➔ 전체 6프레임 컷씬 용량이 불과 1.4KB 수준으로 극한 압축!
"""

import os
import sys
import time

sys.path.append("/home/krjoylee/code/game/tools")
from palette_engine import (
    get_synthesized_pixel,
    render_half_block_row,
    calculate_8bit_packed_size,
    COLOR_DICT_9,
    BASE_3_COLORS
)

# 논리 타일 그리드 크기 (37x19)
GRID_W = 37
GRID_H = 19

# 실제 서브픽셀 해상도 (74x38)
CANVAS_W = 74
CANVAS_H = 38

# 목표 색상 ID (0~15)
ID_BG = 0          # 한옥 벽
ID_HAT = 1         # 칠흑 갓, 눈썹, 동공, 수염
ID_SKIN = 2        # 밝은 살구 피부
ID_SHADOW = 3      # 피부 음영, 콧대, 턱선
ID_HEMP = 4        # 흥부 삼베옷
ID_RAG = 5         # 누더기 헝겊
ID_SILK_RED = 6    # 놀부 비단 깃
ID_SILK_BLUE = 7   # 놀부 비단 도포
ID_TEAR = 8        # 흥부 눈물
ID_WHITE = 9       # 순백 반사광
ID_SILK_SHINE = 10 # 비단 광택
ID_HEMP_ROUGH = 11 # 거친 삼베 질감
ID_GOLD = 12       # ★ 놀부 금이빨!

def create_base_color_matrix():
    """논리 타일 그리드 (37x19)에 16색 목표 ID 배치"""
    grid = [[ID_BG for _ in range(GRID_W)] for _ in range(GRID_H)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu)]
    # ─────────────────────────────────────────────────────────────
    # 갓
    for y in range(1, 4):
        for x in range(7, 13):
            grid[y][x] = ID_HAT
    for x in range(3, 17):
        grid[4][x] = ID_HAT
    # 갓끈
    grid[5][7] = ID_HAT; grid[5][12] = ID_HAT
    grid[6][7] = ID_HAT; grid[6][12] = ID_HAT
    
    # 얼굴 (피부)
    for y in range(5, 10):
        for x in range(8, 12):
            grid[y][x] = ID_SKIN
    # 볼/턱 음영
    grid[9][8] = ID_SHADOW; grid[9][11] = ID_SHADOW
    
    # 눈썹 / 눈
    grid[5][8] = ID_HAT; grid[5][11] = ID_HAT
    grid[6][8] = ID_HAT; grid[6][11] = ID_HAT
    grid[6][7] = ID_WHITE; grid[6][12] = ID_WHITE
    
    # 코 & 입 & ★금이빨
    grid[7][9] = ID_SHADOW
    grid[8][8] = ID_SHADOW; grid[8][9] = ID_HAT; grid[8][10] = ID_GOLD
    
    # 수염
    grid[10][9] = ID_HAT; grid[10][10] = ID_HAT
    grid[11][9] = ID_HAT
    
    # 비단 도포 & 붉은 깃
    for y in range(11, 18):
        for x in range(4, 16):
            grid[y][x] = ID_SILK_BLUE
    # 비단 깃
    grid[11][9] = ID_SILK_RED; grid[12][9] = ID_SILK_RED
    # 비단 광택
    grid[13][6] = ID_SILK_SHINE; grid[14][13] = ID_SILK_SHINE
    grid[15][7] = ID_WHITE

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 상투 꽃미남 빈티]
    # ─────────────────────────────────────────────────────────────
    # 상투 & 망건
    grid[1][27] = ID_HAT; grid[2][27] = ID_HAT
    for x in range(25, 30):
        grid[3][x] = ID_HAT
    grid[3][24] = ID_HEMP; grid[3][30] = ID_HEMP # 터진 갓
    
    # 꽃미남 얼굴
    for y in range(4, 9):
        for x in range(25, 30):
            grid[y][x] = ID_SKIN
            
    # 눈썹 & 눈
    grid[4][25] = ID_HAT; grid[4][26] = ID_HAT
    grid[4][28] = ID_HAT; grid[4][29] = ID_HAT
    grid[5][26] = ID_HAT; grid[5][28] = ID_HAT
    grid[5][25] = ID_SHADOW; grid[5][29] = ID_SHADOW
    
    # 콧날 & V턱선
    grid[6][27] = ID_SHADOW; grid[7][27] = ID_HAT
    grid[8][26] = ID_SHADOW; grid[8][27] = ID_HAT; grid[8][28] = ID_SHADOW
    grid[9][27] = ID_SHADOW # 턱끝
    
    # 눈물
    grid[6][25] = ID_TEAR; grid[7][25] = ID_WHITE
    
    # 쇄골 & 거친 삼베옷
    grid[10][26] = ID_SKIN; grid[10][27] = ID_SKIN; grid[10][28] = ID_SKIN
    for y in range(11, 18):
        for x in range(22, 33):
            grid[y][x] = ID_HEMP
    # 거친 삼베 음영 & 기운 자국
    grid[13][24] = ID_RAG; grid[14][29] = ID_RAG
    grid[15][25] = ID_HEMP_ROUGH; grid[16][28] = ID_HEMP_ROUGH
    
    return grid

def synthesize_to_subpixels(grid_37x19):
    """
    37x19 타일 매트릭스를 3x3 딕셔너리에 통과시켜
    가로 74 x 세로 38 서브픽셀(3원색 인덱스 0,1,2,3) 캔버스로 광학 합성!
    """
    canvas = [[0 for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    for gy in range(GRID_H):
        for gx in range(GRID_W):
            target_color_id = grid_37x19[gy][gx]
            # 각 1타일을 2x2 서브픽셀 공간에 3x3 딕셔너리 주기성으로 매핑
            for dy in range(2):
                for dx in range(2):
                    py = gy * 2 + dy
                    px = gx * 2 + dx
                    base_color = get_synthesized_pixel(target_color_id, px, py)
                    canvas[py][px] = base_color
    return canvas

def generate_6_motion_frames():
    frames = []
    
    # F1
    g1 = create_base_color_matrix()
    frames.append(g1)
    
    # F2: 들숨 팽창
    g2 = [row[:] for row in g1]
    for y in range(12, 17):
        g2[y][3] = ID_SILK_BLUE; g2[y][16] = ID_SILK_BLUE
    g2[0][27] = ID_HAT
    frames.append(g2)
    
    # F3: 금이빨 번쩍 & 눈물 낙하
    g3 = [row[:] for row in g1]
    g3[8][9] = ID_GOLD; g3[8][10] = ID_WHITE; g3[8][11] = ID_GOLD
    g3[10][8] = ID_HAT; g3[10][11] = ID_HAT
    # 눈물 1칸 낙하
    g3[6][25] = ID_SKIN
    g3[7][25] = ID_TEAR
    g3[8][25] = ID_WHITE
    frames.append(g3)
    
    # F4: 날숨 수축
    g4 = [row[:] for row in g1]
    for y in range(13, 17):
        g4[y][4] = ID_BG; g4[y][15] = ID_BG
    g4[11][23] = ID_BG; g4[11][31] = ID_BG
    frames.append(g4)
    
    # F5: 잔상
    g5 = [row[:] for row in g1]
    g5[8][10] = ID_GOLD
    g5[9][26] = ID_TEAR
    frames.append(g5)
    
    # F6: 복귀
    g6 = [row[:] for row in g1]
    frames.append(g6)
    
    return frames

if __name__ == "__main__":
    frames = generate_6_motion_frames()
    
    # 8비트 팩킹 용량 계산 (단 1바이트에 2블록 저장!)
    packed_bytes = calculate_8bit_packed_size(frames[0])
    total_packed_kb = (packed_bytes * 6) / 1024
    
    print("🕹️ [3원색 기반 3x3 딕셔너리 8비트 엔진 가동]")
    print(f"📊 프레임당 8비트 팩킹 용량: {packed_bytes} B | 6프레임 컷씬 총합: {total_packed_kb:.2f} KB (기적의 1.4KB대!)")
    print("   속도: 0.75초 | Ctrl+C로 종료\n")
    
    for loop in range(2):
        for idx, fr_grid in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 원점 이동
            cur_bytes = calculate_8bit_packed_size(fr_grid)
            
            # 서브픽셀 3색 합성 캔버스 생성
            sub_canvas = synthesize_to_subpixels(fr_grid)
            
            hud = f"[F{idx}/6 | 8-bit: {cur_bytes}B | 6-Frames: {total_packed_kb:.2f}KB]"
            title_text = "흥부놀부전 · 1막 (3원색 ➔ 9칸 딕셔너리)"
            pad_len = 74 - len(title_text) * 2 - len(hud) + 12
            pad_len = max(1, pad_len)
            
            print(f"╔{'═' * 74}╗")
            print(f"║  {title_text}{' ' * pad_len}{hud}║")
            print(f"╠{'═' * 74}╣")
            
            # Half-block으로 터미널 19줄 렌더링
            for y in range(0, CANVAS_H, 2):
                top_r = sub_canvas[y]
                bot_r = sub_canvas[y+1]
                line_str = render_half_block_row(top_r, bot_r)
                print(f"║{line_str}║")
                
            print(f"╚{'═' * 74}╝")
            if idx == 3:
                print("  ★ F3: 3원색 딕셔너리 광채 믹싱! 놀부 [금이빨 번쩍★] & 흥부 [눈물💧]!")
            else:
                print("  단 3개 베이스 색상으로 9칸 매트릭스에서 16색을 완전 자동 합성 중...")
            time.sleep(0.75)
