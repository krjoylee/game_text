#!/usr/bin/env python3
"""
tools/build_full_heungbu_game.py
《흥부놀부전》 튜토리얼 팩 완전 정식 게임 완성 빌더
- 1막부터 7막까지의 분기 선택지, 대화(화자별), 선행 게이지 변동, 엔딩 평가(칭호) 탑재
- 네이티브 296x152 영화적 4X 고밀도 6프레임 모션 애니메이션 완벽 연동
- RLE 압축으로 1MB 이하 단일 파일 배포 (D:/game/Divina_Console.html + run_console.bat)
"""

import os
import sys
import json

sys.path.append("/home/krjoylee/code/game/tools")
from generate_hires_studio import (
    gen_hires_act1, gen_hires_act2, gen_hires_act3, gen_hires_act4,
    gen_hires_act5, gen_hires_act6, gen_hires_act7, PALETTE_16
)

def compress_frame_rle(grid):
    flat = [p for row in grid for p in row]
    chunks = []
    cur_c = flat[0]
    cur_cnt = 1
    for p in flat[1:]:
        if p == cur_c and cur_cnt < 255:
            cur_cnt += 1
        else:
            chunks.append(f"{cur_cnt}_{cur_c}")
            cur_c = p
            cur_cnt = 1
    chunks.append(f"{cur_cnt}_{cur_c}")
    return ",".join(chunks)

def build_game():
    print("🎬 296x152 영화적 컷씬 렌더링 및 RLE 압축 중...")
    act1_rle = [compress_frame_rle(f) for f in gen_hires_act1()]
    act2_rle = [compress_frame_rle(f) for f in gen_hires_act2()]
    act3_rle = [compress_frame_rle(f) for f in gen_hires_act3()]
    act4_rle = [compress_frame_rle(f) for f in gen_hires_act4()]
    act5_rle = [compress_frame_rle(f) for f in gen_hires_act5()]
    act6_rle = [compress_frame_rle(f) for f in gen_hires_act6()]
    act7_rle = [compress_frame_rle(f) for f in gen_hires_act7()]

    # 1막~7막 전체 게임 씬 데이터
    scenes = [
        {
            "id": "act01",
            "act": 1,
            "title": "형제의 갈림길",
            "speaker": "놀부",
            "text": "네 이놈 흥부야! 내 집에 더는 쌀 한 톨 축낼 생각 마라! 처자식 데리고 썩 꺼지지 못할까!",
            "rle": act1_rle,
            "is_transition": False,
            "choices": [
                {"text": "부모님 말씀을 떠올리며 조용히 돌아선다", "delta": 1, "next": "act02", "feedback": "흥부는 눈물을 삼키며 빈손으로 형의 집을 나섰습니다. 가슴은 찢어지듯 아팠으나 원망하지 않았습니다."},
                {"text": "억울함에 형에게 따져본다", "delta": -1, "next": "act02", "feedback": "놀부가 몽둥이를 치켜들며 호통쳤습니다! '이놈이 어디서 감히 눈을 부라리느냐!'"}
            ]
        },
        {
            "id": "act02",
            "act": 2,
            "title": "다친 제비",
            "speaker": "흥부 아내",
            "text": "여보! 저 처마 밑 제비 좀 보세요! 구렁이에 놀라 떨어져 다리가 부러졌어요! 짹짹 울며 피를 흘리고 있어요!",
            "rle": act2_rle,
            "is_transition": False,
            "choices": [
                {"text": "정성껏 하얀 부목을 대고 붉은 실로 감아준다", "delta": 2, "next": "act03", "feedback": "흥부는 떨리는 손으로 새끼 제비의 다리에 부목을 대고 붉은 실로 정성껏 묶어주었습니다. '미물이라도 귀한 목숨이지...'"},
                {"text": "우리 먹을 것도 없는데... 모른 척 지나친다", "delta": -2, "next": "act03_alt", "feedback": "흥부는 한숨을 쉬며 발길을 돌렸습니다. 처마 밑에는 제비의 슬픈 울음소리만 흩어졌습니다."}
            ]
        },
        {
            "id": "act03",
            "act": 3,
            "title": "박씨를 물고 온 제비",
            "speaker": "해설",
            "text": "이듬해 봄, 푸른 창공을 가르며 다리를 고쳤던 제비가 돌아왔습니다. 부리에는 눈부신 황금빛 박씨 하나가 영롱하게 빛나고 있었습니다!",
            "rle": act3_rle,
            "is_transition": True,
            "next": "act04",
            "button_text": "박씨를 마당 양지바른 곳에 정성껏 심는다"
        },
        {
            "id": "act03_alt",
            "act": 3,
            "title": "오지 않는 제비",
            "speaker": "해설",
            "text": "봄이 오고 꽃이 피었으나, 제비는 흥부네 집을 찾지 않았습니다. 마당은 적막하고 찬 바람만 휑하니 돕니다.",
            "rle": act2_rle, # 쓸쓸한 회상
            "is_transition": True,
            "next": "act04_poor",
            "button_text": "비참한 현실을 깨닫고 눈물로 후회한다"
        },
        {
            "id": "act04",
            "act": 4,
            "title": "흥부의 박",
            "speaker": "흥부",
            "text": "여보! 지붕 위에 커다란 박이 보름달처럼 열렸소! 톱을 가져와 함께 당깁시다! 슬근슬근 톱질하세, 엉차! 엉차!",
            "rle": act4_rle,
            "is_transition": False,
            "choices": [
                {"text": "쏟아지는 금은보화를 가난한 이웃들과 나눈다", "delta": 2, "next": "act05", "feedback": "쩍 갈라진 박 속에서 번쩍이는 엽전과 은보화, 쌀알이 폭포수처럼 쏟아졌습니다! 흥부 부부는 춤을 추며 마을 사람들을 불렀습니다."},
                {"text": "혹시 모르니 곳간 깊숙이 잘 보관해둔다", "delta": 0, "next": "act05", "feedback": "산더미 같은 재물을 얻었으나, 흥부는 신중하게 문을 걸어 잠갔습니다."}
            ]
        },
        {
            "id": "act04_poor",
            "act": 4,
            "title": "가난의 굴레",
            "speaker": "흥부",
            "text": "지붕 위에는 빈 넝쿨만 마르고, 처자식의 배고픈 울음소리만 깊어갑니다. 자비를 베풀지 않았던 그 날이 뼈에 사무칩니다.",
            "rle": act1_rle,
            "is_transition": True,
            "next": "act07_poor",
            "button_text": "뒤늦은 깨달음을 얻으며 형을 찾아간다"
        },
        {
            "id": "act05",
            "act": 5,
            "title": "놀부의 욕심",
            "speaker": "놀부",
            "text": "뭐라?! 그 알거지 흥부 놈이 박을 타서 벼락부자가 되었다고?! 멀쩡한 제비 놈을 잡아다가 다리를 뚝 분질러서 나도 대박을 타야겠다!",
            "rle": act5_rle,
            "is_transition": True,
            "next": "act06",
            "button_text": "인과응보의 시간이 다가옵니다"
        },
        {
            "id": "act06",
            "act": 6,
            "title": "놀부의 박",
            "speaker": "도깨비",
            "text": "놀부 놀부 못된 놀부야! 죄 없는 미물을 해치고 탐욕을 부린 죗값을 받아라! 가시 쇠몽둥이 맛을 보아라, 철썩!!",
            "rle": act6_rle,
            "is_transition": True,
            "next": "act07",
            "button_text": "알거지가 되어 길바닥에 쫓겨난 놀부"
        },
        {
            "id": "act07",
            "act": 7,
            "title": "눈물의 화해",
            "speaker": "놀부",
            "text": "흥부야... 내가 천하의 몹쓸 놈이다... 네게 죄를 짓고 하늘의 벌을 받아 알거지가 되었구나... 날 용서하지 마라...",
            "rle": act7_rle,
            "is_transition": False,
            "choices": [
                {"text": "울며 형의 손을 굳게 잡고 품에 안아 용서한다", "delta": 3, "next": "ending", "feedback": "흥부는 버선발로 뛰어나와 엎드린 형을 부둥켜안고 통곡했습니다. '형님, 무슨 말씀이십니까! 우리는 한 피를 나눈 형제입니다!'"},
                {"text": "집과 양식은 내주되, 다시는 욕심부리지 말라 꾸짖는다", "delta": 1, "next": "ending", "feedback": "놀부는 고개를 숙이고 참회의 눈물을 흘리며 지난날의 악행을 뉘우쳤습니다."}
            ]
        },
        {
            "id": "act07_poor",
            "act": 7,
            "title": "빈손의 화해",
            "speaker": "흥부",
            "text": "부자가 되지는 못했으나, 욕심을 버리고 서로를 보듬는 법을 배웠습니다. 형제가 빈 마당에 마주 앉아 눈물을 흘립니다.",
            "rle": act7_rle,
            "is_transition": False,
            "choices": [
                {"text": "가난해도 우애를 지키며 함께 살아간다", "delta": 1, "next": "ending", "feedback": "재물은 없어도 형제의 우애는 금보다 단단해졌습니다."}
            ]
        }
    ]

    endings = [
        {"min": 8, "title": "성인군자의 반열 (최고 선행 엔딩)", "desc": "하늘을 감동시킨 지극한 자비와 우애로, 가난과 멸시를 이겨내고 온 나라에 덕망을 떨친 성인(聖人)의 경지에 올랐습니다."},
        {"min": 5, "title": "의좋은 형제 (정석 해피엔딩)", "desc": "미물을 아끼고 혈육의 정을 되살려, 부귀영화와 화목한 가정을 모두 지켜낸 따스한 결말을 맺었습니다."},
        {"min": 2, "title": "평범한 범부 (소시민 엔딩)", "desc": "큰 욕심도 큰 자비도 없이, 세상의 풍파 속에서 가족들의 생계를 지켜낸 소박한 결말입니다."},
        {"min": -99, "title": "깨달음의 길 (고난 극복 엔딩)", "desc": "가혹한 시련과 후회를 거쳐, 물질보다 소중한 양심과 진정한 형제애의 가치를 깨달았습니다."}
    ]

    palette_hex = [f"#{c[2][0]:02x}{c[2][1]:02x}{c[2][2]:02x}" for c in PALETTE_16]
    game_pack = {
        "palette": palette_hex,
        "scenes": scenes,
        "endings": endings
    }

    game_json = json.dumps(game_pack)

    html_app = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Divina Ludus — 흥부놀부전 (Tutorial Story Full Game)</title>
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
  .console-frame {{
    width: 860px;
    height: 820px;
    background: #1e1e1e;
    border: 3px solid #4a4a4a;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.9);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .console-header {{
    background: #2d2d2d;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #3a3a3a;
  }}
  .console-title {{ font-size: 15px; font-weight: bold; color: #ffcc99; }}
  .console-hud {{ font-size: 13px; color: #81d4fa; font-family: monospace; }}
  
  .canvas-container {{
    background: #0a0a0a;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
    border-bottom: 2px solid #333;
  }}
  canvas {{
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    width: 800px;
    height: 410px;
    background: #252525;
    border: 2px solid #444;
    box-shadow: 0 4px 15px rgba(0,0,0,0.7);
  }}
  
  .bottom-panel {{
    flex: 1;
    display: flex;
    padding: 14px 20px;
    gap: 16px;
    background: #181818;
  }}
  .dialogue-box {{
    flex: 6;
    background: #222;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .speaker {{
    font-size: 15px;
    font-weight: bold;
    color: #f4d03f;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .speaker::before {{ content: "◈"; color: #e74c3c; }}
  .dialogue-text {{
    font-size: 14px;
    line-height: 1.6;
    color: #ffffff;
    word-break: keep-all;
    min-height: 50px;
  }}
  
  .system-box {{
    flex: 4;
    background: #222;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .metric-label {{
    font-size: 13px;
    color: #aaa;
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
  }}
  .metric-track {{
    height: 12px;
    background: #333;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #555;
  }}
  .metric-fill {{
    height: 100%;
    width: 30%;
    background: linear-gradient(90deg, #27ae60, #2ecc71);
    transition: width 0.4s ease;
  }}
  .info-tag {{
    font-size: 12px;
    color: #888;
    line-height: 1.4;
  }}
  
  .choice-container {{
    padding: 0 20px 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: #181818;
  }}
  .choice-btn {{
    background: #2c3e50;
    color: #ecf0f1;
    border: 1px solid #34495e;
    padding: 11px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    transition: all 0.15s;
  }}
  .choice-btn:hover {{
    background: #34495e;
    border-color: #f39c12;
    color: #f1c40f;
    transform: translateX(4px);
  }}
</style>
</head>
<body>

<div class="console-frame">
  <div class="console-header">
    <div class="console-title" id="actTitle">◆ 흥부놀부전 · 튜토리얼 스토리 ◆</div>
    <div class="console-status" id="hudStatus">[Native 296x152 | 60FPS]</div>
  </div>

  <div class="canvas-container">
    <canvas id="retroCanvas" width="296" height="152"></canvas>
  </div>

  <div class="bottom-panel">
    <div class="dialogue-box">
      <div>
        <div class="speaker" id="speakerName">놀부</div>
        <div class="dialogue-text" id="dialogueText">대사 내용</div>
      </div>
      <div style="font-size: 12px; color: #888;" id="feedbackText">키보드 [1], [2] 키를 눌러 선택할 수 있습니다.</div>
    </div>
    <div class="system-box">
      <div>
        <div class="metric-label">
          <span>♧ 선행의 씨앗</span>
          <span id="metricVal">3 / 10</span>
        </div>
        <div class="metric-track">
          <div class="metric-fill" id="metricBar" style="width: 30%;"></div>
        </div>
      </div>
      <div class="info-tag">
        ◈ 모드: 튜토리얼 이야기<br>
        ◈ 해상도: 296x152 영화적 도트<br>
        ◈ 조작: 키보드 [1, 2, Enter]
      </div>
    </div>
  </div>

  <div class="choice-container" id="choiceBox"></div>
</div>

<script>
  const game = {game_json};
  const canvas = document.getElementById('retroCanvas');
  const ctx = canvas.getContext('2d');
  
  let curSceneIdx = 0;
  let curFrame = 0;
  let metricValue = 3;
  let isGameOver = false;

  function loadScene(idx) {{
    curSceneIdx = idx;
    curFrame = 0;
    const scene = game.scenes[curSceneIdx];
    
    document.getElementById('actTitle').innerText = `◆ 흥부놀부전 · 제${{scene.act}}막: ${{scene.title}} ◆`;
    document.getElementById('speakerName').innerText = scene.speaker;
    document.getElementById('dialogueText').innerText = scene.text;
    document.getElementById('feedbackText').innerText = scene.is_transition ? "진행하려면 [Enter] 키 또는 아래 버튼을 누르세요." : "키보드 [1], [2] 키로 선택하세요.";
    
    // 선택지 버튼 렌더링
    const box = document.getElementById('choiceBox');
    box.innerHTML = '';
    
    if (scene.is_transition) {{
      const btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.innerText = `▶ ${{scene.button_text}} [Enter]`;
      btn.onclick = () => advanceScene(scene.next, 0);
      box.appendChild(btn);
    }} else {{
      scene.choices.forEach((c, i) => {{
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.innerText = `[${{i+1}}] ${{c.text}} (${{c.delta >= 0 ? '+' + c.delta : c.delta}})`;
        btn.onclick = () => {{
          document.getElementById('dialogueText').innerText = c.feedback;
          setTimeout(() => advanceScene(c.next, c.delta), 900);
        }};
        box.appendChild(btn);
      }});
    }}
    renderFrame();
  }}

  function advanceScene(nextId, delta) {{
    metricValue = Math.max(0, Math.min(10, metricValue + delta));
    document.getElementById('metricVal').innerText = `${{metricValue}} / 10`;
    document.getElementById('metricBar').style.width = `${{metricValue * 10}}%`;
    
    if (nextId === 'ending') {{
      showEnding();
      return;
    }}
    
    const nextIdx = game.scenes.findIndex(s => s.id === nextId);
    if (nextIdx !== -1) {{
      loadScene(nextIdx);
    }}
  }}

  function showEnding() {{
    isGameOver = true;
    let matched = game.endings[game.endings.length - 1];
    for (let end of game.endings) {{
      if (metricValue >= end.min) {{
        matched = end;
        break;
      }}
    }}
    
    document.getElementById('actTitle').innerText = `◆ 흥부놀부전 완결 · 여정의 끝 ◆`;
    document.getElementById('speakerName').innerText = "결말 칭호: " + matched.title;
    document.getElementById('dialogueText').innerText = matched.desc;
    document.getElementById('feedbackText').innerText = `최종 선행의 씨앗: ${{metricValue}}/10 — 플레이해주셔서 감사합니다!`;
    
    const box = document.getElementById('choiceBox');
    box.innerHTML = '<button class="choice-btn" onclick="location.reload()">[처음부터 다시 시작하기 (R)]</button>';
  }}

  function renderFrame() {{
    const scene = game.scenes[curSceneIdx];
    const rleStr = scene.rle[curFrame];
    const imgData = ctx.createImageData(296, 152);
    
    const chunks = rleStr.split(',');
    let pIdx = 0;
    for (let i = 0; i < chunks.length; i++) {{
      const parts = chunks[i].split('_');
      const count = parseInt(parts[0]);
      const colorIdx = parseInt(parts[1]);
      
      const hex = game.palette[colorIdx];
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      
      for (let c = 0; c < count; c++) {{
        imgData.data[pIdx] = r;
        imgData.data[pIdx + 1] = g;
        imgData.data[pIdx + 2] = b;
        imgData.data[pIdx + 3] = 255;
        pIdx += 4;
      }}
    }}
    ctx.putImageData(imgData, 0, 0);
    
    const hud = document.getElementById('hudStatus');
    if (curFrame === 2) {{
      hud.innerText = `[제${{scene.act}}막 | ★ F3 핵심 감정/스파클 ★]`;
      hud.style.color = "#f4d03f";
    }} else {{
      hud.innerText = `[제${{scene.act}}막 | F${{curFrame+1}}/6 Native 296x152]`;
      hud.style.color = "#81d4fa";
    }}
  }}

  setInterval(() => {{
    const scene = game.scenes[curSceneIdx];
    curFrame = (curFrame + 1) % scene.rle.length;
    renderFrame();
  }}, 750);

  // 키보드 조작 체계 (1, 2, Enter, R)
  window.addEventListener('keydown', (e) => {{
    if (isGameOver) {{
      if (e.key === 'r' || e.key === 'R') location.reload();
      return;
    }}
    const scene = game.scenes[curSceneIdx];
    if (scene.is_transition) {{
      if (e.key === 'Enter' || e.code === 'Space') {{
        advanceScene(scene.next, 0);
      }}
    }} else {{
      if (e.key === '1') {{
        const c = scene.choices[0];
        document.getElementById('dialogueText').innerText = c.feedback;
        setTimeout(() => advanceScene(c.next, c.delta), 700);
      }} else if (e.key === '2' && scene.choices.length > 1) {{
        const c = scene.choices[1];
        document.getElementById('dialogueText').innerText = c.feedback;
        setTimeout(() => advanceScene(c.next, c.delta), 700);
      }}
    }}
  }});

  window.addEventListener('wheel', (e) => e.preventDefault(), {{ passive: false }});

  // 시작
  loadScene(0);
</script>

</body>
</html>
"""
    app_path = "/mnt/d/game/Divina_Console.html"
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(html_app)
        
    print(f"✅ 《흥부놀부전》 풀 스토리 정식 게임 완성 배포: {app_path}")

if __name__ == "__main__":
    build_game()
