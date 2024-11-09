#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : haimian
# @Time         : 2024/8/2 15:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx
import json_repair
import jsonpath

from meutils.pipe import *
from meutils.schemas.haimian_types import HaimianRequest
from meutils.schemas.task_types import Task

from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=ax1BQH"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)

# url = "https://www.haimian.com/jd/api/v1/generate/lyric2song?app_name=goat&aid=588628&app_id=588628&app_version=1.0.0.397&channel=online&region=CN&device_platform=web&msToken=hXy3dUqC1FoEKSDhn7h9el2p5Iegrf86G-71wZAL10-HEZxjZWHZdb2iZCsMomcIymhvKkFNFlj6SW0q6M6x-mw3P2UPKMHp73nUYMouCfpdo-_0paLZlgj9XCjCAA%3D%3D&a_bogus=QvW0BfwvDiVpDDmR5RoLfY3quOWwYdR50ajLMDgPEpBKOg39HMOl9exEoNs4RkbjN4%2FkIejjy4hbO3xprQQJ8Hwf7Wsx%2F2CZs640t-Pg-nSSs1feeLbQrsJx-kz5Feep5JV3EcvhqJKczbEk09Cn5iIlO6ZCcHgjxiSmtn3Fv-S%3D"

url = "https://www.haimian.com/jd/api/v1/generate/lyric2song"
BASE_URL = "https://www.haimian.com/jd/api/v1"


@retrying()
async def create_task(request: HaimianRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = request.model_dump()
    headers = {
        'Cookie': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post("/generate/lyric2song", json=payload)

        if response.is_success:
            data = response.json()['data']
            task_ids = jsonpath.jsonpath(data, "$..tasks..task_id")
            return Task(id=f"haimian-{task_ids | xjoin(',')}", data=data, system_fingerprint=token)


async def get_task(task_id, token):
    task_id = task_id.split("-")[-1]
    params = [('task_ids', task_id) for task_id in task_id.split(',')]

    headers = {
        'Cookie': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.get("/generate/tasks/info", params=params)
        if response.is_success:
            return response.json()


@alru_cache(ttl=30)
@retrying()
async def generate_lyrics(prompt: str = "写一首夏日晚风的思念的歌", token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = {
        "input": prompt,
        "type": 0
    }
    headers = {
        'Cookie': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.post("/generate/lyric_tool_stream", json=payload)
        if response.is_success:
            return json_repair.repair_json(response.text, return_objects=True)
        # response: httpx.Response
        # async with client.stream("POST", "/generate/lyric_tool_stream", json=payload) as response:
        #     async for i in response.aiter_lines():
        #         print(i)


if __name__ == '__main__':
    # request = HaimianRequest(prompt="写一首青春一去不复返我们已不再年轻的歌")
    # arun(create_task(request))

    # task_id = "haimian-WlAPDQggva"
    # token = arun(get_next_token_for_polling(FEISHU_URL))
    # arun(get_task(task_id, token))

    arun(generate_lyric())
