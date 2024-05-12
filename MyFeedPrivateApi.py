import asyncio
import time
from pprint import pprint
from unittest import IsolatedAsyncioTestCase

from StudioY.StudioYClient import StudioYClient, get_account_id_and_cookie
from crawler import TiktokCrawler, UserPostRequest, MyFeedRequest
from filter import UserPostsFilter

aweme_ids = set()
class IFeedPostRecipient:
    def on_post_list(self, posts: UserPostsFilter) -> bool:
        # res = StudioYClient().sync_user_videos(posts.itemList)
        # pprint(res)
        # return bool(res and res.get('isSuccess'))
        aweme_ids.update([post.awemeId for post in posts.itemList])
        breakpoint()
        return posts


class MyFeed:
    __last_request: MyFeedRequest | None
    __last_response: UserPostsFilter | None
    __last_success_response: UserPostsFilter | None
    __can_continue: bool
    __load_complete: bool
    __cookie: str = None

    def __init__(self, recipient: IFeedPostRecipient = None, cookie: str = None):
        self.__cookie = cookie
        self.recipient = recipient
        self.api = TiktokCrawler(self.__cookie)
        self.__last_request = None
        self.__last_response = None
        self.__can_continue = True
        self.__load_complete = False
        self.__last_retry = 0
        self.__has_error = False

    async def load_full_list(self):
        while self.__can_continue and not self.__load_complete:
            await self.__load_next_page()

    async def __load_next_page(self):
        self.__last_response = UserPostsFilter(await self.api.fetch_my_feeds(self.__next_page_request))

        if self.__last_response.hasAweme:
            await self.__process_success_response()
        else:
            await self.__process_failed_response()

    @property
    def __next_page_request(self) -> MyFeedRequest:
        cursor = self.__last_response.cursor if self.__last_response else 0
        level = self.__last_response.level if self.__last_response else 1
        self.__last_request = MyFeedRequest(cursor=cursor, level=level)
        return self.__last_request

    async def __process_success_response(self):
        self.__last_retry = 0
        self.__last_success_response = self.__last_response
        self.__load_complete = not self.__last_response.hasMore

        if self.recipient:
            self.__can_continue = self.recipient.on_post_list(self.__last_response)

    @property
    def __can_retry(self):
        return self.__last_retry < 3

    async def __process_failed_response(self):
        if not self.__can_retry:
            self.__can_continue = False
            self.__load_complete = True
            self.__has_error = True
            return
        self.__last_retry += 1

class MyFeedSpider:

    error_count = 0
    async def __sync_all_accounts(self):
        account_id, cookie = get_account_id_and_cookie('FEED1')
        my_feed = MyFeed(IFeedPostRecipient(), cookie)
        try:
            await my_feed.load_full_list()
            self.error_count = 0
        except Exception as e:
            self.error_count += 1
            print(e)

    async def sync_forever(self):
        while True:
            start_time = time.time()
            await self.__sync_all_accounts()
            if self.error_count > 10:
                print('Too many errors, exiting')
                break
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")
            sleep_time = max(1800 - execution_time, 0)
            await asyncio.sleep(sleep_time)

class TestMyFeedPrivateApi(IsolatedAsyncioTestCase):

    async def test_request(self):
        # account_id, cookie = get_account_id_and_cookie('FEED1')
        # my_feed = MyFeed(IFeedPostRecipient(), cookie)
        my_feed = MyFeed(IFeedPostRecipient())
        await my_feed.load_full_list()
        breakpoint()

    async def test_sync_forever(self):
        spider = MyFeedSpider()
        await spider.sync_forever()
