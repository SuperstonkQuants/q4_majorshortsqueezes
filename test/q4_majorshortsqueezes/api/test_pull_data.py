import pytest

from q4_majorshortsqueezes.api.pull_data import main


@pytest.mark.integration_test
def test_main():
    result = main(["GME", "AMC", "TSLA"], "2020-01-01",
                  ["q4_majorshortsqueezes.filter/double_price_within_a_week"])

    assert list(result) == ["GME", "AMC"]
