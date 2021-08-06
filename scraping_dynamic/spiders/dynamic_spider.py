import scrapy
import re
from scrapy_selenium import SeleniumRequest
from scrapy import Request
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from . import helpers

class DynamicSpider(scrapy.Spider):
    name = 'dynamic'
    search_term = None
    max_count = 10
    main_url = "https://www.pdfdrive.com"

    def __init__(self, name=None, search_term ='secret of happinness', **kwargs):
        self.search_term = search_term
        super().__init__(name=name, **kwargs)

    def start_requests(self):
        base = 'https://www.pdfdrive.com/search?q='
        current = base + self.search_term
        yield Request(url = current, callback = self.parse)

    def parse(self, response):
        file_rows = response.css(".file-right")
        my_links = []
        max = 2 if len(file_rows) >3 else len(file_rows)

        for i,row in enumerate(file_rows):
            link = row.css("a").attrib["href"]
            my_links.append(link)
            link = self.main_url + link
            yield response.follow(url = link, callback = self.get_down_link)
            if i > max:
                break

    def get_down_link(self, response):
        down_page = response.css("#download-button-link").attrib["href"]
        yield helpers.selenium_wait_request(
            url = self.main_url +down_page,
            callback = self.final_download_link,
            wait_time=10,
            selector= 'a.btn.btn-primary.btn-user'
        )
    

    def final_download_link(self, response):
        # link = driver.find_element_by_css_selectors("a.btn.btn-primary.btn-user").text
        link = response.css("a.btn.btn-primary.btn-user").attrib["href"]

        # title = driver.find_element_by_css_selectors("h1.ebook-title a::text").text
        title = response.css("h1.ebook-title a::text").get()

        yield {
            "title": title,
            "download_link": self.main_url + link
        }
        

