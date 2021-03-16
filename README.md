## Setting up database
Run these commands. Make sure you have correct rights (sudo).
```
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec db psql -U postgres -f /scripts/crawldb.sql
```
If you already have folder `database/target/`, then you do not need to run the second command, since the database already exists.

## Running crawler
For setting up all dependencies run this first.
```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

For starting crawler run this command:
```
python3 app
```