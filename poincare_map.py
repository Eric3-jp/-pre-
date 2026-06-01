import numpy as np
import sys
from PIL import Image

TARGET_SIZE = 500

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
    if abs(px * qy - py * qx) < 1e-12:
        return {'type': 'line', 'points': [p, q]}
    c = ortho_centre(p, q)
    r = ortho_radius(p, q)
    angles = ortho_angles(p, q)
    return {'type': 'circle', 'center': c, 'radius': r, 'angles': angles}

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

def polygon_round(polygon_vertices, tol=1e-10):
    return [tuple(np.round(v, int(-np.log10(tol)))) for v in polygon_vertices]

def polygon_union(polygons, tol=1e-10):
    if not isinstance(polygons, list):
        return [polygons]
    unique = []
    seen = set()
    for poly in polygons:
        rounded = tuple(polygon_round(poly, tol))
        reversed_rounded = tuple(reversed(rounded))
        if rounded not in seen and reversed_rounded not in seen:
            seen.add(rounded)
            unique.append(poly)
    return unique

def hyperbolic_tessellation(p, q, phi=0.0, k=3, tol=1e-10):
    initial = central_polygon(p, q, phi)
    all_polygons = [initial]
    for _ in range(k):
        new_polys = []
        for poly in all_polygons:
            new_polys.extend(invert_polygon(poly))
        all_polygons = polygon_union(all_polygons + new_polys, tol)
    return all_polygons

def poincare_transform_coords(x, y, p=7, q=3, phi=0.0, k=3):
    polygons = hyperbolic_tessellation(p, q, phi, k)

    point = np.array([x, y])
    r = np.linalg.norm(point)

    if r >= 1.0:
        return point

    for poly in polygons:
        centroid = np.mean(poly, axis=0)
        if np.linalg.norm(centroid) > 1.0:
            continue

        n = len(poly)
        for i in range(n):
            p1 = poly[i]
            p2 = poly[(i + 1) % n]

            if np.linalg.norm(p1) > 1.0 or np.linalg.norm(p2) > 1.0:
                continue

            hl = hyperbolic_line(p1, p2)

            if hl['type'] == 'circle':
                c = np.array(hl['center'])
                circ_r = hl['radius']

                if abs(np.linalg.norm(c) - circ_r) < 1e-8:
                    continue

                d = np.linalg.norm(c)
                if d > 1.0 + 1e-8:
                    continue

                new_point = inversion_circle({'center': c, 'radius': circ_r}, point)

                if np.linalg.norm(new_point) < np.linalg.norm(point):
                    point = new_point
            else:
                continue

    return point

def apply_poincare_transform_to_coords():
    coords = np.mgrid[-1:1:500j, -1:1:500j]
    x_coords = coords[0]
    y_coords = coords[1]

    return x_coords, y_coords

def load_and_preprocess_image(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    width, height = img.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    img_cropped = img.crop((left, top, right, bottom))

    img_resized = img_cropped.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)

    return img_resized

def apply_poincare_transform(img):
    img_array = np.array(img)

    result_array = np.zeros_like(img_array)

    x_grid, y_grid = apply_poincare_transform_to_coords()

    half_size = TARGET_SIZE // 2

    for i in range(TARGET_SIZE):
        for j in range(TARGET_SIZE):
            x = x_grid[i, j]
            y = y_grid[i, j]

            x_new = (x + 1) * half_size
            y_new = (y + 1) * half_size

            x_new = np.clip(x_new, 0, TARGET_SIZE - 1)
            y_new = np.clip(y_new, 0, TARGET_SIZE - 1)

            x0, y0 = int(x_new), int(y_new)
            x1, y1 = min(x0 + 1, TARGET_SIZE - 1), min(y0 + 1, TARGET_SIZE - 1)

            fx = x_new - x0
            fy = y_new - y0

            if x0 >= 0 and x0 < TARGET_SIZE and y0 >= 0 and y0 < TARGET_SIZE:
                c00 = img_array[y0, x0]
                c10 = img_array[y1, x0]
                c01 = img_array[y0, x1]
                c11 = img_array[y1, x1]

                result_array[i, j] = (1 - fx) * (1 - fy) * c00 + \
                                     fx * (1 - fy) * c10 + \
                                     (1 - fx) * fy * c01 + \
                                     fx * fy * c11
            else:
                result_array[i, j] = [0, 0, 0, 0]

    return Image.fromarray(result_array.astype(np.uint8))

def create_disk_mask(size=500):
    y, x = np.ogrid[:size, :size]
    center = size // 2
    radius = size // 2
    mask = (x - center)**2 + (y - center)**2 <= radius**2
    return mask

def apply_disk_mask(img):
    img_array = np.array(img)
    mask = create_disk_mask(TARGET_SIZE)

    result_array = np.zeros_like(img_array)
    result_array[mask] = img_array[mask]

    return Image.fromarray(result_array.astype(np.uint8))

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python poincare_map.py <pngpath>")
        sys.exit(1)

    image_path = sys.argv[1]

    print(f"Loading and preprocessing image: {image_path}")
    img = load_and_preprocess_image(image_path)

    print(f"Applying Poincaré transformation...")
    transformed_img = apply_poincare_transform(img)

    print(f"Applying disk mask...")
    final_img = apply_disk_mask(transformed_img)

    output_path = image_path.rsplit('.', 1)[0] + '_poincare.png'
    final_img.save(output_path)
    print(f"Result saved to: {output_path}")

    final_img.show()

if __name__ == '__main__':
    main()