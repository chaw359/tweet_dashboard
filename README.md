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
* XAMPP if you want run the project in local
* Wikipedia miner services provider url
