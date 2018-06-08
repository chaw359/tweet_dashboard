import csv
import json
import random as rand

maxIDValue = 999999999999
class RelationsExtractor:

    def __init__(self, user = "Giovanni"):
        self.user = user
        self.linkSentiment = dict()
        self.linkIDs = dict()
        self.linkIDs[user] = rand.randrange(maxIDValue)

    def getRelations(self, fileToRead = "resources/tweets.csv"):
        with open(fileToRead, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            ls = dict()
            for row in reader:
                sentiment = row[4]
                links = row[5].split()
                for link in links:
                    if link not in self.linkSentiment:
                        self.linkSentiment[link] = dict()
                        self.linkSentiment[link]["total"] = 0
                        self.linkIDs[link] = rand.randrange(maxIDValue)
                        
                    if sentiment not in self.linkSentiment[link]:
                        self.linkSentiment[link][sentiment] = 0
                        
                    self.linkSentiment[link][sentiment] += 1
                    self.linkSentiment[link]["total"] += 1
                        
        self.sendRelationsJSON()

    def sendRelationsJSON(self):
        
        idUser = str(self.linkIDs[self.user])
        jsonString='{ "nodes": [{"name":"'+self.user+'","label":"'+self.user+'","id":'+idUser+'},'
        jsonLinks = ''
        for link,sentiments in self.linkSentiment.items():
            idLink = str(self.linkIDs[link])
            totalCit = int(sentiments["total"])
            for sent, freq in sentiments.items():
                sentiments[sent] = str(freq*100 / totalCit)+"%"
            del sentiments["total"]
            jsonString += '{"name":"'+link+'","label":"'+link+'","id":'+idLink+'},'
            jsonLinks += '{"source":'+idUser+',"target":'+idLink+',"type":"'+repr(sentiments).replace("'","")+'"},'
        jsonString = jsonString[:-1]+'],"links":['+jsonLinks[:-1]+'] }'
        
        with open('resources/relations.json', 'w') as outfile:
            outfile.write(jsonString)
