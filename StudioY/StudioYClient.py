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
        account_code = 'DF2'
        cookie = 'ttwid=1%7ClZ-8pnFRI86wlOr7uJoCdlXQEc_u9gxrFUlq7GoRqvU%7C1709694308%7C31ae00c2d5af42bb6b1ffb993981978ea887346eb7878f5518b094353b20176c; bd_ticket_guard_client_web_domain=2; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; LOGIN_STATUS=1; store-region=us; store-region-src=uid; my_rd=2; s_v_web_id=verify_ltnje5so_rBZOEQrm_3iTn_4bSI_B07Y_o2easU8yQZI3; __ac_nonce=06637ab8400f155cb4a6e; __ac_signature=_02B4Z6wo00f01-RcHDwAAIDCeMev8zjKkL.kfBiAAJ8q7XIh8g3qqnGzTMb5v7Y9ySTG3eWRIHFJ903H.7Vgy7j2O1Y1lgGkgaquO-lttOweynspgS9Ae0Fq0aY3ajEDDb7463QyMNKrKvZb7e; dy_swidth=3840; dy_sheight=2160; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A3840%2C%5C%22screen_height%5C%22%3A2160%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; csrf_session_id=bcbb96b5a932efbb40a38ec7a5b9a622; passport_csrf_token=ccaab9c00a4a9d763e5eb38e5997e062; passport_csrf_token_default=ccaab9c00a4a9d763e5eb38e5997e062; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; strategyABtestKey=%221714925001.857%22; passport_assist_user=ClASUk2ckVqnCAPss-UO5j5OJhfSZkNElBPndopJE2-Uhh1QqnZjnLAhrdyHTU2SmOY7HS0X8SlhFBnu9234tLF_pwQj8omBiJ28NWyND73D-BpKCjyR5K2vfVnGCzsLQiSdL8rkxJoB2Knc-1ytcX8nblUpBnpcUT9yzyAc6CXxIwBIeAa_WK_-eA80eBGS_98Q5sDQDRiJr9ZUIAEiAQN7R7k6; sso_uid_tt=dc87cc8f5c242fe46b7ec8e9799be391; sso_uid_tt_ss=dc87cc8f5c242fe46b7ec8e9799be391; toutiao_sso_user=cd4817289c7dd5d8ff6bb99ad4c4d02b; toutiao_sso_user_ss=cd4817289c7dd5d8ff6bb99ad4c4d02b; sid_ucp_sso_v1=1.0.0-KDBhZTE4MjcyOWFjYWVhMjMxYTExMzlkMTBmZGQ2MDFhNDE3Y2M5NDEKIQjZtoC85s3eBRDO296xBhjvMSAMMMHyma8GOAVA-wdIAxoCbHEiIGNkNDgxNzI4OWM3ZGQ1ZDhmZjZiYjk5YWQ0YzRkMDJi; ssid_ucp_sso_v1=1.0.0-KDBhZTE4MjcyOWFjYWVhMjMxYTExMzlkMTBmZGQ2MDFhNDE3Y2M5NDEKIQjZtoC85s3eBRDO296xBhjvMSAMMMHyma8GOAVA-wdIAxoCbHEiIGNkNDgxNzI4OWM3ZGQ1ZDhmZjZiYjk5YWQ0YzRkMDJi; uid_tt=a1713692f7cf72037836b341351ccfcf; uid_tt_ss=a1713692f7cf72037836b341351ccfcf; sid_tt=62585ea3624d1e7058e32357e2947019; sessionid=62585ea3624d1e7058e32357e2947019; sessionid_ss=62585ea3624d1e7058e32357e2947019; douyin.com; xg_device_score=7.250131356775587; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%220%22; publish_badge_show_info=%220%2C0%2C0%2C1714925009944%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA25aPwyeSU5rlEaEum_KGSEPSyWF8fUN-oFys4DES7tgmuV3_Jc7mwTR0v-SMive9%2F1714978800000%2F0%2F1714925010371%2F0%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=8a991b91eeeb6975bc54403268501ae3; __security_server_data_status=1; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTnFvaHpDMTN6clVod3ZkcVZMejF6VmlydVRRWERmcTErK3BzMG1KbGhEc0ZidlYwT2RrbXhiSDB6UGhFNnBRRVNXZkNMR1c4WHhDZC9XR3RnQWQ0Z3c9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; passport_fe_beating_status=true; sid_guard=62585ea3624d1e7058e32357e2947019%7C1714925011%7C5183997%7CThu%2C+04-Jul-2024+16%3A03%3A28+GMT; sid_ucp_v1=1.0.0-KDYxMTg4YmUwNTFjMDVlYzI0YmYzYWU4M2M3NTZmYjkxN2E1NGE5OTQKGwjZtoC85s3eBRDT296xBhjvMSAMOAVA-wdIBBoCbGYiIDYyNTg1ZWEzNjI0ZDFlNzA1OGUzMjM1N2UyOTQ3MDE5; ssid_ucp_v1=1.0.0-KDYxMTg4YmUwNTFjMDVlYzI0YmYzYWU4M2M3NTZmYjkxN2E1NGE5OTQKGwjZtoC85s3eBRDT296xBhjvMSAMOAVA-wdIBBoCbGYiIDYyNTg1ZWEzNjI0ZDFlNzA1OGUzMjM1N2UyOTQ3MDE5; odin_tt=69f164c6a3114e10c53c7a8ab9c77630a1a3df312864b758608cb2e5b67ee16d170db08e70d7f22d47293f5d121ff43c3be2640e03b2b20be1126c839e398a03; xgplayer_device_id=87457704722; xgplayer_user_id=329343318797; IsDouyinActive=true; msToken=Lam8Q876-jmNw7KZYr2f1-LTd64sSOuFS5epflPFNFm4SBaWfuFbJeCS6OPKbMOn0At3mMCDW-WtWS0IY-0CrfbG1eKADyfBn_znsMbuWvZ9lA53Sg=='
        client = StudioYClient()
        account_result = client.get_account_id_by_short_code(account_code)
        accountId = account_result['data']
        set_result = client.set_cookie(accountId, cookie)
        cookie = client.get_cookie(accountId)['data']
        assert cookie == cookie

