import os
import argparse
import json

# DATA_JSON_FILE = "hogehoge.json"


class ClipBoardManager:
    main_dir          = os.path.dirname(os.path.abspath(__file__))
    data_dir = main_dir + "/data/"
    json_data = data_dir + 'content.json'
    tmpdir       = data_dir + '.tmp'

    def __init__(self):
        self.data = self.read_data()
        print("data is")
        print(self.data)

    def read_data(self):
        if not os.path.exists(self.json_data):
            print("create {}".format(self.json_data))
            with open(self.json_data, "w") as f:
                json.dump({}, f)

        with open(self.json_data) as f:
            return json.load(f)

    def add_data(self, input):
        self.data[input] = 0
        f = open(self.json_data, "w")
        json.dump(self.data, f)

    def test_func(self):
        print(self.tmpdir)





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="nothing")
    parser.add_argument("input", type=str)
    args = parser.parse_args()

    # parser.add_argument("", type=str)

    print("hwllo wooo")
    var_hoge = ClipBoardManager()
    var_hoge.add_data(args.input)

    var_hoge.test_func()
    

