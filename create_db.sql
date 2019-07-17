BEGIN;

CREATE SCHEMA tasteofindia;

CREATE TABLE tasteofindia.itunes_data
(
	episode INT PRIMARY KEY
	,title VARCHAR(256)
	,image_link VARCHAR(512)
	,duration INT
	,explicit VARCHAR(10)
	,episodeType VARCHAR(10)
	,author VARCHAR(128)
	,subtitle VARCHAR(512)
	,summary VARCHAR(512)
);

CREATE TABLE tasteofindia.media
(
	itunes_episode INT
	,url VARCHAR(512)
	,type VARCHAR(64)
	,duration INT
	,lang VARCHAR(10)
	,medium VARCHAR(10)
	,FOREIGN KEY (itunes_episode) REFERENCES tasteofindia.itunes_data(episode)
);

CREATE TABLE tasteofindia.posts
(
	itunes_episode INT PRIMARY KEY
	,title VARCHAR(256)
	,link VARCHAR(512)
	,enclosure_url VARCHAR(512)
	,enclosure_type VARCHAR(64)
	,enclosure_length VARCHAR(64)
	,guid VARCHAR(512)
	,guid_isPermaLink boolean
	,dc_creator VARCHAR(256)
	,media_rights VARCHAR(32)
	,pubDate TIMESTAMP WITH TIME ZONE
	,content_encoded VARCHAR(512)
	,FOREIGN KEY (itunes_episode) REFERENCES tasteofindia.itunes_data(episode)
);

COMMIT;