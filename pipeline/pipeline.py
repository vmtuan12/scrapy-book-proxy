from kafka import KafkaProducer
import pipeline.topic as topic
import json

class KafkaConnector:

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:29092'], 
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def close(self):
        self.producer.close()

    def send(self, msg: dict, topic=topic.TOPIC_BOOK):
        # to do
        self.producer.send(topic, value=msg)
        self.producer.flush()