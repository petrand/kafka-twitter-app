import time 
import numpy as np  
import pandas as pd 
import plotly.express as px  # interactive charts
import streamlit as st 
import sys 
import os 
import random
import requests 
from collections import deque

from yaml import KeyToken 


sys.path.insert(1, './../../')

from python_service.kafka_twitter_app.kafka_twitter_app import KafkaTwitterApp
import python_service.streamlit_app.utils as utils
from python_service.nlp_service.finbert import FinBERT
from python_service.nlp_service.keybert_api import KeyBERTWrapper

st.set_page_config(
    page_title="Life Twitter Tag Dashboard",
    page_icon="🤖",
    layout="wide",
)

# dashboard title
st.title("Life Twitter Tag Dashboard")


finbert = FinBERT()
keybert_wrapper = KeyBERTWrapper()
kfapp = KafkaTwitterApp()

hashtag = st.text_input("Hashtag to follow", "climate")

if st.button('Start Listening'):
    r = requests.post(url = os.environ["FLASK_API_ENDPOINT"], data = hashtag)
    st.write(f'Listening successfully for {hashtag}')

kafka_consumer = kfapp.create_consumer()
kafka_consumer.bootstrap_connected()
# creating a single-element container
placeholder = st.empty()

q_length = 100
sentiment_q = deque()
keyword_q = deque()

end_time = time.time()

counter = 1
cumm_sentiment = 0
cumm_freshness = 0
cumm_tweets_ps = 0

runn_avg_sentiment_old = 0
runn_avg_freshness_old = 0
runn_avg_tweets_ps_old = 0

for message in kafka_consumer:

    start_time = time.time()
    contents = utils.decode_message(message.value)

    # keyword 
    top_bigram, keyword_list = keybert_wrapper.predict(contents['data']['text'])
    keyword_q.append(top_bigram)
    # sentiment 
    finbert_result = finbert.predict(contents['data']['text'])
    tweet_sentiment = np.mean(finbert_result.sentiment_score)

    sentiment_q.append(tweet_sentiment)
    sentiment_df = pd.DataFrame(dict(sentiment=sentiment_q,keyword=keyword_q, index=[i for i in range(len(sentiment_q))]))


    # freshness
    created_at = contents['data']['created_at']
    freshness = utils.compute_freshness(created_at)
    delay = (start_time-end_time)
    sentiment = random.random()

    cumm_sentiment += tweet_sentiment
    cumm_freshness += freshness
    cumm_tweets_ps += delay
    

    runn_avg_sentiment = round(cumm_sentiment / counter,2)
    runn_avg_freshness = round(cumm_freshness / counter,2)
    runn_avg_tweets_ps = round(cumm_tweets_ps / counter,2)

    delta_sentiment = round(runn_avg_sentiment_old - runn_avg_sentiment, 2)
    delta_freshness = round(runn_avg_freshness_old - runn_avg_freshness, 2)
    delta_tweets_ps = round(runn_avg_tweets_ps_old - runn_avg_tweets_ps, 2)

    with placeholder.container():


        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(
            label="Sentiment",
            value=round(runn_avg_sentiment,1),
            delta=delta_sentiment,
        )

        kpi2.metric(
            label="Tweets/s",
            value=round(runn_avg_tweets_ps,1),
            delta=delta_tweets_ps
        )

        kpi3.metric(
            label="Tweet freshness (s)",
            value=round(runn_avg_freshness, 1),
            delta=delta_freshness,
        )
        graph1, graph2 = st.columns(2)
        with graph1:
            st.markdown("### Sentiment Change")
            fig2 = px.scatter(data_frame=sentiment_df, x="index", y="sentiment", trendline="lowess", trendline_options=dict(frac=0.5))
            st.write(fig2)
        with graph2:
            st.markdown("### Keywords")
            fig3 = px.treemap(sentiment_df,  path=["keyword"], values='sentiment',
                    color='sentiment',
                    color_continuous_scale='RdYlGn',
                    color_continuous_midpoint=0)
            st.write(fig3)

        col1, col2 = st.columns(2)
        with col1: 
            st.markdown("Key Words")
            st.write(keyword_list)
        with col2:
            st.markdown("Tweet contents")
            st.write(contents['data']['text'])



    runn_avg_sentiment_old = runn_avg_sentiment
    runn_avg_freshness_old = runn_avg_freshness
    runn_avg_tweets_ps_old = runn_avg_tweets_ps
    counter += 1

    if counter >= q_length:
        keyword_q.popleft()
        sentiment_q.popleft()

    end_time = time.time()


       
                  
       
     
    #time.sleep(5)


"""
# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### First Chart")
    fig = px.density_heatmap(
        data_frame=df, y="age_new", x="marital"
    )
    st.write(fig)
   
with fig_col2:
    st.markdown("### Second Chart")
    fig2 = px.histogram(data_frame=df, x="age_new")
    st.write(fig2)
"""

