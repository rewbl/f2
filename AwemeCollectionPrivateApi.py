from typing import List, Dict
from unittest import IsolatedAsyncioTestCase

from crawler import TiktokCrawler
from filter import UserPostsFilter
from model import UserPostRequest


class IUserPostRecipient:
    def on_post_list(self, aweme_list: List[Dict]) -> bool:
        return bool(aweme_list)


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


class TestAwemeCollectionPrivateApi(IsolatedAsyncioTestCase):

    async def test_request(self):
        collection=AwemeCollection('MS4wLjABAAAAf09jdtPRY2fU6z-1DjXCP8HWH1CGiN5RmjXyxouWng3TA-3LtsMlJGGtwLCQNHY7',
                                   IUserPostRecipient())
        await collection.load_full_list()
        breakpoint()
