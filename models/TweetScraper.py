import datetime
import os
import re
import time
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from models.LinkCreator import LinkCreator
from models.LinkExtractor import LinkExtractor
from models.SentimentAnalyzer import SentimentAnalyzer
from models.TopicExtractor import TopicExtractor

TWITTER_HOME = "https://twitter.com"
TWITTER_LOGIN ="https://twitter.com/login"
SCROLL_PAUSE_TIME = 10
class TweetScraper:
    """
    This class represent our Twitter scraper built for our precise purpose. In particular, this scraper uses selenium
    as library with chrome driver to do scraping. The data gathered are tweet id, screen name of the monitored user,
    tweet text and timestamp.
    """
    def __init__(self, username = "your_twitter@login_email", password="yourpassword"):
        """
        To visualize a twitter user's home we need to login in Twitter, so is necessary to provide at this class its own
        access data.
        :param username: username of your twitter account
        :param password: password of your twitter account
        """
        #location of the chrome driver, the absolute path is needed if you want run the project from the web
        self.driver = webdriver.Chrome("/Users/gfuccio/GitHub/tweet_dashboard/driver/chromedriver")

        self.sentimentAnalyzer = SentimentAnalyzer()
        self.linkCreator = LinkCreator()

        self.tweet_containers = []
        self.tweets_list = []
        self.__login(username, password)


    def tweet_query(self, username="Google", begin_year = 2017, end_year = 2018):
        """
        This method performs a query on twitter, in particular the query need only the username of the user that
        we want to monitor. This method takes also as argument a year's range, begin year, where to start, and end year,
        where to stop scraping.
        :param username: the tweet username to monitor
        :param begin_year: the year to stop the scrolling down twitter user's home
        :param end_year: the year to stop scrollig up, it would be greater than begin year
        :return: None
        """
        self.username = username
        self.relationExtractor = LinkExtractor(username)
        self.__search_user(username)
        self.__positioning(begin_year)
        print("Total Tweet acquired: ", len(self.tweets_list))

    def get_tweets(self):
        """
        Get the total list gathered
        :return: list of tweets' ids
        """
        return self.tweets_list

    def __positioning(self, from_year):
        """
        This method scroll down the page untill the there is the load, reached that point the showed tweets are gathered,
        then they will be saved on csv and the scroll continues 'till the specified year isn't reached.
        :param from_year: the year to stop the scrolling
        :return: None
        """
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
            print("Write on file...")

            self.__write_tweet_oncsv(self.tweet_containers)
            self.tweet_containers = []
            print("Waiting for new tweets from stream")
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                continue
            last_height = new_height

        self.driver.close()


    def __search_user(self, username):
        """
        Navigate to twitter's user home
        :param username: the user to find
        :return: None
        """
        link = TWITTER_HOME + "/" + str(username)
        print("User page link: " + link)
        self.driver.get(link)

    def __login(self, email, password):
        """
        This method performs the login on twitter. Due to twitter blocks unlogged users to make research, so we need an
        account to login in twitter and make research
        :param email: account email
        :param password: account password
        :return: None
        """
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

    def __write_tweet_oncsv(self, list_of_tweet, root_directory="/Users/gfuccio/GitHub/tweet_dashboard/dataset/", filename = "tweet_dataset.csv", time_step=20):
        """
        This method performs the tweets data writing on a csv. The absloute path is needed if you want run the project
        via Web
        :param list_of_tweet: list of tweet to store
        :param root_directory: absolute path of the folder where to store the dataser
        :param filename: name of the dataset
        :param time_step: each seconds writing is performed
        :return: None
        """
        #if the root directory exists
        if os.path.exists(root_directory):
            #check also if the dataset already exists. If yes we access to dataset
            if os.path.exists(root_directory + filename):
                print("Access to dataset...")
                data = pd.read_csv(root_directory + filename, sep=";", index_col=0)  # leggo il csv relativo al dataset
            else:#otherwise we create the structure
                print("Creating the dataset structure...")
                data = pd.DataFrame(columns=['tweet_id', 'username', 'tweet_text', 'topic', 'sentiment', 'link', 'timestamp'])
        else:#if the root directory doesn't exits, we create it and create also the dataset's structure
            print("Creating the dataset structure...")
            os.mkdir(root_directory)
            data = pd.DataFrame(columns=['tweet_id', 'username', 'tweet_text', 'topic', 'sentiment', 'link', 'timestamp'])

        row = {}
        print("Total tweet to write: ", len(list_of_tweet))
        for tweet in reversed(list_of_tweet):
            try:
                tweet_id = tweet.find_element_by_css_selector("div.content").\
                    find_element_by_css_selector(".tweet-timestamp.js-permalink.js-nav.js-tooltip").\
                    get_attribute("data-conversation-id")
                ts = tweet.find_element_by_css_selector("div.content").\
                    find_element_by_css_selector(".tweet-timestamp.js-permalink.js-nav.js-tooltip"). \
                    find_element_by_tag_name("span").get_attribute("data-time-ms")

                date = datetime.datetime.fromtimestamp(int(ts)/1000.0).strftime("%Y-%m-%d")
                print("Timestamp:", date)


                print("Total tweet reached: ", len(self.tweets_list))
                #check if the tweet is already present in the list
                #print("Is tweet id Present?", tweet_id in self.tweets_list)
                if tweet_id not in self.tweets_list:
                    topicExtractor = TopicExtractor()
                    print("Tweet id not present")
                    tweet_text = tweet.find_element_by_css_selector(".TweetTextSize.js-tweet-text.tweet-text").text
                    tweet_text = self.__remove_emoji(tweet_text)
                    tweet_text = tweet_text.replace("\n", " ")

                    row['tweet_id'] = tweet_id
                    row['username'] = self.username
                    row['tweet_text'] = tweet_text
                    row['topic'] = topicExtractor.analyze_text(tweet_text)
                    row['sentiment'] = self.sentimentAnalyzer.extract_sentiment(tweet_text)
                    row['link']= self.linkCreator.find_link(tweet_text)
                    row['timestamp'] = date
                    print("Tweet id: ", tweet_id, "\nTweet text: ", tweet_text)

                    self.tweets_list.append(tweet_id)
                    data = data.append(row, ignore_index=True)


                else:
                    print("No new tweets from stream")
                    break
            except NoSuchElementException:
                print("HTML error")
                continue

        data.to_csv(root_directory + filename, sep=";")

        time.sleep(time_step)
        # here the script waits the creation of the dataset and its positioning in the relation_dataset folder
        # the dataset positioning is made by NiFi. If you won't use NiFi replace the directory with the dataset
        # directory where this class store the dataset, the default path is ./dataset/. If you do that you can
        # avoid the waiting time.
        self.relationExtractor.read_links("/Users/gfuccio/GitHub/tweet_dashboard/relation_dataset/tweet_dataset.csv")

        print(data.shape)
        print("Dataset is saved to " + root_directory + filename)

    def __remove_emoji(self, string):
        """
        Remove chars junk from given text
        :param string: text to clean
        :return: cleaned string
        """
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)
