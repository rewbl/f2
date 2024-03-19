# path: f2/apps/tiktok/utils.py
import datetime
import random
import secrets
import sys
from unittest.mock import Mock

import importlib_resources
from conf_manager import ConfigManager

import f2
import re
import json
import httpx
import asyncio

from typing import Union, Any
from pathlib import Path

logger=Mock()
def _(msg):
    return msg

from xbogus import XBogus as XB


class TokenManager:
    f2_manager = ConfigManager(f2.F2_CONFIG_FILE_PATH).get_config("f2").get("tiktok")
    token_conf = f2_manager.get("msToken", None)
    ttwid_conf = f2_manager.get("ttwid", None)
    odin_tt_conf = f2_manager.get("odin_tt", None)
    proxies_conf = f2_manager.get("proxies", None)
    proxies = {
        "http://": proxies_conf.get("http", None),
        "https://": proxies_conf.get("https", None),
    }

    @classmethod
    def gen_real_msToken(cls) -> str:
        """
        生成真实的msToken,当出现错误时返回虚假的值
        (Generate a real msToken and return a false value when an error occurs)
        """

        payload = json.dumps(
            {
                "magic": cls.token_conf["magic"],
                "version": cls.token_conf["version"],
                "dataType": cls.token_conf["dataType"],
                "strData": cls.token_conf["strData"],
                "tspFromClient": get_timestamp(),
            }
        )

        headers = {
            "User-Agent": cls.token_conf["User-Agent"],
            "Content-Type": "application/json",
        }

        transport = httpx.HTTPTransport(retries=5)
        with httpx.Client(transport=transport, proxies=cls.proxies) as client:
            try:
                response = client.post(
                    cls.token_conf["url"], headers=headers, content=payload
                )

                if response.status_code == 401:
                    raise Exception(_("由于某些错误, 无法获取msToken"))
                elif response.status_code == 404:
                    raise Exception(_("无法找到API端点"))

                msToken = str(httpx.Cookies(response.cookies).get("msToken"))

                if len(msToken) not in [148]:
                    raise Exception(
                        _(
                            "msToken: 请检查并更新 f2 中 conf.yaml 配置文件中的 msToken，以匹配 tiktok 新规则。"
                        )
                    )

                return msToken

            except httpx.RequestError:
                # 捕获所有与 httpx 请求相关的异常情况 (Captures all httpx request-related exceptions)
                raise Exception(
                    _(
                        "连接端点失败，检查网络环境或代理：{0} 代理：{1} 类名：{2}"
                    ).format(cls.token_conf["url"], cls.proxies, cls.__name__)
                )

            except httpx.HTTPStatusError as e:
                # 捕获 httpx 的状态代码错误 (captures specific status code errors from httpx)
                raise Exception(
                    f"HTTP Status Code {e.response.status_code}: {e.response.text}"
                )

            except Exception as e:
                # 返回虚假的msToken (Return a fake msToken)
                logger.info(_("生成虚假的msToken"))
                return cls.gen_false_msToken()

    @classmethod
    def gen_false_msToken(cls) -> str:
        """生成随机msToken (Generate random msToken)"""
        return gen_random_str(146) + "=="

    @classmethod
    def gen_ttwid(cls) -> str:
        """
        生成请求必带的ttwid (Generate the essential ttwid for requests)
        """
        transport = httpx.HTTPTransport(retries=5)
        with httpx.Client(transport=transport, proxies=cls.proxies) as client:
            try:
                response = client.post(
                    cls.ttwid_conf["url"],
                    headers={
                        "Cookie": cls.ttwid_conf.get("cookie"),
                        "Content-Type": "text/plain",
                    },
                    content=cls.ttwid_conf["data"],
                )

                if response.status_code == 401:
                    raise Exception(_("401 由于某些错误, 无法获取ttwid"))
                elif response.status_code == 404:
                    raise Exception(_("404 无法找到API端点"))

                ttwid = httpx.Cookies(response.cookies).get("ttwid")

                if ttwid is None:
                    raise Exception(
                        _("ttwid: 检查没有通过, 请更新配置文件中的ttwid")
                    )

                return ttwid

            except httpx.RequestError:
                # 捕获所有与 httpx 请求相关的异常情况 (Captures all httpx request-related exceptions)
                raise Exception(
                    _(
                        "连接端点失败，检查网络环境或代理：{0} 代理：{1} 类名：{2}"
                    ).format(cls.ttwid_conf["url"], cls.proxies, cls.__name__)
                )

            except httpx.HTTPStatusError as e:
                # 捕获 httpx 的状态代码错误 (captures specific status code errors from httpx)
                raise Exception(
                    f"HTTP Status Code {e.response.status_code}: {e.response.text}"
                )

    @classmethod
    def gen_odin_tt(cls):
        """
        生成请求必带的odin_tt (Generate the essential odin_tt for requests)
        """
        transport = httpx.HTTPTransport(retries=5)
        with httpx.Client(transport=transport, proxies=cls.proxies) as client:
            try:
                response = client.get(cls.odin_tt_conf["url"])

                if response.status_code == 401:
                    raise Exception(_("401 由于某些错误, 无法获取ttwid"))
                elif response.status_code == 404:
                    raise Exception(_("404 无法找到API端点"))

                odin_tt = httpx.Cookies(response.cookies).get("odin_tt")

                if odin_tt is None:
                    raise Exception(
                        _("odin_tt: 检查没有通过, 请更新配置文件中的odin_tt")
                    )

                return odin_tt

            except httpx.RequestError:
                # 捕获所有与 httpx 请求相关的异常情况 (Captures all httpx request-related exceptions)
                raise Exception(
                    _(
                        "连接端点失败，检查网络环境或代理：{0} 代理：{1} 类名：{2}"
                    ).format(cls.odin_tt_conf["url"], cls.proxies, cls.__name__)
                )

            except httpx.HTTPStatusError as e:
                # 捕获 httpx 的状态代码错误 (captures specific status code errors from httpx)
                raise Exception(
                    f"HTTP Status Code {e.response.status_code}: {e.response.text}"
                )


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


class SecUserIdFetcher:
    _TIKTOK_SECUID_PARREN = re.compile(
        r"<script id=\"__UNIVERSAL_DATA_FOR_REHYDRATION__\" type=\"application/json\">(.*?)</script>"
    )
    _TIKTOK_UNIQUEID_PARREN = re.compile(r"/@([^/?]*)")
    _TIKTOK_NOTFOUND_PARREN = re.compile(r"notfound")

    @classmethod
    async def get_secuid(cls, url: str) -> str:
        """
        获取TikTok用户sec_uid
        Args:
            url: 用户主页链接
        Return:
            sec_uid: 用户唯一标识
        """

        # 进行参数检查
        if not isinstance(url, str):
            raise TypeError("输入参数必须是字符串")

        # 提取有效URL
        url = extract_valid_urls(url)

        if url is None:
            raise (
                Exception(_("输入的URL不合法。类名：{0}".format(cls.__name__)))
            )

        transport = httpx.AsyncHTTPTransport(retries=5)
        async with httpx.AsyncClient(
            transport=transport, proxies=TokenManager.proxies, timeout=10
        ) as client:
            try:
                response = await client.get(url, follow_redirects=True)

                if response.status_code in {200, 444}:
                    if cls._TIKTOK_NOTFOUND_PARREN.search(str(response.url)):
                        raise Exception(
                            _(
                                "页面不可用，可能是由于区域限制（代理）造成的。类名: {0}".format(
                                    cls.__name__
                                )
                            )
                        )
                    match = cls._TIKTOK_SECUID_PARREN.search(str(response.text))
                    if not match:
                        raise Exception(
                            _(
                                "未在响应的地址中找到sec_uid, 检查链接是否为用户主页类名: {0}".format(
                                    cls.__name__
                                )
                            )
                        )

                    # 提取SIGI_STATE对象中的sec_uid
                    data = json.loads(match.group(1))
                    default_scope = data.get("__DEFAULT_SCOPE__", {})
                    user_detail = default_scope.get("webapp.user-detail", {})
                    user_info = user_detail.get("userInfo", {}).get("user", {})
                    sec_uid = user_info.get("secUid")

                    if sec_uid is None:
                        raise RuntimeError(_("获取sec_uid失败, {0}".format(user_info)))

                    return sec_uid
                else:
                    raise ConnectionError(_("接口状态码异常, 请检查重试"))

            except httpx.RequestError:
                raise Exception(
                    _(
                        "连接端点失败，检查网络环境或代理：{0} 代理：{1} 类名：{2}"
                    ).format(url, TokenManager.proxies, cls.__name__)
                )

    @classmethod
    async def get_all_secuid(cls, urls: list) -> list:
        """
        获取列表secuid列表 (Get list sec_user_id list)

        Args:
            urls: list: 用户url列表 (User url list)

        Return:
            secuids: list: 用户secuid列表 (User secuid list)
        """

        if not isinstance(urls, list):
            raise TypeError(_("参数必须是列表类型"))

        # 提取有效URL
        urls = extract_valid_urls(urls)

        if urls == []:
            raise (
                Exception(
                    _("输入的URL List不合法。类名：{0}".format(cls.__name__))
                )
            )

        secuids = [cls.get_secuid(url) for url in urls]
        return await asyncio.gather(*secuids)

    @classmethod
    async def get_uniqueid(cls, url: str) -> str:
        """
        获取TikTok用户unique_id
        Args:
            url: 用户主页链接
        Return:
            unique_id: 用户唯一id
        """

        # 进行参数检查
        if not isinstance(url, str):
            raise TypeError("输入参数必须是字符串")

        # 提取有效URL
        url = extract_valid_urls(url)

        if url is None:
            raise (
                Exception(_("输入的URL不合法。类名：{0}".format(cls.__name__)))
            )

        transport = httpx.AsyncHTTPTransport(retries=5)
        async with httpx.AsyncClient(
            transport=transport, proxies=TokenManager.proxies, timeout=10
        ) as client:
            try:
                response = await client.get(url, follow_redirects=True)

                if response.status_code in {200, 444}:
                    match = cls._TIKTOK_UNIQUEID_PARREN.search(str(response.url))
                    if not match:
                        raise Exception(_("未在响应中找到unique_id"))

                    unique_id = match.group(1)

                    if unique_id is None:
                        raise RuntimeError(
                            _("获取unique_id失败, {0}".format(response.url))
                        )

                    return unique_id
                else:
                    raise ConnectionError(
                        _("接口状态码异常 {0}, 请检查重试").format(response.status_code)
                    )

            except httpx.RequestError:
                raise Exception(
                    _(
                        "连接端点失败，检查网络环境或代理：{0} 代理：{1} 类名：{2}"
                    ).format(url, TokenManager.proxies, cls.__name__),
                )

    @classmethod
    async def get_all_uniqueid(cls, urls: list) -> list:
        """
        获取列表unique_id列表 (Get list sec_user_id list)

        Args:
            urls: list: 用户url列表 (User url list)

        Return:
            unique_ids: list: 用户unique_id列表 (User unique_id list)
        """

        if not isinstance(urls, list):
            raise TypeError(_("参数必须是列表类型"))

        # 提取有效URL
        urls = extract_valid_urls(urls)

        if urls == []:
            raise (
                Exception(
                    _("输入的URL List不合法。类名：{0}".format(cls.__name__))
                )
            )

        unique_ids = [cls.get_uniqueid(url) for url in urls]
        return await asyncio.gather(*unique_ids)


class AwemeIdFetcher:
    # https://www.tiktok.com/@scarlettjonesuk/video/7255716763118226715
    # https://www.tiktok.com/@scarlettjonesuk/video/7255716763118226715?is_from_webapp=1&sender_device=pc&web_id=7306060721837852167

    # 预编译正则表达式
    _TIKTOK_AWEMEID_PARREN = re.compile(r"video/(\d*)")

    @classmethod
    async def get_aweme_id(cls, url: str) -> str:
        """
        获取TikTok作品aweme_id
        Args:
            url: 作品链接
        Return:
            aweme_id: 作品唯一标识
        """

        # 进行参数检查
        if not isinstance(url, str):
            raise TypeError("输入参数必须是字符串")

        # 提取有效URL
        url = extract_valid_urls(url)

        if url is None:
            raise (
                Exception(_("输入的URL不合法。类名：{0}".format(cls.__name__)))
            )

        transport = httpx.AsyncHTTPTransport(retries=5)
        async with httpx.AsyncClient(
            transport=transport, proxies=TokenManager.proxies, timeout=10
        ) as client:
            try:
                response = await client.get(url, follow_redirects=True)

                if response.status_code in {200, 444}:
                    match = cls._TIKTOK_AWEMEID_PARREN.search(str(response.url))
                    if not match:
                        raise Exception(_("未在响应中找到aweme_id"))

                    aweme_id = match.group(1)

                    if aweme_id is None:
                        raise RuntimeError(
                            _("获取aweme_id失败, {0}".format(response.url))
                        )

                    return aweme_id
                else:
                    raise ConnectionError(
                        _("接口状态码异常 {0}, 请检查重试").format(response.status_code)
                    )

            except httpx.RequestError:
                raise Exception(
                    _(
                        "连接端点失败，检查网络环境或代理：{0} 代理：{1} 类名：{2}"
                    ).format(
                        url,
                        TokenManager.proxies,
                        cls.__name__,
                    )
                )

    @classmethod
    async def get_all_aweme_id(cls, urls: list) -> list:
        """
        获取视频aweme_id,传入列表url都可以解析出aweme_id (Get video aweme_id, pass in the list url can parse out aweme_id)

        Args:
            urls: list: 列表url (list url)

        Return:
            aweme_ids: list: 视频的唯一标识，返回列表 (The unique identifier of the video, return list)
        """

        if not isinstance(urls, list):
            raise TypeError(_("参数必须是列表类型"))

        # 提取有效URL
        urls = extract_valid_urls(urls)

        if urls == []:
            raise (
                Exception(
                    _("输入的URL List不合法。类名：{0}".format(cls.__name__))
                )
            )

        aweme_ids = [cls.get_aweme_id(url) for url in urls]
        return await asyncio.gather(*aweme_ids)


def format_file_name(
    naming_template: str,
    aweme_data: dict = {},
    custom_fields: dict = {},
) -> str:
    """
    根据配置文件的全局格式化文件名
    (Format file name according to the global conf file)

    Args:
        aweme_data (dict): 抖音数据的字典 (dict of douyin data)
        naming_template (str): 文件的命名模板, 如 "{create}_{desc}" (Naming template for files, such as "{create}_{desc}")
        custom_fields (dict): 用户自定义字段, 用于替代默认的字段值 (Custom fields for replacing default field values)

    Note:
        windows 文件名长度限制为 255 个字符, 开启了长文件名支持后为 32,767 个字符
        (Windows file name length limit is 255 characters, 32,767 characters after long file name support is enabled)
        Unix 文件名长度限制为 255 个字符
        (Unix file name length limit is 255 characters)
        取去除后的50个字符, 加上后缀, 一般不会超过255个字符
        (Take the removed 50 characters, add the suffix, and generally not exceed 255 characters)
        详细信息请参考: https://en.wikipedia.org/wiki/Filename#Length
        (For more information, please refer to: https://en.wikipedia.org/wiki/Filename#Length)

    Returns:
        str: 格式化的文件名 (Formatted file name)
    """

    # 为不同系统设置不同的文件名长度限制
    os_limit = {
        "win32": 200,
        "cygwin": 60,
        "darwin": 60,
        "linux": 60,
    }

    fields = {
        "create": aweme_data.get("createTime", ""),  # 长度固定19
        "nickname": aweme_data.get("nickname", ""),  # 最长30
        "aweme_id": aweme_data.get("aweme_id", ""),  # 长度固定19
        "desc": split_filename(aweme_data.get("desc", ""), os_limit),
        "uid": aweme_data.get("uid", ""),  # 固定11
    }

    if custom_fields:
        # 更新自定义字段
        fields.update(custom_fields)

    try:
        return naming_template.format(**fields)
    except KeyError as e:
        raise KeyError(_("文件名模板字段 {0} 不存在，请检查".format(e)))


def create_user_folder(kwargs: dict, nickname: Union[str, int]) -> Path:
    """
    根据提供的配置文件和昵称，创建对应的保存目录。
    (Create the corresponding save directory according to the provided conf file and nickname.)

    Args:
        kwargs (dict): 配置文件，字典格式。(Conf file, dict format)
        nickname (Union[str, int]): 用户的昵称，允许字符串或整数。  (User nickname, allow strings or integers)

    Note:
        如果未在配置文件中指定路径，则默认为 "Download"。
        (If the path is not specified in the conf file, it defaults to "Download".)
        仅支持相对路径。
        (Only relative paths are supported.)

    Raises:
        TypeError: 如果 kwargs 不是字典格式，将引发 TypeError。
        (If kwargs is not in dict format, TypeError will be raised.)
    """

    # 确定函数参数是否正确
    if not isinstance(kwargs, dict):
        raise TypeError("kwargs 参数必须是字典")

    # 创建基础路径
    base_path = Path(kwargs.get("path", "Download"))

    # 添加下载模式和用户名
    user_path = (
        base_path / "tiktok" / kwargs.get("mode", "PLEASE_SETUP_MODE") / str(nickname)
    )

    # 获取绝对路径并确保它存在
    resolve_user_path = user_path.resolve()

    # 创建目录
    resolve_user_path.mkdir(parents=True, exist_ok=True)

    return resolve_user_path


def rename_user_folder(old_path: Path, new_nickname: str) -> Path:
    """
    重命名用户目录 (Rename User Folder).

    Args:
        old_path (Path): 旧的用户目录路径 (Path of the old user folder)
        new_nickname (str): 新的用户昵称 (New user nickname)

    Returns:
        Path: 重命名后的用户目录路径 (Path of the renamed user folder)
    """
    # 获取目标目录的父目录 (Get the parent directory of the target folder)
    parent_directory = old_path.parent

    # 构建新目录路径 (Construct the new directory path)
    new_path = old_path.rename(parent_directory / new_nickname).resolve()

    return new_path


def create_or_rename_user_folder(
    kwargs: dict, local_user_data: dict, current_nickname: str
) -> Path:
    """
    创建或重命名用户目录 (Create or rename user directory)

    Args:
        kwargs (dict): 配置参数 (Conf parameters)
        local_user_data (dict): 本地用户数据 (Local user data)
        current_nickname (str): 当前用户昵称 (Current user nickname)

    Returns:
        user_path (Path): 用户目录路径 (User directory path)
    """
    user_path = create_user_folder(kwargs, current_nickname)

    if not local_user_data:
        return user_path

    if local_user_data.get("nickname") != current_nickname:
        # 昵称不一致，触发目录更新操作
        user_path = rename_user_folder(user_path, current_nickname)

    return user_path


def get_timestamp(unit: str = "milli"):
    """
    根据给定的单位获取当前时间 (Get the current time based on the given unit)

    Args:
        unit (str): 时间单位，可以是 "milli"、"sec"、"min" 等
            (The time unit, which can be "milli", "sec", "min", etc.)

    Returns:
        int: 根据给定单位的当前时间 (The current time based on the given unit)
    """

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
    """
    根据传入长度产生随机字符串 (Generate a random string based on the given length)

    Args:
        randomlength (int): 需要生成的随机字符串的长度 (The length of the random string to be generated)

    Returns:
        str: 生成的随机字符串 (The generated random string)
    """

    base_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-"
    return "".join(random.choice(base_str) for _ in range(randomlength))


def timestamp_2_str(
    timestamp: Union[str, int, float], format: str = "%Y-%m-%d %H-%M-%S"
) -> str:
    """
    将 UNIX 时间戳转换为格式化字符串 (Convert a UNIX timestamp to a formatted string)

    Args:
        timestamp (int): 要转换的 UNIX 时间戳 (The UNIX timestamp to be converted)
        format (str, optional): 返回的日期时间字符串的格式。
                                默认为 '%Y-%m-%d %H-%M-%S'。
                                (The format for the returned date-time string
                                Defaults to '%Y-%m-%d %H-%M-%S')

    Returns:
        str: 格式化的日期时间字符串 (The formatted date-time string)
    """
    if timestamp is None or timestamp == "None":
        return ""

    return datetime.datetime.fromtimestamp(float(timestamp)).strftime(format)


def num_to_base36(num: int) -> str:
    """数字转换成base32 (Convert number to base 36)"""

    base_str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    if num == 0:
        return "0"

    base36 = []
    while num:
        num, i = divmod(num, 36)
        base36.append(base_str[i])

    return "".join(reversed(base36))


def split_set_cookie(cookie_str: str) -> str:
    """
    拆分Set-Cookie字符串并拼接 (Split the Set-Cookie string and concatenate)

    Args:
        cookie_str (str): 待拆分的Set-Cookie字符串 (The Set-Cookie string to be split)

    Returns:
        str: 拼接后的Cookie字符串 (Concatenated cookie string)
    """

    # 判断是否为字符串 / Check if it's a string
    if not isinstance(cookie_str, str):
        raise TypeError("`set-cookie` must be str")

    # 拆分Set-Cookie字符串,避免错误地在expires字段的值中分割字符串 (Split the Set-Cookie string, avoiding incorrect splitting on the value of the 'expires' field)
    # 拆分每个Cookie字符串，只获取第一个分段（即key=value部分） / Split each Cookie string, only getting the first segment (i.e., key=value part)
    # 拼接所有的Cookie (Concatenate all cookies)
    return ";".join(
        cookie.split(";")[0] for cookie in re.split(", (?=[a-zA-Z])", cookie_str)
    )


def split_dict_cookie(cookie_dict: dict) -> str:
    return "; ".join(f"{key}={value}" for key, value in cookie_dict.items())


def extract_valid_urls(inputs: Union[str, list[str]]) -> Union[str, list[str], None]:
    """从输入中提取有效的URL (Extract valid URLs from input)

    Args:
        inputs (Union[str, list[str]]): 输入的字符串或字符串列表 (Input string or list of strings)

    Returns:
        Union[str, list[str]]: 提取出的有效URL或URL列表 (Extracted valid URL or list of URLs)
    """
    url_pattern = re.compile(r"https?://\S+")

    # 如果输入是单个字符串
    if isinstance(inputs, str):
        match = url_pattern.search(inputs)
        return match.group(0) if match else None

    # 如果输入是字符串列表
    elif isinstance(inputs, list):
        valid_urls = []

        for input_str in inputs:
            matches = url_pattern.findall(input_str)
            if matches:
                valid_urls.extend(matches)

        return valid_urls


def _get_first_item_from_list(_list) -> list:
    # 检查是否是列表 (Check if it's a list)
    if _list and isinstance(_list, list):
        # 如果列表里第一个还是列表则提起每一个列表的第一个值
        # (If the first one in the list is still a list then bring up the first value of each list)
        if isinstance(_list[0], list):
            return [inner[0] for inner in _list if inner]
        # 如果只是普通列表，则返回这个列表包含的第一个项目作为新列表
        # (If it's just a regular list, return the first item wrapped in a list)
        else:
            return [_list[0]]
    return []


def get_resource_path(filepath: str):
    """获取资源文件的路径 (Get the path of the resource file)

    Args:
        filepath: str: 文件路径 (file path)
    """

    return importlib_resources.files("f2") / filepath


def replaceT(obj: Union[str, Any]) -> Union[str, Any]:
    """
    替换文案非法字符 (Replace illegal characters in the text)

    Args:
        obj (str): 传入对象 (Input object)

    Returns:
        new: 处理后的内容 (Processed content)
    """

    reSub = r"[^\u4e00-\u9fa5a-zA-Z0-9#]"

    if isinstance(obj, list):
        return [re.sub(reSub, "_", i) for i in obj]

    if isinstance(obj, str):
        return re.sub(reSub, "_", obj)

    # raise TypeError("输入应为字符串或字符串列表")


def split_filename(text: str, os_limit: dict) -> str:
    """
    根据操作系统的字符限制分割文件名，并用 '......' 代替。

    Args:
        text (str): 要计算的文本
        os_limit (dict): 操作系统的字符限制字典

    Returns:
        str: 分割后的文本
    """
    # 获取操作系统名称和文件名长度限制
    os_name = sys.platform
    filename_length_limit = os_limit.get(os_name, 200)

    # 计算中文字符长度（中文字符长度*3）
    chinese_length = sum(1 for char in text if "\u4e00" <= char <= "\u9fff") * 3
    # 计算英文字符长度
    english_length = sum(1 for char in text if char.isalpha())
    # 计算下划线数量
    num_underscores = text.count("_")

    # 计算总长度
    total_length = chinese_length + english_length + num_underscores

    # 如果总长度超过操作系统限制或手动设置的限制，则根据限制进行分割
    if total_length > filename_length_limit:
        split_index = min(total_length, filename_length_limit) // 2 - 6
        split_text = text[:split_index] + "......" + text[-split_index:]
        return split_text
    else:
        return text


def ensure_path(path: Union[str, Path]) -> Path:
    """确保路径是一个Path对象 (Ensure the path is a Path object)"""
    return Path(path) if isinstance(path, str) else path
