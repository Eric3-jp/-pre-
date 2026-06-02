# 🚀 第二阶段：部署到公网（Streamlit Community Cloud）

## 📋 部署清单

本指南将帮助您将应用部署到 Streamlit Community Cloud，让所有人都能通过网址访问！

---

## ✅ 第一步：准备依赖文件

### 验证 requirements.txt

您的项目已有 `requirements.txt` 文件，位置：
```
c:\Users\21140\Desktop\数学的天空网站\poincare\requirements.txt
```

### 📝 当前依赖列表

```
streamlit==1.28.1
matplotlib==3.8.2
numpy==1.24.3
Pillow==10.1.0
opencv-python==4.8.1.78
trimesh==4.0.0
scikit-image==0.22.0
```

✅ **所有必要的库都已列出！**

### 💡 依赖说明

| 库                | 版本     | 用途         |
| ----------------- | -------- | ------------ |
| **streamlit**     | 1.28.1   | Web 应用框架 |
| **matplotlib**    | 3.8.2    | 绘图库       |
| **numpy**         | 1.24.3   | 数值计算     |
| **Pillow**        | 10.1.0   | 图片处理     |
| **opencv-python** | 4.8.1.78 | 图像处理     |
| **trimesh**       | 4.0.0    | 3D 模型处理  |
| **scikit-image**  | 0.22.0   | 图像处理算法 |

---

## ✅ 第二步：准备 GitHub 仓库

### 2.1 初始化 Git 仓库（如果还未做）

```bash
cd "c:\Users\21140\Desktop\数学的天空网站\poincare"
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

### 2.2 创建 .gitignore 文件

防止上传不必要的文件：

```
.streamlit/secrets.toml
__pycache__/
*.pyc
.DS_Store
*.stl
*.png
venv/
.env
```

### 2.3 添加所有文件到 Git

```bash
git add .
git commit -m "Initial commit: Poincare Streamlit App"
```

### 2.4 推送到 GitHub

首先在 GitHub 上创建新的仓库，然后：

```bash
git remote add origin https://github.com/YOUR_USERNAME/poincare.git
git branch -M main
git push -u origin main
```

---

## ✅ 第三步：注册 Streamlit Community Cloud

### 3.1 访问 Streamlit Community Cloud

前往：https://streamlit.io/cloud

### 3.2 使用 GitHub 账户登录

- 点击 "Sign up with GitHub"
- 授权 Streamlit 访问您的 GitHub 账户
- 完成注册

### 3.3 链接 GitHub 仓库

1. 在 Streamlit Cloud 仪表板中，点击 "New app"
2. 选择您的 GitHub 仓库
3. 选择主分支（main）
4. 设置应用主文件为 `app.py`
5. 点击 "Deploy"

---

## 🔧 第四步：配置云端应用

### 4.1 应用配置

Streamlit Cloud 会自动：
- ✅ 读取 `requirements.txt` 安装依赖
- ✅ 在 Linux 服务器上运行您的应用
- ✅ 分配唯一的 URL

### 4.2 获取应用 URL

部署完成后，您会获得形如以下的 URL：

```
https://your-username-poincare-app-abc123.streamlit.app/
```

### 4.3 分享给听众

复制这个 URL 分享给演讲听众，他们就可以直接访问您的应用！

---

## ⚠️ 常见问题解决

### 问题 1: 依赖安装失败

**原因**: `requirements.txt` 中的库版本不兼容

**解决方案**:
```bash
# 更新为最新兼容版本
streamlit>=1.28
matplotlib>=3.8
numpy>=1.24
Pillow>=10.0
opencv-python>=4.8
trimesh>=4.0
scikit-image>=0.22
```

### 问题 2: OpenCV 导入错误

**原因**: `opencv-python` 在 Linux 上可能缺少依赖

**解决方案**: 在 `requirements.txt` 中改为：
```
opencv-python-headless
```

### 问题 3: 应用启动很慢

**原因**: 云端首次启动需要安装所有依赖

**解决方案**: 这是正常的，通常需要 2-3 分钟

### 问题 4: 中文字体显示问题

**原因**: Linux 服务器没有中文字体

**解决方案**: 创建 `packages.txt` 文件：
```
fonts-noto-cjk
```

---

## 📦 Linux 依赖文件（可选）

如果遇到系统依赖问题，创建 `packages.txt`：

```
# 中文字体支持
fonts-noto-cjk

# 其他可能需要的系统库
libgl1
libsm6
libxrender1
```

**放置位置**：与 `requirements.txt` 同级

---

## 🔐 安全配置

### 4.1 使用 secrets 管理敏感信息

如果需要 API 密钥等敏感信息，创建 `.streamlit/secrets.toml`：

```toml
[database]
password = "your_secret_password"

[api_keys]
my_api_key = "your_api_key"
```

### 4.2 在云端添加 secrets

1. 进入应用设置
2. 点击 "Secrets" 标签
3. 粘贴 secrets 内容
4. 点击保存

### 4.3 在代码中使用 secrets

```python
import streamlit as st

password = st.secrets["database"]["password"]
```

---

## 📊 部署后的监控

### 监控应用状态

1. 访问 Streamlit Cloud 仪表板
2. 查看应用的实时状态
3. 检查运行日志

### 查看应用日志

```bash
# 在 Streamlit Cloud 中点击应用
# 然后点击右上角的 "Logs" 查看输出
```

---

## 🚀 完整部署流程总结

```
1. ✅ 准备 requirements.txt (已完成)
   └─ 包含所有必要的库和版本

2. ⏳ 上传代码到 GitHub
   ├─ 初始化 Git 仓库
   ├─ 提交代码
   └─ 推送到 GitHub

3. ⏳ 在 Streamlit Cloud 部署
   ├─ 注册账户
   ├─ 连接 GitHub 仓库
   ├─ 配置应用
   └─ 部署

4. ⏳ 获取公网 URL
   ├─ 等待部署完成
   ├─ 获取应用 URL
   └─ 分享给听众
```

---

## 💡 演讲现场使用提示

### 演讲前的检查清单

- [ ] 应用在本地运行正常
- [ ] 网页布局在演讲场地投影机上显示正常
- [ ] 所有参数调整都能流畅运行
- [ ] 网络连接稳定
- [ ] 备用电源（如需要）
- [ ] 备用演讲稿（以防应用崩溃）

### 演讲现场最佳实践

1. **提前 5 分钟打开应用**
   - 让缓存加载完成
   - 确保网络连接正常

2. **使用屏幕镜像软件**
   - Windows: 使用 Miracast 或投影仪缆线
   - Mac: 使用 AirPlay
   - 确保演讲者视图可见

3. **演示参数调整**
   - 从预设参数开始
   - 逐步调整参数
   - 展示实时效果

4. **准备备用方案**
   - 备用截图或视频
   - 本地运行的备份版本
   - 应急脚本

---

## 🎯 高级部署选项

### 选项 1: Streamlit Community Cloud（推荐）
- ✅ 完全免费
- ✅ 自动更新
- ✅ 一键部署
- ✅ 无需服务器管理

### 选项 2: Heroku
- 有免费层限制
- 需要手动配置
- 更多自定义选项

### 选项 3: Docker + 自建服务器
- 完全控制
- 需要服务器和维护
- 最复杂但最灵活

---

## 📝 完整的部署文件清单

部署到云端所需的文件：

```
poincare/
├── app.py                    ✅ 主应用
├── requirements.txt          ✅ Python 依赖（必需）
├── packages.txt             ⏳ Linux 依赖（可选）
├── .streamlit/
│   └── config.toml          ✅ 配置文件
├── poincare.py              ✅ 核心算法
├── poincare_lines.py        ✅ 文字投影
├── plotter.py               ✅ 绘图工具
├── char2lines.py            ✅ 文字处理
├── text2png.py              ✅ 文字处理
├── stlgen.py                ✅ STL 生成
└── .gitignore              ✅ Git 配置
```

---

## 🔍 验证部署成功的标志

部署成功后，您应该能够：

- ✅ 访问公网 URL
- ✅ 在浏览器中看到应用
- ✅ 调整参数看到实时反应
- ✅ 导出文件
- ✅ 从不同设备访问

---

## 📞 如果部署失败

### 检查步骤

1. **查看部署日志**
   - Streamlit Cloud 仪表板 → Logs

2. **检查常见错误**
   - `ModuleNotFoundError`: 检查 requirements.txt
   - `ImportError`: 检查库版本兼容性
   - `FileNotFoundError`: 检查文件路径

3. **本地重现问题**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. **更新 requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```

---

## 🎉 下一步

部署完成后：

1. **分享 URL** 给演讲听众
2. **监控应用** 性能和错误
3. **收集反馈** 改进应用
4. **持续更新** 代码和功能

---

## 📚 参考资源

- [Streamlit Cloud 官方文档](https://docs.streamlit.io/streamlit-cloud)
- [部署指南](https://docs.streamlit.io/streamlit-cloud/get-started)
- [常见问题](https://docs.streamlit.io/streamlit-cloud/troubleshooting)
- [GitHub 与 Streamlit 集成](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

---

## ✨ 演讲场景演示建议

### 推荐演示流程

1. **介绍应用**（30 秒）
   - "这是一个双曲几何的可视化工具"
   - 展示应用 URL

2. **基础镶嵌演示**（1-2 分钟）
   - 调整 p 值，展示多边形变化
   - 调整 k 值，展示递归深度效果

3. **文字投影演示**（1-2 分钟）
   - 输入听众的名字
   - 演示投影效果

4. **参数调整演示**（1-2 分钟）
   - 动态调整各个参数
   - 展示实时效果

5. **导出演示**（1 分钟）
   - 展示如何下载 STL 模型
   - 说明 3D 打印用途

---

**🎊 恭喜！您的应用已准备好部署到公网了！**

现在按照本指南逐步进行部署，很快您就能分享公网 URL 给所有人！

最后更新：2026 年 6 月 2 日
