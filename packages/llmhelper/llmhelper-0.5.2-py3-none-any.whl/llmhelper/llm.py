import re
import os
import json
import logging

from typing import List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple

import yaml
from openai import OpenAI

from .exceptions import ChatError
from .exceptions import PromptOrTemplateRequired
from .base import get_default_llm
from .base import get_default_chat_model
from .base import get_llm_chat_log_name
from .base import get_llm_chat_log_level
from .template import get_template_prompt
from .template import get_template_prompt_by_jinjia2

__all__ = [
    "get_messages",
    "parse_json_response",
    "chat",
    "jsonchat",
    "streaming_chat",
    "chat_with_extra_data",
    "jsonchat_with_extra_data",
    "streaming_chat_with_extra_data",
]
_logger = logging.getLogger(__name__)
_llm_chat_logger = logging.getLogger(get_llm_chat_log_name())
_llm_chat_log_level = get_llm_chat_log_level()


def get_messages(
    prompt: Union[str, List[Dict[str, str]]],
    histories: Optional[List[Tuple[str, str]]] = None,
    system_prompt: str = "You are helpful assistance.",
):
    """将文字版的prompt转化为messages数组。

    @parameter histories: 问答记录记录:
    ```
        histories = [
            ("question1", "answer1"),
            ("question2", "answer2"),
        ]
    ```
    """
    histories = histories or []
    history_messages = []
    for history in histories:
        history_messages.append({"role": "user", "content": history[0]})
        history_messages.append({"role": "assistant", "content": history[1]})

    if isinstance(prompt, str):
        result = [
            {"role": "system", "content": system_prompt},
        ]
        result += history_messages
        result += [
            {"role": "user", "content": prompt},
        ]
    else:
        result = prompt[:1] + history_messages + prompt[1:]
    return result


def _fix_json_escape(match):
    return "\\" + match.group(0)


def parse_json_response(response_text, default=None):
    """把LLM输出解析为json数据。

    如果LLM响应的不是有效的json数据，则抛出`ParseJsonResponseError`异常。
    """
    # 标准json输出，并且没有其它多余输出
    if response_text.startswith("```json"):
        response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
    # s1: 尝试json反序列化
    try:
        return yaml.safe_load(response_text)
    except:
        pass
    # s2: 有多余输出，但有多个```json\nxxx\n```JSON块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    # s3: 有多余输出，但有多个```\nxxx\n```代码块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    # 复杂场景下，字符串没有转义，尝试修正
    response_text = re.sub('\\\\[^\\\\nrt\\"]', _fix_json_escape, response_text)
    # s4: 尝试json反序列化
    try:
        return yaml.safe_load(response_text)
    except:
        pass
    # s5: 有多余输出，但有多个```json\nxxx\n```JSON块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    # s6: 有多余输出，但有多个```\nxxx\n```代码块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    # 所有尝试都失败
    _logger.warning(
        "parse_json_response failed: response_text=%s",
        response_text,
    )
    return default


def chat(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    template: Optional[str] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    template_engine=None,
    template_root: Optional[str] = None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    **context,
):
    """基于提示词模板的对话。"""
    if (prompt is None) and (template is None):
        raise PromptOrTemplateRequired()
    original_prompt = prompt
    llm = llm or get_default_llm()
    model = model or get_default_chat_model()
    if template:
        prompt = get_template_prompt(
            template=template,
            prompt=prompt,
            template_engine=template_engine,
            template_root=template_root,
            **context,
        )
    try:
        messages = get_messages(
            prompt=prompt,
            histories=histories,
            system_prompt=system_prompt,
        )
        result = llm.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
        )
        try:
            logdata = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False,
                "output": result.model_dump(),
            }
            getattr(_llm_chat_logger, _llm_chat_log_level)(
                json.dumps(logdata, ensure_ascii=False)
            )
        except Exception as error:
            _logger.exception(
                "_llm_input_output_logger failed: error=%s",
                error,
            )
        return result.choices[0].message.content
    except Exception as error:
        _logger.error(
            "chat failed: model=%s, llm=%s, original_prompt=%s, prompt=%s, histories=%s, temperature=%s, max_tokens=%s, error=%s",
            model,
            llm,
            original_prompt,
            prompt,
            histories,
            temperature,
            max_tokens,
            error,
        )
        raise ChatError()


def jsonchat(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    template: Optional[str] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    template_engine=None,
    template_root: Optional[str] = None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    **context,
):
    """基于提示词模板的对话。"""
    response_text = chat(
        prompt=prompt,
        histories=histories,
        template=template,
        model=model,
        llm=llm,
        template_engine=template_engine,
        system_prompt=system_prompt,
        template_root=template_root,
        temperature=temperature,
        max_tokens=max_tokens,
        **context,
    )
    return parse_json_response(
        response_text=response_text,
    )


def streaming_chat(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    template: Optional[str] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    template_engine=None,
    template_root: Optional[str] = None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    **context,
):
    """流式AI对话，返回响应文字内容。

    过滤掉空白块。
    """
    if (prompt is None) and (template is None):
        raise PromptOrTemplateRequired()
    original_prompt = prompt
    llm = llm or get_default_llm()
    model = model or get_default_chat_model()
    if template and isinstance(prompt, str):
        prompt = get_template_prompt(
            template=template,
            prompt=prompt,
            template_engine=template_engine,
            template_root=template_root,
            **context,
        )
    try:
        messages = get_messages(
            prompt=prompt,
            histories=histories,
            system_prompt=system_prompt,
        )
        outputs = []
        result = llm.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in result:
            empty_flag = False
            try:
                if not chunk.choices[0].delta.content:
                    empty_flag = True
            except:
                pass
            if not empty_flag:
                output = chunk.model_dump()
                yield output
                outputs.append(output)
        try:
            logdata = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
                "outputs": outputs,
            }
            getattr(_llm_chat_logger, _llm_chat_log_level)(
                json.dumps(logdata, ensure_ascii=False)
            )
        except Exception as error:
            _logger.exception(
                "_llm_input_output_logger failed: error=%s",
                error,
            )
    except Exception as error:
        _logger.error(
            "streaming_chat failed: model=%s, llm=%s, original_prompt=%s, prompt=%s, histories=%s, temperature=%s, max_tokens=%s, error=%s",
            model,
            llm,
            original_prompt,
            prompt,
            histories,
            temperature,
            max_tokens,
            error,
        )
        raise ChatError()


def chat_with_extra_data(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    extra_data: Optional[List[str]] = None,
    **context,
):
    return chat(
        prompt=prompt,
        histories=histories,
        model=model,
        llm=llm,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        template="chat_with_extra_data.md",
        template_engine=get_template_prompt_by_jinjia2,
        template_root=os.path.join(os.path.dirname(__file__), "templates"),
        extra_data=extra_data,
        **context,
    )


def jsonchat_with_extra_data(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    extra_data: Optional[List[str]] = None,
    **context,
):
    return jsonchat(
        prompt=prompt,
        histories=histories,
        model=model,
        llm=llm,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        template="chat_with_extra_data.md",
        template_engine=get_template_prompt_by_jinjia2,
        template_root=os.path.join(os.path.dirname(__file__), "templates"),
        extra_data=extra_data,
        **context,
    )


def streaming_chat_with_extra_data(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    template: Optional[str] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    template_engine=None,
    template_root: Optional[str] = None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    **context,
):
    for chunk in streaming_chat(
        prompt=prompt,
        histories=histories,
        model=model,
        llm=llm,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        template="chat_with_extra_data.md",
        template_engine=get_template_prompt_by_jinjia2,
        template_root=os.path.join(os.path.dirname(__file__), "templates"),
        extra_data=extra_data,
        **context,
    ):
        yield chunk
