import jinja2
import re
import inspect
from functools import wraps
from copy import deepcopy
from typing import Literal, Callable
import pathlib

_root = pathlib.Path(__file__).parent.parent
_sys_ptn = re.compile("^System:([^|]*)(\|\|)?", flags=re.RegexFlag.IGNORECASE)
_user_ptn = re.compile("User:([^|]*)(\|\|)?", flags=re.RegexFlag.IGNORECASE)
_assistant_ptn = re.compile("Assistant:([^|]*)(\|\|)?", flags=re.RegexFlag.IGNORECASE)
_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(f"{_root}/templates"),
    autoescape=jinja2.select_autoescape(enabled_extensions=("jinja2",)),
)


def build_message(role: Literal["system", "user", "assitant"], content):
    return {"role": role, "content": content}


def _get_content_text(content_dict: dict):
    _content_dict = deepcopy(content_dict)
    if isinstance(content_dict["content"], re.Match):
        _content_dict["content"] = content_dict["content"].group(1).strip("\n ")
    return _content_dict


def ai_template(func: Callable | None = None, post_process: Callable | None = None):
    def outer_wrapper(wrap_func: Callable):
        @wraps(wrap_func)
        def wrapper(*args, **kwargs) -> list[dict]:
            doc_str = inspect.getdoc(wrap_func)
            if doc_str is None:
                raw_prompt = _env.get_template(f"{wrap_func.__name__}.jinja2").render(
                    **kwargs
                )
            else:
                raw_prompt = jinja2.Template(doc_str).render(**kwargs)
            match_messages: list[dict] = []
            sys_content = _sys_ptn.search(raw_prompt)
            user_content = _user_ptn.search(raw_prompt)
            assistant_content = _assistant_ptn.search(raw_prompt)

            if sys_content:
                match_messages.append(build_message("system", sys_content))

            if user_content:
                match_messages.append(build_message("user", user_content))
            if assistant_content:
                match_messages.append(build_message("assitant", assistant_content))

            match_messages.sort(key=lambda x: x["content"].span()[0])
            messages = list(map(_get_content_text, match_messages))
            if post_process:
                messages = post_process(messages)
            return messages

        return wrapper

    if func is None:
        return outer_wrapper
    return outer_wrapper(func)


# @ai_template
# def plain_translate(*, content: str, target: str, source: str | None = None):
#     """System: {% if source is defined %}Source Language: {{source}}{% endif %}
#     Task: Translate the user provided content into {{target}}||
#     User: {{content}}"""
#     ...


# @ai_template
# def rich_translate(*, content: str, target: str, source: str | None = None):
#     """System: {% if source is defined %}Source Language: {{source}}{% endif %}
#     Task: Translate the user provided content into {{target}}||
#     Assistant: Hello there!||
#     User: {{content}}"""
#     ...
