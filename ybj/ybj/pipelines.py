# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

from kafka import KafkaProducer


class YbjPipeline:
    def process_item(self, item, spider):
        return item



class KafkaPipeline(object):

    """
    Publishes a serialized item into a Kafka topic
    :param producer: The Kafka producer
    :type producer: kafka.producer.Producer
    :param topic: The Kafka topic being used
    :type topic: str or unicode
    """

    def __init__(self, producer):
        """
        :type producer: kafka.producer.Producer
        :type topic: str or unicode
        """
        self.producer = producer


    def process_item(self, item, spider):
        """
        会根据这个spider的名称+"_"+item的类名作为topic名称发送到kafka
        """
        # put spider name in item

        # topic这里根据不同的item加到不同的kafka的topic中
        topic = spider.name +'_'+ item.__class__.__name__
        item_dict = dict(item)
        item_dict['spider'] = spider.name
        msg = json.dumps(item_dict, ensure_ascii=False).encode('utf-8')
        self.producer.send(topic, msg)

    @classmethod
    def from_settings(cls, settings):
        """
        :param settings: the current Scrapy settings
        :type settings: scrapy.settings.Settings
        :rtype: A :class:`~KafkaPipeline` instance
        """
        bootstrap_servers = settings.get('SCRAPY_KAFKA_HOSTS', ['localhost:9092'])
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        return cls(producer)
    # def open_spider(self, spider):
    #     self.client = pymongo.MongoClient(self.mongo_uri)
    #     self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.producer.close()
