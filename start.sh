#!/bin/bash
docker network create rss

docker run -d --name rss-postgres \
	--net=rss \
	-e POSTGRES_DB=audioboom \
	-e POSTGRES_PASSWORD=parserssfeed \
	-p 5432:5432 \
	-v $(PWD):/home \
	-w /home  \
	postgres


docker run -dt --name rss-python \
	--net=rss \
	-p 8888:8888 \
	-p 8889:8889 \
	-v $(PWD)/src:/home/src \
	-w /home/src  \
	conda/miniconda3-centos6 bash

docker exec rss-python conda update -c base -c defaults conda
docker exec rss-python conda install beautifulsoup4 lxml psycopg2
docker exec rss-python conda install -c conda-forge apscheduler

docker exec -it rss-postgres psql -U postgres -d audioboom -f create_db.sql

docker exec -d rss-python python main.py