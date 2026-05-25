
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
from itertools import chain
import warnings
import sys

# Constant macro: whether to fill polygons with color
FILL_COLOR = False
# Constant macro: whether to generate STL model
CREATE_MODEL = True
# Constant macro: size of the border lines
BORDER_SIZE = 0.02

# Configuration dictionary for different tessellations
CONFIGS = {
    'hex': {
        'p': 7,
        'q': 3,
        'k': 3,
        'ring_inrad': 0.98
    },
    'tri': {
        'p': 3,
        'q': 7,
        'k': 7,
        'ring_inrad': 0.96
    },
    'square': {
        'p': 4,
        'q': 5,
        'k': 8,
        'ring_inrad': 0.98
    }
}

def ortho_centre(p, q):
    """
    Compute the center of the circle passing through p and q that is orthogonal to the unit circle.
    """
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
    """
    Compute the radius of the circle passing through p and q that is orthogonal to the unit circle.
    """
    px, py = p
    qx, qy = q
    if abs(px * qy - py * qx) < 1e-12:
        return np.inf
    c = ortho_centre(p, q)
    return np.sqrt(np.sum(c**2) - 1)

def ortho_angles(p, q):
    """
    Compute the angles of the arc from p to q on the orthogonal circle.
    """
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
    """
    Represent the hyperbolic line between two points p and q as either a line segment or a circular arc.
    Returns a dictionary with type ('line' or 'circle') and parameters.
    """
    px, py = p
    qx, qy = q
    if abs(px * qy - py * qx) < 1e-12:
        return {'type': 'line', 'points': [p, q]}
    c = ortho_centre(p, q)
    r = ortho_radius(p, q)
    angles = ortho_angles(p, q)
    return {'type': 'circle', 'center': c, 'radius': r, 'angles': angles}

def inversion_circle(circle, point):
    """
    Invert a point about a circle.
    circle: {'center': (cx, cy), 'radius': r}
    """
    cx, cy = circle['center']
    r = circle['radius']
    px, py = point
    d_sq = (cx - px)**2 + (cy - py)**2
    if d_sq < 1e-12:
        return np.array([np.inf, np.inf])
    inv = np.array([cx, cy]) + r**2 * (np.array([px, py]) - np.array([cx, cy])) / d_sq
    return inv

def inversion_line(line, point):
    """
    Invert a point about a line (represented by two points).
    line: [(x1, y1), (x2, y2)]
    """
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
    """
    Invert a point about a geometric object (circle or line).
    """
    if isinstance(geo_obj, dict):
        if geo_obj['type'] == 'circle':
            return inversion_circle({'center': geo_obj['center'], 'radius': geo_obj['radius']}, point)
        elif geo_obj['type'] == 'line':
            return inversion_line(geo_obj['points'], point)
    elif isinstance(geo_obj, list) and len(geo_obj) == 2:
        return inversion_line(geo_obj, point)
    raise ValueError("Unsupported geometric object for inversion")

def invert_polygon(polygon_vertices):
    """
    Invert a polygon about each of its edges (hyperbolic lines).
    Returns a list of new polygons.
    """
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
    """
    Generate the initial central polygon for tessellation {p, q}.
    p: number of sides of the polygon
    q: number of polygons meeting at each vertex
    phi: rotation angle (radians)
    """
    cot_p = 1 / np.tan(np.pi / p)
    cot_q = 1 / np.tan(np.pi / q)
    numerator = cot_p * cot_q - 1
    denominator = np.sqrt((cot_p * cot_q)**2 - 1)
    r = numerator / denominator
    theta = np.pi * np.arange(1, 2*p, 2) / p
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    # Apply rotation
    rot_matrix = np.array([[np.cos(phi), -np.sin(phi)],
                           [np.sin(phi),  np.cos(phi)]])
    vertices = rot_matrix @ np.array([x, y])
    return list(vertices.T)

def polygon_round(polygon_vertices, tol=1e-10):
    """
    Round polygon vertices to tolerance.
    """
    return [tuple(np.round(v, int(-np.log10(tol)))) for v in polygon_vertices]

def polygon_union(polygons, tol=1e-10):
    """
    Remove duplicate polygons from a list.
    """
    if not isinstance(polygons, list):
        return [polygons]
    unique = []
    seen = set()
    for poly in polygons:
        rounded = tuple(polygon_round(poly, tol))
        # Also check reversed order to account for different orientations
        reversed_rounded = tuple(reversed(rounded))
        if rounded not in seen and reversed_rounded not in seen:
            seen.add(rounded)
            unique.append(poly)
    return unique

def hyperbolic_tessellation(p, q, phi=0.0, k=3, tol=1e-10):
    """
    Generate hyperbolic tessellation {p, q} up to recursion depth k.
    Returns list of polygons (each polygon is list of vertices).
    """
    initial = central_polygon(p, q, phi)
    all_polygons = [initial]
    for _ in range(k):
        new_polys = []
        for poly in all_polygons:
            new_polys.extend(invert_polygon(poly))
        all_polygons = polygon_union(all_polygons + new_polys, tol)
    return all_polygons

def plot_tessellation(p, q, phi=0.0, k=3, colormap='viridis', use_hyperbolic_lines=True, ax=None):
    """
    Plot the hyperbolic tessellation.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')
        ax.axis('off')
    # Scale BORDER_SIZE for matplotlib linewidth (since linewidth is in points, not world units)
    linewidth = max(0.5, BORDER_SIZE * 20)
    # Draw unit circle
    unit_circle = Circle((0, 0), 1, fill=False, edgecolor='black', linewidth=linewidth)
    ax.add_patch(unit_circle)
    # Get polygons
    polygons = hyperbolic_tessellation(p, q, phi, k)
    # Plot each polygon
    patches = []
    for poly in polygons:
        # Check if polygon is inside unit circle
        centroid = np.mean(poly, axis=0)
        if np.linalg.norm(centroid) > 1.2:
            continue
        # Color based on centroid distance (only if FILL_COLOR is True)
        if FILL_COLOR:
            color_val = np.linalg.norm(centroid)
            cmap = plt.get_cmap(colormap)
            face_color = cmap(color_val)
        else:
            face_color = 'none'
        # Create polygon patch
        poly_patch = Polygon(poly, closed=True, facecolor=face_color, edgecolor='black', linewidth=linewidth)
        patches.append(poly_patch)
    # Add patches to axis
    collection = PatchCollection(patches, match_original=True)
    ax.add_collection(collection)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
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
    polygons = hyperbolic_tessellation(cfg['p'], cfg['q'], k=cfg['k'])
    if CREATE_MODEL:
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
    plt.title("Tessellation")
    plt.show()
