#!/bin/bash
docker exec rss-postgres psql -U postgres -d audioboom -a -f query_status.sql