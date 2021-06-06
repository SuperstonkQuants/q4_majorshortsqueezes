import os
import pytest

from unittest.mock import MagicMock

from q4_majorshortsqueezes.ticker import (
    FileBackedTicketContainer,
    load_ticker_history,
    load_ticker_history_from_csv,
    InMemoryTickerContainer,
    retrieve_tickers_with_get_all_tickers_package,
    store_ticker_to_csv,
    Ticker,
    TickerHistory,
)


class TestInMemoryTickerContainer:
    def test_add_with_single_criterion(self):
        container = InMemoryTickerContainer()
        ticker1 = Ticker("GME", MagicMock(spec=TickerHistory))
        ticker2 = Ticker("AMC", MagicMock(spec=TickerHistory))

        container.add_criterion(lambda t: "GM" in t.symbol)
        container.store_ticker(ticker1.symbol, ticker1.history)
        container.store_ticker(ticker2.symbol, ticker2.history)

        assert container.get_data() == {ticker1.symbol: ticker1.history}

    def test_add_with_multiple_criteria(self):
        container = InMemoryTickerContainer()
        ticker1 = Ticker("GME", MagicMock(spec=TickerHistory))
        ticker2 = Ticker("AMC", MagicMock(spec=TickerHistory))
        ticker3 = Ticker("TSLA", MagicMock(spec=TickerHistory))

        container.add_criterion(lambda t: "M" in t.symbol)
        container.add_criterion(lambda t: "G" in t.symbol)
        container.store_ticker(ticker1.symbol, ticker1.history)
        container.store_ticker(ticker2.symbol, ticker2.history)
        container.store_ticker(ticker3.symbol, ticker3.history)

        assert container.get_data() == {ticker1.symbol: ticker1.history}


class TestFileBackedTicketContainer:
    def test_attach_to_existing_dir(self, ticker_sample_data_dir):
        container = FileBackedTicketContainer(ticker_sample_data_dir)

        assert container.get_tickers() == ["AMC", "GME", "TSLA"]

    def test_add_without_any_filter_criteria(self, ticker_sample_data_dir, tmpdir):
        sample_data_container = FileBackedTicketContainer(ticker_sample_data_dir)

        new_container = FileBackedTicketContainer(tmpdir)
        for ticker, ticker_history in sample_data_container.get_data().items():
            new_container.store_ticker(ticker, ticker_history)

        tickers = new_container.get_tickers()
        assert len(tickers) > 0
        assert tickers == sample_data_container.get_tickers()
        # TODO: For some reason loading and storing the panda data as csv yields different results.
        #  This may indicate a bug.
        ticker = tickers[0]
        assert len(new_container.get_data()[ticker]) == len(sample_data_container.get_data()[ticker])


def assert_ticker_history_data_frame_layout(ticker_history: TickerHistory):
    assert ticker_history.index.name == "Date"

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


@pytest.mark.integration_test
def test_load_ticker_history():
    ticker_history = load_ticker_history("GME", "2021-02-01")

    # Let's check that there is data
    assert len(ticker_history) > 10

    assert_ticker_history_data_frame_layout(ticker_history)


def test_load_ticker_history_from_csv(ticker_sample_data_dir):
    gme_csv = os.path.join(ticker_sample_data_dir, "GME.csv")
    ticker_history = load_ticker_history_from_csv(gme_csv)

    # Let's check that there is data
    assert len(ticker_history) > 10

    assert_ticker_history_data_frame_layout(ticker_history)


@pytest.mark.integration_test
def test_load_ticker_history_equality(tmpdir):
    gme_csv = os.path.join(tmpdir, "GNE.csv")
    ticker_history_downloaded = load_ticker_history("GME", "2020-01-01")
    store_ticker_to_csv(ticker_history_downloaded, gme_csv)
    ticker_history_csv = load_ticker_history_from_csv(gme_csv)

    assert ticker_history_downloaded.equals(ticker_history_csv)


@pytest.mark.integration_test
def test_retrieve_tickers_with_get_all_tickers_package():
    only_nyse = retrieve_tickers_with_get_all_tickers_package(nyse=True)
    assert len(only_nyse) > 1000  # There should be more than 100 tickers on the nyse

    nyse_marketcap = retrieve_tickers_with_get_all_tickers_package(nyse=True, min_market_cap=100000)
    assert nyse_marketcap.issubset(only_nyse)
