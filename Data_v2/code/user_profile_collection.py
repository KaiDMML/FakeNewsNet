import json
import logging
import os
from pathlib import Path

from util.Constants import GET_USER, GET_USER_TWEETS
from util.TwythonConnector import TwythonConnector
from util.util import Config, is_folder_exists, create_dir, multiprocess_data_collection


def get_user_ids_in_folder(samples_folder):
    user_ids = set()

    for news_id in os.listdir(samples_folder):
        news_dir = "{}/{}".format(samples_folder, news_id)
        tweets_dir = "{}/{}/tweets".format(samples_folder, news_id)
        if is_folder_exists(news_dir) and is_folder_exists(tweets_dir):

            for tweet_file in os.listdir(tweets_dir):
                tweet_object = json.load(open("{}/{}".format(tweets_dir, tweet_file)))

                user_ids.add(tweet_object["user"]["id"])

    return user_ids


def dump_user_profile_job(user_id, save_location, twython_connector: TwythonConnector):
    profile_info = None

    # Fetch and save user information if the file is not already present
    if not Path("{}/{}.json".format(save_location, user_id)).is_file():
        try:
            profile_info = twython_connector.get_twython_connection(GET_USER).show_user(user_id=user_id)

        except TwythonRateLimitError as ex:
            logging.exception("Twython API rate limit exception")

        finally:
            if profile_info:
                json.dump(profile_info, open("{}/{}.json".format(save_location, user_id), "w"))


def dump_user_recent_tweets_job(user_id, save_location, twython_connector: TwythonConnector):
    profile_info = None

    # Fetch and save user information if the file is not already present
    if not Path("{}/{}.json".format(save_location, user_id)).is_file():
        try:
            profile_info = twython_connector.get_twython_connection(GET_USER_TWEETS).get_user_timeline(user_id=user_id, count=200)

        except TwythonRateLimitError as ex:
            logging.exception("Twython API rate limit exception")

        finally:
            if profile_info:
                json.dump(profile_info, open("{}/{}.json".format(save_location, user_id), "w"))



def collect_user_profiles(config: Config, twython_connector: TwythonConnector):
    dump_location = config.dump_location

    all_user_ids = set()

    all_user_ids.update(get_user_ids_in_folder("{}/politifact/fake".format(dump_location)))
    all_user_ids.update(get_user_ids_in_folder("{}/politifact/real".format(dump_location)))
    all_user_ids.update(get_user_ids_in_folder("{}/gossipcop/fake".format(dump_location)))
    all_user_ids.update(get_user_ids_in_folder("{}/gossipcop/real".format(dump_location)))

    user_profiles_folder = "{}/{}".format(dump_location, "user_profiles")
    user_timeline_tweets_folder = "{}/{}".format(dump_location, "user_timeline_tweets")

    create_dir(user_profiles_folder)
    create_dir(user_timeline_tweets_folder)

    multiprocess_data_collection(dump_user_profile_job, all_user_ids, (user_profiles_folder, twython_connector), config)
    multiprocess_data_collection(dump_user_recent_tweets_job, all_user_ids, (user_timeline_tweets_folder,
                                                                             twython_connector), config)

