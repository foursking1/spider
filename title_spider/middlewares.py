#-*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
import logging

logging.basicConfig(filename='middleware.log', level=logging.INFO)
logger = logging.getLogger(__name__)

class PhantomJSMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):

        if request.meta.has_key('PhantomJS'):# 如果设置了PhantomJS参数，才执行下面的代码
            logger.info('Using PhantomJS ')
            service_args = ['--load-images=false', '--disk-cache=true']
            if request.meta.has_key('proxy'): # 如果设置了代理(由代理中间件设置)
                service_args.append('--proxy='+request.meta['proxy'][7:])
            try:
                driver = webdriver.PhantomJS(executable_path = 'D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs.exe', service_args = service_args)
                driver.get(request.url)
                driver.save_screenshot
                content = driver.page_source.encode('utf-8')
                url = driver.current_url.encode('utf-8')
                driver.quit()
                if content == '<html><head></head><body></body></html>':# 内容为空，当成503错误。交给重试中间件处理
                    logger.warning('503 error ')
                    return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')
                else: # 返回response对象
                    logger.info('Returing response ')
                    return HtmlResponse(url, encoding = 'utf-8', status = 200, body = content)

            except Exception, e: # 请求异常，当成500错误。交给重试中间件处理
                logger.warning('PhantomJS Exception!')
                logger.error(e)
                return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')
        else:
            logger.warning('Common Requesting: '+request.url)