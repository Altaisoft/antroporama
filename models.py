from typing import Optional
from aristo.models import Collection


class Credit:
    """Credit for using someone's work"""
    name: str
    url: Optional[str]


class Image:
    """Image file used in the article"""
    url: str
    credit: Optional[Credit]
    thumbnail: Optional[str]


class Images(Collection):
    model = Image
