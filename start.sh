#!/bin/bash
docker run -dt --name rss-python \
	-p 8888:8888 \
	-p 8889:8889 \
	-v $(PWD)/src:/home/src \
	-w /home/src  \
	conda/miniconda3-centos6 bash

docker exec rss-python conda update -c base -c defaults conda
docker exec rss-python conda install beautifulsoup4

docker run -d --name rss-postgres \
 -e POSTGRES_DB=audioboom \
 -e POSTGRES_PASSWORD=parserssfeed \
 -p 5432:5432 \
 -v $(PWD):/home \
 -w /home  \
 postgres

docker exec -it rss-postgres psql -U postgres -f create_db.sq

docker exec rss-python python main.py