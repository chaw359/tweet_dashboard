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

4. Import the template that you can find in the project in /nifi_template/ folder, it should be an .xml file.

5. After import right-click on **SendPutOnElasticSearch** processor and 
