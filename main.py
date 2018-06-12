#!/usr/bin/env python
from models.TweetScraper import TweetScraper
import os
import sys
#if you want run the project from here decomment this line
#userToMonitor = "realDonaldTrump"

#if you want to run from command shell and from the dashboard
userToMonitor = sys.argv[1]

deletecommand = 'curl -X DELETE "localhost:9200/tweet_dataset/"'

if not os.system(deletecommand):
    scraper = TweetScraper()
    scraper.tweet_query(userToMonitor, begin_year=2015)

