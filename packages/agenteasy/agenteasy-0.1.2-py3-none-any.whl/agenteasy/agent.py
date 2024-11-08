import openai
from openai.types.chat import ChatCompletionMessageParam

try:
    from agenteasy.models import AIModelBase
except:
    from .models import AIModelBase
from asyncio import Semaphore
import inspect
import tiktoken
from functools import wraps
from .logutil import logger


def deco_storage(wrap_func=None, *, ex=129600):
    """用redis保存生成数据，同时控制内容过期时间"""

    def outer_wrapper(func):

        @wraps(func)
        async def cowrapper(*args, **kwargs):
            # 检测是否存在redis，如果存在一律直接返回结果，不存在再生成
            sig = inspect.signature(func)
            bind_args = sig.bind(*args, **kwargs)
            bind_args.apply_defaults()

            _msgs = bind_args.kwargs.get("messages")
            if not bind_args.args[0].storage_backend:
                result = await func(*bind_args.args, **bind_args.kwargs)
                return result

            # 请求的内容是否已经存在
            content = bind_args.args[0].storage_backend.get(str(_msgs))
            _use_cache = bind_args.kwargs.get("use_backend_cache")
            if content and _use_cache:
                logger.debug(f"content exist, use redis cache")
                return content.decode("utf-8")

            result = await func(*bind_args.args, **bind_args.kwargs)
            bind_args.args[0].storage_backend.set(str(_msgs), result, ex=ex)
            return result

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检测是否存在redis，如果存在一律直接返回结果，不存在再生成
            sig = inspect.signature(func)
            bind_args = sig.bind(*args, **kwargs)
            bind_args.apply_defaults()

            _msgs = bind_args.kwargs.get("messages")
            if not bind_args.args[0].storage_backend:
                result = func(*bind_args.args, **bind_args.kwargs)
                return result

            # 请求的内容是否已经存在
            content = bind_args.args[0].storage_backend.get(str(_msgs))
            _use_cache = bind_args.kwargs.get("use_backend_cache")
            if content and _use_cache:
                logger.debug(f"content exist, use redis cache")
                return content.decode("utf-8")

            result = func(*bind_args.args, **bind_args.kwargs)
            bind_args.args[0].storage_backend.set(str(_msgs), result, ex=ex)
            return result

        if inspect.iscoroutinefunction(func):
            return cowrapper
        return wrapper

    if wrap_func is None:
        return outer_wrapper
    return outer_wrapper(wrap_func)


def deco_token_limit(wrap_func):
    @wraps(wrap_func)
    async def cowrapper(*args, **kwargs):
        msg_num = count_tokens_from_messages(
            args[0]._token_counter, kwargs.get("messages")
        )
        logger.debug(f"message token estimate: {msg_num}")
        if msg_num > args[0].ai_model.tokens_limit:
            raise ValueError(
                f"{msg_num} tokens exceed the limit of {args[0].ai_model.tokens_limit}"
            )
        result = await wrap_func(*args, **kwargs)
        return result

    @wraps(wrap_func)
    def wrapper(*args, **kwargs):
        msg_num = count_tokens_from_messages(
            args[0]._token_counter, kwargs.get("messages")
        )
        logger.debug(f"message token estimate: {msg_num}")
        if msg_num > args[0].ai_model.tokens_limit:
            raise ValueError(
                f"{msg_num} tokens exceed the limit of {args[0].ai_model.tokens_limit}"
            )
        result = wrap_func(*args, **kwargs)
        return result

    if inspect.iscoroutinefunction(wrap_func):
        return cowrapper
    return wrapper


def count_tokens_from_messages(token_counter, messages):
    num_tokens = 0
    for message in messages:
        num_tokens += (
            4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        )
        for key, value in message.items():
            num_tokens += len(token_counter.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


class AIAgent:
    def __init__(
        self,
        ai_model: AIModelBase,
        model_async: bool = False,
        semaphore_num: int = 3,
        **model_kwargs,
    ) -> None:
        self.ai_model = ai_model
        self.client = None
        self.aclient = None
        self._semaphore: Semaphore | None = None
        self._store_backend = None
        self._token_counter = tiktoken.get_encoding(self.ai_model.token_counter)
        self.semaphore_num = semaphore_num
        if model_async:
            self.create_aclient(**model_kwargs)
        else:
            self.create_client(**model_kwargs)

    def __del__(self):
        if self._store_backend:
            self._store_backend.close()

    @property
    def storage_backend(self):
        return self._store_backend

    def create_client(self, **kwargs):
        logger.debug(f"client {self.ai_model.model} created")
        self.client = openai.OpenAI(
            api_key=self.ai_model.api_key, base_url=self.ai_model.base_url, **kwargs
        )

    def create_aclient(self, **kwargs):
        logger.debug(f"async client {self.ai_model.model} created")
        self.aclient = openai.AsyncClient(
            api_key=self.ai_model.api_key, base_url=self.ai_model.base_url, **kwargs
        )
        self._semaphore = Semaphore(self.semaphore_num)

    @deco_storage
    @deco_token_limit
    def generate(
        self,
        *,
        messages: list[ChatCompletionMessageParam],
        use_backend_cache=True,
        auto_continue=True,
        raw_completion=False,
        **kwargs,
    ):
        logger.debug(f"message:{messages}")
        try:
            completion = self.client.chat.completions.create(
                messages=messages,
                model=self.ai_model.model,
                temperature=self.ai_model.temperature,
                stream=False,
                **kwargs,
            )
            result = completion.choices[0].message.content
            logger.debug(completion)
            if raw_completion:
                return completion
            match completion.choices[0].finish_reason:
                case "stop":
                    return result
                case "length":
                    if not auto_continue:
                        return result
                    _msgs = [
                        *messages,
                        {"role": "assistant", "content": result},
                    ]
                    result += self.generate(
                        messages=_msgs,
                        use_backend_cache=use_backend_cache,
                        auto_continue=auto_continue,
                        **kwargs,
                    )
                    return result
                case "tool_calls":
                    ...
                case "function_call":
                    ...
                case "content_filter":
                    ...
                case _:
                    pass
        except Exception as e:
            raise ValueError(e)
        return result

    @deco_storage
    @deco_token_limit
    async def agenerate(
        self,
        *,
        messages: list[ChatCompletionMessageParam],
        use_backend_cache=True,
        auto_continue=True,
        raw_completion=False,
        **kwargs,
    ):
        logger.debug(f"message:{messages}")
        async with self._semaphore:
            try:
                completion = await self.aclient.chat.completions.create(
                    messages=messages,
                    model=self.ai_model.model,
                    temperature=self.ai_model.temperature,
                    stream=False,
                    **kwargs,
                )
                result = completion.choices[0].message.content
                logger.debug(completion)
                if raw_completion:
                    return completion
                match completion.choices[0].finish_reason:
                    case "stop":
                        return result
                    case "length":
                        if not auto_continue:
                            return result
                        _msgs = [
                            *messages,
                            {"role": "assistant", "content": result},
                        ]
                        result += await self.agenerate(
                            messages=_msgs,
                            use_backend_cache=use_backend_cache,
                            auto_continue=auto_continue,
                            **kwargs,
                        )
                        return result
                    case "tool_calls":
                        ...
                    case "function_call":
                        ...
                    case "content_filter":
                        ...
                    case _:
                        pass
            except Exception as e:
                raise ValueError(e)
            return result
