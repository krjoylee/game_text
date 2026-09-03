#!/usr/bin/env python3
"""
흥부놀부전 제1막(형제의 갈림길)을 위한 6프레임 시네마틱 애니메이션 컷씬 생성기
동작 흐름:
Frame 1: 굳게 닫힌 놀부 기와집 대문
Frame 2: 놀부가 대문을 쾅 열고 나타남
Frame 3: 놀부가 삿대질하며 호통침 (치켜뜬 눈 & 턱수염 부르르)
Frame 4: 흥부가 깜짝 놀라 고개 숙이며 물러섬 (눈물 글썽)
Frame 5: 놀부가 문을 쾅 닫음
Frame 6: 찬바람 속에 흥부 가족이 눈물 흘리며 길을 떠남 (최종 프레임)
"""

import sys
import os

sys.path.append("/home/krjoylee/code/game/tools/ascii_studio")
from ascii_studio import generate_braille_art

WIDTH = 148
HEIGHT = 92

def save_pgm(path, draw_func):
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
# 6개 프레임 드로잉 로직
# ─────────────────────────────────────────────────────────────

# F1: 닫힌 대문
def f1(x, y, w, h):
    val = 255
    if 25 <= x <= 123 and 15 <= y <= 85:
        if y <= 30: val = 30 # 기와
        elif 60 <= x <= 88: val = 10 # 굳게 닫힌 대문
        else: val = 180
    return val

# F2: 놀부가 대문을 열고 등장
def f2(x, y, w, h):
    val = 255
    # 문 열림
    if 25 <= x <= 123 and 15 <= y <= 85:
        if y <= 30: val = 30
        elif (35 <= x <= 55) or (95 <= x <= 115): val = 40 # 열린 문짝
        # 중앙에 등장하는 놀부 실루엣
        elif 60 <= x <= 88 and 35 <= y <= 85:
            val = 20
    return val

# F3: 놀부가 삿대질하며 호통 (치켜뜬 눈 & 갓)
def f3(x, y, w, h):
    val = 255
    # 좌측에 가득 찬 성난 놀부 얼굴
    # 갓
    if 40 <= x <= 108 and 10 <= y <= 25: val = 20
    if 20 <= x <= 128 and abs(y - 25) <= 2: val = 0
    # 얼굴
    dx = (x - 74) / 22.0
    dy = (y - 50) / 22.0
    if dx*dx + dy*dy < 1.0:
        val = 200
        # 부릅뜬 세모 눈
        if (abs(x - 62) < 5 or abs(x - 86) < 5) and abs(y - 42) < 4: val = 0
        # 삿대질 손
        if 95 <= x <= 135 and 45 <= y <= 60: val = 0
        # 턱수염
        if 65 <= x <= 83 and 65 <= y <= 78: val = 0
    return val

# F4: 흥부가 깜짝 놀라며 고개 숙임 (눈물 줄기)
def f4(x, y, w, h):
    val = 255
    # 좌: 놀부의 호통 / 우: 흥부의 눈물
    # 놀부 (좌)
    if 15 <= x <= 65 and 20 <= y <= 80: val = 40
    # 흥부 (우) - 고개 숙인 얼굴과 눈물
    dx = (x - 110) / 16.0
    dy = (y - 52) / 18.0
    if dx*dx + dy*dy < 1.0:
        val = 220
        if (abs(x - 104) < 3 or abs(x - 118) < 3) and abs(y - 48) < 3: val = 0
        if (x == 105 or x == 119) and 50 <= y <= 65: val = 0 # 뚝뚝 떨어지는 눈물
    return val

# F5: 문이 쾅 닫힘
def f5(x, y, w, h):
    val = 255
    if 25 <= x <= 123 and 15 <= y <= 85:
        if y <= 30: val = 30
        elif 55 <= x <= 93 and 30 <= y <= 85: val = 0 # 쾅 닫힌 검은 문
        else: val = 120
    # 먼지 일어남
    if (abs(x - 74) < 35) and (75 <= y <= 85): val = 200
    return val

# F6: 찬바람 속 흥부 가족이 길을 떠남 (최종 정지 컷)
def f6(x, y, w, h):
    val = 255
    # 좌측 놀부 기와집
    if 15 <= x <= 55 and 20 <= y <= 80:
        if y <= 32: val = 30
        elif 25 <= x <= 45 and 35 <= y <= 80: val = 50
    # 우측 흥부 가족의 뒷모습과 지팡이
    dx = (x - 105) / 16.0
    dy = (y - 50) / 20.0
    if dx*dx + dy*dy < 1.0:
        val = 60
        # 지팡이
        if abs(x - 122) <= 1 and 35 <= y <= 85: val = 0
    # 아내와 아이 실루엣
    if 124 <= x <= 142 and 55 <= y <= 85: val = 80
    return val

frames_drawings = [f1, f2, f3, f4, f5, f6]

print("🎬 제1막 6프레임 시네마틱 애니메이션 렌더링 중...")
frames_lines = []

for idx, func in enumerate(frames_drawings, 1):
    tmp_path = f"/tmp/heungbu_f{idx}.pgm"
    save_pgm(tmp_path, func)
    with open(tmp_path, "rb") as f:
        # PGM 파싱 및 Braille 변환
        lines_raw = f.read().decode("latin1").split("\n")
        # decode pixels
        toks = " ".join(lines_raw[3:]).split()
        pxs = []
        c = 0
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                row.append(int(toks[c]))
                c += 1
            pxs.append(row)
        lines = generate_braille_art(pxs, WIDTH, HEIGHT, threshold=130)
        frames_lines.append(lines)
        print(f"  ✓ Frame {idx}/6 렌더링 완료 ({len(lines)}줄)")

# YAML 씬 1에 애니메이션 블록 주입
yaml_path = "/home/krjoylee/code/game/packs/heungbu_nolbu/4_game_scene.yaml"
with open(yaml_path, "r", encoding="utf-8") as f:
    content = f.read()

# scene_id: "act01_scene_01" 밑에 animation 블록 작성
anim_yaml = """    animation:
      frame_rate_ms: 350
      loop: false
      frames:
"""

for f_idx, fl in enumerate(frames_lines, 1):
    anim_yaml += f"        # Frame {f_idx}\n        - [\n"
    for l in fl:
        escaped = l.replace('"', '\\"')
        anim_yaml += f'            "{escaped}",\n'
    anim_yaml += "          ]\n"

# 삽입
target_needle = '  - scene_id: "act01_scene_01"\n    act: 1\n    act_name: "형제의 갈림길"\n    title: "쫓겨나는 흥부"\n    theme: "탐욕과 형제의 정"\n    message: "부당한 상황 앞에서 어떤 태도를 취할 것인가"\n    is_interpreted: false\n'

if target_needle in content:
    content = content.replace(target_needle, target_needle + "\n" + anim_yaml + "\n")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✨ 4_game_scene.yaml에 제1막 6프레임 시네마틱 애니메이션 주입 완료!")
else:
    print("⚠️ target needle not matched, writing custom patch")
