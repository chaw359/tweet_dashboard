import re
from ast import literal_eval
import random as rand
import pandas as pd

MAX_ID_VALUE = 999999999999 #highest id value
MAX_LINK_TO_SHOW = 10 #limit for best links to show

class LinkExtractor:
    """
    This class extract links from a dataset and use this link to format a json string that is sent to server to create
    a linked graph. In particular, this class find the best links of the monitored user, the best links are tagged user
    with a number of tags that overcome the average of total general tags, then this links are stored in a list that is
    continuosly updated. The list updating is based on number of tags. At the end this class creates a json string stored
    on a file that is sent to server. The server uses this json to create the linked graph.
    """
    def __init__(self, username = "Dummy"):
        self.username = username
        self.links = {}
        self.link_sentiment = {}
        self.best_links = []
        self.avg_num_tag = 0
        self.user_id = rand.randrange(MAX_ID_VALUE)

    def read_links(self, from_file = "../relation_dataset/tweet_dataset.csv"):
        """
        Read the link from the dataset passed as parameter and creates json file to send to server
        :param from_file: csv file with column link
        :return: None
        """
        data = pd.read_csv(from_file, sep=";", index_col=0, quotechar='"')
        for index, row in data.iterrows():
            dataset_links = literal_eval(row['link']) #the link column contains lists
            sentiment = row['sentiment']
            if len(dataset_links) > 0:
                for link in dataset_links:

                    #cleaning the tagged user name
                    link = " ".join(re.findall("[a-zA-Z]+", link))
                    #if the username isn't in the links list, insert and initialize him
                    if link not in self.links.keys():
                        self.links[link] = {}
                        self.links[link]["num_tag"] = 1
                        self.links[link]["id"] = rand.randrange(MAX_ID_VALUE)
                        self.links[link][sentiment] = 1

                    else:#else number of tags is incremented
                        self.links[link]["num_tag"] += 1
                        #if the sentiment extratect from dataset isn't in the user dictionary, insert and initialize it
                        if sentiment not in self.links[link].keys():
                            self.links[link][sentiment] = 1
                        else:#else increment the counter for that sentiment
                            self.links[link][sentiment] +=1

                    #print(self.links)



        #print(self.links)
        #call those functions only if the list of links has length > 0
        if len(self.links.keys()) > 0:

            print("No Links found!")
            self.__find_best_links() #creates the best links list
            self.__create_link_json() #creates the json string that is stored on file

    def __find_best_links(self, n = MAX_LINK_TO_SHOW):
        """
        This method, given a list of links, extract from that list the n best ones. The best links are tweet users tagged
        by the monitored user that have a number of tags greater than the average of the total tags done by the monitored
        user.
        :param n: the maximum link to store in best links list
        :return: None
        """

        #evaluation of the average of the total tags done by monitored user
        summation = 0
        for link in self.links.keys():
            summation += self.links[link]['num_tag']

        self.avg_num_tag = summation/len(self.links.keys())

        """
        For each link(tagged user) in the links list, is checked if the number of tags received by the link is greater
        than the average. If yes, there are other cheking phase. First if the link is not present in the best links list
        and the lenght of this list is lower than n, append it to list. Otherwise, if the link is present in the best links
        list increment the number of tags of this tagged user. If the link is not present and the best links list is full
        check if the current link has a number of tags greater than someone in the best links list, if yes replace
        the old link with the new one, because the new one has more tags than the old one.
        """
        for link in self.links.keys():

            if self.links[link]['num_tag'] >= self.avg_num_tag:
                if {link:self.links[link]} not in self.best_links and len(self.best_links) < n:
                    self.best_links.append({link:self.links[link]})
                elif {link:self.links[link]} in self.best_links:
                    self.best_links.remove({link:self.links[link]})
                    self.links[link]['num_tag'] += 1
                    self.best_links.append({link:self.links[link]})
                else:
                    print("The list is full, checking if the #tags of", link, "is greater than an element of a best links")
                    toRemove =[]
                    toAdd = []
                    for best_link in self.best_links:
                        if self.links[link]['num_tag'] > best_link[list(best_link[best_link.keys()])[0]]['num_tag']:
                            toRemove = best_link
                            toAdd = {link:self.links[link]}
                            break
                    if toRemove != [] and toAdd != []:
                        self.best_links.remove(toRemove)
                        self.best_links.append(toAdd)

            if len(self.best_links) == n:
                break

        """
        If in the previous for the best links list is not fulled, we full the list here, including also links that
        not overcome the average
        """
        if len(self.best_links) < n:
            for link in self.links.keys():

                if {link: self.links[link]} not in self.best_links:
                    self.best_links.append({link: self.links[link]})

                if len(self.best_links) == n:
                    break

        print(self.best_links)

    def __create_link_json(self):
        """
        Given the best links list, this method formats a json string that is stored on a file.
        :return: None
        """
        id_main_user = str(self.user_id)
        jsonString = '{ "nodes": [{"name":"' + self.username + '","label":"' + self.username + '","id":' + id_main_user + '},'
        jsonLinks = ''
        # print(self.linkSentiment.items())

        for element in self.best_links:
            name = list(element.keys())[0]
            id_link = str(element[name]['id'])
            id_user = str(self.user_id)
            tmp_dict = {}
            for key in element[name].keys():

                if key != "num_tag" and key != "id":
                    tmp_dict[key] = str(round((element[name][key] / element[name]['num_tag']) * 100.00, 2)) + "%"
                    tmp_dict['num_tag'] = element[name]['num_tag']
            sentiment_string = ""
            for key in tmp_dict.keys():

                if key != "num_tag":
                    sentiment_string += key + ":" + tmp_dict[key] + ", "

            type = "#Tags: " + str(tmp_dict['num_tag']) + ", " + sentiment_string
            jsonString += '{"name":"' + name + '","label":"' + name + '","id":' + id_link + '},'
            jsonLinks += '{"source":' + id_user + ',"target":' + id_link + ',"type":"' + type+ '"},'

        jsonString = jsonString[:-1] + '],"links":[' + jsonLinks[:-1] + '] }'

        # here is needed the absolute path if we need to run the project via Web
        with open('/Users/gfuccio/GitHub/tweet_dashboard/relation_dataset/relations.json', 'w') as outfile:
            outfile.write(jsonString)