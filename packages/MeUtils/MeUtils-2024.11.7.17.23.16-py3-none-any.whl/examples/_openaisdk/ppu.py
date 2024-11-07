#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ppu
# @Time         : 2024/1/9 17:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from openai import OpenAI

base_url = "https://oneapi.chatllm.vip/v1"
api_key = "sk-eEFIr6SEuegUOh1S0c8910A652A9428fAd4aD452C97631Acc"

client = OpenAI(base_url=base_url, api_key=api_key)

q = ""
data = {
    'model': 'ppu-file',
    'messages': [
        {'role': 'user', 'content': q}
    ],
    'stream': False
}

print(client.chat.completions.create(**data))
