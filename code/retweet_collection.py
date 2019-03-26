import json
import logging
from twython import TwythonError, TwythonRateLimitError


from tweet_collection import Tweet
from util.TwythonConnector import TwythonConnector
from util.util import create_dir, Config, multiprocess_data_collection

from util.util import DataCollector
from util import Constants


def dump_retweets_job(tweet: Tweet, config: Config, twython_connector: TwythonConnector):
    retweets = []
    connection = None
    try:
        connection = twython_connector.get_twython_connection("get_retweet")
        retweets = connection.get_retweets(id=tweet.tweet_id, count=100, cursor=-1)

    except TwythonRateLimitError:
        logging.exception("Twython API rate limit exception - tweet id : {}".format(tweet.tweet_id))

    except Exception:
        logging.exception(
            "Exception in getting retweets for tweet id %d using connection %s" % (tweet.tweet_id, connection))

    retweet_obj = {"retweets": retweets}

    dump_dir = "{}/{}/{}/{}".format(config.dump_location, tweet.news_source, tweet.label, tweet.news_id)
    retweet_dir = "{}/retweets".format(dump_dir)
    create_dir(dump_dir)
    create_dir(retweet_dir)
    json.dump(retweet_obj, open("{}/{}.json".format(retweet_dir, tweet.tweet_id), "w"))


def collect_retweets(news_list, news_source, label, config: Config):
    create_dir(config.dump_location)
    create_dir("{}/{}".format(config.dump_location, news_source))
    create_dir("{}/{}/{}".format(config.dump_location, news_source, label))

    save_dir = "{}/{}/{}".format(config.dump_location, news_source, label)

    tweet_id_list = []

    for news in news_list:
        for tweet_id in news.tweet_ids:
            tweet_id_list.append(Tweet(tweet_id, news.news_id, news_source, label))

    multiprocess_data_collection(dump_retweets_job, tweet_id_list, (config, config.twython_connector), config)


class RetweetCollector(DataCollector):

    def __init__(self, config):
        super(RetweetCollector, self).__init__(config)

    def collect_data(self, choices):
        for choice in choices:
            news_list = self.load_news_file(choice)
            collect_retweets(news_list, choice["news_source"], choice["label"], self.config)
