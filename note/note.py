import os
import argparse
import json
import datetime
import math
import pandas as pd
import pyperclip
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")
import data_manager_base


class NoteManager(data_manager_base.DataManagerBase):
    # Base
    main_dir          = os.path.dirname(os.path.abspath(__file__))
    data_dir = main_dir + "/data/"
    json_data = data_dir + 'content.json'
    use_category = True
    use_tag = True
    columns_show=["category", "tags", "timestamp"]
    # Note
    note_dir          = main_dir + "/.notes/"


    def __init__(self):
        super().__init__()

    def add_note(self, key, category, tags=[]):
        note_path = os.path.join(self.note_dir, key + ".md")
        if os.path.exists(note_path):
            print("Error: {} already exists.".format(note_path))
            exit(1)
        data_dict = {}
        data_dict["note_path"] = note_path
        data_dict["category"] = category
        data_dict["tags"] = tags
        self._add_data(key, data_dict)
        content = "# {}".format(key)
        self._create_note_file(note_path, content)

    def _create_note_file(self, file_path, content):
        with open(file_path,'w') as f:
            f.write(content)
        print("{} is created!".format(file_path))

    # def show_contents(self, short=False):
    #     columns = ["category", "timestamp", "note_path"]
    #     self._show_contents(columns)
        
    def _write_initial_data(self):
        example_note_path = os.path.join(self.note_dir, "example.md")
        dic = {"example":
                {"note_path": example_note_path,
                "timestamp": 0,
                "category": None,
                "tags": [],
                }}
        with open(self.json_data, "w") as f:
            json.dump(dic, f)
        
    def delete_item_by_key(self, key):
        note_path = self.data[key]["note_path"]
        super().delete_item_by_key(key, note_path)
    
    def reset_contents(self):
        for key in self.data.keys():
            note_path = self.data[key]["note_path"]
            if os.path.exists(note_path):
                os.remove(note_path)
        super().reset_contents()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="nothing....")
    # parser.add_argument("--clip", type=str)
    parser.add_argument("-k", "--key", type=str)
    parser.add_argument("-c", "--category", type=str)
    parser.add_argument("--read", action="store_true")
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--add", action="store_true")
    parser.add_argument("--edit", action="store_true")
    parser.add_argument("-t", "--tags", nargs="*", default = [], type=str)
    args = parser.parse_args()

    NManager = NoteManager()

    # if args.clip != None:
    #     NManager.copy_to_clipboard_by_input(args.clip)
    #     exit(0)

    if args.edit:
        if args.tags:
            NManager.set_tags(args.key, args.tags)
        if args.category:
            NManager.set_category(args.key, args.category)
        exit(0)
    
    if args.read:
        NManager.show_contents()
        exit(0)

    if args.clear:
        NManager.reset_contents()
        NManager.reload()
        NManager.show_contents()
        exit(0)

    if args.add:
        NManager.add_note(args.key, args.category)
        NManager.reload()
        NManager.show_contents()
        exit(0)
    
    if args.delete:
        NManager.delete_item_by_key(args.key)
        NManager.reload()
        NManager.show_contents()
        exit(0)

