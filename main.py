import re

from models.TweetScraper import TweetScraper
import pandas as pd
from subprocess import call
import os

# scraper = TweetScraper()
# scraper.tweet_query("BigDataProject5", begin_year=2017)

#scraper.write_tweet_oncsv()
from models.TopicExtractor import TopicExtractor


def __remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

topic = TopicExtractor()

#textToAnalyze = "Enzymes accelerate chemical reactions. The molecules upon which enzymes may act are called substrates and the enzyme converts the substrates into different molecules known as products. "
#textToAnalyze = "With more space, smarter options, access to experts and more, Google One is a simple plan for expanded storage with extra benefits to help you get more out of Google → http://goo.gl/Kgr2uu "
#textToAnalyze = "Explore the unique stories of Iraq’s endangered heritage sites and the extraordinary efforts to preserve them on @googlearts, in partnership with @WorldMonuments → http://goo.gl/hntYAV "
textToAnalyze = "With this year's theme of 'What Inspires Me...' we're thrilled to announce the five national #Doodle4Google finalists and their artwork → http://goo.gl/aUu5AZ "
#textToAnalyze = "Today’s speedy #GoogleDoodle marks the 131st birthday of Tom Longboat, Canadian long-distance runner and one of the greatest marathoners of all time → http://goo.gl/rSB4zE "
topic.analyze_text(__remove_emoji(textToAnalyze))



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





