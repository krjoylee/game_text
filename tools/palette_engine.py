#!/usr/bin/env python3
"""
tools/palette_engine.py
Phase 2 고전 16색 인덱스 팔레트 및 ANSI 256/16색 터미널 렌더러
"""

# 고전 16색 팔레트 정의 (인덱스: 0~15)
# (이름, ANSI 컬러 코드, RGB 튜플)
PALETTE_16 = [
    ("투명/배경", 0, (0, 0, 0)),         # 0
    ("먹선/갓", 232, (26, 26, 26)),      # 1
    ("피부살구", 223, (255, 204, 153)),   # 2
    ("피부황토", 179, (212, 155, 106)),   # 3
    ("패랭이누런", 186, (194, 178, 128)), # 4
    ("누더기갈색", 94, (139, 90, 43)),    # 5
    ("비단주홍", 160, (192, 57, 43)),     # 6 (놀부 깃)
    ("비단군청", 25, (36, 113, 163)),     # 7 (놀부 도포)
    ("눈물하늘", 75, (93, 173, 226)),     # 8 (흥부 눈물)
    ("순백색", 231, (255, 255, 255)),     # 9 (흰자위, 반사광)
    ("제비흑청", 236, (28, 40, 51)),      # 10
    ("제비붉은", 196, (231, 76, 60)),     # 11
    ("황금빛", 220, (244, 208, 63)),      # 12 (놀부 금이빨!)
    ("도깨비녹", 36, (22, 160, 133)),     # 13
    ("쇠몽둥이회", 242, (86, 101, 115)),  # 14
    ("잔디녹색", 35, (39, 174, 96)),      # 15
]

def ansi_fg(color_idx):
    """팔레트 인덱스로 전경색 ANSI 코드 생성"""
    if color_idx == 0:
        return "\x1b[30m"
    ansi_code = PALETTE_16[color_idx][1]
    return f"\x1b[38;5;{ansi_code}m"

def ansi_reset():
    return "\x1b[0m"

def render_color_grid(grid, char_map=None):
    """
    grid: 2D array of (color_idx, char) or color_idx
    """
    output = []
    for row in grid:
        line_str = []
        cur_color = -1
        for cell in row:
            if isinstance(cell, tuple):
                c_idx, ch = cell
            else:
                c_idx = cell
                ch = char_map.get(c_idx, "█") if char_map else "█"
                
            if c_idx != cur_color:
                line_str.append(ansi_fg(c_idx))
                cur_color = c_idx
            line_str.append(ch)
        line_str.append(ansi_reset())
        output.append("".join(line_str))
    return output

if __name__ == "__main__":
    print("🎨 16색 인덱스 팔레트 프리뷰:")
    for idx, (name, ansi_code, rgb) in enumerate(PALETTE_16):
        print(f" {ansi_fg(idx)}██ {name:<10} (Index: {idx:2d}, ANSI: {ansi_code:3d}){ansi_reset()}")
