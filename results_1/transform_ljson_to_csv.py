import csv
import json
import sys

lines = sys.stdin.readlines()
tickers = [json.loads(line) for line in lines]
if tickers:
    keys = tickers[0].keys()
else:
    keys = ["Ticker", "Date", "Adj Close", "Increase"]
dict_writer = csv.DictWriter(sys.stdout, keys)
dict_writer.writeheader()

if tickers:
    dict_writer.writerows(tickers)
