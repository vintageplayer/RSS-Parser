from bs4 import BeautifulSoup
import requests
import re
import os
import json
import pprint
import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):

	def signal_handler(signum, frame):
		raise TimeoutException
	
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	
	try:
		yield
	finally:
			signal.alarm(0)

def get_response(url):
	hdr = {'User-Agent':'Mozilla/5.0'}
	while True:
		try:
			# Waiting for 30 seconds to receive a response object
			with time_limit(30):
				# print(f"Requesting url data : {url}")
				content	= requests.get(url,headers=hdr).content
				break
		except Exception as e:
			print('Request Timeout!!')
			raise e
		pass
	return content


def get_soup(url):
	response	= get_response(url)
	# print(f"Making soup object for : {url}")

	soup		= BeautifulSoup(response, 'lxml-xml')#'html.parser')
	# print("Returning parseable xml object")
	return soup


def store_tags(content):
	tag_set = set()

	for post in content[:1]:
		# tag_set = tag_set | set([content.name for content in post.find_all()])
		# print([content.attrs for content in post.find_all()])
		for element in post.find_all():
			if element.attrs:
				tag_set = tag_set | set([ f"{element.name}:{attr}" for attr in element.attrs])
			tag_set.add(element.name)
	print(tag_set)

			
	with open('tag_list.txt','w') as f:
		for tag in tag_set:
			# tag = re.sub('[:]','_',tag)
			f.write(f"{tag}\n")

	return tag_set

def get_tags(filename):
	with open(filename) as f:
		return [line.strip() for line in f.readlines()]

def check_tags():
	tag_set = set()
	tagFile		= 'tag_list.txt'
	tags_list = get_tags(tagFile)

	for post in content[current_max:current_max+10]:
		tags = [content.name for content in post.find_all()]
		print((set(tags) -tag_set) | (tag_set - set(tags) ))
		print(post.find('title').text)
		
		for tag in tags_list:
			try:
				line =f"{tag} : {post.find(tag).text}"
			except Exception as e:
				print(f"{tag} NOT found")
		print(tags)	
		print(tags_list)


def parse_record(record):
	details		= {}
	# for tag in record.find_all():
		# tag_name = re.sub('[:]','_',tag.name)
		# details[tag_name] = tag.text

	try:	details['title']	= record.find('title').text
	except Exception as e: details['title'] = None

	try:	details['link']	= record.find('link').text
	except Exception as e: details['link'] = None

	try:	details['enclosure_url']	= record.find('enclosure')['url']
	except Exception as e: details['enclosure_url'] = None

	try:	details['enclosure_type']	= record.find('enclosure')['type']
	except Exception as e: details['enclosure_type'] = None

	try:	details['enclosure_length']	= record.find('enclosure')['length']
	except Exception as e: details['enclosure_length'] = None

	details['media'] = []

	for media in record.find_all('media:content'):
		media	= {}
		try:	media['url']	= record.find('media:content')['url']
		except Exception as e: media['url'] = None

		try:	media['type']	= record.find('media:content')['type']
		except Exception as e: media['type'] = None

		try:	media['duration']	= record.find('media:content')['duration']
		except Exception as e: media['duration'] = None

		try:	media['lang']	= record.find('media:content')['lang']
		except Exception as e: media['lang'] = None

		try:	media['medium']	= record.find('media:content')['medium']
		except Exception as e: media['medium'] = None	

		details['media'].append(media)

	details['itunes']	= {}

	try:	details['itunes']['episode']	= record.find('itunes:episode').text
	except Exception as e: details['itunes']['episode'] = None

	try:	details['itunes']['title']	= record.find('itunes:title').text
	except Exception as e: details['itunes']['title'] = None

	try:	details['itunes']['image_href']	= record.find('itunes:image')['href']
	except Exception as e: details['itunes']['image_href'] = None

	try:	details['itunes']['duration']	= record.find('itunes:duration').text
	except Exception as e: details['itunes']['duration'] = None

	try:	details['itunes']['explicit']	= record.find('itunes:explicit').text
	except Exception as e: details['itunes']['explicit'] = None

	try:	details['itunes']['episodeType']	= record.find('itunes:episodeType').text
	except Exception as e: details['itunes']['episodeType'] = None

	try:	details['itunes']['author']	= record.find('itunes:author').text
	except Exception as e: details['itunes']['author'] = None

	try:	details['itunes']['subtitle']	= record.find('itunes:subtitle').text
	except Exception as e: details['itunes']['subtitle'] = None

	try:	details['itunes']['summary']	= record.find('itunes:summary').text
	except Exception as e: details['itunes']['summary'] = None

	try:	details['guid']	= record.find('guid').text
	except Exception as e: details['guid'] = None

	try:	details['guid_isPermaLink']	= record.find('guid')['isPermaLink']
	except Exception as e: details['guid_isPermaLink'] = None

	try:	details['dc_creator']	= record.find('dc:creator').text
	except Exception as e: details['dc_creator'] = None

	try:	details['media_rights']	= record.find('media:rights').text
	except Exception as e: details['media_rights'] = None

	try:	details['pubDate']	= record.find('pubDate').text
	except Exception as e: details['pubDate'] = None

	try:	details['content_encoded']	= record.find('content:encoded').text
	except Exception as e: details['content_encoded'] = None

	return details

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