# path: f2/apps/tiktok/handler.py

from f2.apps.tiktok.crawler import TiktokCrawler
from f2.apps.tiktok.filter import (
    UserProfileFilter, UserPostFilter,
)
from f2.apps.tiktok.model import (
    UserProfile, UserPost,
)
from f2.cli.cli_console import RichConsoleManager
from f2.i18n.translator import _
from f2.log.logger import logger
from f2.utils.mode_handler import mode_function_map

rich_console = RichConsoleManager().rich_console
rich_prompt = RichConsoleManager().rich_prompt


class TiktokHandler2:

    # 需要忽略的字段（需过滤掉有时效性的字段）
    ignore_fields = ["video_play_addr", "images", "video_bit_rate", "cover"]

    async def handler_user_profile(
        self, secUid: str ="", uniqueId: str = ""
    ) -> UserProfileFilter:
        if not secUid and not uniqueId:
            raise ValueError(_("至少提供 secUid 或 uniqueId 中的一个参数"))

        crawler = TiktokCrawler()
        params = UserProfile(region="US", secUid=secUid, uniqueId=uniqueId)
        response = await crawler.fetch_user_profile(params)
        return UserProfileFilter(response)

    async def get_user_posts(self, secUid: str = "", cursor: int = 0):
        crawler = TiktokCrawler()
        params = UserPost(secUid=secUid, cursor=cursor, count=35)
        response = await crawler.fetch_user_posts(params)
        video = UserPostFilter(response)
        return video

async def main(kwargs):
    mode = kwargs.get("mode")
    if mode in mode_function_map:
        await mode_function_map[mode](TiktokHandler2())
    else:
        logger.error(_("不存在该模式: {0}").format(mode))
        rich_console.print(_("不存在该模式: {0}").format(mode))
