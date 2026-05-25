import numpy as np

def generate_stl(polygons, filename, thickness=0.1):
    """
    Generate STL file from list of 2D polygons by extruding them.
    """
    with open(filename, 'w') as f:
        f.write("solid poincare\n")
        for poly in polygons:
            # Skip polygons outside unit circle
            centroid = np.mean(poly, axis=0)
            if np.linalg.norm(centroid) > 1.0:
                continue
            n = len(poly)
            # Top face (z=thickness)
            for i in range(1, n-1):
                v0 = np.array([poly[0][0], poly[0][1], thickness])
                v1 = np.array([poly[i][0], poly[i][1], thickness])
                v2 = np.array([poly[i+1][0], poly[i+1][1], thickness])
                write_triangle(f, v0, v1, v2)
            # Bottom face (z=0)
            for i in range(1, n-1):
                v0 = np.array([poly[0][0], poly[0][1], 0.0])
                v1 = np.array([poly[i+1][0], poly[i+1][1], 0.0])
                v2 = np.array([poly[i][0], poly[i][1], 0.0])
                write_triangle(f, v0, v1, v2)
            # Side faces
            for i in range(n):
                p1 = poly[i]
                p2 = poly[(i+1)%n]
                v0 = np.array([p1[0], p1[1], 0.0])
                v1 = np.array([p2[0], p2[1], 0.0])
                v2 = np.array([p2[0], p2[1], thickness])
                write_triangle(f, v0, v1, v2)
                v0 = np.array([p1[0], p1[1], 0.0])
                v1 = np.array([p2[0], p2[1], thickness])
                v2 = np.array([p1[0], p1[1], thickness])
                write_triangle(f, v0, v1, v2)
        f.write("endsolid poincare\n")

def write_triangle(f, v0, v1, v2):
    """Write a single triangle to STL file."""
    # Compute normal vector (cross product of edges)
    edge1 = v1 - v0
    edge2 = v2 - v0
    normal = np.cross(edge1, edge2)
    norm = np.linalg.norm(normal)
    if norm > 1e-12:
        normal = normal / norm
    else:
        normal = np.array([0.0, 0.0, 1.0])
    # Round small numbers to avoid issues
    normal = np.round(normal, decimals=10)
    v0 = np.round(v0, decimals=10)
    v1 = np.round(v1, decimals=10)
    v2 = np.round(v2, decimals=10)
    f.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
    f.write("  outer loop\n")
    f.write(f"    vertex {v0[0]} {v0[1]} {v0[2]}\n")
    f.write(f"    vertex {v1[0]} {v1[1]} {v1[2]}\n")
    f.write(f"    vertex {v2[0]} {v2[1]} {v2[2]}\n")
    f.write("  endloop\n")
    f.write("endfacet\n")
