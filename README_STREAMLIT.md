# 🌀 Poincaré 双曲镶嵌生成器

这是一个基于 Streamlit 的交互式网站，用于生成和可视化 Poincaré 圆盘中的双曲镶嵌图案。

## ✨ 功能特点

### 1️⃣ 基础镶嵌生成
- 生成三种经典的双曲镶嵌：六边形、三角形、正方形
- 实时调整参数：
  - `p`: 多边形边数（3-10）
  - `q`: 每个顶点处的多边形数（3-10）
  - `k`: 递归深度（1-10）
  - `ring_inrad`: 外环内半径（0.5-1.0）
  - `phi`: 旋转角度
- 支持填充颜色或仅显示边框
- 可生成可 3D 打印的 STL 模型

### 2️⃣ 文字投影
- 将任意中文文字投影到双曲空间
- 创建独特的双曲文字艺术
- 可调参数：
  - 文字缩放倍数
  - 垂直偏移
  - 字符间距

### 3️⃣ 图片处理
- 上传图片并进行边界检测
- 提取线条投影到双曲空间
- 支持多种图片格式

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

应用将在 `http://localhost:8501` 启动。

## 📋 项目结构

```
poincare/
├── app.py                 # Streamlit 主应用
├── poincare.py           # 核心双曲镶嵌算法
├── poincare_lines.py     # 文字投影模块
├── plotter.py            # 绘图工具
├── char2lines.py         # 文字转线条工具
├── text2png.py           # 文字转图片工具
├── stlgen.py             # STL 模型生成
├── requirements.txt      # Python 依赖
└── .streamlit/
    └── config.toml       # Streamlit 配置
```

## 🔧 参数说明

### 镶嵌类型 `{p, q}`

在双曲几何中，`{p, q}` 表示：
- `p`: 多边形的边数
- `q`: 在每个顶点处相聚的多边形个数

常见的配置：
- `{7, 3}`: 七边形镶嵌（六边形视觉效果）
- `{3, 7}`: 三角形镶嵌
- `{4, 5}`: 正方形镶嵌

### 递归深度 `k`

- 值越大，镶嵌图案越复杂
- 建议值：3-8（过大会导致计算缓慢）

### 其他参数

- **边框大小**: 多边形边框的粗细
- **环内半径**: 3D 模型外环的内半径
- **旋转角度**: 初始多边形的旋转角度
- **填充颜色**: 根据到原点的距离用不同颜色填充

## 💡 使用示例

### 生成基础镶嵌
1. 在左侧边栏选择"基础镶嵌生成"
2. 选择镶嵌类型（hex、tri 或 square）
3. 调整参数查看实时预览
4. 点击"下载 STL 模型"进行 3D 打印

### 创建文字艺术
1. 在左侧边栏选择"文字投影"
2. 输入要投影的文字
3. 调整缩放、偏移等参数
4. 查看投影结果

### 处理图片
1. 在左侧边栏选择"图片处理"
2. 上传图片
3. 调整阈值和参数
4. 查看边界检测结果

## 📚 数学背景

### 双曲几何
在双曲几何中，平行公设不成立。Poincaré 圆盘是一种常见的双曲几何模型，
其中：
- 双曲直线表示为与单位圆正交的圆弧
- 距离和角度的度量遵循双曲度量

### 镶嵌
双曲镶嵌是指用全等的双曲多边形完全覆盖平面的方式。
与欧几里得镶嵌不同，双曲镶嵌具有分形特性。

## 🎨 高级定制

### 修改颜色配置

编辑 `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### 调整 STL 生成参数

在 `app.py` 中修改 `stlgen.generate_stl()` 的调用参数

## 🐛 故障排除

### 问题：STL 生成失败
**解决方案**: 确保 `trimesh` 已正确安装
```bash
pip install --upgrade trimesh numpy-stl
```

### 问题：文字投影错误
**解决方案**: 确保系统中有中文字体（微软雅黑、黑体或宋体）

### 问题：图片处理缓慢
**解决方案**: 减小图片尺寸或降低处理精度

## 📖 参考资源

- [Poincaré 圆盘模型 - Wikipedia](https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model)
- [双曲镶嵌 - Wikipedia](https://en.wikipedia.org/wiki/Hyperbolic_tiling)
- [Streamlit 文档](https://docs.streamlit.io/)
- [Matplotlib 文档](https://matplotlib.org/)

## 📄 许可证

该项目源自 Gitee 上的开源项目。详见 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

有问题或建议？请提交 GitHub Issue。

---

**祝您使用愉快！** 🎉
