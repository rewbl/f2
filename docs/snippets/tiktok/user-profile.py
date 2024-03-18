import asyncio

from f2.apps.tiktok.handler2 import TiktokHandler2

kwargs = {
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Referer": "https://www.tiktok.com/",
    },
    "proxies": {"http": None, "https": None},
    "cookie": "YOUR_COOKIE_HERE",
}


async def main():
    secUid = (
        "MS4wLjABAAAAMUO3QAXA8dzE8GiaYn3RtvPGkqLVYG6bWnQkgF93Wdz8SWRlR4n77UuZWmaTn_fq"
    )
    uniqueId = "saritacharrer.s"
    profile = await TiktokHandler2(kwargs).handler_user_profile(secUid=secUid)
    profle2 = await TiktokHandler2(kwargs).handler_user_profile(uniqueId=uniqueId)
    assert profile.uid == profle2.uid


if __name__ == "__main__":
    asyncio.run(main())
