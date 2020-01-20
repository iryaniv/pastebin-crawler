from scrapers.scraper import WebScraper
from models.paste import Paste
import arrow


class PastebinCrawler(object):
    def __init__(self, archive_url='https://pastebin.com/archive',
                 paste_id_format='https://pastebin.com/{}',
                 raw_paste_id_format='https://pastebin.com/raw/{}',
                 paste_date_format='dddd Do of MMMM YYYY hh:mm:ss A'):
        self.__scraper = WebScraper()
        self.__archive_url = archive_url
        self.__paste_id_format = paste_id_format
        self.__raw_paste_id_format = raw_paste_id_format
        self.__paste_date_format = paste_date_format

    def get_recent_pastes_ids(self):
        root_html = self.__scraper.scrape_html(self.__archive_url)
        pastes_urls = root_html.find('.//table').findall('.//a')
        return [url.get('href').replace('/', '') for url in pastes_urls if 'archive' not in url.get('href')]

    def get_paste(self, paste_id):
        paste_root = self.__scraper.scrape_html(self.__paste_id_format.format(paste_id))
        paste_content = self.__scraper.request_raw(self.__raw_paste_id_format.format(paste_id)).strip()
        paste_name = paste_root.find('.//h1').text
        paste_info = paste_root.xpath(".//div[contains(@class, 'paste_box_line2')]")[0]
        paste_date = self.__parse_date(paste_info.find('.//span').get('title'))
        paste_author = paste_info.find('.//a')
        if paste_author is not None:
            paste_author = paste_author.text
        else:
            paste_author = ''
        return Paste(paste_id, paste_name, paste_author, paste_date, paste_content)

    def __parse_date(self, date):
        return str(arrow.get(date, self.__paste_date_format))
