import os.path
from collections import namedtuple
import rdflib

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('antroporama', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

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
    MARK_WILEY = Source(
        'Mark Wiley',
        'http://www.dpchallenge.com/image.php?IMAGE_ID=1052201'
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


NS = {
    None: 'http://antroporama.iolanta.tech/',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
}

GRAPH_LIST = [
    'antroporama.n3',
    'images.n3',
    'species.n3',
]


def get_graph():
    graph = rdflib.Graph()
    
    for filename in GRAPH_LIST:
        with open(os.path.join('data', filename), 'r') as f:
            graph.parse(data=f.read(), format='n3')

    return graph


def shorten(value):
    for ns in NS.values():
        value = value.replace(ns, '')

    return value


def get_image(name, graph, subquery=None):
    if subquery is None:
        subquery = 'FILTER(?node = :{})'.format(
            name
        )
    
    r, = list(query(
        graph=graph,
        template_name='image',
        subquery=subquery
    ))

    href, name, url = map(str, r)

    return {
        'href': href,
        'author': {
            'name': name,
            'url': url
        }
    }


def about(element, graph):
    template = env.get_template('queries/about.sparql')
    
    (label, comment), = list(graph.query(template.render(
        node=element
    )))

    return {
        'label': label,
        'comment': comment
    }


def query(graph, template_name, **context):
    """Render a SPARQL template and run it"""
    template = env.get_template(os.path.join(
        'queries',
        '{}.sparql'.format(template_name)
    ))

    return graph.query(template.render(**context))


def get_species(name, graph):
    species = {
        shorten(str(key)): str(value)
        for key, value in query(
            graph=graph,
            template_name='species',
            name=name
        )
    }

    species.update({
        'image': get_image(
            None, graph,
            subquery=':{} :image ?node'.format(name)
        )
    })

    return species


def get_species_list(graph):
    return get_species('proconsul', graph)


def get_data():
    graph = get_graph()

    # species = get_species_list(graph)

    return {
        'header': get_image('header', graph),
        'footer': get_image('footer', graph),
        'about': about('http://antroporama.iolanta.tech', graph),
        'human_from_clay': {
            'title': 'Откуда мы?',
            'image': get_image('human_from_clay', graph),
            'content': 'content/clay.html'
        },
    }


species = [{
    'title': 'Проконсул',
    'species': 'Proconsul heseloni',
    'image': Image('species/proconsul.jpg', Credits.EVSEYEV),
    'time': '18 — 15 млн лет назад',
    'location': 'Восточная Африка',
    'description': 'content/proconsul.html',
    'features': {
        'primary': [
            Feature('monkey', 'Четвероногость'),
            Feature('monkey_foot', 'Хватательные конечности'),
            Feature('brain', '305...320 см³')
        ],
        'secondary': [
            Feature('monkey_on_tree', 'На деревьях'),
            Feature('fruit', 'Любил фрукты'),
            Feature('leaf', 'Листву и побеги')
        ]
    }
}, {
    'title': 'Сахелянтроп',
    'species': 'Sahelanthropus tchadensis',
    'image': Image('species/sahelanthropus.jpg', Credits.EVSEYEV),
        # tumai.jpg
    'time': '7 — 6 млн лет назад',
    'location': 'Центральная Африка, Чад, Торос-Меналла',
    'description': 'content/sahelanthropus.html',
    'features': {
        'primary': [
            Feature('bipedal_monkey', 'Начало двуногости'),
            Feature('monkey_foot', 'Хватательные конечности'),
            Feature('brain', '340...360 см³')
        ],
        'secondary': [
            Feature('monkey_on_tree', 'Всё ещё леса'),
            Feature('savannah', 'И полусаванны'),
            Feature('fruit', 'Фрукты'),
            Feature('leaf', 'Растения')
        ]
    }
}, {
    'title': 'Ардипитек рамидус',
    'species': 'Ardipithecus ramidus',
    'image': Image('species/ardipithecus.jpg', Credits.EVSEYEV),
    'time': '4.4 млн лет назад',
    'location': 'Восточная Африка, Эфиопия',
    'description': 'content/ardipithecus.html',
    'features': {
        'primary': [
            Feature('bipedal_monkey', 'Двуногость продолжается'),
            Feature('monkey_foot', 'Хватательные конечности'),
            Feature('brain', '300...350 см³')
        ],
        'secondary': [
            Feature('monkey_on_tree', 'Леса'),
            Feature('savannah', 'И полусаванны'),
            Feature('fruit', 'Фрукты'),
            Feature('leaf', 'Растения')
        ]
    }
}, {
    'title': 'Австралопитек анамский',
    'species': 'Australopithecus anamensis',
    'image': Image('species/anamensis.jpg', Credits.OSIPOV),
    'time': '4.2 — 3.9 млн лет назад',
    'location': 'Восточная Африка, Кения',
    'description': 'content/anamensis.html',
    'features': {
        'primary': [
            Feature('bipedal_monkey', 'Двуногость'),
            Feature('monkey_foot', 'Обезьянья лапа'),
            Feature('brain', 'неизвестен')
        ],
        'secondary': [
            Feature('monkey_on_tree', 'Леса'),
            Feature('savannah', 'И полусаванны'),
            Feature('fruit', 'Фрукты'),
            Feature('leaf', 'Растения')
        ]
    }
}, {
    'title': 'Австралопитек афарский',
    'species': 'Australopithecus afarensis',
    'image': Image('species/afarensis.jpg', Credits.EVSEYEV),
    'time': '4.0 — 2.5 млн лет назад',
    'location': 'Место: Восточная Африка, Кения, Танзания, Эфиопия',
    'description': 'content/afarensis.html',
    'features': {
        'primary': [
            Feature('human', 'Двуногий'),
            Feature('monkey_foot', 'Хватательные конечности'),
            Feature('brain', '350...550 см³')
        ],
        'secondary': [
            Feature('savannah', 'Саванна'),
            Feature('fruit', 'Фрукты'),
            Feature('leaf', 'Растения'),
            Feature('bone', 'Мясо?'),
            Feature('stone', 'Камни и палки')
        ]
    }
}, {
    'title': 'Человек умелый',
    'species': 'Homo habilis',
    'time': '2.3 — 1.5 млн лет назад',
    'location': 'Восточная и Южная Африка',
    'image': Image('species/habilis.jpg', Credits.EVSEYEV),
    'description': 'content/habilis.html',
    'features': {
        'primary': [
            Feature('human', 'Двуногий'),
            Feature('hand', 'Трудовая кисть'),
            Feature('brain', '550...680 см³')
        ],
        'secondary': [
            Feature('savannah', 'Саванна'),
            Feature('fruit', 'Фрукты'),
            Feature('leaf', 'Растения'),
            Feature('bone', 'Мясо'),
            Feature('stone', 'Олдувайская культура')
        ]
    }
}, {
    'title': 'Человек работающий',
    'species': 'Homo ergaster',
    'time': '1.8 — 1.4 млн лет назад',
    'location': 'Кения, Танзания, Грузия',
    'image': Image('species/ergaster.jpg', Credits.EVSEYEV),
    'description': 'content/ergaster.html',
    'features': {
        'primary': [
            Feature('human', 'Двуногий'),
            Feature('hand', 'Трудовая кисть'),
            Feature('brain', '800...900 см³')
        ],
        'secondary': [
            Feature('savannah', 'Саванна'),
            Feature('fruit', 'Фрукты, растения'),
            Feature('bone', 'Мясо'),
            Feature('stone', 'Олдувайская культура'),
            Feature('fire', 'Огонь')
        ]
    }
}, {
    'title': 'Человек прямоходящий',
    'species': 'Homo erectus',
    'time': '1.5 млн — 400 тыс лет назад',
    'location': 'Африка, Южная Европа, Индонезия, Ява, Китай и др',
    'image': Image('species/erectus1.jpg', Credits.EVSEYEV),
    'description': 'content/erectus.html',
    'features': {
        'primary': [
            Feature('human', 'Двуногий'),
            Feature('hand', 'Трудовая кисть'),
            Feature('brain', '700...1300 см³')
        ],
        'secondary': [
            Feature('tropics', 'Тропический пояс'),
            Feature('fruit', 'Фрукты'),
            Feature('leaf', 'Растения'),
            Feature('deer', 'Мясо крупных животных'),
            Feature('stone', 'Ашельская культура'),
            Feature('fire', 'Огонь'),
            Feature('speech', 'Зачатки речи')
        ]
    }
}, {
    'title': 'Человек гейдельбергский',
    'species': 'Homo heidelbergensis',
    'image': Image('species/heidelbergensis1.jpg', Credits.EVSEYEV),
    'time': '800 — 130 тыс лет назад',
    'location': 'Африка, Европа и др',
    'description': 'content/heidelbergensis.html',
    'sources': [
        'http://antropogenez.ru/species/23/',
        'http://antropogenez.ru/zveno-single/152/'
    ],
    'features': {
        'primary': [
            Feature('human', 'Двуногий'),
            Feature('hand', 'Трудовая кисть'),
            Feature('brain', '1000...1300 см³')
        ],
        'secondary': [
            Feature('fir_tree', 'Тропический и умеренный климат'),
            Feature('leaf', 'растения'),
            Feature('deer', 'Мясо крупных животных'),
            Feature('stone', 'Ашельская культура'),
            Feature('fire', 'Огонь'),
            Feature('speech', 'Речь'),
            Feature('skull', 'Первые погребения')
        ]
    }
}, {
    'title': 'Неандерталец',
    'species': 'Homo neanderthalensis',
    'time': '130 — 28 тыс лет назад',
    'location': 'Европа и Западная Азия',
    'image': Image('species/neanderthalensis1.jpg', Credits.EVSEYEV),
    'description': 'content/neanderthalensis.html',
    'features': {
        'primary': [
            Feature('human', 'Двуногий'),
            Feature('hand', 'Трудовая кисть'),
            Feature('brain', '1300...1600 см³')
        ],
        'secondary': [
            Feature('mammoth', 'Ледниковый климат'),
            Feature('deer', 'Мясо крупных животных'),
            Feature('stone', 'Мустьерская культура'),
            Feature('fire', 'Огонь'),
            Feature('speech', 'Речь'),
            Feature('skull', 'Погребения')
        ]
    }
}, {
    'title': 'Человек разумный',
    'species': 'Homo sapiens sapiens',
    'time': '100 тыс лет назад — ...',
    'location': 'Земля и околоземное пространство',
    'image': Image('species/sapiens.jpg', Credits.EVSEYEV),
    'description': 'content/sapiens.html',
    'sources': [
        ''
    ],
    'features': {
        'primary': [
            Feature('human', 'Двуногий'),
            Feature('hand', 'Трудовая кисть'),
            Feature('brain', '1350 см³')
        ],
        'secondary': [
        ]
    }
}]


reasons = {
    'walking': {
        'title': 'Причины прямохождения',
        'intro': [
            'Как видно, у наших самых ранних предков стремление к прямохождению возникло раньше, чем рост объёма мозга или появление <em>трудовой кисти</em> — то есть руки, способной к тонкой моторике.',

            'Почему так произошло?',

            'Скорее всего, причин было много, но мы приведём самые вероятные.'
        ],
        'list': [Reason(
            image=Image(
                filename='walking/savannah_tree.jpg',
                author=Credits.ETOSHA,
                thumb='walking/savannah_tree_thumb.jpg'
            ),
            title='Перемена климата и сокращение лесов',
            content=
                '''<p>Климат Африки становился суше, и дождевые тропические леса медленно, но неуклонно сокращались, уступая место саваннам.</p>
                <p>А значит, всё больше времени приходилось проводить не на уютной и привычной высокой ветке, а на земле, полной опасностей.</p>
                '''
        ), Reason(
            image=Image(
                filename='walking/standing_monkey.jpg',
                thumb='walking/standing_monkey_thumb.jpg'
            ),
            title='По земле на двух ногах перемещаться удобнее',
            content=
                '''
                <ul>
                    <li>Меньше мешает высокая трава;</li>
                    <li>есть вероятность раньше заметить угрозу;</li>
                    <li>жаркое тропическое солнце доставляет меньше неудобств.</li>
                </ul>
                '''
        ), Reason(
            image=Image(
                filename='walking/monkey_food.jpg',
                author=Credits.GOODALL,
                thumb='walking/monkey_food_thumb.jpg',
            ),
            title='Унести с собой можно больше',
            content='<p>Если ваша подруга с детёнышем ждёт вас в укромном месте, а вы, уйдя далеко в поисках еды, наткнулись на кучу вкусных орехов, то идя домой на двух ногах — вы утащите их больше.</p>'
        )],
        'appendix': [
            'В течение многих и многих тысяч лет обезьянам приходилось всё больше и больше времени проводить на земле, а не на дереве, и те, кто хуже умел это делать, реже выживали и оставляли потомство.',
            'Таким образом, больше потомства оставляли те, кто лучше справлялся с новыми условиями, и со временем облик животных менялся.',
        ]
    },
    'brain': {
        'title': 'Мозг, любовь, мясо и булыжники',
        'intro': [
            '<p>Вспоминая наше предыдущее лирическое отступление, — трудовой кисти у афарских австралопитеков всё ещё нет, орудия изготавливать они пока неспособны.</p><p>Но почему они стали так резко умнеть, превзойдя уже по объёму мозга современных шимпанзе?</p>',
        ],
        'list': [Reason(
            image=Image(
                filename='brain/hyene.jpg',
                thumb='brain/hyene_thumb.jpg'
            ),
            title='Хищники',
            content=
                '''<p>Африканская саванна не была безопасным местом: она кишела хищниками. Например, гигантскими гиенами.</p>
                <ul>
                <li>Гиены ведут ночной образ жизни, что, возможно, заставило австралопитеков перейти к дневному;</li>
                <li>Гиены не слишком выносливы и плохо бегают, развитое прямохождение стало преимуществом;</li>
                <li>Но они довольно глупы, и если вас много, вы умеете громко кричать и кидаться камнями — есть шанс, что вы их отпугнёте.</li>
                </ul>
                <p>У австралопитеков не было мощных зубов и физической силы, и оставалось опираться на сообразительность и коллективизм.</p>
            '''
        ), Reason(
            image=Image(
                filename='brain/chimpanzee_teeth.jpg',
                thumb='brain/chimpanzee_teeth_thumb.png',
                author=Credits.WIKIMEDIA
            ),
            title='Сниженнная агрессивность',
            content='''
                <p>На фото — не предок, а современный шимпанзе. Обратите внимание на размер его клыков.

                <p>Клыки нужны шимпанзе не для того, чтоб отбиваться от хищников, а чтоб пугать других шимпанзе и выяснять, кто здесь самый главный.

                <p>Если вы посмотрите на реконструкцию австралопитека выше, то заметите, что его клыки гораздо меньше. Что даёт основание предполагать сравнительно небольшой уровень агрессии между австралопитеками.

                <p>В стаях шимпанзе вражда и конкуренция настолько накалены, что крайне редко они способны совместно заниматься общим делом.</p>
            '''
        ), Reason(
            image=Image(
                filename='brain/kissing.jpg',
                author=Credits.REUTERS,
                thumb='brain/kissing_thumb.jpg',
            ),
            title='Моногамия',
            content='''<p>Одной из главных причин низкой агрессии у австралопитеков могла быть моногамия — то есть существование семьи, когда самец и самка обитают совместно достаточно долго, чтобы вырастить одного или нескольких детёнышей.</p>
                <p>
                Это приводит к тому, что самцы не занимаются постоянной конкуренцией за самок и не пылают друг к другу убийственной ненавистью.
                </p>
            '''
        ), Reason(
            image=Image(
                filename='brain/chimpanzee_child.jpg',
                thumb='brain/chimpanzee_child_thumb.jpg',
                author=Credits.BBC
            ),
            title='Забота о потомстве',
            content='''
                <p>Но возникает другая проблема — детёнышей с большой головой трудно рожать. Поэтому с течением времени оказывается, что детёныши всё чаще рождаются недоношенными, а значит — беспомощными.

                <p>Мы не знаем, насколько самостоятельны были малыши австралопитеков; но человеческие дети сразу после рождения совершенно беспомощны, в отличие от детёнышей шимпанзе, которые способны держаться за шерсть матери и осмысленно глазеть на окружающий мир.

                <p>Самке было бы трудно вырастить такого детёныша в одиночку, — но на помощь приходит его отец и стая в целом.
            '''
        ), Reason(
            title='Мясо',
            image=Image(
                filename='brain/megantereon.jpg',
                thumb='brain/megantereon_thumb.jpg',
                author=Credits.ANTON
            ),
            content='''
                <p>Таким образом, самцам было логично оставить своих подруг с детёнышами в укромном месте, а самим отправиться искать еду. Стае нужно много питательной еды.

                <p>Наилучший вариант — мясо. Как его добыть?

                <p>На вершине пищевой пирамиды в саванне того времени восседали саблезубые кошки. Громадными клыками удобно разрывать тело жертвы, но из-за них же изрядная часть мяса остаётся на костях.</p>

                <p>Разумеется, на обильные остатки кошачьих пиршеств претендовали грифы и гиены. Но если вы — австралопитек, у вас много товарищей и вы быстро бегаете, то у вашей компании есть шанс успеть первыми, урвать добычу и вовремя сделать ноги.</p>
            '''
        ), Reason(
            title='Трудовая деятельность',
            image=Image(
                filename='brain/monkey_stone.jpg',
                thumb='brain/monkey_stone_thumb.jpg',
                author=Credits.BBC_STONE
            ),
            content='''
                <p>Австралопитеки почти наверняка не были способны к изготовлению орудий труда: их кисть для этого непригодна. Однако после <a href="http://antropogenez.ru/single-news/article/10/">долгих и кропотливых раскопок и исследований</a> были найдены кости копытных с довольно непростой посмертной судьбой:
                
                <ul>
                <li>Сначала на костях отметились клыками саблезубые кошачьи,
                <li>Позже их разгрызали гиены,
                <li>Но в промежутке кто-то усердно их царапал острым камнем.
                </ul>
            
                <p>Ну а как иначе быстро ободрать мясо с костей, если зубы и когти у вас откровенно не очень? Но зато вы достаточно сообразительны, чтоб подобрать подходящий камешек.</p>
            '''
        )],
        'appendix': [
            'Австралопитеки, научившись относительно хорошо бегать и став ещё, к тому же, самыми умными существами на планете, достигли широкого разнообразия и приличной численности, но называть их людьми всё ещё нельзя.',
            'Однако их ближайшие последователи покорили следующую вершину — умение целенаправленно изготавливать орудия.'
        ]
    },
    'labor': {
        'title': 'Труд сделал обезьяну человеком?',
        'list': [Reason(
            title='Олдувайская культура',
            image=Image('oldowan.jpg'),
            content='''
                <p>Олдувайское орудие — это зачастую всего лишь камень, <a href="http://antropogenez.ru/term/205/">расколотый пополам</a> или обколотый с нескольких сторон с целью получить острый край.</p>
                <p>Это звучит просто, но в сравнении с австралопитеками было серьёзным шагом вперёд, который отразился даже на строении кисти, ставшем ближе к современному.</p>
            '''
        ), Reason(
            title='Всеядность',
            image=Image('bone.jpg'),
            content='''
                <p><a href="https://www.britannica.com/topic/Homo-habilis">Установлено</a>, что доля мяса в рационе <em>Homo Habilis</em> была существенной. Известно, что он был падальщиком, поскольку сам убить крупных животных, которыми питался, он был не в состоянии.</p>
                
                <p>Однако не исключено, что охотиться на мелкую дичь люди уже тогда умели.</p>
            '''
        ), Reason(
            title='Рост мозга',
            image=Image('habilis_skull.jpg'),
            content='''
                <p>Нежелание дичи быть съеденной и конкуренция с другими группами своего же вида приводили к тому, что первым людям было выгодно быть умными и сообразительными.
                <p>Им это помогало лучше выживать и лучше питаться, а питание, в свою очередь, позволяло наращивать мозг ещё активнее.
                <p>С <em>Homo habilis</em> начинается резкий <a href="http://humanorigins.si.edu/evidence/human-fossils/species/homo-habilis">рост объёма мозга</a>, который продолжался до самого последнего времени.</p>
            '''
        )],
    },
    'georgia': {
        'title': 'Первые в Азии',
        'list': [Reason(
            title='Люди из Дманиси',
            image=Image('ergaster_map.png'),
            content='''
                <p>Очевидно, людей в Африке стало уже достаточно много, и люди стали уже достаточно смелы, чтобы <a href="http://antropogenez.ru/no_cache/locations-map/hominid/21/">пускаться в дальние путешествия</a>. Мы не знаем, как далеко ушли <em>Homo ergaster</em>, но до Грузии они точно добрались, о чём говорят находки в <a href="http://antropogenez.ru/location/78/">Дманиси</a>.
            '''
        ), Reason(
            title='На лицо ужасные',
            image=Image(
                filename='georgia/georgicus.jpg',
                thumb='georgia/georgicus_thumb.jpg',
                author=Credits.EVSEYEV
            ),
            content='''
                <p>В Дманиси найдена целая коллекция черепов и скелетов от пяти людей разных полов и возрастов, это уникальная находка чрезвычайно хорошей сохранности.
                <p>Интересно, что мозг у дманисцев довольно мал относительно других известных <em>Homo ergaster</em> — до 546 см³, а их внешность довольно брутальна и архаична. На фото — реконструкция облика обладателя пятого черепа, известного под индексом D4500.</p>
            '''
        ), Reason(
            title='Добрые внутри',
            image=Image(
                filename='georgia/dmanisi_d3444.jpg',
                thumb='georgia/dmanisi_d3444_thumb.jpg',
                author=Credits.WIKIMEDIA
            ),
            content='''
                <p>А <a href="http://antropogenez.ru/fossil/126/">четвёртый череп</a> принадлежал старику.
                
                <p>Задолго до смерти он потерял все зубы, так что альвеолы их успели полностью зарасти.

                <p>Однако он продолжал жить, что говорит о заботе соплеменников: за стариком ухаживали и кормили его. Это самый древний доказанный пример альтруизма и любви к ближним среди наших предков, датируемый приблизительно <em>1.77 млн лет назад</em>.</p>
            '''
        )]
    },
    'erectus': {
        'title': 'Исчезнувшее человечество',
        'intro': ['''
            <p>Можно пофантазировать, что у <em>Homo erectus</em> были свои обычаи, свой взгляд на жизнь и отношение к ней, может быть, даже свои сказки и легенды. Мы этого, безусловно, никогда не узнаем. Однако, кое-что нам всё же известно.
        '''],
        'list': [Reason(
            title='Ашельская культура',
            image=Image('biface.jpg'),
            content='''
                <p>Ашельская культура характерна <em>ручными рубилами</em>, или <em>бифасами</em>. В отличие от олдувайских орудий, ашельское рубило представляло собой не просто расколотый камень, а обрабатывалось с разных сторон с целью достижения определённой формы.

                <p>Ашельские рубила гораздо удобнее лежат в руке и гораздо эффективнее в работе. Такими орудиями обрабатывали мясо и дерево.
            '''
        ), Reason(
            title='Охота',
            image=Image('shoningen.jpg'),
            content='''
                <p>Обработка дерева в том числе нужна была эректусам для того, чтоб изготавливать деревянные копья, конец которых был заострён и <a href="http://antropogenez.ru/zveno-single/127/">обожжён для прочности</a>. Остатки таких копий были найдены в рёбрах слонов.

                <p>Это свидетельствует о том, что эректусы окончательно оставили роль падальщиков, заняв совершенно новое место в экосистеме — охотников на крупную дичь.
            '''
        ), Reason(
            title='Мозг',
            image=Image('sinantropus.jpg'),
            content='''
                <p>Такое изменение поведения не могло не сказаться на строении мозга. Его объём уже почти достиг современных средних значений. Рельеф, видный на отпечатках черепов <em>(эндокранах)</em> свидетельствует, что:</p>
                <ul>
                    <li>развилась зона речи;
                    <li>улучшилась память и способности к мышлению;
                    <li>наверняка развилось зрение, что важно для меткости и дальности метания копий, например.
                </ul>
            '''
        )]
    },
    'future': {
        'title': 'А дальше?',
        'intro': ['''
            <p>Наука даёт нам возможность оглянуться назад на пройденный за десять миллионов лет путь и осознать, как многого мы за это время добились и через что прошли. Хищники, голод, болезни, смерть, ледниковые периоды. Множество совершённых ошибок, уничтоженные леса и саванны, навсегда исчезнувшие животные. Реки пролитой крови, войны, казни, концлагеря и ядерные бомбардировки.</p>
        '''],
        'list': [Reason(
            title='И это вы называете разумом?',
            image=Image('mind.jpg'),
            content='''
                <p>Называя себя, несмотря на всё перечисленное выше, разумными, мы определяем наше главное качество и отличительную черту, которой мы бы хотели гордиться.

                <p>Из своего прошлого мы помним не столько завоевателей и полководцев, сколько выдающихся учёных, философов, художников и инженеров, — то есть тех, кто познавал природу или силой своего разума создавал то, чего никогда прежде не было.

                <p>В этом смысле Менделеев, открывший фундаментальный закон природы, и Моцарт, писавший полотна языком музыки, одинаково заслужили о себе вечную память.
            '''
        ), Reason(
            title='Зачем?',
            image=Image('earth.jpg'),
            content='''
                <p>Несмотря на все неоспоримые достижения, мы не решили ещё массу проблем и не нашли ответов на массу вопросов:
                <ul>
                    <li>безопасные для планеты и нас самих технологии, энергия и транспорт,
                    <li>всеобщий доступ к знаниям,
                    <li>продление жизни и улучшение её качества,
                    <li>оптимальная организация общества,
                    <li>эффективная структура экономики,
                </ul>
                
                <p>— над всем этим ещё работать и работать.
            '''
        ), Reason(
            title='И что потом?',
            image=Image('mars.jpg'),
            content='''
                И не стоит забывать, что Земля, в конце концов, — всего лишь крохотный уголок огромной Вселенной.

                <p>Если мы хотим существовать сколь-нибудь долго, то нам необходимо думать об освоении космоса и других планет, — сначала в нашей Солнечной системе, а затем и за её пределами. Никто не знает, что нас ждёт в бесконечных безднах. Но ведь это и интересно, не так ли?
            '''
        )]
    }
}