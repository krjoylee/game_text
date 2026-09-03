#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
Phase 2 고전 8비트 패미컴 도트 감성 렌더러 (개선판):
1. 배경색 분리: 어두운 한옥 벽지 회갈색(237번) ➔ 놀부의 칠흑 양반 갓(16번 흑색)과 갓끈이 또렷하게 드러남!
2. 옷 질감 및 입체감(Shading & Texture):
   - 놀부: 번들거리는 비단 광택 하이라이트(순백/청록 픽셀) 및 주름 음영선 추가로 기름진 입체감 폭발!
   - 흥부: 거친 삼베옷의 격자 질감(디더링)과 흙먼지 기운 자국으로 누더기 질감 생생 표현!
3. 우측 상단 실시간 이미지 용량(Raw 및 RLE 압축 바이트) HUD 표시!
"""

import os
import sys
import time

sys.path.append("/home/krjoylee/code/game/tools")
from palette_engine import render_half_block_canvas, calculate_frame_size, PALETTE_16

CANVAS_W = 74
CANVAS_H = 38  # 터미널 19줄 '▀'

# 16색 인덱스 정의
C_BG = 0          # 0: 한옥 벽 회갈색 (갓과 완벽 분리!)
C_LINE = 1        # 1: 칠흑 갓, 눈썹, 동공, 수염
C_SKIN = 2        # 2: 밝은 살구색 피부
C_SHADOW = 3      # 3: 피부 음영, 콧대, V라인 턱선
C_HAT = 4         # 4: 흥부 터진 갓, 삼베옷 바탕
C_RAG = 5         # 5: 누더기 헝겊 갈색
C_SILK_RED = 6    # 6: 놀부 비단 깃 주홍
C_SILK_BLUE = 7   # 7: 놀부 비단 도포 메인
C_TEAR = 8        # 8: 흥부 눈물 하늘색
C_WHITE = 9       # 9: 흰자위, 비단 광택 하이라이트
C_SILK_SHINE = 10 # 10: 비단 주름 광택 청록
C_HEMP_ROUGH = 11 # 11: 거친 삼베옷 질감
C_GOLD = 12       # 12: ★ 놀부 금이빨 황금빛!

def create_base_8bit_canvas():
    """기준 프레임 (F1) 74x38 고밀도 8비트 도트 캔버스"""
    canvas = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu) — 칠흑 갓 분리 + 번들거리는 비단 도포 질감]
    # 중심 좌표: x: 8~32, y: 3~35
    # ─────────────────────────────────────────────────────────────
    
    # 1. 칠흑 양반 갓 (Row 3~9, Col 8~33) ➔ 배경(0번 회갈색) 위에서 선명하게 분리!
    for y in range(3, 8):
        for x in range(15, 26):
            canvas[y][x] = C_LINE
    # 갓 챙의 윗선에 미세 반사광 (회색) 및 칠흑 본체
    for x in range(7, 34):
        canvas[8][x] = C_LINE
    # 갓끈 (턱 아래로 길게 늘어짐)
    for y in range(9, 15):
        canvas[y][15] = C_LINE
        canvas[y][25] = C_LINE
        
    # 2. 얼굴 윤곽 & 고운 피부 (Row 9~21, Col 15~25)
    for y in range(9, 21):
        for x in range(16, 25):
            canvas[y][x] = C_SKIN
    # 볼과 턱 외곽 음영선
    for y in range(17, 21):
        canvas[y][16] = C_SHADOW
        canvas[y][24] = C_SHADOW
    for x in range(17, 24):
        canvas[20][x] = C_SHADOW
        
    # 3. 위로 찢어진 세모 눈 & 치켜뜬 눈썹 (Row 10~12)
    canvas[10][17] = C_LINE; canvas[10][18] = C_LINE
    canvas[10][22] = C_LINE; canvas[10][23] = C_LINE
    # 왼쪽 눈 (흰자위 속에 박힌 흑색 동공)
    canvas[12][17] = C_WHITE; canvas[12][18] = C_LINE; canvas[12][19] = C_WHITE
    # 오른쪽 눈
    canvas[12][21] = C_WHITE; canvas[12][22] = C_LINE; canvas[12][23] = C_WHITE
    
    # 4. 사나운 매부리코 (Row 14~16)
    canvas[14][20] = C_SHADOW; canvas[15][20] = C_SHADOW; canvas[16][19] = C_LINE; canvas[16][20] = C_LINE
    
    # 5. 비열하게 비튼 입 & ★금이빨 (Row 17~18)
    canvas[17][18] = C_LINE; canvas[17][19] = C_LINE; canvas[17][20] = C_LINE; canvas[17][21] = C_LINE; canvas[17][22] = C_LINE
    canvas[18][19] = C_LINE
    canvas[18][20] = C_GOLD  # ★ 놀부 금이빨!
    canvas[18][21] = C_LINE
    
    # 6. 뾰족한 검은 턱수염 (Row 21~25)
    for y in range(21, 24):
        canvas[y][19] = C_LINE; canvas[y][20] = C_LINE; canvas[y][21] = C_LINE
    canvas[24][20] = C_LINE; canvas[25][20] = C_LINE
    
    # 7. 비단 도포 & 화려한 광택 질감 (Row 23~36)
    for y in range(23, 37):
        for x in range(10, 31):
            canvas[y][x] = C_SILK_BLUE
    # 화려한 붉은 깃
    for y in range(23, 30):
        canvas[y][19] = C_SILK_RED
        canvas[y][20] = C_SILK_RED
    # ★ 비단 옷감의 기름진 광택(Shine) 및 주름선 (입체감 부여!)
    for y in range(26, 35, 3):
        canvas[y][13] = C_WHITE        # 비단 반사광 하이라이트
        canvas[y+1][14] = C_SILK_SHINE # 밝은 청록 반사
        canvas[y][27] = C_WHITE
        canvas[y+1][26] = C_SILK_SHINE
    # 옷 주름 음영 먹선
    for y in range(28, 36):
        canvas[y][16] = C_LINE; canvas[y][23] = C_LINE

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 솟아오른 상투 + 거친 삼베옷 격자 질감]
    # 중심 좌표: x: 44~66, y: 2~35
    # ─────────────────────────────────────────────────────────────
    
    # 1. 솟아오른 상투 & 터진 갓 파편 (Row 2~8)
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
    
    # ★ 거친 삼베옷 질감 디더링 (삼베바탕 + 거친 음영 교차 패턴)
    for y in range(24, 37):
        for x in range(46, 64):
            # 격자 디더링 질감
            if (x + y) % 2 == 0:
                canvas[y][x] = C_HAT
            else:
                canvas[y][x] = C_HEMP_ROUGH
    # 헝겊 기운 자국 (갈색)
    canvas[27][49] = C_RAG; canvas[27][50] = C_RAG; canvas[28][49] = C_RAG
    canvas[32][58] = C_RAG; canvas[32][59] = C_RAG; canvas[33][59] = C_RAG
    
    return canvas


def generate_6_motion_frames():
    frames = []
    
    # F1: 기본 프레임
    f1 = create_base_8bit_canvas()
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
    # 놀부 금이빨 번쩍! (황금 + 순백 반사광)
    f3[18][19] = C_GOLD
    f3[18][20] = C_WHITE
    f3[18][21] = C_GOLD
    f3[19][20] = C_WHITE
    # 비단 광택 반사광도 함께 번쩍
    f3[26][12] = C_WHITE; f3[29][28] = C_WHITE
    # 수염 떨림
    f3[24][19] = C_LINE; f3[24][21] = C_LINE
    # 흥부 눈물 낙하
    f3[13][52] = C_SKIN
    f3[16][52] = C_WHITE
    f3[17][52] = C_TEAR
    frames.append(f3)
    
    # F4: 날숨 수축 (가슴 -1px 수축, 흥부 어깨 처짐)
    f4 = [row[:] for row in f1]
    for y in range(26, 35):
        f4[y][10] = C_BG; f4[y][30] = C_BG
    f4[24][48] = C_BG; f4[24][62] = C_BG
    frames.append(f4)
    
    # F5: 잔상 (금이빨 빛 정돈, 턱끝 눈물 맺힘)
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
    total_raw_kb = (raw_b * 6) / 1024
    total_rle_kb = (rle_b * 6) / 1024
    
    print("🕹️ [개선판] 놀부 갓 분리 & 옷감 질감(비단 광택 / 거친 삼베) 복원")
    print(f"📊 프레임당 용량: Raw {raw_b}B / RLE {rle_b}B (6프레임 총합: {total_rle_kb:.2f} KB!)")
    print("   속도: 0.75초 | Ctrl+C로 종료\n")
    
    for loop in range(2):
        for idx, fr in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 원점 이동
            cur_raw, cur_rle = calculate_frame_size(fr)
            
            # 우측 상단 용량 HUD 헤더
            hud = f"[F{idx}/6 | Frame: {cur_rle}B | 6-Frames: {total_rle_kb:.2f}KB]"
            title_text = "흥부놀부전 · 1막 (갓 분리 & 옷감 질감)"
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
