# path: f2/apps/tiktok/crawler.py
from urllib import request

import requests as requests

from f2.apps.tiktok.api import TiktokAPIEndpoints as tkendpoint
from f2.apps.tiktok.model import (
    UserProfile, UserPost,
)
from f2.apps.tiktok.utils import XBogusManager
headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            "Referer": 'https://www.tiktok.com/',
        }

class TiktokCrawler:

    async def fetch_user_profile(self, params: UserProfile):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_DETAIL, params.dict()
        )  # fmt: off

        response = requests.get(endpoint, headers=headers)
        return response.json()


    async def fetch_user_posts(self, params: UserPost):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_POST, params.dict()
        )
        response = requests.get(endpoint, headers=headers)
        return response.json()
