import os
from typing import Optional

import yaml
from openai import OpenAI

__all__ = [
    "get_llmhelper_config",
    "set_llmhelper_default_config",
    "set_llmhelper_config",
    "get_default_llm",
    "get_default_chat_model",
    "get_default_embeddings_model",
    "get_default_rerank_model",
    "get_default_redis_stack_url",
    "get_template_engine",
    "get_llm_base_url",
    "get_llm_api_url",
    "get_llm_chat_log_name",
    "get_llm_chat_log_level",
]

OPENAI_DEFAULT_CHAT_MODEL = "qwen2-instruct"
OPENAI_DEFAULT_EMBEDDINGS_MODEL = "bge-m3"
OPENAI_DEFAULT_RERANK_MODEL = "bge-reranker-v2-m3"
LLMHELPER_DEFAULT_REDIS_STACK_URL = "redis://localhost:6379/0"
LLMHELPER_CONFIG = {}


def get_llmhelper_config():
    """获取llmehlper设置。"""
    return LLMHELPER_CONFIG


def set_llmhelper_default_config(
    api_key=None,
    base_url=None,
    chat_model=None,
    embeddings_model=None,
    rerank_model=None,
    template_engine=None,
    redis_stack_url=None,
    llm_chat_log_name=None,
    llm_chat_log_level=None,
    model=None,  # alias for chat_model
):
    """设置llmhelper全局参数默认值。

    即之前没有设定，则设置。
    如果之前已经设置，则忽略。
    """
    chat_model = chat_model or model
    if api_key:
        LLMHELPER_CONFIG.setdefault("api_key", api_key)
    if base_url:
        LLMHELPER_CONFIG.setdefault("base_url", base_url)
    if chat_model:
        LLMHELPER_CONFIG.setdefault("chat_model", chat_model)
    if embeddings_model:
        LLMHELPER_CONFIG.setdefault("embeddings_model", embeddings_model)
    if rerank_model:
        LLMHELPER_CONFIG.setdefault("rerank_model", rerank_model)
    if template_engine:
        LLMHELPER_CONFIG.setdefault("template_engine", template_engine)
    if redis_stack_url:
        LLMHELPER_CONFIG.setdefault("redis_stack_url", redis_stack_url)
    if llm_chat_log_name:
        LLMHELPER_CONFIG.setdefault("llm_chat_log_name", llm_chat_log_name)
    if llm_chat_log_level:
        LLMHELPER_CONFIG.setdefault("llm_chat_log_level", llm_chat_log_level)


def set_llmhelper_config(
    api_key=None,
    base_url=None,
    chat_model=None,
    embeddings_model=None,
    rerank_model=None,
    template_engine=None,
    redis_stack_urls=None,
    llm_chat_log_name=None,
    llm_chat_log_level=None,
    model=None,  # alias for chat_model
):
    """设置llmhelper全局参数。"""
    chat_model = chat_model or model
    if api_key:
        LLMHELPER_CONFIG["api_key"] = api_key
    if base_url:
        LLMHELPER_CONFIG["base_url"] = base_url
    if chat_model:
        LLMHELPER_CONFIG["chat_model"] = chat_model
    if embeddings_model:
        LLMHELPER_CONFIG["embeddings_model"] = embeddings_model
    if rerank_model:
        LLMHELPER_CONFIG["rerank_model"] = rerank_model
    if template_engine:
        LLMHELPER_CONFIG["template_engine"] = template_engine
    if redis_stack_urls:
        LLMHELPER_CONFIG["redis_stack_urls"] = redis_stack_urls
    if llm_chat_log_name:
        LLMHELPER_CONFIG["llm_chat_log_name"] = llm_chat_log_name
    if llm_chat_log_level:
        LLMHELPER_CONFIG["llm_chat_log_level"] = llm_chat_log_level


def get_default_llm():
    """创建系统默认的OpenAI实例。"""
    api_key = LLMHELPER_CONFIG.get("api_key", os.environ.get("OPENAI_API_KEY"))
    base_url = LLMHELPER_CONFIG.get("base_url", os.environ.get("OPENAI_BASE_URL"))
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
    )


def get_default_chat_model():
    """获取系统默认的对话模型名称。"""
    return LLMHELPER_CONFIG.get(
        "chat_model",
        os.environ.get(
            "OPENAI_CHAT_MODEL",
            os.environ.get(
                "OPENAI_MODEL",
                OPENAI_DEFAULT_CHAT_MODEL,
            ),
        ),
    )


def get_default_embeddings_model():
    """获取系统默认的嵌入模型名称。"""
    return LLMHELPER_CONFIG.get(
        "embeddings_model",
        os.environ.get(
            "OPENAI_EMBEDDINGS_MODEL",
            OPENAI_DEFAULT_EMBEDDINGS_MODEL,
        ),
    )


def get_default_rerank_model():
    """获取系统默认的嵌入模型名称。"""
    return LLMHELPER_CONFIG.get(
        "rerank_model",
        os.environ.get(
            "OPENAI_RERANK_MODEL",
            OPENAI_DEFAULT_RERANK_MODEL,
        ),
    )


def get_default_redis_stack_url(index_name=None):
    """获取系统默认的向量数据库地址。

    默认使用redis-stack作为向量数据库。
    """
    index_name = index_name or "default"
    config = LLMHELPER_CONFIG.get(
        "redis_stack_urls",
        yaml.safe_load(
            os.environ.get(
                "LLMHELPER_REDIS_STACK_URLS",
                "{}",
            )
        ),
    )
    index_parts = index_name.split(":")
    for index in range(len(index_parts)):
        config_key = ":".join(index_parts[: len(index_parts) - index])
        if config_key in config:
            return config[config_key]
    return config.get("default", LLMHELPER_DEFAULT_REDIS_STACK_URL)


def get_template_engine():
    """获取系统提示词模板引擎。"""
    return LLMHELPER_CONFIG.get("template_engine", None)


def get_llm_base_url(
    llm: Optional[OpenAI] = None,
):
    """返回规范化的OPEN AI BASE_URL。

    规范化的URL格式为：http://host/v1/。
    """
    llm = llm or get_default_llm()
    url = str(llm.base_url)
    if not url.endswith("/"):
        url += "/"
    if not url.endswith("v1/"):
        url += "v1/"
    return url


def get_llm_api_url(
    name,
    llm: Optional[OpenAI] = None,
):
    """获取OPENAI接口指定服务的URL地址。"""
    url = get_llm_base_url(llm=llm)
    return url + name


def get_llm_chat_log_name():
    return LLMHELPER_CONFIG.get(
        "get_llm_chat_log_name",
        os.environ.get(
            "LLM_CHAT_LOG_NAME",
            "llmhelper.llm",
        ),
    )


def get_llm_chat_log_level():
    return LLMHELPER_CONFIG.get(
        "llm_chat_log_level",
        os.environ.get(
            "LLM_CHAT_LOG_LEVEL",
            "warning",
        ),
    )
