import json


def read_config() -> dict:
    with open('config.json', "r") as config_file:
        config = json.load(config_file)
        return config


def read_white_list() -> dict:
    with open('white_list.json', "r") as config_file:
        config = json.load(config_file)
        return config