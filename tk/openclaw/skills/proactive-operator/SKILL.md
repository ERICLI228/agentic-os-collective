# Proactive Operator - 主动运营 Agent

> 你的私人运营助手，自动监控市场动态，有新机会时主动通知

---

## 功能

| 功能 | 说明 |
|------|------|
| 📱 TikTok 热门监控 | 定时抓取热门视频，分析趋势 |
| 🛒 电商数据监控 | Amazon、1688 热门商品 |
| 🔥 爆款检测 | 播放量 > 500万 自动告警 |
| 📢 主动通知 | 飞书/邮件通知 |
| 📝 日报生成 | 每日自动生成运营报告 |

---

## 配置文件

编辑 `config.json`:

```json
{
    "watch_keywords": ["3C数码", "手机配件", "耳机"],
    "watch_categories": ["toy", "electronics", "earbuds"],
    "thresholds": {
        "hot_video_plays": 5000000
    }
}
```

---

## 运行方式

### 手动运行
```bash
bash ~/.agents/skills/proactive-operator/proactive-operator.sh
```

### 定时运行 (推荐)
```bash
# 设置每4小时运行一次
openclaw cron add \
  --schedule "every 4h" \
  --command "bash ~/.agents/skills/proactive-operator/proactive-operator.sh"
```

---

## 通知设置

1. 编辑 `notify.sh`
2. 添加飞书 Webhook:
```bash
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
```

---

## 数据输出

| 文件 | 位置 |
|------|------|
| 热门数据 | `data/tiktok_*.json` |
| 运营报告 | `data/report_YYYYMMDD.md` |
| 通知日志 | `logs/notifications.log` |

---

## 示例输出

```
[2026-04-04 07:40:00] 📱 检查 TikTok 热门...
[2026-04-04 07:40:01]   搜索: toy
[2026-04-04 07:40:05]   📊 toy 趋势: 平均:2.3M, 最高:50M
[2026-04-04 07:40:06]   🔥 发现爆款: ohotoy6:Rope launcher:50M
[2026-04-04 07:40:06] 📢 通知: 🔥 发现爆款 - toy
[2026-04-04 07:40:10] ========== 运营 Agent 完成 ==========
```

---

## 扩展

- 添加更多平台 (小红书、抖音、Twitter)
- 添加数据分析 (趋势预测、竞品对比)
- 添加自动执行 (自动发笔记、自动投广告)