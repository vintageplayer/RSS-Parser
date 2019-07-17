import psycopg2
import json


def get_connection(file):
	with open('connection.json') as inFile:
		creds	= json.load(inFile)

	database	= creds['database']
	user		= creds['user']
	password	= creds['password']
	host		= creds['host']
	port		= creds['port']

	connection	= psycopg2.connect(database=database,user=user,password=password,host=host,port=port)

	return connection

def execute_query(conn,query_string):
	return