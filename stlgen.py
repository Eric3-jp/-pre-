import numpy as np

def generate_stl(polygons, filename, thickness=0.1, border_size=0.02, ring_inrad=0.98, num_segments=100):
    """
    Generate STL file from list of 2D polygons by extruding their borders (镂空),
    plus an outer circular border for strength.
    """
    with open(filename, 'w') as f:
        f.write("solid poincare\n")
        seen_edges = set()
        for poly in polygons:
            # Skip polygons outside unit circle
            centroid = np.mean(poly, axis=0)
            if np.linalg.norm(centroid) > ring_inrad:
                continue
            n = len(poly)
            for i in range(n):
                p1 = np.array(poly[i])
                p2 = np.array(poly[(i+1)%n])
                # Create edge key to avoid duplicates
                edge_key = tuple(sorted((tuple(np.round(p1, 10)), tuple(np.round(p2, 10)))))
                if edge_key in seen_edges:
                    continue
                seen_edges.add(edge_key)
                # Generate rectangular border around this edge
                generate_border(f, p1, p2, thickness, border_size)
        # Add outer circular border
        generate_circular_border(f, ring_inrad, 1.0, thickness, num_segments)
        f.write("endsolid poincare\n")

def generate_circular_border(f, inner_radius, outer_radius, thickness, num_segments):
    """Generate a circular border (annulus) and write to STL file."""
    # Generate points on inner and outer circles
    theta = np.linspace(0, 2 * np.pi, num_segments, endpoint=False)
    inner_x = inner_radius * np.cos(theta)
    inner_y = inner_radius * np.sin(theta)
    outer_x = outer_radius * np.cos(theta)
    outer_y = outer_radius * np.sin(theta)
    # Extrude the annulus
    for i in range(num_segments):
        p_inner1 = np.array([inner_x[i], inner_y[i]])
        p_inner2 = np.array([inner_x[(i+1)%num_segments], inner_y[(i+1)%num_segments]])
        p_outer1 = np.array([outer_x[i], outer_y[i]])
        p_outer2 = np.array([outer_x[(i+1)%num_segments], outer_y[(i+1)%num_segments]])
        # Top face (z=thickness)
        write_quad(f, p_inner1, p_outer1, p_outer2, p_inner2, thickness)
        # Bottom face (z=0)
        write_quad(f, p_inner1, p_inner2, p_outer2, p_outer1, 0.0)
        # Inner vertical face
        write_quad(f, p_inner1, p_inner1, p_inner2, p_inner2, None, z1=0.0, z2=thickness)
        # Outer vertical face
        write_quad(f, p_outer1, p_outer2, p_outer2, p_outer1, None, z1=0.0, z2=thickness)

def generate_border(f, p1, p2, thickness, border_size):
    """Generate a rectangular border around an edge and write to STL."""
    # Compute edge direction
    edge_dir = p2 - p1
    edge_len = np.linalg.norm(edge_dir)
    if edge_len < 1e-12:
        return
    edge_dir = edge_dir / edge_len
    # Compute perpendicular direction (for border width)
    perp_dir = np.array([-edge_dir[1], edge_dir[0]])
    # Compute 4 corner points for the rectangle (bottom face)
    p1a = p1 - border_size * perp_dir
    p1b = p1 + border_size * perp_dir
    p2a = p2 - border_size * perp_dir
    p2b = p2 + border_size * perp_dir
    # Generate all 6 faces of the rectangular prism
    # Top face (z=thickness)
    write_quad(f, p1a, p1b, p2b, p2a, thickness)
    # Bottom face (z=0)
    write_quad(f, p1a, p2a, p2b, p1b, 0.0)
    # Side faces
    write_quad(f, p1a, p1a, p1b, p1b, None, z1=0.0, z2=thickness)
    write_quad(f, p2a, p2b, p2b, p2a, None, z1=0.0, z2=thickness)
    write_quad(f, p1a, p2a, p2a, p1a, None, z1=0.0, z2=thickness)
    write_quad(f, p1b, p1b, p2b, p2b, None, z1=0.0, z2=thickness)

def write_quad(f, p0, p1, p2, p3, z=None, z1=None, z2=None):
    """Write a quadrilateral as two triangles to STL file."""
    if z is not None:
        v0 = np.array([p0[0], p0[1], z])
        v1 = np.array([p1[0], p1[1], z])
        v2 = np.array([p2[0], p2[1], z])
        v3 = np.array([p3[0], p3[1], z])
    else:
        v0 = np.array([p0[0], p0[1], z1])
        v1 = np.array([p1[0], p1[1], z2])
        v2 = np.array([p2[0], p2[1], z2])
        v3 = np.array([p3[0], p3[1], z1])
    write_triangle(f, v0, v1, v2)
    write_triangle(f, v0, v2, v3)

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
