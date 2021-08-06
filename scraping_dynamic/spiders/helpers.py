from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def selenium_wait_request(url, callback,selector,wait_time= 10):
    return SeleniumRequest(url = url,
        callback = callback,
        wait_time = wait_time,
        wait_until = EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

def get_text(element, selector):
        return element.css(selector).get(default='').strip()


def get_link(element, selector):
    return element.css("a.btn.btn-primary.btn-user").attrib["href"]