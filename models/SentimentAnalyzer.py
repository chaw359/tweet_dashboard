import json
import urllib.parse,urllib.request

class SentimentAnalyzer:

    def __init__(self):
        pass


    def extract_sentiment(self, text):
        sentiment = self.__get_sentiments(text)
        #Label key return us the sentiment with highest probability
        return sentiment['label']

    def __get_sentiments(self, text):
        data = urllib.parse.urlencode({"text": text}).encode("utf-8")
        u = urllib.request.urlopen("http://text-processing.com/api/sentiment/", data)
        the_page = u.read()
        toReturn = json.loads(the_page.decode())
        return toReturn


    # def getNegative(self, stringa):
    #     print("STRINGA OTTENUTA: ", stringa)
    #     dizionario = self.analyze_text(stringa)
    #     return dizionario["probability"]["neg"]
    #
    # def getNeutral(self, stringa):
    #     print("STRINGA OTTENUTA: ", stringa)
    #     dizionario = self.analyze_text(stringa)
    #     return dizionario["probability"]["neutral"]
    #
    # def getPositive(self, stringa):
    #     print("STRINGA OTTENUTA: ", stringa)
    #     dizionario = self.analyze_text(stringa)
    #     return dizionario["probability"]["pos"]



# if __name__ == '__main__':
#     s = SentimentAnalyzer()
#     print(s.get_label("You're a poor jerk!"))
#     print(s.get_label("I love you!"))
