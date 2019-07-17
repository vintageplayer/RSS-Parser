from bs4 import BeautifulSoup
import re
import pprint
from content_fetcher import get_response

def get_soup(url):
	response	= get_response(url)
	# print(f"Making soup object for : {url}")

	soup		= BeautifulSoup(response, 'lxml-xml')#'html.parser')
	# print("Returning parseable xml object")
	return soup

def parse_record(record):
	details		= {}
	details['itunes']	= {}
	details['media'] = []
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

	try:	details['itunes']['episode']	= record.find('itunes:episode').text
	except Exception as e: details['itunes']['episode'] = None

	details['itunes_episode'] = details['itunes']['episode']

	for media in record.find_all('media:content'):
		media_data	= {}
		media_data['itunes_episode'] = details['itunes']['episode']

		try:	media_data['url']	= media['url']
		except Exception as e: media_data['url'] = None

		try:	media_data['type']	= media['type']
		except Exception as e: media_data['type'] = None

		try:	media_data['duration']	= media['duration']
		except Exception as e: media_data['duration'] = None

		try:	media_data['lang']	= media['lang']
		except Exception as e: media_data['lang'] = None

		try:	media_data['medium']	= media['medium']
		except Exception as e: media_data['medium'] = None	

		details['media'].append(media_data)

	try:	details['itunes']['title']	= record.find('itunes:title').text
	except Exception as e: details['itunes']['title'] = None

	try:	details['itunes']['image_link']	= record.find('itunes:image')['href']
	except Exception as e: details['itunes']['image_link'] = None

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

	try:	details['media_rights']	= record.find('media:rights')['status']
	except Exception as e: details['media_rights'] = None

	try:	details['pubDate']	= record.find('pubDate').text
	except Exception as e: details['pubDate'] = None

	# try:	details['content_encoded']	= record.find('content:encoded').text
	# except Exception as e: details['content_encoded'] = None

	return details

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