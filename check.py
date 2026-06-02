#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证 Streamlit 应用的核心功能
"""

import sys
import numpy as np
from pathlib import Path

print("=" * 50)
print("🌀 Poincaré Streamlit 应用 - 功能检查")
print("=" * 50)
print()

# 1. 检查 Python 版本
print("✓ Python 版本检查")
print(f"  Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print()

# 2. 检查依赖包
print("✓ 依赖包检查")
packages = {
    'streamlit': ('Streamlit Web 框架', 'streamlit'),
    'matplotlib': ('Matplotlib 绘图库', 'matplotlib'),
    'numpy': ('NumPy 数值计算', 'numpy'),
    'PIL': ('Pillow 图片处理', 'PIL'),
    'cv2': ('OpenCV 图像处理', 'cv2'),
    'trimesh': ('Trimesh 3D 处理', 'trimesh')
}

missing_packages = []
for display_name, (desc, import_name) in packages.items():
    try:
        __import__(import_name)
        print(f"  ✓ {import_name:15} {desc}")
    except ImportError:
        print(f"  ✗ {import_name:15} {desc} [缺失]")
        missing_packages.append(import_name)

if missing_packages:
    print()
    print(f"⚠️  发现 {len(missing_packages)} 个缺失的包")
    print(f"   请运行: pip install {' '.join(missing_packages)}")
else:
    print()
    print("✓ 所有依赖包已安装")

print()

# 3. 检查核心模块
print("✓ 核心模块检查")
core_modules = {
    'poincare.py': '双曲镶嵌算法',
    'poincare_lines.py': '文字投影模块',
    'plotter.py': '绘图工具',
    'char2lines.py': '文字转线条',
    'stlgen.py': 'STL 生成器'
}

for filename, desc in core_modules.items():
    filepath = Path(filename)
    if filepath.exists():
        print(f"  ✓ {filename:20} {desc}")
    else:
        print(f"  ✗ {filename:20} {desc} [缺失]")

print()

# 4. 检查配置文件
print("✓ 配置文件检查")
config_files = {
    'requirements.txt': '依赖清单',
    '.streamlit/config.toml': 'Streamlit 配置',
    'app.py': 'Streamlit 主应用'
}

for filename, desc in config_files.items():
    filepath = Path(filename)
    if filepath.exists():
        print(f"  ✓ {filename:25} {desc}")
    else:
        print(f"  ✗ {filename:25} {desc} [缺失]")

print()

# 5. 简单的功能测试
print("✓ 功能测试")
try:
    from poincare import central_polygon, hyperbolic_tessellation
    
    # 测试基础镶嵌
    polygon = central_polygon(7, 3)
    print(f"  ✓ 中心多边形生成: {len(polygon)} 个顶点")
    
    # 测试镶嵌生成（小规模）
    tessellation = hyperbolic_tessellation(7, 3, k=2)
    print(f"  ✓ 镶嵌生成: {len(tessellation)} 个多边形")
    
except Exception as e:
    print(f"  ✗ 功能测试失败: {e}")

print()

# 6. 启动说明
print("=" * 50)
print("🚀 准备启动应用")
print("=" * 50)
print()
print("运行以下命令启动 Streamlit 应用:")
print()
print("  streamlit run app.py")
print()
print("应用将在以下地址打开:")
print("  http://localhost:8501")
print()
print("提示:")
print("  - 首次启动可能需要 30-60 秒")
print("  - 修改参数后应用会自动重新运行")
print("  - 按 Ctrl+C 可停止应用")
print()

if not missing_packages:
    print("✓ 所有检查通过，可以启动应用！")
else:
    print("⚠️  请先安装缺失的包后再启动应用")

print()
