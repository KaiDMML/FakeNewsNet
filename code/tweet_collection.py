import json
import logging
from multiprocessing.pool import Pool

from util.TwythonConnector import TwythonConnector
from twython import TwythonError, TwythonRateLimitError

from util.util import create_dir, Config, multiprocess_data_collection

from util.util import DataCollector
from util import Constants

from util.util import equal_chunks


class Tweet:

    def __init__(self, tweet_id, news_id, news_source, label):
        self.tweet_id = tweet_id
        self.news_id = news_id
        self.news_source = news_source
        self.label = label


def dump_tweet_information(tweet_chunk: list, config: Config, twython_connector: TwythonConnector):
    """Collect info and dump info of tweet chunk containing atmost 100 tweets"""

    tweet_list = []
    for tweet in tweet_chunk:
        tweet_list.append(tweet.tweet_id)

    try:
        tweet_objects_map = twython_connector.get_twython_connection(Constants.GET_TWEET).lookup_status(id=tweet_list,
                                                                                                    include_entities=True,
                                                                                                    map=True)['id']
        for tweet in tweet_chunk:
            tweet_object = tweet_objects_map[str(tweet.tweet_id)]
            if tweet_object:
                dump_dir = "{}/{}/{}/{}".format(config.dump_location, tweet.news_source, tweet.label, tweet.news_id)
                tweet_dir = "{}/tweets".format(dump_dir)
                create_dir(dump_dir)
                create_dir(tweet_dir)

                json.dump(tweet_object, open("{}/{}.json".format(tweet_dir, tweet.tweet_id), "w"))

    except TwythonRateLimitError:
        logging.exception("Twython API rate limit exception")

    except Exception as ex:
        logging.exception("exception in collecting tweet objects")

    return None


def collect_tweets(news_list, news_source, label, config: Config):
    create_dir(config.dump_location)
    create_dir("{}/{}".format(config.dump_location, news_source))
    create_dir("{}/{}/{}".format(config.dump_location, news_source, label))

    save_dir = "{}/{}/{}".format(config.dump_location, news_source, label)

    tweet_id_list = []

    for news in news_list:
        for tweet_id in news.tweet_ids:
            tweet_id_list.append(Tweet(tweet_id, news.news_id, news_source, label))

    tweet_chunks = equal_chunks(tweet_id_list, 100)
    multiprocess_data_collection(dump_tweet_information, tweet_chunks, (config, config.twython_connector), config)


class TweetCollector(DataCollector):

    def __init__(self, config):
        super(TweetCollector, self).__init__(config)

    def collect_data(self, choices):
        for choice in choices:
            news_list = self.load_news_file(choice)
            collect_tweets(news_list, choice["news_source"], choice["label"], self.config)
