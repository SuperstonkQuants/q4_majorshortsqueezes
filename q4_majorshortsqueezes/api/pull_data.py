import importlib
import logging

from q4_majorshortsqueezes.ticker import (
    FileBackedTicketContainer,
    InMemoryTickerContainer,
    load_ticker_history,
    load_ticker_history_from_csv,
    TickerContainer,
    TickerHistory,
)

from typing import Callable, List, Optional, Set


def main(tickers: Set[str], start_date: Optional[str], criterion_paths: List[str],
         csv_dir_path: Optional[str] = None, csv_output_dir_path: Optional[str] = None) \
        -> TickerContainer:
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
        csv_output_dir_path: A directory path which ticker data is stored to.
                             This can be the same dir as `csv_dir_path`. Keep in mind
                             that filtering will not work in this case, since this function
                             does not delete the input files from `csv_dir_path`.
                             If this parameter is set, the function returns a
                             FileBackedTicketContainer, instead of a InMemoryTickerContainer.

    Returns:
        A mapping of tickers and their historical data if they satisfied all filter criteria.
    """
    container = (FileBackedTicketContainer(csv_output_dir_path) if csv_output_dir_path
                 else InMemoryTickerContainer())
    for criterion in import_criterion_functions(criterion_paths):
        container.add_criterion(criterion)

    read_container = FileBackedTicketContainer(csv_dir_path) if csv_dir_path else None

    for i, ticker in enumerate(sorted(tickers), start=1):
        try:
            ticker_history = None

            if read_container:
                logging.info("%s. Looking up `%s` from %s", i, ticker, csv_dir_path)
                ticker_history = read_container[ticker]
                if ticker_history is None:
                    logging.info("%s. Failed to look up `%s` from %s", i, ticker, csv_dir_path)

            if ticker_history is None:
                logging.info("%s. Downloading: `%s`", i, ticker)
                ticker_history = load_ticker_history(ticker, start_date)

            logging.info("%s. Got ticker data. Start filtering of: `%s`", i,  ticker)
            container.store_ticker(ticker, ticker_history)
        except Exception:
            # Swallow all errors and let users check the logs to see what has failed
            logging.exception("%s. Ticker `%s` failed.", i, ticker)

    return container


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
