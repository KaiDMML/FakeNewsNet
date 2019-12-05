import json
import logging

from twython import TwythonError, TwythonRateLimitError

from util import Constants
from util.TwythonConnector import TwythonConnector
from util.util import (
    Tweet,
    Config,
    DataCollector,
    create_dir,
    get_dump_dir,
    is_file_exists,
    multiprocess_data_collection,
)


def _should_skip_retweets(tweet: Tweet, dump_dir: str):
    retweet_filename = "{}/retweets/{}.json".format(dump_dir, tweet.tweet_id)
    if is_file_exists(retweet_filename):
        return True
    tweet_filename = "{}/tweets/{}.json".format(dump_dir, tweet.tweet_id)
    if not is_file_exists(tweet_filename):
        return True
    return False


def _should_fetch_retweets(tweet: Tweet, dump_dir: str):
    tweet_filename = "{}/tweets/{}.json".format(dump_dir, tweet.tweet_id)
    with open(tweet_filename) as file:
        tweet_object = json.load(file)
    return tweet_object.get("retweet_count", 0) > 0


def dump_retweets_job(
    tweet: Tweet, config: Config, twython_connector: TwythonConnector
):
    retweets = []
    connection = None

    dump_dir = get_dump_dir(config, tweet)

    if _should_fetch_retweets(tweet, dump_dir):
        try:
            connection = twython_connector.get_twython_connection(Constants.GET_RETWEET)
            retweets = connection.get_retweets(id=tweet.tweet_id, count=100, cursor=-1)

        except TwythonRateLimitError:
            logging.exception(
                "Twython API rate limit exception - tweet id : {}".format(
                    tweet.tweet_id
                )
            )

        except Exception:
            logging.exception(
                "Exception in getting retweets for tweet id %d using connection %s"
                % (tweet.tweet_id, connection)
            )

    retweet_obj = {"retweets": retweets}

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

    filtered_tweet_id_list = [
        tweet
        for tweet in tweet_id_list
        if not _should_skip_retweets(tweet, get_dump_dir(config, tweet),)
    ]

    multiprocess_data_collection(
        dump_retweets_job,
        filtered_tweet_id_list,
        (config, config.twython_connector),
        config,
    )


class RetweetCollector(DataCollector):
    def __init__(self, config):
        super(RetweetCollector, self).__init__(config)

    def collect_data(self, choices):
        for choice in choices:
            news_list = self.load_news_file(choice)
            collect_retweets(
                news_list, choice["news_source"], choice["label"], self.config
            )
