# path: f2/apps/tiktok/handler.py

from crawler import TiktokCrawler
from filter import (
    UserProfileFilter, UserPostFilter, UserFollowingFilter,
)
from model import (
    UserProfile, UserPost, UserFollowing,
)

class TikTokClient:

    # 需要忽略的字段（需过滤掉有时效性的字段）
    ignore_fields = ["video_play_addr", "images", "video_bit_rate", "cover"]

    async def handler_user_profile(
        self, secUid: str ="", uniqueId: str = ""
    ) -> UserProfileFilter:
        if not secUid and not uniqueId:
            raise ValueError("至少提供 secUid 或 uniqueId 中的一个参数")

        crawler = TiktokCrawler()
        params = UserProfile(region="US", secUid=secUid, uniqueId=uniqueId)
        response = await crawler.fetch_user_profile(params)
        return UserProfileFilter(response)

    async def get_user_posts(self, secUid: str = "", cursor: int = 0):
        crawler = TiktokCrawler()
        params = UserPost(secUid=secUid, cursor=cursor)
        response = await crawler.fetch_user_posts(params)
        video = UserPostFilter(response)
        return video

    async def get_user_following(self, secUid: str, minCursor: int = 0, maxCursor: int = 0):
        crawler = TiktokCrawler()
        params = UserFollowing(secUid=secUid, cursor=minCursor, maxCursor=maxCursor)
        response = await crawler.fetch_user_following(params)
        following = UserFollowingFilter(response)
        return following
