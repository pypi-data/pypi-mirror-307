import time
import logging
from typing import List
from typing import Optional

from openai import OpenAI
from langchain_core.embeddings import Embeddings
from langchain_core.runnables.config import run_in_executor

from .exceptions import GetTextEmbeddingsError
from .base import get_default_llm
from .base import get_default_embeddings_model

__all__ = [
    "OpenAIEmbeddings",
    "get_text_embeddings",
]
_logger = logging.getLogger(__name__)


class OpenAIEmbeddings(Embeddings):
    """由于`langchain_openai.embeddings.OpenAIEmbeddings`无法兼容其它模型，需要重新实现适合国产embeddings模型的OpenAIEmbeddings用于向量数据库检索。"""

    def __init__(
        self,
        llm: Optional[OpenAI] = None,
        model: Optional[str] = None,
    ):
        self.llm: OpenAI = llm or get_default_llm()
        self.model: str = model or get_default_embeddings_model()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        _logger.info(
            "embed_documents start: model=%s, texts=%s",
            self.model,
            texts,
        )
        stime = time.time()
        response = self.llm.embeddings.create(
            input=texts,
            model=self.model,
        )
        result = [x.embedding for x in response.data]
        used_time = time.time() - stime
        _logger.info(
            "embed_documents finished: model=%s, texts=%s, result=%s, used_time=%s",
            self.model,
            texts,
            result,
            used_time,
        )
        return result

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        _logger.info(
            "embed_query start: model=%s, text=%s",
            self.model,
            text,
        )
        stime = time.time()
        response = self.llm.embeddings.create(
            input=text,
            model=self.model,
        )
        result = response.data[0].embedding
        used_time = time.time() - stime
        _logger.info(
            "embed_query finished: model=%s, text=%s, result=%s, used_time=%s",
            self.model,
            text,
            result,
            used_time,
        )
        return result

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous Embed search docs."""
        return await run_in_executor(None, self.embed_documents, texts)

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronous Embed query text."""
        return await run_in_executor(None, self.embed_query, text)


def get_text_embeddings(
    text,
    llm: Optional[OpenAI] = None,
    model: str = None,
):
    """将文字转化为向量用于向量数据库检索。向量以浮点数数组表示。"""
    llm = llm or get_default_llm()
    model = model or get_default_embeddings_model()
    _logger.info(
        "get_text_embeddings start: model=%s, text=%s",
        model,
        text,
    )
    stime = time.time()
    try:
        result = (
            llm.embeddings.create(
                input=text,
                model=model,
            )
            .data[0]
            .embedding
        )
    except Exception as error:
        _logger.warning(
            "get_text_embeddings failed: model=%s, text=%s, error=%s",
            model,
            text,
            error,
        )
        raise GetTextEmbeddingsError()
    used_time = time.time() - stime
    _logger.info(
        "get_text_embeddings finished: model=%s, text=%s, result=%s, used_time=%s",
        model,
        text,
        result,
        used_time,
    )
    return result
