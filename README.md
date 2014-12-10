ZenChamps
========
ZenChamps is a demo script that combines Scrapy and Selenium to scrape the information of all Champions listed on GAW's ZenPortal. This was originally meant as an experiment to improve ZenLogbook, which scrapes "device payout" entries. As a "parser", [ZenLogbook](http://github.com/Scootie/ZenLogbook/) works great, but in many ways, it's stunted in terms of performance, as Selenium is an automation tool. It wasn't intended to scrape or parse.

This is where Scrapy comes into play, a Python lib that's actually meant for scraping. The problem is that a lot of websites load content via javascript, for which Scrapy does not provide support. This means you need to hook Scrapy to something that will execute javascript (like PhantomJS), and then crawl the html source. This is a two edged sword. Using a third party lib, will help you traverse the webpage correctly. However, it also opens up the possiblity that the server identifies your scraper as a bot (which it is), and limits access to the data you seek. This maybe an even greater concern for financial related websites that have additional security layers/sensitivities as a procautionary measure. A good way to circumvent this issue is to combine Scrapy with Selenium, as the later requests and renders the website via commonly used browsers. From the server perspective, it only sees the user agent for "Chrome", "Firefox", or whatever else you choose to load the website with.

By combining Scrapy and Selenium, you get the speed of the first with the thoroughness of the latter. The whole script takes ~10 seconds even with a write function (not included). Doing this in Selenium increases execution time by as much as 100%.

## Notes about the script

As fast as the script is, it's still written with structure in mind. Instead of directly calling individual table cells, we crawl the DOM to find all tables, and parse each one. The benefit of this approach is that it's highly scaleable and the underlying code is more flexible when GAW makes changes to the web interface. For example, adding a champion list to support "Top 10 HashStalker Users" only required adding `0:"stalker"` to an array.

This was adapted from a rather complex scraper that I wrote to track a whole bunch of things in ZenPortal. Currently, I'm working on a couple of other projects, and I haven't had time to update ZenChamps to include a generic write function. Personally, I'd suggest using dataset to throw the parsed data into SQLite DB. This should make it easy to track and look up information.

## Settings

The zenchamps_spider.py file contains the following:
```python
	username.send_keys("myusername")
	password.send_keys("mypassword")
```

You need to change the these values to match your personal login details.

## Requirements
  
* Python bindings for Selenium
* Scrapy lib
* Selenium server
 * JRE 1.6 or newer
  
## Installation instructions

Will be added soon.

## License

Copyright Caleb Ku 2014. Distributed under the MIT License. (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
