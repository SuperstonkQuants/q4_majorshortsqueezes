import csv
import json
import sys

lines = sys.stdin.readlines()
tickers = [json.loads(line) for line in lines]
keys = tickers[0].keys()
dict_writer = csv.DictWriter(sys.stdout, keys)
dict_writer.writeheader()
dict_writer.writerows(tickers)
