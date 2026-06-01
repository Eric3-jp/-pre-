import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

def plotlines(lines, ax=None, title=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')
    
    for line in lines:
        (sx, sy), (ex, ey) = line
        ax.plot([sx, ex], [sy, ey], 'k-', linewidth=1.5)
    
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.3)
    if title:
        ax.set_title(title)
    
    return ax

def plotlinecurves(poincare_curves, ax=None, title=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')
    
    for curve in poincare_curves:
        if curve['type'] == 'line':
            points = curve['points']
            ax.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]], 'k-', linewidth=1.5)
        elif curve['type'] == 'circle':
            center = curve['center']
            radius = curve['radius']
            angles = curve['angles']
            theta = np.linspace(angles[0], angles[1], 100)
            x = center[0] + radius * np.cos(theta)
            y = center[1] + radius * np.sin(theta)
            r_sq = x*x + y*y
            inside = r_sq <= 1.0001
            ax.plot(x[inside], y[inside], 'k-', linewidth=1.5)
    
    unit_circle = Circle((0, 0), 1, fill=False, edgecolor='blue', linewidth=1, linestyle='--')
    ax.add_patch(unit_circle)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.3)
    if title:
        ax.set_title(title)
    
    return ax
