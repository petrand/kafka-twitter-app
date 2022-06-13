from kafka import KafkaProducer
from kafka import KafkaConsumer


def get_kafka_producer(bootstrap_servers=['broker:29029']):
    '''
    This function generates a kafka producer that will send data to a topic

    Inputs: 
        - bootstrap_servers: list, urls and ports on which the kafka server is running.
            When running in docker container those will  be the name of service container and its port, e.g. ['broker:29029']
    Outputs:
        - producer: KafkaProducer, configured instance of kafka producer 
    '''

    # setup kafka producer
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    
    if producer.bootstrap_connected() != True:
        raise Exception(f"Failed to connect to bootstrap server")

    #return producer 
    return producer

def get_kafka_consumer(bootstrap_servers=['broker:29092'], topics=['twitterdata']):
    '''
    This function generates a kafka consumer that will be able
    to consume data from a specified topic from a specified kafka procuder

    Inputs:
        - bootstrap_servers: list, urls and ports on which kafka server is running. 
            When running in docker container those will  be the name of service container and its port, e.g. ['broker:29029']
        - topics: list, names of topics to which consumer will subscribe. e.g. ['twitterdata']. 
    Outputs:
        - consumer: KafkaConsumer, configured instance of kafka consumer 
    '''

    # setup kafka consumer 
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
    consumer.subscribe(topics=topics)

    # check if correctly subsribed to all topics
    #print(consumer.topics(), topics)
    #if consumer.topics() != topics:
    #    raise Exception(f"Failed to subscribe to all topics, check permissions. Currently subscribe topics are {consumer.topics()}")
    
    # return kafka consumer 
    return consumer