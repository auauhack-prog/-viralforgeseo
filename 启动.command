#!/bin/bash
echo "=============================="
echo "  ViralForge V1.0 启动中..."
echo "  AI视频生成 + 社交媒体自动发布"
echo "=============================="
cd "$(dirname "$0")"
if [ ! -f .env ]; then
    cp .env.example .env
    echo "已从 .env.example 创建 .env，请编辑填入 API Keys"
fi
pip install -r requirements.txt -q
python graph.py
