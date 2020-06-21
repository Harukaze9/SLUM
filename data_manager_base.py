import os
import argparse
import json
import datetime
import math
import pyperclip


class DataManagerBase:
    main_dir          = os.path.dirname(os.path.realpath(__file__))
    data_dir = main_dir + "/data/"
    json_data = data_dir + 'content.json'
    use_category = False
    use_tag = False
    columns_show = ["timestamp"]

    def __init__(self):
        self.data = self.read_data()

    def read_data(self):
        if not os.path.exists(self.json_data):
            print("{} was not found".format(self.json_data))
            print("Creating {}".format(self.json_data))
            self._write_initial_data()
        with open(self.json_data) as f:
            data = json.load(f)
            return data

    def add_data(self, add_key, add_content):
        data_dict = {}
        data_dict["content"] = add_content
        self._add_data(add_key, data_dict)

    def _add_data(self, add_key, data_dict):
        if add_key in self.data.keys():
            print("Error: {} already exists.".format(add_key))
            exit(1)
        dt = datetime.datetime.now()
        data_dict["timestamp"] = math.floor(dt.timestamp())
        self.data[add_key] = data_dict
        with open(self.json_data, "w") as f:
            json.dump(self.data, f)
        print("Success: {} is added!".format(add_key))

    def overwrite(self):
        with open(self.json_data, "w") as f:
            json.dump(self.data, f)
        print("Success: overwrtitten")

    def show_contents(self, short=False):
        self._show_contents(self.columns_show)

    def _show_contents(self, columns = []):
        if len(self.data) == 0:
            self.reset_contents()
        print("=============== Database =====================")
        for k in self.data:
            print("{}: \t{}".format(k, self.data[k]["content"]))
            
        print("===============================================")

    def create_backup(self):
        dt = datetime.datetime.now()
        timestamp = str(dt.date()) +"-"+ str(dt.hour) +"-"+ str(dt.minute)
        backup_filename = "content_backup-" + timestamp
        with open(backup_filename, "w") as f:
            json.dump(self.data, f)

    def reset_contents(self):
        self.create_backup()
        exit()
        self._write_initial_data()
        print("Success: cleared")
        self.reload()

    def _write_initial_data(self):
        dic = {"example":
                {"content": "\"this is an example string\"",
                "timestamp": 0} }
        with open(self.json_data, "w") as f:
            json.dump(dic, f)

    def reload(self):
        self.data = self.read_data()

    def delete_item_by_key(self, key, filepath = ""):
        if key in self.data:
            print("\"{}\" is deleted".format(key))
            del self.data[key]
            f = open(self.json_data, "w")
            json.dump(self.data, f)
            if os.path.exists(filepath):
                os.remove(filepath)
                print("{} is removed!".format(filepath))
        else:
            print("\"{}\" is not found in data".format(key))
            exit()

    def set_category(self, key, category):
        if not self.use_category:
            print("Error: this class does not use category")
            exit(1)
        if key not in self.data.keys():
            print("Error: {} is not contained in the data".format(key))
            exit(1)
        self.data[key]["category"]=category
        print("{} is added to {} as the category".format(category, key))
        self.overwrite()

    def set_tags(self, key, tags):
        if not self.use_tag:
            print("Error: this class does not use tag")
            exit(1)
        if key not in self.data.keys():
            print("Error: {} is not contained in the data".format(key))
            exit(1)
        self.data[key]["tags"]= tags
        print("{} is added to {} as the tags".format(tags, key))
        self.overwrite()







