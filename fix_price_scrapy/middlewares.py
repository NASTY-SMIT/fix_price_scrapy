from scrapy import signals


class FixPriceScrapySpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class FixPriceScrapyDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# Если вы имеете proxy сервер, раскоментируйте эти строчки
# и впишите ваши данные
# class CustomProxyMiddleware(object):
#     def __init__(self):
#         self.proxy = "http://<адресс прокси>:<порт>"

#     def process_request(self, request, spider):
#         if 'proxy' not in request.meta:
#             request.meta['proxy'] = self.proxy

#     def get_proxy(self):
#         return self.proxy
