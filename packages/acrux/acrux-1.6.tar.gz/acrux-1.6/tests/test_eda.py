import numpy as np
import pandas as pd
import pytest

from acrux.eda import ExploratoryDataAnalysis

TEST_DATA = [
    pd.DataFrame({
        "col1": [1, 2, 3],
    }),
    pd.DataFrame({
        "col1": [1, 2, 3, np.nan, None],
    }),
    pd.DataFrame({
        "col1": [1, 2, 3, ],
        "col2": [0, -2, -3],
        "col3": [1, 2, -1],
    }),
    pd.DataFrame({
        "col1": ["A", "B", "C"],
    }),
    pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["A", "B", "C"],
    }),
    pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["A", "B", "C"],
        "col3": ["A", None, np.nan],
    }),
]


@pytest.mark.parametrize("df", TEST_DATA)
def test_pair_generator(df: pd.DataFrame, request):
    # Arrange
    eda = ExploratoryDataAnalysis(df=df)

    # Act & Assert
    eda.cat_futures_eda(one_graph_size=3)
    eda.numeric_futures_eda(log_scale=False, one_graph_size=3)
    eda.heat_map(one_graph_size=3, sample_count=len(df))
