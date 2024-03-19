import asyncio

from f2.apps.tiktok.handler2 import TiktokHandler2


async def main():
    for i in range(10):
        # secUid = 'MS4wLjABAAAAMUO3QAXA8dzE8GiaYn3RtvPGkqLVYG6bWnQkgF93Wdz8SWRlR4n77UuZWmaTn_fq'
        secUid='MS4wLjABAAAAQhcYf_TjRKUku-aF8oqngAfzrYksgGLRz8CKMciBFdfR54HQu3qGs-WoJ-KO7hO8'
        data = await TiktokHandler2().get_user_posts(secUid, 0)
        print(bool(data.aweme_id))

if __name__ == "__main__":
    asyncio.run(main())
