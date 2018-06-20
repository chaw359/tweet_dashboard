#!/usr/bin/env python
from models.TweetScraper import TweetScraper
import os
import sys
#if you want run the project from here and you won't use elasticsearch-kibana decomment till line 8 and comment from 11 to 16
#userToMonitor = "Ibra_official"
# scraper = TweetScraper()
# scraper.tweet_query(userToMonitor, begin_year=2015)


#if you want to run from command shell and/or from the dashboard and you have elasticsearch activated decomment till line16
userToMonitor = sys.argv[1]
deletecommand = 'curl -X DELETE "localhost:9200/tweet_dataset/"'
if not os.system(deletecommand):
     scraper = TweetScraper()
     scraper.tweet_query(userToMonitor, begin_year=2015)