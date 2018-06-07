import datetime
import os
import re
import time
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from models.SentimentAnalyzer import SentimentAnalyzer
from models.TopicExtractor import TopicExtractor

TWITTER_HOME = "https://twitter.com/"
TWITTER_LOGIN ="https://twitter.com/login"
SCROLL_PAUSE_TIME = 30
class TweetScraper:

    def __init__(self, username = "bigdataproject.fenza.2018@gmail.com", password="Bigdataproject2018$"):
        self.driver = webdriver.Chrome("./driver/chromedriver")
        self.topicExtractor = TopicExtractor()
        self.sentimentAnalyzer = SentimentAnalyzer()
        self.tweet_containers = []
        self.tweets_list = []
        self.__login(username, password)


    def tweet_query(self, username="BigDataProject5", begin_year = 2017, end_year = 2018):
        self.username = username
        self.__search_user(username)
        self.__positioning(begin_year)
        print("Total Tweet acquired: ", len(self.tweet_containers))

    def get_tweets(self):
        return self.tweets_list

    def __positioning(self, from_year):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        stop = False
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            tweet_stream = self.driver.find_element_by_css_selector(".stream")

            # mi prendo tutti i tag li con questa classe, Nota: Da qui si potrebbe prendere anche l'id del tweet
            self.tweet_containers = tweet_stream.find_elements_by_css_selector(".js-stream-item.stream-item.stream-item")
            #self.tweet_containers = self.driver.find_elements_by_css_selector(".stream")
            print("Tweet:", len(self.tweet_containers))
            year = ""
            for list_item in self.tweet_containers:
                try:
                    tweet_container = list_item.find_element_by_css_selector(".content")
                    #span_timestamp = tweet_container.find_element_by_css_selector("._timestamp.js-short-timestamp.js-relative-timestamp")
                    span_timestamp = tweet_container.find_element_by_css_selector("._timestamp.js-short-timestamp")
                    #a_timestamp = tweet_container.find_element_by_css_selector("")
                    #span_timestamp = div.find_element_by_css_selector("._timestamp.js-short-timestamp.js-relative-timestamp")
                    if span_timestamp.get_attribute("data-time"):
                        timestamp = span_timestamp.get_attribute("data-time")
                        year = datetime.datetime.fromtimestamp(int(timestamp)).year
                        if year == from_year:
                            stop = True
                            break
                except NoSuchElementException:
                    continue
            print("Year: " + str(year))
            if stop:
                break

            # Wait to load page
            print("Scrivo su file...")

            self.__write_tweet_oncsv(self.tweet_containers)
            self.tweet_containers = []
            print("Attendo nuovi tweet dallo stream")
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        self.driver.close()


    def __search_user(self, username):
        link = TWITTER_HOME + "/" + str(username)
        print("User page link: " + link)
        self.driver.get(link)

    def __login(self, email, password):
        self.driver.get(TWITTER_LOGIN)
        login_form = self.driver.find_element_by_css_selector(".t1-form.clearfix.signin.js-signin")
        inputs = login_form.find_elements_by_tag_name("input")
        submit_button = login_form.find_element_by_tag_name("button")
        email_input = inputs[0]
        pass_input = inputs[1]
        print("Access to account...")

        email_input.send_keys(email)
        pass_input.send_keys(password)
        submit_button.click()
        self.driver.get(self.driver.current_url)

    def __write_tweet_oncsv(self, list_of_tweet, root_directory="dataset/", filename = "tweet_dataset.csv", time_step=5):
        if os.path.exists(root_directory):
            if os.path.exists(root_directory + filename):
                print("Accedo al dataset...")
                data = pd.read_csv(root_directory + filename, sep=",", index_col=0)  # leggo il csv relativo al dataset
            else:
                data = pd.DataFrame(columns=['tweet_id', 'username', 'tweet_text', 'topic', 'sentiment'])
                data.to_csv(root_directory + filename, sep=";")
        else:
            print("Creo la struttura del dataset...")
            os.mkdir(root_directory)
            data = pd.DataFrame(columns=['tweet_id', 'username', 'tweet_text', 'topic', 'sentiment'])
            data.to_csv(root_directory + filename, sep=";")

        row = {}
        print("Total tweet to write: ", len(list_of_tweet))
        for tweet in reversed(list_of_tweet):
            try:
                tweet_id = tweet.find_element_by_css_selector("div.content").\
                    find_element_by_css_selector(".tweet-timestamp.js-permalink.js-nav.js-tooltip").\
                    get_attribute("data-conversation-id")
                print(self.tweets_list)
                #controllo se è stato già inserito
                print("Is tweet id Present?", tweet_id in self.tweets_list)
                if tweet_id not in self.tweets_list:
                    print("Tweet id not present")
                    tweet_text = tweet.find_element_by_css_selector(".TweetTextSize.js-tweet-text.tweet-text").text
                    tweet_text = self.__remove_emoji(tweet_text)
                    tweet_text = tweet_text.replace("\n", " ")
                    #Conviene qui fare il calcolo del topic e del sentiment
                    # calcolo topic

                    # calcolo sentiment
                    # calcolo collegamenti
                    row['tweet_id'] = tweet_id
                    row['username'] = self.username
                    row['tweet_text'] = tweet_text
                    row['topic'] = self.topicExtractor.analyze_text(tweet_text)
                    row['sentiment'] = self.sentimentAnalyzer.extract_sentiment(tweet_text)
                    print("Tweet id: ", tweet_id, "\nTweet text: ", tweet_text)

                    print("Waiting for new tweet...")
                    #time.sleep(time_step)
                    self.tweets_list.append(tweet_id)
                    data = data.append(row, ignore_index=True)
                else:
                    print("Nessun nuovo tweet dallo stream!")
            except NoSuchElementException:
                continue

        data.to_csv("dataset/tweet_dataset.csv", sep=";")

        print(data.shape)
        print("Dataset is saved to " + root_directory + filename)

    def __remove_emoji(self, string):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)


