import json
from typing import Optional
from urllib.parse import quote

import requests as requests
from jsonpath_ng import parse
from pydantic import BaseModel

from config import COOKIE, MSTOKEN
from utils import XBogusManager, TiktokAPIEndpoints as tkendpoint, get_timestamp


class BaseRequestModel(BaseModel):
    WebIdLastTime: str = str(get_timestamp("sec"))
    aid: str = "1988"
    app_language: str = "en"
    app_name: str = "tiktok_web"
    browser_language: str = "en-US"
    browser_name: str = "Mozilla"
    browser_online: str = "true"
    browser_platform: str = "Win32"
    browser_version: str = quote(
        "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        safe="",
    )
    channel: str = "tiktok_web"
    cookie_enabled: str = "true"
    device_id: str = "7306060721837852167"
    device_platform: str = "web_pc"
    focus_state: str = "true"
    from_page: str = "user"
    history_len: int = 20
    is_fullscreen: str = "false"
    is_page_visible: str = "true"
    language: str = "en"
    os: str = "windows"
    priority_region: str = ""
    referer: str = ""
    region: str = "DE"  # SG JP KR...
    root_referer: str = quote("https://www.tiktok.com/", safe="")
    screen_height: int = 1080
    screen_width: int = 1920
    webcast_language: str = "en"
    tz_name: str = quote("America/Log_Angeles", safe="")
    # verifyFp: str = VerifyFpManager.gen_verify_fp()
    msToken: str = MSTOKEN


class UserProfile(BaseRequestModel):
    secUid: Optional[str] = ""
    uniqueId: Optional[str] = ""


class UserPostRequest(BaseRequestModel):
    coverFormat: int = 2
    count: int = 35
    cursor: int = 0
    secUid: str


class MyFeedRequest(BaseRequestModel):
    coverFormat: int = 2
    count: int = 35
    cursor: int = 0
    pullType: int = 1
    level: int = 1
    def __init__(self, **data):
        super().__init__(**data)

        self.from_page = 'following'

class UserFollowing(BaseRequestModel):
    count: int = 30
    secUid: str
    scene: int = 21
    minCursor: int = 0
    maxCursor: int = 0


class UserLike(BaseRequestModel):
    coverFormat: int = 2
    count: int = 30
    cursor: int = 0
    secUid: str


class UserCollect(BaseRequestModel):
    coverFormat: int = 2
    count: int = 30
    cursor: int = 0
    secUid: str


class UserPlayList(BaseRequestModel):
    count: int = 30
    cursor: int = 0
    secUid: str


class UserMix(BaseRequestModel):
    count: int = 30
    cursor: int = 0
    mixId: str


class PostDetail(BaseRequestModel):
    itemId: str


class PostComment(BaseRequestModel):
    aweme_id: str
    count: int = 20
    cursor: int = 0
    current_region: str = ""


class JSONModel:
    def __init__(self, data):
        self._data = data

    def _get_attr_value(self, jsonpath_expr):
        expr = parse(jsonpath_expr)
        # expr = parser.parse(jsonpath_expr)
        result = expr.find(self._data)
        if result:
            return (
                [match.value for match in result]
                if len(result) > 1
                else result[0].value
            )
        return None

    def _get_list_attr_value(self, jsonpath_expr, as_json=False):
        values = self._get_attr_value(jsonpath_expr)

        if isinstance(values, (list, tuple)):
            if as_json:
                return json.dumps(values, ensure_ascii=False)
            return values
        if as_json:
            return (
                json.dumps([values], ensure_ascii=False) if values is not None else "[]"
            )

        return [values] if values is not None else []


class TiktokCrawler:
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        "Referer": 'https://www.tiktok.com/',
        'Cookie': COOKIE
    }

    msToken = ''

    def __init__(self, cookie: str = None):
        if not cookie:
            return

        self.headers['Cookie'] = cookie
        cookie_items = cookie.split('; ')
        cookie_dict = {}
        for item in cookie_items:
            key, value = item.split('=', 1)
            cookie_dict[key.strip()] = value.strip()
        self.msToken = cookie_dict['msToken']

    async def fetch_user_profile(self, params: UserProfile):
        params.msToken = self.msToken or params.msToken

        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_DETAIL, params.dict()
        )  # fmt: off
        try:
            response = requests.get(endpoint, headers=self.headers)
            return response.json()
        except Exception as e:
            return {}

    async def fetch_user_posts(self, params: UserPostRequest):
        params.msToken = self.msToken or params.msToken

        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_POST, params.dict()
        )
        try:
            response = requests.get(endpoint, headers=self.headers)
            return response.json()
        except Exception as e:
            return {}

    async def fetch_my_feeds(self, params: MyFeedRequest):
        params.msToken = self.msToken or params.msToken

        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_FEED, params.dict()
        )
        try:
            response = requests.get(endpoint, headers=self.headers)
            return response.json()
        except Exception as e:
            return {}

    async def fetch_user_following(self, params: UserFollowing):
        params.msToken = self.msToken or params.msToken

        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_FOLLOWING, params.dict()
        )
        try:
            response = requests.get(endpoint, headers=self.headers)
            data = response.json()
            return data
        except Exception as e:
            return {}
