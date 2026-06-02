import sys

import numpy as np

from char2lines import text2lines
from poincare import hyperbolic_line


def clamp_point_to_disk(point, epsilon=1e-6):
    x, y = point
    radius_squared = x * x + y * y
    if radius_squared >= 1.0:
        radius = np.sqrt(radius_squared)
        scale = (1.0 - epsilon) / radius
        return (x * scale, y * scale)
    return point


def fisheye_point(point, strength=1.6, radius=1.0):
    x, y = point
    r = np.hypot(x, y)
    if r < 1e-12:
        return [0.0, 0.0]

    normalized_r = min(r / radius, 1.0)
    if strength <= 1e-6:
        warped_r = normalized_r
    else:
        warped_r = np.tanh(strength * normalized_r) / np.tanh(strength)

    scale = warped_r * radius / r
    return [x * scale, y * scale]


def densify_line(start, end, max_step=0.015):
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    distance = np.linalg.norm(end - start)
    steps = max(2, int(np.ceil(distance / max_step)) + 1)
    return np.linspace(start, end, steps)


def text_to_fisheye(text, scale_multiplier=1.0, char_spacing=0.15, y_offset=0.0, strength=1.6):
    lines = text2lines(
        text,
        scale_multiplier=scale_multiplier,
        char_spacing=char_spacing,
        y_offset=y_offset,
    )
    fisheye_polylines = []

    for start, end in lines:
        points = densify_line(start, end)
        warped = [fisheye_point(point, strength=strength) for point in points]
        fisheye_polylines.append(warped)

    return lines, fisheye_polylines


def text_to_poincare(text, scale_multiplier=1.0, char_spacing=0.15, y_offset=0.0):
    lines = text2lines(
        text,
        scale_multiplier=scale_multiplier,
        char_spacing=char_spacing,
        y_offset=y_offset,
    )
    poincare_curves = []

    for p1, p2 in lines:
        p1_clamped = clamp_point_to_disk(p1)
        p2_clamped = clamp_point_to_disk(p2)
        poincare_curves.append(hyperbolic_line(p1_clamped, p2_clamped))

    return lines, poincare_curves


def main():
    import matplotlib.pyplot as plt

    from plotter import plot_fisheye_lines, plotlines

    if len(sys.argv) < 2:
        print("Usage: python poincare_lines.py <text> [scale]")
        print("Example: python poincare_lines.py 你好")
        print("Example: python poincare_lines.py 你好 1.5")
        sys.exit(1)

    text = sys.argv[1]
    scale_multiplier = 1.0

    if len(sys.argv) >= 3:
        try:
            scale_multiplier = float(sys.argv[2])
        except ValueError:
            print(f"Warning: Invalid scale value '{sys.argv[2]}', using default 1.0")

    print(f"Converting text: {text}")
    print(f"Scale multiplier: {scale_multiplier}")

    lines, fisheye_lines = text_to_fisheye(text, scale_multiplier=scale_multiplier)
    print(f"Generated {len(lines)} line segments")
    print(f"Generated {len(fisheye_lines)} fisheye polylines")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    plotlines(lines, ax=ax1, title=f"Original: {text} (scale={scale_multiplier})")
    plot_fisheye_lines(fisheye_lines, ax=ax2, title=f"Fisheye: {text} (scale={scale_multiplier})")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
