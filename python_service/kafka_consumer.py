from kafka import KafkaConsumer


consumer = KafkaConsumer(bootstrap_servers='broker:29092')
consumer.subscribe(topics=['twitterdata'])
print(consumer.topics())
print(consumer.bootstrap_connected())
print(consumer.partitions_for_topic('twitterdata'))
#print(consumer.poll())
topic_parition_tuple = list(consumer.assignment())[0]
print(consumer.position(topic_parition_tuple))
#print(consumer.poll())

for message in consumer:
    print(message.topic, message.value)