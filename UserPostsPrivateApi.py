import asyncio

from handler import TikTokClient


async def main():
    secUid='MS4wLjABAAAAd5TdNesj9_kJCRkzqSHoP6VP2sw1CvpE4PH_Rbhos-M0kZEy0pBw8lbYm8mrnl7y'
    posts = await TikTokClient().get_user_posts(secUid=secUid)
    breakpoint()

if __name__ == '__main__':
    asyncio.run(main())