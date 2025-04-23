import scrapy
from scrapy.http import HtmlResponse
from GIT_API.APIS6.jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

class UnSpider(scrapy.Spider):
    name = "UN"
    allowed_domains = ["unsplash.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/t/{kwargs.get('category')}"]

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@itemprop='contentUrl']")
        for link in links:
           yield response.follow(link, callback=self.parse_photos)


    def parse_photos(self, response:HtmlResponse):
        # name = response.xpath("(//img/@alt)[2]").get()
        # categoriya = response.xpath("//a[@class='qOAId yZhvJ FTKrh']/@title").getall()
        # url = response.url
        # photos = response.xpath("//div[@class='NrLlp']/img/@src")
        #
        # yield(JobparserItem(name=name, categoriya=categoriya, url=url,photos=photos))

        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name', "(//h1/text())")
        loader.add_xpath('categoriya', "//a[@class='qOAId yZhvJ FTKrh']/@title")
        loader.add_xpath('photos', "//div[@class='NrLlp']/img/@src")
        loader.add_value('url', response.url)

        yield loader.load_item()