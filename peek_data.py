import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("target", type=str)
args = parser.parse_args()

main_dir          = os.path.dirname(os.path.abspath(__file__))
if args.target == "clipboard":
    target_dir = os.path.join(main_dir, "clipboard")
elif args.target == "note":
    target_dir = os.path.join(main_dir, "note")
else:
    print("Error: unknown target")
    exit(1)
data_dir = target_dir + "/data/"
json_data = data_dir + 'content.json'
with open(json_data) as f:
    data = json.load(f)
for k in data.keys():
    print(k, end=" ")
print("")


