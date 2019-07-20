from data_parser import get_soup, parse_record, store_tags
from db_connect import get_connection,get_max_records,execute_query
import pprint
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

get_max_query	= 'SELECT COALESCE(max(itunes_episode),0) FROM tasteofindia.posts;'
query_string	= 'INSERT INTO tasteofindia.{0} ({1}) VALUES ({2}{3});'

col_list		= {
	'posts'		: ['itunes_episode','title','link','enclosure_url','enclosure_type','enclosure_length','guid','guid_isPermaLink','dc_creator','media_rights','pubDate']
	,'itunes_data'	: ['episode','title','image_link','duration','explicit','episodeType','author','subtitle','summary']
	,'media'		: ['itunes_episode','url','type','duration','lang','medium']
}
query_strings	= {k: query_string.format(k , ','.join(col_list[k]),('%s,'*(len(col_list[k])-1) ),'%s' ) for k in col_list}

def persist_record(conn,data,tb_name):
	"""
		Format the query parameter script and records it in DB
	"""
	query_param		= tuple(list(map(lambda k : data[k],col_list[tb_name])))
	execute_query(conn,query_strings[tb_name],query_param)
	return


def persist_taste_of_india_record(conn,data):
	"""

	"""
	persist_record(conn,data,'posts')
	persist_record(conn,data['itunes'],'itunes_data')
	for media in data['media']:
		persist_record(conn,media,'media')

	conn.commit()
	return True


def process_records(content,conn):
	record_count	= len(content)

	current_max		= get_max_records(conn,get_max_query)
	print('Current Max : ',current_max)

	records = {}

	if record_count == current_max:
		print("No new records found!!")
		return records

	print(f"Total Records Found: {record_count}. Currently present: {current_max}")

	[persist_taste_of_india_record(conn,record) for record in map(parse_record, content[record_count-current_max-1::-1])]

	# for data in map(parse_record,content[record_count-current_max-1::-1]):
		# records[int(data['itunes']['episode'])] = data

	# for k in sorted(records):
		# print(k)

	return records

def update_feed_data(feed,conn):
	content			= get_soup(feed)

	print(f"Processing Records for : {feed}")
	records			= content.find_all('item')

	process_records(records,conn)

	# store_tags(records)
	return

def begin(feed_url,db_credential_file):
	try:
		connection = get_connection(db_credential_file)
		update_feed_data(feed_url,connection)
	except Exception as e:
		print('Error Received...')
		print(e)
	finally:
		print('Closing connection')
		connection.close()

if __name__ == '__main__':

	feed_url		= 'https://audioboom.com/channels/4930693.rss'
	db_credentials	= 'connection.json'

	print('Main Script Running...')

	begin(feed_url,db_credentials)

	scheduler = BlockingScheduler()
	# scheduler	= BackgroundScheduler()
	scheduler.add_job(begin, 'interval',[feed_url,db_credentials], hours=12)

	try:
		scheduler.start()
	except Exception as e:
		print('Stopping Schedule!!')
	
	print('Main Script Exiting!!')
