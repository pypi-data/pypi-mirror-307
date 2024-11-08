import time
import logging
from typing import Optional

import requests

from openai import OpenAI

from .exceptions import GetRerankScoresError
from .exceptions import RerankNoneValueError
from .base import get_default_llm
from .base import get_default_rerank_model
from .base import get_llm_api_url

__all__ = [
    "get_rerank_scores",
]
_logger = logging.getLogger(__name__)


def get_rerank_scores(
    query,
    documents,
    llm: Optional[OpenAI] = None,
    model: Optional[str] = None,
    max_size: int = 1024,
):
    """返回文本相似度得分列表。"""
    if not documents:
        return []
    if query is None:
        raise RerankNoneValueError()
    for doc in documents:
        if doc is None:
            raise RerankNoneValueError()
    llm = llm or get_default_llm()
    model = model or get_default_rerank_model()
    # 如果query, documents字符串超过最大长度，则截取最前面的字符串
    if len(query) > max_size:
        _logger.warning(
            "get_rerank_scores: the query string exceeds the limit, max_size=%s, query=%s",
            max_size,
            query,
        )
        query = query[:max_size]
    fixed_documents = []
    for document in documents:
        if len(document) > max_size:
            _logger.warning(
                "get_rerank_scores: the document string exceeds the limit, max_size=%s, query=%s, document=%s",
                max_size,
                query,
                document,
            )
            document = document[:max_size]
        fixed_documents.append(document)
    # 构建并请求
    stime = time.time()
    url = get_llm_api_url("rerank", llm=llm)
    headers = {
        "Authorization": "Bearer " + llm.api_key,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "query": query,
        "documents": fixed_documents,
    }
    _logger.debug(
        "get_rerank_scores request start: url=%s, headers=%s, data=%s",
        url,
        headers,
        data,
    )
    response = requests.post(
        url,
        json=data,
        headers=headers,
    )
    _logger.debug(
        "get_rerank_scores request finished: url=%s, headers=%s, data=%s, response=%s",
        url,
        headers,
        data,
        response.text,
    )
    result = [
        x["relevance_score"]
        for x in sorted(response.json().get("results", []), key=lambda z: z["index"])
    ]
    used_time = time.time() - stime
    if not result:
        _logger.error(
            "get_rerank_scores request failed: url=%s, headers=%s, data=%s, response=%s",
            url,
            headers,
            data,
            response.text,
        )
        raise GetRerankScoresError()
    return result
