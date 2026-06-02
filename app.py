import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
from PIL import Image
import io
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from poincare import (
    hyperbolic_tessellation, 
    plot_tessellation, 
    hyperbolic_line,
    CONFIGS
)
from poincare_lines import text_to_poincare
from plotter import plotlinecurves

# Page configuration
st.set_page_config(
    page_title="Poincaré 双曲镶嵌生成器",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌀 Poincaré 双曲镶嵌生成器")
st.markdown("使用双曲几何创建美丽的镶嵌图案和文字艺术")

# Sidebar for mode selection
st.sidebar.header("选择功能")
mode = st.sidebar.radio(
    "功能选择",
    ["基础镶嵌生成", "文字投影", "图片处理"],
    help="选择您想要使用的功能"
)

# ==================== 模式1: 基础镶嵌生成 ====================
if mode == "基础镶嵌生成":
    st.header("基础镶嵌生成")
    st.write("生成不同的双曲镶嵌图案，并调整参数查看实时效果")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("参数设置")
        
        # Tessellation type selection
        config_key = st.selectbox(
            "镶嵌类型",
            list(CONFIGS.keys()),
            format_func=lambda x: f"{x} ({{p={CONFIGS[x]['p']}, q={CONFIGS[x]['q']}}})",
            help="选择不同的镶嵌类型"
        )
        
        cfg = CONFIGS[config_key]
        
        # Parameters
        p = st.slider("p (多边形边数)", 3, 10, cfg['p'], 
                      help="多边形的边数")
        q = st.slider("q (顶点处的多边形数)", 3, 10, cfg['q'],
                      help="每个顶点处相聚的多边形数")
        k = st.slider("k (递归深度)", 1, 10, cfg['k'],
                      help="镶嵌的递归深度，越大越复杂")
        ring_inrad = st.slider("环内半径", 0.5, 1.0, cfg['ring_inrad'], 0.01,
                               help="外环的内半径")
        phi = st.slider("旋转角度 (弧度)", 0.0, 2*np.pi, 0.0, 0.1,
                        help="初始多边形的旋转角度")
        
        fill_color = st.checkbox("填充颜色", False,
                                 help="是否用颜色填充多边形")
        border_size = st.slider("边框大小", 0.005, 0.05, 0.02, 0.005)
        
        generate_stl = st.checkbox("生成 STL 模型", True,
                                   help="是否生成可 3D 打印的 STL 文件")
    
    with col2:
        st.subheader("预览")
        
        # Generate tessellation
        try:
            with st.spinner("生成中..."):
                polygons = hyperbolic_tessellation(p, q, phi, k)
                
                # Create plot
                fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
                ax.set_aspect('equal')
                ax.axis('off')
                
                # Draw unit circle
                unit_circle = Circle((0, 0), 1, fill=False, edgecolor='black', linewidth=2)
                ax.add_patch(unit_circle)
                
                # Draw polygons
                patches = []
                linewidth = max(0.5, border_size * 20)
                
                for poly in polygons:
                    centroid = np.mean(poly, axis=0)
                    if np.linalg.norm(centroid) > 1.2:
                        continue
                    
                    if fill_color:
                        color_val = np.linalg.norm(centroid)
                        cmap = plt.get_cmap('viridis')
                        face_color = cmap(color_val)
                    else:
                        face_color = 'none'
                    
                    poly_patch = Polygon(poly, closed=True, facecolor=face_color, 
                                        edgecolor='black', linewidth=linewidth)
                    patches.append(poly_patch)
                
                collection = PatchCollection(patches, match_original=True)
                ax.add_collection(collection)
                ax.set_xlim(-1.1, 1.1)
                ax.set_ylim(-1.1, 1.1)
                
                st.pyplot(fig)
                plt.close(fig)
                
                # Display statistics
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("多边形数量", len(polygons))
                with col_b:
                    st.metric("递归深度", k)
                with col_c:
                    st.metric("配置", f"({p},{q})")
                
                # Generate STL if requested
                if generate_stl:
                    st.info("💡 STL 模型生成功能需要 trimesh 和 numpy-stl")
                    try:
                        import stlgen
                        with st.spinner("生成 STL 文件中..."):
                            stl_filename = f"poincare_{config_key}_custom.stl"
                            stlgen.generate_stl(
                                polygons,
                                stl_filename,
                                border_size=border_size,
                                ring_inrad=ring_inrad
                            )
                            with open(stl_filename, "rb") as f:
                                st.download_button(
                                    label="📥 下载 STL 模型",
                                    data=f.read(),
                                    file_name=stl_filename,
                                    mime="application/octet-stream"
                                )
                            st.success("✅ STL 文件已生成！")
                    except Exception as e:
                        st.warning(f"⚠️ STL 生成失败: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ 生成失败: {str(e)}")


# ==================== 模式2: 文字投影 ====================
elif mode == "文字投影":
    st.header("文字投影到双曲空间")
    st.write("将您输入的文字投影到 Poincaré 圆盘，创建独特的双曲文字艺术")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("文字设置")
        text_input = st.text_input(
            "输入文字",
            "你好",
            max_chars=20,
            help="输入要投影的文字（最多20个字符）"
        )
        
        scale_multiplier = st.slider(
            "文字缩放",
            0.5, 3.0, 1.0, 0.1,
            help="调整文字的大小"
        )
        
        y_offset = st.slider(
            "垂直偏移",
            -1.0, 1.0, 0.0, 0.1,
            help="调整文字的垂直位置"
        )
        
        char_spacing = st.slider(
            "字符间距",
            0.05, 0.3, 0.15, 0.01,
            help="调整字符之间的间距"
        )
    
    with col2:
        st.subheader("投影结果")
        
        if text_input.strip():
            try:
                with st.spinner("投影处理中..."):
                    # Generate poincare projection
                    lines, poincare_curves = text_to_poincare(text_input, scale_multiplier)
                    
                    # Plot result
                    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
                    ax.set_aspect('equal')
                    
                    plotlinecurves(poincare_curves, ax=ax, title=f"'{text_input}' 的双曲投影")
                    
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    st.success("✅ 文字投影完成！")
            except Exception as e:
                st.error(f"❌ 处理失败: {str(e)}")
        else:
            st.info("👆 请输入要投影的文字")


# ==================== 模式3: 图片处理 ====================
elif mode == "图片处理":
    st.header("图片线条提取与投影")
    st.write("上传一张图片，提取线条后投影到双曲空间")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("图片设置")
        
        uploaded_file = st.file_uploader(
            "上传图片",
            type=["jpg", "jpeg", "png", "bmp"],
            help="上传一张图片进行处理"
        )
        
        if uploaded_file is not None:
            threshold = st.slider(
                "边界检测阈值",
                50, 200, 100, 10,
                help="用于检测图片边界的阈值"
            )
            
            min_line_length = st.slider(
                "最小线条长度",
                5, 50, 20, 5,
                help="过滤掉过短的线条"
            )
            
            scale_factor = st.slider(
                "缩放因子",
                0.2, 2.0, 1.0, 0.1,
                help="调整投影的大小"
            )
    
    with col2:
        st.subheader("处理结果")
        
        if uploaded_file is not None:
            try:
                # Read image
                image = Image.open(uploaded_file)
                image_array = np.array(image)
                
                # Display original image
                st.image(image, caption="原始图片", use_column_width=True)
                
                # Convert to grayscale
                if len(image_array.shape) == 3:
                    gray = np.dot(image_array[...,:3], [0.2989, 0.5870, 0.1140])
                else:
                    gray = image_array
                
                # Edge detection
                import cv2
                with st.spinner("处理中..."):
                    edges = cv2.Canny(gray.astype(np.uint8), threshold, threshold * 2)
                    
                    # Display edges
                    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
                    ax.imshow(edges, cmap='gray')
                    ax.set_title("边界检测结果")
                    ax.axis('off')
                    st.pyplot(fig)
                    plt.close(fig)
                
                st.info("💡 线条提取和双曲投影功能正在开发中...")
                
            except Exception as e:
                st.error(f"❌ 处理失败: {str(e)}")
        else:
            st.info("👆 请上传一张图片")


# Footer
st.markdown("---")
st.markdown("""
### 📚 关于项目
这个工具基于 **Poincaré 圆盘模型** 的双曲几何。它可以生成美丽的镶嵌图案，
并将文字投影到双曲空间中，创建独特的视觉效果。

### 🔗 资源
- [Poincaré 圆盘模型](https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model)
- [双曲镶嵌](https://en.wikipedia.org/wiki/Hyperbolic_tiling)
- [GitHub 项目](https://gitee.com/geyiheng_sjtu/poincare)
""")
