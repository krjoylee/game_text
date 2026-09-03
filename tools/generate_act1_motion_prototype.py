#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
개선 사항:
1. 재생 속도 완화 (0.35초 ➔ 0.75초로 차분하고 명확하게 관찰 가능)
2. 터미널 폰트 비율(세로:가로 ≈ 2:1) 보정: 상하 높이를 1/2로 압축하여 말처럼 길어 보이지 않고 황금비율 유지
3. 흥부 외형 수정: 패랭이 대신 '터진 갓에 상투만 남은 형태(망건 + 삐져나온 상투머리)'로 빈티와 처절함 극대화
4. 놀부 '금이빨 번쩍' & 흥부 '꽃미남 눈물 낙하' 미세 모션 유지
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
C_INK = 1         # 갓, 먹선, 동공, 상투
C_SKIN = 2        # 밝은 피부
C_SHADOW = 3      # 피부 음영, 턱선, 다크서클
C_HAT = 4         # 누런 짚/삼베
C_RAG = 5         # 누더기 갈색
C_SILK_RED = 6    # 놀부 비단 깃
C_SILK_BLUE = 7   # 놀부 비단 도포
C_TEAR = 8        # 눈물 하늘색
C_WHITE = 9       # 순백색 (치아, 반사광)
C_GOLD = 12       # ★ 놀부 금이빨 황금빛!

def create_base_frame():
    """기준 프레임 (F1) — 상하 길이를 절반으로 압축하여 폰트 왜곡 방지"""
    grid = [[(C_BG, ' ') for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu) — 납작하고 넓은 갓, 세모눈, 금이빨, 턱수염]
    # 중심: x: 8~32, y: 5~18 (상하 13줄로 컴팩트화)
    # ─────────────────────────────────────────────────────────────
    
    # 1. 넓은 양반 갓 (Row 5~7)
    for x in range(15, 27): # 갓 모자
        grid[5][x] = (C_INK, '█')
    for x in range(8, 34):  # 가로로 쫙 뻗은 날카로운 갓 챙
        grid[6][x] = (C_INK, '━')
    # 갓끈
    grid[7][15] = (C_INK, '│'); grid[7][26] = (C_INK, '│')
    
    # 2. 얼굴 윤곽 & 피부 (Row 7~11, 상하 5줄)
    for y in range(7, 12):
        for x in range(16, 26):
            grid[y][x] = (C_SKIN, '█')
    # 턱선 음영
    for x in range(17, 25):
        grid[11][x] = (C_SHADOW, '▓')
        
    # 3. 치켜뜬 세모 눈 (Row 8)
    grid[8][18] = (C_INK, '▲'); grid[8][19] = (C_WHITE, '░') # 왼쪽 눈
    grid[8][22] = (C_WHITE, '░'); grid[8][23] = (C_INK, '▲') # 오른쪽 눈
    grid[7][18] = (C_INK, '╱'); grid[7][23] = (C_INK, '╲')   # 눈썹
    
    # 4. 매부리코 & 사납게 비틀린 입 (Row 9~10)
    grid[9][20] = (C_SHADOW, '▌'); grid[9][21] = (C_INK, '◄') # 코
    
    # 기본 입 (다문 상태)
    grid[10][19] = (C_INK, '─')
    grid[10][20] = (C_INK, '━')
    grid[10][21] = (C_GOLD, '■') # ★ 번쩍이는 황금 앞니(금이빨)!
    grid[10][22] = (C_INK, '─')
    
    # 5. 뾰족한 턱수염 (Row 12~13)
    grid[12][19] = (C_INK, '█'); grid[12][20] = (C_INK, '█'); grid[12][21] = (C_INK, '█'); grid[12][22] = (C_INK, '█')
    grid[13][20] = (C_INK, '▼'); grid[13][21] = (C_INK, '▼')
    
    # 6. 비단 도포 & 붉은 깃 (Row 14~18)
    for y in range(14, 19):
        for x in range(11, 31):
            grid[y][x] = (C_SILK_BLUE, '█')
    # 붉은 깃
    grid[14][20] = (C_SILK_RED, '█'); grid[14][21] = (C_SILK_RED, '█')
    grid[15][20] = (C_SILK_RED, '█'); grid[15][21] = (C_SILK_RED, '█')

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 터진 갓에 상투만 남은 꽃미남 빈티]
    # 중심: x: 45~67, y: 4~18 (상하 14줄로 컴팩트화)
    # ─────────────────────────────────────────────────────────────
    
    # 1. 터져서 날아간 갓 & 삐져나온 상투 (Row 4~6)
    # 솟아오른 상투 (Row 4~5)
    grid[4][55] = (C_INK, '▄'); grid[4][56] = (C_INK, '▄') # 상투 꼭지
    grid[5][54] = (C_INK, '█'); grid[5][55] = (C_INK, '█'); grid[5][56] = (C_INK, '█'); grid[5][57] = (C_INK, '█') # 상투 뭉치
    
    # 이마의 망건 & 부서진 갓 테두리 파편 (Row 6)
    grid[6][50] = (C_HAT, '░') # 부서져 덜렁거리는 갓 조각
    for x in range(52, 60):
        grid[6][x] = (C_INK, '▒') # 이마를 졸라맨 검은 망건
    grid[6][61] = (C_HAT, '░')
    # 흩날리는 귀밑머리/잔머리
    grid[6][49] = (C_INK, '╱'); grid[6][62] = (C_INK, '╲')
    
    # 2. 꽃미남 얼굴 윤곽 (Row 7~11)
    for y in range(7, 11):
        for x in range(51, 61):
            grid[y][x] = (C_SKIN, '█')
            
    # 3. 짙고 단정한 귀공자 눈썹 & 처진 눈매 (Row 7~8)
    grid[7][52] = (C_INK, '━'); grid[7][53] = (C_INK, '━') # 왼쪽 눈썹
    grid[7][58] = (C_INK, '━'); grid[7][59] = (C_INK, '━') # 오른쪽 눈썹
    
    # 처진 눈매 & 다크서클
    grid[8][52] = (C_SHADOW, '░'); grid[8][53] = (C_INK, '▼')
    grid[8][58] = (C_INK, '▼'); grid[8][59] = (C_SHADOW, '░')
    
    # 4. 오뚝한 콧날 & 날렵한 V라인 턱선 (Row 9~11)
    grid[9][55] = (C_SHADOW, '│'); grid[9][56] = (C_SKIN, '▌') # 오뚝한 코
    # 베일 듯한 V라인 턱끝
    grid[10][54] = (C_SHADOW, '╲'); grid[10][55] = (C_INK, '─'); grid[10][56] = (C_INK, '─'); grid[10][57] = (C_SHADOW, '╱')
    grid[11][55] = (C_SHADOW, '╲'); grid[11][56] = (C_SHADOW, '╱')
    
    # 5. 뺨을 타고 흐르는 굵은 눈물 (Row 9~10)
    grid[9][53] = (C_TEAR, '💧')
    grid[10][53] = (C_WHITE, '·')
    
    # 6. 목선과 쇄골이 드러난 누더기 삼베옷 (Row 12~18)
    # 드러난 쇄골/목선
    grid[12][54] = (C_SKIN, '░'); grid[12][55] = (C_SKIN, '░'); grid[12][56] = (C_SKIN, '░'); grid[12][57] = (C_SKIN, '░')
    grid[13][55] = (C_SHADOW, '▼'); grid[13][56] = (C_SHADOW, '▼')
    # 누더기 옷몸통
    for y in range(13, 19):
        for x in range(46, 66):
            if y == 13 and (x < 50 or x > 61): continue
            grid[y][x] = (C_HAT, '▒')
    # 기운 자국
    grid[15][48] = (C_RAG, '█'); grid[15][49] = (C_RAG, '█')
    grid[16][59] = (C_RAG, '█'); grid[16][60] = (C_RAG, '█')
    
    return grid


def generate_6_motion_frames():
    frames = []
    
    # F1: 기본 프레임
    f1 = create_base_frame()
    frames.append(f1)
    
    # F2: 들숨 (놀부 어깨 확장 +1px, 흥부 상투 머리칼 1px 들림)
    f2 = [row[:] for row in f1]
    for y in range(14, 18):
        f2[y][10] = (C_SILK_BLUE, '▌')
        f2[y][31] = (C_SILK_BLUE, '▐')
    # 흥부 상투 털끝 1px 들림
    f2[3][55] = (C_INK, '·'); f2[3][56] = (C_INK, '·')
    frames.append(f2)
    
    # F3: ★ 핵심 감정선 (놀부 금이빨 번쩍! On + 흥부 눈물 낙하)
    f3 = [row[:] for row in f1]
    # 놀부 입 벌어지며 황금빛 반사광 폭발
    f3[10][20] = (C_GOLD, '█')
    f3[10][21] = (C_GOLD, '█')
    f3[10][22] = (C_WHITE, '★') # 번쩍광!
    # 놀부 수염 부르르 좌우 1px 진동
    f3[13][19] = (C_INK, '▼'); f3[13][22] = (C_INK, '▼')
    # 흥부 눈물 1px 아래로 똑 떨어짐
    f3[9][53] = (C_SKIN, '█')   # 지나간 자리는 피부
    f3[10][53] = (C_TEAR, '💧') # 눈물방울 낙하
    f3[11][53] = (C_WHITE, '·')
    frames.append(f3)
    
    # F4: 날숨 (놀부 가슴 -1px 수축, 흥부 어깨 처짐)
    f4 = [row[:] for row in f1]
    for y in range(15, 19):
        f4[y][11] = (C_BG, ' ')
        f4[y][30] = (C_BG, ' ')
    f4[13][50] = (C_BG, ' '); f4[13][61] = (C_BG, ' ')
    frames.append(f4)
    
    # F5: 잔상 (금이빨 빛 감쇄, 흥부 턱끝 눈물 맺힘)
    f5 = [row[:] for row in f1]
    f5[10][21] = (C_GOLD, '■')
    f5[11][54] = (C_TEAR, '💧')
    frames.append(f5)
    
    # F6: 복귀
    f6 = [row[:] for row in f1]
    frames.append(f6)
    
    return frames

if __name__ == "__main__":
    frames = generate_6_motion_frames()
    print("🎬 [개선 프로토타입] 놀부 금이빨 & 흥부 상투 꽃미남 (상하 1/2 압축 보정)")
    print("   속도: 0.75초 (차분한 프레임 전환 / Ctrl+C로 종료)\n")
    
    # 2회 루프 시연
    for loop in range(2):
        for idx, fr in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 커서 원점 이동
            print(f"╔{'═' * 74}╗")
            print(f"║  흥부놀부전 · 1막 [프레임 {idx}/6] (상하 압축 & 상투 빈티)                ║")
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
                print("  ★ F3: 놀부의 [금이빨 번쩍광★] 호통 & 흥부의 [눈물방울 낙하💧]!")
            else:
                print("  0.75초 차분한 호흡 모션으로 픽셀 원근감 관찰 중...")
            time.sleep(0.75) # 기존 0.35초에서 0.75초로 2배 이상 늦춤!
