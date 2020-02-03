import datetime
import enum
import re

import requests
from lxml import etree


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

        timestamp = datetime.datetime.now()

        response = requests.get(self.watch.url)
        tree = etree.HTML(response.content.strip())
        offers = tree.xpath('//*[@id="offers_table"]/tbody/tr')
        for offer in offers:
            image = None
            img_ = offer.cssselect("a.thumb img")
            if img_:
                image = img_[0].get("src")

            uid = None
            uid_ = offer.cssselect(".offer-wrapper > table")
            if uid_:
                uid = uid_[0].get("data-id")

            title = None
            title_ = offer.cssselect(".title-cell strong")
            if title_:
                title = title_[0].text

            price = None
            price_ = offer.cssselect(".price strong")
            if price_:
                price = price_[0].text

            link = None
            link_ = offer.cssselect(".title-cell")
            if link_:
                link = link_[0].get("href")

            if title and link:
                yield Item(
                    watch=self.watch,
                    title=title,
                    link=link,
                    description=price,
                    uid=uid,
                    timestamp=timestamp,
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
