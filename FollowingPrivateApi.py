import asyncio
import time
from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import UpdateOne

from conf_manager import TikTokDb
from crawler import TiktokCrawler
from filter import UserFollowingFilter
from model import UserFollowing


class NewFollowingRelations:
    def __init__(self, follower_sec_user_id, following_sec_user_id_list, update_time, min_cursor, max_cursor):
        self.follower_sec_user_id = follower_sec_user_id
        self.following_sec_user_id_list = following_sec_user_id_list
        self.update_time = update_time
        self.min_cursor = min_cursor
        self.max_cursor = max_cursor

    async def save(self):
        collection: AsyncIOMotorCollection = TikTokDb.following_relations
        operations = []
        for following_sec_user_id in self.following_sec_user_id_list:
            document = {
                '_id': {'follower': self.follower_sec_user_id, 'following': following_sec_user_id},
                'update_time': self.update_time,
                'min_cursor': self.min_cursor,
                'max_cursor': self.max_cursor
            }
            operations.append(UpdateOne(
                {'_id': {'follower': self.follower_sec_user_id, 'following': following_sec_user_id}},
                {'$set': document},
                upsert=True
            ))
        await collection.bulk_write(operations)


class NewUserList:
    def __init__(self, user_list):
        self.user_list: List[dict] = user_list or []

    async def save(self):
        collection: AsyncIOMotorCollection = TikTokDb.tiktok_users
        operations = []
        for user in self.user_list:
            user['_update_time'] = int(time.time())
            operations.append(UpdateOne(
                {'_id': user['secUid']},
                {'$set': user},
                upsert=True
            ))
        await collection.bulk_write(operations)


class FollowListCandidates:
    @staticmethod
    async def get_next():
        # Check the following_lists collection first
        following_lists_collection = TikTokDb.following_lists
        document = await following_lists_collection.find_one({"load_complete": False})
        if document is not None:
            return document['_id']

        # If no document was found in following_lists, check the douyin_follow_list_candidates collection
        candidates_collection = TikTokDb.tiktok_follow_list_candidates
        query = {
            "aweme_count": {"$gt": 100},
            "total_favorited": {"$gt": 100 * 1000},
            "follower_count": {"$gt": 1000 * 1000},
            "following_count": {"$gte": 500, "$lte": 5000}  # updated this line
        }
        documents = await candidates_collection.find(query).sort("following_count", -1).limit(1).to_list(None)
        if documents:
            return documents[0]['_id']
        else:
            return None


class FollowingList:
    sec_user_id: str | None
    start_time: int | None
    end_time: int | None

    start_total: int | None
    end_total: int | None

    last_total: int | None
    next_max_cursor: int | None
    next_max_cursor: int | None

    __last_request: UserFollowing
    __last_response: UserFollowingFilter
    __last_success_response: UserFollowingFilter

    __can_continue: bool
    __load_complete: bool

    def __init__(self, sec_user_id: str):
        self.api = TiktokCrawler()
        self.sec_user_id = sec_user_id
        self.start_time = None
        self.end_time = None
        self.start_total = None
        self.end_total = None
        self.last_total = None
        self.next_max_cursor = None
        self.next_min_cursor = None
        self.__last_request = None
        self.__last_response = None
        self.__last_success_response = None
        self.__load_complete = False
        self.__can_continue = True
        self.__last_retry = 0
        self.__has_error = False

    async def __recover_status(self):
        status_document = await TikTokDb.following_lists.find_one({'_id': self.sec_user_id})
        if status_document is None:
            return
        self.start_time = status_document.get('start_time')
        self.end_time = status_document.get('end_time')
        self.start_total = status_document.get('start_total')
        self.end_total = status_document.get('end_total')
        self.last_total = status_document.get('last_total')
        self.next_min_cursor = status_document.get('next_min_cursor')
        self.next_max_cursor = status_document.get('next_max_cursor')
        self.__can_continue = status_document.get('can_continue')
        self.__load_complete = status_document.get('load_complete')
        self.__last_retry = status_document.get('last_retry')
        self.__has_error = status_document.get('has_error')

    async def load_full_list(self):
        await self.__recover_status()
        if not self.start_time:
            self.start_time = int(time.time())

        while self.__can_continue and not self.__load_complete:
            await self.__load_next_page()

    async def __load_next_page(self):
        start_time = time.time()
        self.__last_response = UserFollowingFilter(await self.api.fetch_user_following(self.__next_page_request))
        ms = (time.time() - start_time) * 1000
        print(f"Load Time: {ms}ms")

        if self.__last_response.userList:
            start_time = time.time()
            await self.__process_success_response()
            ms = (time.time() - start_time) * 1000
            print(f"Process Time: {ms}ms")
        else:
            await self.__process_failed_response()

    @property
    def __next_page_request(self) -> UserFollowing:
        min_cursor = self.next_min_cursor if self.next_min_cursor else 0
        max_cursor = int(time.time()) if not self.next_max_cursor else self.next_max_cursor
        self.__last_request = UserFollowing(
            secUid=self.sec_user_id,
            minCursor=min_cursor,
            maxCursor=max_cursor
        )
        return self.__last_request

    async def __process_success_response(self):
        self.__last_retry = 0
        self.__last_success_response = self.__last_response

        await self.__save_followings_users()
        await self.__save_following_relations()
        self.__update_list_status_after_success()
        await self.__save_current_status()
        print(len(self.__last_success_response.userList))

    async def __save_followings_users(self):
        await NewUserList([u._to_dict() for u in self.__last_success_response.userList]).save()

    async def __save_following_relations(self):
        follower_sec_id_list = [f.secUid for f in self.__last_success_response.userList]
        await NewFollowingRelations(self.sec_user_id,
                                    follower_sec_id_list,
                                    int(time.time()),
                                    self.__last_request.minCursor,
                                    self.__last_request.maxCursor) \
            .save()

    def __update_list_status_after_success(self):
        if not self.start_total:
            self.start_total = self.__last_success_response.total
        self.last_total = self.__last_success_response.total
        self.next_min_cursor = self.__last_success_response.minCursor
        self.next_max_cursor = self.__last_success_response.maxCursor
        if self.__last_success_response.hasMore:
            return

        self.__load_complete = True
        self.end_total = self.__last_success_response.total

    async def __save_current_status(self):
        update_filter = {'_id': self.sec_user_id}
        update = {'$set':
            {
                'start_time': self.start_time,
                'end_time': int(time.time()),
                'start_total': self.start_total,
                'end_total': self.end_total,
                'last_total': self.last_total,
                'next_min_cursor': self.next_min_cursor,
                'next_max_cursor': self.next_max_cursor,
                'can_continue': self.__can_continue,
                'load_complete': self.__load_complete,
                'last_retry': self.__last_retry,
                'has_error': self.__has_error
            }}

        await TikTokDb.following_lists.update_one(update_filter, update, upsert=True)

    @property
    def __can_retry(self):
        return self.__last_retry < 3

    async def __process_failed_response(self):
        if self.__last_response.is_list_invisible:
            self.end_time = int(time.time())
            self.__load_complete = True
            self.start_total = 0
            self.end_total = 0
            await self.__save_current_status()
            return

        if not self.__can_retry:
            self.__can_continue = False
            self.__load_complete = True
            self.__has_error = True
            await self.__save_current_status()
            # breakpoint()
            return

        self.__last_retry += 1



async def main():
    while True:
        private_user_id = await FollowListCandidates.get_next()
        # private_user_id='MS4wLjABAAAAKzPWbM2BSR0YsEE4-fsEnoR5mIk7CBh-Nd6v4JfQyAyjKPx_oSxRfESqsG7468Tl'
        following_list = FollowingList(private_user_id)
        await following_list.load_full_list()


if __name__ == '__main__':
    asyncio.run(main())
