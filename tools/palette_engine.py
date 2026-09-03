#!/usr/bin/env python3
"""
tools/palette_engine.py
Phase 2 고전 8비트 패미컴/PC-98 하프블록(Half-Block ▀) 컬러 도트 렌더러
배경색을 어두운 방(한옥 벽지 어두운 황토/남색 톤)으로 조정하여 칠흑 같은 갓(1번)과 완벽 분리!
"""

# 고전 16색 팔레트 정의 (인덱스: 0~15)
PALETTE_16 = [
    ("한옥벽배경", 237, (58, 58, 58)),     # 0: 갓(검정)과 분리되는 어두운 한옥 벽지 회갈색/차콜
    ("칠흑먹선", 16, (0, 0, 0)),           # 1: 칠흑 갓, 눈썹, 동공, 수염, 옷깃 먹선
    ("피부살구", 223, (255, 204, 153)),    # 2: 인물 밝은 피부톤
    ("피부음영", 179, (212, 155, 106)),    # 3: 콧날 음영, V라인 턱선, 다크서클
    ("누런삼베", 186, (194, 178, 128)),    # 4: 흥부 터진 갓, 삼베옷 바탕
    ("누더기갈색", 94, (139, 90, 43)),     # 5: 헝겊 기운 자국, 삼베 음영 주름
    ("비단주홍", 196, (231, 76, 60)),      # 6: 놀부 화려한 비단 깃
    ("비단군청", 25, (36, 113, 163)),      # 7: 놀부 비단 도포 메인
    ("눈물하늘", 81, (93, 173, 226)),      # 8: 흥부 눈물 방울
    ("순백반사", 231, (255, 255, 255)),    # 9: 흰자위, 비단 광택 하이라이트
    ("비단청록", 31, (0, 135, 175)),       # 10: 비단 주름 명암/광택 텍스처
    ("삼베거친음", 137, (175, 135, 95)),   # 11: 거친 삼베옷 격자 질감 픽셀
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

def calculate_frame_size(canvas_data):
    """
    고전 롬팩 기준 4비트 인덱스 팔레트(1바이트 2픽셀) RLE 압축 크기 및 날것(Raw) 크기 계산
    """
    total_pixels = len(canvas_data) * len(canvas_data[0])
    # 4-bit Indexed Color: 1바이트에 2픽셀 저장 (고전 롬팩 표준 포맷)
    raw_bytes = total_pixels // 2
    
    # RLE (Run-Length Encoding) 압축 시뮬레이션
    flat = [pixel for row in canvas_data for pixel in row]
    rle_chunks = []
    curr_pixel = flat[0]
    curr_len = 1
    for p in flat[1:]:
        if p == curr_pixel and curr_len < 15: # 4비트 카운트 (최대 15)
            curr_len += 1
        else:
            rle_chunks.append((curr_pixel, curr_len)) # (4비트 색상 + 4비트 길이 = 1바이트)
            curr_pixel = p
            curr_len = 1
    rle_chunks.append((curr_pixel, curr_len))
    rle_bytes = len(rle_chunks) # 1청크당 1바이트
    
    return raw_bytes, rle_bytes
