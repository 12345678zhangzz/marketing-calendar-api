import os
import json
import random
from datetime import datetime
import requests

# ---------------- 配置区域 ----------------
# ⚠️ 关键修改：只保留 5 个，完美避开飞书收费限制
MAX_EVENTS_PER_DAY = 5  
# ----------------------------------------

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_mock_holidays():
    # 这里为了演示，生成一些固定的模拟数据
    # 实际使用中，你可以替换为真实的 API 调用
    base_date = get_current_date()
    
    events = [
        {
            "id": "holiday_sample_1",
            "event_name": "示例: 国际咖啡日",
            "event_name_en": "International Coffee Day",
            "date": base_date,
            "type": ["节日营销"],
            "priority": "高",
            "target_audience": "咖啡爱好者, 上班族",
            "marketing_copy": {
                "zh": {"headline": "☕️ 今天是国际咖啡日，来一杯续命！", "body": "用一杯香浓咖啡开启高效工作日..."},
                "en": {"headline": "Celebrate International Coffee Day!", "body": "Boost your day with a cup of joy..."}
            },
            "image_prompts": [{"prompt_zh": "一杯热气腾腾的拿铁, 阳光洒在木桌上, 高清摄影", "prompt_en": "Hot latte on wooden table, sunlight, photorealistic, 8k"}]
        },
        {
            "id": "trend_sample_2",
            "event_name": "趋势: AI工具大爆发",
            "event_name_en": "AI Tools Boom",
            "date": base_date,
            "type": ["行业趋势", "竞品功能"],
            "priority": "中",
            "target_audience": "科技极客, 创业者",
            "marketing_copy": {
                "zh": {"headline": "AI时代已来，你跟上了吗？", "body": "盘点本周最火的5款AI生产力工具..."},
                "en": {"headline": "AI Revolution is Here", "body": "Top 5 AI tools you need to know this week..."}
            },
            "image_prompts": [{"prompt_zh": "未来感科技城市, 机器人与人类协作, 赛博朋克风格", "prompt_en": "Futuristic tech city, robot and human collaboration, cyberpunk style"}]
        }
    ]
    
    # 模拟生成更多数据以测试排序功能
    for i in range(3, 10):
        events.append({
            "id": f"auto_gen_{i}",
            "event_name": f"自动生成的热点 {i}",
            "event_name_en": f"Auto Generated Event {i}",
            "date": base_date,
            "type": ["热点事件"],
            "priority": "低",
            "target_audience": "大众",
            "marketing_copy": {
                "zh": {"headline": f"热点 {i} 来了", "body": "这里是正文内容..."},
                "en": {"headline": f"Event {i} is here", "body": "Content body..."}
            },
            "image_prompts": [{"prompt_zh": "抽象背景", "prompt_en": "Abstract background"}]
        })
        
    return events

def main():
    print("开始生成营销日历...")
    
    # 1. 获取原始数据 (这里用模拟函数代替，保留你的原有逻辑结构)
    all_events = get_mock_holidays()
    
    # 2. 核心优化：按优先级排序 (高 > 中 > 低)
    priority_map = {"高": 0, "中": 1, "低": 2}
    # 按照优先级数字从小到大排序
    all_events.sort(key=lambda x: priority_map.get(x.get('priority', '低'), 3))
    
    # 3. 核心优化：只取前 5 个 (完美适配飞书免费版)
    final_events = all_events[:MAX_EVENTS_PER_DAY]
    
    # 4. 构建输出结构
    output_data = {
        "date": get_current_date(),
        "total_events": len(final_events),
        "events": final_events
    }
    
    # 5. 保存文件
    os.makedirs("output", exist_ok=True)
    with open("output/latest.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print(f"成功生成 {len(final_events)} 个热点数据！已保存到 output/latest.json")

if __name__ == "__main__":
    main()
