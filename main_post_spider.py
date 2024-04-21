import asyncio

from AwemeCollectionPrivateApi import AwemeCollectionSpider


async def main():
    spider = AwemeCollectionSpider()
    await spider.sync_forever()

if __name__ == '__main__':
    asyncio.run(main())
