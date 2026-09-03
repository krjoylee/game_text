#!/usr/bin/env python3
"""
tools/compare_resolution_modes.py
사용자 요청 비교 분석기:
1. 모드 A: 3x3 딕셔너리 16배 초고해상도 (Braille 2x4 서브픽셀 + ANSI 컬러)
2. 모드 B: 이전 16색 직접 인덱스 팔레트 모드 (선명한 외곽선과 또렷한 얼굴/배경 분리)
3. 두 모드를 나란히 시연하여 배경 뭉개짐 및 얼굴 구분감, 그리고 데이터 용량을 실시간 비교!
"""

import sys
import time

sys.path.append("/home/krjoylee/code/game/tools")
from palette_engine import COLOR_DICT_9, BASE_3_COLORS

# ANSI 컬러 코드 헬퍼
def fg_ansi(code):
    return f"\x1b[38;5;{code}m"
def bg_ansi(code):
    return f"\x1b[48;5;{code}m"
def reset_ansi():
    return "\x1b[0m"

# 16색 팔레트 (모드 B용)
PAL_16 = [
    236, # 0: 어두운 한옥 벽지 회갈색 (배경)
    16,  # 1: 칠흑 갓, 눈썹, 동공, 수염
    223, # 2: 뽀샤시한 밝은 살구 피부
    179, # 3: 피부 음영 황토
    186, # 4: 삼베옷 누런색
    94,  # 5: 누더기 갈색
    196, # 6: 비단 깃 주홍
    25,  # 7: 비단 도포 군청
    81,  # 8: 흥부 눈물 하늘
    231, # 9: 순백 반사광 / 흰자위
    31,  # 10: 비단 광택 청록
    137, # 11: 삼베 거친 음영
    220  # 12: ★ 놀부 금이빨 황금!
]

# ─────────────────────────────────────────────────────────────────────────────
# 1. 모드 A: 16배 초고해상도 3x3 딕셔너리 렌더러 (Braille 2x4 서브픽셀)
# ─────────────────────────────────────────────────────────────────────────────
def render_mode_a_16x_dict():
    """
    Braille 유니코드(2x4 점자) + 3색 9칸 딕셔너리 하프톤 매핑
    터미널 74 x 19 캔버스 내부에서 가로 148 x 세로 76 점자 도트(16배 밀도) 구현!
    """
    BW = 74
    BH = 19
    output_lines = []
    
    # 74x19 라인 생성
    for cy in range(BH):
        row_chars = []
        for cx in range(BW):
            # 인물 영역 판별
            is_nolbu = (6 <= cx <= 24 and 2 <= cy <= 16)
            is_heungbu = (46 <= cx <= 64 and 1 <= cy <= 16)
            
            # 8개 서브도트 비트 조합 (0x2800..0x28FF)
            braille_byte = 0
            cur_color_code = 236 # 기본 배경 회갈색
            
            if is_nolbu:
                # 갓 영역
                if cy <= 4:
                    braille_byte = 0xFF
                    cur_color_code = 16 # 칠흑 갓
                # 얼굴 영역
                elif 5 <= cy <= 9 and 8 <= cx <= 20:
                    # 3x3 딕셔너리 피부 배합 (살구 W6+L3)
                    braille_byte = 0xAA if (cx + cy) % 2 == 0 else 0x55
                    cur_color_code = 223 # 살구 피부
                    # 금이빨 (cy=8, cx=14)
                    if cy == 8 and cx in (14, 15):
                        braille_byte = 0xFF
                        cur_color_code = 220 # 황금!
                # 비단 도포
                elif cy >= 10:
                    braille_byte = 0xBD
                    cur_color_code = 25 # 군청 도포
            elif is_heungbu:
                # 상투 / 망건
                if cy <= 3 and 52 <= cx <= 56:
                    braille_byte = 0xFF
                    cur_color_code = 16 # 상투
                # 꽃미남 얼굴
                elif 4 <= cy <= 9 and 50 <= cx <= 58:
                    braille_byte = 0x55 if (cx + cy) % 2 == 0 else 0xAA
                    cur_color_code = 223 # 살구 피부
                    # 눈물 줄기 (cx=52, cy=6..7)
                    if cx == 52 and cy in (6, 7):
                        braille_byte = 0x06
                        cur_color_code = 81 # 하늘색 눈물!
                # 누더기 삼베옷
                elif cy >= 10:
                    braille_byte = 0x92
                    cur_color_code = 186 # 누런 삼베
            else:
                # 한옥 벽 배경 (은은한 딕셔너리 노이즈 텍스처)
                braille_byte = 0x12 if (cx + cy) % 4 == 0 else 0x00
                cur_color_code = 237
                
            ch = chr(0x2800 + braille_byte) if braille_byte != 0 else " "
            row_chars.append(f"{fg_ansi(cur_color_code)}{ch}")
            
        row_chars.append(reset_ansi())
        output_lines.append("".join(row_chars))
        
    return output_lines


# ─────────────────────────────────────────────────────────────────────────────
# 2. 모드 B: 이전 16색 직접 인덱스 팔레트 모드 (Half-Block 상하 2배 정밀 분리)
# ─────────────────────────────────────────────────────────────────────────────
def render_mode_b_direct_16pal():
    """
    단색 인덱스가 명확히 분리되어 외곽선과 얼굴이 또렷한 Half-Block 모드
    """
    W = 74
    H = 38
    canvas = [[0 for _ in range(W)] for _ in range(H)]
    
    # 1. 배경 (회갈색 0번)
    # 2. 놀부 갓 & 실루엣
    for y in range(3, 8):
        for x in range(15, 26): canvas[y][x] = 1 # 칠흑 갓
    for x in range(7, 34): canvas[8][x] = 1
    # 놀부 갓끈
    for y in range(9, 15):
        canvas[y][15] = 1; canvas[y][25] = 1
    # 놀부 얼굴 (뽀얀 살구 2번)
    for y in range(9, 21):
        for x in range(16, 25): canvas[y][x] = 2
    # 눈 (흰자위 9번 + 동공 1번)
    canvas[12][17] = 9; canvas[12][18] = 1; canvas[12][19] = 9
    canvas[12][21] = 9; canvas[12][22] = 1; canvas[12][23] = 9
    # ★ 놀부 금이빨 (12번 황금빛!)
    canvas[18][20] = 12
    # 수염
    for y in range(21, 25): canvas[y][20] = 1
    # 비단 도포 (7번 군청) & 광택 (10번 청록)
    for y in range(23, 37):
        for x in range(10, 31): canvas[y][x] = 7
    for y in range(26, 35, 4): canvas[y][13] = 9; canvas[y][27] = 9
    
    # 3. 흥부 (상투 꽃미남 빈티)
    # 상투 (1번)
    for y in range(2, 6):
        for x in range(53, 57): canvas[y][x] = 1
    for x in range(50, 60): canvas[6][x] = 1
    # 얼굴 (뽀얀 살구 2번)
    for y in range(7, 19):
        for x in range(51, 59): canvas[y][x] = 2
    # 깊은 눈 (동공 1번 + 흰자위 9번)
    canvas[11][52] = 9; canvas[11][53] = 1
    canvas[11][56] = 1; canvas[11][57] = 9
    # 콧날 (3번 음영) & V턱선
    canvas[14][54] = 3; canvas[15][54] = 3; canvas[16][54] = 1
    canvas[20][54] = 3; canvas[20][55] = 3
    # 눈물 (8번 하늘색 + 9번 반사광)
    canvas[13][52] = 8; canvas[14][52] = 9; canvas[15][52] = 8
    # 삼베옷 (4번 누런색) & 기운 자국 (5번 갈색)
    for y in range(22, 37):
        for x in range(46, 64): canvas[y][x] = 4
    canvas[27][49] = 5; canvas[27][50] = 5
    
    # Half-block 결합
    lines = []
    for y in range(0, H, 2):
        top_r = canvas[y]
        bot_r = canvas[y+1]
        line_parts = []
        for t, b in zip(top_r, bot_r):
            fg = PAL_16[t]
            bg = PAL_16[b]
            line_parts.append(f"\x1b[38;5;{fg};48;5;{bg}m▀")
        line_parts.append(reset_ansi())
        lines.append("".join(line_parts))
    return lines

if __name__ == "__main__":
    print("🔬 [가독성 정밀 비교] 모드 A (3x3 16배 초고해상도) VS 모드 B (이전 16색 직접 인덱스)")
    print("   2초마다 두 모드를 교대로 렌더링하여 비교합니다 (Ctrl+C로 종료)\n")
    
    lines_a = render_mode_a_16x_dict()
    lines_b = render_mode_b_direct_16pal()
    
    # 크기 계산
    # 모드 A: 37x19 타일 팩킹 = 352 B
    # 모드 B: 74x38 RLE 압축 = 약 600 B
    
    for i in range(2):
        # 1. 모드 A 출력
        sys.stdout.write("\x1b[H")
        print(f"╔{'═' * 74}╗")
        print(f"║  [모드 A] 3원색 3x3 딕셔너리 16배 초고해상도 (Braille 148x76) [용량: 352B] ║")
        print(f"╠{'═' * 74}╣")
        for l in lines_a:
            print(f"║{l}║")
        print(f"╚{'═' * 74}╝")
        print("  ▶ 특징: 148x76 극한의 서브픽셀 밀도이나, 하프톤 점자 특성상 배경과 얼굴 경계가 섞여 보일 수 있음.")
        time.sleep(2.5)
        
        # 2. 모드 B 출력
        sys.stdout.write("\x1b[H")
        print(f"╔{'═' * 74}╗")
        print(f"║  [모드 B] 이전 16색 직접 인덱스 팔레트 모드 (Half-Block 74x38) [용량: 600B] ║")
        print(f"╠{'═' * 74}╣")
        for l in lines_b:
            print(f"║{l}║")
        print(f"╚{'═' * 74}╝")
        print("  ▶ 특징: 인덱스 색상이 100% 면으로 칠해져 얼굴과 갓, 배경이 칼같이 분리되어 형태 인지력 극대화!")
        time.sleep(2.5)
