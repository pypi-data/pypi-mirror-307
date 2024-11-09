import typing as tp

import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns

from .generator import pair_generator
from .utils import get_grid_size, should_skip_pair


def plot_pair_numeric_eda(
        *,
        df: pd.DataFrame,
        columns: tp.List[str],
        target: str,
        one_graph_size: int,
        max_n_cols: int,
        style: str = "kde") -> tp.Optional[plt.Figure]:
    numeric_pairs = [(col1, col2) for col1, col2 in pair_generator(columns) if col1 != target and col2 != target]
    if not numeric_pairs:
        return

    # Filter nan values
    numeric_pairs = [(col1, col2) for col1, col2 in numeric_pairs if not should_skip_pair(df, col1, col2, target)]
    if not numeric_pairs:
        return

    # Divide into plot grids
    n_cols, n_rows = get_grid_size(len(numeric_pairs), max_n_cols)
    fig = plt.figure(figsize=(one_graph_size * n_cols, one_graph_size * n_rows))
    fig.subplots_adjust(top=1.05)

    for index, (col1, col2) in enumerate(numeric_pairs, start=1):
        ax = fig.add_subplot(n_rows, n_cols, index)
        x, y = df[col1], df[col2]
        if style == "kde":
            sns.kdeplot(
                x=x,
                y=y,
                ax=ax,
                warn_singular=False,
                color="darkred",
                fill=False,
                hue=df[target] if target else None,
            )
        elif style == "scatter":
            sns.scatterplot(x=x, y=y, ax=ax, hue=df[target] if target else None)
        elif style == "histplot":
            sns.histplot(x=x, y=y, cmap="vlag", ax=ax, hue=df[target] if target else None)
        else:
            raise "style must be in [kde, scatter, histplot]"

    plt.tight_layout()
    return fig
