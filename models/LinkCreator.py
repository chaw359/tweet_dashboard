import datetime
import pprint
import collections
import re
from collections import defaultdict
import time

import json
import pandas as pd

import numpy as np
import tweepy
import SentimentAnalyzer
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv
from SentimentAnalyzer import SentimentAnalyzer
import re

class LinkCreator:

    def __init__(self):
        self.stringa=""
        self.dizionario={}
        self.tagChiave=[]

    def pulisciStringa(self,stringa):
        return stringa.replace(".", "").replace(":", "").replace(";", "").replace(",", "").replace("!", "").replace("#","").replace("@", "").replace(" ","")


    def calcLink(self, stringa):

        self.stringa=stringa
        s = SentimentAnalyzer()

        for tag in stringa.split():
            if tag.startswith('@'):
                self.tagChiave.append(self.pulisciStringa(tag))
               # print("TAG CHIAVE: ",tagChiave )

                #self.dizionario[tagChiave] = s.extract_sentiment(self.stringa)
        return self.tagChiave
       # print(self.dizionario)



if __name__ == '__main__':
    l = LinkCreator().calcLink("@Trump I hate you")
    print(l)
    l1 = LinkCreator().calcLink("@Trump and @Obama love you")
    print(l1)





