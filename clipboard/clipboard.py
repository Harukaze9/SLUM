import os
import argparse
import json
import datetime
import math
import pandas as pd #こいつのimport だけで0.5[s] かかる (これを外すと実行時間を含めて0.03[s]くらい)
import pyperclip
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")
import data_manager_base


class ClipBoardManager(data_manager_base.DataManagerBase):
    main_dir          = os.path.dirname(__file__)

    def __init__(self):
        super().__init__()
        self.columns_show=["content", "timestamp"]

    def copy_to_clipboard_by_input(self, target):
        if (len(self.df) == 0):
            print("data is empty")
            return
        if target:
            key = target
        else:
            self.show_contents()
            print("select a key to copy from", end=": ")
            print(list(self.df.sort_values("timestamp").index))
            key = input()
        while(key not in self.data):
            print("{} is not found in data. Select from".format(key), end=": ")
            print(list(self.df.sort_values("timestamp").index))
            key = input()
        content = self.data[key]["content"]
        pyperclip.copy(content)
        print("Success: clipboard <== [{}]".format(content))

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
    parser.add_argument("--clip", type=str)
    parser.add_argument("-k", "--key", type=str)
    parser.add_argument("-v", "--value", type=str)
    parser.add_argument("--read", action="store_true")
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--add", action="store_true")
    args = parser.parse_args()

    CBManager = ClipBoardManager()

    if args.clip != None:
        CBManager.copy_to_clipboard_by_input(args.clip)
        exit(0)
    
    if args.read:
        CBManager.show_contents()
        # CBManager.copy_to_clipboard_by_input(args.clip)
        exit(0)

    if args.clear:
        CBManager.reset_contents()
        CBManager.reload()
        CBManager.show_contents()
        exit(0)

    if args.add:
        CBManager.add_data(args.key, args.value)
        CBManager.reload()
        CBManager.show_contents()
        exit(0)
    
    if args.delete:
        CBManager.delete_item_by_key(args.key)
        CBManager.reload()
        CBManager.show_contents()
        exit(0)

