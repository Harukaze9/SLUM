#!/usr/bin/env python
# import rlcompleter
# import readline
# readline.parse_and_bind ('tab: complete')
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
parser.add_argument("--cream", action="store_true")

args = parser.parse_args()
print(args.cream)

print("hello world")