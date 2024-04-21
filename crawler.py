
import requests as requests

from config import COOKIE
from model import (
    UserProfile, UserPostRequest, UserFollowing,
)
from utils import XBogusManager, TiktokAPIEndpoints as tkendpoint

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    "Referer": 'https://www.tiktok.com/',
    'Cookie': COOKIE
}


class TiktokCrawler:

    async def fetch_user_profile(self, params: UserProfile):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_DETAIL, params.dict()
        )  # fmt: off
        try:
            response = requests.get(endpoint, headers=headers)
            return response.json()
        except Exception as e:
            return {}

    async def fetch_user_posts(self, params: UserPostRequest):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_POST, params.dict()
        )
        try:
            response = requests.get(endpoint, headers=headers)
            return response.json()
        except Exception as e:
            return {}

    async def fetch_user_following(self, params: UserFollowing):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_FOLLOWING, params.dict()
        )
        try:
            response = requests.get(endpoint, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            return {}
