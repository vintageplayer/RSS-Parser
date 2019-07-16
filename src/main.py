from data_parser import get_soup, parse_record, store_tags

def process_records(content):
	record_count	= len(content)
	current_max				= 0
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

def update_feed_data(feed):
	content			= get_soup(feed)

	print(f"Processing Records for : {feed}")
	records			= content.find_all('item')

	process_records(records)

	# store_tags(records)
	return


if __name__ == '__main__':
	feed_url = 'https://audioboom.com/channels/4930693.rss'
	# print('Main Script Running...')

	update_feed_data(feed_url)

	# print('Main Script Exiting!!')