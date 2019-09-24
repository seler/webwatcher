import re
import enum


class Parser:
    pass


class OLX(Parser):
    url_prog = re.compile("https?://(www.)?olx.pl.*")
    name = "OLX"


class Allegro(Parser):
    url_prog = re.compile("https?://(www.)?olx.pl.*")
    name = "Allegro"


class Parsers(enum.Enum):
    olx = OLX
    allegro = Allegro


def get_parser_by_url(url):
    for parser in Parsers:
        if parser.value.url_prog.match(url):
            return parser.name
