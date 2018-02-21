from typing import Type, Optional
from .storages.base import CollectionStorage, MappingStorage


class Collection:
    storage: Optional[CollectionStorage]
    model: Type


class Mapping:
    storage: Optional[MappingStorage]
    model: Type

    def get(self, key):
        return self.storage.get(key)
