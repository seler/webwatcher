import datetime
import enum
import re

import dateparser
import feedparser
import requests
from lxml import etree, html


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
            link_ = offer.cssselect(".title-cell a")
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


class PageWithRSS(Parser):
    def get_items(self):
        from .models import Item

        timestamp = datetime.datetime.now()

        response = requests.get(self.watch.url)
        content = html.fromstring(response.content.strip())
        rss_link = content.xpath('*/link[@type="application/rss+xml"]')[0]
        response = requests.get(rss_link.get("href"))
        data = response.content.strip()
        if data.find(b"<link>"):
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


class OTOMOTO(PageWithRSS):
    url_prog = re.compile("https?://(www.)?otomoto.pl.*")
    name = "OTOMOTO"


class Parsers(enum.Enum):
    olx = OLX
    otomoto = OTOMOTO


def get_parser_name_by_url(url):
    for parser in Parsers:
        if parser.value.url_prog.match(url):
            return parser.name


def get_parser_by_name(name):
    return Parsers[name].value
