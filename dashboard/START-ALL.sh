#!/bin/bash
# Agentic OS v3.1 一键启动脚本
# 创建时间: 2026-04-12

echo "🚀 启动 Agentic OS v3.1 指挥中心..."

# 1. 启动主页面 (5002)
echo "启动主页面 (5002)..."
cd ~/.openclaw/dashboard
nohup python3 -m http.server 5002 > /tmp/agentic-dashboard.log 2>&1 &
sleep 2

# 2. 启动API (5001)
echo "启动API (5001)..."
cd ~/.openclaw/core
nohup python3 dashboard_api_v2.py > /tmp/agentic-api.log 2>&1 &
sleep 2

# 3. 启动子页面 (5173)
echo "启动子页面 (5173)..."
cd ~/agentic-os-collective/web
nohup npm run dev > /tmp/vite.log 2>&1 &
sleep 3

# 验证
echo ""
echo "=== 验证服务 ==="
lsof -i :5001 -i :5002 -i :5173 | grep LISTEN

echo ""
echo "✅ 启动完成！"
echo ""
echo "访问地址:"
echo "  主页面: http://localhost:5002/ (指挥中心)"
echo "  子页面: http://localhost:5173/ (数据面板)"
echo "  API: http://localhost:5001/api/dashboard"