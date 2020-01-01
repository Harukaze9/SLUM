import os
import argparse
import json
import datetime
import math
import pandas as pd #こいつのimport だけで0.5[s] かかる (これを外すと実行時間を含めて0.03[s]くらい)
import pyperclip


class DataManagerBase:
    main_dir          = os.path.dirname(os.path.abspath(__file__))
    data_dir = main_dir + "/data/"
    json_data = data_dir + 'content.json'

    def __init__(self):
        self.data = self.read_data()
        self.df = pd.DataFrame.from_dict(self.data, orient="index")
        self.df.index.name="key"

    def read_data(self):
        if not os.path.exists(self.json_data):
            print("{} was not found".format(self.json_data))
            print("Creating {}".format(self.json_data))
            self._create_initial_data()

        with open(self.json_data) as f:
            data = json.load(f)
            return data

    def add_data(self, add_key, add_content):
        data_dict = {}
        data_dict["content"] = add_content
        self._add_data(add_key, data_dict)

    def _add_data(self, add_key, data_dict):
        dt = datetime.datetime.now()
        data_dict["timestamp"] = math.floor(dt.timestamp())
        self.data[add_key] = data_dict
        with open(self.json_data, "w") as f:
            json.dump(self.data, f)
        print("Success: {} is added!".format(add_key))


    def show_contents(self, short=False):
        self._show_contents()

    def _show_contents(self, columns = []):
        if (len(self.df) == 0):
            self.reset_contents()
        print("=============== Database =====================")
        if columns:
            print(self.df.sort_values("timestamp")[columns].head(n=1000))
        else:
            print(self.df.sort_values("timestamp").head(n=1000))
        print("===============================================")


    def reset_contents(self):
        self._create_initial_data()
        print("Success: cleared")
        self.reload()

    def _create_initial_data(self):
        dic = {"example":
                {"content": "\"this is an example string\"",
                "timestamp": 0} }
        with open(self.json_data, "w") as f:
            json.dump(dic, f)

    def reload(self):
        self.data = self.read_data()
        self.df = pd.DataFrame.from_dict(self.data, orient="index")
        self.df.index.name="key"


    def delete_item_by_key(self, key, filepath = ""):
        if key in self.data:
            print("\"{}\" is deleted".format(key))
            del self.data[key]
            f = open(self.json_data, "w")
            json.dump(self.data, f)
            if filepath:
                os.remove(filepath)
                print("{} is removed!".format(filepath))
        else:
            print("\"{}\" is not found in data".format(key))
            exit()


