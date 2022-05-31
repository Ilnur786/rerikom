from flask import Flask, request, session, g, render_template
from db_sqlite import Database
from kafka import KafkaProducer
import json
from uuid import uuid4
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
def message():
    if request.method == 'POST':
        # data = request.get_json()
        # text = data['text']
        text = request.form['message_text']
        # user_id = data['user_id']
        user_id = str(uuid4())
        db = get_db()
        message_id = db.save_message(user_id, text)
        data = {"user_id": user_id, "message_id": message_id}
        producer.send('sample', json.dumps(data).encode('utf-8'))
        producer.flush()
        return render_template('index.html', data=db.get_entries())
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7777)