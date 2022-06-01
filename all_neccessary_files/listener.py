import json
from kafka import KafkaConsumer
import requests as req
from jwt_token import get_token

token = get_token()


def check_message(message_id, message_text):
    trigger = "АБРАКАДАБРА"
    if trigger not in message_text and trigger.lower() not in message_text:
        status = 'correct'
    else:
        status = 'blocked'
    send_status(message_id, status)


def send_status(message_id, status):
    payload = {"message_id": message_id, "status": status}
    header = {"Authorization": token, "Content-type": "application/json"}
    url = 'http://127.0.0.1:5555/api/v1/message_confirmation'
    r = req.post(url=url, data=json.dumps(payload), headers=header)



if __name__ == '__main__':
    # Kafka Consumer
    consumer = KafkaConsumer(
        'sample',
        bootstrap_servers='localhost:9092'
    )
    for message in consumer:
        decode_message = json.loads(message.value.decode())
        print(decode_message)
        message_id = decode_message['message_id']
        message_text = decode_message['message_text']
        check_message(message_id, message_text)

