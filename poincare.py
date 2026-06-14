import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
from itertools import chain
import warnings
import sys

# Constant macro: whether to fill polygons with color
# 提示：如果你想要带颜色的填充效果，请将这里改为 True
FILL_COLOR = True
# Constant macro: whether to generate STL model
CREATE_MODEL = False # 仅作绘图测试可先关闭STL生成
# Constant macro: size of the border lines
BORDER_SIZE = 0.02

# Configuration dictionary for different tessellations
CONFIGS = {
    'hex': {
        'p': 7,
        'q': 3,
        'k': 6,
        'ring_inrad': 0.96
    },
    'tri': {
        'p': 3,
        'q': 7,
        'k': 12,
        'ring_inrad': 0.96
    },
    'square': {
        'p': 4,
        'q': 5,
        'k': 8,
        'ring_inrad': 0.96
    }
}

def ortho_centre(p, q):
    px, py = p
    qx, qy = q
    d = 2 * (px * qy - py * qx)
    if abs(d) < 1e-12:
        return np.array([np.inf, np.inf])
    p_term = 1 + px**2 + py**2
    q_term = 1 + qx**2 + qy**2
    cx = p_term * qy - py * q_term
    cy = -p_term * qx + px * q_term
    return np.array([cx, cy]) / d

def ortho_radius(p, q):
    px, py = p
    qx, qy = q
    if abs(px * qy - py * qx) < 1e-12:
        return np.inf
    c = ortho_centre(p, q)
    return np.sqrt(np.sum(c**2) - 1)

def ortho_angles(p, q):
    c = ortho_centre(p, q)
    p_rel = np.array(p) - c
    q_rel = np.array(q) - c
    a = np.arctan2(p_rel[1], p_rel[0])
    b = np.arctan2(q_rel[1], q_rel[0])
    if a < 0:
        a += 2 * np.pi
    if b < 0:
        b += 2 * np.pi
    a, b = sorted([a, b])
    if b - a > np.pi:
        return (b, a + 2 * np.pi)
    return (a, b)

def hyperbolic_line(p, q):
    px, py = p
    qx, qy = q
    # 共线且过原点，视为直线
    if abs(px * qy - py * qx) < 1e-12:
        return {'type': 'line', 'points': [p, q]}
    c = ortho_centre(p, q)
    r = ortho_radius(p, q)
    angles = ortho_angles(p, q)
    return {'type': 'circle', 'center': c, 'radius': r, 'angles': angles}

# 新增核心函数：获取测地线（圆弧）上的密集采样点
def get_geodesic_arc(p, q, num_points=25):
    """获取两点之间双曲测地线（圆弧或直线）上的采样点"""
    hl = hyperbolic_line(p, q)
    if hl['type'] == 'line':
        return np.linspace(p, q, num_points)
    else:
        c = hl['center']
        r = hl['radius']
        a1 = np.arctan2(p[1] - c[1], p[0] - c[0])
        a2 = np.arctan2(q[1] - c[1], q[0] - c[0])
        
        # 寻找两点间的最短角度路径（因为圆在单位圆盘内的那段弧对应的圆心角始终小于 pi）
        diff = (a2 - a1) % (2 * np.pi)
        if diff > np.pi:
            diff -= 2 * np.pi
            
        theta = a1 + np.linspace(0, diff, num_points)
        return np.column_stack((c[0] + r * np.cos(theta), c[1] + r * np.sin(theta)))

def inversion_circle(circle, point):
    cx, cy = circle['center']
    r = circle['radius']
    px, py = point
    d_sq = (cx - px)**2 + (cy - py)**2
    if d_sq < 1e-12:
        return np.array([np.inf, np.inf])
    inv = np.array([cx, cy]) + r**2 * (np.array([px, py]) - np.array([cx, cy])) / d_sq
    return inv

def inversion_line(line, point):
    (x1, y1), (x2, y2) = line
    u = x1 - x2
    v = y2 - y1
    ux, uy = point
    denom = u**2 + v**2
    if denom < 1e-12:
        return np.array(point)
    inv_x = -ux * (v**2 - u**2) - 2 * u * v * uy
    inv_y = uy * (v**2 - u**2) - 2 * u * v * ux
    return np.array([inv_x, inv_y]) / denom

def inversion(geo_obj, point):
    if isinstance(geo_obj, dict):
        if geo_obj['type'] == 'circle':
            return inversion_circle({'center': geo_obj['center'], 'radius': geo_obj['radius']}, point)
        elif geo_obj['type'] == 'line':
            return inversion_line(geo_obj['points'], point)
    elif isinstance(geo_obj, list) and len(geo_obj) == 2:
        return inversion_line(geo_obj, point)
    raise ValueError("Unsupported geometric object for inversion")

def invert_polygon(polygon_vertices):
    new_polygons = []
    n = len(polygon_vertices)
    for i in range(n):
        p = polygon_vertices[i]
        q = polygon_vertices[(i+1)%n]
        hl = hyperbolic_line(p, q)
        inverted = [inversion(hl, v) for v in polygon_vertices]
        new_polygons.append(inverted)
    return new_polygons

def central_polygon(p, q, phi=0.0):
    cot_p = 1 / np.tan(np.pi / p)
    cot_q = 1 / np.tan(np.pi / q)
    numerator = cot_p * cot_q - 1
    denominator = np.sqrt((cot_p * cot_q)**2 - 1)
    r = numerator / denominator
    theta = np.pi * np.arange(1, 2*p, 2) / p
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    rot_matrix = np.array([[np.cos(phi), -np.sin(phi)],
                           [np.sin(phi),  np.cos(phi)]])
    vertices = rot_matrix @ np.array([x, y])
    return list(vertices.T)

def polygon_key(polygon_vertices, tol=1e-7):
    decimals = max(0, int(-np.log10(tol)))
    rounded = [tuple(np.round(v, decimals)) for v in polygon_vertices]
    candidates = []
    n = len(rounded)
    for seq in (rounded, list(reversed(rounded))):
        for shift in range(n):
            candidates.append(tuple(seq[shift:] + seq[:shift]))
    return min(candidates)

def polygon_is_expandable(poly, expand_radius=0.9999):
    vertices = np.asarray(poly, dtype=float)
    if not np.all(np.isfinite(vertices)):
        return False
    vertex_norms = np.linalg.norm(vertices, axis=1)
    return np.any(vertex_norms < expand_radius)

def hyperbolic_tessellation(p, q, phi=0.0, k=3, tol=1e-7, expand_radius=0.9999):
    initial = central_polygon(p, q, phi)
    all_polygons = [initial]
    frontier = [initial]
    seen = {polygon_key(initial, tol)}

    for _ in range(k):
        next_frontier = []
        for poly in frontier:
            if not polygon_is_expandable(poly, expand_radius):
                continue
            for candidate in invert_polygon(poly):
                if not polygon_is_expandable(candidate, expand_radius=1.2):
                    continue
                key = polygon_key(candidate, tol)
                if key in seen:
                    continue
                seen.add(key)
                all_polygons.append(candidate)
                next_frontier.append(candidate)
        if not next_frontier:
            break
        frontier = next_frontier
    return all_polygons

# 修改后的绘图函数
def plot_tessellation(p, q, phi=0.0, k=3, colormap='viridis', use_hyperbolic_lines=True, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.axis('off')
        
    linewidth = max(0.5, BORDER_SIZE * 20)
    unit_circle = Circle((0, 0), 1, fill=False, edgecolor='black', linewidth=linewidth*2)
    ax.add_patch(unit_circle)
    
    polygons = hyperbolic_tessellation(p, q, phi, k)
    patches = []
    
    for poly in polygons:
        centroid = np.mean(poly, axis=0)
        # 抛弃生成过程中越界的异常多边形
        if np.linalg.norm(centroid) > 1.2:
            continue
            
        if FILL_COLOR:
            color_val = np.linalg.norm(centroid)
            cmap = plt.get_cmap(colormap)
            face_color = cmap(color_val)
        else:
            face_color = 'none'
            
        # -- 关键逻辑：将原本的直角多边形替换为测地线（圆弧）多边形 --
        if use_hyperbolic_lines:
            curved_poly = []
            n = len(poly)
            for i in range(n):
                p1 = poly[i]
                p2 = poly[(i+1)%n]
                # 沿每条测地线采集25个点以拟合圆弧
                arc_points = get_geodesic_arc(p1, p2, num_points=25)
                # 舍弃最后一个点以防止与下一条弧的起点重复
                curved_poly.extend(arc_points[:-1])
            poly_to_draw = curved_poly
        else:
            poly_to_draw = poly

        poly_patch = Polygon(poly_to_draw, closed=True, facecolor=face_color, edgecolor='black', linewidth=linewidth)
        patches.append(poly_patch)
        
    collection = PatchCollection(patches, match_original=True)
    ax.add_collection(collection)
    
    # 稍微留一点边距以便看清单位圆的边界
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    return ax

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python poincare.py <config> where <config> is {', '.join(CONFIGS.keys())}")
        sys.exit(1)
    config_key = sys.argv[1]
    if config_key not in CONFIGS:
        print(f"Error: Invalid config '{config_key}'. Available options: {list(CONFIGS.keys())}")
        sys.exit(1)
    cfg = CONFIGS[config_key]
    
    if CREATE_MODEL:
        polygons = hyperbolic_tessellation(cfg['p'], cfg['q'], k=cfg['k'])
        import stlgen
        stl_filename = f"poincare_{config_key}.stl"
        stlgen.generate_stl(
            polygons, 
            stl_filename, 
            border_size=BORDER_SIZE,
            ring_inrad=cfg['ring_inrad']
        )
        print(f"STL file generated: {stl_filename}")
        
    ax = plot_tessellation(cfg['p'], cfg['q'], k=cfg['k'], colormap='viridis')
    plt.title(f"Poincare Disk Tessellation {{{cfg['p']}, {cfg['q']}}}")
    plt.show()