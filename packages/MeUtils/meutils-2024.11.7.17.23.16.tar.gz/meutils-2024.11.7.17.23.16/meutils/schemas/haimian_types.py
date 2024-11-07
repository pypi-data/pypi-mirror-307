#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : haimian_types
# @Time         : 2024/8/2 15:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class HaimianRequest(BaseModel):
    prompt: str
    generate_cover: bool = False
    generate_title: bool = False
    batch_size: int = 1

    # 自定义模式
    lyrics: str = None
    genre: str = None
    mood: str = None
    gender: str = "Female"
    title: str = ""
