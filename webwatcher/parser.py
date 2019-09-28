import re
import requests
import enum
from lxml import html
import feedparser
import dateparser


class Parser:
    def __init__(self, watch):
        self.watch = watch


class RSS(Parser):
    pass


class OLX(Parser):
    url_prog = re.compile("https?://(www.)?olx.pl.*")
    name = "OLX"

    def get_items(self):
        from .models import Item

        response = requests.get(self.watch.url)
        content = html.fromstring(response.content.strip())
        rss_link = content.xpath('*/link[@type="application/rss+xml"]')[0]
        response = requests.get(rss_link.get("href"))
        data = response.content.strip()
        # remove link as its cousing problems with feedparser
        front = data[: data.find(b"<link>")]
        back = data[data.find(b"</link>") + 7 :]  # noqa
        data = front + back
        feed = feedparser.parse(data)
        for entry in feed.entries:
            if "img" in entry.description:
                image = html.fromstring(entry.description).findall("img")[0].get("src")
            else:
                image = None
            yield Item(
                watch=self.watch,
                title=entry.title,
                link=entry.link,
                description=entry.description,
                uid=entry.id,
                timestamp=dateparser.parse(entry.published),
                image=image,
            )


class Allegro(Parser):
    url_prog = re.compile("https?://(www.)?olx.pl.*")
    name = "Allegro"


class Parsers(enum.Enum):
    olx = OLX
    allegro = Allegro


def get_parser_name_by_url(url):
    for parser in Parsers:
        if parser.value.url_prog.match(url):
            return parser.name


def get_parser_by_name(name):
    return Parsers[name].value
