import jwt
import configparser
import time


# def encode_jwt(user_id, text, timestamp=None):
# 	config = configparser.ConfigParser()
# 	config.read("config.ini")
# 	key = config['JWT']['key']
# 	algorithm = config['JWT']['algorithm']
# 	if timestamp is None:
# 		timestamp = str(time.time())
# 	payload = {"user_id": user_id, "text": text, "timestamp": timestamp}
# 	encoded = jwt.encode(payload, key, algorithm)
# 	return encoded
#
#
# def decode_jwt(encoded):
# 	config = configparser.ConfigParser()
# 	config.read("config.ini")
# 	key = config['JWT']['key']
# 	algorithm = config['JWT']['algorithm']
# 	return jwt.decode(encoded, key, algorithm)

### А ВООБЩЕ ПРОСТО НАДО СГЕНЕРИРОВАТЬ ТОКЕН И СДЕЛАТЬ ЕГО ПЕРЕМЕННОЙ СРЕДЫ И ВСЕ! ###
def create_token(config_path='config.ini'):
	config = configparser.ConfigParser()
	config.read(config_path)
	key = config['JWT']['key']
	algorithm = config['JWT']['algorithm']
	jwt_token = jwt.encode({"post_message_confirm": True}, key, algorithm)
	with open(config_path, 'a') as f:
		f.write(f'\njwt_token = {jwt_token}')
	return jwt_token


def get_token(config_path='config.ini'):
	config = configparser.ConfigParser()
	config.read(config_path)
	jwt_token = config['JWT'].get('jwt_token')
	if jwt_token is None:
		jwt_token = create_token(config_path)
	return jwt_token


def decode_jwt(encoded, config_path='config.ini'):
	config = configparser.ConfigParser()
	config.read("config.ini")
	key = config['JWT']['key']
	algorithm = config['JWT']['algorithm']
	try:
		jwt_token = jwt.decode(encoded, key, algorithm)["post_message_confirm"]
	except jwt.exceptions.InvalidSignatureError:
		jwt_token = False
	except jwt.exceptions.InvalidAlgorithmError:
		jwt_token = False
	return jwt_token

