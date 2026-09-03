#!/usr/bin/env python3
"""
tools/generate_all_cutscenes_studio.py
흥부놀부전 1막~7막 전 씬 16색 하이퀄리티 클로즈업 도트 엔진 리메이크!
- 사용자 피드백 100% 반영:
  * 2막: 제비 초대형 클로즈업! (남색 깃털, 붉은 목덜미, 하얀 배, 눈물 어린 눈망울, 붉은 실과 부목 정밀 묘사)
  * 3막: 힘차게 날아오르는 제비 클로즈업 + 부리에 영롱하게 빛나는 황금 박씨
  * 4막: 톱질하는 흥부 부부의 역동적인 표정 + 쪼개지는 거대한 대박과 쏟아지는 황금 엽전 보화!
  * 5막: 놀부의 잔혹한 손아귀 클로즈업! 멀쩡한 제비 다리를 움켜쥐고 뚝 부러뜨리는 순간의 극적 묘사
  * 6막: 압도적인 뿔 도깨비 얼굴 클로즈업! (부리부리한 눈, 날카로운 송곳니, 가시 쇠몽둥이 강타)
  * 7막: 1막 수준의 인물 표정 클로즈업! 감격의 눈물을 흘리는 흥부와 갓 벗고 눈물로 뉘우치는 놀부의 감동적 재회
"""

import os
import sys
import json

sys.path.append("/home/krjoylee/code/game/tools")
from generate_act1_motion_prototype import (
    generate_6_motion_frames as gen_act1,
    PALETTE_16,
    CANVAS_W,
    CANVAS_H,
    C_BG, C_LINE, C_SKIN, C_SHADOW, C_HAT, C_RAG,
    C_SILK_RED, C_SILK_BLUE, C_TEAR, C_WHITE,
    C_SILK_SHINE, C_HEMP_ROUGH, C_GOLD
)

C_SWALLOW_BLUE = 7   # 제비 감청색 등깃
C_SWALLOW_RED = 6    # 제비 목덜미 붉은 깃 / 부목 붉은 실
C_GOBLIN_GREEN = 13  # 도깨비 험악한 청록색 피부
C_CLUB_GRAY = 14     # 쇠몽둥이 / 무쇠 가시
C_FIELD_GREEN = 15   # 새싹 잔디 녹색
C_GOURD_YELLOW = 12  # 잘 익은 황금빛 박

def make_bg():
    return [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]

# ─────────────────────────────────────────────────────────────────────────────
# 제2막: 다친 제비 클로즈업 (두 손으로 감싼 새끼 제비와 붉은 실 부목)
# ─────────────────────────────────────────────────────────────────────────────
def create_act2_frames():
    f1 = make_bg()
    
    # 1. 배경: 흥부네 낡은 흙벽과 처마 그림자 (은은한 음영)
    for y in range(CANVAS_H):
        for x in range(CANVAS_W):
            if (x + y) % 6 == 0:
                f1[y][x] = C_SHADOW
                
    # 2. 흥부의 거칠지만 따스한 두 손 (화면 하단을 감싸 안는 구도, Col 12~62, Row 20~37)
    # 왼손 바닥 (Col 14~34)
    for y in range(22, 36):
        for x in range(14, 34):
            f1[y][x] = C_SKIN
    for y in range(26, 36):
        f1[y][14] = C_SHADOW; f1[y][33] = C_SHADOW
    # 오른손 바닥 (Col 40~60)
    for y in range(22, 36):
        for x in range(40, 60):
            f1[y][x] = C_SKIN
    for y in range(26, 36):
        f1[y][40] = C_SHADOW; f1[y][59] = C_SHADOW
    # 손가락 주름 및 삼베 소매 (Col 8~16, 58~66)
    for y in range(28, 38):
        for x in range(6, 15):
            f1[y][x] = C_HAT if (x+y)%2==0 else C_HEMP_ROUGH
        for x in range(59, 68):
            f1[y][x] = C_HAT if (x+y)%2==0 else C_HEMP_ROUGH

    # 3. [메인 포커스] 새끼 제비 초대형 클로즈업! (중앙 Col 26~48, Row 6~28)
    # 제비 머리 & 등 (감청색 깃털)
    for y in range(6, 16):
        for x in range(28, 46):
            f1[y][x] = C_SWALLOW_BLUE
    # 이마 먹선 외곽
    for x in range(30, 44):
        f1[6][x] = C_LINE
        
    # 제비의 영롱하고 슬픈 눈망울 (Col 31~34, Row 9~12)
    f1[9][32] = C_LINE; f1[9][33] = C_LINE
    f1[10][31] = C_WHITE; f1[10][32] = C_LINE; f1[10][33] = C_WHITE
    f1[11][32] = C_WHITE # 반사광
    # 부리 (노란 새끼 제비 부리)
    f1[11][26] = C_GOLD; f1[11][27] = C_GOLD; f1[12][26] = C_GOLD; f1[12][27] = C_GOLD
    
    # 제비의 상징: 목덜미 선명한 붉은 깃털 (Col 30~42, Row 14~18)
    for y in range(14, 18):
        for x in range(32, 42):
            f1[y][x] = C_SWALLOW_RED
            
    # 배 쪽 보송보송한 순백 깃털 (Col 30~44, Row 18~24)
    for y in range(18, 25):
        for x in range(31, 43):
            f1[y][x] = C_WHITE
            
    # 날개 깃털 결 (남색 + 청록 광택)
    for y in range(12, 24):
        f1[y][43] = C_LINE; f1[y][44] = C_SWALLOW_BLUE; f1[y][45] = C_LINE
        if y % 3 == 0:
            f1[y][44] = C_SILK_SHINE
            
    # 4. [핵심 디테일] 부러진 다리와 정성껏 묶은 붉은 실 부목 (Col 34~42, Row 24~29)
    # 가느다란 부러진 새 다리뼈
    f1[24][37] = C_LINE; f1[25][38] = C_LINE
    # 하얀 대나무 부목 2조각
    for y in range(25, 29):
        f1[y][37] = C_WHITE; f1[y][39] = C_WHITE
    # 붉은 명주실로 칭칭 감은 마디 (Red Thread)
    f1[25][38] = C_SWALLOW_RED
    f1[26][37] = C_SWALLOW_RED; f1[26][38] = C_SWALLOW_RED; f1[26][39] = C_SWALLOW_RED
    f1[27][38] = C_SWALLOW_RED
    f1[28][38] = C_SWALLOW_RED; f1[29][39] = C_SWALLOW_RED # 실타래 리본 매듭!

    # 5. 상단에서 떨어지는 흥부의 따스한 눈물 한 방울
    f1[4][33] = C_TEAR; f1[5][33] = C_WHITE

    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # 제비 호흡 (가슴 깃털 미세 떨림)
        if i in (1, 3, 5):
            fr[19][31] = C_WHITE; fr[20][42] = C_WHITE
        # 제비 눈 깜빡임
        if i == 4:
            fr[10][31] = C_LINE; fr[10][32] = C_LINE; fr[10][33] = C_LINE
        # F3: 눈물방울 톡 떨어져 붉은 실에 닿고 은은한 치유의 빛 발광!
        if i == 2:
            fr[26][38] = C_WHITE # 부목 매듭 발광!
            fr[27][38] = C_WHITE
            fr[11][32] = C_TEAR  # 제비 눈에 맺힌 눈물
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 제3막: 박씨 (창공을 가르는 제비의 웅장한 비행과 영롱한 황금 박씨)
# ─────────────────────────────────────────────────────────────────────────────
def create_act3_frames():
    f1 = make_bg()
    
    # 먼 산과 푸른 봄 하늘 그라데이션
    for x in range(CANVAS_W):
        f1[33][x] = C_FIELD_GREEN; f1[34][x] = C_FIELD_GREEN
        f1[35][x] = C_LINE; f1[36][x] = C_LINE; f1[37][x] = C_LINE # 기와지붕
        
    # 제비 몸통 & 날개 초대형 묘사 (Col 14~60, Row 6~24)
    # 몸통 (Col 30~44, Row 10~22)
    for y in range(10, 20):
        for x in range(32, 42): f1[y][x] = C_SWALLOW_BLUE
    # 머리 & 붉은 목덜미
    for y in range(8, 12):
        for x in range(34, 40): f1[y][x] = C_SWALLOW_BLUE
    for y in range(12, 15):
        for x in range(35, 39): f1[y][x] = C_SWALLOW_RED
    # 가슴 & 하얀 배
    for y in range(15, 21):
        for x in range(34, 40): f1[y][x] = C_WHITE
        
    # 제비 눈
    f1[9][37] = C_WHITE; f1[9][38] = C_LINE
    # 노란 부리
    f1[8][40] = C_GOLD; f1[8][41] = C_GOLD; f1[9][40] = C_GOLD
    
    # [핵심] 부리에 문 황금빛 영롱한 박씨 (Col 42~46, Row 8~12)
    for y in range(8, 12):
        for x in range(42, 46): f1[y][x] = C_GOLD
    f1[9][43] = C_WHITE; f1[10][44] = C_WHITE # 보석 같은 반사광!
    
    # 양 날개 활짝 편 역동적인 실루엣 (Col 12~32, Col 42~62)
    for y in range(8, 15):
        for x in range(14, 32): f1[y][x] = C_SWALLOW_BLUE
        for x in range(42, 60): f1[y][x] = C_SWALLOW_BLUE
    # 날개 깃털 끝 먹선
    for x in range(12, 20): f1[7][x] = C_LINE
    for x in range(54, 62): f1[7][x] = C_LINE
    
    # 갈라진 제비 꼬리 (Row 21~28, Col 34~40)
    f1[22][34] = C_LINE; f1[23][33] = C_LINE; f1[24][32] = C_LINE
    f1[22][40] = C_LINE; f1[23][41] = C_LINE; f1[24][42] = C_LINE
    # 다리에 선명한 '완치된 붉은 실' 흔적!
    f1[20][36] = C_SWALLOW_RED; f1[20][38] = C_SWALLOW_RED

    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # 날개 펄럭임
        if i in (1, 2, 4):
            for x in range(14, 28): fr[6][x] = C_SWALLOW_BLUE; fr[7][x] = C_LINE
            for x in range(46, 60): fr[6][x] = C_SWALLOW_BLUE; fr[7][x] = C_LINE
        # F3: 황금 박씨에서 축복의 광채 십자 발광!
        if i == 2:
            fr[7][44] = C_WHITE; fr[12][44] = C_WHITE
            fr[9][41] = C_WHITE; fr[9][47] = C_WHITE
            for y in range(8, 12):
                for x in range(42, 46): fr[y][x] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 제4막: 흥부의 박 (대박 타기: 톱질하는 부부의 땀방울과 터져 나오는 황금 보화)
# ─────────────────────────────────────────────────────────────────────────────
def create_act4_frames():
    f1 = make_bg()
    
    # 1. 초가지붕 (하단 26~37)
    for y in range(28, 38):
        for x in range(CANVAS_W):
            f1[y][x] = C_HAT if (x+y)%2==0 else C_HEMP_ROUGH
            
    # 2. 지붕 위 거대한 보름달 같은 대박 (중앙 Col 20~54, Row 4~28)
    for y in range(4, 28):
        for x in range(20, 54):
            # 둥근 박의 볼륨감 그라데이션
            dist = abs(x - 37) + abs(y - 16)
            if dist < 18:
                f1[y][x] = C_GOURD_YELLOW
            elif dist < 22:
                f1[y][x] = C_SHADOW
    # 박 꼭지 & 넝쿨
    f1[2][36] = C_FIELD_GREEN; f1[2][37] = C_FIELD_GREEN; f1[3][37] = C_FIELD_GREEN
    
    # 3. 박이 쩍 갈라진 황금빛 틈새 (Col 36~38)
    for y in range(4, 28):
        f1[y][36] = C_GOLD; f1[y][37] = C_WHITE; f1[y][38] = C_GOLD
    # 뿜어져 나오는 엽전/보화 (Col 32~42)
    for y in range(8, 24, 2):
        f1[y][34] = C_GOLD; f1[y][40] = C_GOLD
        f1[y+1][35] = C_WHITE; f1[y+1][39] = C_WHITE
        
    # 4. 좌측 흥부 (힘차게 톱을 당김, Col 6~18, Row 12~30)
    for y in range(12, 22):
        for x in range(8, 16): f1[y][x] = C_SKIN
    f1[10][10] = C_LINE; f1[11][10] = C_LINE # 상투
    f1[14][13] = C_LINE; f1[14][14] = C_LINE # 열정적인 눈
    f1[16][14] = C_WHITE # 이마의 굵은 땀방울!
    # 흥부 삼베옷
    for y in range(22, 32):
        for x in range(6, 18): f1[y][x] = C_HAT if (x+y)%2==0 else C_HEMP_ROUGH
        
    # 5. 우측 흥부 아내 (함께 톱을 잡고 환호, Col 56~68, Row 12~30)
    for y in range(12, 22):
        for x in range(58, 66): f1[y][x] = C_SKIN
    # 쪽진 머리 & 비녀
    for y in range(10, 14):
        for x in range(64, 68): f1[y][x] = C_LINE
    f1[12][68] = C_WHITE # 하얀 비녀
    # 아내 옷 (무명 저고리)
    for y in range(22, 32):
        for x in range(56, 68): f1[y][x] = C_WHITE if (x+y)%2==0 else C_SHADOW
        
    # 6. 두 사람이 맞잡은 긴 무쇠 톱날 (Col 14~60, Row 20)
    for x in range(14, 60):
        f1[20][x] = C_CLUB_GRAY
        if x % 2 == 0: f1[21][x] = C_WHITE # 톱니바퀴 날!

    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # 톱질 좌우 왕복 진동
        shift = (i % 2) * 2 - 1
        for x in range(16, 58): fr[20][x+shift] = C_WHITE
        # F3: 대박 틈새에서 금은보화 대폭발 번쩍광!
        if i == 2:
            for y in range(5, 27):
                fr[y][36] = C_WHITE; fr[y][37] = C_WHITE; fr[y][38] = C_WHITE
            for y in range(6, 26, 3):
                fr[y][32] = C_GOLD; fr[y][42] = C_GOLD
                fr[y][31] = C_WHITE; fr[y][43] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 제5막: 놀부의 욕심 (놀부의 시커먼 손아귀 & 제비 다리 뚝 분지르는 잔혹한 순간 클로즈업)
# ─────────────────────────────────────────────────────────────────────────────
def create_act5_frames():
    f1 = make_bg()
    
    # 1. 배경: 음침하고 흉흉한 어두운 기운
    for y in range(CANVAS_H):
        for x in range(CANVAS_W):
            if (x * 3 + y * 2) % 7 == 0:
                f1[y][x] = C_LINE
                
    # 2. 좌측 상단: 탐욕과 광기에 찬 놀부의 사악한 얼굴 (Col 6~28, Row 2~20)
    for y in range(4, 16):
        for x in range(10, 22): f1[y][x] = C_SKIN
    # 삐딱한 갓과 갓끈
    for x in range(4, 28): f1[4][x] = C_LINE
    for y in range(1, 4):
        for x in range(8, 24): f1[y][x] = C_LINE
    # 치켜뜬 살기 어린 눈망울
    f1[8][13] = C_LINE; f1[8][18] = C_LINE
    f1[9][13] = C_SWALLOW_RED; f1[9][18] = C_SWALLOW_RED # 핏발 선 눈!
    # 번쩍이는 비열한 금이빨
    f1[13][15] = C_GOLD; f1[13][16] = C_LINE
    # 뾰족한 턱수염
    for y in range(16, 20): f1[y][15] = C_LINE; f1[y][16] = C_LINE
    
    # 3. [메인 포커스] 놀부의 기름지고 거친 시커먼 손아귀 (화면 중앙 Col 26~48, Row 14~32)
    # 억센 손가락들 (Col 26~44, Row 16~28)
    for y in range(16, 28):
        for x in range(26, 42): f1[y][x] = C_SKIN
    # 손등 주름과 뼈마디 음영
    for y in range(18, 26):
        f1[y][30] = C_SHADOW; f1[y][35] = C_SHADOW; f1[y][40] = C_SHADOW
    # 비단 소매 (Col 18~28, Row 22~36)
    for y in range(22, 37):
        for x in range(16, 28): f1[y][x] = C_SILK_BLUE
    for y in range(22, 32): f1[y][27] = C_SILK_RED
    
    # 4. 손아귀에 짓눌려 버둥거리는 가련한 제비 (Col 38~58, Row 12~28)
    for y in range(14, 22):
        for x in range(42, 54): f1[y][x] = C_SWALLOW_BLUE
    # 겁에 질려 튀어나올 듯한 제비 눈!
    f1[15][48] = C_WHITE; f1[15][49] = C_LINE; f1[16][48] = C_WHITE
    # 비명을 지르듯 벌린 부리
    f1[16][54] = C_GOLD; f1[17][55] = C_GOLD
    # 제비의 붉은 목덜미
    f1[18][48] = C_SWALLOW_RED; f1[18][49] = C_SWALLOW_RED
    
    # 5. [결정적 순간] 손가락으로 다리를 잡고 '뚝' 꺾는 지점 (Col 38~46, Row 24~30)
    f1[24][41] = C_LINE; f1[25][42] = C_LINE
    f1[26][42] = C_SHADOW # 꺾여 비틀린 다리뼈
    f1[27][44] = C_LINE

    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # F3: "꺾!" 뼈 부러지는 충격선 번쩍 & 피 한 방울!
        if i == 2:
            fr[26][42] = C_SWALLOW_RED # 핏자국!
            fr[27][43] = C_SWALLOW_RED
            # 충격 번개 이펙트
            fr[24][44] = C_WHITE; fr[25][45] = C_WHITE; fr[26][46] = C_WHITE
            fr[13][15] = C_WHITE # 놀부 금이빨 번쩍
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 제6막: 놀부의 박 (청록색 뿔 도깨비 얼굴 초대형 클로즈업 & 무시무시한 쇠몽둥이)
# ─────────────────────────────────────────────────────────────────────────────
def create_act6_frames():
    f1 = make_bg()
    
    # 1. 붉고 어두운 지옥불 배경 그라데이션
    for y in range(CANVAS_H):
        for x in range(CANVAS_W):
            if (x + y) % 5 == 0: f1[y][x] = C_SILK_RED
            elif (x + y) % 5 == 1: f1[y][x] = C_LINE
            
    # 2. [메인 포커스] 험악한 청록색 외뿔 도깨비 초대형 얼굴 클로즈업! (Col 14~50, Row 4~34)
    # 도깨비 험상궂은 얼굴 윤곽
    for y in range(8, 30):
        for x in range(18, 46): f1[y][x] = C_GOBLIN_GREEN
    # 턱선과 뺨의 짙은 음영
    for y in range(24, 30):
        for x in range(20, 44): f1[y][x] = C_SHADOW
    for y in range(14, 24):
        f1[y][18] = C_LINE; f1[y][45] = C_LINE
        
    # 이마 한가운데 솟구친 날카로운 황금빛 외뿔 (Col 30~34, Row 1~8)
    for y in range(1, 8):
        for x in range(30, 34): f1[y][x] = C_GOLD
    f1[1][31] = C_WHITE; f1[2][32] = C_WHITE # 뿔 끝의 서슬 퍼런 반사광!
    
    # 부리부리하게 치켜뜬 피눈물 붉은 왕방울 눈 (Col 22~27, Col 36~41, Row 12~16)
    for y in range(12, 16):
        for x in range(22, 27): f1[y][x] = C_SWALLOW_RED
        for x in range(37, 42): f1[y][x] = C_SWALLOW_RED
    f1[13][24] = C_WHITE; f1[14][24] = C_LINE # 둥근 동공
    f1[13][39] = C_WHITE; f1[14][39] = C_LINE
    # 험악한 주름과 미간 흉터
    f1[10][31] = C_LINE; f1[11][32] = C_LINE; f1[12][31] = C_LINE
    
    # 찢어진 거대한 입 & 솟구친 하얀 뻐드렁니/송곳니 (Col 24~40, Row 20~26)
    for y in range(21, 25):
        for x in range(24, 40): f1[y][x] = C_LINE
    # 아래위로 삐져나온 거대한 하얀 송곳니 4개
    f1[19][26] = C_WHITE; f1[20][26] = C_WHITE
    f1[19][37] = C_WHITE; f1[20][37] = C_WHITE
    f1[25][28] = C_WHITE; f1[26][28] = C_WHITE
    f1[25][35] = C_WHITE; f1[26][35] = C_WHITE
    
    # 3. 우측: 도깨비가 치켜든 굵직한 가시 쇠몽둥이 (Col 50~66, Row 2~28)
    for y in range(4, 26):
        for x in range(54, 62): f1[y][x] = C_CLUB_GRAY
    # 번쩍이는 무쇠 철 가시 돌기들
    for y in range(6, 24, 4):
        f1[y][52] = C_WHITE; f1[y][53] = C_LINE
        f1[y+2][62] = C_LINE; f1[y+2][63] = C_WHITE
        
    # 4. 하단 좌측: 싹싹 빌며 벌벌 떠는 놀부의 벗겨진 머통 (Col 4~16, Row 28~37)
    for y in range(28, 36):
        for x in range(6, 14): f1[y][x] = C_SKIN
    f1[26][8] = C_LINE # 헝클어진 상투

    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # 눈알 번뜩임
        if i % 2 == 1:
            fr[13][24] = C_LINE; fr[14][24] = C_WHITE
            fr[13][39] = C_LINE; fr[14][39] = C_WHITE
        # F3: 쇠몽둥이 내려치는 벼락 강타 이펙트!
        if i == 2:
            for x in range(CANVAS_W): fr[22][x] = C_WHITE
            for y in range(2, 26): fr[y][57] = C_WHITE
            fr[1][31] = C_WHITE; fr[1][32] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 제7막: 화해 (1막 수준의 고품질 인물 얼굴 클로즈업: 눈물 흘리는 형제의 재회)
# ─────────────────────────────────────────────────────────────────────────────
def create_act7_frames():
    f1 = make_bg()
    
    # 1. 따스한 봄 햇살 배경 (황금빛 & 연초록 들판)
    for x in range(CANVAS_W):
        f1[1][x] = C_GOLD; f1[2][x] = C_GOLD
        f1[35][x] = C_FIELD_GREEN; f1[36][x] = C_FIELD_GREEN; f1[37][x] = C_FIELD_GREEN
        
    # 2. [좌측 흥부 얼굴 클로즈업] (Col 8~28, Row 6~28)
    # 1막과 동일한 꽃미남 귀공자 윤곽과 고운 피부
    for y in range(8, 22):
        for x in range(12, 24): f1[y][x] = C_SKIN
    # 정갈한 상투
    for y in range(3, 8):
        for x in range(16, 20): f1[y][x] = C_LINE
    # 서글프고 자애로운 눈매
    f1[10][14] = C_LINE; f1[10][15] = C_LINE
    f1[10][20] = C_LINE; f1[10][21] = C_LINE
    f1[12][14] = C_WHITE; f1[12][15] = C_LINE
    f1[12][20] = C_LINE; f1[12][21] = C_WHITE
    # 날렵한 V턱선과 뺨
    for y in range(18, 23):
        f1[y][13] = C_SHADOW; f1[y][23] = C_SHADOW
    for x in range(14, 23): f1[22][x] = C_SHADOW
    # 감격의 눈물방울 (하늘색 + 흰색)
    f1[14][15] = C_TEAR; f1[15][15] = C_WHITE; f1[16][15] = C_TEAR
    # 깨끗하고 단정한 도포 (부자가 되었으나 비단 대신 소박하고 정갈한 푸른 옷)
    for y in range(23, 37):
        for x in range(6, 28): f1[y][x] = C_SILK_BLUE
    for y in range(23, 32): f1[y][18] = C_WHITE
    
    # 3. [우측 놀부 얼굴 클로즈업] (Col 46~66, Row 8~30)
    # 갓이 벗겨져 헝클어진 머리칼과 초췌한 피부
    for y in range(10, 24):
        for x in range(50, 62): f1[y][x] = C_SKIN
    # 헝클어져 풀어헤쳐진 산발 상투
    for y in range(5, 11):
        for x in range(53, 59): f1[y][x] = C_LINE
    f1[8][50] = C_LINE; f1[9][49] = C_LINE; f1[8][62] = C_LINE # 흩날리는 머리카락
    # 후회와 참회의 처진 눈 (1막의 세모 눈이 풀려 굵은 눈물을 쏟아냄)
    f1[13][52] = C_LINE; f1[13][53] = C_LINE
    f1[13][58] = C_LINE; f1[13][59] = C_LINE
    f1[14][52] = C_WHITE; f1[14][53] = C_LINE
    f1[14][58] = C_LINE; f1[14][59] = C_WHITE
    # 뼈만 앙상한 수척한 볼 & 턱수염
    for y in range(20, 25):
        f1[y][51] = C_SHADOW; f1[y][61] = C_SHADOW
    for y in range(24, 28): f1[y][56] = C_LINE
    # 참회의 굵은 눈물 줄기 (볼을 타고 뚝뚝 떨어짐)
    f1[15][53] = C_TEAR; f1[16][53] = C_WHITE; f1[17][53] = C_TEAR
    f1[16][58] = C_TEAR; f1[17][58] = C_WHITE
    # 찢겨나간 거지 누더기 옷
    for y in range(25, 37):
        for x in range(46, 68):
            f1[y][x] = C_RAG if (x+y)%2==0 else C_SHADOW
            
    # 4. [중앙] 형제가 눈물로 굳게 맞잡은 두 손 (Col 28~46, Row 24~32)
    for y in range(26, 31):
        for x in range(28, 46): f1[y][x] = C_SKIN
    for x in range(32, 42, 2): f1[27][x] = C_SHADOW; f1[29][x] = C_SHADOW

    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # 흥부와 놀부의 눈물 반짝임
        if i % 2 == 1:
            fr[15][15] = C_WHITE; fr[16][53] = C_WHITE
        # F3: 형제의 눈물과 봄 햇살이 어우러져 따스한 황금빛 광채 발광!
        if i == 2:
            for x in range(24, 50): fr[2][x] = C_WHITE
            for x in range(32, 42): fr[28][x] = C_WHITE # 맞잡은 두 손 발광!
            fr[16][15] = C_WHITE; fr[17][53] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 스튜디오 HTML 갱신 빌드
# ─────────────────────────────────────────────────────────────────────────────
def build_all_studio():
    act1 = gen_act1()
    act2 = create_act2_frames()
    act3 = create_act3_frames()
    act4 = create_act4_frames()
    act5 = create_act5_frames()
    act6 = create_act6_frames()
    act7 = create_act7_frames()
    
    all_acts = [
        {"id": 1, "title": "제1막: 형제의 갈림길", "desc": "[기준 프레임] 탐욕스러운 놀부의 칠흑 갓 + 황금 앞니(금이빨) 번쩍광 vs 서글픈 흥부의 눈물", "frames": act1},
        {"id": 2, "title": "제2막: 다친 제비 클로즈업", "desc": "[피드백 반영] 두 손으로 소중히 감싼 새끼 제비 초대형 클로즈업! 붉은 목덜미, 눈물 어린 눈망울, 붉은 실과 하얀 대나무 부목 묘사", "frames": act2},
        {"id": 3, "title": "제3막: 보은의 비행과 박씨", "desc": "[피드백 반영] 푸른 창공을 가르는 제비의 웅장한 날개짓 클로즈업 + 부리에 영롱하게 빛나는 황금 박씨 광채", "frames": act3},
        {"id": 4, "title": "제4막: 대박 타기와 황금 보화", "desc": "[피드백 반영] 땀방울을 흘리며 신명 나게 톱질하는 흥부 부부의 표정 + 쪼개지는 대박 속에서 쏟아지는 황금 엽전 보화 폭풍", "frames": act4},
        {"id": 5, "title": "제5막: 놀부의 잔혹한 만행", "desc": "[피드백 반영] 놀부의 시커먼 손아귀 클로즈업! 살기 어린 핏발 선 눈과 제비 다리를 뚝 꺾어버리는 극적인 순간", "frames": act5},
        {"id": 6, "title": "제6막: 도깨비의 심판", "desc": "[피드백 반영] 솟구친 황금 외뿔, 부리부리한 눈, 날카로운 송곳니를 드러낸 청록색 도깨비 얼굴 초대형 클로즈업 & 가시 쇠몽둥이 응징", "frames": act6},
        {"id": 7, "title": "제7막: 눈물의 화해", "desc": "[피드백 반영] 1막 수준 인물 클로즈업! 감격의 눈물을 흘리는 흥부와 갓 벗고 눈물로 뉘우치는 놀부의 감동적 재회와 맞잡은 두 손", "frames": act7},
    ]
    
    palette_hex = [f"#{c[2][0]:02x}{c[2][1]:02x}{c[2][2]:02x}" for c in PALETTE_16]
    
    studio_json = json.dumps({
        "palette": palette_hex,
        "acts": all_acts
    })
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Divina Ludus — 컷씬 검토 & 컨펌 스튜디오 (High-Res Close-Up Remake)</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; }}
  html, body {{
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  .studio-frame {{
    width: 980px;
    height: 840px;
    background: #1e1e1e;
    border: 3px solid #4a4a4a;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.9);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .studio-header {{
    background: #2d2d2d;
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #3a3a3a;
  }}
  .studio-title {{ font-size: 16px; font-weight: bold; color: #ffcc99; }}
  .studio-hud {{ font-size: 13px; color: #81d4fa; font-family: monospace; }}
  
  .main-content {{
    flex: 1;
    display: flex;
    background: #181818;
  }}
  .sidebar {{
    width: 250px;
    background: #222;
    border-right: 2px solid #333;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow-y: auto;
  }}
  .nav-btn {{
    background: #2a2a2a;
    color: #bbb;
    border: 1px solid #3c3c3c;
    padding: 11px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    text-align: left;
    transition: all 0.2s;
  }}
  .nav-btn:hover {{
    background: #383838;
    color: #fff;
    border-color: #777;
  }}
  .nav-btn.active {{
    background: #2c3e50;
    color: #f1c40f;
    border-color: #f39c12;
    font-weight: bold;
  }}
  
  .display-area {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 16px 20px;
    gap: 14px;
  }}
  .canvas-wrapper {{
    background: #0a0a0a;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
    border-radius: 6px;
    border: 2px solid #333;
  }}
  canvas {{
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    width: 680px;
    height: 350px;
    background: #252525;
    box-shadow: 0 4px 15px rgba(0,0,0,0.7);
  }}
  
  .info-card {{
    background: #222;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .info-title {{ font-size: 16px; font-weight: bold; color: #f4d03f; }}
  .info-desc {{ font-size: 14px; color: #ccc; line-height: 1.5; }}
  
  .footer-bar {{
    background: #252525;
    padding: 10px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 2px solid #3a3a3a;
    font-size: 13px;
    color: #aaa;
  }}
  .key-hint {{
    color: #81d4fa;
    font-family: monospace;
    font-weight: bold;
  }}
</style>
</head>
<body>

<div class="studio-frame">
  <div class="studio-header">
    <div class="studio-title">🎨 Divina Ludus — 컷씬 검토 & 컨펌 스튜디오 (High-Res Remake)</div>
    <div class="studio-hud" id="hudText">[Act 1 / 7 | 296x152 4X Hi-Res]</div>
  </div>

  <div class="main-content">
    <div class="sidebar" id="sidebar"></div>

    <div class="display-area">
      <div class="canvas-wrapper">
        <canvas id="retroCanvas" width="296" height="152"></canvas>
      </div>

      <div class="info-card">
        <div class="info-title" id="cardTitle">제1막</div>
        <div class="info-desc" id="cardDesc">설명</div>
      </div>
    </div>
  </div>

  <div class="footer-bar">
    <div>조작: <span class="key-hint">[1~7] 숫자키</span>로 씬 즉시 이동 | <span class="key-hint">[Space]</span> 정지/재생 | 마우스 클릭 가능</div>
    <div style="color: #2ecc71;">● 1막 수준 고화질 클로즈업 일괄 리메이크 완료</div>
  </div>
</div>

<script>
  const data = {studio_json};
  const canvas = document.getElementById('retroCanvas');
  const ctx = canvas.getContext('2d');
  
  let curActIdx = 0;
  let curFrame = 0;
  let isPaused = false;
  
  const sidebar = document.getElementById('sidebar');
  data.acts.forEach((act, idx) => {{
    const btn = document.createElement('button');
    btn.className = 'nav-btn' + (idx === 0 ? ' active' : '');
    btn.innerText = `[${{idx+1}}] ${{act.title}}`;
    btn.onclick = () => selectAct(idx);
    sidebar.appendChild(btn);
  }});
  
  function selectAct(idx) {{
    curActIdx = idx;
    curFrame = 0;
    
    const btns = sidebar.querySelectorAll('.nav-btn');
    btns.forEach((b, i) => {{
      b.className = 'nav-btn' + (i === idx ? ' active' : '');
    }});
    
    const act = data.acts[curActIdx];
    document.getElementById('cardTitle').innerText = act.title;
    document.getElementById('cardDesc').innerText = act.desc;
    document.getElementById('hudText').innerText = `[${{act.title}} | F1/6 296x152]`;
    
    renderCurrentFrame();
  }}
  
  function renderCurrentFrame() {{
    const act = data.acts[curActIdx];
    const grid = act.frames[curFrame];
    const srcH = grid.length;
    const srcW = grid[0].length;
    
    for (let y = 0; y < srcH; y++) {{
      for (let x = 0; x < srcW; x++) {{
        const colorIdx = grid[y][x];
        ctx.fillStyle = data.palette[colorIdx];
        ctx.fillRect(x * 4, y * 4, 4, 4);
      }}
    }}
    
    const hud = document.getElementById('hudText');
    if (curFrame === 2) {{
      hud.innerText = `[${{act.title}} | ★ F3 핵심 감정/광채 하이라이트 ★]`;
      hud.style.color = "#f4d03f";
    }} else {{
      hud.innerText = `[${{act.title}} | F${{curFrame+1}}/6 4X Hi-Res 296x152]`;
      hud.style.color = "#81d4fa";
    }}
  }}
  
  setInterval(() => {{
    if (isPaused) return;
    const act = data.acts[curActIdx];
    curFrame = (curFrame + 1) % act.frames.length;
    renderCurrentFrame();
  }}, 750);
  
  selectAct(0);
  
  window.addEventListener('keydown', (e) => {{
    const num = parseInt(e.key);
    if (num >= 1 && num <= data.acts.length) {{
      selectAct(num - 1);
    }} else if (e.code === 'Space') {{
      isPaused = !isPaused;
    }}
  }});
  
  window.addEventListener('wheel', (e) => {{
    e.preventDefault();
  }}, {{ passive: false }});
</script>

</body>
</html>
"""
    studio_html_path = "/mnt/d/game/images/studio.html"
    with open(studio_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 흥부놀부전 1~7막 전 씬 1막 수준 고화질 클로즈업 리메이크 완료: {studio_html_path}")

if __name__ == "__main__":
    build_all_studio()
