import os
import pickle
import yaml
from selenium import webdriver

class Helper:
    @staticmethod
    def config(key=None, config_file='config.yaml'):
        contents = yaml.load(open(config_file, 'r'))

        if key in contents:
            return contents[key]
        else:
            return contents

    @staticmethod
    def store_cache(data, cache_file='.tr-cache'):
        with open(cache_file, 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def read_cache(cache_file='.tr-cache'):
        if not Helper.file_exists(cache_file):
            return False

        with open(cache_file, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def setup_webdriver(driver_path=None):
        if driver_path is None:
            driver_path = Helper.config('driver_path')

        return webdriver.Chrome(driver_path)

    @staticmethod
    def dir_exists(dir):
        return os.path.exists(dir)

    @staticmethod
    def file_exists(file):
        return os.path.isfile(file)

    @staticmethod
    def make_dir(dir):
        if not Helper.dir_exists(dir):
            os.makedirs(dir)

    @staticmethod
    def get_file_size(file):
        return os.stat(file).st_size
