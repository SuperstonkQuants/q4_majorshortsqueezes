import abc
import glob
import io
import os
import pandas as pd
import yfinance as yf
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Union

from q4_majorshortsqueezes import get_tickers_fixed as gt


"""
A Panda's data frame with columns:
Date, Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low
"""
TickerHistory = pd.DataFrame


@dataclass
class Ticker:
    symbol: str
    history: TickerHistory


class TickerContainer(abc.ABC):
    """Base class for containers that store historical ticker data."""
    def __init__(self):
        self._criteria: List[Callable[[Ticker], bool]] = []

    def add_criterion(self, criterion: Callable[[Ticker], bool]):
        self._criteria.append(criterion)

    def store_ticker(self, symbol: str, ticker_history: TickerHistory):
        ticker = Ticker(symbol, ticker_history)
        if all(criterion(ticker) for criterion in self._criteria):
            self._add_ticker_data(symbol, ticker_history)

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
            store_ticker_to_csv(ticker_history, fd)

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
        A Panda's data frame representing the price history of a ticker.
    """
    df_data = yf.download(ticker, start=start_date, progress=False)

    df_data["date_id"] = (df_data.index.date - df_data.index.date.min()).astype(
        "timedelta64[D]"
    )
    df_data["date_id"] = df_data["date_id"].dt.days + 1

    df_data["OC_High"] = df_data[["Open", "Close"]].max(axis=1)
    df_data["OC_Low"] = df_data[["Open", "Close"]].min(axis=1)

    # We need to be consistent with the Panda frames we load when from csv files.
    # To ensure that we are fully compatible with the frame layouts and to avoid
    # float precision errors we use this workaround:
    temp = io.StringIO()
    store_ticker_to_csv(df_data, temp)
    temp.seek(0)

    return load_ticker_history_from_csv(temp)


def load_ticker_history_from_csv(file_path: Union[str, io.StringIO]) -> TickerHistory:
    """Load a tickers historical price data from the given csv.

    Args:
        file_path: The path to the comma-separated csv file that contains the historical price data.

    Returns:
        A Panda's data frame representing the price history of a ticker.
    """
    return pd.read_csv(file_path, index_col="Date")


def store_ticker_to_csv(ticker_history: TickerHistory, file_path: Union[str, io.StringIO]):
    """Store a ticker's historical price information in a csv file.

    We should always use this function to store ticker history data since it
    ensures that we use a unified frame layout and float precision.
    Otherwise, ticker histories might originate from the data, but still end uo
    unequal.
    This function serializes the floats with 6 digits after the decimal point.

    Args:
        ticker_history: The price history of a ticker.
        file_path: The csv file path to write the data to.

    Returns:

    """
    ticker_history.to_csv(file_path, index=True, float_format="%.6f")


def retrieve_tickers_with_get_all_tickers_package(nyse: bool = False,
                                                  nasdaq: bool = False,
                                                  amex: bool = False,
                                                  min_market_cap: int = 0) -> Set[str]:
    tickers = set(gt.get_tickers(NYSE=nyse, NASDAQ=nasdaq, AMEX=amex))
    if min_market_cap:
        tickers_filtered = set(gt.get_tickers_filtered(mktcap_min=min_market_cap))
        tickers = tickers.intersection(tickers_filtered)
    return tickers
