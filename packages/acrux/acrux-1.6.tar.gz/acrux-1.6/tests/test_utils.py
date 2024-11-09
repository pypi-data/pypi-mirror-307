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


@pytest.mark.parametrize("case", [
    dict(col1="col1", col2="col2", target=None, expect=False),
    dict(col1="col1", col2="col2", target="target1", expect=False),
    dict(col1="col1", col2="col2", target="target2", expect=True),
])
def test_should_skip_pair(case: tp.Dict):
    df = pd.DataFrame({
        "col1": [1, None, 2],
        "col2": [1, 3, None],
        "col3": [None, 1, None],
        "target1": [0, None, 1],
        "target2": [None, 1, None],
    })
    actual = utils.should_skip_pair(df, case["col1"], case["col2"], case["target"])
    assert actual == case["expect"]
