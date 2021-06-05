# Summary
This directory contains the results of the short squeeze analysis: How often do major short squeezes happen?

The following process describes how the results were created.
You need to run them in the root dir of this repository to reproduce the result.

## Analysis
TODO

### Reproducing the results
#### 1. Downloading of data (no filtering)
Source of truth for ticker symbols:
https://github.com/shilewenuw/get_all_tickers

Source of truth for price data:
https://github.com/ranaroussi/yfinance

NYSE:
```
# Load market cap min 1000m
mkdir ./ticker_data__nyse_min_1000m
poetry run python bin/pull_data.py -v --nyse --min-market-cap=1000 --output-path ./ticker_data__nyse_min_1000m 2>&1 | tee nyse_min_1000m.log


# Load market cap min 100m (use already cached 1000m data)
mkdir ./ticker_data__nyse_min_100m
poetry run python bin/pull_data.py -v --nyse --min-market-cap=100 --ticker-source-dir ./ticker_data__nyse_min_1000m --output-path ./ticker_data__nyse_min_100m  2>&1 | tee nyse_min_100m.log

# Load market cap min 10m (use already cached 100m data)
mkdir ./ticker_data__nyse_min_10m
poetry run python bin/pull_data.py -v --nyse --min-market-cap=100 --ticker-source-dir ./ticker_data__nyse_min_100m --output-path ./ticker_data__nyse_min_10m  2>&1 | tee nyse_min_10m.log
```

NASDAQ:
```
# Load market cap min 1000m
mkdir ./ticker_data__nasdaq_min_1000m
poetry run python bin/pull_data.py -v --nasdaq --min-market-cap=1000 --output-path ./ticker_data__nasdaq_min_1000m 2>&1 | tee nasdaq_min_1000m.log

# Load market cap min 100m (use already cached 1000m data)
mkdir ./ticker_data__nasdaq_min_100m
poetry run python bin/pull_data.py -v --nasdaq --min-market-cap=100 --ticker-source-dir ./ticker_data__nasdaq_min_1000m --output-path ./ticker_data__nasdaq_min_100m  2>&1 | tee nasdaq_min_100m.log

# Load market cap min 10m (use already cached 100m data)
mkdir ./ticker_data__nasdaq_min_10m
poetry run python bin/pull_data.py -v --nasdaq --min-market-cap=100 --ticker-source-dir ./ticker_data__nasdaq_min_100m --output-path ./ticker_data__nasdaq_min_10m  2>&1 | tee nasdaq_min_10m.log
```

AMEX:
```
# Load market cap min 1000m
mkdir ./ticker_data__amex_min_1000m
poetry run python bin/pull_data.py -v --amex --min-market-cap=1000 --output-path ./ticker_data__amex_min_1000m 2>&1 | tee amex_min_1000m.log

# Load market cap min 100m (use already cached 1000m data)
mkdir ./ticker_data__amex_min_100m
poetry run python bin/pull_data.py -v --amex --min-market-cap=100 --ticker-source-dir ./ticker_data__amex_min_1000m --output-path ./ticker_data__amex_min_100m  2>&1 | tee amex_min_100m.log

# Load market cap min 10m (use already cached 100m data)
mkdir ./ticker_data__amex_min_10m
poetry run python bin/pull_data.py -v --amex --min-market-cap=100 --ticker-source-dir ./ticker_data__amex_min_100m --output-path ./ticker_data__amex_min_10m  2>&1 | tee amex_min_10m.log
```

#### 2. Filtering of data for squeezes
Source of truth for ticker symbols:
https://github.com/shilewenuw/get_all_tickers

Source of truth for price data:
The downloaded data from step 1.

This step produces for the following dimensions:
- Exchange: NYSE, NASDAQ, AMEX
- Min market cap (today): 1000m, 100m, 10m (10m not yet supported since data was too big; need one more day)
- Multiplier: 2 (= double price), 3
- Consecutive days: 5, 10

For each combination a list of tickers (=one file per list) with the following information for each ticker:
- Ticker
- Adjusted close price (that triggered the ticker to satisfy the requirement)
- Date (of the close price when the multiplier threshold was exceeded)
- Percentage increase (between lowest adjusted close price of the consecutive days and the adjusted close price; This value reflects only the increase the first day the threshold was exceeded, not the maximum ever for the ticker)

```
results_1/create_filtered_tickers.sh
```
