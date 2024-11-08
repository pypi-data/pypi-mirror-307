# llmhelper

大模型辅助函数库

## 安装

```shell
pip install llmhelper
```

## 环境变量

- OPENAI_API_KEY
  - 必填
- OPENAI_BASE_URL
  - 必填
- OPENAI_CHAT_MODEL
  - 默认为：qwen2-instruct
- OPENAI_EMBEDDINGS_MODEL
  - 默认为：bge-m3
- OPENAI_RERANK_MODEL
  - 默认为：bge-reranker-v2-m3
- LLMHELPER_REDIS_STACK_URLS
  - 默认为：`{"default": "redis://localhost:3679/0"}`
  - 字典类型，表示指定索引的向量数据库地址。例如：

    ```python
    LLMHELPER_REDIS_STACK_URLS = {
      "default": "redis://localhost:6379/0",
      "kb:qa": "redis://192.168.1.31:6379/0",
      "kb:doc": "redis://192.168.1.32:6379/0",
      "ai:instruct": "redis://192.168.1.33:6379/0",
    }
    ```

## 函数列表

- exceptions
  - ParseJsonResponseError
  - ChatError
  - GetTextEmbeddingsError
  - GetRerankScoresError
  - NoneValueError
  - VectorStoreNoneValueError
  - EmbeddingsNoneValueError
  - RerankNoneValueError
- base
  - get_llmhelper_config
  - set_llmhelper_default_config
  - set_llmhelper_config
  - get_default_llm
  - get_default_chat_model
  - get_default_embeddings_model
  - get_default_rerank_model
  - get_template_engine
  - get_llm_base_url
  - get_llm_api_url
- template
  - get_template_prompt_by_django_template_engine
  - get_template_prompt_by_jinjia2
  - get_template_prompt
- llm
  - get_messages
  - parse_json_response
  - chat
  - jsonchat
  - streaming_chat
- embeddings
  - OpenAIEmbeddings
  - get_text_embeddings
- rerank
  - get_rerank_scores
- vectorestores
  - RedisVectorStore
- extra.django_vectorstore_index_model.models
  - WithVectorStoreIndex

## 版本记录

### v0.1.0

- 版本首发。

### v0.2.0

- 添加embeddings模型操作支持。
- 添加rerank模型操作支持。

### v0.3.0

- 添加向量数据库操作支持。

### v0.4.0

- 添加django_vectorstore_index_model抽象类。

### v0.5.1

#### 新增
- 添加时间增强数据集。
- RedisVectorStore.safe_insert函数自动将超长文本分块创建索引。

#### 修改
- llm.json_parse_response在遇到无法解析的响应时会抛出异常。
- chat中参数template_name建议修改为template。
- vectorstores查询空索引时异常，建议异常时返回空数组。
- get_template_prompt_by_jinjia2允许用户自定义template_root。

#### 修正

- exception类设定默认提示语的方式错误。
- llmhelper.template引擎初始化错误。

### v0.5.2

#### 修正

- 时间计算问题。
