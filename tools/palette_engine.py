#!/usr/bin/env python3
"""
tools/palette_engine.py
Phase 2 고전 8비트 기법:
1. 16색 기본 팔레트
2. 3x3 딕셔너리 하프톤 디더링 패턴(Pattern Dithering Dictionary):
   - 적은 수의 기본 인덱스(RGB/CMY)를 3x3 격자(9칸) 비율로 믹싱하여 수십 가지 풍부한 중간색(피부 중간톤, 비단 그라데이션) 합성!
3. VRAM 용량 압축:
   - 9칸 전체를 일일이 저장하지 않고 "패턴 ID(1바이트)"만 저장 ➔ 4배 고해상도에서도 데이터 용량을 1/4~1/2로 수직 압축!
"""

# 고전 기본 팔레트 (인덱스: 0~15)
PALETTE_16 = [
    ("한옥벽배경", 237, (58, 58, 58)),     # 0: 어두운 한옥 벽지 회갈색
    ("칠흑먹선", 16, (0, 0, 0)),           # 1: 칠흑 갓, 눈썹, 동공, 수염
    ("피부살구", 223, (255, 204, 153)),    # 2: 인물 밝은 피부톤
    ("피부황토", 179, (212, 155, 106)),    # 3: 피부 음영, 콧대, 턱선
    ("누런삼베", 186, (194, 178, 128)),    # 4: 흥부 터진 갓, 삼베옷 바탕
    ("누더기갈색", 94, (139, 90, 43)),     # 5: 헝겊 기운 자국, 삼베 주름
    ("비단주홍", 196, (231, 76, 60)),      # 6: 놀부 화려한 비단 깃
    ("비단군청", 25, (36, 113, 163)),      # 7: 놀부 비단 도포 메인
    ("눈물하늘", 81, (93, 173, 226)),      # 8: 흥부 눈물 방울
    ("순백반사", 231, (255, 255, 255)),    # 9: 흰자위, 비단 광택 하이라이트
    ("비단청록", 31, (0, 135, 175)),       # 10: 비단 주름 광택
    ("삼베거친음", 137, (175, 135, 95)),   # 11: 거친 삼베옷 격자 질감
    ("황금빛", 220, (244, 208, 63)),       # 12: ★ 놀부 금이빨 황금 픽셀!
    ("도깨비녹", 36, (22, 160, 133)),      # 13
    ("쇠몽둥이", 244, (128, 139, 150)),    # 14
    ("화해들판", 41, (46, 204, 113)),      # 15
]

# ─────────────────────────────────────────────────────────────────────────────
# 3x3 하프톤 딕셔너리 패턴 (Color Mixing Dictionary)
# 9칸 안에 색상 A와 B를 채워 새로운 혼합색(중간톤)을 만들어내는 매트릭스
# ─────────────────────────────────────────────────────────────────────────────
PATTERN_3X3 = {
    # 순수 단색 패턴 (9칸 전체가 A)
    "SOLID_A": [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ],
    # A와 B가 50:50으로 교차 믹싱되는 체커보드 패턴 (자연스러운 중간색 합성)
    "MIX_50": [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ],
    # 75% A + 25% B (밝은 광택/하이라이트)
    "MIX_75": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    # 25% A + 75% B (짙은 그림자 음영)
    "MIX_25": [
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0]
    ],
    # 빗살무늬 비단 결 텍스처
    "SILK_STRIPE": [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
}

def get_mixed_color_block(color_a, color_b, pattern_name, px, py):
    """
    (px, py) 좌표에 대해 3x3 딕셔너리 패턴을 반복 타일링하여 
    색상 A와 색상 B의 합성 픽셀 색상을 반환
    """
    pat = PATTERN_3X3.get(pattern_name, PATTERN_3X3["SOLID_A"])
    mask_val = pat[py % 3][px % 3]
    return color_a if mask_val == 1 else color_b

def get_ansi_color(fg_idx, bg_idx):
    fg_code = PALETTE_16[fg_idx][1]
    bg_code = PALETTE_16[bg_idx][1]
    return f"\x1b[38;5;{fg_code};48;5;{bg_code}m"

def ansi_reset():
    return "\x1b[0m"

def render_half_block_canvas(pixel_grid_2x):
    canvas_h = len(pixel_grid_2x)
    canvas_w = len(pixel_grid_2x[0])
    lines = []
    
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

def calculate_pattern_compressed_size(canvas_data):
    """
    3x3 패턴 딕셔너리 기반 압축 용량 계산:
    - 픽셀 9개를 9바이트로 저장하지 않고, 
    - [패턴ID(4비트) + 색상A(4비트) + 색상B(4비트) = 총 12비트(1.5바이트)]로 3x3 타일을 압축 저장!
    ➔ 9픽셀당 1.5바이트 = 픽셀당 불과 0.16바이트! (기존 대비 1/3 수준으로 극단 압축)
    """
    h = len(canvas_data)
    w = len(canvas_data[0])
    tile_w = (w + 2) // 3
    tile_h = (h + 2) // 3
    total_tiles = tile_w * tile_h
    
    # 1타일당 1.5바이트 (12비트 메타데이터)
    pattern_bytes = int(total_tiles * 1.5)
    return pattern_bytes
