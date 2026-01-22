#!/usr/bin/env python3
"""
Haimeta Marketing Calendar Generator
零预算全自动营销日历生成系统
Author: Claude + ZZ
Date: 2025-01-23
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests

class MarketingCalendarGenerator:
    """营销日历生成器主类"""
    
    def __init__(self):
        """初始化配置"""
        self.hf_token = os.getenv('HF_TOKEN', '')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY', '')
        self.today = datetime.now().strftime('%Y-%m-%d')
        
        # 全球节日数据库(示例数据,实际应该更完整)
        self.GLOBAL_HOLIDAYS = self._load_holidays_database()
    
    def _load_holidays_database(self) -> Dict:
        """加载全球节日数据库"""
        return {
            '01-01': {'name': '元旦', 'name_en': 'New Year\'s Day', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '高'},
            '01-23': {'name': '农历小年', 'name_en': 'Chinese Little New Year', 'regions': ['中国', '新加坡'], 'type': ['节日营销'], 'priority': '高'},
            '02-14': {'name': '情人节', 'name_en': 'Valentine\'s Day', 'regions': ['全球'], 'type': ['节日营销', '电商节点'], 'priority': '高'},
            '03-08': {'name': '国际妇女节', 'name_en': 'International Women\'s Day', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '中'},
            '03-17': {'name': '圣帕特里克节', 'name_en': 'St. Patrick\'s Day', 'regions': ['美国', '爱尔兰'], 'type': ['节日营销'], 'priority': '中'},
            '04-01': {'name': '愚人节', 'name_en': 'April Fools\' Day', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '中'},
            '04-22': {'name': '世界地球日', 'name_en': 'Earth Day', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '中'},
            '05-01': {'name': '劳动节', 'name_en': 'Labor Day', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '中'},
            '05-12': {'name': '母亲节', 'name_en': 'Mother\'s Day', 'regions': ['美国', '欧洲'], 'type': ['节日营销', '电商节点'], 'priority': '高'},
            '06-16': {'name': '父亲节', 'name_en': 'Father\'s Day', 'regions': ['美国', '欧洲'], 'type': ['节日营销', '电商节点'], 'priority': '高'},
            '07-04': {'name': '美国独立日', 'name_en': 'Independence Day (US)', 'regions': ['美国'], 'type': ['节日营销'], 'priority': '高'},
            '08-08': {'name': '国际猫咪日', 'name_en': 'International Cat Day', 'regions': ['全球'], 'type': ['用户行为'], 'priority': '低'},
            '09-21': {'name': '国际和平日', 'name_en': 'International Day of Peace', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '中'},
            '10-31': {'name': '万圣节', 'name_en': 'Halloween', 'regions': ['美国', '欧洲'], 'type': ['节日营销', '电商节点'], 'priority': '高'},
            '11-11': {'name': '双十一', 'name_en': 'Singles\' Day', 'regions': ['中国'], 'type': ['电商节点'], 'priority': '高'},
            '11-28': {'name': '感恩节', 'name_en': 'Thanksgiving', 'regions': ['美国'], 'type': ['节日营销', '电商节点'], 'priority': '高'},
            '12-24': {'name': '平安夜', 'name_en': 'Christmas Eve', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '高'},
            '12-25': {'name': '圣诞节', 'name_en': 'Christmas', 'regions': ['全球'], 'type': ['节日营销', '电商节点'], 'priority': '高'},
            '12-31': {'name': '跨年夜', 'name_en': 'New Year\'s Eve', 'regions': ['全球'], 'type': ['节日营销'], 'priority': '高'},
        }
    
    def generate_calendar(self, date: str = None) -> Dict[str, Any]:
        """
        主函数:生成营销日历
        
        Args:
            date: 日期 YYYY-MM-DD,默认今天
            
        Returns:
            完整的营销日历JSON
        """
        if not date:
            date = self.today
        
        print(f"[INFO] 开始生成 {date} 的营销日历...")
        
        events = []
        
        # 1. 获取全球节日
        print("[1/5] 查询全球节日...")
        holidays = self.get_global_holidays(date)
        events.extend(holidays)
        print(f"  ✓ 找到 {len(holidays)} 个节日")
        
        # 2. YouTube热门监控(如果有API Key)
        if self.youtube_api_key:
            print("[2/5] 监控YouTube热门...")
            youtube_events = self.get_youtube_trending(date)
            events.extend(youtube_events)
            print(f"  ✓ 找到 {len(youtube_events)} 个YouTube热点")
        else:
            print("[2/5] 跳过YouTube(无API Key)")
        
        # 3. 竞品监控(RSS)
        print("[3/5] 监控竞品动态...")
        competitor_events = self.monitor_competitors(date)
        events.extend(competitor_events)
        print(f"  ✓ 找到 {len(competitor_events)} 个竞品更新")
        
        # 4. 生成营销文案和配图Prompt
        print("[4/5] 生成营销内容...")
        for event in events:
            event['marketing_copy'] = self.generate_marketing_copy(event)
            event['image_prompts'] = self.generate_image_prompts(event)
        print(f"  ✓ 为 {len(events)} 个事件生成内容")
        
        # 5. 优先级排序
        print("[5/5] 排序和优化...")
        events = self.rank_by_priority(events)
        
        result = {
            'date': date,
            'generated_at': datetime.now().isoformat(),
            'total_events': len(events),
            'categories': self._count_categories(events),
            'events': events
        }
        
        print(f"[SUCCESS] 共生成 {len(events)} 个营销热点")
        return result
    
    def get_global_holidays(self, date: str) -> List[Dict]:
        """获取全球节日"""
        month_day = date[5:]  # 提取 MM-DD
        holidays = []
        
        # 检查当天节日
        if month_day in self.GLOBAL_HOLIDAYS:
            holiday = self.GLOBAL_HOLIDAYS[month_day]
            holidays.append({
                'id': f'holiday_{month_day}',
                'event_name': holiday['name'],
                'event_name_en': holiday['name_en'],
                'source': 'global_holidays',
                'date': date,
                'type': holiday['type'],
                'priority': holiday['priority'],
                'regions': holiday['regions'],
                'target_audience': self._get_target_audience(holiday),
                'alert_days': 7 if holiday['priority'] == '高' else 3
            })
        
        # 检查未来7天的重大节日(用于提前预警)
        for i in range(1, 8):
            future_date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
            future_md = future_date[5:]
            
            if future_md in self.GLOBAL_HOLIDAYS:
                holiday = self.GLOBAL_HOLIDAYS[future_md]
                if holiday['priority'] == '高':  # 只预警高优先级
                    holidays.append({
                        'id': f'holiday_upcoming_{future_md}',
                        'event_name': f"即将到来: {holiday['name']}",
                        'event_name_en': f"Upcoming: {holiday['name_en']}",
                        'source': 'global_holidays',
                        'date': future_date,
                        'type': holiday['type'] + ['提前预警'],
                        'priority': '高',
                        'regions': holiday['regions'],
                        'target_audience': self._get_target_audience(holiday),
                        'alert_days': i
                    })
        
        return holidays
    
    def get_youtube_trending(self, date: str) -> List[Dict]:
        """获取YouTube创意类热门视频"""
        if not self.youtube_api_key:
            return []
        
        trending = []
        
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': 'AI art tools OR AI design OR creative AI OR generative AI',
                'type': 'video',
                'order': 'viewCount',
                'publishedAfter': (datetime.now() - timedelta(days=7)).isoformat() + 'Z',
                'maxResults': 15,
                'key': self.youtube_api_key,
                'relevanceLanguage': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    video_id = item['id']['videoId']
                    title = item['snippet']['title']
                    channel = item['snippet']['channelTitle']
                    
                    trending.append({
                        'id': f"youtube_{video_id}",
                        'event_name': f"YouTube热门: {title[:50]}...",
                        'event_name_en': f"YouTube Trending: {title[:50]}...",
                        'source': 'youtube_trending',
                        'date': date,
                        'type': ['用户行为', '行业趋势'],
                        'priority': '中',
                        'regions': ['全球'],
                        'target_audience': 'AI创作者、设计师、科技爱好者',
                        'video_url': f"https://youtube.com/watch?v={video_id}",
                        'channel': channel,
                        'alert_days': 0
                    })
        except Exception as e:
            print(f"  ⚠ YouTube API错误: {e}")
        
        return trending
    
    def monitor_competitors(self, date: str) -> List[Dict]:
        """监控竞品动态(简化版,实际应该接入RSS)"""
        # 这里是模拟数据,实际部署时应该接入真实RSS
        competitors_mock = []
        
        # 竞品列表
        competitors = ['Pollo', 'Higgsfield', 'OpenArt', 'Pixverse', 'Kling', '即梦']
        
        # 模拟竞品动态(实际应该爬取RSS或官网)
        for comp in competitors[:2]:  # 先mock 2个
            competitors_mock.append({
                'id': f'competitor_{comp.lower()}_{date}',
                'event_name': f'{comp}可能有新动态',
                'event_name_en': f'{comp} Potential Updates',
                'source': 'competitor_updates',
                'date': date,
                'type': ['竞品功能'],
                'priority': '中',
                'regions': ['全球'],
                'target_audience': 'AI工具用户、竞品分析师',
                'competitor_name': comp,
                'alert_days': 0
            })
        
        return competitors_mock
    
    def generate_marketing_copy(self, event: Dict) -> Dict:
        """生成双语营销文案"""
        event_name = event.get('event_name', '')
        event_name_en = event.get('event_name_en', '')
        event_type = event.get('type', [])
        
        # 根据类型选择文案模板
        if '节日营销' in event_type:
            zh_headline = f"🎨 {event_name} | Haimeta助你抢占节日营销先机"
            zh_body = f"把握{event_name}营销窗口,用AI生成惊艳视觉内容。Haimeta提供海量模板,一键生成专业级节日海报、视频素材。"
            en_headline = f"🎨 {event_name_en} | Create Stunning Visuals with Haimeta"
            en_body = f"Leverage AI to create professional designs for {event_name_en}. Haimeta makes holiday marketing easy and impactful."
        elif '竞品功能' in event_type:
            zh_headline = f"⚡ 竞品动态: {event_name}"
            zh_body = f"关注竞品最新功能,Haimeta持续创新,保持领先优势。"
            en_headline = f"⚡ Competitor Alert: {event_name_en}"
            en_body = f"Stay ahead with Haimeta's continuous innovation."
        else:
            zh_headline = f"📊 {event_name} | Haimeta AI创意工具"
            zh_body = f"抓住{event_name}的机会,用Haimeta AI工具创作专业内容。"
            en_headline = f"📊 {event_name_en} | Haimeta AI Creative Tools"
            en_body = f"Seize the opportunity with Haimeta AI tools."
        
        return {
            'zh': {
                'headline': zh_headline,
                'body': zh_body,
                'cta': '立即体验 →',
                'hashtags': [f'#AI设计', f'#{event_name}', '#Haimeta']
            },
            'en': {
                'headline': en_headline,
                'body': en_body,
                'cta': 'Try Now →',
                'hashtags': ['#AIDesign', f'#{event_name_en.replace(" ", "")}', '#Haimeta']
            }
        }
    
    def generate_image_prompts(self, event: Dict) -> List[Dict]:
        """生成AI配图Prompt(基于Hugging Face免费模型)"""
        event_name = event.get('event_name', '')
        event_name_en = event.get('event_name_en', '')
        event_type = event.get('type', [])
        
        # 根据类型选择风格
        if '节日营销' in event_type:
            style_zh = f"{event_name}主题,温馨节日氛围,现代扁平设计,明亮色彩"
            style_en = f"{event_name_en} theme, festive atmosphere, modern flat design, vibrant colors"
        elif '竞品功能' in event_type:
            style_zh = "科技感,对比分析图,专业商务风格"
            style_en = "tech aesthetic, comparison chart, professional business style"
        else:
            style_zh = "科技感,未来主义,渐变配色,简约设计"
            style_en = "futuristic tech aesthetic, gradient colors, minimalist design"
        
        return [
            {
                'model': 'Stable Diffusion XL (Hugging Face)',
                'style': style_zh,
                'prompt_zh': f"{style_zh},高清,8K,专业设计,无文字",
                'prompt_en': f"{style_en}, high quality, 8K, professional design, no text",
                'hf_model_id': 'stabilityai/stable-diffusion-xl-base-1.0',
                'free_api': True,
                'api_endpoint': 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0',
                'usage_note': '复制prompt到Haimeta平台使用'
            }
        ]
    
    def rank_by_priority(self, events: List[Dict]) -> List[Dict]:
        """按优先级排序事件"""
        priority_order = {'高': 3, '中': 2, '低': 1}
        
        def sort_key(event):
            priority_score = priority_order.get(event.get('priority', '低'), 1)
            alert_days = event.get('alert_days', 0)
            # 优先级高的在前,提前预警天数多的在前
            return (-priority_score, -alert_days)
        
        return sorted(events, key=sort_key)
    
    def _count_categories(self, events: List[Dict]) -> Dict:
        """统计事件分类"""
        categories = {
            'global_holidays': 0,
            'youtube_trending': 0,
            'web_trends': 0,
            'competitor_updates': 0,
            'industry_events': 0
        }
        
        for event in events:
            source = event.get('source', '')
            if source in categories:
                categories[source] += 1
        
        return categories
    
    def _get_target_audience(self, holiday: Dict) -> str:
        """根据节日生成目标受众"""
        if '电商节点' in holiday.get('type', []):
            return '在线购物者、礼物购买者、电商卖家'
        elif '节日营销' in holiday.get('type', []):
            return '品牌营销人员、社交媒体运营者、内容创作者'
        else:
            return '普通用户、创意设计师'


def main():
    """主函数"""
    print("="*60)
    print("Haimeta营销日历生成器")
    print("零预算全自动营销热点系统")
    print("="*60)
    
    generator = MarketingCalendarGenerator()
    result = generator.generate_calendar()
    
    # 保存到文件
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f'{output_dir}/calendar_{result["date"]}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 同时保存为latest.json(供飞书调用)
    latest_file = f'{output_dir}/latest.json'
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 日历已保存: {output_file}")
    print(f"✓ 最新版本: {latest_file}")
    print(f"\n摘要:")
    print(f"  - 总事件数: {result['total_events']}")
    print(f"  - 节日: {result['categories']['global_holidays']}")
    print(f"  - YouTube热点: {result['categories']['youtube_trending']}")
    print(f"  - 竞品动态: {result['categories']['competitor_updates']}")
    
    # 显示高优先级事件
    high_priority = [e for e in result['events'] if e.get('priority') == '高']
    if high_priority:
        print(f"\n🔥 高优先级事件 ({len(high_priority)}个):")
        for event in high_priority[:5]:
            print(f"  - {event['event_name']} ({event['date']})")


if __name__ == '__main__':
    main()
