FROM ubuntu:20.04
RUN apt-get update 
# getting python
RUN apt install -y python3-pip
RUN pip install tweepy