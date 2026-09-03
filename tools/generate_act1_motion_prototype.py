#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
놀부 '금이빨(12번 황금)' + 흥부 '꽃미남 빈티(오뚝한 코, 날렵한 턱선, 패랭이, 눈물)'
주변 픽셀 1~2개 On/Off 미세 원근 모션(F1~F6) 프로토타입 생성기
"""

import os
import sys
import time

sys.path.append("/home/krjoylee/code/game/tools")
from palette_engine import ansi_fg, ansi_reset, PALETTE_16

WIDTH = 74
HEIGHT = 23

# 팔레트 인덱스 상수
C_BG = 0          # 배경
C_INK = 1         # 갓, 먹선, 동공
C_SKIN = 2        # 밝은 피부
C_SHADOW = 3      # 피부 음영, 턱선, 다크서클
C_HAT = 4         # 흥부 패랭이 누런색
C_RAG = 5         # 누더기 갈색
C_SILK_RED = 6    # 놀부 비단 깃
C_SILK_BLUE = 7   # 놀부 비단 도포
C_TEAR = 8        # 눈물 하늘색
C_WHITE = 9       # 순백색 (치아, 반사광)
C_GOLD = 12       # ★ 놀부 금이빨 황금빛!

def create_base_frame():
    """기준 프레임 (F1) 그리드 생성 (color_idx, char)"""
    grid = [[(C_BG, ' ') for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu) — 갓, 세모 눈, 심술보, 턱수염, ★금이빨]
    # 중심 좌표: x: 10~32, y: 2~20
    # ─────────────────────────────────────────────────────────────
    
    # 1. 넓은 양반 갓 (Row 2~6, Col 8~34)
    for x in range(14, 28): # 갓 모자
        grid[2][x] = (C_INK, '█')
        grid[3][x] = (C_INK, '█')
        grid[4][x] = (C_INK, '█')
    for x in range(8, 34):  # 날카로운 갓 챙
        grid[5][x] = (C_INK, '━')
    # 갓끈
    grid[6][14] = (C_INK, '│'); grid[7][15] = (C_INK, '│')
    grid[6][27] = (C_INK, '│'); grid[7][26] = (C_INK, '│')
    
    # 2. 얼굴 윤곽 & 피부 (Row 6~14, Col 15~26)
    for y in range(6, 13):
        for x in range(16, 26):
            grid[y][x] = (C_SKIN, '█')
    # 볼/턱 음영
    for x in range(16, 26):
        grid[12][x] = (C_SHADOW, '▓')
        
    # 3. 치켜뜬 세모 눈 (Row 7~8)
    grid[7][18] = (C_INK, '▲'); grid[7][19] = (C_WHITE, '░') # 왼쪽 눈
    grid[7][22] = (C_WHITE, '░'); grid[7][23] = (C_INK, '▲') # 오른쪽 눈
    grid[6][18] = (C_INK, '╱'); grid[6][23] = (C_INK, '╲')   # 치켜뜬 눈썹
    
    # 4. 매부리코 & 사납게 꺾인 입 (Row 9~11)
    grid[9][20] = (C_SHADOW, '▌'); grid[9][21] = (C_INK, '◄') # 코
    
    # 기본 입 (다문 상태)
    grid[10][19] = (C_INK, '─')
    grid[10][20] = (C_INK, '━')
    grid[10][21] = (C_GOLD, '■') # ★ 번쩍이는 금이빨 기본 자리!
    grid[10][22] = (C_INK, '─')
    
    # 5. 빳빳하고 뾰족한 검은 턱수염 (Row 13~16)
    grid[13][19] = (C_INK, '█'); grid[13][20] = (C_INK, '█'); grid[13][21] = (C_INK, '█'); grid[13][22] = (C_INK, '█')
    grid[14][20] = (C_INK, '█'); grid[14][21] = (C_INK, '█')
    grid[15][20] = (C_INK, '▼'); grid[15][21] = (C_INK, '▼')
    
    # 6. 비단 도포 & 붉은 깃 (Row 16~21)
    for y in range(16, 22):
        for x in range(11, 31):
            grid[y][x] = (C_SILK_BLUE, '█')
    # 붉은 깃 (가슴)
    grid[16][20] = (C_SILK_RED, '█'); grid[16][21] = (C_SILK_RED, '█')
    grid[17][20] = (C_SILK_RED, '█'); grid[17][21] = (C_SILK_RED, '█')
    grid[18][20] = (C_SILK_RED, '█'); grid[18][21] = (C_SILK_RED, '█')

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 꽃미남 빈티: 짙은 눈썹, 오뚝한 코, 날렵한 V턱선, 패랭이, 눈물]
    # 중심 좌표: x: 45~65, y: 3~20
    # ─────────────────────────────────────────────────────────────
    
    # 1. 찢어진 패랭이 모자 (Row 3~6, Col 46~66)
    for x in range(50, 62): # 모자 위
        grid[3][x] = (C_HAT, '░')
        grid[4][x] = (C_HAT, '▓')
    for x in range(46, 66): # 찢어진 챙
        grid[5][x] = (C_HAT, '━')
    grid[5][52] = (C_HAT, ' ') # 찢어진 틈새
    grid[5][60] = (C_HAT, ' ')
    
    # 2. 꽃미남 얼굴 윤곽 & 흩날리는 머리칼 (Row 6~14, Col 49~62)
    # 패랭이 틈새 머리칼
    grid[6][50] = (C_INK, '╱'); grid[6][61] = (C_INK, '╲')
    
    # 고운 피부 (V라인 턱선)
    for y in range(6, 12):
        for x in range(51, 61):
            grid[y][x] = (C_SKIN, '█')
            
    # 3. 짙고 단정한 눈썹 & 오뚝한 콧날 (귀공자상)
    grid[7][52] = (C_INK, '━'); grid[7][53] = (C_INK, '━') # 왼쪽 눈썹
    grid[7][58] = (C_INK, '━'); grid[7][59] = (C_INK, '━') # 오른쪽 눈썹
    
    # 서글픈 처진 눈매 & 다크서클
    grid[8][52] = (C_SHADOW, '░'); grid[8][53] = (C_INK, '▼') # 처진 눈
    grid[8][58] = (C_INK, '▼'); grid[8][59] = (C_SHADOW, '░')
    
    # 오뚝하고 날렵한 콧날 (Row 9~10)
    grid[9][55] = (C_SHADOW, '│'); grid[9][56] = (C_SKIN, '▌')
    grid[10][55] = (C_INK, '▲'); grid[10][56] = (C_SHADOW, '▌')
    
    # 4. 베일 듯 날렵한 V라인 턱선 & 다문 입술
    grid[11][54] = (C_SHADOW, '╲'); grid[11][55] = (C_INK, '─'); grid[11][56] = (C_INK, '─'); grid[11][57] = (C_SHADOW, '╱')
    grid[12][55] = (C_SHADOW, '╲'); grid[12][56] = (C_SHADOW, '╱') # 뾰족한 턱끝
    
    # 5. 뺨을 타고 흐르는 굵은 눈물 (Row 9~11, Col 53, 58)
    grid[9][53] = (C_TEAR, '💧')
    grid[10][53] = (C_TEAR, '│')
    grid[11][53] = (C_WHITE, '·')
    
    # 6. 쇄골이 드러난 누더기 삼베옷 (Row 13~21)
    for y in range(13, 22):
        for x in range(45, 67):
            grid[y][x] = (C_HAT, '▒')
    # 기운 자국 (갈색 헝겊)
    grid[15][48] = (C_RAG, '█'); grid[15][49] = (C_RAG, '█')
    grid[17][58] = (C_RAG, '█'); grid[17][59] = (C_RAG, '█')
    # 드러난 쇄골/목선 (음영)
    grid[13][54] = (C_SKIN, '░'); grid[13][55] = (C_SKIN, '░'); grid[13][56] = (C_SKIN, '░'); grid[13][57] = (C_SKIN, '░')
    grid[14][55] = (C_SHADOW, '▼'); grid[14][56] = (C_SHADOW, '▼')
    
    return grid


def generate_6_motion_frames():
    """
    주변 픽셀 1~2개 On/Off를 통한 6프레임 미세 원근/호흡 모션 생성
    F1: 기준
    F2: 들숨 (놀부 어깨 확장 +1px, 흥부 머리칼 1px 들림)
    F3: 번쩍/눈물 (★놀부 금이빨 반사광 On! + 흥부 눈물 1px 낙하)
    F4: 날숨/수축 (놀부 가슴 -1px, 수염 떨림 + 흥부 어깨 처짐)
    F5: 잔상 (금이빨 Off, 턱끝 눈물 맺힘)
    F6: 복귀
    """
    frames = []
    
    # F1: 기본 프레임
    f1 = create_base_frame()
    frames.append(f1)
    
    # F2: 들숨 (팽창 & 미남 머리칼 흩날림)
    f2 = [row[:] for row in f1]
    # 놀부 어깨 외곽 +1px 확장
    for y in range(16, 21):
        f2[y][10] = (C_SILK_BLUE, '▌')
        f2[y][31] = (C_SILK_BLUE, '▐')
    # 흥부 패랭이 틈새 머리칼 1px 위로 들림
    f2[5][50] = (C_INK, '╱')
    f2[5][61] = (C_INK, '╲')
    frames.append(f2)
    
    # F3: ★ 핵심 감정선 (놀부 금이빨 번쩍! On + 흥부 눈물 낙하)
    f3 = [row[:] for row in f1]
    # 놀부 입 크게 벌어지며 금이빨 광채 폭발 (황금 픽셀 + 백색 반사광)
    f3[10][20] = (C_GOLD, '█')
    f3[10][21] = (C_GOLD, '█')
    f3[10][22] = (C_WHITE, '★') # 번쩍광!
    # 놀부 수염 부르르 좌우 1px 떨림
    f3[15][19] = (C_INK, '▼'); f3[15][22] = (C_INK, '▼')
    # 흥부 눈물 방울 1px 아래로 똑 떨어짐
    f3[9][53] = (C_SKIN, '█')   # 위쪽 지나간 자리는 피부 복귀
    f3[10][53] = (C_TEAR, '💧') # 눈물방울 낙하
    f3[11][53] = (C_TEAR, '│')
    f3[12][53] = (C_WHITE, '·')
    frames.append(f3)
    
    # F4: 날숨 (수축 & 가슴 내림)
    f4 = [row[:] for row in f1]
    # 놀부 가슴 수축 (-1px)
    for y in range(17, 21):
        f4[y][11] = (C_BG, ' ')
        f4[y][30] = (C_BG, ' ')
    # 흥부 어깨 처짐
    f4[13][45] = (C_BG, ' '); f4[13][66] = (C_BG, ' ')
    frames.append(f4)
    
    # F5: 잔상 (금이빨 빛 감쇄 & 눈물방울 턱끝 맺힘)
    f5 = [row[:] for row in f1]
    # 놀부 금이빨 다시 은은한 황금으로
    f5[10][21] = (C_GOLD, '■')
    # 흥부 눈물 턱끝 맺힘
    f5[12][54] = (C_TEAR, '💧')
    frames.append(f5)
    
    # F6: 복귀 (기준점으로 부드럽게)
    f6 = [row[:] for row in f1]
    frames.append(f6)
    
    return frames

if __name__ == "__main__":
    frames = generate_6_motion_frames()
    print("🎬 [흥부놀부전 1막] 놀부 금이빨 & 흥부 꽃미남 빈티 6프레임 미세 원근 모션 재생 중...")
    print("   (Ctrl+C를 누르면 멈춥니다)\n")
    
    # 2회 루프 시연
    for loop in range(2):
        for idx, fr in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 커서 원점 이동
            print(f"╔{'═' * 74}╗")
            print(f"║  흥부놀부전 · 제1막 모션 시연 [프레임 {idx}/6]                           ║")
            print(f"╠{'═' * 74}╣")
            for row in fr:
                line_str = []
                cur_color = -1
                for color_idx, ch in row:
                    if color_idx != cur_color:
                        line_str.append(ansi_fg(color_idx))
                        cur_color = color_idx
                    line_str.append(ch)
                line_str.append(ansi_reset())
                print(f"║{''.join(line_str)}║")
            print(f"╚{'═' * 74}╝")
            if idx == 3:
                print("  ★ F3: 놀부의 [금이빨 번쩍광★] 호통 & 흥부의 [눈물방울 낙하💧] 순간!")
            else:
                print("  주변 픽셀 1~2개 On/Off를 통한 숨 쉬는 입체 원근감 형성 중...")
            time.sleep(0.35)
