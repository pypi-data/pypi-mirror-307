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
from typing import TypeVar
from .tools import batch_make_tools, call_tool
import json

T = TypeVar("T")


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
            num_tokens += len(token_counter.encode(str(value)))
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
        if "tools" in kwargs:
            tool_funcs = kwargs.get("tools")
            kwargs.update({"tools": batch_make_tools(tool_funcs)})
        try:
            completion = self.client.chat.completions.create(
                messages=messages,
                model=self.ai_model.model,
                temperature=self.ai_model.temperature,
                stream=False,
                **kwargs,
            )
            logger.debug(completion)
            if raw_completion:
                return completion
            result = completion.choices[0].message.content

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
                    tool_call_id = completion.choices[0].message.tool_calls[0].id
                    tool_name = (
                        completion.choices[0].message.tool_calls[0].function.name
                    )
                    tool_args = json.loads(
                        completion.choices[0].message.tool_calls[0].function.arguments
                    )
                    tool_message = call_tool(
                        tool_call_id, tool_name, func_list=tool_funcs, **tool_args
                    )
                    messages.append(
                        completion.choices[0].message.model_dump(exclude_none=True)
                    )
                    messages.append(tool_message)
                    result = self.generate(
                        messages=messages,
                        use_backend_cache=use_backend_cache,
                        auto_continue=auto_continue,
                        **kwargs,
                    )
                    return result
                case "function_call":
                    func_call_id = completion.choices[0].message.tool_calls[0].id
                    func_name = completion.choices[0].message.tool_calls[0].function
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
                logger.debug(completion)
                if raw_completion:
                    return completion
                result = completion.choices[0].message.content
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

    @deco_storage
    @deco_token_limit
    def beta_generate(
        self,
        *,
        messages: list[ChatCompletionMessageParam],
        response_format: T,
        extract_property: str | None = None,
        use_backend_cache=True,
        auto_continue=True,
        raw_completion=False,
        **kwargs,
    ):
        logger.debug(f"message:{messages}")
        try:
            completion = self.client.beta.chat.completions.parse(
                messages=messages,
                model=self.ai_model.model,
                temperature=self.ai_model.temperature,
                response_format=response_format,
                **kwargs,
            )
            if raw_completion:
                return completion
            logger.debug(completion)
            parsed_model: T = completion.choices[0].message.parsed
            if extract_property is None:
                return parsed_model
            result: str = getattr(parsed_model, extract_property)
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
                    result += self.beta_generate(
                        messages=_msgs,
                        response_format=response_format,
                        extract_property=extract_property,
                        use_backend_cache=use_backend_cache,
                        auto_continue=auto_continue,
                        **kwargs,
                    )
                    return result
                case "tool_calls":
                    ...
                case "function_call":
                    func_call_id = completion.choices[0].message.tool_calls[0].id
                    func_name = completion.choices[0].message.tool_calls[0].function
                case "content_filter":
                    ...
                case _:
                    pass
        except Exception as e:
            raise ValueError(e)
        return result

    @deco_storage
    @deco_token_limit
    async def beta_agenerate(
        self,
        *,
        messages: list[ChatCompletionMessageParam],
        response_format: T,
        extract_property: str | None = None,
        use_backend_cache=True,
        auto_continue=True,
        raw_completion=False,
        **kwargs,
    ):
        logger.debug(f"message:{messages}")
        async with self._semaphore:
            try:
                completion = await self.aclient.chat.completions.parse(
                    messages=messages,
                    model=self.ai_model.model,
                    temperature=self.ai_model.temperature,
                    response_format=response_format,
                    **kwargs,
                )
                if raw_completion:
                    return completion
                logger.debug(completion)
                parsed_model: T = completion.choices[0].message.parsed
                if extract_property is None:
                    return parsed_model
                result: str = getattr(parsed_model, extract_property)
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
                            response_format=response_format,
                            extract_property=extract_property,
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
