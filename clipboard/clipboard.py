import os
import argparse
import json
import datetime
import math
import pandas as pd #こいつのimport だけで0.5[s] かかる (これを外すと実行時間を含めて0.03[s]くらい)
import pyperclip


class ClipBoardManager:
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
            with open(self.json_data, "w") as f:
                dic = self.get_initial_data()
                # json_data = json.dumps(dic)
                json.dump(dic, f)

        with open(self.json_data) as f:
            data = json.load(f)
            return data

    def add_data(self, add_key, add_content):
        dt = datetime.datetime.now()
        self.data[add_key] = {}
        if not add_content:
            print("input content of {}".format(add_key))
            add_content = input()
        self.data[add_key]["content"] = add_content
        self.data[add_key]["timestamp"] = math.floor(dt.timestamp())
        f = open(self.json_data, "w")
        json.dump(self.data, f)
        print("Success: {} is added!".format(add_key))

    def show_contents(self, short=False):
        if (len(self.df) == 0):
            self.reset_contents()
        print("=============== Database =====================")
        if short:
            print(list(self.df.sort_values("timestamp").index))
        else:
            print(self.df.sort_values("timestamp").head(n=10))
        print("===============================================")

    def reset_contents(self):
        with open(self.json_data, "w") as f:
            json.dump(self.get_initial_data(), f)
        print("Success: cleared")
        self.reload()

    def get_initial_data(self):
        dic = {"example":
                {"content": "\"this is an example string\"",
                "timestamp": 0} }
        return dic

    def reload(self):
        self.data = self.read_data()
        self.df = pd.DataFrame.from_dict(self.data, orient="index")
        self.df.index.name="key"

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

    def delete_item_by_key(self, key):
        if key in self.data:
            print("\"{} ({})\" is deleted".format(key, self.data[key]["content"]))
            del self.data[key]
            f = open(self.json_data, "w")
            json.dump(self.data, f)
        else:
            print("\"{}\" is not found in data".format(key))
            exit()

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

