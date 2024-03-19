# path: f2/apps/tiktok/models.py
import json
from typing import Optional
from urllib.parse import quote

from jsonpath_ng import parse
from pydantic import BaseModel

from utils import get_timestamp


# Model
class BaseRequestModel(BaseModel):
    WebIdLastTime: str = str(get_timestamp("sec"))
    aid: str = "1988"
    app_language: str = "zh-Hans"
    app_name: str = "tiktok_web"
    browser_language: str = "zh-CN"
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
    history_len: int = 4
    is_fullscreen: str = "false"
    is_page_visible: str = "true"
    language: str = "zh-Hans"
    os: str = "windows"
    priority_region: str = ""
    referer: str = ""
    region: str = "SG"  # SG JP KR...
    root_referer: str = quote("https://www.tiktok.com/", safe="")
    screen_height: int = 1080
    screen_width: int = 1920
    webcast_language: str = "zh-Hans"
    tz_name: str = quote("Asia/Hong_Kong", safe="")
    # verifyFp: str = VerifyFpManager.gen_verify_fp()
    # msToken: str = TokenManager.gen_real_msToken()
    msToken: str = 'x541bHi1s7WSeHchOdUW2yAEOEP7zrlEl1OGzqFe6J3tq-HZYOtucwzWK2O_2gA3E9xoxmG7QN6dsaOp1T9HuCIbKNm4wLQv-nSuZhH8OQyUvHu2ySp1EDp5xt3STiYycrQ5VJg='


# router model
class UserProfile(BaseRequestModel):
    secUid: Optional[str] = ""
    uniqueId: Optional[str] = ""


class UserPost(BaseRequestModel):
    coverFormat: int = 2
    count: int = 35
    cursor: int = 0
    secUid: str

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
