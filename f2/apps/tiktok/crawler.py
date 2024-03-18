# path: f2/apps/tiktok/crawler.py

from f2.apps.tiktok.api import TiktokAPIEndpoints as tkendpoint
from f2.apps.tiktok.model import (
    UserProfile,
)
from f2.apps.tiktok.utils import XBogusManager
from f2.crawlers.base_crawler import BaseCrawler


class TiktokCrawler(BaseCrawler):
    def __init__(self, kwargs: dict = {}):

        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            "Referer": 'https://www.tiktok.com/',
        }

        super().__init__(crawler_headers=self.headers)

    async def fetch_user_profile(self, params: UserProfile):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_DETAIL, params.dict()
        )  # fmt: off
        return await self._fetch_get_json(endpoint)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
