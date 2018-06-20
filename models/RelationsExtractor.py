import csv
import json
import random as rand
import re

import pandas as pd
from ast import literal_eval
from collections import OrderedDict

maxIDValue = 999999999999
maxLinks = 5


class RelationsExtractor:
    """
    This class has the purpose to extracts relations from the dataset and for each relation is assigned
    the sentiment.
    """
    def __init__(self, user = "Dummy"):
        self.user = user
        self.linkSentiment = dict()
        self.linkIDs = dict()
        self.linkIDs[user] = rand.randrange(maxIDValue)

    def read_links(self, from_file = "../relation_dataset/tweet_dataset.csv"):
        """
        This method reads from the dataset the column link that represents the link
        between the monitored user and other twitter's users. After this call a json
        file is created.
        :param from_file: path where is positioned the dataset to read
        :return: after the call a json file in the same folder of the dataset is created
        """
        data = pd.read_csv(from_file, sep=";", index_col=0, quotechar='"')
        for index, row in data.iterrows():
            links = literal_eval(row['link'])
            sentiment = row['sentiment']
            if len(links) > 0:
                for link in links:

                    link = " ".join(re.findall("[a-zA-Z]+", link))
                    if link not in self.linkSentiment:
                        self.linkSentiment[link] = dict()
                        self.linkSentiment[link]["total"] = 0
                        self.linkIDs[link] = rand.randrange(maxIDValue)

                    if sentiment not in self.linkSentiment[link]:
                        self.linkSentiment[link][sentiment] = 0

                    self.linkSentiment[link][sentiment] += 1
                    self.linkSentiment[link]["total"] += 1

        #print(self.linkSentiment)
        self.__create_graph_file()

    def __create_graph_file(self):
        """
        This method takes the list created in the read_links method and creates the json
        structure that represents the connected graph.
        :return: a json file is created
        """
        
        idUser = str(self.linkIDs[self.user])
        jsonString='{ "nodes": [{"name":"'+self.user+'","label":"'+self.user+'","id":'+idUser+'},'
        jsonLinks = ''
        linkSentiment = sorted(self.linkSentiment.items(), key=lambda x: x[1]["total"],reverse=True)[:maxLinks]
        for link,sentiments in linkSentiment:
            idLink = str(self.linkIDs[link])
            totalCit = int(sentiments["total"])
            tmpList = {}
            for sent, freq in sentiments.items():
                if sent == "total":
                    tmpList["numTags"] = str(freq)
                else:
                    tmpList[sent] = str(int(freq*100 / totalCit))+"%"
                sentiments['total'] = 1
            jsonString += '{"name":"'+link+'","label":"'+link+'","id":'+idLink+'},'
            jsonLinks += '{"source":'+idUser+',"target":'+idLink+',"type":"'+repr(tmpList).replace("'","")+'"},'
        jsonString = jsonString[:-1]+'],"links":['+jsonLinks[:-1]+'] }'
        #print(jsonString)

        # here is needed the absolute path if we need to run the project via Web
        with open('/Users/gfuccio/GitHub/tweet_dashboard/relation_dataset/relations.json', 'w') as outfile:
            outfile.write(jsonString)