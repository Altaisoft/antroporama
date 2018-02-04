from dataclasses import dataclass
from collections import namedtuple
from enum import Enum


Feature = namedtuple('Feature', ['icon', 'title'])
Source = namedtuple('Source', ['name', 'url'])


@dataclass
class Image:
    filename: str
    author: Source = None
    thumb: str = None


@dataclass
class Reason:
    title: str
    image: Image
    content: str

    full_image: Image = None


class Credits:
    # Species artists
    EVSEYEV = Source(
        'Roman Yevseyev',
        'http://other-worlds.ru/'
    )
    OSIPOV = Source('Oleg Osipov', None)

    # Illustrations
    LURSSEN = Source(
        'Jean Lurssen',
        'http://the-watercolorist.blogspot.ru/2011/05/savannah-dawn.html'
    )
    MARK_WILEY = Source(
        'Mark Wiley',
        'http://www.dpchallenge.com/image.php?IMAGE_ID=1052201'
    )

    SPACE_ENGINE = Source(
        'Space Engine Project',
        'http://spaceengine.org/'
        # https://vk.com/photo-40735526_420366748?all=1
    )

    ETOSHA = Source(
        'Etosha National Park',
        'http://www.etoshanamibia.info/what-to-spot/plantlife/'
    )

    ILYES = Source(
        'Laszlo Ilyes',
        'https://www.flickr.com/photos/laszlo-photo/497621041/'
    )

    WIKIMEDIA = Source(
        'Wikimedia Commons',
        'https://commons.wikimedia.org/'
    )

    GOODALL = Source(
        'Dr. Jane Goodall',
        'https://janegoodall.ca/our-stories/10-things-about-chimpanzees/'
    )

    REUTERS = Source(
        'Reuters',
        'https://www.reuters.com/article/us-science-chimpanzees/humans-close-relatives-chimps-and-bonobos-were-kissing-cousins-idUSKCN12R2FV'
    )

    BBC = Source(
        'BBC',
        'http://www.bbc.com/earth/story/20151112-a-wild-chimp-cares-for-her-disabled-child'
    )

    BBC_STONE = Source(
        'BBC',
        'http://www.bbc.com/earth/story/20150818-chimps-living-in-the-stone-age'
    )

    ANTON = Source(
        'Mauricio Antón',
        'http://www.kidneynotes.com/2012/07/paleoillustration-megantereon-smilodon.html'
    )
