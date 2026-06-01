import numpy as np
import trimesh

def generate_stl(polygons, filename, thickness=0.05, border_size=0.02, ring_inrad=None):
    """
    Generate STL file from list of 2D polygons by extruding their borders (镂空) using trimesh for robustness.
    """
    meshes = []
    seen_edges = set()
    for poly in polygons:
        # Skip polygons outside unit circle
        centroid = np.mean(poly, axis=0)
        if np.linalg.norm(centroid) > 1.0:
            continue
        n = len(poly)
        for i in range(n):
            p1 = np.array(poly[i])
            p2 = np.array(poly[(i+1)%n])
            # Create edge key to avoid duplicates
            edge_key = tuple(sorted((tuple(np.round(p1, 12)), tuple(np.round(p2, 12)))))
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)
            # Generate rectangular border mesh
            border_mesh = generate_border_mesh(p1, p2, thickness, border_size)
            if border_mesh is not None:
                meshes.append(border_mesh)
    
    # Add outer ring if ring_inrad is provided
    if ring_inrad is not None:
        outer_ring_mesh = generate_outer_ring_mesh(ring_inrad, thickness, border_size)
        if outer_ring_mesh is not None:
            meshes.append(outer_ring_mesh)
    
    if not meshes:
        print("No meshes to generate!")
        return
    
    # Combine all meshes using trimesh
    combined = trimesh.util.concatenate(meshes)
    # Fix any issues and make manifold
    combined.fix_normals()
    combined.remove_duplicate_faces()
    combined.process(validate=True)
    
    # Export to STL
    combined.export(filename)
    print(f"Generated manifold STL with {len(combined.faces)} faces")

def generate_border_mesh(p1, p2, thickness, border_size):
    """Generate a rectangular border mesh around an edge."""
    # Compute edge direction
    edge_dir = p2 - p1
    edge_len = np.linalg.norm(edge_dir)
    if edge_len < 1e-12:
        return None
    edge_dir = edge_dir / edge_len
    # Compute perpendicular direction (for border width)
    perp_dir = np.array([-edge_dir[1], edge_dir[0]])
    # Compute 4 corner points for the rectangle (bottom face)
    p1a = p1 - border_size * perp_dir
    p1b = p1 + border_size * perp_dir
    p2a = p2 - border_size * perp_dir
    p2b = p2 + border_size * perp_dir
    
    # Create 2D polygon vertices (close the loop)
    vertices_2d = np.array([
        [p1a[0], p1a[1]],
        [p1b[0], p1b[1]],
        [p2b[0], p2b[1]],
        [p2a[0], p2a[1]],
        [p1a[0], p1a[1]]
    ])
    
    # Extrude 2D polygon to 3D using trimesh
    path = trimesh.load_path(vertices_2d)
    mesh = path.extrude(thickness)
    return mesh

def generate_outer_ring_mesh(ring_inrad, thickness, border_size):
    """Generate an outer ring mesh."""
    num_points = 100
    theta = np.linspace(0, 2*np.pi, num_points, endpoint=False)
    x = 1.0 * np.cos(theta)
    y = 1.0 * np.sin(theta)
    outer_circle = np.column_stack([x, y])
    
    meshes = []
    for i in range(num_points):
        p1 = outer_circle[i]
        p2 = outer_circle[(i + 1) % num_points]
        border_mesh = generate_border_mesh(p1, p2, thickness, border_size)
        if border_mesh is not None:
            meshes.append(border_mesh)
    
    if meshes:
        return trimesh.util.concatenate(meshes)
    return None