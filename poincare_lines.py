import numpy as np
import matplotlib.pyplot as plt
import sys
from char2lines import text2lines
from poincare import hyperbolic_line
from plotter import plotlines, plotlinecurves

def text_to_poincare(text):
    lines = text2lines(text)
    poincare_curves = []
    
    for line in lines:
        p1, p2 = line
        curve = hyperbolic_line(p1, p2)
        poincare_curves.append(curve)
    
    return lines, poincare_curves

def main():
    if len(sys.argv) < 2:
        print("Usage: python poincare_lines.py <text>")
        print("Example: python poincare_lines.py 你好")
        sys.exit(1)
    
    text = sys.argv[1]
    print(f"Converting text: {text}")
    
    lines, poincare_curves = text_to_poincare(text)
    print(f"Generated {len(lines)} line segments")
    print(f"Generated {len(poincare_curves)} Poincaré curves")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    plotlines(lines, ax=ax1, title=f"Original: {text}")
    plotlinecurves(poincare_curves, ax=ax2, title=f"Poincaré: {text}")
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
