import json
import logging
import time
import requests

from twython import Twython


class TwythonConnector:

    def __init__(self, keys_server_url, key_file):
        self.streams = []
        self.init_twython_objects(key_file)
        self.url = "http://" + keys_server_url + "/get-keys?resource_type="
        self.max_fail_count = 3

    def init_twython_objects(self, keys_file):
        """
        Reads the keys file and initiates an array of twython objects
        :param keys_file: Twitter keys file
        :return:
        """
        keys = json.load(open(keys_file, 'r'))
        for key in keys:
            self.streams.append(self._get_twitter_connection(connection_mode=1, app_key=key['app_key'],
                                                             app_secret=key['app_secret'],
                                                             oauth_token=key['oauth_token'],
                                                             oauth_token_secret=key['oauth_token_secret']))

    @staticmethod
    def _get_twitter_connection(connection_mode=1, app_key=None, app_secret=None, oauth_token=None,
                                oauth_token_secret=None):
        client_args = {
            'timeout': 30,
        }

        if connection_mode == 1:  # User auth mode
            return Twython(app_key=app_key, app_secret=app_secret, oauth_token=oauth_token,
                           oauth_token_secret=oauth_token_secret, client_args=client_args)

        elif connection_mode == 0:  # App auth mode - more requests are allowed
            # TODO: Fix the code later - app auth has more limit
            # twitter = Twython(app_key, app_secret, oauth_version=2)
            # access_token = twitter.obtain_access_token()
            # return Twython(app_key, access_token=access_token)

            twitter = Twython(app_key, app_secret, oauth_version=2)
            ACCESS_TOKEN = twitter.obtain_access_token()
            twython = Twython(app_key, access_token=ACCESS_TOKEN)
            return twython

    def get_twython_connection(self, resource_type):
        """
        Returns the twython object for making the requests and sleeps if all the twitter keys have reached the usage
        limits
        :return: Twython object for making API calls
        """
        resource_index = self.get_resource_index(resource_type)
        return self.streams[resource_index]

    def get_resource_index(self, resource_type):
        # TODO: IMPORTANT! - Avoid this infinite waiting and use a heap to add those processes and check heap before
        # consuming message from Kafka
        while True:
            response = requests.get(self.url + resource_type)
            if response.status_code == 200:
                response = json.loads(response.text)
                if response["status"] == 200:
                    print("resource id : {}".format(response["id"]))
                    return response["id"]
                else:
                    print("sleeping for {} seconds".format(response["wait_time"]))
                    logging.info("sleeping for {} seconds".format(response["wait_time"]))
                    time.sleep(response["wait_time"])


# if __name__ == "__main__":
#
#     connector = TwythonConnector("0.0.0.0:5000",
#                                  "/Users/deepak/Desktop/DMML/GitRepo/fake_news_crawler/data/twitter_keys_unique.txt")
#
#     for i in range(1000):
#         connection = connector.get_twython_connection("get_followers_ids")
