#!/usr/bin/env python3
"""
흥부놀부전 8개 씬의 74x23 고화질 아스키 아트 생성 및 4_game_scene.yaml 자동 패치기
"""

import sys
import os
import math

sys.path.append("/home/krjoylee/code/game/tools/ascii_studio")
from ascii_studio import generate_ascii_art

ART_DIR = "/home/krjoylee/code/game/packs/heungbu_nolbu/art_assets"
os.makedirs(ART_DIR, exist_ok=True)

def create_pgm(filename, draw_func, width=74, height=46):
    path = os.path.join(ART_DIR, filename)
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            val = draw_func(x, y, width, height)
            row.append(str(max(0, min(255, int(val)))))
        pixels.append(" ".join(row))
    with open(path, "w") as f:
        f.write(f"P2\n{width} {height}\n255\n" + "\n".join(pixels) + "\n")
    return path

# 1. 씬 1: 쫓겨나는 흥부 (좌: 놀부의 으리으리한 기와집과 호통 / 우: 쫓겨나는 흥부 가족의 뒷모습)
def draw_scene_1(x, y, w, h):
    # 배경: 찬바람과 황량한 언덕
    val = 240 + int(8 * math.sin(x/4.0) + 4 * math.cos(y/3.0))
    # 좌측: 웅장한 놀부 기와집
    if 4 <= x <= 32:
        # 처마 곡선
        roof_y = 12 + int(0.04 * (x - 18)**2)
        if roof_y - 4 <= y <= roof_y + 2:
            return 30 # 검은 기와 지붕
        elif roof_y + 2 < y <= 38 and 8 <= x <= 28:
            if 14 <= x <= 22 and 22 <= y <= 38:
                return 45 # 굳게 닫힌 붉은 대문
            return 110 # 기와집 돌담
    # 우측: 지팡이 짚고 떠나는 흥부 가족
    if 46 <= x <= 68:
        # 흥부 머리와 상체
        if (x - 56)**2 + (y - 20)**2 < 18:
            return 50
        elif 52 <= x <= 60 and 24 <= y <= 40:
            return 75 # 흥부 누더기 도포
        # 아내와 아이들
        elif 61 <= x <= 68 and 28 <= y <= 42:
            return 95 # 우는 아내와 아이
    return val

# 2. 씬 2: 다친 제비 (처마 밑 둥지와 떨어져 파닥이는 가련한 제비, 손을 뻗는 흥부)
def draw_scene_2(x, y, w, h):
    val = 245
    # 상단: 초가집 처마 (y: 0~8)
    if y <= 8:
        return 50 + int(10 * math.sin(x/2.0))
    # 상단 중앙: 제비 둥지 (x: 30~44, y: 6~14)
    if 30 <= x <= 44 and 6 <= y <= 14:
        return 70
    # 구렁이의 음침한 곡선 (x: 18~32, y: 8~18)
    snake_x = 25 + int(6 * math.sin(y/2.0))
    if abs(x - snake_x) <= 2 and 6 <= y <= 20:
        return 35
    # 중앙 바닥: 떨어진 새끼 제비 (x: 34~42, y: 30~38)
    if (x - 38)**2 + (y - 34)**2 < 16:
        return 40 # 다친 제비
    # 좌하단: 무릎 꿇고 손을 뻗는 흥부 (x: 10~26, y: 22~42)
    if (x - 18)**2 + (y - 26)**2 < 16:
        return 65 # 흥부 얼굴
    elif 12 <= x <= 24 and 30 <= y <= 44:
        return 85 # 흥부 몸통
    return val

# 3. 씬 3: 박씨 (푸른 하늘을 가르며 날아오는 제비와 입에 문 영롱한 박씨)
def draw_scene_3(x, y, w, h):
    # 하늘 구름
    val = 250 - int(5 * math.sin(x/6.0))
    # 중앙: 날개를 활짝 펴고 날아오는 제비 (x: 28~46, y: 12~26)
    # V자형 날개
    wing_left = abs((x - 37) + (y - 18)) < 3 and 26 <= x <= 37 and 10 <= y <= 22
    wing_right = abs((x - 37) - (y - 18)) < 3 and 37 <= x <= 48 and 10 <= y <= 22
    body = (x - 37)**2 + (y - 20)**2 < 12
    if wing_left or wing_right or body:
        return 30
    # 부리에 물린 빛나는 박씨 (x: 37, y: 24~27)
    if (x - 37)**2 + (y - 26)**2 <= 4:
        return 160
    # 하단: 마당의 작은 싹과 초가집 풍경 (y: 38~46)
    if y >= 38:
        return 90 + int(10 * math.cos(x/3.0))
    return val

# 4. 씬 4: 흥부의 박 (거대한 보름달 같은 대박이 갈라지며 쏟아지는 금은보화와 환호하는 부부)
def draw_scene_4(x, y, w, h):
    val = 240
    # 중앙: 거대한 대박 (x: 24~50, y: 8~38)
    dx = (x - 37) / 13.0
    dy = (y - 22) / 14.0
    if dx*dx + dy*dy < 1.0:
        # 박 안에서 터져나오는 눈부신 보화 (중심부)
        if abs(x - 37) < 3:
            return 255 # 갈라진 틈의 눈부신 빛
        elif dx*dx + dy*dy < 0.6:
            return 40 # 쏟아지는 엽전과 보물
        return 90 # 박 껍질
    # 좌측: 톱을 잡고 환호하는 흥부 (x: 8~22, y: 20~42)
    if (x - 15)**2 + (y - 24)**2 < 14 or (10 <= x <= 20 and 28 <= y <= 42):
        return 60
    # 우측: 춤추는 흥부 아내 (x: 52~66, y: 20~42)
    if (x - 59)**2 + (y - 24)**2 < 14 or (54 <= x <= 64 and 28 <= y <= 42):
        return 65
    return val

# 5. 씬 5: 놀부의 욕심 (음흉한 밤, 억지로 제비 다리를 꺾는 심술궂은 놀부의 얼굴)
def draw_scene_5(x, y, w, h):
    # 어두운 밤하늘
    val = 200 + int(15 * math.sin((x+y)/5.0))
    # 중앙 좌측: 탐욕스러운 표정의 거대한 놀부 얼굴과 손 (x: 20~44, y: 10~38)
    if (x - 32)**2 / 120 + (y - 22)**2 / 100 < 1.0:
        if 26 <= x <= 38 and 18 <= y <= 26:
            return 30 # 놀부의 치켜뜬 눈과 심술보
        return 70
    # 손에 쥐여 비명 지르는 제비 (x: 42~54, y: 24~36)
    if (x - 48)**2 + (y - 30)**2 < 15:
        return 40
    return val

# 6. 씬 6: 놀부의 박 (어둠 속에서 터진 박, 도깨비 몽둥이와 혼비백산 달아나는 놀부)
def draw_scene_6(x, y, w, h):
    val = 235
    # 좌측: 거대한 도깨비의 위압적인 형상과 몽둥이 (x: 8~34, y: 6~42)
    if (x - 20)**2 / 90 + (y - 18)**2 / 70 < 1.0:
        return 35 # 도깨비 머리/뿔
    elif 12 <= x <= 28 and 22 <= y <= 42:
        return 45 # 도깨비 몸통
    elif 28 <= x <= 38 and 8 <= y <= 26:
        return 20 # 치켜든 쇠몽둥이
    # 우측: 넘어져 빌고 있는 놀부 (x: 46~66, y: 24~44)
    if (x - 56)**2 + (y - 32)**2 < 20 or (48 <= x <= 64 and 34 <= y <= 44):
        return 80
    return val

# 7. 씬 7: 화해 (따스한 햇살 아래, 무릎 꿇은 형을 안아 일으키는 흥부와 우애의 잔치)
def draw_scene_7(x, y, w, h):
    # 온화한 봄날 햇살 배경
    val = 245 - int(8 * math.cos(x/5.0))
    # 중앙: 서로 부둥켜안은 흥부와 놀부 형제 (x: 26~48, y: 14~40)
    # 두 머리가 맞닿은 포옹
    if (x - 33)**2 + (y - 20)**2 < 14 or (x - 41)**2 + (y - 22)**2 < 14:
        return 40
    elif 28 <= x <= 46 and 25 <= y <= 42:
        return 65 # 맞닿은 도포와 따스한 품
    # 좌측: 풍요로운 초가집 / 우측: 다시 선 기와집
    if (x <= 18 or x >= 56) and y >= 32:
        return 100
    return val

# 8. 씬 8: 빈 마당 (대체 씬: 황량한 빈 뜰, 제비가 오지 않아 쓸쓸히 하늘을 바라보는 흥부)
def draw_scene_8(x, y, w, h):
    # 황량한 안개 낀 하늘
    val = 230 + int(10 * math.sin(y/4.0))
    # 중앙: 휑하니 비어 있는 마당과 마른 나뭇가지 (x: 30~44, y: 10~30)
    if abs(x - 37) < 2 and 12 <= y <= 36:
        return 60 # 앙상한 나무 줄기
    elif 28 <= x <= 46 and abs(y - 20) < 2:
        return 75 # 마른 가지
    # 우하단: 고개 숙이고 한숨 쉬는 흥부의 쓸쓸한 뒷모습 (x: 52~66, y: 26~44)
    if (x - 59)**2 + (y - 32)**2 < 16 or (54 <= x <= 64 and 35 <= y <= 44):
        return 50
    return val

scene_configs = [
    ("act01_scene_01", draw_scene_1, "dual", 1.8, 30),
    ("act02_scene_01", draw_scene_2, "dual", 1.7, 35),
    ("act03_scene_01", draw_scene_3, "center", 1.6, 35),
    ("act04_scene_01", draw_scene_4, "center", 1.9, 25),
    ("act05_scene_01", draw_scene_5, "dual", 1.8, 30),
    ("act06_scene_01", draw_scene_6, "dual", 1.9, 30),
    ("act07_scene_01", draw_scene_7, "center", 1.6, 35),
    ("act03_scene_01_alt", draw_scene_8, "center", 1.5, 40),
]

print("🎨 흥부놀부전 8개 씬 고화질 이미지 생성 및 아스키 아트 변환 중...")

arts_dict = {}
for sid, func, mode, contrast, edge in scene_configs:
    pgm_path = create_pgm(f"{sid}.pgm", func)
    ascii_lines = generate_ascii_art(pgm_path, mode=mode, ramp_type="block", contrast=contrast, edge_thresh=edge)
    arts_dict[sid] = ascii_lines
    print(f"  ✓ [{sid}] 74x23 아스키 아트 변환 완료 ({len(ascii_lines)}줄)")

# 4_game_scene.yaml 업데이트
yaml_path = "/home/krjoylee/code/game/packs/heungbu_nolbu/4_game_scene.yaml"
with open(yaml_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_yaml_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_yaml_lines.append(line)
    
    # scene_id 탐지
    if line.strip().startswith("- scene_id:"):
        cur_id = line.strip().split('"')[1]
        # scene_art 블록 찾기
        while i < len(lines) and not lines[i].strip().startswith("scene_art:"):
            i += 1
            new_yaml_lines.append(lines[i])
        
        # scene_art: 줄 다음부터 기존 art 줄 건너뛰기
        if i < len(lines) and lines[i].strip().startswith("scene_art:"):
            i += 1
            # 기존 줄 스킵 (들여쓰기 6칸 이상 또는 빈 줄)
            while i < len(lines) and (lines[i].startswith("      -") or lines[i].strip() == ""):
                i += 1
            
            # 새로운 23줄 캔버스 삽입
            if cur_id in arts_dict:
                for art_line in arts_dict[cur_id]:
                    escaped = art_line.replace('"', '\\"')
                    new_yaml_lines.append(f'      - "{escaped}"\n')
            
            # 다음 라인으로 진행
            if i < len(lines):
                new_yaml_lines.append(lines[i])
    i += 1

with open(yaml_path, "w", encoding="utf-8") as f:
    f.writelines(new_yaml_lines)

print("✨ 4_game_scene.yaml에 8개 씬 23줄 고화질 아스키 아트 전체 패치 완료!")
