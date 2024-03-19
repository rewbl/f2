
import requests as requests

from model import (
    UserProfile, UserPost, UserFollowing,
)
from utils import XBogusManager, TiktokAPIEndpoints as tkendpoint

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    "Referer": 'https://www.tiktok.com/',
    'Cookie': '_ttp=2MYJvt2pN7OZmPqz21Crv3OQi0U; tt_csrf_token=3zgtMKET-3NGszpnqQO5v2DFHCloYwPyWGR8; cookie-consent={%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22reddit%22:true%2C%22hubspot%22:true%2C%22version%22:%22v10%22}; tiktok_webapp_theme=light; odin_tt=3308243aafa5b1ae701e533c303b41913c2a1ae913e0fd96d49114498ba3a474009f64a853881daf8ad4438244ae58ec8ada3d507f09198d7b05043e481578535428cad6a32d19534c42a004481b356e; s_v_web_id=verify_lq7f7x9g_FNE66wFk_sGJs_4cdU_ARyx_di8PoOZZs0qx; passport_csrf_token=71c89612011cf1a853180cbaee16ac89; passport_csrf_token_default=71c89612011cf1a853180cbaee16ac89; csrfToken=hOFQkpnW-icEJGyVDpisbeiZjsJ_HaQgyXds; tt_chain_token=aDcc9U5Jqzi9l5PXKvOWQg==; multi_sids=6828224526217774085%3A0283f83bdaccca6da5bb49c6b75fc0ca; cmpl_token=AgQQAPNSF-RO0o78VKD74N08_7u2e6BI_6IaYNCcLQ; uid_tt=812e3b42b46e0a8f4705326d33d0fbc30103255d09eb8f3a7f89d32fc738b620; uid_tt_ss=812e3b42b46e0a8f4705326d33d0fbc30103255d09eb8f3a7f89d32fc738b620; sid_tt=0283f83bdaccca6da5bb49c6b75fc0ca; sessionid=0283f83bdaccca6da5bb49c6b75fc0ca; sessionid_ss=0283f83bdaccca6da5bb49c6b75fc0ca; store-idc=useast5; store-country-code=us; store-country-code-src=uid; tt-target-idc=useast5; tt-target-idc-sign=w9y0Vn9EK4wffEnm0wkRa3k_3qI_wWEP96_woVp7HWyYfV9zp_zqvXFnT4Gf_BV734Gt2sYYRaZ_dgfnS9zYRhleoL-2U04dAcHxDOV0EJvEB0ose-bAzf8gJ9LKUYjDzVwB5jehocFGHWmxSsuX__ivStVZyiF8jm10ttAagD1ZqwMGuLynqwzCVLr8xRUjkvrOsfyo701u_UJ23ILmHpugAiEeiZ-ZtWfCibW0UIOhHxz3wWDcda0iVauiuEppL9Q0ZSPBPttrn0fHGxSApM-U9Z2X68obSAsGpnS7U6xayQ5Bk8nTkglVHHzXM1SVK34oBCIuLKsI78cCcaS19l3pzYt4dgx7sX_kU9oIH9CS6zLFUlaLLwCpb6QL9HlEypSstkRln13zXT3JMrQ4liQkFrXb-3YUqBTvM2M2nuAwbZqGHX-8goJ-xOPs4Etg0AIGluk2v-5ydDjQpI6vIjLmVrBtBcZ6GitVvEryEX_na-h-e5o1d_NSzk-0PUHN; last_login_method=handle; sid_guard=0283f83bdaccca6da5bb49c6b75fc0ca%7C1710564097%7C15551996%7CThu%2C+12-Sep-2024+04%3A41%3A33+GMT; sid_ucp_v1=1.0.0-KDI4MTZiMWE3MjU3MDgyNjU0ZmFlYTFmNDVkOWZmYmM5NTQ0ODZjMDYKGAiFiMie98Cu4V4QgcbUrwYYsws4BEDqBxAEGgd1c2Vhc3Q1IiAwMjgzZjgzYmRhY2NjYTZkYTViYjQ5YzZiNzVmYzBjYQ; ssid_ucp_v1=1.0.0-KDI4MTZiMWE3MjU3MDgyNjU0ZmFlYTFmNDVkOWZmYmM5NTQ0ODZjMDYKGAiFiMie98Cu4V4QgcbUrwYYsws4BEDqBxAEGgd1c2Vhc3Q1IiAwMjgzZjgzYmRhY2NjYTZkYTViYjQ5YzZiNzVmYzBjYQ; perf_feed_cache={%22expireTimestamp%22:1710795600000%2C%22itemIds%22:[%227337394898192059680%22%2C%227338463230970531104%22]}; ak_bmsc=9578438D80D57F95780FBB9420AE9FEA~000000000000000000000000000000~YAAQGqEkF8g/Pj2OAQAAU1VjUxf4qoZ/LvvApvOH0/9ev64S2pLGCVfoE3o6zmbfcs+DZPmQ+95GpoEh8MSymc0/AsiWvBDpDTGr7mBbB6+C/4iJN0zsjb5E5TuKReRP6FHGzA+HYXwNPfJ+Zbzs/C+48HhAE1NxXPFDvwG0HErtsPxLTn12Sg6ofCgOWw9+jof8ZMrWpZ64AkEGvlrBcBRe4bnUx6cUIUHAmNAMDeOTREYVrq41WdRjlPL/D5YmTUigNLv3hXeksXVmiyZAzoKkZPQVXZihneJPvVwBW4/ZLWVzQ4tnyDwHtrSRT31v0yiyKpHm+vBCLXraHwYQqxKED4C/i9OzmX3bnzUHYn+5NkXhzEtsFeowfHmz8yz/DG8sKntU; passport_fe_beating_status=true; ttwid=1%7CkqCKNr0WlzX7xPvflppGD3YDhQX7qUpmO-joKgCQuVM%7C1710796005%7Cf49d3592ddade433ab55cb6e03400840aa3d3ff82ed6eb7903feb3e55edd4586; msToken=x541bHi1s7WSeHchOdUW2yAEOEP7zrlEl1OGzqFe6J3tq-HZYOtucwzWK2O_2gA3E9xoxmG7QN6dsaOp1T9HuCIbKNm4wLQv-nSuZhH8OQyUvHu2ySp1EDp5xt3STiYycrQ5VJg=; bm_sv=2329E92974DD4AC81086E527209ADDFC~YAAQGqEkF+o/Pj2OAQAAlmpjUxcaHoFSDvQnMnkWEicEiZi0Ydmgp5ur80ymfc4coWaJpslwqh66mAyNQVg8A6CmWzLv0gsYNXLnFTa0TcZj74NeAKY0oOFvCymrik9FvG1UV8ey9tLBhNq8XXCeyh96yxaY3Fq2rdxzdla+B0UkmW7+tmEjy/AP+RN+yJCcUixEbj/YLddwvJ5NE5+Np9/wI2KqnOzhEg8T20jpnOgUuvDdO5KElowf1y5NBSBw~1; msToken=6i0C4BLtJB_GpTdqZvEBE7eQAzuHVpwzsaJ_blEH9GKdIcIlPvJlWQNVIJwhw_GQ5UmksxllCOyiR4Kv8Vdnca9cyjlgYW6xvrmqFWuaor4LoVlpaqDIcqe1_7N7JXZv99gtHqe0B40VB1NA'
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
