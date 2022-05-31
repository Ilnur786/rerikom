import jwt
import configparser
import time


def encode_jwt(user_id, text, timestamp=None):
	config = configparser.ConfigParser()
	config.read("config.ini")
	key = config['JWT']['key']
	algorithm = config['JWT']['algorithm']
	if timestamp is None:
		timestamp = str(time.time())
	payload = {"user_id": user_id, "text": text, "timestamp": timestamp}
	encoded = jwt.encode(payload, key, algorithm)
	return encoded


def decode_jwt(encoded):
	config = configparser.ConfigParser()
	config.read("config.ini")
	key = config['JWT']['key']
	algorithm = config['JWT']['algorithm']
	return jwt.decode(encoded, key, algorithm)

