import os
import pytest


@pytest.fixture()
def ticker_sample_data_dir():
    module_path = os.path.abspath(__file__)
    root_dir_path = os.path.dirname(os.path.dirname(module_path))
    yield os.path.join(root_dir_path, "ticker_sample_data")
