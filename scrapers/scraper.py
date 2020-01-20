import requests
from lxml import etree
from io import StringIO


class WebScraper(object):
    def __init__(self):
        pass

    def request_raw(self, url):
        return requests.get(url).text

    def scrape_html(self, url):
        raw_html = self.request_raw(url)
        html_parser = etree.HTMLParser()
        tree = etree.parse(StringIO(raw_html), html_parser)
        return tree.getroot()
