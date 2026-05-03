#!/bin/bash
# generate-sync-report.sh — 对比测试与生产差异，输出审批报告

TEST_DIR="/tmp/agentic-os-test"
PROD_DIR="$(pwd)" # 请在项目根目录运行

REPORT="/tmp/sync_report.md"
echo "# 🔄 同步审批报告" > "$REPORT"
echo "生成时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT"
echo "" >> "$REPORT"

# 差异文件列表
echo "## 📁 修改文件列表" >> "$REPORT"
diff -rq "$TEST_DIR/dashboard" "$PROD_DIR/dashboard" 2>/dev/null >> "$REPORT"
diff -rq "$TEST_DIR/shared" "$PROD_DIR/shared" 2>/dev/null >> "$REPORT"
diff -rq "$TEST_DIR/scripts" "$PROD_DIR/scripts" 2>/dev/null >> "$REPORT"
echo "" >> "$REPORT"

# 每个文件的主要变更（只显示增删行数）
echo "## 📊 变更摘要（行数变化）" >> "$REPORT"
for diff_file in $(diff -rq "$TEST_DIR/dashboard" "$PROD_DIR/dashboard" 2>/dev/null | grep -v "Only in" | awk '{print $2}' | sed 's/:$//'); do
  rel_path="${diff_file#$TEST_DIR/}"
  if [ -f "$PROD_DIR/$rel_path" ]; then
    add=$(diff -u "$PROD_DIR/$rel_path" "$diff_file" | grep -c '^+')
    del=$(diff -u "$PROD_DIR/$rel_path" "$diff_file" | grep -c '^-')
    echo "- \`$rel_path\` : +$add/-$del 行" >> "$REPORT"
  fi
done
for diff_file in $(diff -rq "$TEST_DIR/shared" "$PROD_DIR/shared" 2>/dev/null | grep -v "Only in" | awk '{print $2}' | sed 's/:$//'); do
  rel_path="${diff_file#$TEST_DIR/}"
  if [ -f "$PROD_DIR/$rel_path" ]; then
    add=$(diff -u "$PROD_DIR/$rel_path" "$diff_file" | grep -c '^+')
    del=$(diff -u "$PROD_DIR/$rel_path" "$diff_file" | grep -c '^-')
    echo "- \`$rel_path\` : +$add/-$del 行" >> "$REPORT"
  fi
done
echo "" >> "$REPORT"

# 测试验收清单（硬编码当前标准，可根据实际调整）
echo "## ✅ 测试验收清单" >> "$REPORT"
tests=(
  "Flask 测试服务 :5002 正常响应"
  "Dashboard 全部 10 个模块可点击"
  "DM-0 ~ DM-10 render 函数无 undefined"
  "MS-0 ~ MS-5 面板正常展开"
  "审核四维度卡片折叠/展开"
  "利润瀑布图、雷达图、时间轴渲染"
  "重审闭环弹出对话框"
  "node --check 全部 JS 文件无错误"
  "curl /api/script 返回 6 集概要"
  "curl /api/images 返回产品列表"
)
for t in "${tests[@]}"; do
  echo "- [ ] $t" >> "$REPORT"
done
echo "" >> "$REPORT"

# 结论语
echo "## ⚠️ 风险提示" >> "$REPORT"
echo "本次修改涉及文件数：$(diff -rq "$TEST_DIR/dashboard" "$PROD_DIR/dashboard" 2>/dev/null | wc -l) 个" >> "$REPORT"
echo "请人工确认后执行：\`bash scripts/sync-test-to-prod.sh\`" >> "$REPORT"

echo "报告已生成：$REPORT"
