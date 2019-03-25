
## FakeNewsNet v2

### Data Collection:    
Complete dataset cannot be distributed because of Twitter privacy policies and websites publisher copy right information.  This code repository can be used to download news articles from published websites and relevant social media data from Twitter. 
    
The minimalistic version of v2 dataset provied in this repo (located in `dataset` folder) include following files:

 - `politifact_fake.csv` -  Samples related to fake news collected from PolitiFact 
 - `politifact_real.csv` -  Samples related to real news collected  from PolitiFact 
 - `gossipcop_fake.csv` - Samples related to fake news collected from GossipCop
  - `gossipcop_real.csv` - Samples related to real news collected from GossipCop

Each of the above CSV files are comma separated files and have the following columns

 - `id` - unique identifider added for each sample
 - `url` - Url of the article from web that published that news 
 - `title` - Title of the news article found in the URL
 - `tweet_ids` - Tweet ids of tweets related to news sample posted on Twitter. This field is list of tweet ids separated by tab.
 - 
Social engagements and user information are not disclosed because of Twitter Policy. 

### Requirements:    

 python 3.6 +  

Twitter API keys for collecting data from Twitter.     
    
Make use of the following link to get Twitter API keys    
https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html   
    
The API keys needs to the updated in _tweet_keys_file.txt_ file.  Provide the keys as rows where each row represents the parts of the keys in the following order `app_key,app_secret,oauth_token,oauth_token_secret`

  
Install all the libraries in `requirements.txt` using the following command
    
    pip install -r requirements.txt

 FakeNewsNet v2 contains 2 datasets collected using ground truths from _Politifact_ and _Gossipcop_.  
    
The `config.json` can be used to configure and collect only certain parts of the dataset.    
    
Following attributes can be configured    
  
 - **num_process** - (default: 4) This attribute indicates the number of  
   parallel processes used to collect data.    
 - **tweet_keys_file** - Provide the number of keys available configured in tweet_keys_file.txt file       
 - **data_collection_choice** - It is an array of choices of various parts  
   of the dataset. Configure accordingly to download only certain parts of the dataset.       
   Available values are  
  
     {"news_source": "politifact", "label": "fake"},{"news_source": "politifact", "label":    "real"}, {"news_source": "gossipcop", "label": "fake"},{"news_source": "gossipcop", "label": "real"}  
  
 - **data_features_to_collect** - FakeNewsNet has multiple dimensions of data (News + Social). This configuration allows one to download desired dimension of the dataset. This is an array field and can take following values.  
	              
	 - **news_articles** : This option downloads the news articles for the dataset.  
     - **tweets** : Download tweets objects posted sharing the news in Twitter. This makes use of Twitter API to download tweets.  
     - **retweets**: This option allows to download the retweets of the tweets provided in the dataset.  
      - **user_profile**: This option allows to download the user profile information of the users involved in tweets. To download user profiles, tweet objects need to be downloaded first inorder to identify users involved in tweets.  
      - **user_timeline_tweets**: This option allows to download upto 200 recent tweets from the user timeline. To download user's recent tweets, tweet objects needs to be downloaded first inorder to identify users involved in tweets.

### Running data collection
Inorder to collect data set fast, code makes user of process parallelism and to synchronize twitter key limitations across mutiple python processes, a lightweight flask application is used as keys management server.
Execute the following commands inside `code` folder,

    nohup python -m resource_server.app &> keys_server.out&

The above command will start the flask server in port 5000 by default.

Configure before starting the data collection.
Execute the following command to start data collection,

    nohup python main.py &> data_collection.out&

Logs are wittern in the same folder in a file named as `data_collection_<timestamp>.log` and can be used for debugging purposes.

The dataset will be downloaded in the directory provided in the `config.json`

### Dataset format
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
└── user_timeline_tweets
```
**News Content** - `news content.json`
This json includes all the meta information of the news articles collected using the provided news source URLs. This is a JSON object with attributes including:

 - `text` is the text of the body of the news article. 
 - `images` is a list of the URLs of all the images in the news article web page. 
 - `publish date`  indicate the date that news article is published.

**Social Context**

**`tweets` folder**:
This folder contains all tweets related to the news sample. This contains the tweet objects of the all the tweet ids provided in the tweet_ids attribute of the dataset csv. All the files in this folder are named as `<tweet_id>.json` . Each `<tweet_id>.json` file is a JSON file with format mentioned [https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html).

**`retweets` folder**:
This folder contains the retweets of the all tweets posted sharing a particular news article. This folder contains files named as  `<tweet_id>.json` and it contains a array of the retweets for a particular tweets.  Each object int the retweet array have format mentioned in [https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-retweets-id](https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-retweets-id).

**`user_profiles` folder**:
This folder contains all the user profiles of the users posting tweets related to all news articles. This same folder is used for both datasources ( Politifact and GossipCop). It contains files named as `<user_id>.json` and have JSON formated mentioned in [https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object.html](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object.html)

**`user_timeline_tweets` folder**:
This folder contains files representing the time line of tweets of users posting tweets related to fake and real news. All files in the folder are named as `<user_id>.json` and have JSON array of upto 200 recent tweets of the users. The files have format mentioned same as [https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html](https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html).

