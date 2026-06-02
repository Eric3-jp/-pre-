from pathlib import Path
from tempfile import TemporaryDirectory
import io

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Polygon
from PIL import Image

from plotter import plot_fisheye_lines
from poincare import CONFIGS, hyperbolic_tessellation
from poincare_lines import text_to_fisheye

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
    st.write("将文字轮廓投影到 Poincaré 圆盘，创建鱼眼文字艺术。")

    controls, preview = st.columns([1, 3])

    with controls:
        st.subheader("文字设置")
        text_input = st.text_input("输入文字", "你好", max_chars=20)
        scale_multiplier = st.slider("文字缩放", 0.5, 3.0, 1.0, 0.1)
        y_offset = st.slider("垂直偏移", -1.0, 1.0, 0.0, 0.1)
        char_spacing = st.slider("字符间距", 0.05, 0.3, 0.15, 0.01)
        fisheye_strength = st.slider(
            "鱼眼强度",
            0.0,
            4.0,
            1.6,
            0.1,
            help="0 表示不变形，数值越大越接近鱼眼镜头的径向压缩效果。",
        )

    with preview:
        st.subheader("投影结果")
        if not text_input.strip():
            st.info("请输入要投影的文字。")
            return

        try:
            with st.spinner("投影处理中..."):
                _, fisheye_lines = text_to_fisheye(
                    text_input.strip(),
                    scale_multiplier=scale_multiplier,
                    char_spacing=char_spacing,
                    y_offset=y_offset,
                    strength=fisheye_strength,
                )
                fig, ax = plt.subplots(figsize=(8, 8), dpi=120)
                ax.set_aspect("equal")
                plot_fisheye_lines(fisheye_lines, ax=ax, title=f"'{text_input}' 的鱼眼投影")
                st.pyplot(fig)
                plt.close(fig)
            st.success("鱼眼投影完成。")
        except Exception as exc:
            st.error(f"处理失败：{exc}")


def resize_image_for_display(image_array, max_size=1200):
    height, width = image_array.shape[:2]
    scale = min(1.0, max_size / max(height, width))
    if scale >= 1.0:
        return image_array

    import cv2

    new_size = (int(width * scale), int(height * scale))
    return cv2.resize(image_array, new_size, interpolation=cv2.INTER_AREA)


def apply_fisheye_to_image(image_array, strength=1.6, zoom=1.0, circular_mask=True, background=(0, 0, 0)):
    import cv2

    source = resize_image_for_display(image_array)
    height, width = source.shape[:2]
    cx = (width - 1) / 2
    cy = (height - 1) / 2
    radius = min(cx, cy) * max(zoom, 1e-6)

    y, x = np.indices((height, width), dtype=np.float32)
    dx = x - cx
    dy = y - cy
    r_out = np.sqrt(dx * dx + dy * dy)
    theta = np.arctan2(dy, dx)
    normalized_out = r_out / radius

    if strength <= 1e-6:
        normalized_in = normalized_out
    else:
        normalized_in = np.arctanh(np.clip(normalized_out, 0, 0.999999) * np.tanh(strength)) / strength

    r_in = normalized_in * radius
    map_x = cx + r_in * np.cos(theta)
    map_y = cy + r_in * np.sin(theta)

    valid = normalized_out <= 1.0
    map_x = np.where(valid, map_x, -1).astype(np.float32)
    map_y = np.where(valid, map_y, -1).astype(np.float32)
    warped = cv2.remap(source, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=background)

    if circular_mask:
        result = np.zeros_like(warped)
        result[:, :] = np.array(background, dtype=np.uint8)
        result[valid] = warped[valid]
        return result

    return warped


def image_to_png_bytes(image_array):
    image = Image.fromarray(image_array.astype(np.uint8))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def render_image_mode():
    st.header("图片鱼眼镜头")
    st.write("直接对整张图片做像素级鱼眼畸变，保留颜色、纹理和明暗，更接近真实鱼眼相机效果。")

    controls, preview = st.columns([1, 3])

    with controls:
        st.subheader("图片设置")
        uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png", "bmp"])
        fisheye_strength = st.slider(
            "鱼眼强度",
            0.0,
            4.0,
            1.6,
            0.1,
            help="0 表示不变形；数值越大，中心膨胀和边缘压缩越明显。",
        )
        zoom = st.slider("镜头缩放", 0.5, 1.5, 1.0, 0.05, help="控制鱼眼镜头覆盖范围。")
        crop_to_circle = st.checkbox(
            "裁成圆形镜头",
            True,
            help="开启后只保留圆形鱼眼视野，圆外填黑；关闭后显示完整矩形画布。",
        )
        show_original = st.checkbox("显示原始图片", False)

    with preview:
        st.subheader("处理结果")
        if uploaded_file is None:
            st.info("请上传一张图片。")
            return

        try:
            image = Image.open(uploaded_file).convert("RGB")
            image_array = np.array(image)

            if show_original:
                st.image(image, caption="原始图片", use_container_width=True)

            with st.spinner("正在生成真实鱼眼图片..."):
                fisheye_image = apply_fisheye_to_image(
                    image_array,
                    strength=fisheye_strength,
                    zoom=zoom,
                    circular_mask=crop_to_circle,
                )

            st.image(fisheye_image, caption="真实鱼眼图片", use_container_width=True)
            st.download_button(
                "下载鱼眼 PNG",
                data=image_to_png_bytes(fisheye_image),
                file_name="fisheye_image.png",
                mime="image/png",
            )
        except Exception as exc:
            st.error(f"处理失败：{exc}")

def render_footer():
    st.markdown("---")
    st.markdown(
        """
### 关于项目
这个工具基于 **Poincaré 圆盘模型** 的双曲几何，可生成双曲镶嵌图案、STL 模型和文字/图片鱼眼投影效果。

### 资源
- [Poincaré 圆盘模型](https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model)
- [双曲镶嵌](https://en.wikipedia.org/wiki/Hyperbolic_tiling)
- [原始项目](https://gitee.com/geyiheng_sjtu/poincare)
"""
    )


def main():
    st.title("🌀 Poincaré 双曲镶嵌生成器")
    st.markdown("使用双曲几何创建镶嵌图案、文字艺术、图片鱼眼投影和 3D 打印模型。")

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
