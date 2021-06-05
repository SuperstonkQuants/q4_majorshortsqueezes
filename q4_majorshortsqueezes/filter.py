import json
import logging
from functools import partial
from typing import Any, Callable, Generic, List, TypeVar

from q4_majorshortsqueezes.ticker import Ticker


T = TypeVar('T')


class RingbufferWithAutomaticFIFORemoval(Generic[T]):
    """Data structure to track items in FIFO order.

    Properties of the data structure:
     - Items are traced in FIFO order
     - If the max size is reached, the next added item replaces the first item ( = FIFO deletion)
    """
    def __init__(self, size: int):
        self.size = size
        self.items = [None] * self.size
        self.read_index = 0
        self.write_index = 0

    def enqueue(self, item: T) -> T:
        """Enqueue the given item and return the previous item that was replaced.

        Runtime complexity: O(1)

        Args:
            item: The item to add.

        Returns:
            The element that was replaced by the new element. The initial values are None.
            Hence, until `self.size` elements have been enqueued, this function returns `None`.
        """
        replaced_item = self.items[self.write_index]

        self.items[self.write_index] = item
        self.write_index = (self.write_index + 1) % self.size

        return replaced_item


class SortedFIFOCache(Generic[T]):
    """A value cache which keeps the values sorted while also tracking the insertion order.

    Properties:
     - Items are traced in FIFO order
     - If the max size is reached, the next added item replaces the first item ( = FIFO deletion)
     - The first value according to the given sort function can be retrieved in constant time
    """
    def __init__(self, size: int, sort_key_func: Callable[[T], Any]):
        self.size = size
        self.sort_key_func = sort_key_func
        # We keep track of the insertion order of the values with the following buffer:
        self._value_fifo_buffer = RingbufferWithAutomaticFIFORemoval[T](size=self.size)
        # We are using a simple list to track the sorting of the added values
        # since we expect small cache sizes.
        # To make this more scalable we should use a skip-list or
        # a self-balancing binary search tree.
        self._sorted_values: List[T] = []

    def add(self, value: T) -> T:
        """Add a value to the cache and return the value that was replaced.

        Runtime complexity: O(n*log(n))

        Args:
            value: The value to cache.

        Returns:
            The element that was replaced by the new element. The initial values are None.
            Hence, until `self.size` elements have been added, this function returns `None`.
        """
        removed_value = self._value_fifo_buffer.enqueue(value)
        if removed_value is not None:
            self._sorted_values.remove(removed_value)

        self._sorted_values.append(value)
        self._sorted_values.sort(key=self.sort_key_func)

        return removed_value

    def get_first(self) -> T:
        """Return the first value according to the used sort function.

        Runtime complexity: O(1)

        Returns:
            The first value of the cached values according to the sort function.
        """
        return next(iter(self._sorted_values), None)


def multiply_price_within_x_days(ticker: Ticker,
                                 multiplier: int, days: int) -> bool:
    """Check whether the price of the ticker has ever increased by a multiplier within consecutive days.

    The function used the highs (`High` attribute) and lows (`Low` attribute) of each day.

    Args:
        ticker: Ticker data object.
        multiplier: How much multiplicative increase do we expect between the ticker's low and high
                    prices during any consecutive days.
        days: The amount of days in which the increase must be observed.
              Internally, this is translated to a moving time window which simply moves forward
              one trading day after another.

    Returns:
        True, if the ticket multiplied by `multiplier` within the given consecutive `days`;
        Otherwise, returns false.
    """
    cache_adj_close = SortedFIFOCache(size=days, sort_key_func=lambda x: x)

    for adj_close, date in zip(ticker.history['Adj Close'], ticker.history['Date']):
        # At first there are no values cached:
        if cache_adj_close.get_first():
            increase = adj_close / cache_adj_close.get_first()
            if increase >= multiplier:
                info_json = json.dumps({"Ticker": ticker.symbol, "Date": date,
                                        "Adj Close": adj_close, "Increase": increase})
                logging.info("%s - satisfied filter `%s(multiplier=%s, days=%s)`.",
                             info_json, multiply_price_within_x_days.__name__, multiplier, days)
                return True

        cache_adj_close.add(adj_close)

    logging.info("Failed filter: %s(multiplier=%s, days=%s)",
                 multiply_price_within_x_days.__name__, multiplier, days)
    return False


"""
The following filters implement the requested short squeeze filter:
`definition of a major short squeeze is when a stock doubles in price (or more) within one week`.
This function is compliant with the criterion interface of `ticker.TicketContainer.`
"""
price_multi_2_within_5_days = partial(multiply_price_within_x_days, multiplier=2, days=5)
price_multi_2_within_10_days = partial(multiply_price_within_x_days, multiplier=2, days=10)
price_multi_3_within_5_days = partial(multiply_price_within_x_days, multiplier=3, days=5)
price_multi_3_within_10_days = partial(multiply_price_within_x_days, multiplier=3, days=10)
price_multi_5_within_5_days = partial(multiply_price_within_x_days, multiplier=5, days=5)
price_multi_5_within_10_days = partial(multiply_price_within_x_days, multiplier=5, days=10)
double_price_within_a_week = price_multi_2_within_5_days  # More readable name for the README.md
