import csv
import errno
import os
import sys
from multiprocessing.pool import Pool

from tqdm import tqdm

from util.TwythonConnector import TwythonConnector


class News:

    def __init__(self, info_dict, label, news_platform):
        self.news_id = info_dict["id"]
        self.news_url = info_dict["news_url"]
        self.news_title = info_dict["title"]
        self.tweet_ids =[]

        try:
            tweets =  [int(tweet_id) for tweet_id in info_dict["tweet_ids"].split("\t")]
            self.tweet_ids = tweets
        except:
            pass

        self.label = label
        self.platform = news_platform



class Config:

    def __init__(self, data_dir, data_collection_dir, tweet_keys_file, num_process):
        self.dataset_dir = data_dir
        self.dump_location = data_collection_dir
        self.tweet_keys_file = tweet_keys_file
        self.num_process = num_process

        self.twython_connector = TwythonConnector("localhost:5000", tweet_keys_file)



class DataCollector:

    def __init__(self, config):
        self.config = config

    def collect_data(self, choices):
        pass

    def load_news_file(self, data_choice):
        maxInt = sys.maxsize
        while True:
            # decrease the maxInt value by factor 10
            # as long as the OverflowError occurs.
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt / 10)

        news_list = []
        with open('{}/{}_{}.csv'.format(self.config.dataset_dir, data_choice["news_source"],
                                        data_choice["label"]), encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for news in reader:
                news_list.append(News(news, data_choice["label"], data_choice["news_source"]))

        return news_list


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def is_folder_exists(folder_name):
    return os.path.exists(folder_name)


def equal_chunks(list, chunk_size):
    """return successive n-sized chunks from l."""
    chunks = []
    for i in range(0, len(list), chunk_size):
        chunks.append(list[i:i + chunk_size])

    return chunks


def multiprocess_data_collection(function_reference, data_list, args, config: Config):
    # Create process pool of pre defined size
    pool = Pool(config.num_process)

    pbar = tqdm(total=len(data_list))

    def update(arg):
        pbar.update()

    for i in range(pbar.total):
        pool.apply_async(function_reference, args=(data_list[i],)+ args, callback=update)

    pool.close()
    pool.join()
