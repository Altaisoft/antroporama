"""Semantic Web storage based on RDFLib"""

from .base import MappingStorage, Storage
from typing import Optional, List, Mapping, Union
import rdflib
from rdflib.plugins.sparql import prepareQuery


class SemanticStorage(Storage):
    filenames: Optional[List[str]] = None
    namespaces: Mapping[Optional[str], rdflib.Namespace]

    def __init__(self):
        self.graph = self.get_graph()

    def get_filenames(self) -> List[str]:
        if self.filenames is not None:
            return self.filenames

        else:
            raise ValueError(
                'Please specify {}.filenames or override get_filenames().'.format(
                    str(self.__class__)
                )
            )

    def get_namespaces(self) -> Mapping[Optional[str], rdflib.Namespace]:
        if self.namespaces is not None:
            return self.namespaces

        else:
            raise ValueError(
                'Please specify {}.namespaces or override get_namespaces().'.format(
                    str(self.__class__)
                )
            )

    @property
    def namespace(self) -> rdflib.Namespace:
        return self.get_namespaces()[None]

    def get_graph(self):
        graph = rdflib.Graph()

        for filename in self.get_filenames():
            with open(filename, 'r') as f:
                graph.parse(data=f.read(), format='n3')

        return graph

    def query(self, query: str, **kwargs):
        return self.graph.query(prepareQuery(
            query,
            initNs=self.get_namespaces(),
        ), initBindings=kwargs)

    def get(self, key: str, field_list: List[str] = None):
        return self.query(
            '''SELECT ?href { ?node :href ?href }''',
            node=self.namespace[key]
        )


class SemanticMapping(MappingStorage):
    storage: SemanticStorage

    def get(self, key):
        return self.storage.get(key)
