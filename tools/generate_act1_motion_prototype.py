#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
Phase 2 신기술: 3x3 딕셔너리 패턴 하프톤 디더링 (Pattern Dithering Dictionary) 적용!
- 3x3 격자(9칸) 패턴을 통해 색상 A와 B를 조합하여 풍부한 중간색과 질감(비단 그라데이션, 고운 피부 음영) 표현!
- 픽셀 9개를 1개의 [1.5바이트 타일 코드]로 압축하여, 4배로 화질이 올라가도 용량은 오히려 절반 이하로 압축!
- 우상단 HUD: [타일 압축 크기 및 6프레임 총합 용량(불과 2KB 대!)] 표시
"""

import os
import sys
import time

sys.path.append("/home/krjoylee/code/game/tools")
from palette_engine import (
    render_half_block_canvas, 
    calculate_pattern_compressed_size,
    get_mixed_color_block,
    PALETTE_16
)

CANVAS_W = 74
CANVAS_H = 38  # 터미널 19줄 '▀'

# 16색 기본 인덱스
C_BG = 0          # 한옥 벽 회갈색
C_LINE = 1        # 칠흑 먹선, 갓, 수염
C_SKIN = 2        # 밝은 살구 피부
C_SHADOW = 3      # 피부 음영
C_HAT = 4         # 흥부 터진 갓, 삼베
C_RAG = 5         # 누더기 갈색
C_SILK_RED = 6    # 비단 깃 주홍
C_SILK_BLUE = 7   # 비단 도포 청색
C_TEAR = 8        # 눈물 하늘색
C_WHITE = 9       # 순백 반사광
C_SILK_SHINE = 10 # 청록 광택
C_HEMP_ROUGH = 11 # 거친 삼베
C_GOLD = 12       # ★ 놀부 금이빨 황금빛!

def create_base_canvas_with_3x3_dict():
    """3x3 딕셔너리 패턴으로 다채로운 중간색 질감을 합성한 캔버스"""
    canvas = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu) — 칠흑 갓 + 3x3 비단 그라데이션 믹싱]
    # ─────────────────────────────────────────────────────────────
    
    # 1. 칠흑 양반 갓 (Row 3~8)
    for y in range(3, 8):
        for x in range(15, 26):
            canvas[y][x] = C_LINE
    for x in range(7, 34):
        canvas[8][x] = C_LINE
    # 갓끈
    for y in range(9, 15):
        canvas[y][15] = C_LINE; canvas[y][25] = C_LINE
        
    # 2. 얼굴 & 3x3 하프톤 피부 음영 (살구 C_SKIN + 황토 C_SHADOW의 부드러운 그라데이션)
    for y in range(9, 21):
        for x in range(16, 25):
            # 얼굴 중심은 100% 뽀얀 살구, 턱과 볼 외곽은 3x3 50% 믹싱으로 자연스러운 입체 음영!
            if x in (16, 24) or y in (19, 20):
                canvas[y][x] = get_mixed_color_block(C_SKIN, C_SHADOW, "MIX_50", x, y)
            else:
                canvas[y][x] = C_SKIN
                
    # 3. 눈/눈썹
    canvas[10][17] = C_LINE; canvas[10][18] = C_LINE
    canvas[10][22] = C_LINE; canvas[10][23] = C_LINE
    canvas[12][17] = C_WHITE; canvas[12][18] = C_LINE; canvas[12][19] = C_WHITE
    canvas[12][21] = C_WHITE; canvas[12][22] = C_LINE; canvas[12][23] = C_WHITE
    
    # 4. 매부리코 & 사나운 입 & ★금이빨
    canvas[14][20] = C_SHADOW; canvas[15][20] = C_SHADOW; canvas[16][19] = C_LINE; canvas[16][20] = C_LINE
    canvas[17][18] = C_LINE; canvas[17][19] = C_LINE; canvas[17][20] = C_LINE; canvas[17][21] = C_LINE; canvas[17][22] = C_LINE
    canvas[18][19] = C_LINE
    canvas[18][20] = C_GOLD  # ★ 놀부 황금 앞니!
    canvas[18][21] = C_LINE
    
    # 5. 턱수염
    for y in range(21, 24):
        canvas[y][19] = C_LINE; canvas[y][20] = C_LINE; canvas[y][21] = C_LINE
    canvas[24][20] = C_LINE; canvas[25][20] = C_LINE
    
    # 6. 비단 도포 & 3x3 빗살무늬 광택 딕셔너리 합성 (SILK_STRIPE)
    for y in range(23, 37):
        for x in range(10, 31):
            # 군청색과 청록 광택을 3x3 빗살 패턴으로 믹싱하여 고급 비단 결 합성!
            canvas[y][x] = get_mixed_color_block(C_SILK_BLUE, C_SILK_SHINE, "SILK_STRIPE", x, y)
    # 화려한 붉은 깃
    for y in range(23, 30):
        canvas[y][19] = C_SILK_RED; canvas[y][20] = C_SILK_RED
    # 순백색 비단 하이라이트 반사광
    for y in range(26, 35, 4):
        canvas[y][13] = C_WHITE; canvas[y][27] = C_WHITE

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 3x3 격자 삼베옷 질감 & 수려한 이목구비]
    # ─────────────────────────────────────────────────────────────
    
    # 1. 솟아오른 상투 & 터진 갓
    canvas[2][54] = C_LINE; canvas[2][55] = C_LINE
    for y in range(3, 6):
        for x in range(53, 57):
            canvas[y][x] = C_LINE
    for x in range(50, 60):
        canvas[6][x] = C_LINE
    canvas[6][48] = C_HAT; canvas[6][49] = C_HAT
    canvas[6][60] = C_HAT; canvas[6][61] = C_HAT
    canvas[7][49] = C_LINE; canvas[7][60] = C_LINE
    
    # 2. 꽃미남 얼굴 & 3x3 고운 피부 음영
    for y in range(7, 19):
        for x in range(51, 59):
            if y >= 17:
                canvas[y][x] = get_mixed_color_block(C_SKIN, C_SHADOW, "MIX_50", x, y)
            else:
                canvas[y][x] = C_SKIN
                
    # 3. 짙고 단정한 눈썹 & 사연 있는 처진 눈매
    canvas[9][52] = C_LINE; canvas[9][53] = C_LINE
    canvas[9][56] = C_LINE; canvas[9][57] = C_LINE
    canvas[11][52] = C_WHITE; canvas[11][53] = C_LINE
    canvas[11][56] = C_LINE; canvas[11][57] = C_WHITE
    canvas[12][51] = C_SHADOW; canvas[12][54] = C_SHADOW
    canvas[12][55] = C_SHADOW; canvas[12][58] = C_SHADOW
    
    # 4. 오뚝한 콧날 & V라인 턱선
    canvas[13][54] = C_SHADOW; canvas[14][54] = C_SHADOW; canvas[15][54] = C_SHADOW
    canvas[16][54] = C_LINE; canvas[16][55] = C_SHADOW
    canvas[17][53] = C_SHADOW; canvas[17][54] = C_LINE; canvas[17][55] = C_LINE; canvas[17][56] = C_SHADOW
    canvas[19][52] = C_SHADOW; canvas[19][57] = C_SHADOW
    canvas[20][54] = C_SHADOW; canvas[20][55] = C_SHADOW
    
    # 5. 뺨을 타고 흐르는 굵은 눈물 (하늘색 + 순백 반사광)
    canvas[13][52] = C_TEAR; canvas[14][52] = C_WHITE; canvas[15][52] = C_TEAR
    
    # 6. 목선/쇄골 & 3x3 삼베옷 격자 딕셔너리 (누런삼베 + 거친음영)
    canvas[22][53] = C_SKIN; canvas[22][54] = C_SKIN; canvas[22][55] = C_SKIN; canvas[22][56] = C_SKIN
    canvas[23][54] = C_SHADOW; canvas[23][55] = C_SHADOW
    
    # 거친 삼베옷: 3x3 MIX_50 패턴으로 직조 질감 합성!
    for y in range(24, 37):
        for x in range(46, 64):
            canvas[y][x] = get_mixed_color_block(C_HAT, C_HEMP_ROUGH, "MIX_50", x, y)
    # 기운 자국
    canvas[27][49] = C_RAG; canvas[27][50] = C_RAG; canvas[28][49] = C_RAG
    canvas[32][58] = C_RAG; canvas[32][59] = C_RAG; canvas[33][59] = C_RAG
    
    return canvas


def generate_6_motion_frames():
    frames = []
    
    f1 = create_base_canvas_with_3x3_dict()
    frames.append(f1)
    
    # F2: 들숨 팽창 (비단 옷깃 1px 돌출, 상투 머리칼 들림)
    f2 = [row[:] for row in f1]
    for y in range(25, 35):
        f2[y][9] = C_SILK_BLUE
        f2[y][31] = C_SILK_BLUE
    f2[1][54] = C_LINE; f2[1][55] = C_LINE
    frames.append(f2)
    
    # F3: ★ 핵심 감정선 (놀부 금이빨 번쩍광 On! + 흥부 눈물 낙하)
    f3 = [row[:] for row in f1]
    f3[18][19] = C_GOLD
    f3[18][20] = C_WHITE # ★ 번쩍!
    f3[18][21] = C_GOLD
    f3[19][20] = C_WHITE
    f3[26][12] = C_WHITE; f3[29][28] = C_WHITE
    f3[24][19] = C_LINE; f3[24][21] = C_LINE
    # 흥부 눈물 낙하
    f3[13][52] = C_SKIN
    f3[16][52] = C_WHITE
    f3[17][52] = C_TEAR
    frames.append(f3)
    
    # F4: 날숨 수축
    f4 = [row[:] for row in f1]
    for y in range(26, 35):
        f4[y][10] = C_BG; f4[y][30] = C_BG
    f4[24][48] = C_BG; f4[24][62] = C_BG
    frames.append(f4)
    
    # F5: 잔상
    f5 = [row[:] for row in f1]
    f5[18][20] = C_GOLD
    f5[20][53] = C_TEAR
    frames.append(f5)
    
    # F6: 복귀
    f6 = [row[:] for row in f1]
    frames.append(f6)
    
    return frames


if __name__ == "__main__":
    frames = generate_6_motion_frames()
    tile_bytes = calculate_pattern_compressed_size(frames[0])
    total_tile_kb = (tile_bytes * 6) / 1024
    
    print("🕹️ [3x3 딕셔너리 패턴 압축] 9칸 하프톤 믹싱으로 색상은 다채롭게, 용량은 반으로!")
    print(f"📊 프레임당 3x3 압축 크기: {tile_bytes} B | 6프레임 총합: {total_tile_kb:.2f} KB (놀라운 압축률!)")
    print("   속도: 0.75초 | Ctrl+C로 종료\n")
    
    for loop in range(2):
        for idx, fr in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 원점 이동
            cur_tile_b = calculate_pattern_compressed_size(fr)
            
            # 우상단 HUD
            hud = f"[F{idx}/6 | 3x3 Tile: {cur_tile_b}B | 6-Frames: {total_tile_kb:.2f}KB]"
            title_text = "흥부놀부전 · 1막 (3x3 딕셔너리 색상 믹싱)"
            pad_len = 74 - len(title_text) * 2 - len(hud) + 12
            pad_len = max(1, pad_len)
            
            print(f"╔{'═' * 74}╗")
            print(f"║  {title_text}{' ' * pad_len}{hud}║")
            print(f"╠{'═' * 74}╣")
            lines = render_half_block_canvas(fr)
            for l in lines:
                print(f"║{l}║")
            print(f"╚{'═' * 74}╝")
            if idx == 3:
                print("  ★ F3: 3x3 딕셔너리 비단 광택 & 놀부 [금이빨 번쩍★] & 흥부 [눈물💧]!")
            else:
                print("  3x3 타일링으로 풍부한 중간색을 합성하면서도 용량은 2KB대로 극단 압축!")
            time.sleep(0.75)
