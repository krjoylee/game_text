#!/usr/bin/env python3
"""
tools/apply_balanced_packs.py
모든 팩의 분기 이벤트 선택지 델타(+1, -1) 표준화 및 티어별 맥스/엔딩 컷오프 수학적 일치
"""

import sys
import re

# 1. make_expanded_data.py 수정
with open("/home/krjoylee/code/game/tools/make_expanded_data.py") as f:
    text = f.read()

# Replace any (+2), (+3), (-2), (-3) in choices with (+1) and (-1) or (0)
# Use regex to normalize choice deltas
# Matches tuple: ("text", delta)
def norm_choice(m):
    txt = m.group(1)
    val = int(m.group(2))
    new_val = 1 if val > 0 else (-1 if val < 0 else 0)
    return f'("{txt}", {new_val})'

text = re.sub(r'\("([^"]+)",\s*(-?\d+)\)', norm_choice, text)

# Update ending thresholds in make_expanded_data.py
# Medium (15 scenes): Max 14 -> Ending A: 11, Ending B: 7, Ending C: -99
text = re.sub(r'\{"min":\s*\d+,\s*"title":\s*"([^"]+)",\s*"desc":\s*"([^"]+)"\}', lambda m: m.group(0), text)

# Explicitly replace thresholds for medium and hard in make_expanded_data.py:
# Charlie (10 scenes, 7 choices) -> Max 10 -> min 8, min 5
# Matilda (10 scenes, 7 choices) -> Max 10 -> min 8, min 5
# Animal Farm (15 scenes, 11 choices) -> Max 14 -> min 11, min 7
text = text.replace('"min": 16, "title": "깨어있는 역사의 감시자"', '"min": 11, "title": "깨어있는 역사의 감시자"')
text = text.replace('"min": 10, "title": "고뇌하는 농장의 관찰자"', '"min": 7, "title": "고뇌하는 농장의 관찰자"')

# 1984 (15 scenes, 11 choices) -> Max 14 -> min 11, min 7
text = text.replace('"min": 16, "title": "불멸하는 정신의 수호자"', '"min": 11, "title": "불멸하는 정신의 수호자"')
text = text.replace('"min": 10, "title": "고뇌하는 저항자"', '"min": 7, "title": "고뇌하는 저항자"')

# Under Wheel (15 scenes, 11 choices) -> Max 14 -> min 11, min 7
text = text.replace('"min": 16, "title": "수레바퀴를 벗어난 자유로운 영혼"', '"min": 11, "title": "수레바퀴를 벗어난 자유로운 영혼"')
text = text.replace('"min": 10, "title": "상처 입은 시인"', '"min": 7, "title": "상처 입은 시인"')

# Dante Comedy (20 scenes, 14 choices) -> Max 17 -> min 13, min 8
text = text.replace('"min": 22, "title": "천상의 빛과 합일한 성스러운 대시인"', '"min": 13, "title": "천상의 빛과 합일한 성스러운 대시인"')
text = text.replace('"min": 14, "title": "연옥을 넘어선 순례자"', '"min": 8, "title": "연옥을 넘어선 순례자"')

# Zarathustra (20 scenes, 14 choices) -> Max 17 -> min 13, min 8
text = text.replace('"min": 22, "title": "영원을 긍정하는 위버멘쉬 (초인)"', '"min": 13, "title": "영원을 긍정하는 위버멘쉬 (초인)"')
text = text.replace('"min": 14, "title": "포효하는 자유의 사자"', '"min": 8, "title": "포효하는 자유의 사자"')

with open("/home/krjoylee/code/game/tools/make_expanded_data.py", "w") as f:
    f.write(text)

print("make_expanded_data.py normalized!")

# 2. build_master_game.py 수정
with open("/home/krjoylee/code/game/tools/build_master_game.py") as f:
    btext = f.read()

# Normalize choices in peach, heungbu, demian
btext = re.sub(r'\{"text":\s*"([^"]+)",\s*"delta":\s*(-?\d+),\s*"feedback":\s*"([^"]+)"\}',
               lambda m: f'{{"text": "{m.group(1)}", "delta": {1 if int(m.group(2))>0 else (-1 if int(m.group(2))<0 else 0)}, "feedback": "{m.group(3)}"}}',
               btext)

# Update demian endings to 11 / 7
btext = btext.replace('"min": 16, "title": "아브락사스에 도달한 자"', '"min": 11, "title": "아브락사스에 도달한 자"')
btext = btext.replace('"min": 10, "title": "표식을 지닌 자 (카인의 후예)"', '"min": 7, "title": "표식을 지닌 자 (카인의 후예)"')

# Update getMaxScoreForPack:
# 10막: Max 10 (시작 3 + 선택 7)
# 15막: Max 14 (시작 3 + 선택 11)
# 20막: Max 17 (시작 3 + 선택 14)
old_get_max = """  function getMaxScoreForPack(pack) {{
    if (!pack) return 10;
    if (pack.scenes.length >= 20) return 25;
    if (pack.scenes.length >= 15) return 18;
    return 10;
  }}"""

new_get_max = """  function getMaxScoreForPack(pack) {{
    if (!pack) return 10;
    if (pack.scenes.length >= 20) return 17;
    if (pack.scenes.length >= 15) return 14;
    return 10;
  }}"""

btext = btext.replace(old_get_max, new_get_max)

with open("/home/krjoylee/code/game/tools/build_master_game.py", "w") as f:
    f.write(btext)

print("build_master_game.py normalized!")
