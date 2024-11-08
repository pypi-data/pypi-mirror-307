import logging
from typing import Dict
from typing import List

import yaml

from django.db import models
from django.db import transaction
from llmhelper.vectorstores import get_cached_vectorstore

__all__ = [
    "WithVectorStoreIndex",
]
_logger = logging.getLogger(__name__)


class WithVectorStoreIndex(models.Model):
    _cached_vectorstores = {}
    enable_vectorstore_index = True

    vectorstore_updated = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="已更新向量数据库",
    )
    vectorstore_uids_data = models.TextField(
        null=True,
        blank=True,
        verbose_name="向量数据库记录编号",
        help_text="添加至向量数据库后返回的编号。用于后续向量数据库的数据维护。",
    )

    class Meta:
        abstract = True

    def get_enable_vectorstore_index_flag(self) -> bool:
        """用于判断该记录是否需要被索引。

        返回True表示需要被索引。
        返回False表示不需要被索引。
        """
        return True

    def get_vectorstore_index_names(self) -> List[str]:
        """返回该记录需要添加到哪个索引。"""
        raise NotImplementedError()

    def get_vectorstore_index_contents(self) -> List[str]:
        raise NotImplementedError()

    def get_vectorstore_index_metas(self) -> List[Dict[str, str]]:
        return []

    def get_vectorstore_uids(self):
        if not self.vectorstore_uids_data:
            return []
        else:
            return yaml.safe_load(self.vectorstore_uids_data)

    def set_vectorstore_uids(self, value):
        if not value:
            self.vectorstore_uids_data = None
        else:
            self.vectorstore_uids_data = yaml.safe_dump(value)

    vectorstore_uids = property(get_vectorstore_uids, set_vectorstore_uids)

    def save(self, *args, **kwargs):
        self.vectorstore_updated = False
        result = super().save(*args, **kwargs)
        transaction.on_commit(self.update_vectorstore_index)
        return result

    def update_vectorstore_index(self):
        try:
            if self.enable_vectorstore_index:
                if self.get_enable_vectorstore_index_flag():
                    self.upsert_index(save=False)
                else:
                    self.delete_index(save=False)
            else:
                self.delete_index(save=False)
            self.vectorstore_updated = True
        except Exception as error:
            self.vectorstore_updated = False
            _logger.error(
                "更新向量数据库失败：model=%s.%s, id=%s, error=%s",
                self._meta.app_label,
                self._meta.model_name,
                self.id,
                error,
            )
        self.__class__.objects.bulk_update(
            [self],
            fields=[
                "vectorstore_updated",
                "vectorstore_uids_data",
            ],
        )

    def delete_index(self, save=False):
        deleted = 0
        if self.vectorstore_uids:
            vs = get_cached_vectorstore()
            deleted += vs.delete_many(self.vectorstore_uids)
            self.vectorstore_uids = None
            if save:
                self.save()
        return deleted

    def upsert_index(self, save=False):
        vs_cotnents = self.get_vectorstore_index_contents()
        vs_metas = self.get_vectorstore_index_metas()
        # 先删除
        self.delete_index(save=False)
        # 后添加
        uids = []
        for index_name in self.get_vectorstore_index_names():
            vs = get_cached_vectorstore(index_name=index_name)
            uids += vs.insert_many(contents=vs_cotnents, metas=vs_metas)
        # 更新数据库记录
        self.vectorstore_uids = uids
        if save:
            self.save()
