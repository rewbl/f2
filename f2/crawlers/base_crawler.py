# path: f2/crawlers/base_crawler.py

import asyncio
import json

import httpx
from httpx import Response

from f2.exceptions.api_exceptions import (
    APIError,
    APIConnectionError,
    APIRetryExhaustedError,
)


class BaseCrawler:
    """
    基础爬虫客户端 (Base crawler client)
    """

    def __init__(self ):

        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            "Referer": 'https://www.tiktok.com/',
        }

        self.crawler_headers = headers
        limits = httpx.Limits(max_connections=10)
        self.atransport = httpx.AsyncHTTPTransport(retries=3)

        timeout = httpx.Timeout(10)
        self.aclient = httpx.AsyncClient(
            headers=self.crawler_headers,
            timeout=timeout,
            limits=limits,
            transport=self.atransport,
        )

    async def _fetch_response(self, endpoint: str) -> Response:
        return await self.get_fetch_data(endpoint)

    async def _fetch_get_json(self, endpoint: str) -> dict:
        response = await self.get_fetch_data(endpoint)
        return self.parse_json(response)

    async def _fetch_post_json(self, endpoint: str, params: dict = {}) -> dict:
        response = await self.post_fetch_data(endpoint, params)
        return self.parse_json(response)

    def parse_json(self, response: Response) -> dict:

        if (
                response is not None
                and isinstance(response, Response)
                and response.status_code == 200
        ):
            try:
                return response.json()
            except json.JSONDecodeError as e:
                # logger.error(_("解析 {0} 接口 JSON 失败： {1}").format(response.url, e))
                ...
        else:
            if isinstance(response, Response):
                #
                ...
            else:
                # logger.error(_("无效响应类型。响应类型: {0}").format(type(response)))
                ...
        return {}

    async def get_fetch_data(self, url: str):
        response = await self.aclient.get(url, follow_redirects=True)
        return response

    async def post_fetch_data(self, url: str, params: dict = {}):

        for attempt in range(3):
            try:
                response = await self.aclient.post(
                    url, json=dict(params), follow_redirects=True
                )
                if not response.text.strip() or not response.content:
                    error_message = _(
                        "第 {0} 次响应内容为空, 状态码: {1}, URL:{2}"
                    ).format(attempt + 1, response.status_code, response.url)

                    # logger.warning(error_message)

                    if attempt == 3 - 1:
                        raise APIRetryExhaustedError(
                            _("获取端点数据失败, 次数达到上限")
                        )

                    await asyncio.sleep(1)
                    continue

                # logger.debug(_("响应状态码: {0}").format(response.status_code))
                response.raise_for_status()
                return response

            except httpx.RequestError:
                raise APIConnectionError(
                    # _(
                    #     "连接端点失败，检查网络环境或代理：{0} 代理：{1} 类名：{2}"
                    # ).format(url, self.proxies, self.__class__.__name__)
                )

            except httpx.HTTPStatusError as http_error:
                self.handle_http_status_error(http_error, url, attempt + 1)

            except APIError as e:
                e.display_error()

    def handle_http_status_error(self, http_error, url: str, attempt):
        ...

    async def close(self):
        await self.aclient.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclient.aclose()
