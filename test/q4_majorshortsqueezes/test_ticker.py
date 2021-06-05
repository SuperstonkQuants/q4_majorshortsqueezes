import os
import pytest

from unittest.mock import MagicMock

from q4_majorshortsqueezes.ticker import (
    load_ticker_history,
    load_ticker_history_from_csv,
    retrieve_tickers_with_get_all_tickers_package,
    TickerContainer,
    TickerHistory,
)


class TestTickerContainer:
    def test_add_with_single_criterion(self):
        container = TickerContainer()
        ticker_history1 = MagicMock(spec=TickerHistory)
        ticker_history1.__len__.side_effect = lambda: 10
        ticker_history2 = MagicMock(spec=TickerHistory)
        ticker_history2.__len__.side_effect = lambda: 0

        container.add_criterion(lambda th: len(th) > 0)
        container.store_ticker("A", ticker_history1)
        container.store_ticker("B", ticker_history2)

        assert container.get_stored_tickers() == {"A": ticker_history1}

    def test_add_with_multiple_criteria(self):
        container = TickerContainer()
        ticker_history1 = MagicMock(spec=TickerHistory)
        ticker_history1.__len__.side_effect = lambda: 10
        ticker_history2 = MagicMock(spec=TickerHistory)
        ticker_history2.__len__.side_effect = lambda: 5
        ticker_history3 = MagicMock(spec=TickerHistory)
        ticker_history3.__len__.side_effect = lambda: 0

        container.add_criterion(lambda th: len(th) > 0)
        container.add_criterion(lambda th: len(th) < 10)
        container.store_ticker("A", ticker_history1)
        container.store_ticker("B", ticker_history2)
        container.store_ticker("C", ticker_history3)

        assert container.get_stored_tickers() == {"B": ticker_history2}


@pytest.mark.integration_test
def test_load_ticker_history():
    ticker_history = load_ticker_history("GME", "2021-05-01")

    # Let's check that there is data
    assert len(ticker_history) > 10

    column_names = list(ticker_history)
    assert column_names[0] == "Open"
    assert column_names[1] == "High"
    assert column_names[2] == "Low"
    assert column_names[3] == "Close"
    assert column_names[4] == "Adj Close"
    assert column_names[5] == "Volume"
    assert column_names[6] == "date_id"
    assert column_names[7] == "OC_High"
    assert column_names[8] == "OC_Low"


def test_load_ticker_history_from_csv(ticker_sample_data_dir):
    gme_csv = os.path.join(ticker_sample_data_dir, "GME.csv")
    ticker_history = load_ticker_history_from_csv(gme_csv)

    # Let's check that there is data
    assert len(ticker_history) > 10

    column_names = list(ticker_history)
    assert column_names[0] == "Date"  # An own column instead of having tuples in each data series
    assert column_names[1] == "Open"
    assert column_names[2] == "High"
    assert column_names[3] == "Low"
    assert column_names[4] == "Close"
    assert column_names[5] == "Adj Close"
    assert column_names[6] == "Volume"
    assert column_names[7] == "date_id"
    assert column_names[8] == "OC_High"
    assert column_names[9] == "OC_Low"


@pytest.mark.integration_test
@pytest.mark.xfail(strict=True)
def test_load_ticker_history_equality(ticker_sample_data_dir):
    ticker_history_downloaded = load_ticker_history("GME", "2020-01-01")
    gme_csv = os.path.join(ticker_sample_data_dir, "GME.csv")
    ticker_history_csv = load_ticker_history_from_csv(gme_csv)

    assert ticker_history_downloaded.equals(ticker_history_csv)


@pytest.mark.integration_test
def test_retrieve_tickers_with_get_all_tickers_package():
    only_nyse = retrieve_tickers_with_get_all_tickers_package(nyse=True)
    assert len(only_nyse) > 1000  # There should be more than 100 tickers on the nyse

    nyse_marketcap = retrieve_tickers_with_get_all_tickers_package(nyse=True, min_market_cap=100000)
    assert nyse_marketcap.issubset(only_nyse)
