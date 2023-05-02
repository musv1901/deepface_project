from confluent_kafka import Consumer, Producer

conf = {
    'bootstrap.servers': 'pkc-75m1o.europe-west3.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'QCAARICNTEWCKZFG',
    'sasl.password': 'xr83il99N0MmvyGctKgVzW4uEdMAY4J7FDh4CQ46LJ1phfS92GHKIqwkd8xlVuhU',
    'auto.offset.reset': 'earliest',
    'group.id': 'python_group1'
}

consumer = Consumer(conf)
consumer.subscribe(["toAnalyze"])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting...")
        elif msg.error():
            print("ERROR: %s".format(msg.error()))
        else:
            # Extract the (optional) key and value, and print.
            print("Test")
except KeyboardInterrupt:
    pass
finally:
    ##Leave group and commit final offsets
    consumer.close()
