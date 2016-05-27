#-*- coding: utf-8 -*-
import scrapy
from utils.common import UrlGenerator2
from items import TitleSpiderItem
import logging
from scrapy.utils.log import configure_logging
from scrapy_webdriver.http import WebdriverRequest
from scrapy_webdriver.http import WebdriverActionRequest
import time

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='jingdong.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class JingDongSpider(scrapy.Spider):
    name = 'jingdong'
    url = UrlGenerator2("http://search.jd.com/Search?keyword=%s&enc=utf-8",  "./entity/test_entity.txt")
    count = 0;

    def start_requests(self):
        for title, url in self.url:
            yield WebdriverRequest(url, callback=self.parse_first)

    def parse_first(self, response):

        query = response.webdriver.find_element_by_css_selector("input#key-re-search").get_attribute("value")
        driver = response.webdriver

        for i in range(5):
            js = "window.scrollTo(100,10000)"
            driver.execute_script(js)
            time.sleep(2)
            # 等待一下dom才加载完毕， 所以这个步骤也许会失败吧
            product = response.webdriver.find_elements_by_css_selector("div.p-name")
            for e in product:
                title = e.text.strip()
                self.logger.info("query=%s, title=%s" % (query.encode('utf-8'), title.encode('utf-8')))
                item = TitleSpiderItem()
                item['title'] = title.encode('utf-8')
                item['query'] = query.encode('utf-8')
                yield item

            # 点击下一页
            pages = driver.find_elements_by_css_selector("span.p-num a")
            index = 0
            for j, page in enumerate(pages):
                if page.get_attribute("class") == "curr":
                    index = j
            pages[index + 1].click()





