#!/usr/bin/env python3
"""
tools/generate_act1_motion_prototype.py
진짜 고전 8비트(패미컴/MSX) 도트 감성 복원:
- 터미널 74 x 38 서브픽셀 캔버스 (Half-block '▀' 기반)
- 상하 2배 정밀 해상도로 눈동자, 쌍꺼풀, 콧날, 수염의 미세 디테일 완벽 복원!
- 칠흑 같은 덩어리 칠이 아닌, [또렷한 외곽선 + 밝은 피부톤 + 선명한 눈동자 + 반짝이는 금이빨]의 8비트 명작 스타일!
- 0.75초 차분한 6프레임 미세 원근 모션
"""

import os
import sys
import time

sys.path.append("/home/krjoylee/code/game/tools")
from palette_engine import render_half_block_canvas, PALETTE_16

CANVAS_W = 74
CANVAS_H = 38  # 38줄 픽셀 ➔ 터미널 19줄 '▀'로 렌더링!

# 16색 인덱스 정의
C_BG = 0          # 0: 어두운 배경
C_LINE = 1        # 1: 칠흑 먹선, 갓, 눈썹, 동공, 수염
C_SKIN = 2        # 2: 밝은 살구색 피부
C_SHADOW = 3      # 3: 피부 음영, 콧대, 턱선, 다크서클
C_HAT = 4         # 4: 흥부 터진 갓 파편, 삼베옷
C_RAG = 5         # 5: 누더기 헝겊 갈색
C_SILK_RED = 6    # 6: 놀부 비단 깃 주홍
C_SILK_BLUE = 7   # 7: 놀부 비단 도포 청색
C_TEAR = 8        # 8: 흥부 눈물 하늘색
C_WHITE = 9       # 9: 흰자위, 치아, 눈물 반사광
C_GOLD = 12       # 12: ★ 놀부 금이빨 황금빛!

def create_base_8bit_canvas():
    """기준 프레임 (F1) 74x38 고밀도 8비트 도트 캔버스 생성"""
    canvas = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # ─────────────────────────────────────────────────────────────
    # [좌측: 놀부 (Nolbu) — 8비트 패미컴 보스 스타일]
    # 중심 좌표: x: 8~32, y: 3~34
    # ─────────────────────────────────────────────────────────────
    
    # 1. 넓은 양반 갓 (Row 3~9, Col 8~32)
    # 갓 모자
    for y in range(3, 8):
        for x in range(15, 26):
            canvas[y][x] = C_LINE
    # 갓 챙 (날카롭고 넓은 가로선)
    for x in range(7, 34):
        canvas[8][x] = C_LINE
    # 갓끈
    for y in range(9, 14):
        canvas[y][15] = C_LINE
        canvas[y][25] = C_LINE
        
    # 2. 얼굴 윤곽 & 피부 (Row 9~21, Col 15~25)
    for y in range(9, 21):
        for x in range(16, 25):
            canvas[y][x] = C_SKIN
    # 볼과 턱 외곽 음영선
    for y in range(17, 21):
        canvas[y][16] = C_SHADOW
        canvas[y][24] = C_SHADOW
    for x in range(17, 24):
        canvas[20][x] = C_SHADOW
        
    # 3. 위로 찢어진 세모 눈 & 치켜뜬 눈썹 (Row 11~13)
    # 눈썹 (사납게 치켜뜸)
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
    # 아랫입술 벌림 & 금이빨 (12번 황금 도트)
    canvas[18][19] = C_LINE
    canvas[18][20] = C_GOLD  # ★ 놀부의 상징: 황금 앞니!
    canvas[18][21] = C_LINE
    
    # 6. 빳빳하고 뾰족한 검은 턱수염 (Row 21~25)
    for y in range(21, 24):
        canvas[y][19] = C_LINE; canvas[y][20] = C_LINE; canvas[y][21] = C_LINE
    canvas[24][20] = C_LINE; canvas[25][20] = C_LINE
    
    # 7. 비단 도포 & 붉은 깃 (Row 23~35)
    for y in range(23, 36):
        for x in range(10, 31):
            canvas[y][x] = C_SILK_BLUE
    # 화려한 붉은 깃
    for y in range(23, 30):
        canvas[y][19] = C_SILK_RED
        canvas[y][20] = C_SILK_RED

    # ─────────────────────────────────────────────────────────────
    # [우측: 흥부 (Heungbu) — 8비트 수려한 꽃미남 빈티]
    # 중심 좌표: x: 44~66, y: 2~35
    # ─────────────────────────────────────────────────────────────
    
    # 1. 터진 갓 & 솟아오른 상투 (Row 2~8, Col 48~62)
    # 상투 꼭지 & 머리 뭉치
    canvas[2][54] = C_LINE; canvas[2][55] = C_LINE
    for y in range(3, 6):
        for x in range(53, 57):
            canvas[y][x] = C_LINE
    # 이마의 망건 (검은 띠)
    for x in range(50, 60):
        canvas[6][x] = C_LINE
    # 부서져 덜렁거리는 갓 테두리 조각 (누런색)
    canvas[6][48] = C_HAT; canvas[6][49] = C_HAT
    canvas[6][60] = C_HAT; canvas[6][61] = C_HAT
    # 흩날리는 잔머리
    canvas[7][49] = C_LINE; canvas[7][60] = C_LINE
    
    # 2. 꽃미남 고운 피부 윤곽 & V라인 턱선 (Row 7~20, Col 50~59)
    for y in range(7, 19):
        for x in range(51, 59):
            canvas[y][x] = C_SKIN
            
    # 3. 짙고 단정한 귀공자 눈썹 & 사연 있는 처진 눈매 (Row 9~12)
    # 짙고 곧은 눈썹
    canvas[9][52] = C_LINE; canvas[9][53] = C_LINE
    canvas[9][56] = C_LINE; canvas[9][57] = C_LINE
    # 깊고 맑은 눈망울 (흰자위와 흑색 동공)
    canvas[11][52] = C_WHITE; canvas[11][53] = C_LINE
    canvas[11][56] = C_LINE; canvas[11][57] = C_WHITE
    # 처진 눈가 음영 (다크서클)
    canvas[12][51] = C_SHADOW; canvas[12][54] = C_SHADOW
    canvas[12][55] = C_SHADOW; canvas[12][58] = C_SHADOW
    
    # 4. 오뚝하고 곧은 콧날 (Row 13~16)
    canvas[13][54] = C_SHADOW; canvas[14][54] = C_SHADOW; canvas[15][54] = C_SHADOW
    canvas[16][54] = C_LINE; canvas[16][55] = C_SHADOW # 콧방울
    
    # 5. 서글프게 다문 입술 & 날렵한 V라인 턱끝 (Row 17~20)
    canvas[17][53] = C_SHADOW; canvas[17][54] = C_LINE; canvas[17][55] = C_LINE; canvas[17][56] = C_SHADOW
    # V라인 턱선
    canvas[19][52] = C_SHADOW; canvas[19][57] = C_SHADOW
    canvas[20][53] = C_SHADOW; canvas[20][54] = C_SHADOW; canvas[20][55] = C_SHADOW; canvas[20][56] = C_SHADOW
    canvas[21][54] = C_SHADOW; canvas[21][55] = C_SHADOW # 뾰족한 턱끝
    
    # 6. 뺨을 타고 흐르는 굵은 눈물 (Row 13~16, Col 52)
    canvas[13][52] = C_TEAR   # 눈물 시작
    canvas[14][52] = C_WHITE  # 반사광
    canvas[15][52] = C_TEAR   # 흐르는 줄기
    
    # 7. 목선과 쇄골이 드러난 누더기 삼베옷 (Row 22~35)
    # 드러난 목선/쇄골 (피부톤)
    canvas[22][53] = C_SKIN; canvas[22][54] = C_SKIN; canvas[22][55] = C_SKIN; canvas[22][56] = C_SKIN
    canvas[23][54] = C_SHADOW; canvas[23][55] = C_SHADOW # 쇄골 음영
    # 누더기 옷몸통
    for y in range(24, 36):
        for x in range(46, 64):
            canvas[y][x] = C_HAT
    # 헝겊 기운 자국 (갈색)
    canvas[27][49] = C_RAG; canvas[27][50] = C_RAG; canvas[28][49] = C_RAG
    canvas[30][59] = C_RAG; canvas[30][60] = C_RAG; canvas[31][60] = C_RAG
    
    return canvas


def generate_6_motion_frames():
    """8비트 도트 6프레임 미세 원근/호흡 모션 (F1~F6)"""
    frames = []
    
    # F1: 기본 프레임
    f1 = create_base_8bit_canvas()
    frames.append(f1)
    
    # F2: 들숨 팽창 (+1px 외곽 확장, 상투 머리칼 들림)
    f2 = [row[:] for row in f1]
    for y in range(24, 34):
        f2[y][9] = C_SILK_BLUE
        f2[y][31] = C_SILK_BLUE
    f2[1][54] = C_LINE; f2[1][55] = C_LINE # 상투 털끝 1px 들림
    frames.append(f2)
    
    # F3: ★ 핵심 순간 (놀부 금이빨 번쩍광 On! + 흥부 눈물 낙하)
    f3 = [row[:] for row in f1]
    # 놀부 입 크게 열리며 순백/황금 번쩍광 폭발!
    f3[18][19] = C_GOLD
    f3[18][20] = C_WHITE # ★ 번쩍!
    f3[18][21] = C_GOLD
    f3[19][20] = C_WHITE # 반사광
    # 놀부 수염 부르르 좌우 1px 진동
    f3[24][19] = C_LINE; f3[24][21] = C_LINE
    # 흥부 눈물 1px 아래로 똑 떨어짐
    f3[13][52] = C_SKIN  # 지나간 자리는 피부
    f3[16][52] = C_WHITE # 눈물방울 낙하
    f3[17][52] = C_TEAR
    frames.append(f3)
    
    # F4: 날숨 수축 (-1px 수축, 흥부 어깨 처짐)
    f4 = [row[:] for row in f1]
    for y in range(25, 34):
        f4[y][10] = C_BG; f4[y][30] = C_BG
    f4[24][48] = C_BG; f4[24][62] = C_BG
    frames.append(f4)
    
    # F5: 잔상 (금이빨 빛 감쇄, 흥부 턱끝에 눈물 맺힘)
    f5 = [row[:] for row in f1]
    f5[18][20] = C_GOLD  # 금이빨 기본 복귀
    f5[20][53] = C_TEAR  # 턱끝에 영롱하게 맺힌 눈물
    frames.append(f5)
    
    # F6: 복귀 루프
    f6 = [row[:] for row in f1]
    frames.append(f6)
    
    return frames


if __name__ == "__main__":
    frames = generate_6_motion_frames()
    print("🕹️ [고전 8비트 도트 모션] 패미컴/MSX 스타일 2x 정밀 하프블록(Half-Block) 렌더링")
    print("   속도: 0.75초 | 또렷한 눈동자/콧날 디테일 | Ctrl+C로 종료\n")
    
    for loop in range(2):
        for idx, fr in enumerate(frames, 1):
            sys.stdout.write("\x1b[H") # 화면 원점 이동
            print(f"╔{'═' * 74}╗")
            print(f"║  흥부놀부전 · 1막 [프레임 {idx}/6] (고전 8비트 패미컴 도트 감성)         ║")
            print(f"╠{'═' * 74}╣")
            lines = render_half_block_canvas(fr)
            for l in lines:
                print(f"║{l}║")
            print(f"╚{'═' * 74}╝")
            if idx == 3:
                print("  ★ F3: 놀부의 [황금빛 앞니 번쩍★] & 흥부의 [하늘색 눈물방울 낙하💧]!")
            else:
                print("  8비트 도트 픽셀의 살아있는 원근 호흡 모션 구동 중...")
            time.sleep(0.75)
