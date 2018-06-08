import re
import sys

from models.TweetScraper import TweetScraper
import pandas as pd
from subprocess import call
import os

userToMonitor = sys.argv[1]
scraper = TweetScraper()
scraper.tweet_query(userToMonitor, begin_year=2017)



#data = pd.read_csv("dataset/tweet_dataset.csv", sep=",")

# print(data)
#
# curl_list = []
# for index, row in data.iterrows():
#     document = '\'{"tweet_id":"' + str(row['tweet_text']) + '", "Topic":"' + str(row['username']) + '"}\''
#     command_string = ["curl", "-X", "PUT",'\"localhost:9200/tweet_dataset/tweet/' + str(row['tweet_id']) +'\"', "-H", "'Content-Type: application/json'",
#                   "-d", document]
#
#     curlstring = 'curl -X PUT "localhost:9200/tweet_dataset/tweet/' + str(row['tweet_id']) + '" -H ' + "'Content-Type: application/json' -d "
#
#     print(curlstring + document)
#     curl_list.append(curlstring + document)

#     for arg in command_string:
#         print(arg, end=" ")
#
#     curl_list.append(command_string)
#     print("\n")
#
# call(curl_list[2])

#os.system(curl_list[2])

# print("First curl request:")
# print(curl_list[0])
# call(curl_list[0])





