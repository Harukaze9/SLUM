import os
import argparse
import json
import datetime
import math
import pandas as pd
import pyperclip
import sys

sys.path.append("../")
import data_manager_base


class NoteManager(data_manager_base.DataManagerBase):
    main_dir          = os.path.dirname(os.path.abspath(__file__))
    data_dir = main_dir + "/data/"
    note_dir = main_dir + "/.notes/"
    json_data = data_dir + 'content.json'

    def __init__(self):
        super().__init__()

    def add_data(self, key, category):
        note_path = os.path.join(self.note_dir, key + ".md")
        data_dict = {}
        data_dict["note_path"] = note_path
        data_dict["category"] = category
        self._add_data(key, data_dict)
        content = "# {}".format(key)
        self._create_note_file(note_path, content)

    def _create_note_file(self, file_path, content):
        with open(file_path,'w') as f:
            f.write(content)
        print("{} is created!".format(file_path))

    def show_contents(self, short=False):
        columns = ["category", "timestamp", "note_path"]
        self._show_contents(columns)
        
    def _get_initial_data(self):
        example_note_path = os.path.join(self.note_dir, "example.md")
        dic = {"example":
                {"note_path": example_note_path,
                "timestamp": 0,
                "category": None,
                }}
        return dic

    def delete_item_by_key(self, key):
        note_path = self.data[key]["note_path"]
        super().delete_item_by_key(key, note_path)
        # os.remove(note_path)
        # print("{} is removed!".format(note_path))
    
    def reset_contents(self):
        for key in self.data.keys():
            note_path = self.data[key]["note_path"]
            if os.path.exists(note_path):
                os.remove(note_path)
        super().reset_contents()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="nothing....")
    parser.add_argument("--clip", type=str)
    parser.add_argument("-k", "--key", type=str)
    parser.add_argument("-c", "--category", type=str)
    parser.add_argument("--read", action="store_true")
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--add", action="store_true")
    args = parser.parse_args()

    NManager = NoteManager()

    if args.clip != None:
        NManager.copy_to_clipboard_by_input(args.clip)
        exit(0)
    
    if args.read:
        NManager.show_contents()
        # NManager.copy_to_clipboard_by_input(args.clip)
        exit(0)

    if args.clear:
        NManager.reset_contents()
        NManager.reload()
        NManager.show_contents()
        exit(0)

    if args.add:
        NManager.add_data(args.key, args.category)
        NManager.reload()
        NManager.show_contents()
        exit(0)
    
    if args.delete:
        NManager.delete_item_by_key(args.key)
        NManager.reload()
        NManager.show_contents()
        exit(0)

