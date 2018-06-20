# A web dashboard for tweets analysis

This project has the aim to analyze a stream of a tweet and to analyze some of its attributes that are shown on a web dashboard.
This platform gets data from a Twitter's user (the one that we want to monitor) with a customized twitter scraper in a temporal range, from a beginning year to an end year. On each tweet got a pre-processing process is applied, in particular, the greatest part of pre-processing is made on the tweet's text for evaluating the topic, the sentiment and to find links between the monitored user and other twitter's users mentioned by the monitored one.

# Motivation
This platform has been developed as an academic project for Big Data Analytics' course. The purpose is to provides to users the possibility to analyze a Twitter's users and see nice and funny analytics on him.

# Requirements
The following is the recommended configuration used to run the project without problems:

* Nifi v6.2.4
* Kibana v6.2.4
* Elasticsearch v6.2.4
* Python 3.6 with Pandas and Selenium libraries installed
* XAMPP if you want run the project from the dashboard
* Wikipedia miner services provider url

# How to run the project without the dashboard
## The main file
After the project is downloaded go to the project folder and open **main.py** script.
If you want to run the entire project from the script using command shell you have to comment these lines

```python
#userToMonitor = "Google"
# scraper = TweetScraper()
# scraper.tweet_query(userToMonitor, begin_year=2015)
```
If you open this project in an IDE as PyCharm and you want run from there, de-comment these lines and comment the line where the script takes arguments from the shell:

```python
userToMonitor = "Google"
scraper = TweetScraper()
scraper.tweet_query(userToMonitor, begin_year=2015)

#userToMonitor = sys.argv[1]
```

There are other lines in the main file that requires that elasticsearch is running on your machine:

```python
deletecommand = 'curl -X DELETE "localhost:9200/tweet_dataset/"'
if not os.system(deletecommand):
     scraper = TweetScraper()
     scraper.tweet_query(userToMonitor, begin_year=2015)
```
If you don't need to use elasticsearch or you don't want to delete the index content on each run, you can delete or comment these lines and leave the previous:

```python
#if you want run the project from here and you won't use elasticsearch-kibana decomment till line 8 and comment from 11 to 16
userToMonitor = sys.argv[1] #if you need  to take arguments from shell
#userToMonitor = "Google" #if you don't need to take arguments from shell de-comment this line
scraper = TweetScraper()
scraper.tweet_query(userToMonitor, begin_year=2015)


#if you want to run from command shell and/or from the dashboard and you have elasticsearch activated decomment till line16

#deletecommand = 'curl -X DELETE "localhost:9200/tweet_dataset/"'
#if not os.system(deletecommand):
#     scraper = TweetScraper()
#     scraper.tweet_query(userToMonitor, begin_year=2015)
```
## NiFi configuration
At following link you can download NiFi: [NiFi download](https://nifi.apache.org/download.html)
Choose the right package for your OS. The version used in this project is 1.6.0.
This project has been tested only on Macbook pro 13''. The following are instructions for Mac users:

1. Download the .zip file in *Sources* section in the download page of NiFi.

2. Unzip the nifi project, go to NiFi folder and run nifi with *root* permissions:

     `sudo bin/nifi.sh start`

3. Wait few minutes and then go to nifi's web user interface:
http://localhost:8080/nifi/

4. Import the template that you can find in the project in */nifi_template/* folder, it should be an *.xml* file.

5. After import right-click on **SendPutOnElasticSearch** processor:
     
     *Configure --> Properties*
  
   Check if the properties are set as the following:
   * **Script Engine**: Python
   * **Script Body**: Should contain a python script, if it isn't, go to */nifi_template/scripts/* folder and copy the contents of the curl_generator.py script and paste in this property.

6. Check if the **Controller Services** in *Nifi Flow Configuration* panel are running, if not, run them before to run the processors

After these steps, NiFi is ready to get data coming from the scraper. (Here we suppose that you know something about NiFi, this is not a NiFi tutorial)

## Elasticsearch and Kibana
At following link you can download elasticsearch sources folder: [ES download](https://www.elastic.co/downloads/elasticsearch)
At following link you can download kibana sources folder: [Kibana download](https://www.elastic.co/downloads/kibana)
Choose the right package for your OS. The version used in this project is 6.2.4 for both ES and Kibana
This project has been tested only on Macbook pro 13''. The following are instructions for Mac users:

1. Download the .zip file in the download page.

2. Unzip the elasticsearch project, go to its root folder and run ES:

     `bin/elasticsearch`

3. Unzip the kibana project, open another terminal and go to its root folder:

     `bin/kibana`

3. Wait few minutes and then go to kibana's web user interface:
http://localhost:5601

4. Before starting to draw charts you have to create an **index pattern**:
     
     *Management --> Index Patterns --> Create index patterns*
   Then filter the different indexes in a way that only one match with your filtering query. Then click on *Next step* and confirm the creation

5. Now you can draw charts in the *Visualize* section

6. After charts are created in the *Dashboard* section you can create a new dashboard where you can add your charts.

7. When you have created the dashboard save it and click on *share* button in the top menu and see the different ways to share your dashboard.

After these steps elasticsearch and kibana are ready to get data coming from nifi and visualize them.

## The Data flow
When you complete the configuration of NiFi, Elasticsearch, and Kibana, go to NiFi and run all the processors then go to the *main.py* script and run it. After few seconds you can see the scraper that opens a chrome web page and starts to acquire data from Twitter. From NiFi you can see data flowing along processors. Elasticsearch receives the first PUT and creates an index called *tweet_dataset*, from Kibana you can start to visualize the coming data.


