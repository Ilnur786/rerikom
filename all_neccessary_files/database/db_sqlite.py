import sqlite3


class Database(object):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			cls._instance.__initial = False
		return cls._instance

	def __init__(self, db_name='test.db'):
		if self.__initial:
			return
		self.__initial = True
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

	def get_message_text_by_id(self, message_id):
		con = self._connection()
		with con:
			cursor_obj = con.cursor()
			cursor_obj.execute("select MessageText from Messages where MessageId = ?", (str(message_id),))
			message_text = cursor_obj.fetchone()[0]
		return message_text
