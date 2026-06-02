# 🚀 GitHub + Streamlit Cloud 快速部署指南

## 5 分钟快速部署流程

### 前置条件

- ✅ 本地应用已正常运行
- ✅ 已安装 Git
- ✅ 拥有 GitHub 账户
- ✅ 拥有网络连接

---

## 第 1 步：上传代码到 GitHub（3 分钟）

### 1.1 在 GitHub 创建新仓库

1. 访问 https://github.com/new
2. 输入仓库名：`poincare` 或 `poincare-streamlit-app`
3. 选择 **Public**（公开，让所有人都能访问）
4. 点击 "Create repository"

### 1.2 获取仓库 URL

复制仓库的 HTTPS URL，形如：
```
https://github.com/YOUR_USERNAME/poincare.git
```

### 1.3 初始化并推送代码

在项目目录中运行：

```bash
cd "c:\Users\21140\Desktop\数学的天空网站\poincare"

# 初始化 Git（如果还未初始化）
git init

# 配置 Git 用户信息
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: Poincare Streamlit Application"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/poincare.git

# 重命名主分支为 main（GitHub 默认）
git branch -M main

# 推送代码到 GitHub
git push -u origin main
```

**完成后**：您的代码就在 GitHub 上了！✅

---

## 第 2 步：在 Streamlit Cloud 部署（2 分钟）

### 2.1 访问 Streamlit Cloud

前往：https://streamlit.io/cloud

### 2.2 使用 GitHub 账户登录

1. 点击 **"Sign up with GitHub"** 或 **"Sign in with GitHub"**
2. 授权 Streamlit 访问您的 GitHub 账户
3. 完成注册/登录

### 2.3 创建新应用

1. 进入仪表板后，点击 **"New app"** 或 **"Create app"**
2. 出现部署对话框

### 2.4 配置应用部署

在对话框中：

1. **Repository** 选择：`YOUR_USERNAME/poincare`
2. **Branch** 选择：`main`
3. **Main file path** 输入：`app.py`
4. 点击 **"Deploy"**

Streamlit 会自动：
- 📥 拉取您的代码
- 📦 安装 requirements.txt 中的依赖
- 🚀 启动应用

### 2.5 等待部署完成

部署过程会显示进度，第一次通常需要 2-5 分钟。

---

## 第 3 步：获取公网 URL（自动）

### 部署完成后

您会看到一个形如下面的公网 URL：

```
https://your-username-poincare-xxxxx.streamlit.app
```

🎉 **现在所有人都可以访问您的应用了！**

---

## 📋 检查清单

部署前确认：

- [ ] `requirements.txt` 存在且包含所有必要的库
- [ ] `app.py` 文件存在
- [ ] 本地测试通过：`streamlit run app.py`
- [ ] 代码已提交到 GitHub
- [ ] Streamlit Cloud 部署完成

---

## 🔄 更新应用

如果您修改了代码，如何更新云端应用？

### 方法 1：自动更新（推荐）

1. 本地修改代码
2. 提交并推送到 GitHub：
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. Streamlit Cloud 会自动检测并重新部署！

### 方法 2：手动重新部署

1. 进入 Streamlit Cloud 仪表板
2. 找到您的应用
3. 点击右上角的 **"..."** 菜单
4. 选择 **"Reboot app"** 或 **"Delete app"** 然后重新创建

---

## 🆘 常见问题

### Q: 部署失败显示 "ModuleNotFoundError"

**A**: 检查 `requirements.txt`：
- 确认文件名拼写正确
- 确认文件在项目根目录
- 检查库名和版本格式

### Q: 中文显示为方块

**A**: 创建 `packages.txt` 文件，添加：
```
fonts-noto-cjk
```

### Q: 应用加载很慢

**A**: 正常现象，首次加载需要安装依赖。之后会快得多。

### Q: 如何看错误日志

**A**: 在应用页面右上角点击 **"Logs"** 查看实时日志。

### Q: 能否私有部署（不公开）

**A**: Streamlit Cloud 只支持公开部署。如需私密，考虑自建服务器。

---

## 💡 部署后的优化

### 提高应用速度

在 `.streamlit/config.toml` 中添加：

```toml
[client]
showErrorDetails = false

[logger]
level = "error"

[server]
maxUploadSize = 200
```

### 自定义应用名称

在应用设置中修改应用名称（会改变 URL）

### 添加自定义域名（高级）

Streamlit 支持连接自定义域名，但需要升级到企业版。

---

## 🎯 演讲现场使用

### 分享 URL 给听众

1. 提前获取公网 URL
2. 打印在演讲稿或投影幻灯片上
3. 演讲时分享链接

### 演讲 URL 格式建议

```
长 URL: https://your-username-poincare-xxxxx.streamlit.app
短 URL: 使用 bit.ly 或 tinyurl 缩短
```

例如：
```
https://bit.ly/poincare-demo
```

### 演讲时的最佳实践

1. **提前测试网络**
   - 演讲场地的网络连接
   - 投影设备的兼容性

2. **打开应用预热**
   - 演讲开始前 5 分钟打开应用
   - 让缓存加载完成

3. **准备备用方案**
   - 本地运行版本
   - 预录视频
   - 静态截图

4. **与听众互动**
   - 现场调整参数
   - 接受听众的建议
   - 实时展示效果

---

## 📊 部署后的监控

### 查看应用使用情况

Streamlit Cloud 提供：
- 📈 访问统计
- 📊 性能指标
- 🐛 错误日志
- 💾 内存使用

在仪表板中点击应用即可查看。

---

## 🔐 安全建议

1. **Keep requirements.txt 精简**
   - 只包含实际使用的库
   - 定期检查版本更新

2. **不要暴露敏感信息**
   - 不要在代码中写密钥
   - 使用 `.streamlit/secrets.toml`（本地）
   - 在云端使用 Streamlit Secrets 管理

3. **监控应用安全**
   - 定期查看日志
   - 监测异常访问

---

## ✅ 部署完成检查

部署成功标志：

- ✅ URL 可访问
- ✅ 应用界面正常显示
- ✅ 参数可调整
- ✅ 功能正常运行
- ✅ 没有明显错误

---

## 🎉 恭喜！

您的 Poincaré 双曲镶嵌应用现已部署到公网！

现在您可以：
- 🌍 与世界分享您的应用
- 🎤 在演讲中展示实时演示
- 👥 邀请他人参与和反馈
- 🚀 持续改进和更新应用

---

## 📞 如果需要帮助

### 官方资源

- Streamlit Cloud 文档: https://docs.streamlit.io/streamlit-cloud
- GitHub Help: https://docs.github.com
- 社区论坛: https://discuss.streamlit.io

### 常见错误查询

在 Streamlit Cloud 日志中查看具体错误信息，通常会提供解决方案。

---

**祝您演讲成功！** 🎊

---

最后更新：2026 年 6 月 2 日
