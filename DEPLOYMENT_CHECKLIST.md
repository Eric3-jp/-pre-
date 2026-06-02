# ✅ 部署检查清单与步骤

## 🎯 部署前的最终检查

### 📋 本地测试检查

- [ ] 应用在本地正常运行
  ```bash
  streamlit run app.py
  ```
  
- [ ] 所有参数调整都能正常工作

- [ ] 没有明显的错误信息或警告

- [ ] 所有功能都能使用（文字投影、镶嵌生成、图片处理）

- [ ] 导出功能正常（下载 STL、截图等）

### 📁 文件检查

- [ ] `requirements.txt` 存在
  ```
  位置: c:\Users\21140\Desktop\数学的天空网站\poincare\requirements.txt
  ```

- [ ] `requirements.txt` 包含所有必要的库
  ```
  streamlit>=1.28
  matplotlib>=3.8
  numpy>=1.24
  Pillow>=10.0
  opencv-python>=4.8
  trimesh>=4.0
  scikit-image>=0.22
  ```

- [ ] `.gitignore` 文件存在

- [ ] `packages.txt` 文件存在（可选，用于 Linux 依赖）

- [ ] `.streamlit/config.toml` 文件存在

- [ ] 没有遗留的调试代码

### 🔧 代码检查

- [ ] 没有硬编码的文件路径（使用相对路径）

- [ ] 没有敏感信息（密钥、密码等）

- [ ] 代码注释清晰

- [ ] `app.py` 中的所有导入都在 `requirements.txt` 中

---

## 🚀 部署步骤

### 第 1 步：初始化 Git（如果还未做）

```bash
cd "c:\Users\21140\Desktop\数学的天空网站\poincare"
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

### 第 2 步：提交代码到本地 Git

```bash
git add .
git commit -m "Initial commit: Poincare Streamlit App"
```

### 第 3 步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `poincare` 或 `poincare-streamlit-app`
   - **Visibility**: 选择 `Public`
3. 点击 "Create repository"

### 第 4 步：推送代码到 GitHub

```bash
# 替换 YOUR_USERNAME 为您的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/poincare.git
git branch -M main
git push -u origin main
```

### 第 5 步：部署到 Streamlit Cloud

1. 访问 https://streamlit.io/cloud
2. 点击 "Sign up with GitHub"
3. 授权并登录
4. 点击 "New app"
5. 选择您的仓库和分支
6. 点击 "Deploy"

### 第 6 步：获取公网 URL

部署完成后，您会获得形如下面的 URL：
```
https://your-username-poincare-xxxxx.streamlit.app
```

---

## 📊 部署状态检查

### 部署进行中

✓ 看到进度条和日志信息
✓ 依赖包正在安装
✓ 应用正在启动

### 部署完成

✓ 看到绿色的 "App is running!" 消息
✓ 自动跳转到应用页面
✓ 可以看到应用界面

### 如果出错

✗ 查看日志找出错误原因
✗ 检查 `requirements.txt`
✗ 查看代码中是否有硬编码路径
✗ 检查代码中的中文字体问题

---

## 🆘 常见问题快速修复

### 问题 1: "ModuleNotFoundError: No module named 'xxx'"

**原因**: 库未在 `requirements.txt` 中

**修复**:
1. 打开 `requirements.txt`
2. 添加缺失的库
3. 保存文件
4. 提交并推送
5. Streamlit Cloud 会自动重新部署

### 问题 2: 中文显示为方块或乱码

**原因**: Linux 服务器缺少中文字体

**修复**: 创建或编辑 `packages.txt`，添加：
```
fonts-noto-cjk
```

### 问题 3: 应用加载很慢

**原因**: 正常，首次启动需要安装依赖

**修复**: 等待 2-5 分钟，之后会快很多

### 问题 4: 图片处理错误

**原因**: OpenCV 依赖问题

**修复**: 在 `requirements.txt` 中改为：
```
opencv-python-headless
```

### 问题 5: STL 生成失败

**原因**: trimesh 导入问题

**修复**: 确保 `requirements.txt` 中有：
```
trimesh>=4.0
numpy-stl
```

---

## 📝 部署后的维护

### 定期检查清单

每周检查一次：

- [ ] 应用是否还能访问
- [ ] 是否有错误日志
- [ ] 用户反馈了什么问题
- [ ] 是否需要更新库

### 更新应用

当需要更新应用时：

1. 修改本地代码
2. 提交到 Git：
   ```bash
   git add .
   git commit -m "Update: description"
   git push
   ```
3. Streamlit Cloud 会自动检测并重新部署

### 监控日志

在 Streamlit Cloud 仪表板：

1. 找到您的应用
2. 点击应用名称
3. 点击右上角的 "Logs"
4. 查看实时日志

---

## 🎤 演讲使用检查清单

演讲前 30 分钟检查：

- [ ] 网络连接正常
- [ ] 访问应用 URL，确保可以打开
- [ ] 调整参数，确保功能正常
- [ ] 投影设置正确
- [ ] 音频设置（如有演讲配音）
- [ ] 备用方案已准备（本地版本或视频）

演讲中：

- [ ] 有投影屏幕实时显示应用
- [ ] 与听众分享 URL 或二维码
- [ ] 实时演示参数调整
- [ ] 展示不同的镶嵌类型
- [ ] 邀请听众参与（输入他们的名字等）

---

## 📱 分享 URL 的方式

### 方式 1: 直接分享 URL

```
https://your-username-poincare-xxxxx.streamlit.app
```

### 方式 2: 使用短链接服务

使用 bit.ly 或 tinyurl 生成短链接：

```
https://bit.ly/poincare-demo
```

### 方式 3: 生成二维码

使用 QR 码生成工具（如 qr-server.com）为 URL 生成二维码，
展示在演讲稿中，听众可以扫码访问。

### 方式 4: 在演讲稿中说明

- "访问这个网址查看应用"
- "扫描二维码即可尝试"
- "演讲后，您可以继续访问这个应用"

---

## 🔐 安全检查

部署前确认：

- [ ] 没有在代码中硬编码密钥或密码
- [ ] 没有暴露任何敏感信息
- [ ] 依赖库都来自官方来源
- [ ] 没有包含个人隐私信息

---

## 📊 部署成功的标志

✅ 所有以下都成立，说明部署成功：

1. ✅ URL 可访问
2. ✅ 应用界面正常显示
3. ✅ 所有参数可调整
4. ✅ 实时预览正常
5. ✅ 导出功能可用
6. ✅ 没有明显错误消息
7. ✅ 加载速度可以接受

---

## 🎯 部署完成后

### 立即采取的行动

1. 📋 记录 URL（保存在文档中）
2. 🔗 生成短链接
3. 📱 生成二维码
4. 📧 分享给相关人员
5. 🎤 准备演讲稿

### 后续维护

1. 📅 定期检查应用状态
2. 📊 监控使用情况
3. 🐛 修复 bug 和错误
4. ✨ 添加新功能

---

## 📞 获取帮助

### 官方资源

- [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-cloud)
- [GitHub 帮助](https://docs.github.com)
- [Streamlit 社区论坛](https://discuss.streamlit.io)

### 查找错误信息

大多数错误可以通过以下方式找到：

1. Streamlit Cloud 的 Logs 标签
2. 浏览器开发者工具 (F12)
3. GitHub Actions 日志（如适用）

---

## ✨ 恭喜！

完成这个清单后，您的应用就已部署到公网，
可以与世界分享了！

🎊 **祝演讲成功！** 🎊

---

最后更新：2026 年 6 月 2 日
