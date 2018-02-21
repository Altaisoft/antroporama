from rdflib import Namespace, namespace
from aristo.storages.semantic import SemanticMapping, SemanticStorage
from aristo.storages import register
import models


class AntroporamaStorage(SemanticStorage):
    filenames = [
        'data/antroporama.n3',
        'data/images.n3',
        'data/species.n3'
    ]

    # Will be useful to build queries
    namespaces = {
        None: Namespace('http://antroporama.iolanta.tech/'),

        'rdf': namespace.RDF,
        'rdfs': namespace.RDFS,
        'owl': namespace.OWL,
        'dc': namespace.DC,
        'xsd': namespace.XSD
    }


@register(models.Images)
class SemanticImages(SemanticMapping):
    storage = AntroporamaStorage

