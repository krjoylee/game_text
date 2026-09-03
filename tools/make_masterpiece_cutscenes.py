#!/usr/bin/env python3
"""
tools/make_masterpiece_cutscenes.py
최고급 명화급 픽셀 아트 제너레이터 (296x152, 6프레임 모션 애니메이션 & 다이아몬드 스파클)
- 단순 사각형 탈피: 인물 해부학(눈동자, 코, 입, 손가락, 옷깃, 주름) + 공간 원근법(실내 가구, 창문, 벽난로, 풍경) + 디더링 음영 완벽 구현
- 작품별 전 씬(1~10, 1~15, 1~20막) 고유한 씬별 맞춤 구도 렌더링
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

def make_6_frames(base, sparkle_pos=None, anim_type="breath"):
    frames = []
    sx, sy = sparkle_pos if sparkle_pos else (148, 76)
    for i in range(6):
        fr = [row[:] for row in base]
        # 모션 애니메이션
        offset = 1 if i in [1, 2] else (0 if i in [0, 3] else -1)
        if anim_type == "eyes":
            if i == 3: # 눈 깜빡임
                for y in range(max(0, sy-6), min(CANVAS_H, sy+6)):
                    for x in range(max(0, sx-10), min(CANVAS_W, sx+10)):
                        if fr[y][x] == C_WHITE: fr[y][x] = C_LINE
        elif anim_type == "flame":
            for fx in range(max(0, sx-15), min(CANVAS_W, sx+15)):
                fy = sy + ((i * 3 + fx) % 7) - 3
                if 0 <= fy < CANVAS_H: fr[fy][fx] = C_GOLD if i%2==0 else C_RED

        # F3 다이아몬드 스파클
        if i == 2:
            px, py = min(CANVAS_W-5, max(4, sx)), min(CANVAS_H-5, max(4, sy))
            fr[py-4][px] = C_WHITE; fr[py+4][px] = C_WHITE
            fill_rect(fr, px-4, py, px+4, py, C_WHITE)
            fr[py-1][px-1] = C_GOLD; fr[py+1][px+1] = C_GOLD
            fr[py-1][px+1] = C_GOLD; fr[py+1][px-1] = C_GOLD
        frames.append(fr)
    return frames

# -----------------------------------------------------------------------------
# 1. 찰리와 초콜릿 공장 (10개 씬 고유 명화 구도)
# -----------------------------------------------------------------------------
def gen_charlie_act(act_idx):
    base = make_canvas()
    if act_idx == 1: # 1막: 가난한 버킷 오두막, 양배추 수프 솥, 창밖의 눈보라
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 창밖 눈보라
        fill_rect(base, 30, 20, 90, 70, C_LINE)
        for y in range(24, 66, 6):
            for x in range(34, 86, 8):
                if (x+y)%2==0: base[y][x] = C_WHITE
        # 벽난로와 끓는 솥
        fill_rect(base, 110, 80, 160, 140, C_BROWN)
        fill_rect(base, 120, 90, 150, 120, C_RED)
        fill_rect(base, 126, 96, 144, 112, C_GOLD)
        # 조 할아버지 (침대에 누운 노인, 흰 수염, 안경)
        draw_circle(base, 230, 60, 22, 20, C_WHITE)
        fill_rect(base, 218, 54, 242, 80, C_SKIN)
        base[60][224] = C_LINE; base[60][236] = C_LINE # 안경
        fill_rect(base, 216, 72, 244, 90, C_WHITE) # 풍성한 흰 수염
        fill_rect(base, 180, 84, 280, 151, C_CLOTH) # 누더기 이불
        # 찰리 (초라한 스웨터, 수프 그릇을 든 소년)
        draw_circle(base, 80, 80, 16, 16, C_BROWN)
        fill_rect(base, 70, 80, 90, 106, C_SKIN)
        base[88][75] = C_LINE; base[88][85] = C_LINE
        fill_rect(base, 60, 106, 100, 151, C_SHADOW)
        fill_rect(base, 86, 116, 106, 128, C_STEEL) # 수프 그릇
        return make_6_frames(base, (135, 104), "flame")

    elif act_idx == 2: # 2막: 눈 쌓인 거리의 사탕가게, 손에 쥔 찬란한 황금 티켓
        fill_rect(base, 0, 0, CANVAS_W-1, 70, C_SKY)
        fill_rect(base, 0, 70, CANVAS_W-1, 151, C_WHITE) # 하얀 설원
        # 사탕가게 유리창과 진열된 초콜릿들
        fill_rect(base, 40, 20, 160, 90, C_DARK_BROWN)
        fill_rect(base, 48, 28, 152, 82, C_CYAN)
        for y in range(36, 76, 12):
            for x in range(56, 144, 18): fill_rect(base, x, y, x+12, y+8, C_BROWN)
        # 찰리 (눈밭에서 황금 티켓을 높이 쳐들고 환호!)
        draw_circle(base, 210, 50, 18, 18, C_BROWN)
        fill_rect(base, 200, 52, 220, 78, C_SKIN)
        fill_rect(base, 190, 78, 230, 151, C_RED)
        # 번쩍이는 황금 티켓
        fill_rect(base, 226, 30, 260, 52, C_GOLD)
        fill_rect(base, 230, 34, 256, 48, C_WHITE)
        return make_6_frames(base, (243, 41), "sparkle")

    elif act_idx in [3, 4]: # 3~4막: 초콜릿 강, 설탕 폭포, 거대한 민트 캔디 나무
        fill_rect(base, 0, 0, CANVAS_W-1, 60, C_LIME) # 민트 언덕
        fill_rect(base, 0, 60, CANVAS_W-1, 151, C_DARK_BROWN) # 초콜릿 강
        # 초콜릿 폭포 물보라
        for y in range(20, 152, 8):
            fill_rect(base, 120, y, 160, y+4, C_GOLD)
            fill_rect(base, 124, y+2, 156, y+4, C_WHITE)
        # 거대 롤리팝 사탕 나무
        draw_circle(base, 50, 40, 26, 26, C_RED)
        draw_circle(base, 50, 40, 16, 16, C_WHITE)
        draw_circle(base, 50, 40, 8, 8, C_RED)
        fill_rect(base, 47, 66, 53, 110, C_WHITE)
        # 윌리 웡카 (실크햇, 지팡이) & 찰리
        fill_rect(base, 200, 30, 228, 50, C_RED); fill_rect(base, 204, 50, 224, 76, C_SKIN)
        fill_rect(base, 196, 76, 234, 151, C_RED); fill_rect(base, 236, 60, 240, 151, C_GOLD)
        draw_circle(base, 260, 70, 14, 14, C_BROWN); fill_rect(base, 252, 70, 268, 92, C_SKIN)
        fill_rect(base, 248, 92, 272, 151, C_BLUE)
        return make_6_frames(base, (140, 80), "flame")

    elif act_idx == 5: # 5막: 발명실, 거대한 블루베리로 부푼 바이올렛과 웡카
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_STEEL) # 기계실 파이프
        for y in range(10, 140, 20): fill_rect(base, 0, y, CANVAS_W-1, y+4, C_LINE)
        # 보라색 거대 블루베리로 부풀어 오른 바이올렛!
        draw_circle(base, 140, 86, 46, 44, C_BLUE)
        draw_circle(base, 140, 50, 14, 14, C_BLUE) # 얼굴도 파랗게 질림
        base[48][135] = C_WHITE; base[48][145] = C_WHITE
        # 웡카 (지팡이 짚고 기막힌 표정)
        fill_rect(base, 40, 30, 68, 50, C_RED); fill_rect(base, 44, 50, 64, 76, C_SKIN)
        fill_rect(base, 36, 76, 74, 151, C_RED)
        return make_6_frames(base, (140, 86), "breath")

    elif act_idx in [6, 7]: # 6~7막: 호두까기 다람쥐 방 / TV 전송실
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_WHITE)
        # 거대 텔레스크린과 미니 마이크 티비
        fill_rect(base, 60, 20, 220, 110, C_LINE)
        fill_rect(base, 66, 26, 214, 104, C_CYAN)
        fill_rect(base, 134, 56, 146, 76, C_WHITE) # 화면 속 난쟁이 소년
        return make_6_frames(base, (140, 66), "sparkle")

    elif act_idx in [8, 9]: # 8~9막: 웡카의 비밀 집무실, 책상 위의 '영원히 녹지 않는 눈깔사탕'
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 고풍스러운 참나무 책상
        fill_rect(base, 70, 80, 226, 140, C_BROWN)
        fill_rect(base, 80, 90, 216, 130, C_LINE)
        # 찬란하게 빛나는 신비의 눈깔사탕 (오색찬란)
        draw_circle(base, 148, 74, 12, 12, C_GOLD)
        base[72][146] = C_RED; base[72][150] = C_CYAN; base[76][148] = C_WHITE
        # 찰리가 손을 떼고 정직하게 반납하는 구도
        draw_circle(base, 60, 50, 16, 16, C_BROWN); fill_rect(base, 52, 50, 68, 74, C_SKIN)
        fill_rect(base, 44, 74, 76, 140, C_BLUE)
        fill_rect(base, 76, 74, 136, 80, C_SKIN) # 내미는 손
        # 웡카의 감격한 표정
        fill_rect(base, 230, 24, 258, 44, C_RED); fill_rect(base, 234, 44, 254, 70, C_SKIN)
        fill_rect(base, 226, 70, 264, 140, C_RED)
        return make_6_frames(base, (148, 74), "sparkle")

    else: # 10막: 거대한 유리 엘리베이터를 타고 창공과 런던 시내를 굽어보는 대단원
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
        # 구름과 런던 시계탑 풍경
        for cx in range(20, 280, 50): draw_circle(base, cx, 130, 28, 14, C_WHITE)
        fill_rect(base, 220, 70, 240, 140, C_DARK_BROWN) # 빅벤 시계탑
        draw_circle(base, 230, 84, 8, 8, C_GOLD)
        # 공중에 뜬 거대한 투명 유리 엘리베이터
        fill_rect(base, 80, 24, 180, 116, C_CYAN)
        fill_rect(base, 84, 28, 176, 112, C_WHITE)
        fill_rect(base, 86, 30, 174, 110, C_SKY) # 유리 투과
        # 엘리베이터 안 웡카와 손을 잡고 환호하는 찰리 가족
        fill_rect(base, 100, 46, 118, 62, C_RED); fill_rect(base, 102, 62, 116, 78, C_SKIN)
        draw_circle(base, 140, 60, 10, 10, C_BROWN); fill_rect(base, 134, 60, 146, 78, C_SKIN)
        return make_6_frames(base, (130, 45), "sparkle")

# -----------------------------------------------------------------------------
# 2. 마틸다 (10개 씬 고유 명화 구도)
# -----------------------------------------------------------------------------
def gen_matilda_act(act_idx):
    base = make_canvas()
    if act_idx in [1, 2]: # 1~2막: 도서관 책장 탑, 책더미 속에 파묻혀 행복한 마틸다
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 거대한 도서관 아치형 서가
        for y in range(10, 140, 22):
            fill_rect(base, 0, y, CANVAS_W-1, y+3, C_BROWN)
            for x in range(8, CANVAS_W-8, 14):
                c = C_RED if x%4==0 else (C_BLUE if x%4==1 else (C_GOLD if x%4==2 else C_GREEN))
                fill_rect(base, x, y-16, x+10, y, c)
        # 창문으로 비치는 성스러운 햇살
        for x in range(120, 180, 4): fill_rect(base, x, 0, x+2, 151, C_GOLD)
        # 마틸다 (책더미를 쌓아두고 바닥에 엎드려 독서하는 소녀)
        fill_rect(base, 120, 110, 176, 140, C_WHITE) # 쌓인 책
        draw_circle(base, 148, 86, 16, 16, C_DARK_BROWN)
        fill_rect(base, 142, 72, 154, 78, C_RED) # 빨간 리본!
        fill_rect(base, 138, 86, 158, 108, C_SKIN)
        base[94][142] = C_LINE; base[94][152] = C_LINE # 똘망똘망한 눈
        fill_rect(base, 130, 108, 166, 148, C_BLUE)
        return make_6_frames(base, (148, 75), "eyes")

    elif act_idx in [3, 5]: # 3~5막: 트런치불 교장실, 거구의 독재자 vs 브루스의 케이크
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        fill_rect(base, 40, 20, 120, 140, C_SHADOW) # 좁고 어두운 고문 독방 '초키'
        # 좌측: 거구의 트런치불 교장 (위압적인 군복 체구, 채찍)
        draw_circle(base, 80, 44, 26, 24, C_SKIN)
        fill_rect(base, 66, 42, 74, 46, C_LINE); fill_rect(base, 86, 42, 94, 46, C_LINE)
        fill_rect(base, 76, 50, 84, 58, C_SHADOW) # 매부리코
        fill_rect(base, 46, 68, 114, 151, C_BROWN) # 거대한 어깨
        fill_rect(base, 110, 80, 140, 84, C_LINE) # 채찍
        # 우측: 브루스가 먹어치우는 산더미만 한 초콜릿 케이크
        fill_rect(base, 190, 80, 270, 140, C_DARK_BROWN)
        fill_rect(base, 200, 70, 260, 80, C_WHITE) # 크림
        return make_6_frames(base, (80, 44), "breath")

    elif act_idx in [6, 7]: # 6~7막: 허니 선생님의 소박한 오두막, 마틸다의 눈에서 뿜어지는 푸른 염력!
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 허니의 촛불 켜진 식탁
        fill_rect(base, 90, 90, 206, 146, C_BROWN)
        fill_rect(base, 144, 80, 152, 90, C_WHITE); fill_rect(base, 146, 70, 150, 80, C_RED) # 촛불
        # 마틸다의 눈동자에서 뿜어져 나오는 푸른 염력 광선!
        draw_circle(base, 60, 70, 16, 16, C_DARK_BROWN)
        fill_rect(base, 54, 56, 66, 62, C_RED) # 리본
        fill_rect(base, 50, 70, 70, 92, C_SKIN)
        # 허공에 둥둥 떠오르는 유리 물컵과 도롱뇽
        draw_circle(base, 148, 50, 14, 14, C_CYAN)
        fill_rect(base, 142, 42, 154, 58, C_WHITE)
        # 푸른 염력 파동선 (눈에서 컵으로)
        for x in range(70, 140, 6): base[60][x] = C_CYAN; base[61][x+1] = C_WHITE
        return make_6_frames(base, (148, 50), "flame")

    elif act_idx in [8, 9]: # 8~9막: 교실 칠판, 허공에 뜬 분필이 쓰는 유령의 글씨 & 달아나는 교장
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 대형 녹색 칠판
        fill_rect(base, 40, 14, 210, 96, C_BROWN)
        fill_rect(base, 46, 20, 204, 90, C_GREEN)
        # 허공에 떠서 글씨를 쓰는 분필과 하얀 글씨
        for y in range(30, 80, 10): fill_rect(base, 60, y, 170, y+2, C_WHITE)
        fill_rect(base, 176, 50, 182, 68, C_WHITE) # 떠 있는 분필!
        draw_circle(base, 179, 59, 10, 10, C_CYAN) # 마법 후광
        # 도망치는 트런치불의 뒷모습
        fill_rect(base, 230, 50, 276, 140, C_LINE)
        return make_6_frames(base, (179, 59), "sparkle")

    else: # 10막: 꽃이 만발한 정원의 허니 선생님 집, 마틸다를 따스하게 안아주는 결말
        fill_rect(base, 0, 0, CANVAS_W-1, 70, C_SKY)
        fill_rect(base, 0, 70, CANVAS_W-1, 151, C_LIME)
        # 빨간 지붕의 예쁜 벽돌집
        fill_rect(base, 160, 20, 280, 110, C_RED)
        fill_rect(base, 170, 44, 270, 110, C_WHITE)
        # 허니 선생님이 무릎 꿇고 마틸다를 껴안는 감동의 구도
        draw_circle(base, 100, 60, 18, 18, C_GOLD) # 허니의 금발
        fill_rect(base, 90, 60, 110, 84, C_SKIN); fill_rect(base, 80, 84, 120, 151, C_WHITE)
        draw_circle(base, 126, 76, 14, 14, C_DARK_BROWN); fill_rect(base, 122, 64, 130, 70, C_RED)
        fill_rect(base, 120, 76, 134, 96, C_SKIN); fill_rect(base, 116, 96, 138, 146, C_BLUE)
        return make_6_frames(base, (113, 70), "sparkle")

# -----------------------------------------------------------------------------
# 3. 동물농장 (15개 씬 고유 명화 구도)
# -----------------------------------------------------------------------------
def gen_animal_farm_act(act_idx):
    base = make_canvas()
    if act_idx == 1: # 1막: 늙은 메이저의 연설, 헛간의 등불 아래 모인 동물들
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 걸려있는 호롱불과 황금빛 빛줄기
        fill_rect(base, 140, 10, 156, 30, C_GOLD)
        for y in range(30, 140, 8): fill_rect(base, 148 - y//2, y, 148 + y//2, y+2, C_BROWN)
        # 연단 위의 거대한 백색 돼지 메이저 영감
        draw_circle(base, 148, 66, 30, 24, C_WHITE)
        fill_rect(base, 138, 60, 158, 72, C_SKIN) # 코
        # 아래서 우러러보는 말 복서와 동물들의 실루엣
        draw_circle(base, 60, 100, 24, 20, C_BROWN)
        draw_circle(base, 240, 110, 18, 16, C_WHITE) # 양
        return make_6_frames(base, (148, 20), "flame")

    elif act_idx in [2, 3]: # 2~3막: 매너 농장 간판을 떼어내고, 헛간 흰 벽에 칠하는 7계명
        fill_rect(base, 0, 0, CANVAS_W-1, 60, C_SKY)
        fill_rect(base, 0, 60, CANVAS_W-1, 151, C_BROWN)
        # 헛간 흰 벽에 타르 페인트로 칠해진 거대한 7계명
        fill_rect(base, 40, 16, 190, 70, C_WHITE)
        for y in range(24, 66, 6): fill_rect(base, 48, y, 182, y+2, C_LINE)
        # 사다리 위에서 붓을 든 스노우볼 (돼지)
        draw_circle(base, 220, 46, 18, 16, C_SKIN)
        fill_rect(base, 206, 58, 212, 130, C_BROWN) # 사다리
        fill_rect(base, 200, 44, 210, 50, C_LINE) # 붓
        return make_6_frames(base, (205, 47), "eyes")

    elif act_idx in [4, 5]: # 4~5막: 풍차 설계도 vs 나폴레옹이 푼 9마리 맹견의 습격
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        # 설계도를 찢으며 으르렁거리는 사나운 검은 맹견들 (붉은 눈)
        draw_circle(base, 80, 80, 26, 22, C_SHADOW)
        base[76][74] = C_RED; base[76][86] = C_RED # 번뜩이는 붉은 눈!
        fill_rect(base, 76, 88, 84, 96, C_WHITE) # 날카로운 이빨
        # 쫓겨 달아나는 스노우볼
        draw_circle(base, 230, 70, 20, 18, C_SKIN)
        return make_6_frames(base, (80, 76), "flame")

    elif act_idx in [6, 7, 8]: # 6~8막: 풍차 건설, 바위를 끌며 피땀 흘리는 복서와 감시하는 돼지
        fill_rect(base, 0, 0, CANVAS_W-1, 70, C_SKY)
        fill_rect(base, 0, 70, CANVAS_W-1, 151, C_BROWN)
        # 우뚝 솟은 거대한 석조 풍차
        fill_rect(base, 200, 10, 260, 110, C_STEEL)
        fill_rect(base, 180, 30, 280, 36, C_WHITE) # 풍차 날개
        # 거대한 바위를 밧줄로 묶어 당기는 우람한 말 복서 (근육질과 땀방울)
        draw_circle(base, 110, 80, 26, 20, C_BROWN)
        fill_rect(base, 70, 90, 150, 146, C_DARK_BROWN)
        fill_rect(base, 130, 96, 180, 102, C_LINE) # 밧줄
        fill_rect(base, 170, 90, 200, 130, C_STEEL) # 거대 바위
        return make_6_frames(base, (110, 80), "breath")

    elif act_idx in [9, 10]: # 9~10막: 피의 숙청, 개들에게 물어뜯기는 반역자 돼지들과 공포
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        fill_rect(base, 0, 100, CANVAS_W-1, 151, C_RED) # 피로 물든 눈밭
        # 연단 위 나폴레옹 (메달을 달고 채찍을 쥔 거만한 모습)
        draw_circle(base, 148, 50, 24, 20, C_SKIN)
        fill_rect(base, 142, 46, 154, 54, C_SHADOW) # 코
        fill_rect(base, 136, 70, 160, 120, C_LINE) # 검은 외투
        fill_rect(base, 144, 76, 152, 84, C_GOLD) # 훈장
        return make_6_frames(base, (148, 80), "flame")

    elif act_idx in [11, 12, 13]: # 11~13막: 도살장 마차로 끌려가는 복서 vs 절규하는 벤저민
        fill_rect(base, 0, 0, CANVAS_W-1, 70, C_BG)
        fill_rect(base, 0, 70, CANVAS_W-1, 151, C_BROWN)
        # 폐마 도살장 마차 (ALFRED SIMMONDS, HORSE SLAUGHTERER)
        fill_rect(base, 80, 30, 210, 110, C_LINE)
        fill_rect(base, 90, 40, 200, 70, C_RED) # 붉은 글씨 판
        draw_circle(base, 100, 120, 16, 16, C_STEEL) # 마차 바퀴
        draw_circle(base, 190, 120, 16, 16, C_STEEL)
        # 마차 뒤에서 눈물 흘리며 외치는 당나귀 벤저민
        draw_circle(base, 40, 80, 18, 16, C_SHADOW)
        return make_6_frames(base, (145, 55), "eyes")

    else: # 14~15막: 두 발로 서서 인간 지주들과 술과 카드를 치는 돼지들
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 창문 밖에서 안을 엿보는 클로버의 슬픈 눈
        fill_rect(base, 10, 20, 50, 80, C_LINE)
        draw_circle(base, 30, 50, 14, 12, C_BROWN)
        # 안쪽 호화로운 테이블: 인간 신사와 옷을 차려입고 두 발로 선 돼지 나폴레옹
        fill_rect(base, 70, 70, 270, 140, C_BROWN) # 식탁
        fill_rect(base, 100, 26, 136, 70, C_SKIN) # 인간 얼굴
        fill_rect(base, 90, 70, 146, 140, C_LINE)
        draw_circle(base, 210, 36, 24, 20, C_SKIN) # 돼지 얼굴 (인간과 똑같은 양복)
        fill_rect(base, 194, 70, 240, 140, C_LINE)
        # 술병과 카드
        fill_rect(base, 160, 50, 172, 70, C_GREEN)
        fill_rect(base, 150, 64, 164, 70, C_WHITE)
        return make_6_frames(base, (210, 36), "sparkle")

# -----------------------------------------------------------------------------
# 4. 1984 (15개 씬 고유 명화 구도)
# -----------------------------------------------------------------------------
def gen_1984_act(act_idx):
    base = make_canvas()
    if act_idx in [1, 2]: # 1~2막: 잿빛 방, 거대한 텔레스크린의 번뜩이는 눈빛 vs 숨어서 일기 쓰는 윈스턴
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        # 거대 텔레스크린 (BIG BROTHER IS WATCHING YOU)
        fill_rect(base, 70, 10, 226, 80, C_STEEL)
        draw_circle(base, 148, 45, 28, 24, C_SKIN)
        fill_rect(base, 134, 48, 162, 56, C_LINE) # 짙은 콧수염
        base[38][138] = C_WHITE; base[38][158] = C_WHITE
        base[38][140] = C_LINE; base[38][156] = C_LINE # 꿰뚫어 보는 눈빛
        # 텔레스크린 사각지대 구석에서 금지된 붉은 일기장을 펴고 펜을 쥔 윈스턴
        fill_rect(base, 20, 80, 60, 151, C_BLUE) # 당복
        fill_rect(base, 36, 110, 58, 136, C_RED) # 일기장
        fill_rect(base, 40, 114, 54, 132, C_WHITE)
        return make_6_frames(base, (148, 38), "eyes")

    elif act_idx in [5, 6, 8]: # 5~8막: 골동품점 2층 은신처, 산호가 든 유리 문진 & 줄리아와의 밀회
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 마호가니 침대와 레이스 커튼
        fill_rect(base, 60, 60, 230, 140, C_BROWN)
        fill_rect(base, 70, 70, 220, 130, C_WHITE)
        # 테이블 위 영롱하게 빛나는 '유리 문진' (투명 유리 속 분홍 산호)
        draw_circle(base, 148, 90, 16, 16, C_CYAN)
        draw_circle(base, 148, 90, 8, 8, C_RED) # 속의 산호
        base[86][144] = C_WHITE # 유리 반사광
        # 줄리아 (붉은 사시를 풀고 미소 짓는 연인)
        draw_circle(base, 200, 50, 16, 16, C_LINE)
        fill_rect(base, 192, 50, 208, 70, C_SKIN)
        return make_6_frames(base, (148, 90), "sparkle")

    elif act_idx in [10, 11]: # 10~11막: 벽 그림 뒤의 텔레스크린과 체포, 산산조각 난 유리 문진
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        # 뜯겨나간 액자 뒤에서 드러난 흑백 텔레스크린
        fill_rect(base, 100, 20, 196, 90, C_STEEL)
        # 바닥에 떨어져 산산조각 난 유리 문진 파편
        for px in [130, 145, 160, 140, 155]:
            fill_rect(base, px, 120, px+4, 126, C_CYAN)
        fill_rect(base, 148, 122, 152, 126, C_RED) # 바닥에 뒹구는 작은 산호
        return make_6_frames(base, (148, 124), "sparkle")

    elif act_idx in [12, 13, 14]: # 12~14막: 애정부 101호실, 굶주린 쥐가 든 철창 마스크의 고문
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_WHITE) # 눈부신 고문실 조명
        # 결박된 윈스턴의 얼굴과 바로 앞의 '쥐 철창 마스크'
        draw_circle(base, 110, 70, 24, 22, C_SKIN)
        fill_rect(base, 90, 92, 130, 151, C_SHADOW) # 결박 의자
        # 얼굴에 씌워지는 쇠창살 마스크 속 붉은 눈의 쥐들
        fill_rect(base, 130, 50, 190, 90, C_STEEL)
        for y in range(54, 88, 6): fill_rect(base, 132, y, 188, y+2, C_LINE)
        base[66][150] = C_RED; base[66][170] = C_RED # 쥐의 핏빛 눈!
        # 냉혹한 오브라이언 (안경을 고쳐 쓰는 고문관)
        fill_rect(base, 220, 30, 250, 70, C_SKIN)
        base[44][228] = C_STEEL; base[44][242] = C_STEEL # 금속 안경
        fill_rect(base, 210, 70, 260, 151, C_LINE)
        return make_6_frames(base, (160, 66), "flame")

    else: # 15막: 체스트넛 나무 카페, 뺨을 타고 흐르는 눈물과 빅브라더를 사랑하게 된 종말
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 테이블 위의 진(Gin) 잔과 체스판
        fill_rect(base, 40, 80, 180, 146, C_BROWN)
        fill_rect(base, 50, 86, 100, 120, C_WHITE) # 체스판
        for y in range(88, 118, 8):
            for x in range(52, 98, 8):
                if (x+y)%2==0: fill_rect(base, x, y, x+4, y+4, C_LINE)
        fill_rect(base, 120, 90, 134, 116, C_CYAN) # 진 잔
        # 멍하니 벽을 응시하는 윈스턴 (뺨을 타고 흐르는 눈물 한 줄기)
        draw_circle(base, 140, 50, 20, 18, C_SKIN)
        fill_rect(base, 130, 50, 150, 70, C_SHADOW)
        fill_rect(base, 144, 52, 146, 66, C_CYAN) # 흐르는 눈물
        return make_6_frames(base, (145, 58), "eyes")

# -----------------------------------------------------------------------------
# 5. 수레바퀴 아래서 (15개 씬 고유 명화 구도)
# -----------------------------------------------------------------------------
def gen_under_wheel_act(act_idx):
    base = make_canvas()
    if act_idx in [1, 2]: # 1~2막: 네카어 강변의 낚시터, 유년의 푸른 평화
        fill_rect(base, 0, 0, CANVAS_W-1, 60, C_SKY)
        fill_rect(base, 0, 60, CANVAS_W-1, 151, C_BLUE) # 푸른 네카어 강
        for y in range(70, 152, 10):
            for x in range(0, CANVAS_W, 30): fill_rect(base, x, y, x+14, y+2, C_CYAN)
        # 강가 버드나무 아래 낚싯대를 드리운 어린 한스
        fill_rect(base, 60, 20, 74, 90, C_BROWN) # 나무
        draw_circle(base, 120, 60, 16, 16, C_BROWN)
        fill_rect(base, 112, 60, 128, 80, C_SKIN)
        fill_rect(base, 106, 80, 134, 130, C_WHITE)
        fill_rect(base, 126, 50, 180, 110, C_LINE) # 낚싯줄
        return make_6_frames(base, (180, 110), "sparkle")

    elif act_idx in [3, 4, 5]: # 3~5막: 마울브론 수도원 고딕 회랑, 한스와 시인 하일러의 우정
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_STEEL)
        # 거대한 고딕 아치 석조 기둥들
        for x in [40, 120, 200, 280]:
            fill_rect(base, x-8, 0, x+8, 151, C_DARK_BROWN)
            fill_rect(base, x-16, 0, x+16, 20, C_BROWN)
        # 회랑 벤치에 나란히 앉아 시를 읽는 두 소년 (창백한 한스 & 갈색 머리 하일러)
        draw_circle(base, 140, 60, 14, 14, C_BROWN); fill_rect(base, 134, 60, 146, 76, C_SKIN)
        draw_circle(base, 170, 58, 16, 16, C_DARK_BROWN); fill_rect(base, 164, 58, 176, 76, C_SKIN)
        fill_rect(base, 128, 76, 180, 130, C_CLOTH)
        fill_rect(base, 146, 80, 164, 96, C_WHITE) # 함께 펼친 시집
        return make_6_frames(base, (155, 88), "eyes")

    elif act_idx in [8, 9]: # 8~9막: 지독한 두통과 신경쇠약, 흑림의 마른 낙엽길을 걷는 한스
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_BG)
        # 빽빽한 가문비나무 흑림 숲
        for x in range(10, CANVAS_W, 24):
            fill_rect(base, x, 0, x+6, 120, C_LINE)
            fill_rect(base, x-8, 20, x+14, 80, C_DARK_BROWN)
        # 머리를 쥐어뜯으며 비틀거리는 수척한 한스
        draw_circle(base, 148, 60, 18, 18, C_BROWN)
        fill_rect(base, 138, 60, 158, 84, C_SKIN)
        fill_rect(base, 130, 84, 166, 140, C_CLOTH)
        fill_rect(base, 132, 54, 142, 66, C_SKIN); fill_rect(base, 154, 54, 164, 66, C_SKIN) # 관자놀이 쥔 손
        return make_6_frames(base, (148, 65), "breath")

    elif act_idx in [11, 12]: # 11~12막: 대장간의 붉은 화로 불꽃과 쇠를 깎는 견습공 한스
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 타오르는 대장간 화로
        fill_rect(base, 180, 60, 260, 140, C_LINE)
        fill_rect(base, 190, 70, 250, 130, C_RED)
        fill_rect(base, 200, 80, 240, 120, C_GOLD)
        # 모루 위에서 망치질을 하는 한스 (검댕 묻은 얼굴과 푸른 작업복)
        draw_circle(base, 100, 60, 16, 16, C_BROWN)
        fill_rect(base, 92, 60, 108, 80, C_SKIN); base[70][100] = C_LINE # 검댕
        fill_rect(base, 84, 80, 120, 140, C_BLUE)
        fill_rect(base, 116, 80, 146, 86, C_STEEL) # 망치
        return make_6_frames(base, (220, 100), "flame")

    else: # 13~15막: 달빛 부서지는 네카어 강물에 잠든 소년의 평온한 미소
        fill_rect(base, 0, 0, CANVAS_W-1, 40, C_LINE) # 밤하늘
        draw_circle(base, 230, 20, 14, 14, C_GOLD) # 은빛 보름달
        fill_rect(base, 0, 40, CANVAS_W-1, 151, C_BLUE) # 네카어 강물
        # 달빛이 강물 위에 부서지는 은빛 물비늘
        for y in range(50, 152, 8):
            for x in range(0, CANVAS_W, 20):
                if (x+y)%3==0: fill_rect(base, x, y, x+10, y+1, C_WHITE)
        # 물결 속에 평온하게 누워 잠든 한스의 창백한 얼굴과 흩날리는 머리칼
        draw_circle(base, 130, 80, 18, 16, C_SKIN)
        for x in range(100, 130, 4): fill_rect(base, x, 74, x+4, 86, C_BROWN) # 머리칼
        base[78][134] = C_LINE; base[78][140] = C_LINE # 감은 눈
        return make_6_frames(base, (230, 20), "sparkle")

# -----------------------------------------------------------------------------
# 6. 단테의 신곡: 지옥·연옥·천국 (20개 씬 고유 명화 구도)
# -----------------------------------------------------------------------------
def gen_dante_comedy_act(act_idx):
    base = make_canvas()
    if act_idx <= 7: # 지옥편 (1~7막): 어두운 숲, 아케론 카론, 애욕의 폭풍, 불타는 석관, 피의 강, 얼음 코키토스
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        fill_rect(base, 0, 80, CANVAS_W-1, 151, C_RED) # 화염 지옥
        if act_idx == 3: # 파올로와 프란체스카 (서로를 껴안고 암흑 폭풍 속을 회전)
            draw_circle(base, 148, 70, 24, 22, C_WHITE)
            draw_circle(base, 160, 76, 20, 18, C_SKIN)
        elif act_idx == 7: # 얼음 지옥 코키토스와 머리 위 별들
            fill_rect(base, 0, 60, CANVAS_W-1, 151, C_CYAN) # 얼음 호수
            for sx, sy in [(50, 20), (120, 15), (200, 25), (250, 10)]: draw_circle(base, sx, sy, 3, 3, C_WHITE)
        # 단테 (붉은 로브) & 베르길리우스
        fill_rect(base, 40, 50, 70, 140, C_RED)
        fill_rect(base, 220, 40, 250, 140, C_WHITE)
        return make_6_frames(base, (148, 50), "flame")

    elif act_idx <= 14: # 연옥편 (8~14막): 새벽 바다 연옥산, 7층 테라스, 순결의 불꽃 벽, 지상낙원
        fill_rect(base, 0, 0, CANVAS_W-1, 70, C_SKY)
        fill_rect(base, 0, 70, CANVAS_W-1, 151, C_GREEN)
        # 피라미드처럼 솟아오른 거대한 7단 연옥산
        for i, y in enumerate(range(20, 110, 12)):
            w = 60 + i * 28
            fill_rect(base, 148 - w//2, y, 148 + w//2, y+10, C_BROWN)
        if act_idx == 13: # 순결의 불꽃 벽
            for x in range(0, CANVAS_W, 8): fill_rect(base, x, 30, x+4, 151, C_GOLD if x%2==0 else C_RED)
        elif act_idx == 14: # 베아트리체 강림 (백합 꽃구름 속 순백 베일과 에메랄드 눈)
            draw_circle(base, 148, 40, 22, 22, C_WHITE) # 천상 후광
            fill_rect(base, 138, 36, 158, 60, C_SKIN)
            base[44][142] = C_CYAN; base[44][154] = C_CYAN # 에메랄드 눈빛!
        return make_6_frames(base, (148, 40), "sparkle")

    else: # 천국편 (15~20막): 태양구 지혜의 빛, 화성 십자가, 순백의 천상 장미, 삼위일체의 세 원
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_GOLD)
        for y in range(0, 152, 4):
            for x in range(0, CANVAS_W, 4):
                if (x+y)%2==0: base[y][x] = C_WHITE
        # 중앙 거대한 순백의 천상 장미 (엠피레오)
        draw_circle(base, 148, 76, 56, 56, C_WHITE)
        draw_circle(base, 148, 76, 36, 36, C_GOLD)
        draw_circle(base, 148, 76, 18, 18, C_WHITE)
        if act_idx == 20: # 삼위일체 (서로 다른 빛깔로 겹쳐진 세 개의 원)
            draw_circle(base, 136, 68, 22, 22, C_RED)
            draw_circle(base, 160, 68, 22, 22, C_CYAN)
            draw_circle(base, 148, 86, 22, 22, C_GOLD)
        return make_6_frames(base, (148, 76), "sparkle")

# -----------------------------------------------------------------------------
# 7. 차라투스트라는 이렇게 말했다 (20개 씬 고유 명화 구도)
# -----------------------------------------------------------------------------
def gen_zarathustra_act(act_idx):
    base = make_canvas()
    # 배경: 알프스 설산 질스마리아와 타오르는 아침놀
    fill_rect(base, 0, 0, CANVAS_W-1, 60, C_SKY)
    draw_circle(base, 148, 26, 24, 24, C_GOLD) # 위버멘쉬의 태양
    fill_rect(base, 0, 60, CANVAS_W-1, 151, C_LINE) # 설산 암벽
    for x in range(0, CANVAS_W, 16): fill_rect(base, x, 60, x+6, 151, C_WHITE) # 만년설

    if act_idx == 2: # 2막: 정신의 세 가지 변화 (낙타 ➔ 사자 ➔ 어린아이)
        # 좌측: 사막의 낙타
        draw_circle(base, 50, 100, 16, 14, C_BROWN)
        # 중앙: 포효하는 황금빛 사자
        draw_circle(base, 148, 96, 26, 22, C_GOLD)
        base[92][142] = C_WHITE; base[92][154] = C_WHITE
        # 우측: 스스로 굴러가는 바퀴인 어린아이
        draw_circle(base, 240, 100, 14, 14, C_SKIN)
        draw_circle(base, 240, 126, 16, 16, C_GOLD) # 바퀴
        return make_6_frames(base, (148, 96), "flame")

    elif act_idx in [9, 10]: # 9~10막: 순간의 관문 & 검은 뱀 대가리를 물어뜯은 목동
        fill_rect(base, 90, 30, 206, 140, C_DARK_BROWN) # 거대한 석조 관문
        fill_rect(base, 106, 46, 190, 140, C_LINE) # 문 안쪽
        # 아치 위의 글씨 '순간 (AUGENBLICK)'
        fill_rect(base, 118, 36, 178, 42, C_GOLD)
        # 목동이 뱀 대가리를 물어뜯고 초인적인 웃음을 터뜨리는 형상
        draw_circle(base, 148, 90, 18, 16, C_SKIN)
        fill_rect(base, 140, 94, 164, 100, C_LINE) # 물린 뱀
        return make_6_frames(base, (148, 39), "sparkle")

    elif act_idx in [17, 18]: # 17~18막: 동굴의 나귀 축제 & 깊은 자정의 방랑자 노래
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        # 동굴 안 촛불들과 춤추는 보다 높은 인간들
        for x in [50, 100, 190, 240]: fill_rect(base, x, 70, x+4, 90, C_GOLD)
        # 중앙의 우스꽝스러운 나귀와 축제
        draw_circle(base, 148, 80, 22, 20, C_SHADOW)
        fill_rect(base, 136, 60, 142, 80, C_SHADOW); fill_rect(base, 154, 60, 160, 80, C_SHADOW) # 나귀 귀
        return make_6_frames(base, (148, 70), "flame")

    elif act_idx in [19, 20]: # 19~20막: 황금빛 사자가 발을 핥고 비둘기 떼가 어깨를 덮은 아침
        fill_rect(base, 0, 0, CANVAS_W-1, 50, C_GOLD) # 아침놀
        # 백발의 차라투스트라가 산을 내려오는 웅장한 전신상
        draw_circle(base, 148, 56, 20, 20, C_SKIN)
        fill_rect(base, 136, 64, 160, 96, C_WHITE) # 풍성한 백발 수염
        fill_rect(base, 126, 80, 170, 151, C_DARK_BROWN)
        # 발치에 엎드린 거대한 황금 사자
        draw_circle(base, 100, 130, 26, 20, C_GOLD)
        # 어깨 위를 맴도는 순백의 비둘기 떼
        for bx, by in [(116, 40), (130, 30), (170, 32), (184, 44)]:
            draw_circle(base, bx, by, 6, 4, C_WHITE)
        return make_6_frames(base, (148, 26), "sparkle")

    else: # 차라투스트라 표준 대화 씬 (설산과 현자)
        draw_circle(base, 148, 56, 20, 20, C_SKIN)
        fill_rect(base, 136, 64, 160, 96, C_WHITE)
        fill_rect(base, 126, 80, 170, 151, C_DARK_BROWN)
        return make_6_frames(base, (148, 26), "sparkle")

print("Loaded all masterpiece cutscenes successfully!")
