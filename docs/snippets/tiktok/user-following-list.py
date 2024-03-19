from unittest import IsolatedAsyncioTestCase

from f2.apps.tiktok.handler2 import TiktokHandler2


async def main():
    secUid = 'MS4wLjABAAAAmnirnqYgyT26EZrYFGn4yeVeUqZbjXgOrsH-GvJKGu2qROcHvt_HF-3L6hQ8O-0T'
    data = await TiktokHandler2().get_user_following(secUid)
    breakpoint()
class Test(IsolatedAsyncioTestCase):
    async def test_user_following_list(self):
        await main()
