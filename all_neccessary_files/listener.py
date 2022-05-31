import json
from kafka import KafkaConsumer


if __name__ == '__main__':
    # Kafka Consumer
    consumer = KafkaConsumer(
        'sample',
        bootstrap_servers='localhost:9092'
    )
    for message in consumer:
        print(json.loads(message.value.decode()))
