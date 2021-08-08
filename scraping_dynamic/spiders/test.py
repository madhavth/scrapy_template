import scrapy
import re
from scrapy_splash import SplashRequest

class DefaultSpider(scrapy.Spider):
    name = 'test'
    base = 'https://www.youtube.com/watch?v=vOBKxUT9Da4'

    def start_requests(self):
        yield SplashRequest(url=self.base)

    def parse(self, response):
        views = response.css(".ytd-video-view-count-renderer::text").get()
        print(views)
        yield {
            "views": views
        }
