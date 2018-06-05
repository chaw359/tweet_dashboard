import requests


found = False
def check_parent_category(category_id, num_call):
    url = "http://193.205.163.45:8080/wikipedia-miner/services/exploreCategory?id=" + str(category_id) + "&responseFormat=json&parentCategories=true"
    categoryResponse = requests.post(url)
    categories = categoryResponse.json()
    print(categories)
    if num_call == 0:
        return 0

    if categories['title'] == "Technology":
        print("found!")
        return "Technology"
    else:
        return check_parent_category(categories['parentCategories'][0]['id'], num_call - 1)


#textToAnalyze = "Enzymes accelerate chemical reactions. The molecules upon which enzymes may act are called substrates and the enzyme converts the substrates into different molecules known as products. "
textToAnalyze = "With more space, smarter options, access to experts and more, Google One is a simple plan for expanded storage with extra benefits to help you get more out of Google → http://goo.gl/Kgr2uu "

urlSearch = "http://193.205.163.45:8080/wikipedia-miner/services/wikify?source=" + textToAnalyze + "&responseFormat=json"

categoryToFind = ["Technology"]
categoryFound = {"Technology": 0}
response = requests.post(urlSearch)

topics = response.json()['detectedTopics']

topicFound = False
for topic in topics:
    print(topic)
    print("ID: " + str(topic['id']) + " Topic Name: " + topic['title'])
    urlArticle = "http://193.205.163.45:8080/wikipedia-miner/services/exploreArticle?id="+str(topic['id'])+"&responseFormat=json&parentCategories=true"
    response = requests.post(urlArticle)
    categories = response.json()
    print(response.json())
    if(categories['title'] == "Technology"):
        categoryFound["Technology"] += 1
        break
    else:
        for category in categories['parentCategories']:
            found = check_parent_category(category['id'],20)
            if(found == "Technology"):
                print("Technology has been found")
                categoryFound["Technology"] += 1
                topicFound = True
                break
        if topicFound:
            break

print(categoryFound)



# url = "http://193.205.163.45:8080/wikipedia-miner/services/exploreCategory?id=17200193&responseFormat=json&parentCategories=true"
#
#
#
# categories = response.json()
#
# print(categories['parentCategories'])