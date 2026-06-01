import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
import sys

def find_chinese_font():
    font_names = [
        "Microsoft YaHei",
        "SimHei",
        "SimSun",
        "Arial Unicode MS"
    ]
    for name in font_names:
        try:
            font = FontProperties(family=name)
            return font
        except:
            continue
    return FontProperties()

def text2lines(text, char_spacing=0.15, y_offset=0.0):
    font = find_chinese_font()
    
    all_lines = []
    char_bboxes = []
    char_paths = []
    
    for char in text:
        path = TextPath((0, 0), char, size=1.0, prop=font)
        vertices = path.vertices
        codes = path.codes
        
        if len(vertices) > 0:
            min_x = np.min(vertices[:, 0])
            max_x = np.max(vertices[:, 0])
            min_y = np.min(vertices[:, 1])
            max_y = np.max(vertices[:, 1])
            char_bboxes.append((min_x, max_x, min_y, max_y))
            char_paths.append(path)
    
    if not char_bboxes:
        return []
    
    total_width = sum(max_x - min_x for min_x, max_x, _, _ in char_bboxes)
    total_spacing = char_spacing * (len(char_bboxes) - 1)
    total_needed = total_width + total_spacing
    
    scale = 1.8 / total_needed if total_needed > 1.8 else 1.0
    start_x = -0.9
    
    for path, (min_x, max_x, min_y, max_y) in zip(char_paths, char_bboxes):
        offset_x = start_x - min_x * scale
        offset_y = y_offset - (min_y + (max_y - min_y) / 2) * scale
        
        polygons = path.to_polygons()
        for poly in polygons:
            if len(poly) >= 2:
                transformed = poly * scale + np.array([offset_x, offset_y])
                for i in range(len(transformed) - 1):
                    p1 = transformed[i]
                    p2 = transformed[i + 1]
                    all_lines.append([p1.tolist(), p2.tolist()])
        
        start_x += (max_x - min_x) * scale + char_spacing
    
    return all_lines
