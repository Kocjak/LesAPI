import scrapy


class MdSpider(scrapy.Spider):
    name = "MD"
    allowed_domains = ["vkusnoitochka.ru"]
    start_urls = ["https://vkusnoitochka.ru"]

    def parse(self, response):
        pass
