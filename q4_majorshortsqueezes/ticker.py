import pandas as pd
import yfinance as yf

from typing import Callable, Dict, List

"""
A Panda's data frame with columns:
Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low
"""
TickerHistory = pd.DataFrame


class TickerContainer:
    """A container to store historical ticker data.

    The container only store tickers that meet all of the added criteria.
    """
    def __init__(self, ):
        self._criteria: List[Callable[[TickerHistory], bool]] = []
        self.__stored_tickers: Dict[str, TickerHistory] = {}

    def add_criterion(self, criterion: Callable[[TickerHistory], bool]):
        self._criteria.append(criterion)

    def store_ticker(self, ticker: str, ticker_history: TickerHistory):
        if all(criterion(ticker_history) for criterion in self._criteria):
            self.__stored_tickers[ticker] = ticker_history

    def get_stored_tickers(self) -> Dict[str, TickerHistory]:
        return self.__stored_tickers


def load_ticker_history(ticker: str, start_date: str) -> TickerHistory:
    """Loads a ticker data from Yahoo Finance, adds a data index column data_id and Open-Close High/Low columns.

    This code was taken from:
    https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/gamestonk_terminal/technical_analysis/trendline_api.py#L9

    Args:
        ticker: The stock ticker.
        start_date: Start date to load stock ticker data formatted YYYY-MM-DD.

    Returns:
        A Panda's data frame with columns Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low.
    """
    # print(f"Start date: {start_date}")
    df_data = yf.download(ticker, start=start_date, progress=False)

    df_data["date_id"] = (df_data.index.date - df_data.index.date.min()).astype(
        "timedelta64[D]"
    )
    df_data["date_id"] = df_data["date_id"].dt.days + 1

    df_data["OC_High"] = df_data[["Open", "Close"]].max(axis=1)
    df_data["OC_Low"] = df_data[["Open", "Close"]].min(axis=1)

    return df_data
