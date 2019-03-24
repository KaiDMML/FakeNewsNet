import csv
import json

from util.util import Config, News

from code.news_content_collection import NewsContentCollector
from code.retweet_collection import RetweetCollector
from code.tweet_collection import TweetCollector
from code.user_profile_collection import UserProfileCollector, UserTimelineTweetsCollector


class DataCollectorFactory:

    def __init__(self, config):
        self.config = config

    def get_collector_object(self, feature_type):

        if feature_type == "news_articles":
            return NewsContentCollector()
        elif feature_type == "tweets":
            return TweetCollector()
        elif feature_type == "retweets":
            return RetweetCollector()
        elif feature_type == "user_profile":
            return UserProfileCollector()
        elif feature_type == "user_timeline_tweets":
            return UserTimelineTweetsCollector()


def init_config():
    json_object = json.load(open("config.json"))

    config = Config(json_object["dump_location"], json_object["dataset_dir"], json_object["tweet_keys_file"],
                    int(json_object["num_process"]))

    data_choices = json_object["data_collection_choice"]
    data_features_to_collect = json_object["data_features_to_collect"]

    return config, data_choices, data_features_to_collect


def download_dataset():
    config, data_choices, data_features_to_collect = init_config()
    data_collector_factory = DataCollectorFactory(config)

    for feature_type in data_features_to_collect:
        data_collector = data_collector_factory.get_collector_object(feature_type)
        data_collector.collect_data(data_choices)


if __name__ == "__main__":
    download_dataset()