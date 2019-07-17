import psycopg2
import json


def get_connection(file):
	with open(file) as inFile:
		creds	= json.load(inFile)

	database	= creds['database']
	user		= creds['user']
	password	= creds['password']
	host		= creds['host']
	port		= creds['port']

	connection	= psycopg2.connect(database=database,user=user,password=password,host=host,port=port)

	return connection


def get_max_records(conn,query):
	cursor	= conn.cursor()
	try:
		cursor.execute(query)
		record = cursor.fetchone()
		print('Record received: ',record)
	finally:
		cursor.close()
	return record[0]


def execute_query(conn,query,params):
	try:
		cursor	= conn.cursor()
		cursor.execute(query,params)
	except Exception as e:
		raise e
	finally:
		cursor.close()

if __name__ == '__main__':
	get_max_query = 'SELECT COALESCE(max(episode),0) FROM tasteofindia.itunes_data;'
	# get_max_query = 'SELECT * FROM tasteofindia.posts;'
	conn = get_connection('connection.json')
	print(get_max_records(conn,get_max_query))