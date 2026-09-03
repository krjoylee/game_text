#!/usr/bin/env python3
"""
tools/generate_all_cutscenes_studio.py
흥부놀부전 1막~7막 전체 컷씬(8개) 도트 데이터 생성 및
D:/game/images/ 뷰어 콘솔(HTML/배치파일) 자동 구축기!
사용자가 윈도우에서 더블 클릭 한 번으로 모든 막의 컷씬을 전환해가며 편하게 검토하고 컨펌할 수 있도록 함.
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

# 추가 색상 인덱스
C_SWALLOW_BLUE = 7   # 제비 푸른 등
C_SWALLOW_RED = 6    # 제비 목밑 붉은 깃 / 부목 붉은 실
C_GOBLIN_GREEN = 13  # 도깨비 피부 녹색
C_CLUB_GRAY = 14     # 도깨비 방망이 / 쇠가시 회색
C_FIELD_GREEN = 15   # 화해의 들판 새싹 녹색
C_GOURD_YELLOW = 12  # 잘 익은 누런 대박

# ─────────────────────────────────────────────────────────────────────────────
# 2막: 다친 제비 (처마 밑 둥지 & 피 흘리는 부러진 제비 다리를 감싸 쥔 흥부)
# ─────────────────────────────────────────────────────────────────────────────
def create_act2_frames():
    f1 = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # 1. 처마선 (상단)
    for x in range(CANVAS_W):
        f1[0][x] = C_LINE; f1[1][x] = C_LINE
    for x in range(0, CANVAS_W, 6):
        f1[2][x] = C_SHADOW; f1[2][x+1] = C_SHADOW
        
    # 2. 좌측: 서글프고 간절한 흥부 (고개 숙여 손을 모음)
    for y in range(8, 20):
        for x in range(12, 22): f1[y][x] = C_SKIN
    # 상투
    for y in range(4, 8):
        for x in range(14, 18): f1[y][x] = C_LINE
    # 눈 (처진 서글픈 눈)
    f1[12][14] = C_LINE; f1[12][19] = C_LINE
    f1[13][13] = C_SHADOW; f1[13][20] = C_SHADOW
    # V턱선
    for x in range(14, 20): f1[20][x] = C_SHADOW
    # 흥부의 두 손 (가슴 앞에 조심스레 모음)
    for y in range(22, 26):
        for x in range(22, 32): f1[y][x] = C_SKIN
    # 삼베옷
    for y in range(21, 38):
        for x in range(8, 25):
            f1[y][x] = C_HAT if (x+y)%2==0 else C_HEMP_ROUGH
            
    # 3. 중앙: 두 손 안의 작은 새끼 제비
    for y in range(20, 25):
        for x in range(32, 44): f1[y][x] = C_SWALLOW_BLUE
    # 제비 목밑 붉은 깃
    f1[23][34] = C_SWALLOW_RED; f1[23][35] = C_SWALLOW_RED
    # 제비 반짝이는 눈
    f1[21][33] = C_WHITE; f1[21][34] = C_LINE
    # 꺾여 늘어진 다리 & 붉은 명주실
    f1[25][38] = C_LINE
    f1[26][39] = C_SWALLOW_RED # 붉은 실로 감은 부목!
    f1[27][39] = C_WHITE       # 하얀 부목
    f1[26][40] = C_SWALLOW_RED
    
    # 6프레임 호흡
    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        if i % 2 == 1:
            fr[21][33] = C_WHITE # 제비 눈 깜빡임
            fr[26][39] = C_WHITE; fr[26][40] = C_SWALLOW_RED
        if i == 2: # F3: 흥부의 눈물 한 방울 제비 다리로 톡!
            fr[15][19] = C_TEAR
            fr[24][36] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 3막: 박씨 (이듬해 봄, 은혜 갚으러 허공을 가르며 박씨를 물고 날아온 제비)
# ─────────────────────────────────────────────────────────────────────────────
def create_act3_frames():
    f1 = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # 봄날의 먼 산과 구름
    for x in range(CANVAS_W):
        f1[35][x] = C_FIELD_GREEN; f1[36][x] = C_FIELD_GREEN; f1[37][x] = C_FIELD_GREEN
        
    # 날아드는 제비의 힘찬 날개짓 (중앙 상단)
    for y in range(8, 16):
        for x in range(28, 48): f1[y][x] = C_SWALLOW_BLUE
    # 날개 편 실루엣
    for x in range(18, 28): f1[6][x] = C_SWALLOW_BLUE; f1[7][x] = C_SWALLOW_BLUE
    for x in range(48, 58): f1[6][x] = C_SWALLOW_BLUE; f1[7][x] = C_SWALLOW_BLUE
    # 배 쪽 하얀 깃털
    for y in range(12, 17):
        for x in range(35, 42): f1[y][x] = C_WHITE
    # 목덜미 붉은 깃
    f1[11][37] = C_SWALLOW_RED; f1[11][38] = C_SWALLOW_RED
    
    # 부리에 문 황금빛 영롱한 박씨 (F3에서 번쩍!)
    f1[10][39] = C_GOLD; f1[10][40] = C_GOLD
    
    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # 날개 위아래 퍼덕임
        if i in (1, 2, 4):
            for x in range(18, 28): fr[5][x] = C_SWALLOW_BLUE; fr[6][x] = C_BG
            for x in range(48, 58): fr[5][x] = C_SWALLOW_BLUE; fr[6][x] = C_BG
        if i == 2: # F3 박씨 황금빛 발광!
            fr[9][39] = C_WHITE; fr[10][40] = C_WHITE; fr[11][39] = C_GOLD
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 4막: 흥부의 박 (초가지붕 위 거대한 대박을 켜자 쏟아지는 황금빛 엽전과 쌀)
# ─────────────────────────────────────────────────────────────────────────────
def create_act4_frames():
    f1 = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # 초가지붕 (하단)
    for y in range(28, 38):
        for x in range(CANVAS_W):
            f1[y][x] = C_HAT if (x+y)%2==0 else C_SHADOW
            
    # 지붕 위 둥글고 커다란 황금빛 박 (중앙)
    for y in range(6, 26):
        for x in range(24, 52): f1[y][x] = C_GOURD_YELLOW
    # 박 갈라진 틈 (톱질 선)
    for y in range(6, 26): f1[y][38] = C_WHITE
    # 박 꼭지 & 넝쿨
    f1[4][37] = C_FIELD_GREEN; f1[4][38] = C_FIELD_GREEN; f1[5][38] = C_FIELD_GREEN
    
    # 박 속에서 뿜어져 나오는 보물 광채 (황금빛 & 은빛)
    for y in range(10, 22):
        f1[y][36] = C_GOLD; f1[y][37] = C_WHITE; f1[y][39] = C_GOLD; f1[y][40] = C_WHITE
        
    # 좌우 흥부 부부의 신명 나는 톱질 (엉차!)
    for y in range(16, 28):
        for x in range(8, 16): f1[y][x] = C_SKIN # 흥부
        for x in range(60, 68): f1[y][x] = C_SKIN # 아내
    # 긴 톱날
    for x in range(16, 60): f1[20][x] = C_CLUB_GRAY
    
    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        # 톱질 좌우 왕복
        shift = (i % 2) * 2 - 1
        for x in range(18, 58): fr[20][x+shift] = C_WHITE
        if i == 2: # F3 금은보화 대분출!
            for y in range(7, 25, 2):
                fr[y][37] = C_WHITE; fr[y][38] = C_GOLD; fr[y][39] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 5막: 놀부의 욕심 (시커먼 속셈으로 죄 없는 제비 다리를 뚝 분지르는 섬뜩한 손)
# ─────────────────────────────────────────────────────────────────────────────
def create_act5_frames():
    f1 = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # 놀부의 비열하고 거대한 얼굴 (좌측 상단에서 내려다봄)
    for y in range(2, 14):
        for x in range(10, 24): f1[y][x] = C_SKIN
    # 갓
    for y in range(0, 3):
        for x in range(8, 26): f1[y][x] = C_LINE
    # 사악하게 치켜뜬 세모 눈 & 금이빨
    f1[6][14] = C_LINE; f1[6][20] = C_LINE
    f1[10][17] = C_GOLD # 번뜩이는 금이빨
    
    # 탐욕스러운 놀부의 거친 큰 손 (중앙)
    for y in range(14, 26):
        for x in range(26, 42): f1[y][x] = C_SKIN
    for y in range(18, 24): f1[y][28] = C_SHADOW; f1[y][34] = C_SHADOW
    
    # 붙잡혀 버둥거리는 가련한 새끼 제비 (손아귀 속)
    for y in range(16, 24):
        for x in range(40, 52): f1[y][x] = C_SWALLOW_BLUE
    f1[18][42] = C_WHITE; f1[18][43] = C_LINE # 겁에 질린 동공
    
    # 다리를 잡고 꺾으려는 찰나의 순간
    f1[23][46] = C_LINE; f1[24][47] = C_LINE
    
    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        if i == 2: # F3: 꺾! 다리 분지름 & 제비 비명 & 번쩍광!
            fr[24][46] = C_SWALLOW_RED # 핏자국!
            fr[25][47] = C_SWALLOW_RED
            fr[10][17] = C_WHITE # 놀부 비열한 미소
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 6막: 놀부의 박 (박을 타자 터져 나오는 험악한 청록색 도깨비와 쇠몽둥이 폭풍)
# ─────────────────────────────────────────────────────────────────────────────
def create_act6_frames():
    f1 = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # 깨진 흉측한 박 껍질 (좌우로 갈라짐)
    for y in range(10, 32):
        for x in range(8, 22): f1[y][x] = C_SHADOW
        for x in range(54, 68): f1[y][x] = C_SHADOW
        
    # 중앙에서 치솟은 거대한 청록색 외뿔 도깨비 (위압적 구도)
    for y in range(4, 22):
        for x in range(26, 50): f1[y][x] = C_GOBLIN_GREEN
    # 솟구친 날카로운 황금빛 외뿔!
    for y in range(1, 6): f1[y][38] = C_GOLD
    # 부리부리한 붉은 눈 & 튀어나온 뻐드렁니
    f1[10][32] = C_SWALLOW_RED; f1[10][33] = C_WHITE
    f1[10][43] = C_WHITE; f1[10][44] = C_SWALLOW_RED
    f1[15][36] = C_WHITE; f1[15][40] = C_WHITE # 송곳니
    
    # 도깨비가 휘두르는 거대한 가시 쇠몽둥이!
    for y in range(2, 16):
        for x in range(50, 58): f1[y][x] = C_CLUB_GRAY
    # 쇠가시 돌기
    f1[4][49] = C_WHITE; f1[8][59] = C_WHITE; f1[12][49] = C_WHITE
    
    # 바닥에 나뒹굴며 싹싹 비는 놀부 실루엣 (우측 하단)
    for y in range(28, 36):
        for x in range(30, 46): f1[y][x] = C_SILK_BLUE
    f1[26][36] = C_SKIN; f1[26][37] = C_SKIN
    
    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        if i == 2: # F3: 쇠몽둥이 강타 이펙트 번쩍!
            for x in range(48, 62): fr[6][x] = C_WHITE
            fr[10][32] = C_WHITE; fr[10][44] = C_WHITE
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 7막: 눈물의 화해 (알거지가 된 형을 품에 안고 눈물 흘리는 형제의 감동적 재회)
# ─────────────────────────────────────────────────────────────────────────────
def create_act7_frames():
    f1 = [[C_BG for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]
    
    # 따스한 봄날 햇살 (상단 원경)
    for x in range(30, 44): f1[1][x] = C_GOLD; f1[2][x] = C_GOLD
    
    # 좌측: 부자가 되었으나 비단옷 대신 정갈한 옷으로 형을 부축하는 흥부
    for y in range(8, 24):
        for x in range(16, 28): f1[y][x] = C_SKIN
    # 따스한 눈매와 흘러내리는 감격의 눈물
    f1[13][20] = C_LINE; f1[13][24] = C_LINE
    f1[15][21] = C_TEAR # 감격의 눈물
    
    # 우측: 갓도 옷도 찢겨 누더기를 걸치고 엎드려 통곡하는 놀부
    for y in range(14, 28):
        for x in range(36, 52): f1[y][x] = C_SKIN
    # 찢긴 옷
    for y in range(20, 36):
        for x in range(38, 56): f1[y][x] = C_RAG
    # 무릎 꿇고 손을 맞잡음
    for x in range(28, 38):
        f1[20][x] = C_SKIN; f1[21][x] = C_SKIN
        
    # 하단: 파릇파릇 돋아난 화해의 들판 잔디
    for y in range(34, 38):
        for x in range(CANVAS_W): f1[y][x] = C_FIELD_GREEN
        
    frames = []
    for i in range(6):
        fr = [row[:] for row in f1]
        if i == 2: # F3: 따스한 봄 햇살 광채 번쩍 & 형제의 눈물
            for x in range(28, 46): fr[2][x] = C_WHITE
            fr[16][21] = C_WHITE; fr[22][40] = C_TEAR
        frames.append(fr)
    return frames

# ─────────────────────────────────────────────────────────────────────────────
# 마스터 스튜디오 빌더 (D:/game/images/ 및 D:/game/images/studio.html)
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
        {"id": 1, "title": "제1막: 형제의 갈림길 (쫓겨나는 흥부)", "desc": "놀부의 탐욕스러운 칠흑 갓과 번쩍이는 황금 앞니(금이빨), 서글픈 흥부의 눈물", "frames": act1},
        {"id": 2, "title": "제2막: 다친 제비 (지극한 자비)", "desc": "구렁이에 놀라 떨어진 새끼 제비의 부러진 다리에 붉은 실로 부목을 대어주는 흥부의 두 손", "frames": act2},
        {"id": 3, "title": "제3막: 박씨 (보은의 비행)", "desc": "이듬해 봄, 푸른 창공을 가르며 황금빛 박씨를 부리에 물고 흥부네로 날아오는 제비", "frames": act3},
        {"id": 4, "title": "제4막: 흥부의 박 (대박의 축복)", "desc": "지붕 위 거대한 대박을 타자 눈부신 황금 엽전과 은보화, 쌀알이 쏟아져 나오는 기적", "frames": act4},
        {"id": 5, "title": "제5막: 놀부의 욕심 (인과응보의 시작)", "desc": "박씨를 탐내어 멀쩡한 제비 다리를 시커먼 손으로 일부러 뚝 분지르는 놀부의 섬뜩한 만행", "frames": act5},
        {"id": 6, "title": "제6막: 놀부의 박 (도깨비의 심판)", "desc": "박 속에서 터져 나온 험악한 청록색 외뿔 도깨비가 가시 쇠몽둥이로 놀부를 응징하는 아수라장", "frames": act6},
        {"id": 7, "title": "제7막: 화해 (형제의 봄날)", "desc": "알거지가 된 형을 품에 안고 용서하는 흥부, 눈물로 참회하며 맞잡은 두 손과 화해의 봄 들판", "frames": act7},
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
<title>Divina Ludus — 컷씬 검토 & 컨펌 스튜디오 (Cutscene Studio)</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; }}
  html, body {{
    width: 100%;
    height: 100%;
    overflow: hidden; /* 휠 스크롤 고정 */
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  .studio-frame {{
    width: 960px;
    height: 820px;
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
  
  /* 메인 뷰: 좌측 씬 네비게이션 + 우측 캔버스 및 설명 */
  .main-content {{
    flex: 1;
    display: flex;
    background: #181818;
  }}
  .sidebar {{
    width: 240px;
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
    padding: 10px 14px;
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
    width: 660px;
    height: 338px;
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
    <div class="studio-title">🎨 Divina Ludus — 컷씬 검토 & 컨펌 스튜디오</div>
    <div class="studio-hud" id="hudText">[Act 1 / 7 | 296x152 4X Hi-Res]</div>
  </div>

  <div class="main-content">
    <!-- 좌측 막 전환 탭 -->
    <div class="sidebar" id="sidebar"></div>

    <!-- 우측 4배 캔버스 렌더러 -->
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
    <div>조작 안내: <span class="key-hint">[1~7] 숫자키</span>로 씬 즉시 이동 | <span class="key-hint">[Space]</span> 일시정지 | 마우스 클릭 가능</div>
    <div style="color: #2ecc71;">● 윈도우 원클릭 컨펌 스튜디오</div>
  </div>
</div>

<script>
  const data = {studio_json};
  const canvas = document.getElementById('retroCanvas');
  const ctx = canvas.getContext('2d');
  
  let curActIdx = 0;
  let curFrame = 0;
  let isPaused = false;
  
  // 사이드바 탭 생성
  const sidebar = document.getElementById('sidebar');
  data.acts.forEach((act, idx) => {{
    const btn = document.createElement('button');
    btn.className = 'nav-btn' + (idx === 0 ? ' active' : '');
    btn.innerText = `[${{idx+1}}] 막: ${{act.title.split(' ')[0]}}`;
    btn.onclick = () => selectAct(idx);
    sidebar.appendChild(btn);
  }});
  
  function selectAct(idx) {{
    curActIdx = idx;
    curFrame = 0;
    
    // 버튼 스타일
    const btns = sidebar.querySelectorAll('.nav-btn');
    btns.forEach((b, i) => {{
      b.className = 'nav-btn' + (i === idx ? ' active' : '');
    }});
    
    // 정보 카드 갱신
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
  
  // 0.75초 간격 모션 루프
  setInterval(() => {{
    if (isPaused) return;
    const act = data.acts[curActIdx];
    curFrame = (curFrame + 1) % act.frames.length;
    renderCurrentFrame();
  }}, 750);
  
  // 초기 렌더
  selectAct(0);
  
  // 키보드 조작 (1~7 바로가기, Space 정지)
  window.addEventListener('keydown', (e) => {{
    const num = parseInt(e.key);
    if (num >= 1 && num <= data.acts.length) {{
      selectAct(num - 1);
    }} else if (e.code === 'Space') {{
      isPaused = !isPaused;
    }}
  }});
  
  // 휠 스크롤 화면 흔들림 완전 락
  window.addEventListener('wheel', (e) => {{
    e.preventDefault();
  }}, {{ passive: false }});
</script>

</body>
</html>
"""
    # 1. images/studio.html 저장
    studio_html_path = "/mnt/d/game/images/studio.html"
    with open(studio_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # 2. images/view_images.bat 런처 저장
    launcher_bat_path = "/mnt/d/game/images/view_images.bat"
    bat_content = """@echo off
title Divina Ludus - Cutscene Studio
start msedge.exe --app="file:///D:/game/images/studio.html" --window-size=980,860 || start chrome.exe --app="file:///D:/game/images/studio.html" --window-size=980,860 || start "" "D:\\game\\images\\studio.html"
exit
"""
    with open(launcher_bat_path, "w", encoding="cp949") as f:
        f.write(bat_content)
        
    # 3. 루트 D:/game/view_images.bat 바로가기도 생성
    root_launcher_path = "/mnt/d/game/view_images.bat"
    with open(root_launcher_path, "w", encoding="cp949") as f:
        f.write(bat_content)

    print(f"✅ 흥부놀부전 1~7막 전 컷씬 스튜디오 생성 완료!")
    print(f"   - 뷰어 파일: {studio_html_path}")
    print(f"   - 실행 런처: {launcher_bat_path} 및 {root_launcher_path}")

if __name__ == "__main__":
    build_all_studio()
