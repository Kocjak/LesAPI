# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv
import json
from scrapy.pipelines.images import ImagesPipeline

class JobparserPipeline:
    def process_item(self, item, spider):
        rows = []
        fieldnames = ['name', 'categoriya', 'photo_url', 'photo_checksum', 'photo_path', 'photo_status', 'source_url']

        for photo in item['photos']:
            row = {
                'name': item['name'][0],
                'categoriya': ', '.join(item['categoriya']),
                'photo_checksum': photo['checksum'],
                'photo_path': photo['path'],
                'photo_status': photo['status'],
                'photo_url': photo['url'],
                'source_url': item['url'][0]
            }
            rows.append(row)

        with open('photos.csv', 'a', newline='', encoding='windows-1251') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerows(rows)

        return item


class PicturesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print()
        if item['photos']:
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print()
        if results:
            item['photos']=[itm[1] for itm in results if itm[0]]
        return item