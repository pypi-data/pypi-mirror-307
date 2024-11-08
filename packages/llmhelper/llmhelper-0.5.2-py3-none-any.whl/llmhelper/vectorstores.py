from typing import Optional
import logging

from zenutils import strutils
import pydantic
import redis
from redis import Redis
from langchain_community.vectorstores.redis import Redis as LangchainRedisVectorStore
from openai import OpenAI

from .exceptions import VectorStoreNoneValueError
from .base import get_default_llm
from .base import get_default_embeddings_model
from .base import get_default_rerank_model
from .base import get_default_redis_stack_url
from .embeddings import OpenAIEmbeddings
from .rerank import get_rerank_scores

__all__ = [
    "RedisVectorStoreMetaBase",
    "RedisVectorStore",
    "get_cached_vectorstore",
]
_logger = logging.getLogger(__name__)


class RedisVectorStoreMetaBase(pydantic.BaseModel):
    """Redis向量数据库meta基础类"""

    vs_uid: Optional[str] = None
    vs_page_content: Optional[str] = None
    vs_embeddings_score: Optional[float] = None
    vs_rerank_score: Optional[float] = None


class RedisVectorStore(object):
    """基于redis-stack的向量数据库。"""

    def __init__(
        self,
        index_name=None,
        redis_stack_url: str = None,
        llm: Optional[OpenAI] = None,
        model: Optional[str] = None,
        embeddings_model: Optional[str] = None,
        rerank_model: Optional[str] = None,
        max_size: Optional[int] = 1024,
    ):
        # 获取参数或获取默认参数
        self.max_size: int = max_size or 1024
        self.index_name: str = index_name
        self.redis_stack_url = redis_stack_url or get_default_redis_stack_url(
            index_name=index_name
        )
        self.embeddings_model = (
            embeddings_model or model or get_default_embeddings_model()
        )
        self.rerank_model = rerank_model or get_default_rerank_model()
        # 构建AI实例
        self.llm = llm or get_default_llm()
        self.store: LangchainRedisVectorStore = None
        self.redis: Redis = None
        # 加载实例
        self.redis = redis.from_url(self.redis_stack_url)
        self.embeddings = OpenAIEmbeddings(
            llm=self.llm,
            model=self.embeddings_model,
        )
        if index_name:
            self.store = LangchainRedisVectorStore(
                redis_url=self.redis_stack_url,
                index_name=self.index_name,
                key_prefix=self.index_name,
                embedding=self.embeddings,
            )

    def safe_insert(self, content, meta=None):
        if content is None:
            raise VectorStoreNoneValueError()
        if not self.store:
            raise RuntimeError("未指定index_name的VectorStore实例不允许新建索引")
        contents = strutils.chunk(content, self.max_size)
        if meta:
            return self.store.add_texts(contents, [meta] * len(contents))
        else:
            return self.store.add_texts(contents)

    def insert(self, content, meta=None):
        if content is None:
            raise VectorStoreNoneValueError()
        if not self.store:
            raise RuntimeError("未指定index_name的VectorStore实例不允许新建索引")
        if len(content) > self.max_size:
            _logger.warning(
                "Insert content length exceeds the limit, truncate to the limit length. size=%s, max_size=%s",
                len(content),
                self.max_size,
            )
            content = content[: self.max_size]
        if meta:
            return self.store.add_texts([content], [meta])
        else:
            return self.store.add_texts([content])

    def insert_many(self, contents, metas=None):
        for content in contents:
            if content is None:
                raise VectorStoreNoneValueError()
        if not self.store:
            raise RuntimeError("未指定index_name的VectorStore实例不允许新建索引")
        safe_contents = []
        for content in contents:
            if len(content) > self.max_size:
                _logger.warning(
                    "Insert content length exceeds the limit, truncate to the limit length. size=%s, max_size=%s",
                    len(content),
                    self.max_size,
                )
                content = content[: self.max_size]
            safe_contents.append(content)
        if metas:
            return self.store.add_texts(contents, metas)
        else:
            return self.store.add_texts(contents)

    def delete(self, uid):
        return self.redis.delete(uid)

    def delete_many(self, uids):
        if uids:
            return self.redis.delete(*uids)
        else:
            return 0

    def similarity_search_with_relevance_scores(
        self,
        query,
        k=4,
        raise_on_error=False,
        **kwargs,
    ):
        if query is None:
            _logger.exception(
                "similarity_search_with_relevance_scores got None query..."
            )
            return []
        try:
            docs = []
            for (
                doc,
                vs_embeddings_score,
            ) in self.store.similarity_search_with_relevance_scores(
                query=query, k=k, **kwargs
            ):
                docs.append(
                    {
                        "vs_uid": doc.metadata["id"],
                        "vs_page_content": doc.page_content,
                        "vs_embeddings_score": vs_embeddings_score,
                    }
                )
            for doc in docs:
                info = self.redis.hgetall(doc["vs_uid"])
                for k, v in info.items():
                    if isinstance(k, bytes):
                        k = k.decode("utf-8")
                    if k in ["content_vector"]:
                        continue
                    if isinstance(v, bytes):
                        v = v.decode("utf-8")
                    if not v:
                        v = None
                    doc[k] = v
            docs.sort(
                key=lambda x: -x["vs_embeddings_score"],
            )
            return docs
        except Exception as error:
            _logger.exception(
                "similarity_search_with_relevance_scores failed: error=%s, query=%s",
                error,
                query,
            )
            if raise_on_error:
                raise error
            else:
                return []

    def search_and_rerank(
        self,
        query,
        k=4,
        scale=4,
        reranker_score_threshold=None,
        raise_on_error=False,
        **kwargs,
    ):
        """搜索并重排

        @parameter: scale，表示一次搜索的放大位数，即一次搜索时获取的文档数量为[k*scale]个。
        """
        try:
            scale = int(scale)
            if scale < 1:
                scale = 1
            docs = self.similarity_search_with_relevance_scores(
                query=query,
                k=k * scale,
                **kwargs,
            )
            documents = [doc["vs_page_content"] for doc in docs]
            scores = get_rerank_scores(
                query=query,
                documents=documents,
                llm=self.llm,
                model=self.rerank_model,
            )
            for doc, score in zip(docs, scores):
                doc["vs_rerank_score"] = score
            docs.sort(
                key=lambda x: -x["vs_rerank_score"],
            )
            if reranker_score_threshold:
                docs = [
                    doc
                    for doc in docs
                    if doc["vs_rerank_score"] >= reranker_score_threshold
                ]
            return docs[:k]
        except Exception as error:
            _logger.exception(
                "search_and_rerank failed: error=%s, query=%s",
                error,
                query,
            )
            if raise_on_error:
                raise error
            else:
                return []

    def flush(self):
        """清空指定索引。"""
        # 删除所有索引项
        keys = self.redis.keys(self.index_name + ":*")
        if keys:
            self.redis.delete(*keys)
        # 删除索引
        indexes = self.redis.execute_command("FT._LIST")
        if indexes:
            indexes = [x.decode("utf-8") for x in indexes]
        if self.index_name in indexes:
            self.redis.execute_command(f"FT.DROPINDEX {self.index_name}")
        return len(keys)


GLOBAL_CACHED_VECTORSTORES = {}


def get_cached_vectorstore(
    index_name=None,
    redis_stack_url: str = None,
    llm: Optional[OpenAI] = None,
    model: Optional[str] = None,
    embeddings_model: Optional[str] = None,
    rerank_model: Optional[str] = None,
) -> RedisVectorStore:
    """获取缓存过的Redis向量数据库实例"""
    cache_key = f"{index_name}:{model}:{embeddings_model}:{rerank_model}"

    if index_name in GLOBAL_CACHED_VECTORSTORES:
        return GLOBAL_CACHED_VECTORSTORES[cache_key]

    rvs = RedisVectorStore(
        index_name=index_name,
        redis_stack_url=redis_stack_url,
        llm=llm,
        model=model,
        embeddings_model=embeddings_model,
        rerank_model=rerank_model,
    )
    GLOBAL_CACHED_VECTORSTORES[cache_key] = rvs
    return GLOBAL_CACHED_VECTORSTORES[cache_key]
