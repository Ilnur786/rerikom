from flask import Flask, request, g, render_template, jsonify
from kafka import KafkaProducer
import json
from uuid import uuid4
from all_neccessary_files.jwt_token import get_token
from all_neccessary_files.database.db_sqlite import Database
import configparser
import time

app = Flask(__name__)


config_path = '../config.ini'
token = get_token(config_path)
config = configparser.ConfigParser()
config.read(config_path)


def serializer(message):
    return json.dumps(message).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'], api_version=(2,6,0)
)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database()
    return db


@app.route('/', methods=['get', 'post'])
def message_handler():
    db = get_db()
    if request.method == 'POST':
        text = request.form['message_text']
        user_id = str(uuid4())
        message_id = db.save_message(user_id, text)
        data = {"message_id": message_id}
        producer.send('sample', json.dumps(data).encode('utf-8'))
        producer.flush()
        time.sleep(0.1)
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
        data = {"message_id": message_id}
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
