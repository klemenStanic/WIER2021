#!/bin/bash

echo "—> Stopping db container"
docker stop wier2021_db_1
docker rm wier2021_db_1

echo "—> Removing db target data"
rm -r ./database/target

echo "—> Creating new db container"
docker-compose -f docker-compose.yml up -d
sleep 5
docker-compose -f docker-compose.yml exec db psql -U postgres -f /scripts/crawldb.sql
