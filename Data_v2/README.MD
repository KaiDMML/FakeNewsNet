### Data Collection:    
    
Complete dataset cannot be distributed because of Twitter privacy policies and websites publisher copy right information.    
    
This code can be used to download news articles from published websites and relevant social media data from Twitter.  
    
### Requirements:    
      
 python 3.6 +  

Twitter API keys for collecting data from Twitter.     
    
Make use of the following link to get Twitter API keys    
https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html    
    
The API keys needs to the updated in _tweet_keys_file.txt_ file.    
  
Install all the libraries in `requirements.txt`    
    
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


### Dataset format
The downloaded dataset will have the following  folder structure,
```bash
├── gossipcop
│   ├── fake
│   │   ├── gossipcop-1
│   │	│	├── news content.json
│   │	│	├── tweets
│	│	│	│	├── 886941526458347521.json
│	│	│	│	├── 887096424105627648.json
│	│	│	│	└── ....		
│   │	│  └── retweets
│	│	│		├── 887096424105627648.json
│	│	│		├── 887096424105627648.json
│	│	│		└── ....
│	│	└── ....			
│   └── real
│      ├── gossipcop-1
│      │	├── news content.json
│      │	├── tweets
│	   │	└── retweets
│		└── ....		
├── politifact
│   ├── fake
│   │   ├── politifact-1
│   │   │	├── news content.json
│   │   │	├── tweets
│	│   │	└── retweets
│	│	└── ....		
│	│
│   └── real
│      ├── poliifact-2
│      │	├── news content.json
│      │	├── tweets
│	   │	└── retweets
│		└── ....					
├── user_profiles
└── user_timeline_tweets
```

