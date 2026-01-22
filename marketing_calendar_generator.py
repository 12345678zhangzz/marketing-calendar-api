import os
import json
import requests
import random
from datetime import datetime, timedelta

# ================= 配置区域 =================
# 飞书免费版限制每日自动写入 5 条，我们这里做智能截取
MAX_EVENTS_PER_DAY = 5  

# 从 GitHub Secrets 获取密钥
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
# ===========================================

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# --- 1. 获取真实节日数据 (模拟数据库，可扩展) ---
def get_global_holidays():
    # 这里列出近期的真实营销节点
    # 实际项目中可以使用 python-holidays 库或外部 API
    base_events = [
        {"name": "春节 (Chinese New Year)", "en": "Chinese New Year", "date": "2026-02-17", "type": ["节日营销"], "priority": "高"},
        {"name": "情人节", "en": "Valentine's Day", "date": "2026-02-14", "type": ["节日营销", "用户行为"], "priority": "高"},
        {"name": "超级碗", "en": "Super Bowl", "date": "2026-02-08", "type": ["热点事件"], "priority": "高"},
        {"name": "世界移动通信大会 (MWC)", "en": "MWC Barcelona", "date": "2026-03-02", "type": ["行业趋势"], "priority": "中"},
        {"name": "妇女节", "en": "International Women's Day", "date": "2026-03-08", "type": ["节日营销"], "priority": "高"},
    ]
    
    today = datetime.now()
    upcoming = []
    
    for evt in base_events:
        evt_date = datetime.strptime(evt['date'], "%Y-%m-%d")
        days_diff = (evt_date - today).days
        
        # 只关注未来 45 天内的热点
        if 0 <= days_diff <= 45:
            evt['target_audience'] = "大众, 节日消费者"
            evt['source'] = "global_holidays"
            # 简单的文案模板 (如果 HF 失败用这个兜底)
            evt['marketing_copy'] = {
                "zh": {"headline": f"🔥 {evt['name']} 倒计时 {days_diff} 天", "body": f"建议提前布局 {evt['name']} 营销活动..."},
                "en": {"headline": f"Upcoming: {evt['en']} in {days_diff} days", "body": f"Prepare your campaign for {evt['en']}..."}
            }
            evt['image_prompts'] = [{"prompt_zh": f"{evt['name']} 主题海报, 节日氛围", "prompt_en": f"{evt['en']} theme poster, 8k"}]
            upcoming.append(evt)
            
    return upcoming

# --- 2. 调用 YouTube API 获取真实趋势 ---
def fetch_youtube_trends():
    if not YOUTUBE_API_KEY:
        print("⚠️ 未检测到 YOUTUBE_API_KEY，跳过 YouTube 数据抓取")
        return []

    print("📡 正在连接 YouTube API...")
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=5&key={YOUTUBE_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        trends = []
        if "items" in data:
            for item in data["items"]:
                title = item["snippet"]["title"]
                channel = item["snippet"]["channelTitle"]
                
                trends.append({
                    "name": f"YouTube热榜: {title[:20]}...",
                    "en": title,
                    "date": get_current_date(),
                    "type": ["用户行为", "热点事件"],
                    "priority": "中", # 趋势类通常优先级为中
                    "target_audience": "视频观众, 社交媒体用户",
                    "source": "youtube_api",
                    "marketing_copy": {
                        "zh": {"headline": f"热点追踪: {title[:15]}", "body": f"YouTube 热门视频趋势，来自频道 {channel}"},
                        "en": {"headline": f"Trending: {title[:30]}", "body": f"Viral video from {channel}"}
                    },
                    "image_prompts": [{"prompt_zh": "社交媒体热门风格, 现代感", "prompt_en": "Trending on social media, modern style"}]
                })
        return trends
    except Exception as e:
        print(f"❌ YouTube API 调用失败: {e}")
        return []

# --- 3. 调用 Hugging Face API 优化文案 (可选) ---
def enhance_with_ai(events):
    if not HF_TOKEN:
        return events
        
    # 这里可以添加调用 HF Inference API 的逻辑
    # 为了保证代码稳定性，这里做简单的逻辑处理，实际可扩展
    print("🧠 AI 正在优化部分文案 (模拟调用)...")
    return events

# --- 主程序 ---
def main():
    print("🚀 开始执行营销日历生成任务...")
    
    all_events = []
    
    # 1. 获取节日
    holidays = get_global_holidays()
    all_events.extend(holidays)
    
    # 2. 获取 YouTube 趋势
    yt_trends = fetch_youtube_trends()
    all_events.extend(yt_trends)
    
    # 3. 如果数据太少，生成一些占位数据防止表格空着
    if len(all_events) < 3:
        all_events.append({
            "name": "行业趋势: AI生成内容", 
            "en": "Trend: AIGC Boom", 
            "date": get_current_date(), 
            "type": ["行业趋势"], 
            "priority": "中",
            "target_audience": "内容创作者",
            "source": "backup_data",
            "marketing_copy": {"zh": {"headline": "AIGC 持续升温", "body": "关注 AI 对内容生产的影响"}, "en": {"headline": "AIGC is heating up", "body": "Focus on AI content creation"}},
            "image_prompts": [{"prompt_zh": "AI 机器人, 未来科技", "prompt_en": "AI robot, futuristic"}]
        })

    # 4. 核心排序逻辑：高优先级 > 中优先级 > 低优先级
    priority_map = {"高": 0, "中": 1, "低": 2}
    # 先按优先级排，再按日期排
    all_events.sort(key=lambda x: (priority_map.get(x.get('priority', '低'), 3), x.get('date')))
    
    # 5. 截取 Top 5 (适配飞书)
    final_events = all_events[:MAX_EVENTS_PER_DAY]
    
    # 6. 标准化输出格式
    output_events = []
    for evt in final_events:
        output_events.append({
            "id": f"evt_{random.randint(10000,99999)}",
            "date": evt['date'],
            "event_name": evt['name'],
            "event_name_en": evt['en'],
            "type": evt['type'], # 这是一个列表
            "priority": evt['priority'],
            "target_audience": evt.get('target_audience', '大众'),
            "marketing_copy": evt['marketing_copy'],
            "image_prompts": evt['image_prompts'],
            "timing_suggestion": "建议立即跟进" if evt['priority'] == "高" else "保持关注"
        })

    output_data = {
        "date": get_current_date(),
        "total_events": len(output_events),
        "events": output_events
    }
    
    # 7. 保存
    os.makedirs("output", exist_ok=True)
    with open("output/latest.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 完成！成功抓取并生成 {len(output_events)} 条数据 (已按优先级排序)")

if __name__ == "__main__":
    main()
