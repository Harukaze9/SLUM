import os
import argparse
import json


class ClipBoardManager:
    main_dir          = os.path.dirname(os.path.abspath(__file__))
    data_dir = main_dir + "/data/"
    json_data = data_dir + 'content.json'
    tmpdir       = data_dir + '.tmp'

    def __init__(self):
        self.data = self.read_data()

    def read_data(self):
        if not os.path.exists(self.json_data):
            print("{} was not found".format(self.json_data))
            print("Creating {}".format(self.json_data))
            with open(self.json_data, "w") as f:
                json_data = json.dumps({})
                json.dump(json_data, f)
        with open(self.json_data) as f:
            data = json.load(f)
            return data

    def add_data(self, input_key, input_value):
        self.data[input_key] = input_value
        f = open(self.json_data, "w")
        json.dump(self.data, f)

    def test_func(self):
        print(self.tmpdir)

    def show_contents(self):
        print(self.data)

    def reset_contents(self):
        with open(self.json_data, "w") as f:
            json.dump({}, f)

    def get_iniial_data(self):
        return {}



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="nothing")
    parser.add_argument("--key", type=str)
    parser.add_argument("--value", type=str)
    parser.add_argument("--read", action="store_true")
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    CBManager = ClipBoardManager()

    if args.read:
        CBManager.show_contents()
        exit(0)

    if args.reset:
        CBManager.reset_contents()
        CBManager.show_contents()
        exit(0)

    CBManager.add_data(args.key, args.value)
    CBManager.show_contents()
    

