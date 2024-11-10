# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from db_hj3415 import mymongo, myredis


class ValidationPipeline:
    def process_item(self, item, spider):
        return item


class RedisPipeline:
    def process_item(self, item, spider):
        print(f"\tIn RedisPipeline.. db: mi / index: {item['title']} / date: {item['date']} / value: {item['value']}")
        mi_index = 'mi.' + item['title']
        del_redis_names = [ mi_index + '_recent', mi_index + '_trend']
        for redis_name in del_redis_names:
            print(f"\t\tDelete redis name : '{redis_name}'")
            myredis.Base.delete(redis_name)
        return item


class MongoPipeline:
    # 몽고 데이터 베이스에 저장하는 파이프라인
    def process_item(self, item, spider):
        """
        아이템 구조
            title = scrapy.Field()
            date = scrapy.Field()
            value = scrapy.Field()
        """
        print(f"\tIn MongoPipeline.. db: mi / index: {item['title']} / date: {item['date']} / value: {item['value']}")
        mymongo.MI.save(item['title'], {"date": item['date'], "value": item['value']})
        return item