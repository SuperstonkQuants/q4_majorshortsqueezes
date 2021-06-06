import pytest
from unittest import mock

from q4_majorshortsqueezes.api.pull_data import main
from q4_majorshortsqueezes.ticker import FileBackedTicketContainer


@pytest.mark.integration_test
def test_main_download_data():
    result = main(tickers={"GME", "AMC", "TSLA"},
                  start_date="2020-01-01",
                  criterion_paths=["q4_majorshortsqueezes.filter/price_multi_2_within_5_days"])

    assert result.get_tickers() == ["AMC", "GME"]


def test_main_use_csv_data(ticker_sample_data_dir):
    # Disable downloading and ensure we load the data from csv
    with mock.patch("q4_majorshortsqueezes.api.pull_data.load_ticker_history") as m:
        m.side_effect = RuntimeError("The ticker should be loaded via a csv file.")
        result = main(tickers={"GME", "AMC", "TSLA"},
                      start_date="2020-01-01",
                      criterion_paths=["q4_majorshortsqueezes.filter/price_multi_2_within_5_days"],
                      csv_dir_path=ticker_sample_data_dir)

    assert result.get_tickers() == ["AMC", "GME"]


def test_main_use_and_store_csv_data(ticker_sample_data_dir, tmpdir):
    # Disable downloading and ensure we load the data from csv
    with mock.patch("q4_majorshortsqueezes.api.pull_data.load_ticker_history") as m:
        m.side_effect = RuntimeError("The ticker should be loaded via a csv file.")
        result = main(tickers={"GME", "AMC", "TSLA"},
                      start_date="2020-01-01",
                      criterion_paths=[],
                      csv_dir_path=ticker_sample_data_dir,
                      csv_output_dir_path=tmpdir)

    assert isinstance(result, FileBackedTicketContainer)
    assert result.ticker_data_dir_path == tmpdir
    assert result.get_tickers() == ["AMC", "GME", "TSLA"]
