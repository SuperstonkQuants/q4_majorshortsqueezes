import importlib

from q4_majorshortsqueezes.ticker import load_ticker_history, TickerContainer, TickerHistory

from typing import Callable, Dict, List, Optional


def main(tickers: Optional[List[str]], start_date: Optional[str], criterion_paths: List[str]) \
        -> Dict[str, TickerHistory]:
    """Pull data for all given tickers and return the ones that satisfy all filter criteria.

    Args:
        tickers: A list of tickers, e.g, ["GME", "AMC", "SPY"].
        start_date: The start date in the form YYYY-MM-DD.
                    If `None` is given the max date range will be used.
        criterion_paths: Python paths to python functions which each adhere to the
                         this interface: `List[Callable[[TickerHistory], bool]`.
                         The path format for a criterion function is:
                         `full.qualified.path.to.module/func_name`

    Returns:
        A mapping of tickers and their historical data if they satisfied all filter criteria.
    """
    container = TickerContainer()
    for criterion in import_criterion_functions(criterion_paths):
        container.add_criterion(criterion)

    for ticker in tickers:
        ticker_history = load_ticker_history(ticker, start_date)
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
