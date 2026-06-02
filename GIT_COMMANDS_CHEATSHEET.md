# 📝 Git 命令速查表（复制即用）

## 🚀 部署到 GitHub 的完整命令

### 第一次上传代码到 GitHub

复制整个代码块，在项目目录执行：

```bash
# 进入项目目录
cd "c:\Users\21140\Desktop\数学的天空网站\poincare"

# 初始化 Git 仓库
git init

# 配置用户信息（替换为您的信息）
git config user.name "Your Name"
git config user.email "your.email@gmail.com"

# 添加所有文件
git add .

# 首次提交
git commit -m "Initial commit: Poincare Streamlit Application"

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/poincare.git

# 重命名分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

### 更新代码到 GitHub

之后每次修改代码后，只需运行：

```bash
git add .
git commit -m "Description of your changes"
git push
```

---

## 📋 必要的替换项

### 1. GitHub 用户名

**查找您的 GitHub 用户名**:
1. 访问 https://github.com
2. 登录后，点击右上角头像
3. 选择 "Profile"
4. URL 中的 `/YOUR_USERNAME/` 就是

**替换方式**:
```bash
# 错误 ❌
git remote add origin https://github.com/YOUR_USERNAME/poincare.git

# 正确 ✅（假设您的用户名是 "john"）
git remote add origin https://github.com/john/poincare.git
```

### 2. 您的邮箱和名字

```bash
# 替换示例
git config user.name "John Doe"
git config user.email "john@example.com"
```

---

## ⚠️ 常见错误及解决方案

### 错误 1: "fatal: Not a git repository"

**解决**:
```bash
# 确保您在项目目录中
cd "c:\Users\21140\Desktop\数学的天空网站\poincare"

# 查看是否有 .git 目录
dir /a

# 如果没有，运行
git init
```

### 错误 2: "error: The following files would be overwritten by merge"

**解决**:
```bash
# 先提交本地更改
git add .
git commit -m "Save local changes"
```

### 错误 3: "fatal: 'origin' does not appear to be a 'git' repository"

**解决**:
```bash
# 检查远程仓库设置
git remote -v

# 如果不存在，添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/poincare.git
```

### 错误 4: "Permission denied (publickey)"

**解决**:
```bash
# 使用 HTTPS 而不是 SSH
# 已确保 URL 格式为
git remote set-url origin https://github.com/YOUR_USERNAME/poincare.git
```

---

## 🔍 常用 Git 命令

### 查看状态

```bash
# 查看当前状态
git status

# 查看最后的提交
git log --oneline -5

# 查看远程仓库
git remote -v
```

### 修改和撤销

```bash
# 查看未暂存的更改
git diff

# 撤销未暂存的更改
git checkout -- <file>

# 撤销上一次提交（保留代码）
git reset --soft HEAD~1

# 撤销上一次提交（删除代码）
git reset --hard HEAD~1
```

### 分支操作

```bash
# 查看所有分支
git branch -a

# 创建新分支
git branch feature-name

# 切换分支
git checkout feature-name

# 创建并切换到新分支
git checkout -b feature-name

# 删除分支
git branch -d feature-name
```

---

## 🎯 完整的分步流程

### 步骤 1: 初始化并首次推送（仅一次）

```powershell
# 在 PowerShell 中运行

cd "c:\Users\21140\Desktop\数学的天空网站\poincare"

git init
git config user.name "Your Name"
git config user.email "your@email.com"
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/poincare.git
git branch -M main
git push -u origin main
```

### 步骤 2: 之后每次更新

```powershell
cd "c:\Users\21140\Desktop\数学的天空网站\poincare"
git add .
git commit -m "Update description"
git push
```

---

## 📊 Git 工作流程图

```
┌─────────────────────────────────────┐
│  修改文件                            │
│  (app.py, requirements.txt 等)      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  git add .                          │
│  (暂存所有更改)                     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  git commit -m "message"            │
│  (创建本地提交)                     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  git push                           │
│  (推送到 GitHub)                    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Streamlit Cloud 自动检测更新       │
│  并重新部署应用                     │
└─────────────────────────────────────┘
```

---

## 🛠️ 推荐的 PowerShell 别名

为了快速操作，在 PowerShell 配置文件中添加别名：

```powershell
# 打开 PowerShell 配置文件
notepad $PROFILE

# 添加以下别名
function gs { git status }
function ga { git add . }
function gc { param([string]$msg = "Update") ; git commit -m $msg }
function gp { git push }
function gl { git log --oneline -10 }

# 一键上传
function gall { 
    git add . ; 
    git commit -m "Update" ; 
    git push
}
```

使用示例：
```powershell
gs              # git status
ga              # git add .
gc "My changes" # git commit
gp              # git push
gall            # 全部操作
```

---

## 🔐 保存凭证（可选）

如果每次推送都要输入密码，可以保存凭证：

### Windows 本地保存（仅本机）

```bash
git config --global credential.helper wincred
```

### 生成 Personal Access Token（推荐安全）

1. GitHub 设置 → Developer settings → Personal access tokens
2. 生成新 token，选择 `repo` 权限
3. 复制 token
4. 使用时，将 token 作为密码输入

---

## 📚 更多资源

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 快速入门](https://docs.github.com/en/get-started/quickstart)
- [Git 交互式学习](https://learngitbranching.js.org/)

---

## ✅ 检查清单

部署前确认：

- [ ] 代码已保存
- [ ] `requirements.txt` 最新
- [ ] `.gitignore` 文件存在
- [ ] Git 已初始化
- [ ] GitHub 仓库已创建
- [ ] 远程 origin 已配置
- [ ] 代码已推送到 GitHub

---

**准备好了吗？现在就开始部署！** 🚀

最后更新：2026 年 6 月 2 日
