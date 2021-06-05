import importlib
import logging
import os

from q4_majorshortsqueezes.ticker import (
    load_ticker_history,
    load_ticker_history_from_csv,
    TickerContainer,
    TickerHistory,
)

from typing import Callable, Dict, List, Optional, Set


def main(tickers: Set[str], start_date: Optional[str], criterion_paths: List[str],
         csv_dir_path: Optional[str] = None) -> Dict[str, TickerHistory]:
    """Pull data for all given tickers and return the ones that satisfy all filter criteria.

    Args:
        tickers: A set of tickers, e.g, {"GME", "AMC", "SPY"}.
                 The tickers will always be processed in alphabetical order.
        start_date: The start date in the form YYYY-MM-DD.
                    This has only effect on newly downloaded price data.
                    If `None` is given the max date range will be used.
        criterion_paths: Python paths to python functions which each adhere to the
                         this interface: `List[Callable[[TickerHistory], bool]`.
                         The path format for a criterion function is:
                         `full.qualified.path.to.module/func_name`
        csv_dir_path: A directory path which is looked through for ticker data.
                      When processing a ticker (e.g. GME) the function looks for
                      a file named `GME.csv` to load the data from there.
                      If no file is found or this parameter is `None`, the ticker
                      data is downloaded.

    Returns:
        A mapping of tickers and their historical data if they satisfied all filter criteria.
    """
    container = TickerContainer()
    for criterion in import_criterion_functions(criterion_paths):
        container.add_criterion(criterion)

    for ticker in sorted(tickers):
        ticker_history = None

        if csv_dir_path:
            ticker_file_path = os.path.join(csv_dir_path, f"{ticker}.csv")
            if os.path.isfile(ticker_file_path):
                logging.info("Reading `%s` from %s", ticker, ticker_file_path)
                ticker_history = load_ticker_history_from_csv(ticker_file_path)

        if ticker_history is None:
            logging.info("Downloading: `%s`", ticker)
            ticker_history = load_ticker_history(ticker, start_date)

        logging.info("Got ticker data. Start filtering of: `%s`", ticker)
        container.store_ticker(ticker, ticker_history)

    return container.get_stored_tickers()


def import_criterion_functions(criterion_paths: List[str]) -> List[Callable[[TickerHistory], bool]]:
    """Import and return a criterion functions for each given path.

    Args:
        criterion_paths: Python paths to python functions which each adhere to the
                         this interface: `List[Callable[[TickerHistory], bool]`.
                         The path format for a criterion function is:
                         `full.qualified.path.to.module/func_name`

    Returns:
        The imported criterion functions.
    """
    functions = []
    for criterion_path in criterion_paths:
        module_path, func_name = criterion_path.split("/")
        module = importlib.import_module(module_path)
        functions.append(getattr(module, func_name))

    return functions
