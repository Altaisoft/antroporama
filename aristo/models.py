from typing import Type, Optional
from .storages.base import CollectionStorage


class Collection:
    storage: Optional[CollectionStorage]
    model: Type

    def all(self):
        return self.storage.all()
