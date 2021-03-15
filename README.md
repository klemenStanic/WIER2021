## Setting up database
Run these commands. Make sure you have correct rights (sudo).
```
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec db psql -U postgres -f /scripts/crawldb.sql
```
If you already have folder `database/target/`, then you do not need to run the second command, since the database already exists.