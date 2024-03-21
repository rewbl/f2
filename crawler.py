
import requests as requests

from model import (
    UserProfile, UserPost, UserFollowing,
)
from utils import XBogusManager, TiktokAPIEndpoints as tkendpoint

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    "Referer": 'https://www.tiktok.com/',
    'Cookie': 'tiktok_webapp_theme=light; passport_csrf_token=0e03b1dc09cbe1d6379a45256b06bea9; passport_csrf_token_default=0e03b1dc09cbe1d6379a45256b06bea9; multi_sids=7330736351522309162%3A0681d1c02994a74fd480acdcbdc2b7b1; cmpl_token=AgQQAPNSF-RO0rWC73imtR0T_5ko24pOv5zZYNCM_w; sid_guard=0681d1c02994a74fd480acdcbdc2b7b1%7C1710797491%7C15552000%7CSat%2C+14-Sep-2024+21%3A31%3A31+GMT; uid_tt=109567da0f488fc74762733c132bda13d460bab0b0508cba48b29425f5b952a4; uid_tt_ss=109567da0f488fc74762733c132bda13d460bab0b0508cba48b29425f5b952a4; sid_tt=0681d1c02994a74fd480acdcbdc2b7b1; sessionid=0681d1c02994a74fd480acdcbdc2b7b1; sessionid_ss=0681d1c02994a74fd480acdcbdc2b7b1; sid_ucp_v1=1.0.0-KDYwZjkzMjQyNGEzNTY2NDdjNzI2ZWRmNjRhNjA4MWNkNDk0NjE1ZDcKIAiqiJ_08ruA3mUQs-XirwYYswsgDDCohPCtBjgEQOoHEAQaB3VzZWFzdDUiIDA2ODFkMWMwMjk5NGE3NGZkNDgwYWNkY2JkYzJiN2Ix; ssid_ucp_v1=1.0.0-KDYwZjkzMjQyNGEzNTY2NDdjNzI2ZWRmNjRhNjA4MWNkNDk0NjE1ZDcKIAiqiJ_08ruA3mUQs-XirwYYswsgDDCohPCtBjgEQOoHEAQaB3VzZWFzdDUiIDA2ODFkMWMwMjk5NGE3NGZkNDgwYWNkY2JkYzJiN2Ix; store-idc=useast5; store-country-code=us; store-country-code-src=uid; tt-target-idc=useast8; tt-target-idc-sign=WN996Btf2WTWdqdaDXkH2qCgeZDFyCUMSrJq3ildQOvEaXQFGRHb_1eCGVP-a9RF4OMBbXSSJorX33-1U61U_KgF2ItK7peYuULYuaKTX4WlQPIDwsezhrKtVe-Zo3qJsLtc1hwjU2COvkXt7CVLH2O_AlkVexkDW8x3K4vtMn-zSpta6gDOK71Wrmh5XTGgf1Pd34QQIqXFWbdvuz7A1BmYE6yBTq06H4fDyQbKrmH95HFMVG31Jg2-5UgRSD_KWPfJGdjB7FjiYxXmjhldD1QayJtoNZ4ZF3IloS7g2f8ChthuiNoO-jfE5RtoiPkiFV-VOgOCV-MF70vuANSySmxaBpNNkx3BDI7uUwp885KCHpvOr4qjLONqAMbpO6y2ZpirAa_Xe_8tVrIkS7ac9Fs1AHOuekJlSgxqTxlYb9y3NzjZEENfNBnT5g041PSvd-CmPnafbIwm_9g4csL1DNR6yVPJ85f5TTz-t_QiMJt0HqRj1ul2YP7i4gkPsIkb; last_login_method=handle; tt_chain_token=B8dXbSuXYCBhbnjEEqGGgw==; tt_csrf_token=eGYLFZgU-KW4KnL3K5l3DmL_wBWkdsHma5M8; ak_bmsc=9684A40417E72EE077A4F5910199463D~000000000000000000000000000000~YAAQFRUhF+N2+VOOAQAAhbvsXBdW3XPxKGoVgoqhWvw5MeHbONZcO+sfeBHN4suMbtNf02flNqc9j9nIXySpFTK5fFjHY/MwBvTifgzuJvOjmU384Tvvzs24/IdYnAuo8yohCTo6VetGy7OBFUmSBZ8cCJ5YV+piPOzaUdluRBfcPeLlg/IPUJEfTWGknvfIKqfib46yU5Kqw/kT12D+lYJZc8jgLuXbU8sxGEkvUfG7ITUGqaaYjXGyP2dHQs5HnVTy7Y5VGlySeiHl6EHZrAQFaIXeTXHomZ0dr8WCPq385RcXI3EJy6c+JySKrLgfUwEsUJ9KAMaXJoajMPbLUgQfPdFbwbfF14iSY0nXqhiymcLSqhfQyNeB1gbVcg2muaFg0cz1YyLg; passport_fe_beating_status=true; ttwid=1%7CB5zGWNDzs99KqnL8hHF4DVrFjOVIr7pvYLGWAMg_y-0%7C1710956002%7C7350db473760f7f1548101179b918de9b8bc92f0a12ae6a987f1f3395111d08e; odin_tt=7b6e2d2c72f791045510b5f90dda2dc6bdbc44fa7302b5280100e0c54e11bb322dd279975a5b383f71b116fe02d2da64f9fe111bced9ada19a9633255be88b5f2db3e93432a2a3fcf5dfd84ba7188bc6; msToken=PKbOuxVD4GRRasliPootRA8a2deWAD_JfmaLFqdJ8IhdwH_2fQYo9qZlT7QrUtXdM5o4kRsLZ5vzeCVQmtHbDVKQUMd0IwXDrKNuV2l3F8y6fYWOOKWLUCrzT8YkcX3HLkwV6Iddhf9vXiQS; perf_feed_cache={%22expireTimestamp%22:1711126800000%2C%22itemIds%22:[%227342967563321822497%22%2C%227338823235246640390%22%2C%227331114580422298926%22]}; bm_sv=361DEC54660C029452217C5A8D8DFB54~YAAQHBUhF1U9j1uOAQAAw+XsXBe4mOFS1NsUljKAOO/p4wWriF5TGMoBCiiUfj5iBnJ0FRFLV+zWX/b6qBFPkTU1Q+J7kI8jKXfSkHsoAtXBUva8VxzYqH0R+C3hGWs+hpVOvYRWJ2aGc0dZWQDO3kWJrXvty3YtZ6Zn+4s7/dp/JDkp3IwbqVMU3HAHRx56Yt5+qUXCHPIqGSLQ6jcH3nvIvROsvbERZEzS2ewjCByUHso9J4IpU0N4dDVXaWT3~1; msToken=n0fS9JmP-cdFmpxJ5anwc48AxdgN2wwvNozYo6FHwjjKgup_j91zMYL5T_ktYjn-zZWU3KUEfsZZT6Utr8W--pMeJNnX4V4SdIrHNxMw2DHKkSIsdruIvEoMbniLwvlty3eN9DMYpRe8gArl'
}


class TiktokCrawler:

    async def fetch_user_profile(self, params: UserProfile):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_DETAIL, params.dict()
        )  # fmt: off

        response = requests.get(endpoint, headers=headers)
        return response.json()

    async def fetch_user_posts(self, params: UserPost):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_POST, params.dict()
        )
        response = requests.get(endpoint, headers=headers)
        try:
            return response.json()
        except Exception as e:
            return {}

    async def fetch_user_following(self, params: UserFollowing):
        endpoint = XBogusManager.model_2_endpoint(
            tkendpoint.USER_FOLLOWING, params.dict()
        )
        response = requests.get(endpoint, headers=headers)
        try:
            return response.json()
        except Exception as e:
            return {}
