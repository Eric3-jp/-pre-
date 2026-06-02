from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Polygon
from PIL import Image

from plotter import plotlinecurves
from poincare import CONFIGS, hyperbolic_tessellation
from poincare_lines import text_to_poincare

APP_TITLE = "Poincaré 双曲镶嵌生成器"
MODES = ["基础镶嵌生成", "文字投影", "图片处理"]


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def get_tessellation(p: int, q: int, phi: float, depth: int):
    return hyperbolic_tessellation(p, q, phi, depth)


def create_tessellation_figure(polygons, fill_color: bool, border_size: float):
    fig, ax = plt.subplots(figsize=(8, 8), dpi=120)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor="black", linewidth=2))

    patches = []
    cmap = plt.get_cmap("viridis")
    linewidth = max(0.5, border_size * 20)

    for poly in polygons:
        centroid = np.mean(poly, axis=0)
        if np.linalg.norm(centroid) > 1.2:
            continue

        face_color = cmap(np.linalg.norm(centroid)) if fill_color else "none"
        patches.append(
            Polygon(
                poly,
                closed=True,
                facecolor=face_color,
                edgecolor="black",
                linewidth=linewidth,
            )
        )

    ax.add_collection(PatchCollection(patches, match_original=True))
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    return fig


def render_tessellation_mode():
    st.header("基础镶嵌生成")
    st.write("生成不同的双曲镶嵌图案，并调整参数查看实时效果。")

    controls, preview = st.columns([1, 3])

    with controls:
        st.subheader("参数设置")
        config_key = st.selectbox(
            "镶嵌类型",
            list(CONFIGS.keys()),
            format_func=lambda key: f"{key} (p={CONFIGS[key]['p']}, q={CONFIGS[key]['q']})",
            help="选择预置的双曲镶嵌类型。",
        )
        cfg = CONFIGS[config_key]
        p = st.slider("p（多边形边数）", 3, 10, cfg["p"])
        q = st.slider("q（顶点处多边形数）", 3, 10, cfg["q"])
        depth = st.slider("递归深度", 1, 8, min(cfg["k"], 8), help="越大越复杂，计算也越慢。")
        ring_inrad = st.slider("外环内半径", 0.5, 1.0, cfg["ring_inrad"], 0.01)
        phi = st.slider("旋转角度（弧度）", 0.0, float(2 * np.pi), 0.0, 0.1)
        border_size = st.slider("边框大小", 0.005, 0.05, 0.02, 0.005)
        fill_color = st.checkbox("填充颜色", False)
        generate_stl = st.checkbox("生成 STL 模型", False, help="需要安装 trimesh。")

    with preview:
        st.subheader("预览")
        try:
            with st.spinner("生成中..."):
                polygons = get_tessellation(p, q, phi, depth)
                fig = create_tessellation_figure(polygons, fill_color, border_size)
                st.pyplot(fig)
                plt.close(fig)

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("多边形数量", len(polygons))
            col_b.metric("递归深度", depth)
            col_c.metric("配置", f"({p}, {q})")

            if generate_stl:
                render_stl_download(polygons, config_key, ring_inrad, border_size)
        except Exception as exc:
            st.error(f"生成失败：{exc}")


def render_stl_download(polygons, config_key: str, ring_inrad: float, border_size: float):
    try:
        import stlgen

        with TemporaryDirectory() as tmp_dir:
            stl_name = f"poincare_{config_key}_custom.stl"
            stl_path = Path(tmp_dir) / stl_name
            with st.spinner("生成 STL 文件中..."):
                stlgen.generate_stl(
                    polygons,
                    str(stl_path),
                    border_size=border_size,
                    ring_inrad=ring_inrad,
                )

            if not stl_path.exists():
                st.warning("STL 文件未生成，请降低递归深度或调整参数后重试。")
                return

            st.download_button(
                label="下载 STL 模型",
                data=stl_path.read_bytes(),
                file_name=stl_name,
                mime="application/octet-stream",
            )
    except Exception as exc:
        st.warning(f"STL 生成失败：{exc}")


def render_text_mode():
    st.header("文字投影到双曲空间")
    st.write("将文字轮廓投影到 Poincaré 圆盘，创建双曲文字艺术。")

    controls, preview = st.columns([1, 3])

    with controls:
        st.subheader("文字设置")
        text_input = st.text_input("输入文字", "你好", max_chars=20)
        scale_multiplier = st.slider("文字缩放", 0.5, 3.0, 1.0, 0.1)
        y_offset = st.slider("垂直偏移", -1.0, 1.0, 0.0, 0.1)
        char_spacing = st.slider("字符间距", 0.05, 0.3, 0.15, 0.01)

    with preview:
        st.subheader("投影结果")
        if not text_input.strip():
            st.info("请输入要投影的文字。")
            return

        try:
            with st.spinner("投影处理中..."):
                _, poincare_curves = text_to_poincare(
                    text_input.strip(),
                    scale_multiplier=scale_multiplier,
                    char_spacing=char_spacing,
                    y_offset=y_offset,
                )
                fig, ax = plt.subplots(figsize=(8, 8), dpi=120)
                ax.set_aspect("equal")
                plotlinecurves(poincare_curves, ax=ax, title=f"'{text_input}' 的双曲投影")
                st.pyplot(fig)
                plt.close(fig)
            st.success("文字投影完成。")
        except Exception as exc:
            st.error(f"处理失败：{exc}")


def render_image_mode():
    st.header("图片线条提取")
    st.write("上传图片并提取边缘线条。双曲投影部分仍需后续接入线段追踪算法。")

    controls, preview = st.columns([1, 3])

    with controls:
        st.subheader("图片设置")
        uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png", "bmp"])
        threshold = st.slider("边界检测阈值", 50, 200, 100, 10)

    with preview:
        st.subheader("处理结果")
        if uploaded_file is None:
            st.info("请上传一张图片。")
            return

        try:
            import cv2

            image = Image.open(uploaded_file)
            image_array = np.array(image)
            st.image(image, caption="原始图片", use_container_width=True)

            if image_array.ndim == 3:
                gray = np.dot(image_array[..., :3], [0.2989, 0.5870, 0.1140])
            else:
                gray = image_array

            with st.spinner("处理中..."):
                edges = cv2.Canny(gray.astype(np.uint8), threshold, threshold * 2)
                fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
                ax.imshow(edges, cmap="gray")
                ax.set_title("边界检测结果")
                ax.axis("off")
                st.pyplot(fig)
                plt.close(fig)

            st.info("当前已完成边缘检测；如需真正投影图片线条，需要增加轮廓线段化模块。")
        except Exception as exc:
            st.error(f"处理失败：{exc}")


def render_footer():
    st.markdown("---")
    st.markdown(
        """
### 关于项目
这个工具基于 **Poincaré 圆盘模型** 的双曲几何，可生成双曲镶嵌图案、STL 模型和文字投影效果。

### 资源
- [Poincaré 圆盘模型](https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model)
- [双曲镶嵌](https://en.wikipedia.org/wiki/Hyperbolic_tiling)
- [原始项目](https://gitee.com/geyiheng_sjtu/poincare)
"""
    )


def main():
    st.title("🌀 Poincaré 双曲镶嵌生成器")
    st.markdown("使用双曲几何创建镶嵌图案、文字艺术和 3D 打印模型。")

    st.sidebar.header("选择功能")
    mode = st.sidebar.radio("功能选择", MODES)

    if mode == "基础镶嵌生成":
        render_tessellation_mode()
    elif mode == "文字投影":
        render_text_mode()
    else:
        render_image_mode()

    render_footer()


if __name__ == "__main__":
    main()
