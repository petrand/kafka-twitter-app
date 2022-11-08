from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import sys
import os
import numpy as np

sys.path.insert(1, './../../')

from python_service.kafka_twitter_app.kafka_twitter_app import KafkaTwitterApp
import python_service.streamlit_app.utils as utils
from python_service.nlp_service.finbert import FinBERT
from python_service.nlp_service.keybert_api import KeyBERTWrapper


app = Flask(__name__)

finbert = FinBERT()
keybert_wrapper = KeyBERTWrapper()
kfapp = KafkaTwitterApp()

@app.route("/set-hashtag", methods=['POST'])

def set_hashtag():
    hashtag = request.get_data().decode('utf-8')
    print(hashtag)
    hashtag += " lang:en"
    rules = [{"value": hashtag, "tag": hashtag}] 
    topic_name = os.environ.get("TOPIC_NAME")

    kfapp.start_stream(rules, topic_name)   
    
    return f"All good. Following new hashtag: {hashtag}"

@app.route("/stop-listening", methods=['POST'])

def stop():
    kfapp.stop_stream()
    return f"All good. Stopped the stream"

@app.route("/get-keywords", methods=['GET'])

def get_keywords():

    text = request.get_data().decode('utf-8')
    top_bigram, keyword_list = keybert_wrapper.predict(text)
    return {"top_bigram": top_bigram, "keyword_list":keyword_list}

@app.route("/get-sentiment", methods=['GET'])

def get_sentiment():

    text = request.get_data().decode('utf-8')
    finbert_result = finbert.predict(text)
    tweet_sentiment = np.mean(finbert_result.sentiment_score)
    return {"tweet_sentiment": float(tweet_sentiment)}

if __name__ == "__main__":
    print("app.running")
    app.run(host='0.0.0.0',debug=False,port='5001')