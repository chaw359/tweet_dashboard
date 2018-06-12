import requests
from simplejson import JSONDecodeError
import xml.etree.ElementTree as ET


class TopicExtractor:
    """
    This class evaluates the topic of a given a text. In particular, for each tweet from the stream
    this class evaluates the topic making requests to wikify to get the topic of tweet's text.
    """
    def __init__(self):
        #These are macro categories of Wikipedia that will be matched we the tweet topic
        self.categoryToFind = ["Technology", "Music", "Sport", "Finance", "Economy", "Politics",
                          "Entertainment", "Games", "Nutrition", "Medicine", "History", "Mathematics",
                          "Biology", "Nature", "Religion", "Society", "Business", "Computing",
                          "Electronics", "Engineering", "Transport"]
        #To check if the topic is found
        self.found = False

        """This represent the categories found. In particular, it is a dictionary that holds the frequency of the 
        category found"""
        self.categoryFound = {"Technology": 0, "Music": 0, "Sport": 0, "Finance":0, "Economy":0, "Politics":0,
                 "Entertainment":0, "Games":0, "Nutrition":0, "Medicine":0, "History":0, "Mathematics":0,
                 "Biology":0, "Nature":0, "Religion":0, "Society":0, "Business":0, "Computing":0,
                 "Electronics":0, "Engineering":0, "Transport":0, "Various":0}

        #Represent the best categories that overcome the average of topics frequency
        self.best_categories = []

        #Represent the principal text's topics. Category that have frequency >0
        self.main_topics = {}


    def check_parent_category(self, category_id, num_call = 20):
        """
        This is a recursive function that navigates the category tree of wikipedia. To avoid infinite recursion process
        we set a fixed number of call, if within these calls the category isn't found, we set the topic of the text as
        Various. So, with the category id, wikify services returns the ids of parent categories that will be used to go
        up the tree, but only the first branch of the tree.
        :param category_id: the category id that represent the leaf to start the tree's climbing
        :param num_call: maximumn number of call to avoid infinite recursion process
        :return: the label of the category found
        """
        url = "http://193.205.163.45:8080/wikipedia-miner/services/exploreCategory?id=" + str(category_id) + "&responseFormat=json&parentCategories=true"
        categoryResponse = requests.post(url)
        categories = categoryResponse.json()
        #print(categories)
        if num_call == 0:
            #categoryFound['Various'] = 1
            return "Various"

        if categories['title'] in self.categoryToFind:
            #print(categories['title'] + " found!")
            #categoryFound[categories['title']] = 1
            return categories['title']
        else:
            if categories['totalParentCategories'] == 0:
                #print("Total parent categories = 0")
                return
                #
                # return check_parent_category(categories['id'], num_call - 1)
            else:
                return self.check_parent_category(categories['parentCategories'][0]['id'], num_call - 1)


    def analyze_text(self, text):
        """
        This method analyzes the given text and returns the best category found for the text.
        :param text: text to analyze
        :return: the best category found, that match with the category to find
        """
        self.main_topics = {}
        self.best_categories = []
        #with this call we found the first level of categories detected for the given text
        urlSearch = "http://193.205.163.45:8080/wikipedia-miner/services/wikify?source=" + text + "&responseFormat=json"
        response = requests.post(urlSearch)
        try:
            topics = response.json()['detectedTopics']
            #print(topics)
            #this method's call start the recursion if the first level of topics isn't in the categoryToFind list
            self.__wikify_request_for_categories(topics)

            print("Main topic:")
            #each category that overcome the zero is a main topic of the given text
            for key in self.categoryFound:
                if self.categoryFound[key] > 0:
                    print(key, ": ", self.categoryFound[key])
                    self.main_topics[key] = self.categoryFound[key]
        except JSONDecodeError:# For some texts isn't returned the json, so we make the parsing of the returned XML
            print("No Json... XML Parsing...")

            root = ET.fromstring(response.text)
            topics =[]
            for child in root:
                if child.tag == "detectedTopics":#detectedTopics is the attribute of our interest
                    for topicChild in child:
                        topics.append({"id": topicChild.attrib['id'], "title": topicChild.attrib['title'], "weight":topicChild.attrib["weight"]})
                        #print(topicChild.tag, topicChild.attrib['id'])
            #print(topics)

            self.__wikify_request_for_categories(topics)

            print("Main topic:")
            for key in self.categoryFound:
                if self.categoryFound[key] > 0:
                    print(key, ": ", self.categoryFound[key])
                    self.main_topics[key] = self.categoryFound[key]
        except KeyError:
            pass


        self.__evaluate_best_topics()
        if len(self.best_categories) == 0:
            return "Various"
        else:
            return self.best_categories[0]



    def __evaluate_best_topics(self):
        """
        This method is used to find the best categories. The best categories are the categories that in frequency
        overcome the average
        :return: None
        """
        summation = 0
        if len(self.main_topics.keys()) > 0:
            if len(self.main_topics.keys()) == 1:
                self.best_categories.append(list(self.main_topics.keys())[0])

            for key in self.main_topics:
                summation += self.main_topics[key]

            avg = summation/len(self.main_topics.keys())
            print("Average:", avg)
            for key in self.main_topics:
                if self.main_topics[key] >= avg:
                    self.best_categories.append(key)

            print("The best categories are:")
            print(self.best_categories)

    def __wikify_request_for_categories(self, topics):
        """
        For each topic in the list of topics passed a call to wikify service is done to get the first level of parent
        categories of the current topic. If one of these parent categories matches with categoryToFind list, its counter
        is updated, otherwise for each category in the parent categories a call to recursive function is done.
        :param topics: list of topic as dictionary
        :return: None
        """
        topicFound = False
        for topic in topics:
            #print(topic)
            print("ID: " + str(topic['id']) + " Topic Name: " + topic['title'])
            urlArticle = "http://193.205.163.45:8080/wikipedia-miner/services/exploreArticle?id=" + str(
                topic['id']) + "&responseFormat=json&parentCategories=true"
            print("Request:", urlArticle)
            response = requests.post(urlArticle)
            categories = response.json()
            #print(response.json())
            try:
                if (categories['title'] in self.categoryToFind):
                    self.categoryFound[categories['title']] += 1
                    break
                else:
                    for category in categories['parentCategories']:
                        found = self.check_parent_category(category['id'], 20)
                        if found in self.categoryToFind:
                            self.categoryFound[found] += 1
                            topicFound = True
                    if topicFound:
                        break
            except KeyError:
                continue