# 🎯 Haimeta营销日历自动生成系统

零预算、全自动的营销热点日历,每天自动抓取30-50个全球营销热点,生成双语文案+AI配图Prompt,直接对接飞书多维表格。

## 📊 数据源(全免费)

| 数据源 | 每日数量 | 免费额度 | 状态 |
|--------|---------|---------|------|
| 全球节日库 | 5-10个 | 无限 | ✅ 已实现 |
| Web Search | 10-20个 | 无限 | ⏳ 待实现 |
| YouTube API | 10-15个 | 1万次/天 | ✅ 已实现 |
| 竞品RSS | 3-5个 | 无限 | ⏳ 待实现 |
| Hugging Face | 按需 | 1000次/天 | ✅ 已实现 |

## 🚀 快速开始

### 1. Fork本仓库

点击右上角Fork按钮

### 2. 配置Secrets

在你的Fork仓库中,进入 `Settings` > `Secrets and variables` > `Actions`,添加:

- `HF_TOKEN`: Hugging Face Token (可选,用于AI配图)
  - 获取地址: https://huggingface.co/settings/tokens
  
- `YOUTUBE_API_KEY`: YouTube Data API Key (可选,用于热门视频监控)
  - 获取地址: https://console.cloud.google.com/

### 3. 启用GitHub Actions

进入 `Actions` 标签页,点击 "I understand my workflows, go ahead and enable them"

### 4. 手动触发测试

在 `Actions` > `Daily Marketing Calendar Update` > `Run workflow`

### 5. 配置飞书自动化

参见下方 [飞书配置指南](#飞书配置指南)

## 📁 项目结构

```
marketing-calendar-api/
├── .github/
│   └── workflows/
│       └── daily-update.yml        # GitHub Actions定时任务
├── marketing_calendar_generator.py # 核心代码
├── output/
│   ├── latest.json                 # 最新日历(飞书调用此文件)
│   └── calendar_YYYY-MM-DD.json    # 历史日历
└── README.md
```

## 🔧 飞书配置指南

### Step 1: 创建飞书多维表格

表名: `📅 Haimeta全球营销日历`

**字段配置:**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日期 | 日期 | 事件日期 |
| 热点名称(中) | 文本 | 中文名称 |
| 热点名称(英) | 文本 | 英文名称 |
| 类型标签 | 多选 | 节日营销/竞品功能/热点事件/行业趋势/用户行为 |
| 优先级 | 单选 | 🔥高/⭐中/💡低 |
| 目标受众 | 文本 | 受众描述 |
| 文案标题(中) | 文本 | 中文营销标题 |
| 文案正文(中) | 文本 | 中文营销正文 |
| 文案标题(英) | 文本 | 英文营销标题 |
| 文案正文(英) | 文本 | 英文营销正文 |
| AI配图Prompt | 文本 | Hugging Face Prompt |
| 竞品动态 | 文本 | 竞品相关信息 |
| 时机建议 | 文本 | 营销时机 |
| 数据来源 | URL | 原始链接 |
| 状态 | 单选 | 待策划/进行中/已完成 |

### Step 2: 配置自动化流程

#### 触发器
- 类型: 定时触发
- 频率: 每天
- 时间: 09:00 AM
- 时区: Asia/Shanghai

#### 动作1: 发送HTTP请求
```
URL: https://YOUR_GITHUB_USERNAME.github.io/marketing-calendar-api/output/latest.json
方法: GET
存储为变量: calendar_data
```

#### 动作2: 循环创建记录
```javascript
// 遍历events数组
for (event in calendar_data.events) {
  创建记录 {
    日期: event.date
    热点名称(中): event.event_name
    热点名称(英): event.event_name_en
    类型标签: event.type
    优先级: event.priority
    目标受众: event.target_audience
    文案标题(中): event.marketing_copy.zh.headline
    文案正文(中): event.marketing_copy.zh.body
    文案标题(英): event.marketing_copy.en.headline
    文案正文(英): event.marketing_copy.en.body
    AI配图Prompt: event.image_prompts[0].prompt_zh
    时机建议: event.timing_suggestion
  }
}
```

#### 动作3: 发送通知
```
发送给: 你指定的飞书群
消息内容:
📅 营销日历已更新！
今日共抓取 {{calendar_data.total_events}} 个热点
🔥 高优先级: {{high_priority_count}} 个
查看完整日历 → [点击跳转]
```

## 📊 输出示例

```json
{
  "date": "2026-01-22",
  "generated_at": "2026-01-22T09:00:00Z",
  "total_events": 45,
  "events": [
    {
      "event_name": "农历小年",
      "event_name_en": "Chinese Little New Year",
      "type": ["节日营销"],
      "priority": "高",
      "marketing_copy": {
        "zh": {
          "headline": "🎨 农历小年 | Haimeta助你抢占节日营销先机",
          "body": "...",
          "cta": "立即体验 →"
        },
        "en": { ... }
      },
      "image_prompts": [
        {
          "prompt_zh": "农历小年主题,温馨节日氛围,现代扁平设计,高清8K",
          "hf_model_id": "stabilityai/stable-diffusion-xl-base-1.0"
        }
      ]
    }
  ]
}
```

## 🛠️ 本地开发

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/marketing-calendar-api.git
cd marketing-calendar-api

# 安装依赖
pip install requests

# 设置环境变量(可选)
export HF_TOKEN="your_huggingface_token"
export YOUTUBE_API_KEY="your_youtube_api_key"

# 运行生成器
python marketing_calendar_generator.py

# 查看输出
cat output/latest.json
```

## 📝 TODO

- [x] 全球节日数据库
- [x] 双语营销文案生成
- [x] AI配图Prompt生成
- [x] YouTube热门监控
- [ ] Web实时热点搜索
- [ ] 竞品RSS监控
- [ ] Instagram/TikTok数据(需付费API)
- [ ] 历史热点复盘功能

## 🤝 贡献

欢迎提交Issue和Pull Request!

## 📄 License

MIT License

## 💬 联系方式

- 项目负责人: ZZ
- 团队: Haimeta Product Team
