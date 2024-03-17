# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer
import json
from book_scrapy.items import BookScrapyItem

class BookScrapyPipeline:
    def open_spider(self, spider):
            
        self.producer = KafkaProducer(bootstrap_servers=['localhost:29092'], 
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        self.topic = 'book_scrapy'
        
    def close_spider(self, spider):
        self.producer.close()

    def send_to_kafka(self, msg: dict):
        self.producer.send(self.topic, value=msg)
        self.producer.flush()

    def process_item(self, item, spider):
        msg = ItemAdapter(item).asdict()
        self.send_to_kafka(msg=msg)
        return item
