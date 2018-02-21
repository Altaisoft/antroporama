from typing import Type


class Storage:
    pass


class CollectionStorage:
    collection: Type

    def all(self):
        raise NotImplementedError()


class MappingStorage:
    storage: Type[Storage]
    collection: Type

    def get(self, key):
        raise NotImplementedError()
