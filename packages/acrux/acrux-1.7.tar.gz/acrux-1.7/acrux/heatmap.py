import typing as tp

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .generator import pair_generator
from .utils import get_grid_size
from .utils import series_truncator


def correlation_matrix(*,
                       df: pd.DataFrame,
                       numeric_columns: tp.List[str],
                       fig_size: int,
                       font_size: int) -> tp.Optional[plt.Figure]:
    if len(numeric_columns) < 2:
        return

    # Compute the correlation matrix
    corr = df[numeric_columns].corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    figure, ax = plt.subplots(figsize=(fig_size, fig_size))

    ax.set_title("Correlation matrix", fontsize=font_size)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap="vlag", vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})

    return figure


def heatmap(*, df: pd.DataFrame, col1: str, col2: str, ax, n_top: int = 10, cmap: str):
    data = df[[col1, col2]].copy()
    data[col1] = series_truncator(data[col1], n_top)
    data[col2] = series_truncator(data[col2], n_top)

    data["__count__"] = 1

    data = data.groupby([col1, col2]).apply(lambda x: sum(x["__count__"])).reset_index(name="__count__")
    data = data.pivot(index=col1, columns=col2, values="__count__").fillna(0)
    data = 100 * data / data.values.sum()
    data = data.astype(int)

    sns.heatmap(data, annot=False, linewidths=.5, ax=ax, cmap=cmap, square=True, cbar=True)


def categorical_heatmap(*,
                        df: pd.DataFrame,
                        columns: tp.List[str],
                        max_n_cols: int,
                        one_graph_size: int,
                        n_top: int = 10) -> tp.Optional[plt.Figure]:
    pairs = list(pair_generator(columns))
    if not pairs:
        return

    n_cols, n_rows = get_grid_size(len(pairs), max_n_cols)
    fig = plt.figure(figsize=(one_graph_size * n_cols, one_graph_size * n_rows))

    fig.subplots_adjust(top=1.05)

    for index, (col1, col2) in enumerate(pairs, start=1):
        ax = fig.add_subplot(n_rows, n_cols, index)
        heatmap(
            df=df,
            col1=col1,
            col2=col2,
            ax=ax,
            n_top=n_top,
            cmap="Reds",
        )

    plt.tight_layout()
    return fig
