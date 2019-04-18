import json
import logging
import os
from pathlib import Path
from twython import TwythonError, TwythonRateLimitError

from util.Constants import GET_USER, GET_USER_TWEETS, USER_ID, FOLLOWERS, GET_FRIENDS_ID, FOLLOWING
from util.TwythonConnector import TwythonConnector
from util.util import Config, is_folder_exists, create_dir, multiprocess_data_collection

from util.util import DataCollector

from util.Constants import GET_FOLLOWERS_ID


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
            profile_info = twython_connector.get_twython_connection(GET_USER_TWEETS).get_user_timeline(user_id=user_id,
                                                                                                       count=200)

        except TwythonRateLimitError as ex:
            logging.exception("Twython API rate limit exception")

        finally:
            if profile_info:
                json.dump(profile_info, open("{}/{}.json".format(save_location, user_id), "w"))


def fetch_user_follower_ids(user_id, twython_connection):
    user_followers = []

    try:
        user_followers = twython_connection.get_followers_ids(user_id=user_id)
        user_followers = user_followers["ids"]
    except:
        logging.exception("Exception in follower_ids for user : {}".format(user_id))

    return user_followers


def fetch_user_friends_ids(user_id, twython_connection):
    user_friends = []

    try:
        user_friends = twython_connection.get_friends_ids(user_id=user_id)
        user_friends = user_friends["ids"]
    except:
        logging.exception("Exception in follower_ids for user : {}".format(user_id))

    return user_friends


def dump_user_followers(user_id, save_location, twython_connector: TwythonConnector):

    # Fetch and save user information if the file is not already present
    if not Path("{}/{}.json".format(save_location, user_id)).is_file():
        try:
            user_followers = fetch_user_follower_ids(user_id, twython_connector.get_twython_connection(GET_FOLLOWERS_ID))

            user_followers_info = {USER_ID: user_id, FOLLOWERS: user_followers}
            json.dump(user_followers_info, open("{}/{}.json".format(save_location, user_id), "w"))

        except:
            logging.exception("Exception in getting follower_ids for user : {}".format(user_id))


def dump_user_following(user_id, save_location, twython_connector: TwythonConnector):

    # Fetch and save user information if the file is not already present
    if not Path("{}/{}.json".format(save_location, user_id)).is_file():
        try:
            user_following = fetch_user_friends_ids(user_id, twython_connector.get_twython_connection(GET_FRIENDS_ID))

            user_following_info = {USER_ID: user_id,FOLLOWING : user_following}
            json.dump(user_following_info, open("{}/{}.json".format(save_location, user_id), "w"))

        except:
            logging.exception("Exception in getting follower_ids for user : {}".format(user_id))



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


class UserProfileCollector(DataCollector):

    def __init__(self, config):
        super(UserProfileCollector, self).__init__(config)

    def collect_data(self, choices):
        all_user_ids = set()

        for choice in choices:
            all_user_ids.update(get_user_ids_in_folder(
                "{}/{}/{}".format(self.config.dump_location, choice["news_source"], choice["label"])))

        user_profiles_folder = "{}/{}".format(self.config.dump_location, "user_profiles")
        create_dir(user_profiles_folder)

        multiprocess_data_collection(dump_user_profile_job, list(all_user_ids),
                                     (user_profiles_folder, self.config.twython_connector),
                                     self.config)


class UserTimelineTweetsCollector(DataCollector):

    def __init__(self, config):
        super(UserTimelineTweetsCollector, self).__init__(config)

    def collect_data(self, choices):
        all_user_ids = set()

        for choice in choices:
            all_user_ids.update(get_user_ids_in_folder(
                "{}/{}/{}".format(self.config.dump_location, choice["news_source"], choice["label"])))

        user_timeline_tweets_folder = "{}/{}".format(self.config.dump_location, "user_timeline_tweets")
        create_dir(user_timeline_tweets_folder)

        multiprocess_data_collection(dump_user_recent_tweets_job, list(all_user_ids), (user_timeline_tweets_folder,
                                                                                       self.config.twython_connector),
                                     self.config)


class UserFollowersCollector(DataCollector):

    def __init__(self, config):
        super(UserFollowersCollector, self).__init__(config)

    def collect_data(self, choices):
        all_user_ids = set()

        for choice in choices:
            all_user_ids.update(get_user_ids_in_folder(
                "{}/{}/{}".format(self.config.dump_location, choice["news_source"], choice["label"])))

        user_followers_folder = "{}/{}".format(self.config.dump_location, "user_followers")
        create_dir(user_followers_folder)

        multiprocess_data_collection(dump_user_followers, list(all_user_ids), (user_followers_folder,
                                                                                       self.config.twython_connector),
                                     self.config)


class UserFollowingCollector(DataCollector):

    def __init__(self, config):
        super(UserFollowingCollector, self).__init__(config)

    def collect_data(self, choices):
        all_user_ids = set()

        for choice in choices:
            all_user_ids.update(get_user_ids_in_folder(
                "{}/{}/{}".format(self.config.dump_location, choice["news_source"], choice["label"])))

        user_friends_folder = "{}/{}".format(self.config.dump_location, "user_following")
        create_dir(user_friends_folder)

        multiprocess_data_collection(dump_user_following, list(all_user_ids), (user_friends_folder,
                                                                                       self.config.twython_connector),
                                     self.config)

