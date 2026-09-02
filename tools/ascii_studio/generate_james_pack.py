#!/usr/bin/env python3
"""
제임스와 슈퍼 복숭아 팩 (3_scene.yaml, 4_game_scene.yaml) 생성기
- 8개 씬 74x23 Braille 8배 초고해상도 도트 아트
- 제1막 6프레임 시네마틱 애니메이션 컷씬 (고모들의 호통 -> 노인의 마법 콩 -> 복숭아 싹)
"""

import os
import sys

sys.path.append("/home/krjoylee/code/game/tools/ascii_studio")
from ascii_studio import generate_braille_art

WIDTH = 148
HEIGHT = 92
OUT_DIR = "/home/krjoylee/code/game/packs/james_peach"

def draw_to_braille(draw_func, threshold=130):
    pixels = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            val = draw_func(x, y, WIDTH, HEIGHT)
            row.append(max(0, min(255, int(val))))
        pixels.append(row)
    return generate_braille_art(pixels, WIDTH, HEIGHT, threshold=threshold)

# ─────────────────────────────────────────────────────────────
# 8개 씬 드로잉 로직
# ─────────────────────────────────────────────────────────────

# 1. 씬 1: 절벽 위의 외톨이 (좌: 스파이커/스펀지 고모 / 우: 슬픈 제임스와 노인의 마법 콩)
def draw_scene_1(x, y, w, h):
    val = 255
    # 좌: 스파이커(마른 체형) & 스펀지(뚱뚱한 체형) 고모
    # 스파이커 (x: 15~35, y: 15~80)
    if 22 <= x <= 28 and 18 <= y <= 35: val = 30 # 긴 코와 마른 얼굴
    if 18 <= x <= 32 and 35 <= y <= 85: val = 50
    # 스펀지 (x: 35~65, y: 25~85)
    dx = (x - 50) / 14.0
    dy = (y - 55) / 25.0
    if dx*dx + dy*dy < 1.0: val = 40 # 뚱뚱한 몸집
    if (x - 50)**2 + (y - 28)**2 < 45: val = 20 # 둥근 얼굴
    
    # 우: 제임스와 무릎 꿇은 흰 수염 노인 (x: 80~135, y: 20~85)
    # 제임스 (작은 소년, x: 80~105, y: 35~80)
    if (x - 92)**2 + (y - 42)**2 < 25: val = 200 # 얼굴
    if 84 <= x <= 100 and 50 <= y <= 85: val = 80 # 옷
    # 노인과 마법 종이봉투 (x: 105~135, y: 30~85)
    if (x - 120)**2 + (y - 40)**2 < 30: val = 30 # 노인 머리
    if 115 <= x <= 125 and 45 <= y <= 62: val = 255 # 흰 수염
    # 반짝이는 초록 콩 종이봉투 (x: 102~112, y: 55~68)
    if 102 <= x <= 112 and 55 <= y <= 68: val = 0 # 빛나는 봉투
    return val

# 2. 씬 2: 거대한 기적 (중앙: 집채보다 커진 황금빛 슈퍼 복숭아와 열린 터널)
def draw_scene_2(x, y, w, h):
    val = 255
    # 중앙 거대한 복숭아 외곽 (x: 25~123, y: 8~85)
    dx = (x - 74) / 46.0
    dy = (y - 48) / 36.0
    if dx*dx + dy*dy < 1.0:
        val = 40 # 든든하고 탐스러운 복숭아 과육
        # 꼭지 잎사귀 (상단)
        if 65 <= x <= 83 and 5 <= y <= 15: val = 10
        # 과육 표면에 뚫린 터널 입구 (x: 64~84, y: 52~72)
        dx_t = (x - 74) / 10.0
        dy_t = (y - 62) / 10.0
        if dx_t*dx_t + dy_t*dy_t < 1.0:
            val = 255 # 신비한 빛이 새어 나오는 터널 입구
    # 좌하단: 깜짝 놀라 다가가는 제임스 실루엣 (x: 10~25, y: 55~85)
    if (x - 18)**2 + (y - 62)**2 < 20 or (12 <= x <= 24 and 68 <= y <= 85): val = 30
    return val

# 3. 씬 3: 복숭아 속의 친구들 (좌: 제임스 / 우: 늙은 메뚜기와 지네, 무당벌레)
def draw_scene_3(x, y, w, h):
    val = 255
    # 좌측: 깜짝 놀란 제임스 (x: 15~40, y: 30~80)
    if (x - 28)**2 + (y - 42)**2 < 30: val = 60
    if 20 <= x <= 36 and 50 <= y <= 85: val = 90
    # 우측: 늙은 메뚜기(더듬이와 연주복) & 지네(수많은 부츠)
    # 메뚜기 (x: 55~85, y: 20~80)
    if abs(x - 70) <= 2 and 15 <= y <= 35: val = 0 # 더듬이
    if (x - 70)**2 + (y - 45)**2 < 40: val = 30 # 메뚜기 상체
    # 지네 (x: 90~135, y: 30~85)
    dx = (x - 110) / 20.0
    dy = (y - 55) / 22.0
    if dx*dx + dy*dy < 1.0: val = 40
    # 부츠 행렬 (하단)
    if 90 <= x <= 135 and 75 <= y <= 85:
        if x % 6 < 3: val = 0
    return val

# 4. 씬 4: 상어와 갈매기 비행 (상: 500마리 갈매기 밧줄 / 중: 비행하는 복숭아 / 하: 파도와 상어 지느러미)
def draw_scene_4(x, y, w, h):
    val = 255
    # 상단: 갈매기 떼 (x: 20~128, y: 5~28)
    if y <= 25:
        if (x % 14 < 6) and (abs(y - 15) < 6): val = 10 # V자 갈매기들
    # 밧줄 줄기선 (y: 25~42)
    if 28 <= y <= 42 and (x % 10 == 0): val = 60
    # 중앙: 떠오른 복숭아 (x: 45~103, y: 40~75)
    dx = (x - 74) / 28.0
    dy = (y - 58) / 18.0
    if dx*dx + dy*dy < 1.0: val = 35
    # 하단: 바다 파도와 상어 지느러미 (y: 78~90)
    if y >= 80: val = 120
    # 삼각 상어 지느러미 (x: 25~35, x: 110~120)
    if (25 <= x <= 35 or 115 <= x <= 125) and 74 <= y <= 85: val = 0
    return val

# 5. 씬 5: 구름 사람들과의 충돌 (좌: 화난 구름 거인 / 우: 우박을 피하는 복숭아)
def draw_scene_5(x, y, w, h):
    val = 255
    # 좌측: 거대한 먹구름 거인 얼굴과 주먹 (x: 10~60, y: 10~75)
    dx = (x - 35) / 22.0
    dy = (y - 40) / 26.0
    if dx*dx + dy*dy < 1.0:
        val = 30 # 먹구름 몸체
        if (abs(x - 28) < 4 or abs(x - 42) < 4) and abs(y - 35) < 4: val = 255 # 번뜩이는 눈
    # 쏟아지는 우박 점들 (x: 60~95, y: 15~80)
    if 60 <= x <= 95 and (x % 8 < 3) and (y % 8 < 3): val = 0 # 단단한 우박
    # 우측: 비행 복숭아 (x: 95~138, y: 35~75)
    dx2 = (x - 116) / 20.0
    dy2 = (y - 55) / 18.0
    if dx2*dx2 + dy2*dy2 < 1.0: val = 50
    return val

# 6. 씬 6: 엠파이어 스테이트 빌딩 (중앙: 엠파이어 빌딩 첨탑에 꽂힌 복숭아와 맨해튼 빌딩 숲)
def draw_scene_6(x, y, w, h):
    val = 255
    # 상단: 뾰족탑에 꽂힌 슈퍼 복숭아 (x: 50~98, y: 10~45)
    dx = (x - 74) / 24.0
    dy = (y - 28) / 16.0
    if dx*dx + dy*dy < 1.0: val = 40
    # 중앙 엠파이어 스테이트 빌딩 첨탑 기둥 (x: 70~78, y: 30~60)
    if 71 <= x <= 77 and 25 <= y <= 60: val = 0
    # 하단: 뉴욕 마천루 빌딩 실루엣 (y: 60~90)
    if y >= 60:
        if (15 <= x <= 35) or (45 <= x <= 65) or (83 <= x <= 105) or (115 <= x <= 135):
            val = 30 # 고층 빌딩들
            if y % 6 < 3 and x % 4 < 2: val = 255 # 창문 불빛
    return val

# 7. 씬 7: 센트럴 파크의 축제 (중앙: 복숭아 씨앗 집과 환호하는 제임스 & 뉴욕 아이들)
def draw_scene_7(x, y, w, h):
    val = 255
    # 중앙: 복숭아 씨앗 하우스 (x: 52~96, y: 20~75)
    dx = (x - 74) / 22.0
    dy = (y - 48) / 25.0
    if dx*dx + dy*dy < 1.0:
        val = 50
        # 창문과 문
        if 70 <= x <= 78 and 55 <= y <= 74: val = 255 # 열린 문
        if 62 <= x <= 68 and 38 <= y <= 46: val = 255 # 둥근 창문
    # 좌우: 환호하며 춤추는 아이들과 곤충 친구들 (y: 60~88)
    if y >= 65:
        if (x % 15 < 6): val = 30 # 아이들 실루엣
    # 하늘에 흩날리는 축제 꽃가루
    if y <= 35 and (x % 9 == 0): val = 0
    return val

# 8. 대체 씬: 복숭아 밖의 어둠
def draw_scene_alt(x, y, w, h):
    val = 255
    # 중앙: 차갑게 닫힌 복숭아 껍질과 어두운 절벽
    dx = (x - 74) / 35.0
    dy = (y - 45) / 28.0
    if dx*dx + dy*dy < 1.0: val = 80
    # 우하단: 고개 숙이고 주저앉은 제임스
    if (x - 115)**2 + (y - 68)**2 < 25 or (108 <= x <= 122 and 72 <= y <= 88): val = 30
    return val

# ─────────────────────────────────────────────────────────────
# 6프레임 시네마틱 애니메이션 (제1막)
# ─────────────────────────────────────────────────────────────
def anim_f1(x, y, w, h): # 1. 절벽 위 외딴집과 뙤약볕
    val = 255
    if (x - 120)**2 + (y - 20)**2 < 45: val = 0 # 뜨거운 태양
    if 25 <= x <= 75 and 40 <= y <= 85: val = 60 # 외딴집
    if 85 <= x <= 105 and 60 <= y <= 85: val = 120 # 울고 있는 제임스
    return val

def anim_f2(x, y, w, h): # 2. 고모들의 채찍과 호통
    val = 255
    if 20 <= x <= 60 and 30 <= y <= 85: val = 30 # 성난 두 고모
    if 65 <= x <= 85 and abs(y - 50) <= 2: val = 0 # 날아드는 채찍
    if 95 <= x <= 115 and 60 <= y <= 85: val = 150 # 쓰러진 제임스
    return val

def anim_f3(x, y, w, h): # 3. 흰 수염 노인의 등장
    val = 255
    if 35 <= x <= 65 and 35 <= y <= 85: val = 40 # 신비한 노인
    if 50 <= x <= 58 and 48 <= y <= 65: val = 255 # 흰 수염
    if 85 <= x <= 115 and 45 <= y <= 85: val = 100 # 깜짝 놀란 제임스
    return val

def anim_f4(x, y, w, h): # 4. 마법의 초록 콩 종이봉투를 건넴
    val = 255
    if 45 <= x <= 65 and 45 <= y <= 80: val = 40 # 노인의 손
    if 68 <= x <= 80 and 52 <= y <= 66: val = 0 # 빛나는 마법 봉투
    if 83 <= x <= 105 and 45 <= y <= 80: val = 70 # 제임스의 손
    return val

def anim_f5(x, y, w, h): # 5. 넘어지며 나무 밑으로 콩이 쏟아짐
    val = 255
    if 25 <= x <= 50 and 65 <= y <= 85: val = 80 # 넘어진 제임스
    if 70 <= x <= 125 and (x % 8 < 3) and (y % 8 < 3) and y >= 65: val = 0 # 흩어지는 마법 콩들
    if 105 <= x <= 135 and 20 <= y <= 85: val = 50 # 늙은 복숭아나무
    return val

def anim_f6(x, y, w, h): # 6. 흙 속에서 빛이 나며 복숭아가 꿈틀거림 (최종 정지 컷)
    return draw_scene_1(x, y, w, h)

print("🎨 [James and the Giant Peach] 8배 Braille 도트 및 6프레임 애니메이션 생성 중...")

arts = {
    "act01_scene_01": draw_to_braille(draw_scene_1),
    "act02_scene_01": draw_to_braille(draw_scene_2),
    "act03_scene_01": draw_to_braille(draw_scene_3),
    "act04_scene_01": draw_to_braille(draw_scene_4),
    "act05_scene_01": draw_to_braille(draw_scene_5),
    "act06_scene_01": draw_to_braille(draw_scene_6),
    "act07_scene_01": draw_to_braille(draw_scene_7),
    "act02_scene_01_alt": draw_to_braille(draw_scene_alt),
}

anim_frames = [
    draw_to_braille(anim_f1),
    draw_to_braille(anim_f2),
    draw_to_braille(anim_f3),
    draw_to_braille(anim_f4),
    draw_to_braille(anim_f5),
    draw_to_braille(anim_f6),
]

print("✨ 모든 아스키 아트 렌더링 완료. 정식 YAML 팩 생성 중...")

# YAML 생성 로직
yaml_content = """# ============================================
# 제임스와 슈퍼 복숭아 — 정식 게임 팩 (4/4)
# ============================================
# 원작: 로알드 달 (Roald Dahl) — James and the Giant Peach
# 78x40 고화질 시네마틱 프레임 + 8배 Braille 도트 + 6프레임 애니메이션 탑재
# ============================================

pack:
  id: "james_peach"
  title: "제임스와 슈퍼 복숭아"
  author: "로알드 달 (Roald Dahl)"
  description: "절벽 외딴집을 탈출하여 거대한 슈퍼 복숭아를 타고 대서양을 건너는 환상 모험"
  language: "ko"

  tones:
    casual:
      name: "동화 구어체"
      description: "로알드 달 특유의 재치와 유쾌한 대화체"
    classic:
      name: "영미 문학체"
      description: "고전 영미 문학의 품격과 운율을 살린 문체"
    default: "casual"

  world:
    metric:
      name: "모험의 용기"
      name_en: "Courage & Wonder"
      icon: "★"
      max: 10
      initial: 3
      description: "두려움을 극복하고 친구들과 지혜를 나눌수록 용기가 차오른다"

    chapter_term: "막"
    chapter_term_en: "Act"

    failure:
      speaker: "narrator"
      message_key: "fail_message"
      return_strategy: "scene_retry"

    password:
      enabled: true
      description: "각 막 도달 시 핵심 키워드를 암호로 부여"

  structure:
    type: "linear"
    chapters:
      - id: "act_01"
        name: "절벽 위의 외톨이"
        password: "초록콩"
        scenes: ["act01_scene_01"]
      - id: "act_02"
        name: "거대한 기적"
        password: "슈퍼복숭아"
        scenes: ["act02_scene_01", "act02_scene_01_alt"]
      - id: "act_03"
        name: "복숭아 속의 친구들"
        password: "곤충친구들"
        scenes: ["act03_scene_01"]
      - id: "act_04"
        name: "상어와 갈매기 비행"
        password: "갈매기"
        scenes: ["act04_scene_01"]
      - id: "act_05"
        name: "구름 사람들과의 충돌"
        password: "우박"
        scenes: ["act05_scene_01"]
      - id: "act_06"
        name: "엠파이어 스테이트 빌딩"
        password: "뉴욕"
        scenes: ["act06_scene_01"]
      - id: "act_07"
        name: "센트럴 파크의 축제"
        password: "대축제"
        scenes: ["act07_scene_01"]

  modes:
    full:
      name: "전체 여정"
      description: "제1막부터 제7막까지 모든 서사를 온전히 체험"
      chapters: ["act_01", "act_02", "act_03", "act_04", "act_05", "act_06", "act_07"]

  characters:
    protagonist:
      id: "james"
      name: "제임스"
      icon: "★"
    antagonist:
      id: "aunts"
      name: "스파이커 & 스펀지 고모"
      icon: "☠"
    guide:
      id: "grasshopper"
      name: "늙은 메뚜기"
      icon: "♪"
    support:
      - id: "centipede"
        name: "지네"
        icon: "👟"
      - id: "ladybug"
        name: "무당벌레"
        icon: "🐞"

  endings:
    - id: "ending_a"
      name: "하늘을 난 꿈"
      min_virtue: 7
      description: "두려움의 절벽을 넘어 대양을 건너 세상 모든 아이들에게 경이로움을 선물한 위대한 모험가"
    - id: "ending_b"
      name: "구름 위의 항해가"
      min_virtue: 4
      description: "곤충 친구들의 손을 잡고 미지의 하늘을 개척한 지혜로운 탐험가"
    - id: "ending_c"
      name: "외딴집의 방랑자"
      min_virtue: 0
      description: "기적 앞에서도 의심과 불안에 흔들렸으나 끝내 소중한 친구를 얻은 사색가"

scenes:
  # ──────────────────────────────────────────────
  # 제1막: 절벽 위의 외톨이
  # ──────────────────────────────────────────────
  - scene_id: "act01_scene_01"
    act: 1
    act_name: "절벽 위의 외톨이"
    title: "절벽 위의 외톨이"
    theme: "학대와 신비한 희망"
    message: "가장 어두운 순간에도 믿음의 씨앗을 품을 수 있는가"
    is_interpreted: false

    animation:
      frame_rate_ms: 350
      loop: false
      frames:
"""

for f_idx, fl in enumerate(anim_frames, 1):
    yaml_content += f"        # Frame {f_idx}\n        - [\n"
    for l in fl:
        escaped = l.replace('"', '\\"')
        yaml_content += f'            "{escaped}",\n'
    yaml_content += "          ]\n"

yaml_content += """
    scene_art:
"""
for l in arts["act01_scene_01"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "스파이커 고모"
          text: "제임스! 뼈골이 빠지도록 장작을 패란 말이야! 밥 먹을 자격도 없는 녀석!"
        - speaker: "스펀지 고모"
          text: "얼굴만 반반하고 쓸모없는 녀석! 뙤약볕 아래서 밤새도록 일해!"
        - speaker: "노인"
          text: "울지 마라, 얘야. 이 종이봉투 속 마법의 초록 콩을 보아라. 곧 놀라운 기적이 너를 찾아갈 테니!"
      tone_classic:
        - speaker: "스파이커 고모"
          text: "게으른 악동아! 손이 닳도록 장작을 쪼개지 못할까!"
        - speaker: "스펀지 고모"
          text: "가련한 척 울먹이지 마라! 식충이에게 베풀 자비란 없다!"
        - speaker: "노인"
          text: "슬퍼 말거라, 작은 친구여. 태고의 신비가 깃든 이 씨앗들이 네 운명을 완전히 뒤바꾸리라."

    substitutions:
      tone_casual:
        status_line: "외딴집의 절벽"
      tone_classic:
        status_line: "고난의 외딴집"

    choices:
      - id: "act01_c1"
        text:
          tone_casual: "노인의 말을 믿고 희망을 품으며 쏟아진 콩을 찾는다"
          tone_classic: "기적의 약속을 신뢰하며 흩어진 신비의 씨앗을 모은다"
        virtue_change: 1
        next_scene: "act02_scene_01"

      - id: "act01_c2"
        text:
          tone_casual: "내 팔자에 무슨 기적이람... 슬픔에 잠겨 체념한다"
          tone_classic: "혹독한 운명을 탓하며 체념 속에 주저앉는다"
        virtue_change: -1
        next_scene: "act02_scene_01"

  # ──────────────────────────────────────────────
  # 제2막: 거대한 기적
  # ──────────────────────────────────────────────
  - scene_id: "act02_scene_01"
    act: 2
    act_name: "거대한 기적"
    title: "거대한 기적"
    theme: "기적의 탄생과 탐험"
    message: "미지의 문턱 앞에서 두려움을 딛고 전진할 용기가 있는가"
    is_interpreted: false

    scene_art:
"""
for l in arts["act02_scene_01"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "제임스"
          text: "세상에! 죽어가던 복숭아나무에 달린 복숭아가 집채보다 더 커졌어!"
        - speaker: "스파이커 고모"
          text: "이게 웬 횡재냐! 입장료를 받고 구경꾼들을 불러 모으자!"
        - speaker: "제임스"
          text: "어라? 복숭아 밑바닥에 사람 하나가 기어들어갈 만한 터널이 있네...?"
      tone_classic:
        - speaker: "제임스"
          text: "오, 하느님! 메마른 고목에서 황금빛 거대한 태양 같은 복숭아가 부풀어 오르다니!"
        - speaker: "스펀지 고모"
          text: "돈 벼락이 굴러들어왔구나! 은화 한 닢씩 받고 구경을 시키자!"
        - speaker: "제임스"
          text: "달콤한 향기가 뿜어져 나오는 저 터널... 나를 부르고 있어."

    substitutions:
      tone_casual:
        status_line: "거대 복숭아 앞"
      tone_classic:
        status_line: "황금 과육의 방주"

    choices:
      - id: "act02_c1"
        text:
          tone_casual: "두려움을 떨치고 복숭아 속 터널로 기어 들어간다"
          tone_classic: "두려움을 극복하고 신비로운 과육의 통로로 나아간다"
        virtue_change: 2
        next_scene: "act03_scene_01"

      - id: "act02_c2"
        text:
          tone_casual: "괴물 과일일지도 몰라... 뒷걸음질 치며 물러선다"
          tone_classic: "미지의 환영을 두려워하며 뒤로 물러선다"
        virtue_change: -1
        next_scene: "act02_scene_01_alt"

  # ──────────────────────────────────────────────
  # 제3막: 복숭아 속의 친구들 (전환씬)
  # ──────────────────────────────────────────────
  - scene_id: "act03_scene_01"
    act: 3
    act_name: "복숭아 속의 친구들"
    title: "복숭아 속의 친구들"
    theme: "우정과 새로운 세계로의 출항"
    message: "겉모습 너머의 따스한 마음을 알아볼 수 있는가"
    is_interpreted: true
    is_transition: true
    next_scene: "act04_scene_01"

    scene_art:
"""
for l in arts["act03_scene_01"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "늙은 메뚜기"
          text: "안녕하신가, 꼬마 도련님! 우린 자네를 아주 오랫동안 기다렸다네!"
        - speaker: "지네"
          text: "누가 내 부츠 42켤레 벗는 것 좀 도와줄 사람 없소? 허리가 끊어지겠네!"
        - speaker: "무당벌레"
          text: "무서워하지 마렴, 착한 제임스. 우린 이제 한 배를 탄 가족이란다."
      tone_classic:
        - speaker: "늙은 메뚜기"
          text: "환영하오, 친애하는 제임스! 자네야말로 이 위대한 방주의 주인이오."
        - speaker: "미스 스파이더"
          text: "당신을 해치지 않아요. 우린 두 고모의 핍박에서 함께 탈출할 동료들이랍니다."
        - speaker: "지네"
          text: "자, 복숭아 꼭지를 끊었다! 신대륙을 향해 굴러가자!"

    substitutions:
      tone_casual:
        status_line: "바다로의 출항"
      tone_classic:
        status_line: "대양의 첫 항해"

  # ──────────────────────────────────────────────
  # 제4막: 상어와 갈매기 비행
  # ──────────────────────────────────────────────
  - scene_id: "act04_scene_01"
    act: 4
    act_name: "상어와 갈매기 비행"
    title: "상어와 갈매기 비행"
    theme: "위기 극복과 기발한 지혜"
    message: "절체절명의 위기에서 지혜와 협동으로 하늘을 날아오르라"
    is_interpreted: false

    scene_art:
"""
for l in arts["act04_scene_01"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "지렁이"
          text: "으앙! 상어가 복숭아를 다 갉아먹고 있어! 우린 이제 끝장이야!"
        - speaker: "제임스"
          text: "지렁이 아저씨가 잠깐 미끼가 되어주세요! 갈매기들이 다가오면 거미줄로 묶을게요!"
        - speaker: "지네"
          text: "세상에, 복숭아가 하늘로 둥실 떠오른다! 제임스, 넌 천재야!"
      tone_classic:
        - speaker: "지렁이"
          text: "비극이로다! 대양의 포식자들이 우리의 방주를 물어뜯고 있사옵니다!"
        - speaker: "제임스"
          text: "절망하지 마세요. 하늘의 갈매기들과 미스 스파이더의 명주실이 결합하면 창공이 우리의 길이 됩니다!"
        - speaker: "늙은 메뚜기"
          text: "경이롭도다! 500마리 백옥 같은 날갯짓이 대양을 발아래 두었구나!"

    substitutions:
      tone_casual:
        status_line: "하늘 비행 중"
      tone_classic:
        status_line: "창공의 대항해"

    choices:
      - id: "act04_c1"
        text:
          tone_casual: "제임스의 지혜를 믿고 갈매기 500마리 결박 작전을 감행한다"
          tone_classic: "기발한 지혜를 좇아 갈매기 편대 결박 작전을 결행한다"
        virtue_change: 2
        next_scene: "act05_scene_01"

      - id: "act04_c2"
        text:
          tone_casual: "위험하니 일단 과육 깊숙이 숨어 상어가 지나가길 기다린다"
          tone_classic: "안전을 도모하며 과육 속 깊은 곳에 은신한다"
        virtue_change: 0
        next_scene: "act05_scene_01"

  # ──────────────────────────────────────────────
  # 제5막: 구름 사람들과의 충돌 (전환씬)
  # ──────────────────────────────────────────────
  - scene_id: "act05_scene_01"
    act: 5
    act_name: "구름 사람들과의 충돌"
    title: "구름 사람들과의 충돌"
    theme: "천상의 신비와 결속"
    message: "어떤 거친 폭풍우 속에서도 서로의 손을 놓지 마라"
    is_interpreted: true
    is_transition: true
    next_scene: "act06_scene_01"

    scene_art:
"""
for l in arts["act05_scene_01"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "구름 사람"
          text: "감히 신성한 구름 공장에 침입해 장난을 치다니! 우박 맛을 보아라!"
        - speaker: "반딧불이"
          text: "앞이 안 보여요! 제가 꽁무니 불빛을 최대로 밝힐게요!"
        - speaker: "제임스"
          text: "갈매기들아, 힘을 내! 저 먹구름만 뚫고 나가면 맑은 햇살이야!"
      tone_classic:
        - speaker: "구름 사람"
          text: "천상의 영역을 어지럽힌 불경한 자들이여, 우박과 폭풍의 징벌을 받으라!"
        - speaker: "늙은 메뚜기"
          text: "전율의 뇌우가 몰아치는도다! 날개를 굳게 펴고 고도를 높여라!"
        - speaker: "제임스"
          text: "우리의 결속은 어떤 폭풍우보다 강합니다! 전방을 돌파하십시오!"

    substitutions:
      tone_casual:
        status_line: "구름 돌파"
      tone_classic:
        status_line: "뇌우의 시련"

  # ──────────────────────────────────────────────
  # 제6막: 엠파이어 스테이트 빌딩 (전환씬)
  # ──────────────────────────────────────────────
  - scene_id: "act06_scene_01"
    act: 6
    act_name: "엠파이어 스테이트 빌딩"
    title: "엠파이어 스테이트 빌딩"
    theme: "신세계 도달과 영광스러운 착륙"
    message: "불가능해 보이던 꿈이 마침내 눈앞의 현실로 우뚝 서다"
    is_interpreted: true
    is_transition: true
    next_scene: "act07_scene_01"

    scene_art:
"""
for l in arts["act06_scene_01"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "뉴욕 시민들"
          text: "하늘에 거대한 괴물 과일이 나타났다! 공습경보를 울려라!"
        - speaker: "지네"
          text: "야호! 우리가 대서양을 건넜어! 저 아래 끝없는 빌딩 숲을 좀 봐!"
        - speaker: "제임스"
          text: "비행기가 줄을 끊었지만... 첨탑 위에 완벽하게 꽂혀서 착륙했어!"
      tone_classic:
        - speaker: "뉴욕 시장"
          text: "신의 조화인가, 미지의 비행선인가! 전 대원들은 구조 태세를 갖추라!"
        - speaker: "무당벌레"
          text: "오, 하느님 감사합니다. 대서양의 험난한 파도를 넘어 꿈의 도시에 안착했군요."
        - speaker: "제임스"
          text: "우리가 해냈어요! 절벽 외딴집에서 이곳 신세계의 심장부까지 날아왔어요!"

    substitutions:
      tone_casual:
        status_line: "뉴욕 상공 착륙"
      tone_classic:
        status_line: "신세계의 첨탑"

  # ──────────────────────────────────────────────
  # 제7막: 센트럴 파크의 축제
  # ──────────────────────────────────────────────
  - scene_id: "act07_scene_01"
    act: 7
    act_name: "센트럴 파크의 축제"
    title: "센트럴 파크의 축제"
    theme: "나눔과 영원한 우정"
    message: "기적의 열매를 세상과 나눌 때 진정한 영광이 완성된다"
    is_interpreted: false

    scene_art:
"""
for l in arts["act07_scene_01"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "뉴욕 아이들"
          text: "와아! 복숭아가 너무 달콤하고 맛있어요! 제임스 만세!"
        - speaker: "지네 & 메뚜기"
          text: "우린 이제 뉴욕의 명예 시민이자 가장 멋진 친구들이라네!"
        - speaker: "제임스"
          text: "이 거대한 복숭아 씨앗 집에서, 매일 친구들과 행복한 모험을 쓸 거예요."
      tone_classic:
        - speaker: "뉴욕 시장"
          text: "용기 있는 소년 제임스와 고귀한 신사 곤충들에게 뉴욕시의 황금 열쇠를 바칩니다!"
        - speaker: "무당벌레"
          text: "사랑과 나눔이 있는 곳에 진정한 안식처가 있음을 배웠습니다."
        - speaker: "제임스"
          text: "외로움은 끝났습니다. 온 세상 아이들에게 꿈과 경이로움을 전하는 작가가 되겠습니다."

    substitutions:
      tone_casual:
        status_line: "센트럴 파크 축제"
      tone_classic:
        status_line: "영광의 대축제"

    choices:
      - id: "act07_c1"
        text:
          tone_casual: "온 도시의 아이들을 초대해 달콤한 복숭아 과육을 배불리 나눈다"
          tone_classic: "도시의 모든 어린 영혼들을 초대하여 풍요로운 결실을 나눈다"
        virtue_change: 2
        next_scene: "ending"

      - id: "act07_c2"
        text:
          tone_casual: "우리를 도와준 곤충 친구들과 조촐하게 우리만의 승리를 축하한다"
          tone_classic: "생사를 함께한 동료들과 조용히 승리의 기쁨을 나눈다"
        virtue_change: 0
        next_scene: "ending"

  # ──────────────────────────────────────────────
  # 대체 씬: 복숭아 밖의 어둠
  # ──────────────────────────────────────────────
  - scene_id: "act02_scene_01_alt"
    act: 2
    act_name: "거대한 기적"
    title: "복숭아 밖의 어둠"
    theme: "망설임과 후회"
    message: "두려움에 주저앉지 말고 다시 용기 내어 기적으로 나아가라"
    is_interpreted: true
    is_transition: true
    next_scene: "act02_scene_01"

    scene_art:
"""
for l in arts["act02_scene_01_alt"]:
    escaped = l.replace('"', '\\"')
    yaml_content += f'      - "{escaped}"\n'

yaml_content += """
    dialogue:
      tone_casual:
        - speaker: "제임스"
          text: "내가 왜 바보같이 도망쳤을까... 저 복숭아 속에는 분명 다른 세상이 있었는데..."
        - speaker: "스파이커 고모"
          text: "제임스! 멍하니 서 있지 말고 구경꾼들 신발이나 닦아!"
        - speaker: "제임스"
          text: "아니야, 난 평생 이렇게 살 순 없어. 지금이라도 터널 속으로 뛰어들어야 해!"
      tone_classic:
        - speaker: "제임스"
          text: "나약한 두려움이 기적의 문을 닫아버렸구나... 회한이 가슴을 찌르는도다."
        - speaker: "스펀지 고모"
          text: "식충이 녀석, 잔말 말고 바닥이나 쓸어라!"
        - speaker: "제임스"
          text: "운명의 부름을 외면하지 않으리라. 다시 저 과육의 심장부로 나아가리라!"

    substitutions:
      tone_casual:
        status_line: "어둠 속의 후회"
      tone_classic:
        status_line: "회한의 마당"
"""

with open(os.path.join(OUT_DIR, "3_scene.yaml"), "w", encoding="utf-8") as f:
    f.write(yaml_content)

with open(os.path.join(OUT_DIR, "4_game_scene.yaml"), "w", encoding="utf-8") as f:
    f.write(yaml_content)

print("🎉 [james_peach] 3_scene.yaml 및 4_game_scene.yaml 생성 완료!")
