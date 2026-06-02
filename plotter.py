from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle

WINDOWS_FONT_DIR = Path("C:/Windows/Fonts")
FONT_FILE_CANDIDATES = (
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


def find_chinese_font():
    for font_path in FONT_FILE_CANDIDATES:
        if font_path.exists():
            font_manager.fontManager.addfont(str(font_path))
            font = FontProperties(fname=str(font_path))
            plt.rcParams["font.family"] = [font.get_name()]
            plt.rcParams["axes.unicode_minus"] = False
            return font
    return None


CHINESE_FONT = find_chinese_font()


def set_title(ax, title):
    if CHINESE_FONT is not None:
        ax.set_title(title, fontproperties=CHINESE_FONT)
    else:
        ax.set_title(title)


def plotlines(lines, ax=None, title=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect("equal")

    for line in lines:
        (sx, sy), (ex, ey) = line
        ax.plot([sx, ex], [sy, ey], "k-", linewidth=1.5)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.3)
    if title:
        set_title(ax, title)

    return ax


def plot_fisheye_lines(polylines, ax=None, title=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect("equal")

    for polyline in polylines:
        points = np.array(polyline, dtype=float)
        if len(points) < 2:
            continue
        ax.plot(points[:, 0], points[:, 1], "k-", linewidth=1.5)

    unit_circle = Circle((0, 0), 1, fill=False, edgecolor="blue", linewidth=1, linestyle="--")
    ax.add_patch(unit_circle)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    if title:
        set_title(ax, title)

    return ax


def plotlinecurves(poincare_curves, ax=None, title=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect("equal")

    for curve in poincare_curves:
        if curve["type"] == "line":
            points = curve["points"]
            ax.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]], "k-", linewidth=1.5)
        elif curve["type"] == "circle":
            center = curve["center"]
            radius = curve["radius"]
            angles = curve["angles"]
            theta = np.linspace(angles[0], angles[1], 100)
            x = center[0] + radius * np.cos(theta)
            y = center[1] + radius * np.sin(theta)
            r_sq = x * x + y * y
            inside = r_sq <= 1.0001
            ax.plot(x[inside], y[inside], "k-", linewidth=1.5)

    unit_circle = Circle((0, 0), 1, fill=False, edgecolor="blue", linewidth=1, linestyle="--")
    ax.add_patch(unit_circle)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.3)
    if title:
        set_title(ax, title)

    return ax
