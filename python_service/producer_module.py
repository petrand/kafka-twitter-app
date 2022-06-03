# Adapted from https://towardsdatascience.com/using-kafka-to-optimize-data-flow-of-your-twitter-stream-90523d25f3e8
# Thanks to Variable for the awesome quickstart 

import os


"""API KEYS"""

api_key = os.environ['API_KEY']
api_key_secret = os.environ['API_KEY_SECRET']
bearer_token = os.environ['BEARER_TOKEN']

import tweepy
from tweepy import StreamingClient
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='broker:29092') #Same port as your Kafka server


topic_name = "twitterdata"


class twitterClient(): 
    """
    Setup twitter api client
    """
    def get_twitter_client(self, bearer_token):
        client = tweepy.Client(bearer_token)
        return client


stream_client = StreamingClient(bearer_token)
x = stream_client.add_rules(dry_run=True)
print(x)

#class twitterAuth():
#    """SET UP TWITTER AUTHENTICATION"""

#    def authenticateTwitterApp(self):
#        auth = tweepy.Client(bearer_token)
#        auth.set_access_token(access_token, access_token_secret)
#        return auth


'''

class TwitterStreamer():

    """SET UP STREAMER"""
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.twitterClient = twitterClient()

    def stream_tweets(self):
        while True:
            listener = ListenerTS() 
            auth = self.twitterClient.get_twitter_client(self.bearer_token)
            stream = Stream(auth, listener)
            stream.filter(track=["Apple"], stall_warnings=True, languages= ["en"])


class ListenerTS(StreamListener):

    def on_data(self, raw_data):
            producer.send(topic_name, str.encode(raw_data))
            return True


if __name__ == "__main__":
    TS = TwitterStreamer(bearer_token)
    TS.stream_tweets()

'''