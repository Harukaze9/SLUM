import os
import argparse
import json
import datetime
import math
import pyperclip
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")
import data_manager_base


class GotoManager(data_manager_base.DataManagerBase):
    # Base
    main_dir          = os.path.dirname(os.path.realpath(__file__))
    data_dir = main_dir + "/data/"
    json_data = data_dir + 'content.json'
    use_category = False
    use_tag = False
    columns_show = ["timestamp"]


    def __init__(self):
        super().__init__()
        self.columns_show=["content", "timestamp"]

    def add_data(self, add_key, add_content):
        dt = datetime.datetime.now()
        dic = {}
        if not add_content:
            print("input content of {}".format(add_key))
            add_content = input()
        dic["content"] = add_content
        dic["timestamp"] = math.floor(dt.timestamp())
        self._add_data(add_key, dic)

    def delete_item_by_key(self, key, filepath = ""):
        print("content: {}".format(self.data[key]["content"]))
        super().delete_item_by_key(key, filepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="nothing....")
    parser.add_argument("--get", type=str)
    parser.add_argument("-k", "--key", type=str)
    parser.add_argument("-v", "--value", type=str)
    parser.add_argument("--read", action="store_true")
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--add", action="store_true")
    args = parser.parse_args()

    GTManager = GotoManager()

    if args.get != None:
        print(GTManager.data[args.get]["content"])
        exit(0)
    
    if args.read:
        GTManager.show_contents()
        exit(0)

    if args.clear:
        GTManager.reset_contents()
        GTManager.reload()
        GTManager.show_contents()
        exit(0)

    if args.add:
        GTManager.add_data(args.key, args.value)
        GTManager.reload()
        GTManager.show_contents()
        exit(0)
    
    if args.delete:
        GTManager.delete_item_by_key(args.key)
        GTManager.reload()
        GTManager.show_contents()
        exit(0)

