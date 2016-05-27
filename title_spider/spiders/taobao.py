#-*- coding: utf-8 -*-
import scrapy
from utils.common import UrlGenerator
from items import TitleSpiderItem
import logging
from scrapy.utils.log import configure_logging
from scrapy_webdriver.http import WebdriverRequest
from datetime import datetime
# from selenium import webdriver
#
# driver = webdriver.PhantomJS()
# driver.save_screenshot()

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='taobao.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    url = UrlGenerator("https://s.taobao.com/search?q=%s&s=%d", 10, "./entity/test_entity.txt")
    count = 0;

    def start_requests(self):
        for title, url in self.url:
            #request = scrapy.Request(url, self.parse)
            #request.meta['PhantomJS'] = True

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

            # print type(response)
            # self.count += 1;
            # response.webdriver.save_screenshot('./' + str(self.count) + '.png')

# product = response.webdriver.find_element_by_css_selector("div.title a.J_ClickStat")
#  print product
#  query = response.webdriver.find_element_by_css_selector("input.search-combobox-input")
#  #product = response.css("div.title a.J_ClickStat")
# # query = response.css("input.search-combobox-input").xpath('@value').extract_first()
#  for e in product:
#      titles = e.xpath('text()').extract()
#      # map(lambda x : x.replace('\n', '').strip(' '), titles)
#      #print e.xpath('text()').extract()
#      title = ''.join(titles)
#      title =  title.replace('\n', '').strip(' ')
#      self.logger.info("query=%s, title=%s" % (query.encode('utf-8'), title.encode('utf-8')))
#      item = TitleSpiderItem()
#      item['title'] = title.encode('utf-8')
#      item['query'] = query.encode('utf-8')
#      yield item
