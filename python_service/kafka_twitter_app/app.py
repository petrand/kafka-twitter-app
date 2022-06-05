from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import sys
import os

sys.path.insert(1, './../../')

from python_service.kafka_twitter_app.kafka_twitter_app import KafkaTwitterApp

app = Flask(__name__)


kfapp = KafkaTwitterApp()

@app.route("/set-hashtag", methods=['POST'])

def set_hashtag():
    hashtag = request.get_json()
    rules = [{"value": hashtag, "tag": hashtag}] 
    topic_name = os.environ.get("TOPIC_NAME")

    kfapp.start_stream(rules, topic_name)   
    
    return f"All goood. Following new hashtag: {hashtag}"
