from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
WINDOWS_FONT_DIR = Path("C:/Windows/Fonts")
FONT_FILE_CANDIDATES = (
    BASE_DIR / "fonts" / "SourceHanSerifSC-Heavy.ttf",
    WINDOWS_FONT_DIR / "simhei.ttf",
    WINDOWS_FONT_DIR / "msyh.ttc",
    WINDOWS_FONT_DIR / "simsun.ttc",
    WINDOWS_FONT_DIR / "simkai.ttf",
    WINDOWS_FONT_DIR / "simfang.ttf",
    WINDOWS_FONT_DIR / "Source Han Serif SC Heavy (TrueType).ttf",
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
)
CANVAS_SIZE = 700
FONT_SIZE = 420
MARGIN = 50


def find_chinese_font_path():
    for font_path in FONT_FILE_CANDIDATES:
        if font_path.exists():
            return font_path
    return None


def load_font(size=FONT_SIZE):
    font_path = find_chinese_font_path()
    if font_path is None:
        raise RuntimeError("Chinese font file not found: fonts/SourceHanSerifSC-Heavy.ttf")
    return ImageFont.truetype(str(font_path), size=size)


def render_text_mask(text):
    font = load_font()
    scratch = Image.new("L", (1, 1), 0)
    scratch_draw = ImageDraw.Draw(scratch)
    bbox = scratch_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    image_width = max(CANVAS_SIZE, text_width + MARGIN * 2)
    image_height = max(CANVAS_SIZE, text_height + MARGIN * 2)
    image = Image.new("L", (image_width, image_height), 0)
    draw = ImageDraw.Draw(image)
    x = (image_width - text_width) / 2 - bbox[0]
    y = (image_height - text_height) / 2 - bbox[1]
    draw.text((x, y), text, fill=255, font=font)
    return np.array(image)


def contours_to_lines(contours, image_shape, char_spacing, y_offset, scale_multiplier):
    height, width = image_shape
    center = np.array([width / 2, height / 2], dtype=float)
    scale = 1.8 * scale_multiplier / max(width, height)
    lines = []

    for contour in contours:
        epsilon = max(1.0, 0.008 * cv2.arcLength(contour, closed=True))
        simplified = cv2.approxPolyDP(contour, epsilon, closed=True)
        points = simplified[:, 0, :].astype(float)
        if len(points) < 2:
            continue

        normalized = points - center
        normalized[:, 1] *= -1
        normalized *= scale
        normalized[:, 1] += y_offset

        for start, end in zip(normalized, np.roll(normalized, -1, axis=0)):
            if np.linalg.norm(end - start) < 1e-5:
                continue
            lines.append([start.tolist(), end.tolist()])

    if char_spacing != 0.15:
        spacing_adjustment = char_spacing - 0.15
        for line in lines:
            for point in line:
                point[0] *= 1 + spacing_adjustment

    return lines


def text2lines(text, char_spacing=0.15, y_offset=0.0, scale_multiplier=1.0):
    if not text:
        return []

    mask = render_text_mask(text)
    _, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return []

    return contours_to_lines(
        contours,
        binary.shape,
        char_spacing=char_spacing,
        y_offset=y_offset,
        scale_multiplier=scale_multiplier,
    )
