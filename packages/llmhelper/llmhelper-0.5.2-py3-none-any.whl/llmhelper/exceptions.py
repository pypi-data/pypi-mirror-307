__all__ = [
    "ParseJsonResponseError",
    "ChatError",
    "PromptOrTemplateRequired",
    "GetTextEmbeddingsError",
    "GetRerankScoresError",
    "NoneValueError",
    "VectorStoreNoneValueError",
    "EmbeddingsNoneValueError",
    "RerankNoneValueError",
]


class ParseJsonResponseError(RuntimeError):
    """LLM输出不能解析为json数据。"""

    def __init__(self, *args, **kwargs):
        args = args or ["LLM输出不能解析为json数据。"]
        super().__init__(*args, **kwargs)


class ChatError(RuntimeError):
    """大模型对话失败。"""

    def __init__(self, *args, **kwargs):
        args = args or ["大模型对话失败。"]
        super().__init__(*args, **kwargs)


class PromptOrTemplateRequired(RuntimeError):
    """prompt或template不能同时为空。"""

    def __init__(self, *args, **kwargs):
        args = args or ["prompt或template不能同时为空。"]
        super().__init__(*args, **kwargs)


class GetTextEmbeddingsError(RuntimeError):
    """获取文本向量失败。"""

    def __init__(self, *args, **kwargs):
        args = args or ["获取文本向量失败。"]
        super().__init__(*args, **kwargs)


class GetRerankScoresError(RuntimeError):
    """获取rerank得分失败。"""

    def __init__(self, *args, **kwargs):
        args = args or ["获取rerank得分失败。"]
        super().__init__(*args, **kwargs)


class NoneValueError(RuntimeError):
    """不允许None值。"""

    def __init__(self, *args, **kwargs):
        args = args or ["不允许None值。"]
        super().__init__(*args, **kwargs)


class VectorStoreNoneValueError(NoneValueError):
    """向量数据库不允许None值进行查询和插入。"""

    def __init__(self, *args, **kwargs):
        args = args or ["向量数据库不允许None值进行查询和插入。"]
        super().__init__(*args, **kwargs)


class EmbeddingsNoneValueError(NoneValueError):
    """None值无法进行向量化处理。"""

    def __init__(self, *args, **kwargs):
        args = args or ["None值无法进行向量化处理。"]
        super().__init__(*args, **kwargs)


class RerankNoneValueError(NoneValueError):
    """None值无法参与重排。"""

    def __init__(self, *args, **kwargs):
        args = args or ["None值无法参与重排。"]
        super().__init__(*args, **kwargs)
