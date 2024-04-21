import asyncio

from FollowingPrivateApi import FollowListCandidates, FollowingList


async def main():
    while True:
        private_user_id = await FollowListCandidates.get_next()
        # private_user_id='MS4wLjABAAAAKzPWbM2BSR0YsEE4-fsEnoR5mIk7CBh-Nd6v4JfQyAyjKPx_oSxRfESqsG7468Tl'
        following_list = FollowingList(private_user_id)
        await following_list.load_full_list()

if __name__ == '__main__':
    asyncio.run(main())
