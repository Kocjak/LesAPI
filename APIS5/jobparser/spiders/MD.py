import scrapy
from scrapy.http import HtmlResponse
from GIT_API.APIS5.jobparser.items import JobparserItem

class MdSpider(scrapy.Spider):
    name = "MD"
    allowed_domains = ["tvigle.ru"]
    start_urls = ["https://www.tvigle.ru/catalog/filmy/"]

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='styles_root__XM0Up']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.film_parse)

    def film_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").get()
        genre = response.xpath("//div[@class='styles_group__6Bp4K']//text()").getall()
        rating = response.xpath("//p[@class ='styles_ratingValue__N25mD styles_good___fYqr']//text()").getall()
        url = response.url

        yield JobparserItem(name=name, genre=genre, rating=rating, url=url)

        print()





