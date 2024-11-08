import typing as tp

import pandas as pd
import pytest

from acrux import utils


def test_columns_classification():
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })
    assert utils.get_numeric_columns(df) == ["col1"]
    assert utils.get_categorical_columns(df) == ["col2"]


@pytest.mark.parametrize("case", [
    dict(n=1, n_cols=5, expected=(1, 1)),
    dict(n=3, n_cols=2, expected=(2, 2)),
    dict(n=3, n_cols=3, expected=(3, 1)),
    dict(n=4, n_cols=3, expected=(3, 2)),
])
def test_grid_size(case: tp.Dict):
    assert case["expected"] == utils.get_grid_size(case["n"], case["n_cols"])


@pytest.mark.parametrize("case", [
    dict(text="text", n=2, expected="te..."),
    dict(text="text", n=10, expected="text"),
])
def test_text_truncator(case: tp.Dict):
    assert case["expected"] == utils.text_truncator(case["text"], case["n"])


def test_series_truncator():
    df = pd.DataFrame({
        "col": ["a", "a", "a", "b", "b", "c"]
    })
    series = utils.series_truncator(df["col"], n_top=2)
    pd.testing.assert_series_equal(series, pd.Series(["a", "a", "a", "b", "b", "others"]), check_names=False)
