FROM ubuntu:20.04
RUN apt-get update 
# getting python
RUN apt install -y python3-pip
RUN pip install tweepy
RUN pip install kafka-python
RUN pip install streamlit
RUN pip install plotly
RUN pip install transformers
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install nltk
# RUN streamlit run app.py --server.port 8051