import time 
import numpy as np  
import pandas as pd 
import plotly.express as px  # interactive charts
import streamlit as st 
import sys 
import os 

sys.path.insert(1, './../../')

from python_service.kafka_twitter_app.kafka_twitter_app import KafkaTwitterApp

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


for message in kafka_consumer:
    #message.topic, message.value
    with placeholder.container():
        st.write(message.value)

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
            value=int(count_married),
            delta=-10 + count_married,
        )

        kpi2.metric(
            label="Tweet freshness",
            value=int(count_married),
            delta=-10 + count_married,
        )


       
        avg_age += 1
        count_married += 1
       
     
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

