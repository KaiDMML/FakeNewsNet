import csv
import json

from util.util import Config, News


class DataCollector:

    def __init__(self, config, function_reference):
        self.config = config
        self.function_reference = function_reference

    def collect_data(self, choices):
        for choice in choices:
            news_list = self.load_news_file(choice)
            self.function_reference(news_list, choice["news_source"], choice["label"], self.config)

    def load_news_file(self, data_choice):
        news_list = []
        with open('{}/{}_{}.csv'.format(self.config.dataset_dir, data_choice["news_source"],
                                        data_choice["label"])) as csvfile:
            reader = csv.DictReader(csvfile)
            for news in reader:
                news_list.append(News(news, data_choice["label"], data_choice["news_source"]))

        return news_list


def init_config():
    json_object = json.load(open("config.json"))

    config = Config(json_object["dump_location"], json_object["dataset_dir"], json_object["tweet_keys_file"],
                    int(json_object["num_process"]))

    data_choices = json_object["data_collection_choice"]
    data_features_to_collect = json_object["data_features_to_collect"]

    return config, data_choices, data_features_to_collect


if __name__ == "__main__":
    config, data_choices, data_features_to_collect = init_config()

