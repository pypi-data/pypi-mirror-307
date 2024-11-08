#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : channel
# @Time         : 2024/10/9 18:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.schemas.oneapi_types import BASE_URL


async def edit_channel(models, token: Optional[str] = None):
    token = token or os.environ.get("CHATFIRE_ONEAPI_TOKEN")

    models = ','.join(filter(lambda model: model.startswith(("api", "official-api", "ppu")), models))
    payload = {
        "id": 289,
        "type": 1,
        "key": "",
        "openai_organization": "",
        "test_model": "ppu",
        "status": 1,
        "name": "按次收费 ppu",
        "weight": 100,
        "created_time": 1717038002,
        "test_time": 1728212103,
        "response_time": 9,
        "base_url": "https://ppu.chatfire.cn",
        "other": "",
        "balance": 0,
        "balance_updated_time": 1726793323,
        "models": models,
        "group": "chatfire,default,2B,ssvip,svip,vip,国产",
        "used_quota": 4220352321,
        "model_mapping": "",
        "status_code_mapping": "",
        "priority": 666,
        "auto_ban": 0,
        "other_info": "",
        "groups": [
            "chatfire",
            "default",
            "2B",
            "ssvip",
            "svip",
            "vip",
            "国产"
        ]
    }
    headers = {
        'authorization': f'Bearer {token}'
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30) as client:
        response = await client.put("/api/channel/", json=payload)
        response.raise_for_status()
        if response.is_success:
            return response.json()
