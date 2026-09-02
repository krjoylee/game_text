#!/usr/bin/env python3
"""
AsciiArt Studio (아스키아트 스튜디오) — 단일 실행 이미지 ➔ 74x23 아스키/도트 아트 변환 엔진
기능:
1. Block 모드 (1x1 기본 명암)
2. Half-Block 모드 (상하 2배 서브픽셀: 74 x 46 도트)
3. Braille 모드 (상하 4배 x 좌우 2배 = 8배 초고해상도 도트: 148 x 92 픽셀)
4. Character Portrait (인물 흉상/외형 프리셋 생성)
"""

import sys
import os
import math
import argparse

CANVAS_WIDTH = 74
CANVAS_HEIGHT = 23

# 고밀도 블록 명암 램프 (어두움 -> 밝음)
RAMP_BLOCK = ["█", "▓", "▒", "░", "■", "▫", "·", " "]
RAMP_ASCII = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

class ImageDecoder:
    """Zero-dependency BMP / PPM / PGM 이미지 디코더"""
    @staticmethod
    def load(path):
        ext = os.path.splitext(path)[1].lower()
        with open(path, "rb") as f:
            data = f.read()

        if ext == ".bmp" or data.startswith(b"BM"):
            return ImageDecoder._decode_bmp(data)
        elif ext in [".ppm", ".pgm", ".pbm"] or data.startswith(b"P"):
            return ImageDecoder._decode_pnm(data)
        else:
            raise ValueError(f"지원하지 않는 포맷입니다 (BMP 또는 PPM 권장): {ext}")

    @staticmethod
    def _decode_bmp(data):
        import struct
        file_header = data[:14]
        dib_header = data[14:54]
        offset = struct.unpack("<I", file_header[10:14])[0]
        width, height, planes, bpp, compression = struct.unpack("<iiHHII", dib_header[4:24])

        is_top_down = height < 0
        height = abs(height)

        if bpp not in [24, 32]:
            raise ValueError(f"24bit 또는 32bit BMP만 지원합니다 (현재: {bpp}bit)")

        row_size = ((bpp * width + 31) // 32) * 4
        pixels = []

        bytes_per_pixel = bpp // 8
        for y in range(height):
            actual_y = y if is_top_down else (height - 1 - y)
            row_start = offset + actual_y * row_size
            row = []
            for x in range(width):
                px_idx = row_start + x * bytes_per_pixel
                b = data[px_idx]
                g = data[px_idx + 1]
                r = data[px_idx + 2]
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                row.append(gray)
            pixels.append(row)

        return width, height, pixels

    @staticmethod
    def _decode_pnm(data):
        header = []
        idx = 0
        while len(header) < 4:
            if idx < len(data) and chr(data[idx]) == '#':
                while idx < len(data) and data[idx] != 10:
                    idx += 1
                idx += 1
                continue

            token = b""
            while idx < len(data) and chr(data[idx]).isspace():
                idx += 1
            while idx < len(data) and not chr(data[idx]).isspace():
                token += bytes([data[idx]])
                idx += 1
            if token:
                header.append(token.decode("latin1"))

        p_type, width_s, height_s, max_val_s = header
        width, height, max_val = int(width_s), int(height_s), int(max_val_s)
        while idx < len(data) and chr(data[idx]).isspace():
            idx += 1

        pixels = []
        if p_type == "P2":
            tokens = data[idx:].decode("latin1").split()
            tok_idx = 0
            for y in range(height):
                row = []
                for x in range(width):
                    if tok_idx < len(tokens):
                        val = int(int(tokens[tok_idx]) * 255 / max_val)
                        row.append(max(0, min(255, val)))
                        tok_idx += 1
                    else:
                        row.append(0)
                pixels.append(row)
        elif p_type == "P5":
            for y in range(height):
                row = []
                for x in range(width):
                    row.append(data[idx])
                    idx += 1
                pixels.append(row)
        elif p_type == "P6":
            for y in range(height):
                row = []
                for x in range(width):
                    r, g, b = data[idx], data[idx+1], data[idx+2]
                    idx += 3
                    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                    row.append(gray)
                pixels.append(row)
        else:
            raise ValueError(f"지원하지 않는 PNM 타입: {p_type}")

        return width, height, pixels


def resize_bilinear(src_pixels, src_w, src_h, dst_w, dst_h):
    """쌍선형 보간 리사이징"""
    dst_pixels = []
    x_ratio = float(src_w - 1) / dst_w if dst_w > 0 else 0
    y_ratio = float(src_h - 1) / dst_h if dst_h > 0 else 0

    for i in range(dst_h):
        row = []
        for j in range(dst_w):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            x_diff = (x_ratio * j) - x
            y_diff = (y_ratio * i) - y

            a = src_pixels[y][x]
            b = src_pixels[y][min(x + 1, src_w - 1)]
            c = src_pixels[min(y + 1, src_h - 1)][x]
            d = src_pixels[min(y + 1, src_h - 1)][min(x + 1, src_w - 1)]

            gray = int(a * (1 - x_diff) * (1 - y_diff) +
                       b * (x_diff) * (1 - y_diff) +
                       c * (y_diff) * (1 - x_diff) +
                       d * (x_diff * y_diff))
            row.append(max(0, min(255, gray)))
        dst_pixels.append(row)
    return dst_pixels


def generate_braille_art(img_pixels, w, h, threshold=128):
    """
    유니코드 점자 비트맵 변환 (2x4 서브픽셀 매핑)
    실제 해상도: 148 x 92 픽셀 ➔ 터미널 74 x 23 글자로 압축 출력!
    점자 인덱스 매핑:
    [0, 3]
    [1, 4]
    [2, 5]
    [6, 7]
    Unicode = 0x2800 + sum(bit * (1 << dot))
    """
    target_pw = CANVAS_WIDTH * 2  # 148
    target_ph = CANVAS_HEIGHT * 4 # 92

    # 148 x 92 픽셀로 초고해상도 리사이징
    res_px = resize_bilinear(img_pixels, w, h, target_pw, target_ph)

    # Braille 점 비트 가중치
    dot_map = [
        (0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04),
        (1, 0, 0x08), (1, 1, 0x10), (1, 2, 0x20),
        (0, 3, 0x40), (1, 3, 0x80)
    ]

    lines = []
    for cy in range(CANVAS_HEIGHT):
        row_chars = []
        for cx in range(CANVAS_WIDTH):
            px_x = cx * 2
            px_y = cy * 4

            braille_code = 0
            for dx, dy, bit in dot_map:
                val = res_px[px_y + dy][px_x + dx]
                # 어두운 픽셀(피사체)을 점으로 표현
                if val < threshold:
                    braille_code |= bit

            ch = chr(0x2800 + braille_code)
            row_chars.append(ch)
        lines.append("".join(row_chars))

    return lines


def generate_halfblock_art(img_pixels, w, h, threshold=128):
    """
    상하 2배 서브픽셀 변환 (Half-Block: ▀ ▄ █ ' ')
    실제 해상도: 74 x 46 도트 ➔ 터미널 74 x 23 글자로 압축 출력!
    """
    target_ph = CANVAS_HEIGHT * 2 # 46
    res_px = resize_bilinear(img_pixels, w, h, CANVAS_WIDTH, target_ph)

    lines = []
    for cy in range(CANVAS_HEIGHT):
        row_chars = []
        for cx in range(CANVAS_WIDTH):
            top_dark = res_px[cy * 2][cx] < threshold
            bot_dark = res_px[cy * 2 + 1][cx] < threshold

            if top_dark and bot_dark:
                ch = '█'
            elif top_dark and not bot_dark:
                ch = '▀'
            elif not top_dark and bot_dark:
                ch = '▄'
            else:
                ch = ' '
            row_chars.append(ch)
        lines.append("".join(row_chars))

    return lines


def generate_ascii_art(img_path, format_type="braille", threshold=128):
    src_w, src_h, src_pixels = ImageDecoder.load(img_path)

    if format_type == "braille":
        return generate_braille_art(src_pixels, src_w, src_h, threshold)
    elif format_type == "halfblock":
        return generate_halfblock_art(src_pixels, src_w, src_h, threshold)
    else:
        # 일반 블록 모드
        res_px = resize_bilinear(src_pixels, src_w, src_h, CANVAS_WIDTH, CANVAS_HEIGHT)
        lines = []
        for y in range(CANVAS_HEIGHT):
            row = []
            for x in range(CANVAS_WIDTH):
                idx = (res_px[y][x] * len(RAMP_BLOCK)) // 256
                row.append(RAMP_BLOCK[min(len(RAMP_BLOCK) - 1, idx)])
            lines.append("".join(row))
        return lines


def main():
    parser = argparse.ArgumentParser(description="AsciiArt Studio — 고화질 도트/아스키 생성기")
    parser.add_argument("image", help="입력 이미지 경로 (BMP, PPM, PGM)")
    parser.add_argument("--format", choices=["braille", "halfblock", "block"], default="braille",
                        help="렌더링 모드: braille(8배 초고해상도 도트), halfblock(상하 2배), block(기본)")
    parser.add_argument("--threshold", type=int, default=130, help="도트 이진화 임계값 (0~255)")
    parser.add_argument("--yaml", action="store_true", help="YAML scene_art 형식 출력")

    args = parser.parse_args()

    lines = generate_ascii_art(args.image, format_type=args.format, threshold=args.threshold)

    if args.yaml:
        print("    scene_art:")
        for line in lines:
            print(f'      - "{line}"')
    else:
        print("┌" + "─" * CANVAS_WIDTH + "┐")
        for line in lines:
            print(f"│{line}│")
        print("└" + "─" * CANVAS_WIDTH + "┘")


if __name__ == "__main__":
    main()
