#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2024/6/7 17:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from openai.types.chat import ChatCompletion as _ChatCompletion, ChatCompletionChunk as _ChatCompletionChunk
from openai.types.chat.chat_completion import Choice as _Choice, ChatCompletionMessage as _ChatCompletionMessage, \
    CompletionUsage as _CompletionUsage
from openai.types.chat.chat_completion_chunk import Choice as _ChunkChoice, ChoiceDelta
from openai._types import FileTypes
from openai.types import ImagesResponse as _ImagesResponse
from openai.types.shared_params import FunctionDefinition
from openai.types.chat import ChatCompletionToolParam

TOOLS = [
    {"type": "web_browser"},
    {"type": "code_interpreter"},
    {"type": "drawing_tool"},
]

BACKUP_MODEL = os.getenv("BACKUP_MODEL", "glm-4")


class Tool(BaseModel):
    # {"id": "", "type": "web_browser", "function": {}} => {"type": "web_browser", "function": None}
    function: Optional[dict] = None  # FunctionDefinition
    type: str

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.function = self.function or None


class CompletionUsage(_CompletionUsage):
    prompt_tokens: int = 1000
    completion_tokens: int = 1000
    total_tokens: int = 2000


class ChatCompletionMessage(_ChatCompletionMessage):
    role: Literal["assistant"] = "assistant"
    """The role of the author of this message."""


class Choice(_Choice):
    index: int = 0
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"] = None


class ChatCompletion(_ChatCompletion):
    id: str = Field(default_factory=shortuuid.random)
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion"
    usage: CompletionUsage = CompletionUsage()


class ChunkChoice(_ChunkChoice):
    index: int = 0


class ChatCompletionChunk(_ChatCompletionChunk):
    id: str = Field(default_factory=shortuuid.random)
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = "chat.completion.chunk"


chat_completion = ChatCompletion(
    choices=[Choice(message=ChatCompletionMessage(content=""))]
)
chat_completion_chunk = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(content=""))]
)
chat_completion_chunk_stop = ChatCompletionChunk(
    choices=[ChunkChoice(delta=ChoiceDelta(content=""), finish_reason="stop")]
)


# chat_completion.choices[0].message.content = "*"
# chat_completion_chunk.choices[0].delta.content = "*"


class ChatCompletionRequest(BaseModel):
    """
    prompt_filter_result.content_filter_results
    choice.content_filter_results

    todo: ['messages', 'model', 'frequency_penalty', 'function_call', 'functions', 'logit_bias', 'logprobs', 'max_tokens', 'n', 'presence_penalty', 'response_format', 'seed', 'stop', 'stream', 'temperature', 'tool_choice', 'tools', 'top_logprobs', 'top_p', 'user']
    """
    model: str = ''  # "gpt-3.5-turbo-file-id"

    # [{'role': 'user', 'content': 'hi'}]
    # [{'role': 'user', 'content':  [{"type": "text", "text": ""}]]
    # [{'role': 'user', 'content': [{"type": "image_url", "image_url": ""}]}] # 也兼容文件
    # [{'role': 'user', 'content': [{"type": "image_url", "image_url": {"url": ""}}]}] # 也兼容文件
    # [{'role': 'user', 'content':  [{"type": "file", "file_url": ""}]]
    messages: Optional[List[Dict[str, Any]]] = None

    top_p: Optional[float] = 0.7
    temperature: Optional[float] = 0.7

    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    stream: Optional[bool] = False
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    user: Optional[str] = None

    # tools
    response_format: Optional[Any] = None
    function_call: Optional[Any] = None
    functions: Optional[Any] = None
    tools: Optional[List[Tool]] = None  # 为了兼容 oneapi
    tool_choice: Optional[Any] = None
    parallel_tool_calls: Optional[Any] = None

    # 拓展字段
    last_content: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if isinstance((last_content := self.messages[-1].get('content')), list):  # 多模态
        #     self.last_content = last_content
        self.messages = self.messages or [{'role': 'user', 'content': 'hi'}]
        self.last_content: str = self.messages[-1].get("content", "")  # 大部分时间等价于user_content

        # 兼容 glm-4
        self.top_p = self.top_p is not None and np.clip(self.top_p, 0.01, 0.99)
        self.temperature = self.temperature is not None and np.clip(self.temperature, 0.01, 0.99)

        if self.model.startswith('o1'):
            self.top_p = 1
            self.temperature = 1

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "hi"
                        }
                    ],
                    "stream": False
                },

                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "请按照下面标题，写一篇400字的文章\n王志文说，一个不熟的人找你借饯，说明他已经把熟人借遍了。除非你不想要了，否则不要借"
                        }
                    ],
                    "stream": False
                },

                # url
                {
                    "model": "url-gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": "总结一下https://mp.weixin.qq.com/s/Otl45GViytuAYPZw3m7q9w"
                        }
                    ],
                    "stream": False
                },

                # rag
                {
                    "messages": [
                        {
                            "content": "分别总结这两篇文章",
                            "role": "user"
                        }
                    ],
                    "model": "gpt-3.5-turbo",
                    "stream": False,
                    "file_ids": ["cn2a0s83r07am0knkeag", "cn2a3ralnl9crebipv4g"]
                }

            ]
        }
    }


class ImageRequest(BaseModel):
    prompt: str

    model: str = 'pro'
    n: int = 1
    quality: str = 'hd'
    response_format: Literal["url", "b64_json"] = "url"
    size: str = '1024x1024'  # 测试默认值
    # sd: 768x1024 1024x576
    style: Union[str, Literal["vivid", "natural"]] = "natural"

    # 拓展参数
    guidance_scale: float = Field(default=5, alias="guidance")

    # https://blog.csdn.net/qq_37508554/article/details/133975130
    num_inference_steps: int = Field(default=20, alias="steps")

    seed: Optional[int] = None
    negative_prompt: Optional[str] = None

    # 拓展字段
    nsfw_level: str = "2"  # 小于等于6
    url: Optional[str] = None
    image: Optional[str] = None  # url/base64

    prompt_enhancement: bool = False

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.model.lower().__contains__('stabilityai'):
            self.num_inference_steps = 25
            self.guidance_scale = 7.5
        elif any(i in self.model.lower() for i in {"turbo", "lightning"}):
            self.num_inference_steps = 4
            self.guidance_scale = 1

    class Config:
        # frozen = True
        populate_by_name = True

        json_schema_extra = {
            "examples": [
                {
                    "model": "stable-diffusion-3-medium",  # sd3
                    "prompt": "画条狗",
                },
            ]
        }


class ImagesResponse(_ImagesResponse):
    created: int = Field(default_factory=lambda: int(time.time()))


class TTSRequest(BaseModel):
    input: str
    model: Optional[Union[str, Literal["tts-1", "tts-1-hd"]]] = 'tts'
    voice: Optional[Union[str, Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]]] = ""
    speed: Optional[float] = None

    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3"

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "model": "tts-1",
                    "voice": "7f92f8afb8ec43bf81429cc1c9199cb1",
                    "input": "你好，我是AI助手",
                }
            ]
        }


class STTRequest(BaseModel):  # ASR
    file: Union[bytes, str]
    model: str = "whisper-1"
    prompt: Optional[str] = None
    response_format: Literal["text", "srt", "verbose_json", "vtt"] = "text"
    language: Optional[str] = None
    temperature: Optional[float] = None
    timestamp_granularities: Optional[List[Literal["word", "segment"]]] = None


if __name__ == '__main__':
    pass


    # print(ChatCompletion(choices=[Choice(message=ChatCompletionMessage(content="ChatCompletion"))]))
    # print(ChatCompletionChunk(choices=[ChunkChoice(delta=ChoiceDelta(content="ChatCompletionChunk"))]))
    #
    # print(chat_completion)
    # print(chat_completion_chunk)
    # print(chat_completion_chunk_stop)

    # print(ChatCompletionRequest(temperature=0, top_p=1))
    # print(ChatCompletionRequest(temperature=1, top_p=0))

    # file = UploadFile(open("/Users/betterme/PycharmProjects/AI/ChatLLM/chatllm/api/routers/cocopilot.py", "rb"))
    # #
    # print(AudioRequest(file=file))
    # print(ImagesResponse(data=[]))
    # print(ChatCompletionRequest(tools=[
    #     {
    #         # "id": "",
    #         "type": "web_browser",
    #         # "function": {}
    #     }
    # ],
    #     max_tokens=None,
    # ).model_dump_json(indent=4))

    # 创建实例
    # req1 = ImageRequest(guidance_scale=5.0, prompt="画条狗")
    # req2 = ImageRequest(guidance=5.0, prompt="画条狗")
    #
    # print(req1.guidance_scale)  # 输出: 5.0
    # print(req2.guidance_scale)  # 输出: 5.0
    #
    # # 两种方式都可以访问这个值
    # print(req1.model_dump())  # 输出: {'guidance_scale': 5.0}
    # print(req1.model_dump(by_alias=True))  # 输出: {'guidance': 5.0}

    class A(BaseModel):
        n: int = Field(1, ge=1, le=0)


    print(A(n=11))
