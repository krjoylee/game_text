#!/usr/bin/env python3
"""
tools/export_act1_to_yaml.py
확정된 16색 하이브리드 도트 모션(6프레임)을 
packs/heungbu_nolbu/4_game_scene.yaml의 act01_scene_01에 주입하는 변환 스크립트
"""

import sys
import yaml

sys.path.append("/home/krjoylee/code/game/tools")
from generate_act1_motion_prototype import generate_6_motion_frames, render_half_block_canvas

def export_to_yaml():
    frames_data = generate_6_motion_frames()
    yaml_frames = []
    
    for fr in frames_data:
        # 19줄의 하프블록 텍스트 획득
        lines_19 = render_half_block_canvas(fr)
        
        # 23줄 규격에 맞추기 위해 상단 2줄, 하단 2줄 빈 배경 패딩
        empty_bg_line = "\x1b[38;5;237;48;5;237m" + "▀" * 74 + "\x1b[0m"
        frame_23 = [empty_bg_line, empty_bg_line] + lines_19 + [empty_bg_line, empty_bg_line]
        yaml_frames.append(frame_23)
        
    yaml_path = "/home/krjoylee/code/game/packs/heungbu_nolbu/4_game_scene.yaml"
    with open(yaml_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Python yaml을 쓰면 주석이 날아갈 수 있으므로 정밀 치환
    # animation 블록 치환
    import re
    
    # 6개 프레임의 YAML 블록 텍스트 생성
    anim_yaml_lines = ["    animation:", "      frame_rate_ms: 750", "      loop: false", "      frames:"]
    for f_idx, fr in enumerate(yaml_frames, 1):
        anim_yaml_lines.append(f"        # Frame {f_idx}")
        anim_yaml_lines.append("        - [")
        for line in fr:
            # YAML 문자열 이스케이프
            escaped_line = line.replace('"', '\\"')
            anim_yaml_lines.append(f'            "{escaped_line}",')
        anim_yaml_lines.append("          ]")
        
    anim_replacement = "\n".join(anim_yaml_lines)
    
    # regex로 act01_scene_01의 animation: ... choices: 전까지 치환
    pattern = r"(  - scene_id: \"act01_scene_01\"[\s\S]*?is_interpreted: false\n\n)(    animation:[\s\S]*?)(    choices:)"
    
    match = re.search(pattern, content)
    if not match:
        print("❌ 정규식 매칭 실패!")
        return False
        
    new_content = content[:match.start(2)] + anim_replacement + "\n\n" + content[match.start(3):]
    
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("✅ act01_scene_01 16색 하이브리드 컬러 애니메이션 주입 성공!")
    return True

if __name__ == "__main__":
    export_to_yaml()
