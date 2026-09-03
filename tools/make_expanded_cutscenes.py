#!/usr/bin/env python3
"""
tools/make_expanded_cutscenes.py
신규 및 확장 팩 울트라 픽셀 아트 제너레이터
- 팔레트: PALETTE_16 (16색 인덱스)
- 해상도: 296x152, 6프레임 모션 애니메이션, F3 다이아몬드 스파클
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

def make_6_frames_with_sparkle(base, sparkle_x, sparkle_y, motion_cb=None):
    frames = []
    for i in range(6):
        fr = [row[:] for row in base]
        if motion_cb:
            motion_cb(fr, i)
        if i == 2: # F3 핵심 감정/스파클
            sx = min(CANVAS_W-4, max(4, sparkle_x))
            sy = min(CANVAS_H-4, max(4, sparkle_y))
            fr[sy-3][sx] = C_WHITE
            fill_rect(fr, sx-3, sy, sx+3, sy, C_WHITE)
            fr[sy+3][sx] = C_WHITE
        frames.append(fr)
    return frames

# =============================================================================
# 1. 찰리와 초콜릿 공장 (10개 씬)
# =============================================================================
def gen_charlie_act_scene(act_idx):
    base = make_canvas()
    # 공장 및 실내/초콜릿강 기본 배경
    if act_idx in [3, 4]: # 초콜릿 강, 캔디 정원
        fill_rect(base, 0, 0, CANVAS_W-1, 60, C_LIME)
        fill_rect(base, 0, 60, CANVAS_W-1, 151, C_DARK_BROWN) # 초콜릿 폭포와 강
        for y in range(70, 152, 12):
            for x in range(0, CANVAS_W, 20): fill_rect(base, x, y, x+8, y+2, C_GOLD)
        draw_circle(base, 220, 90, 20, 18, C_RED) # 거대 사탕
    elif act_idx == 10: # 유리 엘리베이터 비행
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_SKY)
        for cx in range(30, 280, 60): draw_circle(base, cx, 130, 30, 14, C_WHITE)
        fill_rect(base, 110, 40, 186, 110, C_CYAN) # 유리벽
        fill_rect(base, 114, 44, 182, 106, C_WHITE)
    else: # 웡카 공장 복도 / 가난한 오두막
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
        for y in range(0, 152, 16):
            for x in range(0, 296, 24):
                if (x+y)%2 == 0: fill_rect(base, x, y, x+12, y+8, C_BROWN)

    # 인물 1: 윌리 웡카 (자줏빛 실크햇, 뾰족한 턱수염, 금지팡이)
    fill_rect(base, 50, 20, 84, 40, C_RED) # 자줏빛 모자
    fill_rect(base, 54, 40, 80, 70, C_SKIN)
    fill_rect(base, 44, 70, 90, 151, C_RED) # 자줏빛 연미복
    fill_rect(base, 92, 60, 96, 151, C_GOLD) # 금손잡이 지팡이

    # 인물 2: 찰리 버킷 (초라한 회색 스웨터에 황금 티켓을 쥔 소년)
    draw_circle(base, 190, 60, 16, 16, C_BROWN)
    fill_rect(base, 178, 60, 202, 90, C_SKIN)
    fill_rect(base, 170, 90, 210, 151, C_CLOTH)
    # 손에 쥔 황금 티켓
    fill_rect(base, 140, 80, 166, 96, C_GOLD)
    fill_rect(base, 142, 82, 164, 94, C_WHITE)

    # 서브 캐릭터: 움파룸파족 (오렌지 피부, 초록 머리)
    if act_idx in [4, 5, 6, 7]:
        fill_rect(base, 110, 110, 130, 146, C_GOLD) # 주황 피부
        draw_circle(base, 120, 104, 8, 8, C_LIME) # 초록 머리
        fill_rect(base, 106, 120, 134, 151, C_WHITE) # 하얀 멜빵

    return make_6_frames_with_sparkle(base, 153, 88)

# =============================================================================
# 2. 마틸다 (10개 씬)
# =============================================================================
def gen_matilda_act_scene(act_idx):
    base = make_canvas()
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_DARK_BROWN)
    # 서재 책장 / 트런치불 교장실
    for y in range(10, 140, 20):
        fill_rect(base, 0, y, CANVAS_W-1, y+2, C_BROWN)
        for x in range(10, CANVAS_W-10, 16):
            c = C_RED if x%3==0 else (C_BLUE if x%3==1 else C_GOLD)
            fill_rect(base, x, y-14, x+12, y, c) # 알록달록 책들

    # 좌측: 악명 높은 트런치불 교장 (거구, 올림픽 투포환 복장, 사나운 눈매)
    draw_circle(base, 66, 44, 24, 22, C_SKIN)
    fill_rect(base, 54, 44, 62, 48, C_LINE); fill_rect(base, 70, 44, 78, 48, C_LINE)
    fill_rect(base, 36, 66, 96, 151, C_LINE) # 거대한 위압적 체구

    # 우측: 천재 소녀 마틸다 (빨간 리본, 책을 펼쳐 든 단정한 소녀)
    draw_circle(base, 210, 60, 16, 16, C_DARK_BROWN)
    fill_rect(base, 204, 46, 216, 52, C_RED) # 빨간 리본!
    fill_rect(base, 198, 60, 222, 90, C_SKIN)
    fill_rect(base, 190, 90, 230, 151, C_BLUE) # 원피스
    # 펼쳐진 하얀 책
    fill_rect(base, 170, 84, 198, 102, C_WHITE)

    # 초능력 씬 (염력의 푸른 파동)
    if act_idx in [7, 8, 9]:
        draw_circle(base, 148, 76, 20, 20, C_CYAN)
        fill_rect(base, 144, 66, 152, 86, C_WHITE) # 허공에 뜬 분필

    return make_6_frames_with_sparkle(base, 210, 49)

# =============================================================================
# 3. 동물농장 (15개 씬)
# =============================================================================
def gen_animal_farm_act_scene(act_idx):
    base = make_canvas()
    # 배경: 매너 농장의 헛간 벽과 풍차
    fill_rect(base, 0, 0, CANVAS_W-1, 60, C_SKY)
    fill_rect(base, 0, 60, CANVAS_W-1, 151, C_BROWN)
    # 헛간 흰 벽에 칠해진 7계명
    fill_rect(base, 20, 16, 120, 56, C_WHITE)
    for y in range(24, 52, 5): fill_rect(base, 26, y, 114, y+1, C_LINE) # 글귀

    # 좌측: 지배자 돼지 나폴레옹 (채찍을 쥐고 두 발로 선 돼지)
    draw_circle(base, 80, 74, 22, 18, C_SKIN) # 돼지 얼굴
    fill_rect(base, 72, 70, 88, 78, C_SHADOW) # 돼지 코구멍
    base[74][76] = C_LINE; base[74][84] = C_LINE
    fill_rect(base, 64, 92, 96, 151, C_LINE) # 인간의 검은 정장!
    # 손에 쥔 가죽 채찍
    fill_rect(base, 102, 96, 126, 100, C_LINE)

    # 우측: 우직한 충직한 일꾼 말 복서 (우람한 갈기와 눈물)
    draw_circle(base, 210, 70, 28, 22, C_BROWN) # 말 머리
    fill_rect(base, 194, 64, 200, 70, C_LINE); base[66][196] = C_WHITE
    fill_rect(base, 170, 92, 250, 151, C_DARK_BROWN) # 등과 앞굽
    # 마차 끄는 무거운 멍에
    fill_rect(base, 180, 88, 240, 94, C_LINE)

    # 풍차 배경 (후반부)
    if act_idx >= 8:
        fill_rect(base, 240, 10, 260, 60, C_STEEL)
        fill_rect(base, 220, 20, 280, 24, C_WHITE) # 날개

    return make_6_frames_with_sparkle(base, 114, 98)

# =============================================================================
# 4. 1984 (15개 씬)
# =============================================================================
def gen_1984_act_scene(act_idx):
    base = make_canvas()
    # 배경: 런던 잿빛 오세아니아 거리 & 텔레스크린
    fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
    # 거대한 텔레스크린 (BIG BROTHER IS WATCHING YOU)
    fill_rect(base, 90, 10, 206, 68, C_STEEL)
    draw_circle(base, 148, 38, 24, 20, C_SKIN) # 빅브라더의 거대한 얼굴
    fill_rect(base, 136, 42, 160, 48, C_LINE) # 짙은 콧수염
    fill_rect(base, 134, 30, 144, 34, C_WHITE); fill_rect(base, 152, 30, 162, 34, C_WHITE)
    base[32][139] = C_LINE; base[32][157] = C_LINE # 꿰뚫어 보는 눈빛

    # 좌측: 윈스턴 스미스 (파란 당복 작업복, 일기장과 펜을 쥔 수척한 남자)
    fill_rect(base, 40, 70, 72, 100, C_SKIN)
    fill_rect(base, 34, 100, 80, 151, C_BLUE) # 당복
    fill_rect(base, 60, 110, 84, 130, C_WHITE) # 금지된 하얀 일기장

    # 우측: 줄리아 (붉은 반성동맹 띠) 또는 오브라이언
    fill_rect(base, 220, 70, 252, 100, C_SKIN)
    fill_rect(base, 214, 100, 260, 151, C_BLUE)
    fill_rect(base, 214, 114, 260, 120, C_RED) # 붉은 사시(띠)

    # 101호 고문실 (후반부)
    if act_idx >= 12:
        fill_rect(base, 120, 80, 176, 140, C_STEEL) # 쥐가 든 철창 마스크!
        base[100][148] = C_RED

    return make_6_frames_with_sparkle(base, 148, 32)

# =============================================================================
# 5. 수레바퀴 아래서 (15개 씬)
# =============================================================================
def gen_under_wheel_act_scene(act_idx):
    base = make_canvas()
    # 배경: 흑림의 자연과 신학교 마울브론 수도원의 고딕 석조
    fill_rect(base, 0, 0, CANVAS_W-1, 70, C_SKY)
    fill_rect(base, 0, 70, CANVAS_W-1, 151, C_LIME)
    # 네카어 강물
    fill_rect(base, 0, 110, CANVAS_W-1, 151, C_BLUE)
    for y in range(120, 152, 8):
        for x in range(0, CANVAS_W, 24): fill_rect(base, x, y, x+10, y+1, C_CYAN)

    # 좌측: 한스 기벤라트 (수척하고 창백한 우등생 소년, 두통과 고뇌)
    draw_circle(base, 80, 50, 18, 18, C_BROWN)
    fill_rect(base, 66, 50, 94, 84, C_SKIN)
    fill_rect(base, 68, 58, 76, 62, C_LINE); fill_rect(base, 84, 58, 92, 62, C_LINE)
    fill_rect(base, 56, 84, 104, 146, C_CLOTH) # 신학생 복장
    # 낚싯대 (유년의 평화)
    fill_rect(base, 98, 40, 102, 130, C_BROWN)

    # 우측: 자유로운 시인 친구 헤르만 하일러 (자유분방한 갈색 머리칼)
    draw_circle(base, 210, 48, 22, 20, C_DARK_BROWN)
    fill_rect(base, 196, 48, 224, 82, C_SKIN)
    fill_rect(base, 186, 82, 234, 146, C_BLUE)

    return make_6_frames_with_sparkle(base, 80, 60)

# =============================================================================
# 6. 단테의 신곡: 연옥 & 천국편 (20개 씬 통합)
# =============================================================================
def gen_dante_comedy_act_scene(act_idx):
    base = make_canvas()
    if act_idx <= 7: # 지옥편
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_LINE)
        fill_rect(base, 0, 80, CANVAS_W-1, 151, C_RED) # 화염과 핏빛 강
    elif act_idx <= 14: # 연옥편 (새벽빛과 연옥산)
        fill_rect(base, 0, 0, CANVAS_W-1, 80, C_SKY)
        fill_rect(base, 0, 80, CANVAS_W-1, 151, C_GREEN)
        # 연옥산의 거대한 7층 테라스
        for i, y in enumerate(range(30, 110, 12)):
            w = 80 + i * 24
            fill_rect(base, 148 - w//2, y, 148 + w//2, y+10, C_BROWN)
    else: # 천국편 (눈부신 황금빛 엠피레오, 천상의 장미)
        fill_rect(base, 0, 0, CANVAS_W-1, 151, C_GOLD)
        for y in range(0, 152):
            for x in range(0, CANVAS_W):
                if (x+y)%3 == 0: base[y][x] = C_WHITE
        draw_circle(base, 148, 76, 50, 50, C_WHITE) # 천상의 순백 장미

    # 좌측: 단테 (진홍색 학자 두건과 로브)
    fill_rect(base, 40, 50, 70, 86, C_RED)
    fill_rect(base, 46, 60, 66, 92, C_SKIN)
    fill_rect(base, 30, 86, 80, 151, C_RED)

    # 우측: 스승 베르길리우스(지옥/연옥) 또는 천상의 성녀 베아트리체(천국)
    if act_idx <= 13: # 베르길리우스
        fill_rect(base, 220, 44, 250, 80, C_WHITE)
        draw_circle(base, 235, 42, 10, 4, C_LIME) # 월계관
        fill_rect(base, 210, 80, 260, 151, C_WHITE)
    else: # 베아트리체 (순백 베일과 에메랄드 눈동자, 성스러운 황금 후광)
        draw_circle(base, 235, 50, 20, 20, C_WHITE) # 후광
        fill_rect(base, 222, 46, 248, 80, C_SKIN)
        base[56][228] = C_CYAN; base[56][242] = C_CYAN # 에메랄드 눈
        fill_rect(base, 210, 80, 260, 151, C_WHITE)

    return make_6_frames_with_sparkle(base, 235, 42)

# =============================================================================
# 7. 니체: 차라투스트라는 이렇게 말했다 (20개 씬)
# =============================================================================
def gen_zarathustra_act_scene(act_idx):
    base = make_canvas()
    # 배경: 알프스 질스마리아 설산 봉우리와 타오르는 아침 태양
    fill_rect(base, 0, 0, CANVAS_W-1, 70, C_SKY)
    draw_circle(base, 148, 30, 26, 26, C_GOLD) # 위버멘쉬의 태양
    # 웅장한 설산 암벽
    fill_rect(base, 0, 70, CANVAS_W-1, 151, C_LINE)
    for x in range(0, CANVAS_W, 20): fill_rect(base, x, 70, x+8, 151, C_WHITE)

    # 중앙: 산에서 내려오는 현자 차라투스트라 (풍성한 백발과 수염, 굳건한 눈빛)
    fill_rect(base, 132, 40, 164, 82, C_SKIN)
    for y in range(60, 104): fill_rect(base, 126, y, 170, y, C_WHITE) # 사자의 갈기 같은 수염
    fill_rect(base, 136, 48, 144, 52, C_LINE); fill_rect(base, 152, 48, 160, 52, C_LINE)
    base[50][140] = C_GOLD; base[50][156] = C_GOLD # 번뜩이는 불꽃 눈!
    fill_rect(base, 118, 84, 178, 151, C_DARK_BROWN) # 은둔자의 로브

    # 좌측 동물: 현명한 뱀 (팔을 감음)
    draw_circle(base, 104, 96, 12, 12, C_GREEN)
    # 우측 동물: 긍지 높은 독수리 (창공 선회)
    fill_rect(base, 210, 36, 250, 42, C_GOLD) # 날개
    fill_rect(base, 226, 30, 234, 38, C_WHITE) # 머리

    # 3대 변화: 낙타 ➔ 사자 ➔ 어린아이 (1~3막)
    if act_idx == 2: # 사자
        draw_circle(base, 60, 110, 20, 20, C_GOLD)
    elif act_idx == 3: # 어린아이
        draw_circle(base, 60, 110, 12, 12, C_SKIN)

    return make_6_frames_with_sparkle(base, 148, 30)

print("Loaded all expanded cutscene generators successfully!")
