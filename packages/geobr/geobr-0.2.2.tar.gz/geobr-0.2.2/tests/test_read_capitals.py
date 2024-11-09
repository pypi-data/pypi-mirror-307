import os
import pytest
import geopandas as gpd
import pandas as pd
from geobr import read_capitals


def skip_if(condition):
    return pytest.mark.skipif(condition, reason="Skipping test due to condition")


@skip_if(os.getenv("TEST_ONE") != "")
@pytest.mark.skip(reason="Skipping tests on CRAN")
def test_read_capitals_sf():
    assert isinstance(read_capitals(), gpd.GeoDataFrame)


@skip_if(os.getenv("TEST_ONE") != "")
@pytest.mark.skip(reason="Skipping tests on CRAN")
def test_read_capitals_df():
    assert isinstance(read_capitals(as_sf=False), pd.DataFrame)


def test_read_capitals_errors():
    with pytest.raises(Exception):
        read_capitals(as_sf=9999999)
    with pytest.raises(Exception):
        read_capitals(showProgress=9999999)