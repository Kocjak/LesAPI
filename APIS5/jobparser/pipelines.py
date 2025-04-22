# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv


class JobparserPipeline:
    def process_item(self, item, spider):
        try:
            with open('movies.csv', 'a', newline='', encoding='Windows-1251') as file:
                writer = csv.writer(file, delimiter=';')

                if file.tell() == 0:
                    writer.writerow(['Название', 'URL', 'Рейтинг', 'Жанры'])

                second_rating = item['rating'][1] if len(item['rating']) > 1 else ''

                row = [
                    item['name'],
                    item['url'],
                    second_rating,
                    ', '.join(item['genre'])
                ]
                writer.writerow(row)
        except Exception as e:
            print(f"Ошибка при сохранении в CSV: {e}")
        return item