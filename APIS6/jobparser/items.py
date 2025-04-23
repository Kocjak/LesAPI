# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import TakeFirst, MapCompose, Compose
from openpyxl.styles.builtins import output


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_proccesor=TakeFirst())
    categoriya = scrapy.Field()
    url = scrapy.Field(output_proccesor=TakeFirst())
    photos = scrapy.Field(output_proccesor=TakeFirst())

