import asyncio

from f2.apps.tiktok.handler2 import TiktokHandler2


async def main():
    secUid = (
        "MS4wLjABAAAAMUO3QAXA8dzE8GiaYn3RtvPGkqLVYG6bWnQkgF93Wdz8SWRlR4n77UuZWmaTn_fq"
    )
    uniqueId = "saritacharrer.s"
    profile = await TiktokHandler2().handler_user_profile(secUid=secUid)
    profle2 = await TiktokHandler2().handler_user_profile(uniqueId=uniqueId)
    assert profile and profle2
    assert profile.uid
    assert profile.uid == profle2.uid


if __name__ == "__main__":
    asyncio.run(main())
