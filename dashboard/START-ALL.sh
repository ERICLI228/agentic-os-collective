#!/bin/bash
# Agentic OS v3.3 一键启动脚本
# 2026-04-24: 已废弃静态HTML (port 5002)，统一使用 Vue 3 SPA

echo "🚀 启动 Agentic OS v3.3..."

# 1. 启动 API 服务 (5001)
echo "启动 API v2 (5001)..."
cd ~/agentic-os-collective/dashboard
nohup python3 dashboard_api_v2.py > /tmp/agentic-api.log 2>&1 &
sleep 2

# 2. 启动 FastAPI v3 (5004)
echo "启动 API v3 (5004)..."
cd ~/agentic-os-collective/api/v3
nohup python3 dashboard_api_v3.py > /tmp/agentic-api-v3.log 2>&1 &
sleep 2

# 3. 启动 Vue 3 SPA 开发服务器 (5173)
echo "启动 Vue SPA (5173)..."
cd ~/agentic-os-collective/web
nohup npm run dev > /tmp/vite.log 2>&1 &
sleep 4

# 验证
echo ""
echo "=== 验证服务 ==="
lsof -i :5001 -i :5004 -i :5173 | grep LISTEN || echo "(部分服务可能未启动)"

echo ""
echo "✅ 启动完成！"
echo ""
echo "访问地址:"
echo "  Vue SPA:     http://localhost:5173/ (主数据面板)"
echo "  API v2:      http://localhost:5001/ (Flask)"
echo "  API v3:      http://localhost:5004/ (FastAPI)"
echo "  Swagger:     http://localhost:5004/docs"
echo ""
echo "注意: 静态 HTML Dashboard (port 5002) 已废弃"
