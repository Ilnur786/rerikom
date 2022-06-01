import sqlite3
import os


# название дб можно написать в конфиг, а от туда загружать его в переменные среды

class Database(object):
	_instance = None

	def __init__(self, db_name):
		self.db_name = db_name
		connection = self._connection()
		print("db was created or loaded")
		cursor_obj = connection.cursor()
		try:
			# create table
			cursor_obj.execute(
				"create table if not exists Messages(MessageId INTEGER PRIMARY KEY, UserId text, MessageText text, MessageStatus text)")
		except sqlite3.OperationalError as e:
			print(e)
			pass
		else:
			connection.commit()
			connection.close()

	@staticmethod
	def create(db_name='test.db'):
		if Database._instance is None:
			Database._instance = Database(db_name)
		return Database._instance

	def _connection(self):
		connection = sqlite3.connect(self.db_name)
		return connection

	def save_message(self, user_id, message_text):
		con = self._connection()
		with con:
			cursor_obj = con.cursor()
			cursor_obj.execute("insert into Messages(UserId, MessageText, MessageStatus) values(?, ?, ?)",
							   (user_id, message_text, 'review'))
		message_id = cursor_obj.lastrowid
		return message_id

	# @staticmethod
	# def review_status(message_id):
	# 	trigger = "АБРАКАДАБРА"
	# 	d = decode_jwt(message_id)
	# 	if trigger not in d['text'] or trigger.lower() not in d['text']:
	# 		status = 'correct'
	# 	else:
	# 		status = 'blocked'
	# 	return status

	# def change_status(self, message_id):
	# 	status = review_status(message_id)
	# 	with self.connection:
	# 		cursor_obj = self.connection.cursor()
	# 		cursor_obj.execute("update Messages set status = ? where message_id = ?", (status, message_id))

	def get_entries(self):
		con = self._connection()
		with con:
			cursor_obj = con.cursor()
			rows = cursor_obj.execute("select * from Messages").fetchall()
		return rows

	def update_status(self, message_id, status):
		con = self._connection()
		with con:
			cursor_obj = con.cursor()
			cursor_obj.execute("update Messages set MessageStatus = ? where MessageId = ?", (status, message_id))


# def create_db(db_name='test.db'):
# 	sqlite_connection = sqlite3.connect
# 	sqlite_connection = sqlite_connection(db_name)
# 	print("db was created or loaded")
# 	cursor_obj = sqlite_connection.cursor()
# 	try:
# 		# create table
# 		cursor_obj.execute("create table User_Message(MessageId text primary key, UserId integer)")
# 		cursor_obj.execute(
# 			"create table Message_Text_Status(MessageId text primary key, MessageText text, Status text)")
# 	except sqlite3.OperationalError:
# 		pass
# 	else:
# 		sqlite_connection.commit()
#
#
# def get_connection_to_db(db_name='test.db'):
# 	sqlite_connection = sqlite3.connect(db_name)
# 	return sqlite_connection
#
#
# def save_message(user_id, message_text, db_name='test.db'):
# 	message_id = encode_jwt(user_id, message_text)
# 	sqlite_connection = sqlite3.connect(db_name)
# 	with sqlite_connection:
# 		cursor_obj = sqlite_connection.cursor()
# 		cursor_obj.execute("insert into User_Message(MessageId, UserId) values(?, ?)", (message_id, user_id))
# 		cursor_obj.execute("insert into Message_Text_Status(MessageId, MessageText, Status) values(?, ?, ?)",
# 						   (message_id, message_id, 'review'))
#
#
# def review_status(message_id):
# 	trigger = "АБРАКАДАБРА"
# 	d = decode_jwt(message_id)
# 	if trigger not in d['text'] or trigger.lower() not in d['text']:
# 		status = 'correct'
# 	else:
# 		status = 'blocked'
# 	return status
#
#
# def change_status(message_id, db_name='test.db'):
# 	status = review_status(message_id)
# 	sqlite_connection = sqlite3.connect(db_name)
# 	with sqlite_connection:
# 		cursor_obj = sqlite_connection.cursor()
# 		cursor_obj.execute("update Message_Text_Status set status = ? where message_id = ?", (status, message_id))
