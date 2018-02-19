from aristo.storages.semantic import SemanticStorage
from aristo.storages import register
import models


@register(models.Images)
class ImagesStorage(SemanticStorage):
    pass
