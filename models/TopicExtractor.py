import requests
from simplejson import JSONDecodeError
import xml.etree.ElementTree as ET


class TopicExtractor:

    def __init__(self):
        #categorie da ricercare all'interno della gerarchia di wikipedia
        self.categoryToFind = ["Technology", "Music", "Sport", "Finance", "Economy", "Politics",
                          "Entertainment", "Games", "Nutrition", "Medicine", "History", "Mathematics",
                          "Biology", "Nature", "Religion", "Society", "Business", "Computing",
                          "Electronics", "Engineering", "Transport"]
        self.found = False
        #Indica le categorie trovate, si tratta di un dizionario che mantiene la frequenze delle categorie trovate
        self.categoryFound = {"Technology": 0, "Music": 0, "Sport": 0, "Finance":0, "Economy":0, "Politics":0,
                 "Entertainment":0, "Games":0, "Nutrition":0, "Medicine":0, "History":0, "Mathematics":0,
                 "Biology":0, "Nature":0, "Religion":0, "Society":0, "Business":0, "Computing":0,
                 "Electronics":0, "Engineering":0, "Transport":0, "Various":0}


    def check_parent_category(self, category_id, num_call):
        url = "http://193.205.163.45:8080/wikipedia-miner/services/exploreCategory?id=" + str(category_id) + "&responseFormat=json&parentCategories=true"
        categoryResponse = requests.post(url)
        categories = categoryResponse.json()
        print(categories)
        if num_call == 0:
            #categoryFound['Various'] = 1
            return "Various"

        if categories['title'] in self.categoryToFind:
            print(categories['title'] + " found!")
            #categoryFound[categories['title']] = 1
            return categories['title']
        else:
            if categories['totalParentCategories'] == 0:
                print("Total parent categories = 0")
                return
                #
                # return check_parent_category(categories['id'], num_call - 1)
            else:
                return self.check_parent_category(categories['parentCategories'][0]['id'], num_call - 1)

    def analyze_text(self, text):
        urlSearch = "http://193.205.163.45:8080/wikipedia-miner/services/wikify?source=" + text + "&responseFormat=json"
        response = requests.post(urlSearch)
        try:
            topics = response.json()['detectedTopics']
            print(topics)
            self.__wikify_request_for_categories(topics)

            print("Main topic:")
            for key in self.categoryFound:
                if self.categoryFound[key] > 0:
                    print(key, ": ", self.categoryFound[key])
        except JSONDecodeError:# Per alcuni testi non viene fornita la risposta JSON quindi si fa il parsing dell' XML
            print("No Json... XML Parsing...")
            #attenzione ai detected topics che potrebbero non esserci
            root = ET.fromstring(response.text)
            topics =[]
            for child in root:
                if child.tag == "detectedTopics":
                    for topicChild in child:
                        topics.append({"id": topicChild.attrib['id'], "title": topicChild.attrib['title'], "weight":topicChild.attrib["weight"]})
                        #print(topicChild.tag, topicChild.attrib['id'])
            print(topics)
            self.__wikify_request_for_categories(topics)

            print("Main topic:")
            for key in self.categoryFound:
                if self.categoryFound[key] > 0:
                    print(key, ": ", self.categoryFound[key])

    def __wikify_request_for_categories(self, topics):

        topicFound = False
        for topic in topics:
            print(topic)
            print("ID: " + str(topic['id']) + " Topic Name: " + topic['title'])
            urlArticle = "http://193.205.163.45:8080/wikipedia-miner/services/exploreArticle?id=" + str(
                topic['id']) + "&responseFormat=json&parentCategories=true"
            print(urlArticle)
            response = requests.post(urlArticle)
            categories = response.json()
            print(response.json())
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