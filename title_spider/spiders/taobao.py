#-*- coding: utf-8 -*-
import scrapy
from utils.common import UrlGenerator
from items import TitleSpiderItem
import logging
from scrapy.utils.log import configure_logging
from scrapy_webdriver.http import WebdriverRequest

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='taobao.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    url = UrlGenerator("https://s.taobao.com/search?q=%s&s=%d", 10, "./entity/test_entity.txt")

    def start_requests(self):
        for title, url in self.url:
            yield WebdriverRequest(url, callback=self.parse)

    def parse(self, response):
        product = response.webdriver.find_elements_by_css_selector("div.title a.J_ClickStat")
        query = response.webdriver.find_element_by_css_selector("input.search-combobox-input").get_attribute("value")
        for e in product:
            title = e.text.strip()
            self.logger.info("query=%s, title=%s" % (query.encode('utf-8'), title.encode('utf-8')))
            item = TitleSpiderItem()
            item['title'] = title.encode('utf-8')
            item['query'] = query.encode('utf-8')
            yield item


