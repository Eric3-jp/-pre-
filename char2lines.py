from pathlib import Path

import numpy as np
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.textpath import TextPath

WINDOWS_FONT_DIR = Path("C:/Windows/Fonts")
FONT_FILE_CANDIDATES = (
    WINDOWS_FONT_DIR / "simhei.ttf",
    WINDOWS_FONT_DIR / "simsun.ttc",
    WINDOWS_FONT_DIR / "simkai.ttf",
    WINDOWS_FONT_DIR / "simfang.ttf",
    WINDOWS_FONT_DIR / "msyh.ttc",
    WINDOWS_FONT_DIR / "Source Han Serif SC Heavy (TrueType).ttf",
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
)
PREFERRED_FAMILIES = (
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "FangSong",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "PingFang SC",
    "Arial Unicode MS",
)


def find_chinese_font():
    for font_path in FONT_FILE_CANDIDATES:
        if font_path.exists():
            return FontProperties(fname=str(font_path))

    for family in PREFERRED_FAMILIES:
        font = FontProperties(family=family)
        try:
            font_path = findfont(font, fallback_to_default=False)
        except ValueError:
            continue

        if font_path and Path(font_path).exists():
            return FontProperties(fname=font_path)

    return FontProperties()


def text2lines(text, char_spacing=0.15, y_offset=0.0, scale_multiplier=1.0):
    font = find_chinese_font()
    char_data = []

    for char in text:
        path = TextPath((0, 0), char, size=1.0, prop=font)
        vertices = path.vertices
        if len(vertices) == 0:
            continue

        min_x = np.min(vertices[:, 0])
        max_x = np.max(vertices[:, 0])
        min_y = np.min(vertices[:, 1])
        max_y = np.max(vertices[:, 1])
        char_data.append((path, (min_x, max_x, min_y, max_y)))

    if not char_data:
        return []

    total_width = sum(max_x - min_x for _, (min_x, max_x, _, _) in char_data)
    total_spacing = char_spacing * (len(char_data) - 1)
    total_needed = total_width + total_spacing
    base_scale = 1.8 / total_needed if total_needed > 1.8 else 1.0
    scale = base_scale * scale_multiplier
    cursor_x = -0.9 * scale_multiplier
    lines = []

    for path, (min_x, max_x, min_y, max_y) in char_data:
        offset_x = cursor_x - min_x * scale
        offset_y = y_offset - (min_y + (max_y - min_y) / 2) * scale

        for polygon in path.to_polygons():
            if len(polygon) < 2:
                continue

            transformed = polygon * scale + np.array([offset_x, offset_y])
            for start, end in zip(transformed[:-1], transformed[1:]):
                lines.append([start.tolist(), end.tolist()])

        cursor_x += (max_x - min_x) * scale + char_spacing

    return lines
