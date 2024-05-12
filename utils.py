# path: f2/apps/tiktok/utils.py
import datetime
import hashlib
import random
import re
import secrets
import time
from typing import Union, Any
from unittest.mock import Mock

from motor import motor_asyncio

logger = Mock()


def _(msg):
    return msg


class XBogus:
    def __init__(self) -> None:

        self.Array = [
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, 10, 11, 12, 13, 14, 15
        ]
        self.character = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="

    def md5_str_to_array(self, md5_str):
        """
        将字符串使用md5哈希算法转换为整数数组。
        Convert a string to an array of integers using the md5 hashing algorithm.
        """
        if isinstance(md5_str, str) and len(md5_str) > 32:
            return [ord(char) for char in md5_str]
        else:
            array = []
            idx = 0
            while idx < len(md5_str):
                array.append((self.Array[ord(md5_str[idx])] << 4) | self.Array[ord(md5_str[idx + 1])])
                idx += 2
            return array

    def md5_encrypt(self, url_path):
        """
        使用多轮md5哈希算法对URL路径进行加密。
        Encrypt the URL path using multiple rounds of md5 hashing.
        """
        hashed_url_path = self.md5_str_to_array(self.md5(self.md5_str_to_array(self.md5(url_path))))
        return hashed_url_path

    def md5(self, input_data):
        """
        计算输入数据的md5哈希值。
        Calculate the md5 hash value of the input data.
        """
        if isinstance(input_data, str):
            array = self.md5_str_to_array(input_data)
        elif isinstance(input_data, list):
            array = input_data
        else:
            raise ValueError("Invalid input type. Expected str or list.")

        md5_hash = hashlib.md5()
        md5_hash.update(bytes(array))
        return md5_hash.hexdigest()

    def encoding_conversion(self, a, b, c, e, d, t, f, r, n, o, i, _, x, u, s, l, v, h, p):
        """
        第一次编码转换。
        Perform encoding conversion.
        """
        y = [a]
        y.append(int(i))
        y.extend([b, _, c, x, e, u, d, s, t, l, f, v, r, h, n, p, o])
        re = bytes(y).decode('ISO-8859-1')
        return re

    def encoding_conversion2(self, a, b, c):
        """
        第二次编码转换。
        Perform an encoding conversion on the given input values and return the result.
        """
        return chr(a) + chr(b) + c

    def rc4_encrypt(self, key, data):
        """
        使用RC4算法对数据进行加密。
        Encrypt data using the RC4 algorithm.
        """
        S = list(range(256))
        j = 0
        encrypted_data = bytearray()

        # 初始化 S 盒
        # Initialize the S box
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        # 生成密文
        # Generate the ciphertext
        i = j = 0
        for byte in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            encrypted_byte = byte ^ S[(S[i] + S[j]) % 256]
            encrypted_data.append(encrypted_byte)

        return encrypted_data

    def calculation(self, a1, a2, a3):
        """
        对给定的输入值执行位运算计算，并返回结果。
        Perform a calculation using bitwise operations on the given input values and return the result.
        """
        x1 = (a1 & 255) << 16
        x2 = (a2 & 255) << 8
        x3 = x1 | x2 | a3
        return self.character[(x3 & 16515072) >> 18] + self.character[(x3 & 258048) >> 12] + self.character[
            (x3 & 4032) >> 6] + self.character[
            x3 & 63]

    def getXBogus(self, url_path):
        """
        获取 X-Bogus 值。
        Get the X-Bogus value.
        """
        array1 = self.md5_str_to_array("d88201c9344707acde7261b158656c0e")
        array2 = self.md5_str_to_array(
            self.md5(self.md5_str_to_array("d41d8cd98f00b204e9800998ecf8427e")))
        url_path_array = self.md5_encrypt(url_path)

        timer = int(time.time())
        ct = 536919696
        array3 = []
        array4 = []
        xb_ = ""

        new_array = [
            64, 0.00390625, 1, 8,
            url_path_array[14], url_path_array[15], array2[14], array2[15], array1[14], array1[15],
            timer >> 24 & 255, timer >> 16 & 255, timer >> 8 & 255, timer & 255,
            ct >> 24 & 255, ct >> 16 & 255, ct >> 8 & 255, ct & 255
        ]

        xor_result = new_array[0]
        for i in range(1, len(new_array)):
            # a = xor_result
            b = new_array[i]
            if isinstance(b, float):
                b = int(b)
            xor_result ^= b

        new_array.append(xor_result)

        idx = 0
        while idx < len(new_array):
            array3.append(new_array[idx])
            try:
                array4.append(new_array[idx + 1])
            except IndexError:
                pass
            idx += 2

        merge_array = array3 + array4

        garbled_code = self.encoding_conversion2(
            2, 255, self.rc4_encrypt("ÿ".encode('ISO-8859-1'),
                                     self.encoding_conversion(*merge_array).encode('ISO-8859-1')).decode('ISO-8859-1'))

        idx = 0
        while idx < len(garbled_code):
            xb_ += self.calculation(ord(garbled_code[idx]), ord(
                garbled_code[idx + 1]), ord(garbled_code[idx + 2]))
            idx += 3
        self.params = '%s&X-Bogus=%s' % (url_path, xb_)
        self.xb = xb_
        return (self.params, self.xb)


XB = XBogus



class XBogusManager:
    @classmethod
    def str_2_endpoint(cls, endpoint: str) -> str:
        try:
            final_endpoint = XB().getXBogus(endpoint)
        except Exception as e:
            raise RuntimeError(_("生成X-Bogus失败: {0})").format(e))

        return final_endpoint[0]

    @classmethod
    def model_2_endpoint(cls, base_endpoint: str, params: dict) -> str:
        # 检查params是否是一个字典 (Check if params is a dict)
        if not isinstance(params, dict):
            raise TypeError(_("参数必须是字典类型"))

        param_str = "&".join([f"{k}={v}" for k, v in params.items()])

        try:
            xb_value = XB().getXBogus(param_str)
        except Exception as e:
            raise RuntimeError(_("生成X-Bogus失败: {0})").format(e))

        # 检查base_endpoint是否已有查询参数 (Check if base_endpoint already has query parameters)
        separator = "&" if "?" in base_endpoint else "?"

        final_endpoint = f"{base_endpoint}{separator}{param_str}&X-Bogus={xb_value[1]}"

        return final_endpoint


def get_timestamp(unit: str = "milli"):
    now = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
    if unit == "milli":
        return int(now.total_seconds() * 1000)
    elif unit == "sec":
        return int(now.total_seconds())
    elif unit == "min":
        return int(now.total_seconds() / 60)
    else:
        raise ValueError("Unsupported time unit")


seed_bytes = secrets.token_bytes(16)
seed_int = int.from_bytes(seed_bytes, "big")


def gen_random_str(randomlength: int) -> str:
    base_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-"
    return "".join(random.choice(base_str) for _ in range(randomlength))


def timestamp_2_str(
        timestamp: Union[str, int, float], format: str = "%Y-%m-%d %H-%M-%S"
) -> str:
    if timestamp is None or timestamp == "None":
        return ""

    return datetime.datetime.fromtimestamp(float(timestamp)).strftime(format)




def replaceT(obj: Union[str, Any]) -> Union[str, Any]:
    reSub = r"[^\u4e00-\u9fa5a-zA-Z0-9#]"

    if isinstance(obj, list):
        return [re.sub(reSub, "_", i) for i in obj]

    if isinstance(obj, str):
        return re.sub(reSub, "_", obj)

    # raise TypeError("输入应为字符串或字符串列表")


class TiktokAPIEndpoints:
    """
    API Endpoints for TikTok
    """

    # 抖音域名 (Tiktok Domain)
    TIKTOK_DOMAIN = "https://www.tiktok.com"

    # 直播域名 (Webcast Domain)
    WEBCAST_DOMAIN = "https://webcast.tiktok.com"

    # 登录 (Login)
    LOGIN_ENDPOINT = f"{TIKTOK_DOMAIN}/login/"

    # 首页推荐 (Home Recommend)
    HOME_RECOMMEND = f"{TIKTOK_DOMAIN}/api/recommend/item_list/"

    # 用户详细信息 (User Detail Info)
    USER_DETAIL = f"{TIKTOK_DOMAIN}/api/user/detail/"

    # 用户作品 (User Post)
    USER_POST = f"{TIKTOK_DOMAIN}/api/post/item_list/"

    USER_FEED = f"{TIKTOK_DOMAIN}/api/following/item_list/"

    # 用户点赞 (User Like)
    USER_LIKE = f"{TIKTOK_DOMAIN}/api/favorite/item_list/"

    # 用户收藏 (User Collect)
    USER_COLLECT = f"{TIKTOK_DOMAIN}/api/user/collect/item_list/"

    # 用户播放列表 (User Play List)
    USER_PLAY_LIST = f"{TIKTOK_DOMAIN}/api/user/playlist/"

    # 用户合辑 (User Mix)
    USER_MIX = f"{TIKTOK_DOMAIN}/api/mix/item_list/"

    # 猜你喜欢 (Guess You Like)
    GUESS_YOU_LIKE = f"{TIKTOK_DOMAIN}/api/related/item_list/"

    # 用户关注 (User Follow)
    # USER_FOLLOW = f"{TIKTOK_DOMAIN}/api/relation/user/list/"

    # 用户粉丝 (User Fans)
    # USER_FANS = f"{TIKTOK_DOMAIN}/api/relation/follower/list/"

    # 作品信息 (Post Detail)
    AWEME_DETAIL = f"{TIKTOK_DOMAIN}/api/item/detail/"

    # 作品评论 (Post Comment)
    POST_COMMENT = f"{TIKTOK_DOMAIN}/api/comment/list/"

    USER_FOLLOWING = f"{TIKTOK_DOMAIN}/api/user/list/"


class TikTokMongoDb:
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(
            'mongodb://app:Supers8*@192.168.196.83:27018,192.168.196.98:27018,192.168.196.85:27018,192.168.196.86:27018,192.168.196.87:27018/?replicaSet=tiktok')
        self.db = self.client['tiktok']
        self.following_lists = self.db['following_lists']
        self.following_relations = self.db['following_relations']
        self.tiktok_users = self.db['tiktok_users']
        self.tiktok_follow_list_candidates = self.db['tiktok_users_follow_no_lists_view']
        self.tiktok_follow_view = self.db['tiktok_users_follow_view']


TikTokDb = TikTokMongoDb()
