#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat_tune
# @Time         : 2024/9/20 20:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
#  curl -X POST "https://any2chat.chatfire.cn/tune/v1/chat/completions" \
# -H "Authorization: Bearer sk-tune-0UkSny4Fe7ouhF3GPI0lIAKIAj7B2kkJmOV" \
# -H "Content-Type: application/json" \
# -d '{
#   "temperature": 0.8,
#   "messages": [
#   {
#     "role": "user",
#     "content": "1+1"
#   }
# ],
#   "model": "anthropic/claude-3.5-sonnet",
#   "stream": true,
#   "frequency_penalty": 0,
#   "max_tokens": 900
# }'


from meutils.pipe import *
from openai import OpenAI

base_url = "https://any2chat.chatfire.cn/tune/v1"
api_key = "sk-tune-0UkSny4Fe7ouhF3GPI0lIAKIAj7B2kkJmOV"
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

completion = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    # model="openai/gpt-4o-mini",
    # model="openai/gpt-4o",
    # model="anthropic/claude-3.5-sonnet",

    messages=[
        {"role": "user", "content": "1+1"},
    ],
    # max_tokens=10
)

print(completion)
