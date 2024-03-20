import asyncio
from pprint import pprint

from StudioY.StudioYClient import StudioYClient
from filter import UserProfileFilter
from handler import TikTokClient
from pydantic import BaseModel
from typing import Optional


class TikTokUserDto(BaseModel):
    Id: str = '00000000-0000-0000-0000-000000000000'
    SecUid: str
    Uid: str
    AvatarUrl: Optional[str] = None
    AvatarThumbUrl: Optional[str] = None
    Nickname: Optional[str] = None
    VideoCount: Optional[int] = None
    FollowerCount: Optional[int] = None
    FollowingCount: Optional[int] = None
    HeartCount: Optional[int] = None
    Signature: Optional[str] = None
    UniqueId: Optional[str] = None

    @staticmethod
    def from_user_profile_filter(user: UserProfileFilter) -> 'TikTokUserDto':
        return TikTokUserDto(
            SecUid=user.secUid,
            Uid=user.uid,
            AvatarUrl=user.avatarLarger,
            AvatarThumbUrl=user.avatarThumb,
            Nickname=user.nickname,
            VideoCount=user.videoCount,
            FollowerCount=user.followerCount,
            FollowingCount=user.followingCount,
            HeartCount=user.heartCount,
            Signature=user.signature,
            UniqueId=user.uniqueId
        )


accs =[
    ('Girls-5', 'annelle.astafan'),
]



async def main():
    for acc in accs:
        await process_one(*acc)


async def process_one(shortCode, username):
    user = TikTokUserDto.from_user_profile_filter(await TikTokClient().handler_user_profile(uniqueId=username))
    json = user.dict()
    result = StudioYClient().link_account(shortCode.upper(), json)

    assert result['isSuccess']
    assert result['data']['tikTokUser']['secUid'] == json['SecUid']
    pprint(result)


if __name__ == '__main__':
    asyncio.run(main())
