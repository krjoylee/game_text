#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
🏆 [최종 확정 하이브리드 표준]
사용자가 가장 만족했던 "개선 전전 이미지(배경과 갓이 뚜렷이 분리되고 옷감 질감이 입체적인 상태)" 복원:
1. 배경색: 은은한 한옥 벽지 회갈색(ANSI 237) ➔ 칠흑 갓(16번)과 갓끈의 날카로운 실루엣 100% 분리!
2. 인물 얼굴: 살구색 뽀샤시 피부(223번) + 또렷한 눈동자/흰자위 + 날렵한 V턱선
3. 의복 입체감: 번들거리는 비단 광택 하이라이트(순백 231번/청록 31번) + 거친 삼베옷 격자 디더링 질감
4. 핵심 포인트: F3 놀부 [황금 앞니(220번) 번쩍★] 호통 & 흥부 [하늘색(81번) 눈물방울 낙하💧]
5. 우상단 HUD: 프레임당 600B / 6프레임 총합 3.52KB 실시간 모니터링
"""

import os
import sys
import time

CANVAS_W = 74
CANVAS_H = 38  # 터미널 19줄 '▀'

# 16색 하이브리드 팔레트 정의 (인덱스: 0~15)
PALETTE_16 = [
    ("한옥벽배경", 237, (58, 58, 58)),     # 0: 갓(검정)과 분리되는 어두운 한옥 벽지 회갈색
    ("칠흑먹선", 16, (0, 0, 0)),           # 1: 칠흑 갓, 눈썹, 동공, 수염, 외곽선
    ("피부살구", 223, (255, 204, 153)),    # 2: 인물 밝고 고운 피부톤
    ("피부음영", 179, (212, 155, 106)),    # 3: 콧날 음영, V라인 턱선, 다크서클
    ("누런삼베", 186, (194, 178, 128)),    # 4: 흥부 터진 갓, 삼베옷 바탕
    ("누더기갈색", 94, (139, 90, 43)),     # 5: 헝겊 기운 자국, 삼베 주름
    ("비단주홍", 196, (231, 76, 60)),      # 6: 놀부 화려한 비단 깃
    ("비단군청", 25, (36, 113, 163)),      # 7: 놀부 비단 도포 메인
    ("눈물하늘", 81, (93, 173, 226)),      # 8: 흥부 눈물 방울
    ("순백반사", 231, (255, 255, 255)),    # 9: 흰자위, 비단 광택 하이라이트
    ("비단청록", 31, (0, 135, 175)),       # 10: 비단 주름 광택
    ("삼베거친음", 137, (175, 135, 95)),   # 11: 거친 삼베옷 격자 질감
    ("황금빛", 220, (244, 208, 63)),       # 12: ★ 놀부 번쩍이는 금이빨!
    ("도깨비녹", 36, (22, 160, 133)),      # 13
    ("쇠몽둥이", 244, (128, 139, 150)),    # 14
    ("화해들판", 41, (46, 204, 113)),      # 15
]

# 팔레트 인덱스 상수
C_BG = 0
C_LINE = 1
C_SKIN = 2
C_SHADOW = 3
C_HAT = 4
C_RAG = 5
C_SILK_RED = 6
C_SILK_BLUE = 7
C_TEAR = 8
C_WHITE = 9
C_SILK_SHINE = 10
C_HEMP_ROUGH = 11
C_GOLD = 12

def get_ansi_color(fg_idx, bg_idx):
    fg_code = PALETTE_16[fg_idx][1]
    bg_code = PALETTE_16[bg_idx][1]
    return f"\x1b[38;5;{fg_code};48;5;{bg_code}m"

def ansi_reset():
    return "\x1b[0m"

def render_half_block_canvas(pixel_grid_2x):
    canvas_h = len(pixel_grid_2x)
    canvas_w = len(pixel_grid_2x[0])
    lines = []
    
    for y in range(0, canvas_h, 2):
        top_row = pixel_grid_2x[y]
        bot_row = pixel_grid_2x[y + 1] if y + 1 < canvas_h else [0] * canvas_w
        
        line_parts = []
        cur_fg = -1
        cur_bg = -1
        for x in range(canvas_w):
            c_top = top_row[x]
            c_bot = bot_row[x]
            if c_top != cur_fg or c_bot != cur_bg:
                line_parts.append(get_ansi_color(c_top, c_bot))
                cur_fg = c_top
                cur_bg = c_bot
            line_parts.append("▀")
        line_parts.append(ansi_reset())
        lines.append("".join(line_parts))
        
    return lines

def calculate_frame_size(canvas_data):
    total_pixels = len(canvas_data) * len(canvas_data[0])
    raw_bytes = total_pixels // 2
    flat = [pixel for row in canvas_data for pixel in row]
    rle_chunks = []
    curr_pixel = flat[0]
    curr_len = 1
    for p in flat[1:]:
        if p == curr_pixel and curr_len < 15:
            curr_len += 1
        else:
            rle_chunks.append((curr_pixel, curr_len))
            curr_pixel = p
            curr_len = 1
    rle_chunks.append((curr_pixel, curr_len))
    rle_bytes = len(rle_chunks)
    return raw_bytes, rle_bytes

def create_base_8bit_canvas():
    """기준 프레임 (F1) 74x38 고밀도 8비트 도트 캔버스"""
    canvas = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu) — 칠흑 갓 + 번들거리는 비단 도포]
    # ─────────────────────────────────────────────────────────────
    # 1. 칠흑 양반 갓 (Row 3~9, Col 8~33)
    for y in range(3, 8):
        for x in range(15, 26):
            canvas[y][x] = C_LINE
    for x in range(7, 34):
        canvas[8][x] = C_LINE
    # 갓끈
    for y in range(9, 15):
        canvas[y][15] = C_LINE
        canvas[y][25] = C_LINE
        
    # 2. 얼굴 윤곽 & 고운 피부 (Row 9~21, Col 15~25)
    for y in range(9, 21):
        for x in range(16, 25):
            canvas[y][x] = C_SKIN
    for y in range(17, 21):
        canvas[y][16] = C_SHADOW
        canvas[y][24] = C_SHADOW
    for x in range(17, 24):
        canvas[20][x] = C_SHADOW
        
    # 3. 위로 찢어진 세모 눈 & 치켜뜬 눈썹 (Row 10~12)
    canvas[10][17] = C_LINE; canvas[10][18] = C_LINE
    canvas[10][22] = C_LINE; canvas[10][23] = C_LINE
    canvas[12][17] = C_WHITE; canvas[12][18] = C_LINE; canvas[12][19] = C_WHITE
    canvas[12][21] = C_WHITE; canvas[12][22] = C_LINE; canvas[12][23] = C_WHITE
    
    # 4. 사나운 매부리코 & 입 & ★금이빨
    canvas[14][20] = C_SHADOW; canvas[15][20] = C_SHADOW; canvas[16][19] = C_LINE; canvas[16][20] = C_LINE
    canvas[17][18] = C_LINE; canvas[17][19] = C_LINE; canvas[17][20] = C_LINE; canvas[17][21] = C_LINE; canvas[17][22] = C_LINE
    canvas[18][19] = C_LINE
    canvas[18][20] = C_GOLD  # ★ 놀부 금이빨!
    canvas[18][21] = C_LINE
    
    # 5. 뾰족한 검은 턱수염 (Row 21~25)
    for y in range(21, 24):
        canvas[y][19] = C_LINE; canvas[y][20] = C_LINE; canvas[y][21] = C_LINE
    canvas[24][20] = C_LINE; canvas[25][20] = C_LINE
    
    # 6. 비단 도포 & 화려한 광택 질감 (Row 23~36)
    for y in range(23, 37):
        for x in range(10, 31):
            canvas[y][x] = C_SILK_BLUE
    # 화려한 붉은 깃
    for y in range(23, 30):
        canvas[y][19] = C_SILK_RED
        canvas[y][20] = C_SILK_RED
    # 비단 옷감의 기름진 광택 및 주름선
    for y in range(26, 35, 3):
        canvas[y][13] = C_WHITE
        canvas[y+1][14] = C_SILK_SHINE
        canvas[y][27] = C_WHITE
        canvas[y+1][26] = C_SILK_SHINE
    for y in range(28, 36):
        canvas[y][16] = C_LINE; canvas[y][23] = C_LINE

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 솟아오른 상투 + 거친 삼베옷 격자 질감]
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
    
    # 2. 꽃미남 얼굴 윤곽 & 고운 피부 (Row 7~20)
    for y in range(7, 19):
        for x in range(51, 59):
            canvas[y][x] = C_SKIN
            
    # 3. 짙고 단정한 귀공자 눈썹 & 서글픈 처진 눈매 (Row 9~12)
    canvas[9][52] = C_LINE; canvas[9][53] = C_LINE
    canvas[9][56] = C_LINE; canvas[9][57] = C_LINE
    canvas[11][52] = C_WHITE; canvas[11][53] = C_LINE
    canvas[11][56] = C_LINE; canvas[11][57] = C_WHITE
    canvas[12][51] = C_SHADOW; canvas[12][54] = C_SHADOW
    canvas[12][55] = C_SHADOW; canvas[12][58] = C_SHADOW
    
    # 4. 오뚝한 콧날 & 날렵한 V턱선 (Row 13~21)
    canvas[13][54] = C_SHADOW; canvas[14][54] = C_SHADOW; canvas[15][54] = C_SHADOW
    canvas[16][54] = C_LINE; canvas[16][55] = C_SHADOW
    canvas[17][53] = C_SHADOW; canvas[17][54] = C_LINE; canvas[17][55] = C_LINE; canvas[17][56] = C_SHADOW
    canvas[19][52] = C_SHADOW; canvas[19][57] = C_SHADOW
    canvas[20][53] = C_SHADOW; canvas[20][54] = C_SHADOW; canvas[20][55] = C_SHADOW; canvas[20][56] = C_SHADOW
    canvas[21][54] = C_SHADOW; canvas[21][55] = C_SHADOW
    
    # 5. 뺨을 타고 흐르는 굵은 눈물 (Row 13~15)
    canvas[13][52] = C_TEAR; canvas[14][52] = C_WHITE; canvas[15][52] = C_TEAR
    
    # 6. 목선과 쇄골이 드러난 누더기 삼베옷 (Row 22~36)
    canvas[22][53] = C_SKIN; canvas[22][54] = C_SKIN; canvas[22][55] = C_SKIN; canvas[22][56] = C_SKIN
    canvas[23][54] = C_SHADOW; canvas[23][55] = C_SHADOW
    
    # 거친 삼베옷 질감 디더링 (삼베바탕 + 거친 음영 교차 패턴)
    for y in range(24, 37):
        for x in range(46, 64):
            if (x + y) % 2 == 0:
                canvas[y][x] = C_HAT
            else:
                canvas[y][x] = C_HEMP_ROUGH
    # 헝겊 기운 자국
    canvas[27][49] = C_RAG; canvas[27][50] = C_RAG; canvas[28][49] = C_RAG
    canvas[32][58] = C_RAG; canvas[32][59] = C_RAG; canvas[33][59] = C_RAG
    
    return canvas


def generate_6_motion_frames():
    frames = []
    
    # F1
    f1 = create_base_8bit_canvas()
    frames.append(f1)
    
    # F2: 들숨 팽창
    f2 = [row[:] for row in f1]
    for y in range(25, 35):
        f2[y][9] = C_SILK_BLUE
        f2[y][31] = C_SILK_BLUE
    f2[1][54] = C_LINE; f2[1][55] = C_LINE
    frames.append(f2)
    
    # F3: ★ 핵심 감정선 (놀부 금이빨 번쩍광 On! + 흥부 눈물 낙하)
    f3 = [row[:] for row in f1]
    f3[18][19] = C_GOLD
    f3[18][20] = C_WHITE
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
    raw_b, rle_b = calculate_frame_size(frames[0])
    total_rle_kb = (rle_b * 6) / 1024
    
    print("🏆 [최종 확정 하이브리드 표준] 놀부 갓 분리 & 비단/삼베 질감 입체화 렌더링")
    print(f"📊 프레임당 용량: {rle_b} B | 6프레임 총합: {total_rle_kb:.2f} KB (1MB 제한의 0.3% 방어!)")
    print("   속도: 0.75초 | Ctrl+C로 종료\n")
    
    for loop in range(2):
        for idx, fr in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 원점 이동
            cur_raw, cur_rle = calculate_frame_size(fr)
            
            # 우상단 용량 HUD 헤더
            hud = f"[F{idx}/6 | Frame: {cur_rle}B | 6-Frames: {total_rle_kb:.2f}KB]"
            title_text = "흥부놀부전 · 1막 (하이브리드 도트 표준)"
            pad_len = 74 - len(title_text) * 2 - len(hud) + 6
            pad_len = max(1, pad_len)
            
            print(f"╔{'═' * 74}╗")
            print(f"║  {title_text}{' ' * pad_len}{hud}║")
            print(f"╠{'═' * 74}╣")
            lines = render_half_block_canvas(fr)
            for l in lines:
                print(f"║{l}║")
            print(f"╚{'═' * 74}╝")
            if idx == 3:
                print("  ★ F3: 놀부의 [황금빛 앞니 번쩍★] & 흥부의 [하늘색 눈물방울 낙하💧]!")
            else:
                print("  비단 광택과 거친 삼베옷의 입체감 & 갓 실루엣 호흡 모션 구동 중...")
            time.sleep(0.75)
