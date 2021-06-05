import abc
import glob
import os
import pandas as pd
import yfinance as yf
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set

from q4_majorshortsqueezes import get_tickers_fixed as gt


"""
A Panda's data frame with columns:
Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low
"""
TickerHistory = pd.DataFrame


class TickerContainer(abc.ABC):
    """Base class for containers that store historical ticker data."""
    def __init__(self):
        self._criteria: List[Callable[[TickerHistory], bool]] = []

    def add_criterion(self, criterion: Callable[[TickerHistory], bool]):
        self._criteria.append(criterion)

    def store_ticker(self, ticker: str, ticker_history: TickerHistory):
        if all(criterion(ticker_history) for criterion in self._criteria):
            self._add_ticker_data(ticker, ticker_history)

    @abc.abstractmethod
    def _add_ticker_data(self, ticker: str, ticker_history: TickerHistory):
        pass

    @abc.abstractmethod
    def __getitem__(self, ticker: str) -> Optional[TickerHistory]:
        """Return the ticker price history for a ticker.

        Args:
            ticker: A ticker symbol.

        Returns:
            The ticker's price history. If the ticker is not stored in the container, return `None`.
        """
        pass

    @abc.abstractmethod
    def get_data(self) -> Dict[str, TickerHistory]:
        pass

    @abc.abstractmethod
    def get_tickers(self) -> List[str]:
        pass


class InMemoryTickerContainer(TickerContainer):
    """A container to store historical ticker data.

    The container only store tickers that meet all of the added criteria.
    """
    def __init__(self):
        super().__init__()
        self.__stored_tickers: Dict[str, TickerHistory] = {}

    def _add_ticker_data(self, ticker: str, ticker_history: TickerHistory):
        self.__stored_tickers[ticker] = ticker_history

    def __getitem__(self, ticker) -> Optional[TickerHistory]:
        return self.__stored_tickers.get(ticker, None)

    def get_data(self) -> Dict[str, TickerHistory]:
        return self.__stored_tickers

    def get_tickers(self) -> List[str]:
        return sorted(list(self.__stored_tickers.keys()))


class FileBackedTicketContainer(TickerContainer):
    """A ticket container that does not keep the data in memory but on the file system.

    If ticker data is already present, it will also have access to them.
    """
    def __init__(self, ticker_data_dir_path: str):
        super().__init__()
        self.ticker_data_dir_path = ticker_data_dir_path

    def _add_ticker_data(self, ticker: str, ticker_history: TickerHistory):
        with open(self._ticker_data_path(ticker), mode="w") as fd:
            ticker_history.to_csv(fd)

    def _ticker_data_path(self, ticker):
        return os.path.join(self.ticker_data_dir_path, f"{ticker}.csv")

    def __getitem__(self, ticker) -> Optional[TickerHistory]:
        if ticker not in self.get_tickers():
            return None
        else:
            return load_ticker_history_from_csv(self._ticker_data_path(ticker))

    def get_data(self) -> Dict[str, TickerHistory]:
        tickers = self.get_tickers()
        data = {}
        for ticker in tickers:
            data[ticker] = self[ticker]

        return data

    def get_tickers(self) -> List[str]:
        file_pattern = os.path.join(self.ticker_data_dir_path, "*.csv")
        return sorted(Path(path).stem for path in glob.glob(file_pattern))


def load_ticker_history(ticker: str, start_date: Optional[str]) -> TickerHistory:
    """Loads a ticker data from Yahoo Finance, adds a data index column data_id and Open-Close High/Low columns.

    Args:
        ticker: The stock ticker.
        start_date: Start date to load stock ticker data formatted YYYY-MM-DD.
                    If `None` is given the max date range will be used.

    Returns:
        A Panda's data frame with columns Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low.
    """
    df_data = yf.download(ticker, start=start_date, progress=False)

    df_data["date_id"] = (df_data.index.date - df_data.index.date.min()).astype(
        "timedelta64[D]"
    )
    df_data["date_id"] = df_data["date_id"].dt.days + 1

    df_data["OC_High"] = df_data[["Open", "Close"]].max(axis=1)
    df_data["OC_Low"] = df_data[["Open", "Close"]].min(axis=1)

    return df_data


def load_ticker_history_from_csv(file_path: str) -> TickerHistory:
    """Load a tickers historical price data from the given csv.

    Attention:
    The loaded dataframes are not fully identical with the ones downloaded.
    When loaded from csv a new column `date` exists which is stored in the data series as
    tuples when loading the data from `yfinance`.

    Args:
        file_path: The path to the comma-separated csv file that contains the historical price data.

    Returns:
        A Panda's data frame with columns Date, Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low.
    """
    # TODO: Make the format identical with `yfinance` loading
    return pd.read_csv(file_path)


def retrieve_tickers_with_get_all_tickers_package(nyse: bool = False,
                                                  nasdaq: bool = False,
                                                  amex: bool = False,
                                                  min_market_cap: int = 0) -> Set[str]:
    tickers = set(gt.get_tickers(NYSE=nyse, NASDAQ=nasdaq, AMEX=amex))
    if min_market_cap:
        tickers_filtered = set(gt.get_tickers_filtered(mktcap_min=min_market_cap))
        tickers = tickers.intersection(tickers_filtered)
    return tickers
