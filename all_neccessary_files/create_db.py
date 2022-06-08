def create_db():
	import sqlite3
	import configparser
	config_path = 'config.ini'
	config = configparser.ConfigParser()
	config.read(config_path)
	db_name = config['Database']['db_name']
	connection = sqlite3.connect(db_name)
	cursor_obj = connection.cursor()
	cursor_obj.execute(
		"create table if not exists Messages(MessageId INTEGER PRIMARY KEY, UserId text, MessageText text, MessageStatus text)")
	connection.commit()
	connection.close()


if __name__ == '__main__':
	create_db()
