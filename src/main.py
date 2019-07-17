from data_parser import get_soup, parse_record, store_tags
from db_connect import get_connection,get_max_records

get_max_query = 'SELECT COALESCE(max(episode),0) FROM tasteofindia.itunes_data;'

def process_records(content,conn):
	record_count	= len(content)

	current_max		= get_max_records(conn,get_max_query)
	print('Current Max : ',current_max)

	records = {}

	if record_count == current_max:
		print("No new records found!!")
		return records

	print(f"Total Records Found: {record_count}. Currently present: {current_max}")

	for data in map(parse_record,content[record_count-current_max-1::-1]):
		records[int(data['itunes']['episode'])] = data

	# for k in sorted(records):
		# print(k)

	return records

def update_feed_data(feed,conn):
	content			= get_soup(feed)

	# print(f"Processing Records for : {feed}")
	records			= content.find_all('item')

	process_records(records,conn)

	# store_tags(records)
	return

def begin(feed_url,db_credential_file):
	try:
		connection = get_connection(db_credential_file)
		update_feed_data(feed_url,connection)
	except Exception as e:
		print(e)
	finally:
		connection.close()

if __name__ == '__main__':
	feed_url		= 'https://audioboom.com/channels/4930693.rss'
	db_credentials	= 'connection.json'

	print('Main Script Running...')
	begin(feed_url,db_credentials)
	print('Main Script Exiting!!')