#!/usr/bin/env python3
"""
tools/palette_engine.py
Phase 2 고전 8비트 패미컴/게임보이 하프블록(Half-Block ▀, ▄) 컬러 도트 렌더러!

핵심 원리:
- 터미널 1문자 공간(가로 1칸, 세로 2줄 분량)을 위쪽 픽셀(Top)과 아래쪽 픽셀(Bottom)로 분할!
- 문자 '▀'(상단 블록): 전경색은 위 픽셀 색, 배경색은 아래 픽셀 색!
- 결과: 가로 74 x 세로 38의 초밀도 8비트 고전 컬러 도트 구현 (눈동자, 콧날, 금이빨의 1px 미세 묘사 완벽 복원!)
"""

# 고전 16색 팔레트 정의 (인덱스: 0~15)
PALETTE_16 = [
    ("배경암흑", 233, (18, 18, 18)),       # 0: 어두운 방/배경
    ("외곽선먹선", 16, (0, 0, 0)),          # 1: 칠흑 갓, 눈썹, 동공, 수염
    ("피부살구", 223, (255, 204, 153)),    # 2: 인물 밝은 피부톤
    ("피부음영", 179, (212, 155, 106)),    # 3: 콧날 음영, V라인 턱선, 다크서클
    ("누런삼베", 186, (194, 178, 128)),    # 4: 흥부 터진 갓, 삼베옷
    ("누더기갈색", 94, (139, 90, 43)),     # 5: 헝겊 기운 자국
    ("비단주홍", 196, (231, 76, 60)),      # 6: 놀부 화려한 깃
    ("비단군청", 32, (41, 128, 185)),      # 7: 놀부 비단 도포
    ("눈물하늘", 81, (93, 173, 226)),      # 8: 흥부 눈물 방울
    ("순백반사", 231, (255, 255, 255)),    # 9: 흰자위, 반짝광
    ("제비흑청", 236, (28, 40, 51)),       # 10
    ("제비다홍", 203, (231, 76, 60)),      # 11
    ("황금빛", 220, (244, 208, 63)),       # 12: ★ 놀부 번쩍이는 금이빨!
    ("도깨비녹", 36, (22, 160, 133)),      # 13
    ("쇠몽둥이", 244, (128, 139, 150)),    # 14
    ("화해들판", 41, (46, 204, 113)),      # 15
]

def get_ansi_color(fg_idx, bg_idx):
    """상단 픽셀(전경)과 하단 픽셀(배경)의 결합 ANSI 코드"""
    fg_code = PALETTE_16[fg_idx][1]
    bg_code = PALETTE_16[bg_idx][1]
    return f"\x1b[38;5;{fg_code};48;5;{bg_code}m"

def ansi_reset():
    return "\x1b[0m"

def render_half_block_canvas(pixel_grid_2x):
    """
    pixel_grid_2x: 가로 W, 세로 H*2 크기의 2차원 컬러 인덱스 배열
    출력: 터미널 H줄의 '▀' 블록 라인 리스트
    """
    canvas_h = len(pixel_grid_2x)
    canvas_w = len(pixel_grid_2x[0])
    lines = []
    
    # 2줄씩 묶어서 1문자 줄로 렌더링
    for y in range(0, canvas_h, 2):
        top_row = pixel_grid_2x[y]
        bot_row = pixel_grid_2x[y + 1] if y + 1 < canvas_h else [0] * canvas_w
        
        line_parts = []
        cur_fg = -1
        cur_bg = -1
        for x in range(canvas_w):
            c_top = top_row[x]
            c_bot = bot_row[x]
            if c_top != cur_fg or c_bot != cur_bg:
                line_parts.append(get_ansi_color(c_top, c_bot))
                cur_fg = c_top
                cur_bg = c_bot
            line_parts.append("▀")
        line_parts.append(ansi_reset())
        lines.append("".join(line_parts))
        
    return lines

if __name__ == "__main__":
    print("🎨 고전 8비트 하프블록 16색 팔레트 테스트:")
    for idx, (name, code, rgb) in enumerate(PALETTE_16):
        print(f" {get_ansi_color(idx, 0)}▀▀{ansi_reset()} {name:<8} (Index: {idx:2d})")
