# path: f2/apps/tiktok/crawler.py

from f2.apps.tiktok.api import TiktokAPIEndpoints as tkendpoint
from f2.apps.tiktok.model import (
    UserProfile,
    UserPost,
    UserLike,
    UserMix,
    UserCollect,
    PostDetail,
    UserPlayList,
    PostComment,
)
from f2.apps.tiktok.utils import XBogusManager
from f2.crawlers.base_crawler import BaseCrawler
from f2.i18n.translator import _
from f2.log.logger import logger


class TiktokCrawler(BaseCrawler):
    def __init__(self, kwargs: dict = {}):
        proxies = {
            "http://": None,
            "https://": None,
        }

        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            "Referer": 'https://www.tiktok.com/',
            "Cookie": kwargs["cookie"],
        }

        super().__init__(proxies=proxies, crawler_headers=self.headers)

    async def fetch_user_profile(self, params: UserProfile):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_DETAIL, params.dict()
        )  # fmt: off
        logger.debug(_("用户信息接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_user_post(self, params: UserPost):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_POST, params.dict()
        )  # fmt: off
        logger.debug(_("主页作品接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_user_like(self, params: UserLike):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_LIKE, params.dict()
        )  # fmt: off
        logger.debug(_("喜欢作品接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_user_collect(self, params: UserCollect):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_COLLECT, params.dict()
        )
        logger.debug(_("收藏作品接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_user_play_list(self, params: UserPlayList):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_PLAY_LIST, params.dict()
        )
        logger.debug(_("合辑列表接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_user_mix(self, params: UserMix):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_MIX, params.dict()
        )  # fmt: off
        logger.debug(_("合辑作品接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_post_detail(self, params: PostDetail):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.AWEME_DETAIL, params.dict()
        )
        logger.debug(_("作品详情接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_post_comment(self, params: PostComment):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.POST_COMMENT, params.dict()
        )
        logger.debug(_("作品评论接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def fetch_post_recommend(self, params: PostDetail):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.HOME_RECOMMEND, params.dict()
        )
        logger.debug(_("首页推荐接口地址:" + endpoint))
        return await self._fetch_get_json(endpoint)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
