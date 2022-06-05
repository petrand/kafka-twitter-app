import os 
import sys
import json 

sys.path.insert(1, './../../')

import python_service.kafka_twitter_app.twitter_api as twitter_api
import python_service.kafka_twitter_app.kafka_api as kafka_api



class KafkaTwitterApp:
    def __init__(self):
        self.bearer_token = os.environ.get("BEARER_TOKEN")
        self.bootstrap_servers = [os.environ.get("BOOTSTRAP_SERVER")]
        self.topics = [os.environ.get("TOPIC_NAME")]


    def create_producer(self):
        producer = kafka_api.get_kafka_producer(bootstrap_servers=self.bootstrap_servers)
        return producer

    def create_consumer(self, topics=[os.environ.get("TOPIC_NAME")]):
        consumer = kafka_api.get_kafka_consumer(bootstrap_servers=self.bootstrap_servers, topics=topics)
        return consumer

    def create_stream(self, rules):

        old_rules = twitter_api.get_rules()
        stream_clean = twitter_api.delete_all_rules(old_rules)
        stream_set_rules = twitter_api.set_rules(stream_clean, rules)

        return stream_set_rules

    def start_stream(self, rules, topic_name): 
        
        stream_set_rules = self.create_stream(rules)
        # create producer 
        producer = self.create_producer()
        # create stream
        twitter_api.get_stream(stream_set_rules, topic_name, producer)

    def stop_stream(self):
        old_rules = twitter_api.get_rules()
        stream_clean = twitter_api.delete_all_rules(old_rules)
        return 

def decode_message(msg):
    msg_string =msg.decode('utf-8')

    msg_json = json.loads(msg_string)
    return msg_json


#for message in consumer:
#    print(message.topic, message.value)

if __name__ == "__main__":

    kfapp = KafkaTwitterApp()
    #hashtag_consumer = kfapp.create_consumer(topics="hashtag")

    #for message in hashtag_consumer:

    twitter_tag = 'tesla'
    rules = [{"value": twitter_tag, "tag": twitter_tag}]
    topic_name = os.environ.get("TOPIC_NAME")

    kfapp.start_stream(rules, topic_name)   