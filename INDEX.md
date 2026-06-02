# 📖 Poincaré Streamlit 项目 - 文件索引

## 🎯 快速导航

### 🚀 立即开始
1. **[QUICK_START.md](QUICK_START.md)** ⭐ - **从这里开始！**
   - 三步启动应用
   - 常见操作
   - 快速示例

### 📚 完整指南
2. **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - 详细使用手册
   - 功能概览
   - 参数详解
   - 常见问题

3. **[README_STREAMLIT.md](README_STREAMLIT.md)** - 项目文档
   - 功能介绍
   - 数学背景
   - 高级用法

### 📋 项目信息
4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 完成总结
   - 已完成工作
   - 技术栈
   - 扩展方向

---

## 📁 文件结构

### 📂 应用文件（新建）

#### 主应用
```
app.py                      (400+ 行)
├─ 基础镶嵌生成模块
├─ 文字投影模块
├─ 图片处理模块
└─ UI 界面和布局
```

#### 配置
```
.streamlit/config.toml     
├─ 主题配置
├─ 服务器设置
└─ 日志配置
```

#### 启动脚本
```
run.bat                    - Windows 批处理脚本
run.ps1                    - PowerShell 脚本
check.py                   - 功能检查脚本
```

#### 文档
```
QUICK_START.md             - 快速启动指南
USAGE_GUIDE.md             - 详细使用指南
README_STREAMLIT.md        - 完整项目文档
PROJECT_SUMMARY.md         - 项目总结
INDEX.md                   - 本文件
requirements.txt           - 依赖清单
```

### 📂 原始项目文件（已集成）

```
poincare.py               - 双曲镶嵌算法核心
poincare_lines.py         - 文字投影模块
plotter.py                - 绘图工具
char2lines.py             - 文字转线条
text2png.py               - 文字转图片
stlgen.py                 - STL 生成器
```

### 📂 示例和资源

```
poincare_hex.stl          - 六边形镶嵌 3D 模型
poincare_tri.stl          - 三角形镶嵌 3D 模型
poincare_square.stl       - 正方形镶嵌 3D 模型
你好.png                  - 示例文字图像
你好_poincare.png         - 投影后的效果
```

---

## 🎯 按用途查找文件

### 我想快速启动应用
→ **[QUICK_START.md](QUICK_START.md)**

### 我想了解如何使用各个功能
→ **[USAGE_GUIDE.md](USAGE_GUIDE.md)**

### 我想修改参数或自定义功能
→ **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - 高级用法部分

### 我想了解项目完成情况
→ **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**

### 我想查看完整的技术文档
→ **[README_STREAMLIT.md](README_STREAMLIT.md)**

### 我想诊断问题或检查依赖
→ 运行 `python check.py`

### 我想查看所有文件
→ 本文件 **[INDEX.md](INDEX.md)**

---

## 🚀 启动应用

### 推荐方式 1: 双击启动
- **Windows 用户**：双击 `run.bat`
- **PowerShell 用户**：双击 `run.ps1`

### 推荐方式 2: 命令行
```bash
cd "c:\Users\21140\Desktop\数学的天空网站\poincare"
streamlit run app.py
```

应用将在 `http://localhost:8501` 打开

---

## 📊 应用功能速览

### 模块 1: 基础镶嵌生成
- 生成双曲镶嵌图案
- 支持 hex、tri、square 三种类型
- 实时参数调整
- STL 模型导出

### 模块 2: 文字投影
- 投影文字到双曲空间
- 支持中文、英文、符号
- 参数调整（缩放、偏移、间距）
- 实时预览

### 模块 3: 图片处理
- 上传图片
- 边界检测
- 线条提取
- 投影处理（开发中）

---

## 🔧 关键配置

### Python 版本
```
Python 3.12.10
```

### 主要依赖包
```
streamlit==1.28.1
matplotlib==3.8.2
numpy==1.24.3
pillow==10.1.0
opencv-python-headless==4.8.1.78
trimesh==4.0.0
```

完整依赖：[requirements.txt](requirements.txt)

---

## 🎓 技术栈

### Web 框架
- **Streamlit** - 交互式 Web 应用框架

### 数值计算
- **NumPy** - 矩阵和数组运算
- **SciPy** - 高级数学算法

### 图形和可视化
- **Matplotlib** - 2D 绘图
- **Pillow** - 图片操作
- **OpenCV** - 图像处理

### 3D 处理
- **Trimesh** - 3D 网格处理
- **NumPy-STL** - STL 格式支持

---

## 📈 项目统计

| 项目             | 数值  |
| ---------------- | ----- |
| 总文件数         | 20+   |
| Python 代码行数  | 1000+ |
| 文档行数         | 500+  |
| 功能模块数       | 3     |
| 支持的镶嵌类型   | 3     |
| 最大参数调整范围 | 20+   |

---

## 🆘 快速故障排除

### 问题：应用无法启动
**解决方案**：
```bash
python check.py  # 运行检查脚本
pip install -r requirements.txt  # 重新安装依赖
```

### 问题：端口被占用
**解决方案**：
```bash
streamlit run app.py --server.port=8502
```

### 问题：文字显示错误
**解决方案**：
- 确保系统有中文字体（微软雅黑、黑体或宋体）
- 尝试减少输入的字符数

### 问题：内存不足
**解决方案**：
- 降低镶嵌的 k 值
- 减小图片尺寸
- 关闭其他应用

更多问题：查看 [USAGE_GUIDE.md](USAGE_GUIDE.md) 的"常见问题"部分

---

## 💡 使用建议

1. **首次使用**：阅读 [QUICK_START.md](QUICK_START.md)
2. **遇到问题**：查看 [USAGE_GUIDE.md](USAGE_GUIDE.md)
3. **想要深入**：阅读 [README_STREAMLIT.md](README_STREAMLIT.md)
4. **检查依赖**：运行 `python check.py`
5. **修改参数**：查看 [USAGE_GUIDE.md](USAGE_GUIDE.md) 的参数表

---

## 📞 支持

### 获取帮助
1. 运行 `python check.py` 检查环境
2. 查看相关文档文件
3. 检查浏览器控制台（F12）是否有错误
4. 尝试清除浏览器缓存

### 报告问题
- 检查所有文档中的常见问题部分
- 查看终端输出是否有错误信息

---

## 📝 文件修改指南

### 想要修改应用界面
编辑：`app.py`

### 想要修改镶嵌参数
编辑：`app.py` 中的参数范围
或修改：`poincare.py` 中的 CONFIGS

### 想要修改主题颜色
编辑：`.streamlit/config.toml`

### 想要添加新功能
1. 在 `app.py` 中添加新的选项卡
2. 集成相应的模块功能
3. 更新文档

---

## 🎉 开始使用

**准备好了吗？** 

👉 **现在就启动应用：** [QUICK_START.md](QUICK_START.md)

---

## 📚 完整文档列表

| 文件                | 说明         | 长度    |
| ------------------- | ------------ | ------- |
| QUICK_START.md      | 快速启动指南 | 200+ 行 |
| USAGE_GUIDE.md      | 详细使用指南 | 400+ 行 |
| README_STREAMLIT.md | 完整项目文档 | 300+ 行 |
| PROJECT_SUMMARY.md  | 项目完成总结 | 350+ 行 |
| INDEX.md            | 本文件       | 本体    |
| requirements.txt    | Python 依赖  | 7 行    |

---

**祝您使用愉快！** 🚀✨

最后更新：2026 年 6 月 2 日
