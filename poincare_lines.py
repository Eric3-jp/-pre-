import numpy as np
import matplotlib.pyplot as plt
import sys
from char2lines import text2lines
from poincare import hyperbolic_line
from plotter import plotlines, plotlinecurves

def clamp_point_to_disk(point, epsilon=1e-6):
    x, y = point
    r_sq = x*x + y*y
    if r_sq >= 1.0:
        r = np.sqrt(r_sq)
        scale = (1.0 - epsilon) / r
        return (x * scale, y * scale)
    return point

def text_to_poincare(text, scale_multiplier=1.0):
    lines = text2lines(text, scale_multiplier=scale_multiplier)
    poincare_curves = []
    
    for line in lines:
        p1, p2 = line
        p1_clamped = clamp_point_to_disk(p1)
        p2_clamped = clamp_point_to_disk(p2)
        curve = hyperbolic_line(p1_clamped, p2_clamped)
        poincare_curves.append(curve)
    
    return lines, poincare_curves

def main():
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
            scale_multiplier = 1.0
    
    print(f"Converting text: {text}")
    print(f"Scale multiplier: {scale_multiplier}")
    
    lines, poincare_curves = text_to_poincare(text, scale_multiplier)
    print(f"Generated {len(lines)} line segments")
    print(f"Generated {len(poincare_curves)} Poincaré curves")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    plotlines(lines, ax=ax1, title=f"Original: {text} (scale={scale_multiplier})")
    plotlinecurves(poincare_curves, ax=ax2, title=f"Poincaré: {text} (scale={scale_multiplier})")
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
