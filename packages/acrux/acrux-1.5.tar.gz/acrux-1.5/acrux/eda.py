import typing as tp

import pandas as pd

from .categorical import categorical_eda
from .heatmap import categorical_heatmap
from .heatmap import correlation_matrix
from .numeric import numeric_eda
from .pair_numeric import plot_pair_numeric_eda
from .utils import get_categorical_columns
from .utils import get_numeric_columns


class ExploratoryDataAnalysis:
    def __init__(self,
                 df: pd.DataFrame,
                 target: tp.Optional[str] = None,
                 color: str = "darkred",
                 max_n_cols: int = 4,
                 font_size: int = 7,
                 n_top: int = 10,
                 cmap: str = "vlag",
                 ):
        """
        :param df: pandas dataframe.
        :param color: color plate of graphs.
        :param max_n_cols: maximum graph counts which can put to one row.
        :param font_size: text size.
        :param n_top: leaves only n_top frequent categorical values, rest will be replaced with "others" value.
        :param cmap: color map. NOTE: better to use diverging palettes.
        """
        self._df = df.copy()
        self._color = color
        self._max_n_cols = max_n_cols
        self._font_size = font_size
        self._cats_columns = get_categorical_columns(self._df)
        self._nums_columns = get_numeric_columns(self._df)
        self._n_top = n_top
        self._cmap = cmap
        self._target = target

    def cat_futures_eda(self, one_graph_size: int = 4):
        categorical_eda(
            df=self._df,
            columns=self._cats_columns,
            max_n_cols=self._max_n_cols,
            color=self._color,
            one_graph_size=one_graph_size,
            font_size=self._font_size,
            n_top=self._n_top,
        )

    def numeric_futures_eda(self, log_scale: bool, one_graph_size: int = 4):
        numeric_eda(
            df=self._df,
            columns=self._nums_columns,
            max_n_cols=self._max_n_cols,
            one_graph_size=one_graph_size,
            color=self._color,
            font_size=self._font_size,
            log_scale=log_scale,
        )

    def heat_map(self, sample_count: int, one_graph_size: int = 4):
        df = self._df.sample(n=sample_count, random_state=101)
        correlation_matrix(
            df=df,
            numeric_columns=self._nums_columns,
            fig_size=one_graph_size,
            font_size=self._font_size,
        )
        categorical_heatmap(
            df=df,
            columns=self._cats_columns,
            max_n_cols=self._max_n_cols,
            one_graph_size=one_graph_size,
            n_top=self._n_top,
        )

    def bivariate(self, one_graph_size: int, style: str, sample_count: int):
        """
        style: None or in ["kde", "scatter", "histplot"]
        """
        df = self._df.sample(n=sample_count, random_state=101)
        plot_pair_numeric_eda(
            df=df,
            columns=self._nums_columns,
            one_graph_size=one_graph_size,
            max_n_cols=self._max_n_cols,
            style=style,
            target=self._target,
        )
