#-*- coding: utf-8 -*-
import scrapy
from utils.common import UrlGenerator
from items import TitleSpiderItem
import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='amazon.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    url = UrlGenerator("https://www.amazon.cn/s/?field-keywords=%s&page=%d", 1, "./entity/test_entity.txt")

    def start_requests(self):
        for title, url in self.url:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        product = response.css("a.s-access-detail-page")
        query = response.css("input#twotabsearchtextbox").xpath('@value').extract_first()
        for e in product:
            for title in e.xpath('@title').extract():
                self.logger.info("query=%s, title=%s" % (query.encode('utf-8'), title.encode('utf-8')))
                item = TitleSpiderItem()
                item['title'] = title.encode('utf-8')
                item['query'] = query.encode('utf-8')
                yield item

        # product = soup.find_all("a", class_="s-access-detail-page")
        # for d in product:
        #     # 编码问题
        #     title = d['title'].encode('utf-8')
        #     if title in self.title_set:
        #         continue
        #     self.title_set.add(title)
        #     logger.info("seed word= %s, page = %d, thread_name = %s, title = %s " % (item, page, self.name, title))
        #     self.out_queue.put(title)
