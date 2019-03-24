import csv
import errno
import os
from multiprocessing.pool import Pool

from tqdm import tqdm


class News:

    def __init__(self, info_dict, label, news_platform):
        self.news_id = info_dict["id"]
        self.news_url = info_dict["news_url"]
        self.news_title = info_dict["title"]
        self.tweet_ids = [int(tweet_id) for tweet_id in info_dict["tweet_ids"].split("\t")]

        self.label = label
        self.platform = news_platform

        self.twython_connector = None


class Config:

    def __init__(self, data_dir, data_collection_dir, tweet_keys_file, num_process):
        self.dataset_dir = data_dir
        self.dump_location = data_collection_dir
        self.tweet_keys_file = tweet_keys_file
        self.num_process = num_process


class DataCollector:

    def __init__(self, config):
        self.config = config

    def collect_data(self, choices):
        pass

    def load_news_file(self, data_choice):
        news_list = []
        with open('{}/{}_{}.csv'.format(self.config.dataset_dir, data_choice["news_source"],
                                        data_choice["label"])) as csvfile:
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


def multiprocess_data_collection(function_reference, data_list, args, config: Config):
    # Create process pool of pre defined size
    pool = Pool(config.num_process)

    pbar = tqdm(total=100)

    def update():
        pbar.update()

    for i in range(pbar.total):
        pool.apply_async(function_reference, args=(data_list[i], args), callback=update)

    pool.close()
    pool.join()
