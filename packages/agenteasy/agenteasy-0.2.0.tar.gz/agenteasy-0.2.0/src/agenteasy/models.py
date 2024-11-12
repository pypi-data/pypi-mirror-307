from pydantic import BaseModel, HttpUrl, Field
from typing import Literal

__all__ = ["DeepSeek", "GPT", "QWen", "Moonshot"]


class AIModelBase(BaseModel):
    model: str
    base_url: HttpUrl | None = None
    api_key: str | None = Field(
        pattern="^sk-", description="should start with sk", default=None
    )
    temperature: float = Field(
        ge=0.0, le=2.0, description="float between 0 to 2", default=1.0
    )
    tokens_limit: int = 8192
    token_counter: str = "cl100k_base"


class DeepSeek(AIModelBase):
    model: Literal["deepseek-chat", "deepseek-coder"] = "deepseek-chat"
    base_url: HttpUrl | None = "https://api.deepseek.com"
    tokens_limit: int = 32000


class QWen(AIModelBase):
    model: Literal["qwen-long", "qwen-turbo", "qwen-plus", "qwen-max"] = "qwen-long"
    base_url: HttpUrl | None = "https://dashscope.aliyuncs.com/compatible-mode/v1"


class GPT(AIModelBase):
    model: Literal["gpt-4o", "gpt-3.5-turbo"] = "gpt-4o"


class Moonshot(AIModelBase):
    model: Literal["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"] = (
        "moonshot-v1-8k"
    )
    base_url: HttpUrl | None = "https://api.moonshot.cn/v1"
