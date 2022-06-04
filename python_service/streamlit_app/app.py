import time 
import numpy as np  
import pandas as pd 
import plotly.express as px  # interactive charts
import streamlit as st 
import sys 
import os 
import random

sys.path.insert(1, './../../')

from python_service.kafka_twitter_app.kafka_twitter_app import KafkaTwitterApp
import python_service.streamlit_app.utils as utils

st.set_page_config(
    page_title="Life Twitter Tag Dashboard",
    page_icon="🤖",
    layout="wide",
)

# dashboard title
st.title("Life Twitter Tag Dashboard")

# top-level filters
#twitter_tag = st.selectbox("Select the Job", ['cat', 'dog', 'banana'])
twitter_tag = "dog"
rules = [{"value": twitter_tag, "tag": twitter_tag}]
topic_name = os.environ.get("TOPIC_NAME")


kfapp = KafkaTwitterApp()

kafka_consumer = kfapp.create_consumer()
kafka_consumer.bootstrap_connected()
# creating a single-element container
placeholder = st.empty()


sentiment_arr = [0 for i in range(0,100)]

end_time = time.time()

counter = 1
cumm_sentiment = 0
cumm_freshness = 0
cumm_tweets_ps = 0

runn_avg_sentiment_old = 0
runn_avg_freshness_old = 0
runn_avg_tweets_ps_old = 0

for message in kafka_consumer:

    sentiment_arr[counter%100] = random.random()
    #message.topic, message.value
    start_time = time.time()
    contents = utils.decode_message(message.value)

    # freshness
    created_at = contents['data']['created_at']
    freshness = utils.compute_freshness(created_at)
    delay = (start_time-end_time)
    sentiment = random.random()

    cumm_sentiment += 0
    cumm_freshness += freshness
    cumm_tweets_ps += delay
    

    runn_avg_sentiment = 0 
    runn_avg_freshness = round(cumm_freshness / counter,2)
    runn_avg_tweets_ps = round(cumm_tweets_ps / counter,2)

    delta_sentiment = round(runn_avg_sentiment_old - runn_avg_sentiment, 2)
    delta_freshness = round(runn_avg_freshness_old - runn_avg_freshness, 2)
    delta_tweets_ps = round(runn_avg_tweets_ps_old - runn_avg_tweets_ps, 2)

    with placeholder.container():

        


        avg_age = 10
        count_married = 10

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(
            label="Sentiment",
            value=round(avg_age),
            delta=round(avg_age) - 10,
        )

        kpi2.metric(
            label="Tweets/s",
            value=round(start_time-end_time,1),
            delta=delta_tweets_ps
        )

        kpi3.metric(
            label="Tweet freshness (s)",
            value=round(runn_avg_freshness, 1),
            delta=delta_freshness,
        )

        st.markdown("### Second Chart")
        fig2 = px.line(data_frame=pd.DataFrame([sentiment_arr, [i for i in range(0,100)]], columns=['Sentiment', 'Index']), x="index", y="Sentiment")
        st.write(fig2)

        st.write(contents)


    runn_avg_sentiment_old = runn_avg_sentiment
    runn_avg_freshness_old = runn_avg_freshness
    runn_avg_tweets_ps_old = runn_avg_tweets_ps
    counter += 1

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

