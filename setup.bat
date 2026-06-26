@echo off
chcp 65001 >nul
title 办公自动化工具箱 - 安装程序
echo ============================================
echo    🔧 办公自动化工具箱 - 安装程序
echo ============================================
echo.
echo 正在检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python 已检测到
echo.
echo 正在安装依赖（首次安装可能需要几分钟）...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败，请检查网络连接后重试
    pause
    exit /b 1
)
echo.
echo ============================================
echo    ✅ 安装完成！
echo.
echo    运行方式：双击 gui_launcher.py
echo    或：      双击 启动工具箱.bat
echo ============================================
pause
