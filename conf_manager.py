# path: f2/utils/conf_manager.py
from unittest.mock import Mock

import f2
import time

import motor
import yaml
import click

from pathlib import Path

APP_CONFIG_FILE_PATH = "conf/app.yaml"
F2_CONFIG_FILE_PATH = "conf/conf.yaml"
F2_DEFAULTS_FILE_PATH = "conf/defaults.yaml"


def _(msg):
    return msg
logger=Mock()


class ConfigManager:
    # 如果不传入应用配置路径，则返回项目配置 (If the application conf path is not passed in, the project conf is returned)
    def __init__(self, filepath: str = f2.F2_CONFIG_FILE_PATH):
        if Path(filepath).exists():
            self.filepath = Path(filepath)
        else:
            from utils import get_resource_path
            self.filepath = Path(get_resource_path(filepath))
        self.config = self.load_config()

    def load_config(self) -> dict:
        """从文件中加载配置 (Load the conf from the file)"""

        try:
            if not self.filepath.exists():
                raise Exception(_("'{0}' 配置文件路径不存在").format(self.filepath))
            return yaml.safe_load(self.filepath.read_text(encoding="utf-8")) or {}
        except Exception as e:
            e.display_error()
            time.sleep(2)
            exit(0)

    def get_config(self, app_name: str, default=None) -> dict:
        """
        从配置中获取给定键的值 (Get the value of the given key from the conf)

        Args:
            app_name: str: 应用名称 (app name)
            default: any: 默认值 (default value)

        Return:
            self.config.get 配置字典 (conf dict)
        """

        return self.config.get(app_name, default)

    def save_config(self, config: dict):
        """将配置保存到文件 (Save the conf to the file)
        Args:
            config: dict: 配置字典 (conf dict)
        """
        try:
            self.filepath.write_text(yaml.dump(config), encoding="utf-8")
        except PermissionError:
            raise Exception(
                _("'{0}' 配置文件路径无写权限").format(self.filepath)
            )

    def backup_config(self):
        """在进行更改前备份配置文件 (Backup the conf file before making changes)"""
        # 如果已经是备份文件，直接返回 (If it is already a backup file, return directly)
        if self.filepath.suffix == ".bak":
            return

        backup_path = self.filepath.with_suffix(".bak")
        if backup_path.exists():
            backup_path.unlink()  # 删除已经存在的备份文件 (Delete existing backup files)
        self.filepath.rename(backup_path)

    def generate_config(self, app_name: str, save_path: Path):
        """生成应用程序特定配置文件 (Generate application-specific conf file)"""

        if not isinstance(app_name, str):
            return

        # 将save_path转换为Path对象
        save_path = Path(save_path)

        # 如果save_path是相对路径，则将其转换为绝对路径
        if not save_path.is_absolute():
            save_path = Path.cwd() / save_path

        # 确保目录存在，如果不存在则创建
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # 读取默认配置
        default_config = (
            yaml.safe_load(
                Path(get_resource_path(f2.F2_DEFAULTS_FILE_PATH)).read_text(
                    encoding="utf-8"
                )
            )
            or {}
        )

        if app_name in default_config:
            # 将app_name作为外层键 # https://github.com/Johnserf-Seed/TikTokDownload/issues/626  #629
            app_config = {app_name: default_config[app_name]}

            # 写入应用程序特定配置
            save_path.write_text(yaml.dump(app_config), encoding="utf-8")
            logger.info(
                _("{0} 应用配置文件生成成功，保存至 {1}").format(app_name, save_path)
            )
        else:
            logger.info(_("{0} 应用配置未找到").format(app_name))

    def update_config_with_args(self, app_name: str, **kwargs):
        """
        使用提供的参数更新配置 (Update the conf with the provided parameters)

        Args:
            app_name: str: 应用名称 (app name)
            kwargs: dict: 配置字典 (conf dict)
        """

        app_config = self.config.get(app_name, {})

        # 使用提供的参数更新特定应用的配置
        for key, value in kwargs.items():
            if key == "app_name":
                continue
            if value is not None:
                app_config[key] = value

        self.config[app_name] = app_config

        # 在保存前询问用户确认 (Ask the user for confirmation before saving)
        if click.confirm(
            _("是否要使用命令行的参数更新配置文件？")
            + (f"`{Path.cwd() / self.filepath}`"),
            default=True,
        ):
            # 备份原始配置文件
            self.backup_config()
            # 保存更新的配置 (Save the updated conf)
            self.save_config(self.config)
            click.echo(_("配置文件已更新!"))
        else:
            click.echo(_("已取消更新配置文件!"))


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
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            'mongodb://192.168.196.85:27018,192.168.196.86:27018,192.168.196.87:27018/?replicaSet=tiktok')
        self.db = self.client['tiktok']
        self.following_lists = self.db['following_lists']
        self.following_relations = self.db['following_relations']
        self.tiktok_users = self.db['tiktok_users']
        self.tiktok_follow_list_candidates = self.db['tiktok_users_follow_no_lists_view']
        self.tiktok_follow_view = self.db['tiktok_users_follow_view']


TikTokDb = TikTokMongoDb()
