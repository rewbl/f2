import asyncio
from f2.apps.tiktok.handler import TiktokHandler
from f2.apps.tiktok.handler2 import TiktokHandler2
from f2.apps.tiktok.utils import SecUserIdFetcher


async def main():
    secUid = 'MS4wLjABAAAAMUO3QAXA8dzE8GiaYn3RtvPGkqLVYG6bWnQkgF93Wdz8SWRlR4n77UuZWmaTn_fq'
    data = await TiktokHandler2().get_user_posts(secUid, 0)
    breakpoint()


if __name__ == "__main__":
    asyncio.run(main())
