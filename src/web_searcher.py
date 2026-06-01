"""联网搜索模块 - 支持多个搜索引擎和中文优化"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class WebSearcher:
    """支持多引擎的联网搜索"""

    def __init__(
        self,
        engine: Optional[str] = None,
        api_key: Optional[str] = None,
        cache_dir: Optional[str] = None,
        cache_ttl: int = 86400
    ):
        """
        初始化搜索引擎

        Args:
            engine: 搜索引擎 (bing/google/duckduckgo)
            api_key: API Key
            cache_dir: 缓存目录
            cache_ttl: 缓存有效期（秒）
        """
        self.engine = engine or os.getenv("SEARCH_ENGINE", "bing")
        self.api_key = api_key or os.getenv("SEARCH_API_KEY")
        self.cache_dir = cache_dir or os.getenv("SEARCH_CACHE_DIR", "./data/search_cache")
        self.cache_ttl = cache_ttl
        self.enable_cache = os.getenv("CACHE_SEARCH_RESULTS", "true").lower() == "true"

        os.makedirs(self.cache_dir, exist_ok=True)
        logger.info(f"✅ 搜索引擎已初始化: {self.engine}")

    def search(
        self,
        query: str,
        language: str = "zh-CN",
        num_results: int = 5,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        执行搜索

        Args:
            query: 搜索查询
            language: 语言
            num_results: 结果数量
            use_cache: 使用缓存

        Returns:
            搜索结果列表
        """
        # 检查缓存
        if use_cache and self.enable_cache:
            cached = self._get_from_cache(query)
            if cached:
                logger.info(f"📦 使用缓存结果: {query}")
                return cached

        logger.info(f"🔍 搜索中: {query}")

        results = []

        if self.engine == "bing":
            results = self._search_bing(query, language, num_results)
        elif self.engine == "google":
            results = self._search_google(query, num_results)
        elif self.engine == "duckduckgo":
            results = self._search_duckduckgo(query, num_results)
        else:
            logger.error(f"❌ 不支持的搜索引擎: {self.engine}")
            return []

        # 缓存结果
        if results and self.enable_cache:
            self._save_to_cache(query, results)

        return results

    def _search_bing(
        self,
        query: str,
        language: str = "zh-CN",
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Bing 搜索"""
        if not self.api_key:
            logger.error("❌ Bing API Key 未配置")
            return []

        try:
            headers = {"Ocp-Apim-Subscription-Key": self.api_key}
            params = {
                "q": query,
                "count": num_results,
                "mkt": language,
                "responseFilter": "Webpages"
            }

            response = requests.get(
                "https://api.cognitive.microsoft.com/bing/v7.0/search",
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            results = []

            for item in data.get("webPages", {}).get("value", []):
                results.append({
                    "title": item.get("name", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "bing"
                })

            logger.info(f"✅ Bing 搜索完成: {len(results)} 个结果")
            return results

        except Exception as e:
            logger.error(f"❌ Bing 搜索错误: {e}")
            return []

    def _search_google(
        self,
        query: str,
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Google 搜索"""
        api_key = os.getenv("GOOGLE_API_KEY")
        engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

        if not api_key or not engine_id:
            logger.error("❌ Google 搜索未配置")
            return []

        try:
            params = {
                "q": query,
                "key": api_key,
                "cx": engine_id,
                "num": num_results,
                "hl": "zh-CN"
            }

            response = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            results = []

            for item in data.get("items", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "google"
                })

            logger.info(f"✅ Google 搜索完成: {len(results)} 个结果")
            return results

        except Exception as e:
            logger.error(f"❌ Google 搜索错误: {e}")
            return []

    def _search_duckduckgo(
        self,
        query: str,
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """DuckDuckGo 搜索（无需 API Key）"""
        try:
            from bs4 import BeautifulSoup

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            params = {"q": query}

            response = requests.get(
                "https://html.duckduckgo.com/",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            for item in soup.find_all('div', class_='result__wrapper')[:num_results]:
                title_elem = item.find('a', class_='result__url')
                snippet_elem = item.find('a', class_='result__snippet')

                if title_elem and snippet_elem:
                    results.append({
                        "title": title_elem.get_text().strip(),
                        "url": title_elem.get('href', ''),
                        "snippet": snippet_elem.get_text().strip(),
                        "source": "duckduckgo"
                    })

            logger.info(f"✅ DuckDuckGo 搜索完成: {len(results)} 个结果")
            return results

        except Exception as e:
            logger.error(f"❌ DuckDuckGo 搜索错误: {e}")
            return []

    def _get_cache_path(self, query: str) -> str:
        """获取缓存文件路径"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{query_hash}.json")

    def _get_from_cache(self, query: str) -> Optional[List[Dict]]:
        """从缓存获取结果"""
        cache_path = self._get_cache_path(query)

        if not os.path.exists(cache_path):
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > timedelta(seconds=self.cache_ttl):
                os.remove(cache_path)
                return None

            return cache_data['results']

        except Exception as e:
            logger.warning(f"⚠️ 缓存读取错误: {e}")
            return None

    def _save_to_cache(self, query: str, results: List[Dict]) -> None:
        """保存结果到缓存"""
        cache_path = self._get_cache_path(query)

        try:
            cache_data = {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "results": results
            }

            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.warning(f"⚠️ 缓存写入错误: {e}")


if __name__ == "__main__":
    searcher = WebSearcher(engine="duckduckgo")

    results = searcher.search("唐宋时期商业")
    for result in results:
        print(f"📌 {result['title']}")
        print(f"   {result['snippet']}")
        print(f"   {result['url']}\n")
