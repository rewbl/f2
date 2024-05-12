# path: f2/apps/tiktok/filter.py

from typing import List, Dict

from crawler import JSONModel
from utils import timestamp_2_str, replaceT


class UserSummaryFilter(JSONModel):
    @property
    def diggCount(self):
        return self._get_attr_value("$.diggCount")

    @property
    def followerCount(self):
        return self._get_attr_value("$.followerCount")

    @property
    def followingCount(self):
        return self._get_attr_value("$.followingCount")

    @property
    def friendCount(self):
        return self._get_attr_value("$.friendCount")

    @property
    def heart(self):
        return self._get_attr_value("$.heart")

    @property
    def heartCount(self):
        return self._get_attr_value("$.heartCount")

    @property
    def videoCount(self):
        return self._get_attr_value("$.videoCount")

    @property
    def avatarLarger(self):
        return self._get_attr_value("$.avatarLarger")

    @property
    def avatarMedium(self):
        return self._get_attr_value("$.avatarMedium")

    @property
    def avatarThumb(self):
        return self._get_attr_value("$.avatarThumb")

    @property
    def commentSetting(self):
        return self._get_attr_value("$.commentSetting")

    @property
    def downloadSetting(self):
        return self._get_attr_value("$.downloadSetting")

    @property
    def duetSetting(self):
        return self._get_attr_value("$.duetSetting")

    @property
    def ftc(self):
        return self._get_attr_value("$.ftc")

    @property
    def id(self):
        return self._get_attr_value("$.id")

    @property
    def isADVirtual(self):
        return self._get_attr_value("$.isADVirtual")

    @property
    def nickname(self):
        return replaceT(self._get_attr_value("$.nickname"))

    @property
    def openFavorite(self):
        return self._get_attr_value("$.openFavorite")

    @property
    def privateAccount(self):
        return self._get_attr_value("$.privateAccount")

    @property
    def relation(self):
        return self._get_attr_value("$.relation")

    @property
    def secUid(self):
        return self._get_attr_value("$.secUid")

    @property
    def secret(self):
        return self._get_attr_value("$.secret")

    @property
    def signature(self):
        return replaceT(self._get_attr_value("$.signature"))

    @property
    def stitchSetting(self):
        return self._get_attr_value("$.stitchSetting")

    @property
    def ttSeller(self):
        return self._get_attr_value("$.ttSeller")

    @property
    def uniqueId(self):
        return self._get_attr_value("$.uniqueId")

    @property
    def verified(self):
        return self._get_attr_value("$.verified")

    def _to_dict(self) -> dict:
        return {
            prop_name: getattr(self, prop_name)
            for prop_name in dir(self)
            if not prop_name.startswith("__") and not prop_name.startswith("_")
        }


class UserFollowingFilter(JSONModel):

    def __init__(self, data):
        self.__userList = None
        super().__init__(data)

    @property
    def hasMore(self) -> bool:
        return self._get_attr_value("$.hasMore")

    @property
    def maxCursor(self):
        return self._get_attr_value("$.maxCursor")

    @property
    def minCursor(self):
        return self._get_attr_value("$.minCursor")

    @property
    def total(self):
        return self._get_attr_value("$.total")

    @property
    def statusCode(self):
        return self._get_attr_value("$.statusCode")

    @property
    def userList(self) -> List[UserSummaryFilter]:
        if self.__userList is None:
            self.__userList = [UserSummaryFilter({**u['stats'], **u['user']}) for u in
                               self._get_attr_value("$.userList") or []]
        return self.__userList

    @property
    def is_list_invisible(self) -> bool:
        return self.statusCode in [10222, 10101]


class UserProfileFilter(JSONModel):
    @property
    def api_status_code(self):
        return self._get_attr_value("$.statusCode")

    # stats
    @property
    def diggCount(self):
        return self._get_attr_value("$.userInfo.stats.diggCount")

    @property
    def followerCount(self):
        return self._get_attr_value("$.userInfo.stats.followerCount")

    @property
    def followingCount(self):
        return self._get_attr_value("$.userInfo.stats.followingCount")

    @property
    def friendCount(self):
        return self._get_attr_value("$.userInfo.stats.friendCount")

    @property
    def heartCount(self):
        return self._get_attr_value("$.userInfo.stats.heartCount")

    @property
    def videoCount(self):
        return self._get_attr_value("$.userInfo.stats.videoCount")

    # user
    @property
    def uid(self):
        return self._get_attr_value("$.userInfo.user.id")

    @property
    def nickname(self):
        return replaceT(self._get_attr_value("$.userInfo.user.nickname"))

    @property
    def secUid(self):
        return self._get_attr_value("$.userInfo.user.secUid")

    @property
    def uniqueId(self):
        return self._get_attr_value("$.userInfo.user.uniqueId")

    @property
    def commentSetting(self) -> bool:
        return bool(self._get_attr_value("$.userInfo.user.commentSetting"))

    @property
    def followingVisibility(self) -> bool:
        return bool(self._get_attr_value("$.userInfo.user.followingVisibility"))

    @property
    def openFavorite(self) -> bool:
        return bool(self._get_attr_value("$.userInfo.user.openFavorite"))

    @property
    def privateAccount(self) -> bool:
        return bool(self._get_attr_value("$.userInfo.user.privateAccount"))

    @property
    def showPlayListTab(self) -> bool:
        return bool(self._get_attr_value("$.userInfo.user.profileTab.showPlayListTab"))

    @property
    def relation(self) -> bool:  # follow 1, no follow 0
        return bool(self._get_attr_value("$.userInfo.user.relation"))

    @property
    def signature(self):
        return replaceT(self._get_attr_value("$.userInfo.user.signature"))

    @property
    def ttSeller(self) -> bool:
        return bool(self._get_attr_value("$.userInfo.user.ttSeller"))

    @property
    def verified(self) -> bool:
        return bool(self._get_attr_value("$.userInfo.user.verified"))

    @property
    def avatarLarger(self):
        return self._get_attr_value("$.userInfo.user.avatarLarger")

    @property
    def avatarThumb(self):
        return self._get_attr_value("$.userInfo.user.avatarThumb")

    def _to_dict(self) -> dict:
        return {
            prop_name: getattr(self, prop_name)
            for prop_name in dir(self)
            if not prop_name.startswith("__") and not prop_name.startswith("_")
        }


class UserPostFilter(JSONModel):
    @property
    def author(self) -> Dict:
        return self._get_attr_value("$.author")

    @property
    def awemeId(self):
        return self._get_attr_value("$.id")

    @property
    def createTime(self):
        return self._get_attr_value("$.createTime")

    @property
    def desc(self):
        return replaceT(self._get_attr_value("$.desc"))

    @property
    def collectCount(self):
        return self._get_attr_value("$.statsV2.collectCount")

    @property
    def commentCount(self):
        return self._get_attr_value("$.statsV2.commentCount")

    @property
    def diggCount(self):
        return self._get_attr_value("$.statsV2.diggCount")

    @property
    def playCount(self):
        return self._get_attr_value("$.statsV2.playCount")

    @property
    def shareCount(self):
        return self._get_attr_value("$.statsV2.shareCount")

    @property
    def music(self):
        return self._get_attr_value("$.music")

    @property
    def videoCover(self):
        return self._get_attr_value("$.video.cover")

    @property
    def videoRatio(self):
        return self._get_attr_value("$.video.ratio")

    @property
    def videoHeight(self):
        return self._get_attr_value("$.video.height")

    @property
    def videoWidth(self):
        return self._get_attr_value("$.video.width")

    def _to_dict(self) -> dict:
        return {
            prop_name: getattr(self, prop_name)
            for prop_name in dir(self)
            if not prop_name.startswith("__") and not prop_name.startswith("_")
        }


class UserPostsFilter(JSONModel):
    @property
    def hasAweme(self) -> bool:
        return bool(self._get_attr_value("$.itemList"))

    @property
    def hasMore(self) -> bool:
        return bool(self._get_attr_value("$.hasMore"))

    @property
    def cursor(self):
        return self._get_attr_value("$.cursor")

    @property
    def level(self):
        return self._get_attr_value("$.level")

    @property
    def statusCode(self):
        return self._get_attr_value("$.statusCode")

    @property
    def itemList(self) -> List[UserPostFilter]:
        return [UserPostFilter(item) for item in self._get_attr_value("$.itemList") or []]

    def _to_dict(self) -> dict:
        return {
            prop_name: getattr(self, prop_name)
            for prop_name in dir(self)
            if not prop_name.startswith("__") and not prop_name.startswith("_")
        }


class UserCollectFilter(UserPostsFilter):
    def __init__(self, data):
        super().__init__(data)


class UserMixFilter(UserPostsFilter):
    def __init__(self, data):
        super().__init__(data)


class UserLikeFilter(UserPostsFilter):
    def __init__(self, data):
        super().__init__(data)


class UserPlayListFilter(JSONModel):
    @property
    def api_status_code(self):
        return self._get_attr_value("$.statusCode")

    @property
    def hasPlayList(self) -> bool:
        return bool(self._get_attr_value("$.playList"))

    @property
    def hasMore(self) -> bool:
        return bool(self._get_attr_value("$.hasMore"))

    @property
    def mixId(self):
        return self._get_attr_value("$.playList[*].mixId")

    @property
    def mixName(self):
        return self._get_attr_value("$.playList[*].mixName")

    @property
    def videoCount(self):
        return self._get_attr_value("$.playList[*].videoCount")

    def _to_dict(self) -> dict:
        return {
            prop_name: getattr(self, prop_name)
            for prop_name in dir(self)
            if not prop_name.startswith("__") and not prop_name.startswith("_")
        }


class PostDetailFilter(JSONModel):
    @property
    def api_status_code(self):
        return self._get_attr_value("$.statusCode")

    # author
    @property
    def author_avatarLarger(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.avatarLarger")

    @property
    def commentSetting(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.commentSetting")

    @property
    def downloadSetting(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.downloadSetting")

    @property
    def uid(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.id")

    @property
    def nickname(self):
        return replaceT(self._get_attr_value("$.itemInfo.itemStruct.author.nickname"))

    @property
    def secUid(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.secUid")

    @property
    def uniqueId(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.uniqueId")

    @property
    def signature(self):
        return replaceT(self._get_attr_value("$.itemInfo.itemStruct.author.signature"))

    @property
    def openFavorite(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.openFavorite")

    @property
    def privateAccount(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.privateAccount")

    @property
    def verified(self):
        return self._get_attr_value("$.itemInfo.itemStruct.author.verified")

    # challenges
    @property
    def challenges_title(self):
        return self._get_attr_value("$.itemInfo.itemStruct.challenges[*].title")

    @property
    def challenges_desc(self):
        return self._get_attr_value("$.itemInfo.itemStruct.challenges[*].desc")

    # aweme
    @property
    def createTime(self):
        return timestamp_2_str(
            str(self._get_attr_value("$.itemInfo.itemStruct.createTime"))
        )

    @property
    def desc(self):
        return replaceT(self._get_attr_value("$.itemInfo.itemStruct.desc"))

    @property
    def textExtra(self):
        return self._get_attr_value("$.itemInfo.itemStruct.textExtra")

    @property
    def aweme_id(self):
        return self._get_attr_value("$.itemInfo.itemStruct.id")

    # aweme stats
    @property
    def collected(self) -> bool:
        return bool(self._get_attr_value("$.itemInfo.itemStruct.collected"))

    @property
    def digged(self) -> bool:
        return bool(self._get_attr_value("$.itemInfo.itemStruct.digged"))

    @property
    def forFriend(self) -> bool:
        return bool(self._get_attr_value("$.itemInfo.itemStruct.forFriend"))

    @property
    def itemCommentStatus(self) -> bool:
        return bool(self._get_attr_value("$.itemInfo.itemStruct.itemCommentStatus"))

    @property
    def privateItem(self) -> bool:
        return bool(self._get_attr_value("$.itemInfo.itemStruct.privateItem"))

    @property
    def secret(self) -> bool:
        return bool(self._get_attr_value("$.itemInfo.itemStruct.secret"))

    @property
    def shareEnabled(self) -> bool:
        return bool(self._get_attr_value("$.itemInfo.itemStruct.shareEnabled"))

    # stats
    @property
    def commentCount(self):
        return self._get_attr_value("$.itemInfo.itemStruct.stats.commentCount")

    @property
    def diggCount(self):
        return self._get_attr_value("$.itemInfo.itemStruct.stats.diggCount")

    @property
    def playCount(self):
        return self._get_attr_value("$.itemInfo.itemStruct.stats.playCount")

    @property
    def shareCount(self):
        return self._get_attr_value("$.itemInfo.itemStruct.stats.shareCount")

    # suggestedWords
    @property
    def suggestedWords(self):
        return self._get_attr_value("$.itemInfo.itemStruct.suggestedWords")

    @property
    def videoSuggestWordsList(self):
        return self._get_attr_value(
            "$.itemInfo.itemStruct.videoSuggestWordsList.video_suggest_words_struct"
        )

    # music
    @property
    def music_authorName(self):
        return replaceT(self._get_attr_value("$.itemInfo.itemStruct.music.authorName"))

    @property
    def music_coverLarge(self):
        return self._get_attr_value("$.itemInfo.itemStruct.music.coverLarge")

    @property
    def music_duration(self):
        return self._get_attr_value("$.itemInfo.itemStruct.music.duration")

    @property
    def music_id(self):
        return self._get_attr_value("$.itemInfo.itemStruct.music.id")

    @property
    def music_original(self):
        return self._get_attr_value("$.itemInfo.itemStruct.music.original")

    @property
    def music_playUrl(self):
        return self._get_attr_value("$.itemInfo.itemStruct.music.playUrl")

    @property
    def music_title(self):
        return replaceT(self._get_attr_value("$.itemInfo.itemStruct.music.title"))

    # video
    @property
    def video_bitrate(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.bitrate")

    @property
    def video_bitrateInfo(self):
        bit_rate_data = self._get_attr_value("$.itemInfo.itemStruct.video.bitrateInfo")
        if bit_rate_data is None:
            return []  # 或者根据实际需求返回其他默认值
        return [item["Bitrate"] for item in bit_rate_data]

    @property
    def video_codecType(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.codecType")

    @property
    def video_cover(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.cover")

    @property
    def video_dynamicCover(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.dynamicCover")

    @property
    def video_playAddr(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.playAddr")

    @property
    def video_definition(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.definition")

    @property
    def video_duration(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.duration")

    @property
    def video_height(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.height")

    @property
    def video_width(self):
        return self._get_attr_value("$.itemInfo.itemStruct.video.width")

    def _to_dict(self) -> dict:
        return {
            prop_name: getattr(self, prop_name)
            for prop_name in dir(self)
            if not prop_name.startswith("__") and not prop_name.startswith("_")
        }

    def _to_list(self):
        exclude_list = []
        keys = [
            prop_name
            for prop_name in dir(self)
            if not prop_name.startswith("__")
               and not prop_name.startswith("_")
               and prop_name not in exclude_list
        ]
        aweme_entries = self._get_attr_value("$.itemInfo.itemStruct") or []
        list_dicts = []

        for entry in aweme_entries:
            d = {}
            for key in keys:
                attr_values = getattr(self, key, [])
                index = aweme_entries.index(entry)
                d[key] = attr_values[index] if index < len(attr_values) else None
            list_dicts.append(d)
        return list_dicts
