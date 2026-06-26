#!/bin/bash
echo "============================================"
echo "   🔧 办公自动化工具箱 - 安装程序"
echo "============================================"
echo ""
echo "正在检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.8+"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi
echo "Python3 已检测到"
echo ""
echo "正在安装依赖..."
python3 -m pip install --upgrade pip -q
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 依赖安装失败，请检查网络连接后重试"
    exit 1
fi
echo ""
echo "============================================"
echo "   ✅ 安装完成！"
echo ""
echo "  运行方式：python3 gui_launcher.py"
echo "============================================"
