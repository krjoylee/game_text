#!/usr/bin/env python3
"""
흥부놀부전 8개 씬의 인물 흉상 및 핵심 상징을 8배 초고해상도 Braille 도트(148x92)로 렌더링하여
4_game_scene.yaml에 전면 교체 적용하는 스크립트
"""

import sys
import os
import math

sys.path.append("/home/krjoylee/code/game/tools/ascii_studio")
from ascii_studio import generate_ascii_art

ART_DIR = "/home/krjoylee/code/game/packs/heungbu_nolbu/art_assets"
os.makedirs(ART_DIR, exist_ok=True)

WIDTH = 148
HEIGHT = 92

def save_pgm(filename, draw_func):
    path = os.path.join(ART_DIR, filename)
    pixels = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            val = draw_func(x, y, WIDTH, HEIGHT)
            row.append(str(max(0, min(255, int(val)))))
        pixels.append(" ".join(row))
    with open(path, "w") as f:
        f.write(f"P2\n{WIDTH} {HEIGHT}\n255\n" + "\n".join(pixels) + "\n")
    return path

# ─────────────────────────────────────────────────────────────
# 1. 씬 1: 형제의 갈림길 (좌: 갓 쓴 호통치는 놀부 흉상 / 우: 패랭이 쓰고 눈물 흘리는 흥부 흉상)
# ─────────────────────────────────────────────────────────────
def draw_scene_1(x, y, w, h):
    val = 255
    # [좌측: 놀부 흉상]
    # 갓 모자 & 챙
    if 20 <= x <= 55 and 15 <= y <= 28: val = 20
    if 8 <= x <= 67 and abs(y - 28) <= 2: val = 10
    # 얼굴 & 눈/코/입/수염
    dx = (x - 37) / 13.0
    dy = (y - 48) / 16.0
    if dx*dx + dy*dy < 1.0:
        val = 200
        if (abs(x - 30) < 3 or abs(x - 44) < 3) and abs(y - 42) < 3: val = 0 # 치켜뜬 눈
        if 35 <= x <= 39 and 46 <= y <= 56: val = 20 # 코/입
        if 30 <= x <= 44 and 58 <= y <= 66: val = 0  # 턱수염
    # 비단 도포
    if 12 <= x <= 63 and 65 <= y <= 90: val = 30

    # [우측: 흥부 흉상]
    # 찢어진 패랭이
    if 92 <= x <= 128 and 20 <= y <= 32: val = 80
    if 80 <= x <= 140 and abs(y - 32) <= 2: val = 30
    # 얼굴 & 처진 눈/눈물
    dx2 = (x - 110) / 13.0
    dy2 = (y - 50) / 15.0
    if dx2*dx2 + dy2*dy2 < 1.0:
        val = 220
        if (abs(x - 103) < 3 or abs(x - 117) < 3) and abs(y - 45) < 3: val = 0 # 처진 눈
        if (x == 104 or x == 118) and 48 <= y <= 58: val = 0 # 눈물 자국
        if 106 <= x <= 114 and abs(y - 60) <= 1: val = 20
    # 누더기 옷
    if 85 <= x <= 135 and 68 <= y <= 90: val = 40
    return val

# ─────────────────────────────────────────────────────────────
# 2. 씬 2: 다친 제비 (좌: 떨어진 새끼 제비 클로즈업 / 우: 정성껏 감싸 쥔 흥부의 따스한 손)
# ─────────────────────────────────────────────────────────────
def draw_scene_2(x, y, w, h):
    val = 255
    # 좌측: 새끼 제비의 날개와 떨어진 다리 (x: 20~65, y: 25~75)
    dx = (x - 42) / 18.0
    dy = (y - 48) / 18.0
    if dx*dx + dy*dy < 1.0:
        val = 40 # 제비 깃털
        if (x - 36)**2 + (y - 42)**2 < 6: val = 255 # 반짝이는 눈
    # 벌어진 부리
    if 24 <= x <= 32 and abs(y - 45) <= 3: val = 10
    # 꺾인 다리
    if 45 <= x <= 58 and 62 <= y <= 76: val = 0

    # 우측: 흥부의 자애로운 손과 실 감는 손길 (x: 80~135, y: 30~80)
    dx2 = (x - 105) / 22.0
    dy2 = (y - 55) / 20.0
    if dx2*dx2 + dy2*dy2 < 1.0:
        val = 60
        if 92 <= x <= 118 and abs(y - 55) <= 2: val = 0 # 치료하는 붉은 실
    return val

# ─────────────────────────────────────────────────────────────
# 3. 씬 3: 박씨 (중앙: 활짝 날개 편 보은의 제비와 빛나는 박씨 클로즈업)
# ─────────────────────────────────────────────────────────────
def draw_scene_3(x, y, w, h):
    val = 255
    # 날아오는 제비의 웅장한 날개 (x: 25~123, y: 15~55)
    # V자 날개선
    wl = abs((x - 74) + (y - 35)) < 6 and 25 <= x <= 74 and 15 <= y <= 45
    wr = abs((x - 74) - (y - 35)) < 6 and 74 <= x <= 123 and 15 <= y <= 45
    body = (x - 74)**2 / 100 + (y - 42)**2 / 180 < 1.0
    if wl or wr or body: val = 20
    # 제비 눈
    if (x - 74)**2 + (y - 34)**2 < 4: val = 255
    # 부리에 물린 영롱한 황금 박씨 (x: 74, y: 55~70)
    dx = (x - 74) / 8.0
    dy = (y - 62) / 10.0
    if dx*dx + dy*dy < 1.0:
        val = 10 # 빛나는 씨앗
    return val

# ─────────────────────────────────────────────────────────────
# 4. 씬 4: 흥부의 박 (중앙: 쩍 갈라진 거대한 대박과 쏟아지는 엽전/비단 더미)
# ─────────────────────────────────────────────────────────────
def draw_scene_4(x, y, w, h):
    val = 255
    # 거대한 박의 윤곽선 (x: 35~113, y: 10~80)
    dx = (x - 74) / 38.0
    dy = (y - 45) / 34.0
    if dx*dx + dy*dy < 1.0:
        # 갈라진 중심 틈 (보화 쏟아짐)
        if abs(x - 74) < 12 and 15 <= y <= 75:
            # 엽전 동그라미들
            if (x % 6 < 3) and (y % 6 < 3): val = 0
            else: val = 120
        else:
            val = 40 # 든든한 박 껍질
    return val

# ─────────────────────────────────────────────────────────────
# 5. 씬 5: 놀부의 욕심 (중앙: 제비 다리를 움켜쥔 놀부의 거대한 손과 탐욕의 눈빛)
# ─────────────────────────────────────────────────────────────
def draw_scene_5(x, y, w, h):
    val = 255
    # 거대한 놀부의 치켜뜬 두 눈 (x: 40~108, y: 15~38)
    if ((x - 54)**2 + (y - 25)**2 < 36) or ((x - 94)**2 + (y - 25)**2 < 36):
        val = 0 # 무서운 눈동자
    # 억지로 부러뜨리는 거친 손아귀 (x: 45~103, y: 45~85)
    dx = (x - 74) / 25.0
    dy = (y - 65) / 18.0
    if dx*dx + dy*dy < 1.0:
        val = 30
        # 비명 지르는 제비
        if (x - 74)**2 + (y - 65)**2 < 30: val = 180
    return val

# ─────────────────────────────────────────────────────────────
# 6. 씬 6: 놀부의 박 (좌: 쇠몽둥이 든 무시무시한 도깨비 흉상 / 우: 납작 엎드린 놀부)
# ─────────────────────────────────────────────────────────────
def draw_scene_6(x, y, w, h):
    val = 255
    # [좌측: 도깨비 흉상]
    # 뿔과 머리
    if (25 <= x <= 33 or 45 <= x <= 53) and 10 <= y <= 22: val = 0 # 뿔
    dx = (x - 39) / 18.0
    dy = (y - 38) / 18.0
    if dx*dx + dy*dy < 1.0:
        val = 40
        # 왕방울 눈과 뻐드렁니
        if (abs(x - 32) < 4 or abs(x - 46) < 4) and abs(y - 32) < 4: val = 255
        if 34 <= x <= 44 and 44 <= y <= 50: val = 0
    # 치켜든 가시 쇠몽둥이 (x: 55~68, y: 15~65)
    if 56 <= x <= 64 and 15 <= y <= 65: val = 0

    # [우측: 빌고 있는 놀부]
    dx2 = (x - 110) / 22.0
    dy2 = (y - 60) / 16.0
    if dx2*dx2 + dy2*dy2 < 1.0: val = 50
    return val

# ─────────────────────────────────────────────────────────────
# 7. 씬 7: 화해 (중앙: 눈물로 부둥켜안은 흥부와 놀부의 뜨거운 포옹 흉상)
# ─────────────────────────────────────────────────────────────
def draw_scene_7(x, y, w, h):
    val = 255
    # 흥부 머리 (좌) & 놀부 머리 (우) 맞닿은 포옹
    dx1 = (x - 62) / 14.0
    dy1 = (y - 35) / 15.0
    dx2 = (x - 86) / 14.0
    dy2 = (y - 35) / 15.0
    if (dx1*dx1 + dy1*dy1 < 1.0) or (dx2*dx2 + dy2*dy2 < 1.0):
        val = 40 # 머리와 갓
    # 감싸 안은 두 형제의 몸통과 눈물 (x: 48~100, y: 45~85)
    dx = (x - 74) / 26.0
    dy = (y - 65) / 20.0
    if dx*dx + dy*dy < 1.0:
        val = 30
        if abs(x - 74) < 3: val = 255 # 따스한 빛줄기
    return val

# ─────────────────────────────────────────────────────────────
# 8. 씬 8: 빈 마당 (중앙: 앙상한 마른 가지와 고개 숙인 흥부의 쓸쓸한 흉상)
# ─────────────────────────────────────────────────────────────
def draw_scene_8(x, y, w, h):
    val = 255
    # 앙상한 마른 나뭇가지
    if abs(x - 74) < 3 and 10 <= y <= 70: val = 30
    if (50 <= x <= 74 and abs(y - 30) < 2) or (74 <= x <= 98 and abs(y - 45) < 2): val = 30
    # 고개 숙인 흥부 (우하단)
    dx = (x - 110) / 16.0
    dy = (y - 62) / 16.0
    if dx*dx + dy*dy < 1.0: val = 50
    return val

scene_drawings = [
    ("act01_scene_01", draw_scene_1),
    ("act02_scene_01", draw_scene_2),
    ("act03_scene_01", draw_scene_3),
    ("act04_scene_01", draw_scene_4),
    ("act05_scene_01", draw_scene_5),
    ("act06_scene_01", draw_scene_6),
    ("act07_scene_01", draw_scene_7),
    ("act03_scene_01_alt", draw_scene_8),
]

print("🎨 [AsciiArt Studio] 8배 초고해상도 Braille 도트 씬 생성 시작...")

arts_dict = {}
for sid, func in scene_drawings:
    pgm_path = save_pgm(f"{sid}_braille.pgm", func)
    braille_lines = generate_ascii_art(pgm_path, format_type="braille", threshold=130)
    arts_dict[sid] = braille_lines
    print(f"  ✓ [{sid}] 148x92 ➔ 74x23 Braille 도트 변환 완료 ({len(braille_lines)}줄)")

# 4_game_scene.yaml 패치
yaml_path = "/home/krjoylee/code/game/packs/heungbu_nolbu/4_game_scene.yaml"
with open(yaml_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_yaml_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_yaml_lines.append(line)
    
    if line.strip().startswith("- scene_id:"):
        cur_id = line.strip().split('"')[1]
        while i < len(lines) and not lines[i].strip().startswith("scene_art:"):
            i += 1
            new_yaml_lines.append(lines[i])
        
        if i < len(lines) and lines[i].strip().startswith("scene_art:"):
            i += 1
            while i < len(lines) and (lines[i].startswith("      -") or lines[i].strip() == ""):
                i += 1
            
            if cur_id in arts_dict:
                for art_line in arts_dict[cur_id]:
                    escaped = art_line.replace('"', '\\"')
                    new_yaml_lines.append(f'      - "{escaped}"\n')
            
            if i < len(lines):
                new_yaml_lines.append(lines[i])
    i += 1

with open(yaml_path, "w", encoding="utf-8") as f:
    f.writelines(new_yaml_lines)

print("✨ 4_game_scene.yaml에 8개 씬 8배 초고해상도 Braille 도트 전체 패치 완료!")
