import json
import urllib.parse,urllib.request
from urllib.error import HTTPError


class SentimentAnalyzer:
    """
    This class has the purpose to analyze a text and extract the sentiment from that text.
    """
    def __init__(self):
        pass


    def extract_sentiment(self, text):
        """
        Given a text the sentiment is returned
        :param text: text to analyze
        :return: sentiment: Pos, Neutral or Neg
        """
        sentiment = self.__get_sentiments(text)
        #Label key return us the sentiment with highest probability
        return sentiment['label']

    def __get_sentiments(self, text):
        """
        Service request for sentiment analysis
        :param text: text to analyze
        :return: dictionary with sentiments as key and value its probability
        """
        try:
            data = urllib.parse.urlencode({"text": text}).encode("utf-8")
            u = urllib.request.urlopen("http://text-processing.com/api/sentiment/", data)
            the_page = u.read()
            toReturn = json.loads(the_page.decode())
            return toReturn
        except HTTPError:
            toReturn = {'label': 'neutral'}
            return toReturn