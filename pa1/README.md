# WebCrawler
## Setting up database
Our database backup is located on this link. We couldn't upload it to github because it's to large.
https://drive.google.com/file/d/1D4m2isYIRqKJL64mH-kaQP5KM4yLOugT/view?usp=sharing


Run these commands. Make sure you have correct rights (sudo).
```
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec db psql -U postgres -f /scripts/crawldb.sql
```
If you already have folder `database/target/`, then you do not need to run the second command, since the database already exists.

## Running crawler
To install all required dependencies run this first:
```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

For starting crawler run this command:
```
python3 app
```

Configuration of the crawler is in `app/config.py`. Database configuration for crawler is in `app/models.py`.


## Database scheme
![DatabaseScheme](images/db_scheme.png)

## How it works
The webcrawler is composed of several separate entities, that work together.
Crawler scheme is presented below.
Each part of crawler is explained below.

![CrawlerScheme](images/crawler_scheme.png)

### Scheduler
Schedulers main function is to throttle the number of calls to a certain domain and ip address.
It's configured to allow a single visit of a site every 5 seconds.
This class can be called with `seed_path` parameter, where if given it inserts sites written in seed file into site table of database.
At each call of `Scheduler.get_free_site()` method, scheduler updates sites in db with ip addresses if they are not there already and selects site which is not finished with crawling and has not been visited in the last 5 seconds and returns it.
After the crawling site has been selected, `Scheduler.update_timestamp(<site_id>)` should be called, where all sites in database with the same ip address have their timestamp updated to current time and thus are delayed from crawling for 5 seconds.
If the site has been fully crawled it should be updated in database with `Scheduler.remove_site(<site_id>)` method, where this site is marked as done.

### Frontier
Frontiers main function is to select the next page to crawl and its main method is `Frontier.get_next_url()`.
In this method first `Frontier` gets which site to crawl from `Scheduler`, then it checks which pages is next to be crawled. Such pages are marked as `FRONTIER` in `Page.page_type_code` parameter.
If there are none, it inserts a root page into database with url equal to the sites domain.
Once the page has been selected, it checks if sitemap and robots.txt are saved for given site and downloads them if they are not.
Then it checks if pages url can be crawled based on robots.txt rules, if they do not allow crawling, its marked as `DISALLOWED` and a new page is selected.
Finally the site is marked with `Scheduler.update_timestamp(<site_id>)`

### Crawler
This is main method of the crawler. Its initializes `Frontier` and selected number of workers, which is determined in config file.
Crawler continues to get pages to crawl from Frontier and passes them to `PageHandlers` to crawl them.
In case `PageHandler` runs into any sort of trouble, it marks this page as `ERROR` and continues its work.

### PageHandler
