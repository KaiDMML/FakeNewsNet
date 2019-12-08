

## FakeNewsNet

***We released a tool [FakeNewsTracker], for collecting, analyzing, and visualizing of fake news and the related dissemination on social media. Check it out!***

***The latest dataset paper with detailed analysis on the dataset  can be found at [FakeNewsNet]***

**Please use the current up-to-date version of dataset**

Previous version of the dataset is available in branch named `old-version` of this repository.


## Overview  

Complete dataset cannot be distributed because of Twitter privacy policies and news publisher copy rights.  Social engagements and user information are not disclosed because of Twitter Policy. This code repository can be used to download news articles from published websites and relevant social media data from Twitter. 

The minimalistic version of latest dataset provided in this repo (located in `dataset` folder) include following files:

 - `politifact_fake.csv` -  Samples related to fake news collected from PolitiFact 
 - `politifact_real.csv` -  Samples related to real news collected  from PolitiFact 
 - `gossipcop_fake.csv` - Samples related to fake news collected from GossipCop
  - `gossipcop_real.csv` - Samples related to real news collected from GossipCop

Each of the above CSV files is comma separated file and have the following columns

 - `id` - Unique identifider for each news
 - `url` - Url of the article from web that published that news 
 - `title` - Title of the news article
 - `tweet_ids` - Tweet ids of tweets sharing the news. This field is list of tweet ids separated by tab.

## Installation    

###  Requirements:
 Data download scripts are writtern in python and requires `python 3.6 +` to run.
 
Twitter API keys are used for collecting data from Twitter.  Make use of the following link to get Twitter API keys    
https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html   

Script make use of keys from  _tweet_keys_file.json_ file located in `code/resources` folder. So the API keys needs to be updated in `tweet_keys_file.json` file.  Provide the keys as array of JSON object with attributes `app_key,app_secret,oauth_token,oauth_token_secret` as mentioned in sample file.

Install all the libraries in `requirements.txt` using the following command
    
    pip install -r requirements.txt


###  Configuration:

 FakeNewsNet contains 2 datasets collected using ground truths from _Politifact_ and _Gossipcop_.  
    
The `config.json` can be used to configure and collect only certain parts of the dataset. Following attributes can be configured    
  
 - **num_process** - (default: 4) This attribute indicates the number of parallel processes used to collect data.    
 - **tweet_keys_file** - Provide the number of keys available configured in tweet_keys_file.txt file       
 - **data_collection_choice** - It is an array of choices of various parts of the dataset. Configure accordingly to download only certain parts of the dataset.       
   Available values are  
     {"news_source": "politifact", "label": "fake"},{"news_source": "politifact", "label":    "real"}, {"news_source": "gossipcop", "label": "fake"},{"news_source": "gossipcop", "label": "real"}  
  
 - **data_features_to_collect** - FakeNewsNet has multiple dimensions of data (News + Social). This configuration allows one to download desired dimension of the dataset. This is an array field and can take following values.  
	              
	 - **news_articles** : This option downloads the news articles for the dataset.  
     - **tweets** : This option downloads tweets objects posted sharing the news in Twitter. This makes use of Twitter API to download tweets.  
     - **retweets**: This option allows to download the retweets of the tweets provided in the dataset.  
     - **user_profile**: This option allows to download the user profile information of the users involved in tweets. To download user profiles, tweet objects need to be downloaded first in order to identify users involved in tweets.  
     - **user_timeline_tweets**: This option allows to download upto 200 recent tweets from the user timeline. To download user's recent tweets, tweet objects needs to be downloaded first in order to identify users involved in tweets.
     - **user_followers**: This option allows to download the user followers ids of the users involved in tweets. To download user followers ids, tweet objects need to be downloaded first in order to identify users involved in tweets.  
     - **user_following**: This option allows to download the user following ids of the users involved in tweets. To download user's following ids, tweet objects needs to be downloaded first in order to identify users involved in tweets.


## Running Code

Inorder to collect data set fast, code makes user of process parallelism and to synchronize twitter key limitations across mutiple python processes, a lightweight flask application is used as keys management server.
Execute the following commands inside `code` folder,

    nohup python -m resource_server.app &> keys_server.out&

The above command will start the flask server in port 5000 by default.

**Configurations should be done before proceeding to the next step !!**

Execute the following command to start data collection,

    nohup python main.py &> data_collection.out&

Logs are wittern in the same folder in a file named as `data_collection_<timestamp>.log` and can be used for debugging purposes.

The dataset will be downloaded in the directory provided in the `config.json` and progress can be monitored in `data_collection.out` file. 

### Dataset Structure
The downloaded dataset will have the following  folder structure,
```bash
├── gossipcop
│   ├── fake
│   │   ├── gossipcop-1
│   │	│	├── news content.json
│   │	│	├── tweets
│   │	│	│	├── 886941526458347521.json
│   │	│	│	├── 887096424105627648.json
│   │	│	│	└── ....		
│   │	│  	└── retweets
│   │	│		├── 887096424105627648.json
│   │	│		├── 887096424105627648.json
│   │	│		└── ....
│   │	└── ....			
│   └── real
│      ├── gossipcop-1
│      │	├── news content.json
│      │	├── tweets
│      │	└── retweets
│		└── ....		
├── politifact
│   ├── fake
│   │   ├── politifact-1
│   │   │	├── news content.json
│   │   │	├── tweets
│   │   │	└── retweets
│   │	└── ....		
│   │
│   └── real
│      ├── poliifact-2
│      │	├── news content.json
│      │	├── tweets
│      │	└── retweets
│      └── ....					
├── user_profiles
│		├── 374136824.json
│		├── 937649414600101889.json
│   		└── ....
├── user_timeline_tweets
│		├── 374136824.json
│		├── 937649414600101889.json
│	   	└── ....
└── user_followers
│		├── 374136824.json
│		├── 937649414600101889.json
│	   	└── ....
└──user_following
        	├── 374136824.json
		├── 937649414600101889.json
	   	└── ....
```
**News Content**

`news content.json`:
This json includes all the meta information of the news articles collected using the provided news source URLs. This is a JSON object with attributes including:

 - `text` is the text of the body of the news article. 
 - `images` is a list of the URLs of all the images in the news article web page. 
 - `publish date`  indicate the date that news article is published.

**Social Context**

**`tweets` folder**:
This folder contains all tweets related to the news sample. This contains the tweet objects of the all the tweet ids provided in the tweet_ids attribute of the dataset csv. All the files in this folder are named as `<tweet_id>.json` . Each `<tweet_id>.json` file is a JSON file with format mentioned in [https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html).

**`retweets` folder**:
This folder contains the retweets of the all tweets posted sharing a particular news article. This folder contains files named as  `<tweet_id>.json` and it contains a array of the retweets for a particular tweets.  Each object int the retweet array have format mentioned in [https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-retweets-id](https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-retweets-id).

**`user_profiles` folder**:
This folder contains all the user profiles of the users posting tweets related to all news articles. This same folder is used for both datasources ( Politifact and GossipCop). It contains files named as `<user_id>.json` and have JSON formated mentioned in [https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object.html](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object.html)

**`user_timeline_tweets` folder**:
This folder contains files representing the time line of tweets of users posting tweets related to fake and real news. All files in the folder are named as `<user_id>.json` and have JSON array of upto 200 recent tweets of the users. The files have format mentioned same as [https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html](https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html).

**`user_followers` folder**:
This folder contains all the user followers ids of the users posting tweets related to all news articles. This same folder is used for both datasources ( Politifact and GossipCop). It contains files named as `<user_id>.json` and have JSON data with `user_id` and `followers` attributes.

**`user_following` folder**:
This folder contains all the user following ids of the users posting tweets related to all news articles. This same folder is used for both datasources ( Politifact and GossipCop). It contains files named as `<user_id>.json` and have JSON data with `user_id` and `following` attributes.


## References
If you use this dataset, please cite the following papers:
~~~~
@article{shu2018fakenewsnet,
  title={FakeNewsNet: A Data Repository with News Content, Social Context and Dynamic Information for Studying Fake News on Social Media},
  author={Shu, Kai and  Mahudeswaran, Deepak and Wang, Suhang and Lee, Dongwon and Liu, Huan},
  journal={arXiv preprint arXiv:1809.01286},
  year={2018}
}
~~~~
~~~~
@article{shu2017fake,
  title={Fake News Detection on Social Media: A Data Mining Perspective},
  author={Shu, Kai and Sliva, Amy and Wang, Suhang and Tang, Jiliang and Liu, Huan},
  journal={ACM SIGKDD Explorations Newsletter},
  volume={19},
  number={1},
  pages={22--36},
  year={2017},
  publisher={ACM}
}
~~~~
~~~~
@article{shu2017exploiting,
  title={Exploiting Tri-Relationship for Fake News Detection},
  author={Shu, Kai and Wang, Suhang and Liu, Huan},
  journal={arXiv preprint arXiv:1712.07709},
  year={2017}
}
~~~~



[Fake News Detection on Social Media: A Data Mining Perspective]:<https://arxiv.org/abs/1708.01967>
[Exploiting Tri-Relationship for Fake News Detection]:<http://arxiv.org/abs/1712.07709>
[FakeNewsTracker]:<http://blogtrackers.fulton.asu.edu:3000>
[FakeNewsNet]:<https://arxiv.org/abs/1809.01286>

(C) 2019 Arizona Board of Regents on Behalf of ASU

