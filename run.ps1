#!/usr/bin/env pwsh

# Poincaré 双曲镶嵌生成器 - Streamlit 启动脚本

Write-Host "================================" -ForegroundColor Cyan
Write-Host "🌀 Poincaré 双曲镶嵌生成器" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 版本
Write-Host "检查 Python 环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "✓ $pythonVersion" -ForegroundColor Green
Write-Host ""

# 检查依赖
Write-Host "检查依赖包..." -ForegroundColor Yellow
$requiredPackages = @("streamlit", "matplotlib", "numpy", "PIL", "cv2")
$allInstalled = $true

foreach ($package in $requiredPackages) {
    try {
        python -c "import $package" 2>$null
        Write-Host "✓ $package" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ $package - 缺失" -ForegroundColor Red
        $allInstalled = $false
    }
}

if (-not $allInstalled) {
    Write-Host ""
    Write-Host "⚠️  某些依赖缺失，正在安装..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "启动 Streamlit 应用..." -ForegroundColor Yellow
Write-Host "应用将在浏览器中打开，地址: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

# 启动应用
python -m streamlit run app.py

# 保持窗口打开
Read-Host "按 Enter 键关闭此窗口"
