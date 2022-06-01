from flask import Flask, request, session, g, render_template, jsonify
from db_sqlite import Database
from kafka import KafkaProducer
import json
from uuid import uuid4
from jwt_token import get_token
import os
import configparser
app = Flask(__name__)



# with serializer function inside
# def serializer(message):
#     return json.dumps(message).encode('utf-8')
#
#
# producer = KafkaProducer(
#     bootstrap_servers=['localhost:9092'],
#     value_serializer=serializer
# )

config_path = 'config.ini'
token = get_token(config_path)
config = configparser.ConfigParser()
config.read(config_path)
# db_name = config['DATABASE']['db_name']


def serializer(message):
    return json.dumps(message).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'], api_version=(2,6,0)
)


def get_db():
    """ Возвращает объект соединения с БД"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database.create()
    return db


@app.route('/', methods=['get', 'post'])
def message_handler():
    db = get_db()
    if request.method == 'POST':
        text = request.form['message_text']
        user_id = str(uuid4())
        message_id = db.save_message(user_id, text)
        data = {"message_id": message_id, "message_text": text}
        producer.send('sample', json.dumps(data).encode('utf-8'))
        producer.flush()
        return render_template('index.html', data=db.get_entries())
    else:
        return render_template('index.html', data=db.get_entries())


@app.route('/api/v1/message', methods=['get', 'post'])
def message():
    if request.method == 'POST':
        data = request.get_json()
        message_text = data['message_text']
        user_id = data['user_id']
        db = get_db()
        message_id = db.save_message(user_id, message_text)
        data = {"message_id": message_id, "message_text": message_text}
        producer.send('sample', json.dumps(data).encode('utf-8'))
        producer.flush()
        return jsonify(data)
    else:
        return 'Available method is POST'


@app.route('/api/v1/message_confirmation', methods=['get', 'post'])
def message_confirmation():
    if request.method == 'POST':
        data = request.get_json()
        received_token = request.headers.get('Authorization')
        if token == received_token:
            message_id = data['message_id']
            status = data['status']
            db = get_db()
            db.update_status(message_id, status)
            return f'Status of Message with id={message_id} was updated to the {status}'
        else:
            return "Authorization token wasn't given or incorrect"
    else:
        return 'Available method is POST'


if __name__ == '__main__':
    print(token)
    app.run(host='127.0.0.1', port=5555)