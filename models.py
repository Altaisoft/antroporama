from dataclasses import dataclass
from collections import namedtuple
from enum import Enum


Feature = namedtuple('Feature', ['icon', 'title'])
Image = namedtuple('Image', ['filename', 'author'])
Source = namedtuple('Source', ['name', 'url'])


class Credits(Enum):
    MARK_WILEY = Source('Mark Wiley', 'http://www.dpchallenge.com/image.php?IMAGE_ID=1052201')
    EVSEYEV = Source('Roman Yevseyev', 'http://other-worlds.ru/')
    OSIPOV = Source('Oleg Osipov', None)
