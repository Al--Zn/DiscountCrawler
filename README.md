# DiscountCrawler

A Crawler for fetching discount data

----

### Requirement

- python 2.7
- scrapy 0.24
- scrapyd

----

### Usage

1. Make sure you have successfully installed `python2.7`, `scrapy` and `scrapyd`
2. In your terminal, use the command `scrapy crawl <spider_name>` to crawl data
3. Available spider_name: `jd`(for data on jd.com), `smzdm`(for data on smzdm.com)
4. To ensure the data is up-to-date, you may use the `crontab` command in your Unix-like system to run the command periodically (i.e. every 1 hour) 