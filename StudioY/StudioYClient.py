from typing import List
from unittest import TestCase

import requests
import json

from filter import UserPostFilter


class StudioYMapper:
    @staticmethod
    def convert_to_tiktok_user_dto(author: dict):
        return {
            'SecUid': author['secUid'],
            'Uid': author['id'],
            'AvatarUrl': author['avatarLarger'],
            'AvatarThumbUrl': author['avatarThumb'],
            'Nickname': author['nickname'],
            'VideoCount': 0,  # There is no corresponding property in UserPostFilter
            'FollowerCount': 0,  # There is no corresponding property in UserPostFilter
            'FollowingCount': 0,  # There is no corresponding property in UserPostFilter
            'HeartCount': 0,  # There is no corresponding property in UserPostFilter
            'Signature': author['signature'],
            'UniqueId': author['uniqueId']
        }

    @staticmethod
    def convert_to_tiktok_user_video_dto(user_post_filter: UserPostFilter):
        return {
            'AwemeId': user_post_filter.awemeId,
            'Caption': user_post_filter.desc,
            'Description': user_post_filter.desc,
            'Height': user_post_filter.videoHeight,
            'Width': user_post_filter.videoWidth,
            'Duration': 0,  # There is no corresponding property in UserPostFilter
            'CoverUrl': user_post_filter.videoCover,
            'Ratio': user_post_filter.videoRatio,
            'BestBitRateUrl': '',  # There is no corresponding property in UserPostFilter
            'CreateTime': user_post_filter.createTime,
            'CollectCount': user_post_filter.collectCount,
            'CommentCount': user_post_filter.commentCount,
            'DiggCount': user_post_filter.diggCount,
            'PlayCount': user_post_filter.playCount,
            'ShareCount': user_post_filter.shareCount,
            'TikTokUser': StudioYMapper.convert_to_tiktok_user_dto(user_post_filter.author)
        }
class StudioYClient:
    # def __init__(self, base_url='https://localhost:44358/api'):
    def __init__(self, base_url='https://eu1.tta.rewbl.us/api'):
        self.base_url = base_url

    def get_cookie(self, account_id):
        response = requests.get(f'{self.base_url}/tiktok-accounts/cookie', params={'accountId': account_id}, verify=False)
        return response.json()

    def set_cookie(self, account_id, cookie):
        response = requests.put(f'{self.base_url}/tiktok-accounts/cookie', params={'accountId': account_id},
                                data=json.dumps(cookie), headers={'Content-Type': 'application/json'}, verify=False)
        return response.json()

    def get_account_id_by_short_code(self, short_code):
        response = requests.get(f'{self.base_url}/tiktok-accounts/account-id', params={'shortCode': short_code}, verify=False)
        return response.json()

    def link_account(self, short_code, user_json):
        url = f'{self.base_url}/tiktok-accounts/link-user'
        headers = {'Content-Type': 'application/json'}
        params = {'shortCode': short_code}
        response = requests.post(url, params=params, data=json.dumps(user_json), headers=headers, verify=False)
        return response.json()

    def sync_user_videos(self, videos: List[UserPostFilter]):
        url = f'{self.base_url}/tiktok-accounts/sync-videos'
        headers = {'Content-Type': 'application/json'}
        payload =json.dumps([StudioYMapper.convert_to_tiktok_user_video_dto(video) for video in videos])
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response.json()

    def get_all_accounts(self):
        response = requests.get(f'{self.base_url}/tiktok-accounts/all', verify=False)
        return response.json()

    def get_all_sec_uids(self):
        accs = self.get_all_accounts()
        if not accs:
            return []
        if not accs['isSuccess']:
            return []

        sec_uid_list = [(acc.get('tikTokUser') or {}).get('secUid') for acc in accs['data']]
        sec_uid_list = [sec_uid for sec_uid in sec_uid_list if sec_uid]
        return sec_uid_list

def get_account_id_and_cookie(short_code):
    client = StudioYClient()
    account_result = client.get_account_id_by_short_code(short_code)
    accountId = account_result['data']
    cookie = client.get_cookie(accountId)['data']
    return accountId, cookie


class TestStudioYClient(TestCase):
    def test_account_id_and_cookie(self):
        accountId, Cookie = get_account_id_and_cookie('TestA1')
        breakpoint()

    def test_set_cookie(self):
        account_code = 'J3'
        cookie = '__ac_signature=_02B4Z6wo00f01HO2G5gAAIDCkrb4msrVouRzlh8AAHr6fb; ttwid=1%7CUwm5AQc4NyEJQ4Hejip0Z3htCZFpXI51EppgvSJGz8g%7C1713327549%7C5a73624d77f7aa2c5757a91f8ff2a9aa9984eb5bbd750a76e05d7a1664f07c51; xgplayer_user_id=477104682270; passport_csrf_token=df92eecba6b6d828adf7a1427b706cd8; passport_csrf_token_default=df92eecba6b6d828adf7a1427b706cd8; bd_ticket_guard_client_web_domain=2; s_v_web_id=verify_lv3b24oj_KQG14o7n_FtGm_4qaP_8CUy_WuFUxq3thrRI; d_ticket=35eb3f5357edc7698288ef2d7698ba3657f3c; passport_assist_user=CjwAHUNLruhnyC2A3T15efQbzfgK-7B-aQZbPocW-oiEwbovrqeXs0EPGKnWAakH-6h4cLUkJHOL4x2U72YaSgo8Cs7kyf4mR9aRsg35fqy-t_UAbd5qHW81NZoIzmKY9uFcd3Q5vz0Y9rtqzumme1rPLfDXwT2iAr8VBz0lELjvzg0Yia_WVCABIgED9p73HQ%3D%3D; n_mh=WxEkjpdQfBvzKmRpX0jDUaKutRNsRB-rHE9v6vu8tnI; sso_uid_tt=5ae885ba95ce38b6f9e523cc0f7812a8; sso_uid_tt_ss=5ae885ba95ce38b6f9e523cc0f7812a8; toutiao_sso_user=5b671ad34fb3cb5f266d4cdfe96c1d8c; toutiao_sso_user_ss=5b671ad34fb3cb5f266d4cdfe96c1d8c; sid_ucp_sso_v1=1.0.0-KGVlNDBiN2Y2MjU5ZGIwYTgxMjFmNjFlYzVhM2FjZjRlOTc3NzNhZTYKHQjOxKKe2wIQzZz9sAYY7zEgDDD9vJjUBTgGQPQHGgJscSIgNWI2NzFhZDM0ZmIzY2I1ZjI2NmQ0Y2RmZTk2YzFkOGM; ssid_ucp_sso_v1=1.0.0-KGVlNDBiN2Y2MjU5ZGIwYTgxMjFmNjFlYzVhM2FjZjRlOTc3NzNhZTYKHQjOxKKe2wIQzZz9sAYY7zEgDDD9vJjUBTgGQPQHGgJscSIgNWI2NzFhZDM0ZmIzY2I1ZjI2NmQ0Y2RmZTk2YzFkOGM; passport_auth_status=12d24e7ad99e6fdad3bc5130a4ad940b%2C; passport_auth_status_ss=12d24e7ad99e6fdad3bc5130a4ad940b%2C; uid_tt=3fcb79d675f8567f1369f580c89b5e2e; uid_tt_ss=3fcb79d675f8567f1369f580c89b5e2e; sid_tt=6002831b214b0267e10046a4e1074ed9; sessionid=6002831b214b0267e10046a4e1074ed9; sessionid_ss=6002831b214b0267e10046a4e1074ed9; LOGIN_STATUS=1; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=a435e46ad408af09705d31d105625875; __security_server_data_status=1; store-region=de; store-region-src=uid; sid_guard=6002831b214b0267e10046a4e1074ed9%7C1713327702%7C5183994%7CSun%2C+16-Jun-2024+04%3A21%3A36+GMT; sid_ucp_v1=1.0.0-KDVmMjVkOGIxNGEwMzRmODhhMjNjZjViZmJmNGE2ZGNmZjJhMGFiMWYKGQjOxKKe2wIQ1pz9sAYY7zEgDDgGQPQHSAQaAmxmIiA2MDAyODMxYjIxNGIwMjY3ZTEwMDQ2YTRlMTA3NGVkOQ; ssid_ucp_v1=1.0.0-KDVmMjVkOGIxNGEwMzRmODhhMjNjZjViZmJmNGE2ZGNmZjJhMGFiMWYKGQjOxKKe2wIQ1pz9sAYY7zEgDDgGQPQHSAQaAmxmIiA2MDAyODMxYjIxNGIwMjY3ZTEwMDQ2YTRlMTA3NGVkOQ; _waftokenid=eyJ2Ijp7ImEiOiJub0IwRjdvSHR0V28zdGw4K21XdXQyMER2TWQ3a2pERnhleUtUMGJEeWtnPSIsImIiOjE3MTUzMTMyNDcsImMiOiI2WU9BOGs3VnBLbHpVeE9kaGlVL1ZraEhtSUlxdnVhZEl2NEpLOFFhaVhnPSJ9LCJzIjoicWYxalNOUWg2WjRhWVBoUE8xeTlpbTZJbzk1ekVYNFhFWWRRY0tIWFFaZz0ifQ; douyin.com; xg_device_score=7.008154088107373; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; IsDouyinActive=true; dy_swidth=1920; dy_sheight=1080; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; publish_badge_show_info=%220%2C0%2C0%2C1715313248777%22; csrf_session_id=1d90c9356ba786de489c4bfdbd06d713; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAMrvjaHYRAba46eapQ25N1pERhv1igxHBeWuBqQGNlSA%2F1715378400000%2F0%2F1715313249222%2F0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQmsrVWVKcFc3Unovb055cXJJaE9FZFNtOUVoN2VxMmR3S2tFTTJMOWR2Q0IxaUlvUUNGN2wvdjB2eGprUmpYeWtzMjZITm9ibTJmbitNT3o2VUdBdVE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; strategyABtestKey=%221715313249.855%22; passport_fe_beating_status=true; home_can_add_dy_2_desktop=%221%22; odin_tt=faf746e6d90de6ddfc49085758630f1979e164f2d8ba32ba52c58fa44962bbe147264861476386f6c041d84af7c56f09; msToken=e6dFSCat3pZs8QnfJS4u5n3QzykRKRPuhFRaHnRRC0J1wobMtVRCF9r57LxzY-jD16GNa99FkrU9WgXs10r-lGTYHiIRyxErz6gdxhm8iyKDmI5YtJ6B'
        client = StudioYClient()
        account_result = client.get_account_id_by_short_code(account_code)
        accountId = account_result['data']
        set_result = client.set_cookie(accountId, cookie)
        cookie = client.get_cookie(accountId)['data']
        assert cookie == cookie

