from confluent_kafka.admin import AdminClient, NewTopic

a = AdminClient({'bootstrap.servers': '192.168.70.40:9092'})
#new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in ["toAnalyze", "toUI"]]

#a.create_topics(new_topics)

print(a.list_topics().topics)

