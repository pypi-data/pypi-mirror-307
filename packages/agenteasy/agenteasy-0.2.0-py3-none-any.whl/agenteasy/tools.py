import inspect
from pydantic import create_model
import openai
from functools import wraps
from typing import Callable


def craft_tool_from_function(func):
    # 获取函数签名
    signature = inspect.signature(func)

    # 提取参数信息，构造 Pydantic 类的字段类型字典
    fields = {}
    for name, param in signature.parameters.items():
        if param.default is param.empty:
            fields[name] = (param.annotation, ...)
        else:
            fields[name] = (param.annotation, param.default)

    # 获取函数文档字符串作为类的文档字符串
    docstring = func.__doc__

    # 动态创建 Pydantic 模型
    model = create_model(func.__name__, __doc__=docstring, **fields)
    tool = openai.pydantic_function_tool(model)
    return tool


def batch_make_tools(funcs) -> list[dict]:
    tools = []
    for func in funcs:
        if isinstance(func, dict):
            tools.append(func)
        elif isinstance(func, Callable):
            tools.append(craft_tool_from_function(func))
        else:
            raise ValueError(f"Wrong type of parameters: {func.__name__}:{type(func)}")
    return tools


def call_tool(tool_call_id, func_name, func_list: list, **kwargs):
    for func in func_list:
        if func.__name__ == func_name:
            return {
                "tool_call_id": tool_call_id,
                "role": "tool",
                "content": str(func(**kwargs)),
            }
