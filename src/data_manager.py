import asyncio
import json
import logging
import httpx
from pathlib import Path
from . import providers
from .config import Config, BASE_DIR

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self):
        self.cache_file = Config.DATA_DIR / "data_cache.json"
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    def load_cache(self):
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load cache: {e}")
        return {}

    def save_cache(self, data):
        try:
            with open(self.cache_file, "w") as f:
                # 将所有数据转换为可序列化的格式
                # 注意：如果有非基本类型需要处理，这里暂时假设都是基本类型
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    async def fetch_all_data(self):
        """并发获取所有数据，失败时回退到缓存"""
        cached_data = self.load_cache()
        
        # 检查是否是年终总结日 (12月31日)
        import pendulum
        now = pendulum.now(Config.TIMEZONE)
        is_year_end = (now.month == 12 and now.day == 31)
        
        # 定义任务列表
        tasks = {
            "weather": providers.get_weather(self.client),
            "github_commits": providers.get_github_commits(self.client),
            "vps_usage": providers.get_vps_info(self.client),
            "btc_price": providers.get_btc_data(self.client),
            "douban": providers.get_douban_stats(self.client),
        }
        
        if is_year_end:
            tasks["github_year_summary"] = providers.get_github_year_summary(self.client)
        
        results = {}
        keys = list(tasks.keys())
        futures = list(tasks.values())
        
        # 并发执行
        # return_exceptions=True 确保一个失败不会导致全部失败
        done_results = await asyncio.gather(*futures, return_exceptions=True)
        
        for key, result in zip(keys, done_results):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch {key}: {result}")
                # 使用缓存数据
                val = cached_data.get(key)
                if val is None:
                    # 设置默认值以防缓存也没有
                    if key == "weather": val = {"temp": "--", "desc": "NetErr", "icon": ""}
                    elif key == "github_commits": val = 0
                    elif key == "vps_usage": val = 0
                    elif key == "btc_price": val = {"usd": "---", "usd_24h_change": 0}
                    elif key == "douban": val = {"book": 0, "movie": 0, "music": 0}
                    elif key == "github_year_summary": val = None
                results[key] = val
            else:
                results[key] = result
        
        # 总是计算周进度（不需要网络）
        results["week_progress"] = providers.get_week_progress()
        results["is_year_end"] = is_year_end
        
        # 保存缓存
        self.save_cache(results)
        
        return results
