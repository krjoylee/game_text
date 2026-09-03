#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
Phase 2 고전 픽셀 아트 렌더러:
- 눈, 코, 입 사이의 거슬리는 흰색 빈틈/글꼴 이질감 100% 제거!
- 배경색 ANSI(48;5;Nm)와 꽉 찬 2칸 블록을 결합하여, 실제 1980년대 패미컴/PC-98의 '솔리드 도트' 완벽 구현!
- 가로 37도트 x 세로 19도트 (터미널 74컬럼 x 19줄에 정사각형 1:1 도트 안착)
- 놀부 금이빨(12번 황금빛) & 흥부 상투 미남 눈물 6프레임 미세 원근 모션
"""

import os
import sys
import time

sys.path.append("/home/krjoylee/code/game/tools")
from palette_engine import ansi_bg, ansi_reset, PALETTE_16, render_solid_pixel_row

GRID_W = 37  # 1도트 = 가로 2칸 ➔ 총 74칸 터미널 화면 폭에 칼같이 일치!
GRID_H = 19  # 세로 19줄

# 16색 인덱스 정의
C_BG = 0          # 0: 어두운 배경 (검정)
C_INK = 1         # 1: 칠흑 갓, 눈썹, 동공, 수염
C_SKIN = 2        # 2: 밝은 피부 살구색
C_SHADOW = 3      # 3: 피부 음영, 날렵한 V턱선
C_HAT = 4         # 4: 흥부 터진 갓 부스러기, 삼베
C_RAG = 5         # 5: 누더기 갈색 헝겊
C_SILK_RED = 6    # 6: 놀부 비단 깃 주홍
C_SILK_BLUE = 7   # 7: 놀부 비단 도포 군청
C_TEAR = 8        # 8: 흥부 눈물 하늘색
C_WHITE = 9       # 9: 흰자위, 반사광
C_GOLD = 12       # 12: ★ 놀부 번쩍이는 금이빨!

def create_base_dot_matrix():
    """기준 프레임 (F1) — 흰색 빈틈이 1px도 없는 100% 솔리드 컬러 도트 매트릭스"""
    # 기본은 배경색(0번)으로 꽉 채움
    matrix = [[C_BG for _ in range(GRID_W)] for _ in range(GRID_H)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu) — 갓, 세모 눈, 금이빨, 턱수염] (x: 3~16, y: 2~16)
    # ─────────────────────────────────────────────────────────────
    
    # 1. 넓은 양반 갓 (Row 2~5)
    for x in range(6, 13):
        matrix[2][x] = C_INK
        matrix[3][x] = C_INK
    for x in range(3, 16):  # 좌우로 시원하게 뻗은 갓 챙
        matrix[4][x] = C_INK
    # 갓끈
    matrix[5][6] = C_INK; matrix[5][12] = C_INK
    matrix[6][6] = C_INK; matrix[6][12] = C_INK
    
    # 2. 얼굴 윤곽 (Row 5~9, Col 7~11)
    for y in range(5, 10):
        for x in range(7, 12):
            matrix[y][x] = C_SKIN
    # 볼과 턱 음영
    for x in range(7, 12):
        matrix[9][x] = C_SHADOW
        
    # 3. 눈과 눈썹 (Row 6)
    matrix[5][8] = C_INK; matrix[5][10] = C_INK     # 45도 치켜뜬 눈썹
    matrix[6][8] = C_INK; matrix[6][10] = C_INK     # 쏘아보는 검은 동공
    matrix[6][7] = C_WHITE; matrix[6][11] = C_WHITE # 흰자위
    
    # 4. 매부리코 & 사납게 비틀린 입 & ★금이빨 (Row 7~8)
    matrix[7][9] = C_SHADOW # 코 음영
    # 입술 라인 (틈새 없이 피부와 완벽 밀착)
    matrix[8][8] = C_SHADOW
    matrix[8][9] = C_INK
    matrix[8][10] = C_GOLD  # ★ 놀부의 상징: 황금 앞니(금이빨)!
    
    # 5. 뾰족한 검은 턱수염 (Row 10~11)
    matrix[10][8] = C_INK; matrix[10][9] = C_INK; matrix[10][10] = C_INK
    matrix[11][9] = C_INK
    
    # 6. 비단 도포 & 붉은 깃 (Row 12~16)
    for y in range(12, 17):
        for x in range(4, 15):
            matrix[y][x] = C_SILK_BLUE
    # 가슴의 화려한 붉은 깃
    matrix[12][9] = C_SILK_RED
    matrix[13][9] = C_SILK_RED
    matrix[14][9] = C_SILK_RED

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 터진 갓 상투 꽃미남 빈티] (x: 21~34, y: 1~16)
    # ─────────────────────────────────────────────────────────────
    
    # 1. 솟아오른 상투 & 터진 갓 파편 (Row 1~4)
    matrix[1][27] = C_INK; matrix[1][28] = C_INK   # 상투 꼭지
    matrix[2][26] = C_INK; matrix[2][27] = C_INK; matrix[2][28] = C_INK; matrix[2][29] = C_INK # 상투 뭉치
    # 이마의 망건 (검은 띠)
    for x in range(25, 30):
        matrix[3][x] = C_INK
    # 터져서 덜렁거리는 갓 부스러기 (누런색)
    matrix[3][24] = C_HAT; matrix[3][30] = C_HAT
    
    # 2. 꽃미남 귀공자 얼굴 (Row 4~9) — 베일 듯한 V라인 턱선
    for y in range(4, 9):
        for x in range(25, 30):
            matrix[y][x] = C_SKIN
            
    # 3. 짙고 단정한 눈썹 & 서글픈 처진 눈매 (Row 5~6)
    matrix[4][25] = C_INK; matrix[4][26] = C_INK   # 왼쪽 눈썹
    matrix[4][28] = C_INK; matrix[4][29] = C_INK   # 오른쪽 눈썹
    matrix[5][26] = C_INK; matrix[5][28] = C_INK   # 깊은 눈동자
    matrix[5][25] = C_SHADOW; matrix[5][29] = C_SHADOW # 눈가 그늘/다크서클
    
    # 4. 오뚝한 콧날 & 날렵한 턱선 (Row 6~9)
    matrix[6][27] = C_SHADOW # 오뚝한 콧대
    matrix[7][27] = C_INK    # 콧방울
    # 다문 입술
    matrix[8][26] = C_SHADOW; matrix[8][27] = C_INK; matrix[8][28] = C_SHADOW
    # V라인 턱끝
    matrix[9][26] = C_SHADOW; matrix[9][27] = C_SHADOW; matrix[9][28] = C_SHADOW
    matrix[10][27] = C_SHADOW # 뾰족한 턱끝
    
    # 5. 뺨을 타고 흐르는 굵은 눈물 (Row 6~7)
    matrix[6][25] = C_TEAR   # 눈물방울
    matrix[7][25] = C_WHITE  # 눈물 반사광
    
    # 6. 쇄골이 드러난 누더기 삼베옷 (Row 11~16)
    # 드러난 쇄골/목선 (피부색 음영)
    matrix[11][26] = C_SKIN; matrix[11][27] = C_SKIN; matrix[11][28] = C_SKIN
    matrix[12][27] = C_SHADOW
    # 거친 삼베옷 몸통
    for y in range(12, 17):
        for x in range(22, 33):
            if y == 12 and (x < 24 or x > 30): continue
            matrix[y][x] = C_HAT
    # 기운 자국 (갈색 헝겊)
    matrix[14][23] = C_RAG; matrix[14][24] = C_RAG
    matrix[15][29] = C_RAG; matrix[15][30] = C_RAG
    
    return matrix


def generate_6_motion_frames():
    """주변 픽셀 1~2개 On/Off 미세 원근/호흡 모션 (F1~F6)"""
    frames = []
    
    # F1: 기본 프레임
    f1 = create_base_dot_matrix()
    frames.append(f1)
    
    # F2: 들숨 팽창 (놀부 어깨 1px 돌출 + 흥부 상투 머리칼 1px 들림)
    f2 = [row[:] for row in f1]
    for y in range(12, 16):
        f2[y][3] = C_SILK_BLUE  # 어깨 1도트 확장
        f2[y][15] = C_SILK_BLUE
    f2[0][27] = C_INK; f2[0][28] = C_INK # 상투 털끝 1px 살짝 들림
    frames.append(f2)
    
    # F3: ★ 핵심 감정선 (놀부 금이빨 번쩍 광채 폭발! + 흥부 눈물 낙하)
    f3 = [row[:] for row in f1]
    # 놀부 입 크게 열리며 금이빨 주위에 눈부신 순백 반사광 On!
    f3[8][9] = C_GOLD
    f3[8][10] = C_WHITE # ★ 번쩍!
    f3[8][11] = C_GOLD
    # 놀부 수염 부르르 좌우 1px 진동
    f3[11][8] = C_INK; f3[11][10] = C_INK
    # 흥부 눈물 1px 아래로 뚝 떨어짐
    f3[6][25] = C_SKIN  # 지나간 자리는 피부 복귀
    f3[7][25] = C_TEAR  # 눈물방울 낙하
    f3[8][25] = C_WHITE
    frames.append(f3)
    
    # F4: 날숨 수축 (놀부 가슴 -1px, 흥부 어깨 처짐)
    f4 = [row[:] for row in f1]
    for y in range(13, 17):
        f4[y][4] = C_BG; f4[y][14] = C_BG
    f4[12][24] = C_BG; f4[12][30] = C_BG
    frames.append(f4)
    
    # F5: 잔상 (금이빨 빛 정돈, 흥부 턱끝 눈물 맺힘)
    f5 = [row[:] for row in f1]
    f5[8][10] = C_GOLD  # 금이빨 기본 복귀
    f5[9][26] = C_TEAR  # 턱끝에 맺힌 눈물
    frames.append(f5)
    
    # F6: 복귀
    f6 = [row[:] for row in f1]
    frames.append(f6)
    
    return frames


if __name__ == "__main__":
    frames = generate_6_motion_frames()
    print("🎬 [솔리드 도트 모션] 1980년대 패미컴/PC-98 스타일 100% 빈틈없는 도트 렌더링")
    print("   속도: 0.75초 | 흰색 글꼴 빈틈 제로 | Ctrl+C로 종료\n")
    
    for loop in range(2):
        for idx, fr in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 화면 원점 이동
            print(f"╔{'═' * 74}╗")
            print(f"║  흥부놀부전 · 1막 [프레임 {idx}/6] (솔리드 도트 · 빈틈 제거)               ║")
            print(f"╠{'═' * 74}╣")
            for row in fr:
                row_str = render_solid_pixel_row(row)
                print(f"║{row_str}║")
            print(f"╚{'═' * 74}╝")
            if idx == 3:
                print("  ★ F3: 놀부의 [황금빛 앞니 번쩍★] & 흥부의 [하늘색 눈물방울 낙하💧]!")
            else:
                print("  고전 게임 롬팩 수준의 100% 솔리드 컬러 픽셀 애니메이션 구동 중...")
            time.sleep(0.75)
