import asyncio
import time
from pprint import pprint
from typing import List, Dict
from unittest import IsolatedAsyncioTestCase

from StudioY.StudioYClient import StudioYClient, StudioYMapper
from crawler import TiktokCrawler
from filter import UserPostsFilter
from model import UserPostRequest


class IUserPostRecipient:
    def on_post_list(self, posts: UserPostsFilter) -> bool:
        res = StudioYClient().sync_user_videos(posts.itemList)
        pprint(res)
        return bool(res and res.get('isSuccess'))


class AwemeCollection:
    __last_request: UserPostRequest | None
    __last_response: UserPostsFilter | None
    __last_success_response: UserPostsFilter | None
    __can_continue: bool
    __load_complete: bool

    def __init__(self, sec_uid: str, recipient: IUserPostRecipient = None):
        self.recipient = recipient
        self.api = TiktokCrawler()
        self.sec_uid = sec_uid
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
        self.__last_response = UserPostsFilter(await self.api.fetch_user_posts(self.__next_page_request))

        if self.__last_response.hasAweme:
            await self.__process_success_response()
        else:
            await self.__process_failed_response()

    @property
    def __next_page_request(self) -> UserPostRequest:
        cursor = self.__last_response.cursor if self.__last_response else 0
        self.__last_request = UserPostRequest(secUid=self.sec_uid, cursor=cursor)
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

class AwemeCollectionSpider:

    error_count = 0
    async def __sync_all_accounts(self):
        accs = StudioYClient().get_all_sec_uids()
        for sec_uid in accs:
            print(f'\r\n{sec_uid}')
            collection = AwemeCollection(sec_uid, IUserPostRecipient())
            try:
                await collection.load_full_list()
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
            sleep_time = max(900 - execution_time, 0)
            await asyncio.sleep(sleep_time)

class TestAwemeCollectionPrivateApi(IsolatedAsyncioTestCase):

    async def test_request(self):
        collection = AwemeCollection('MS4wLjABAAAAMUO3QAXA8dzE8GiaYn3RtvPGkqLVYG6bWnQkgF93Wdz8SWRlR4n77UuZWmaTn_fq',
                                     IUserPostRecipient())
        await collection.load_full_list()
        breakpoint()


    async def test_sync_forever(self):
        spider = AwemeCollectionSpider()
        await spider.sync_forever()
