import pytest
from unittest import mock

from q4_majorshortsqueezes.api.pull_data import main


@pytest.mark.integration_test
def test_main_download_data():
    result = main(tickers={"GME", "AMC", "TSLA"},
                  start_date="2020-01-01",
                  criterion_paths=["q4_majorshortsqueezes.filter/double_price_within_a_week"])

    assert list(result) == ["AMC", "GME"]


def test_main_use_csv_data(ticker_sample_data_dir):
    # Disable downloading and ensure we load the data from csv
    with mock.patch("q4_majorshortsqueezes.api.pull_data.load_ticker_history") as m:
        m.side_effect = RuntimeError("The ticker should be loaded via a csv file.")
        result = main(tickers={"GME", "AMC", "TSLA"},
                      start_date="2020-01-01",
                      criterion_paths=["q4_majorshortsqueezes.filter/double_price_within_a_week"],
                      csv_dir_path=ticker_sample_data_dir)

    assert list(result) == ["AMC", "GME"]
