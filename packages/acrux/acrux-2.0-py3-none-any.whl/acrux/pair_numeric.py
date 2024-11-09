import typing as tp

import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns
from joblib import delayed

from .generator import pair_generator
from .utils import get_grid_size, should_skip_pair, ProgressParallel


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
    fig, axes = plt.subplots(nrows=n_rows,
                             ncols=n_cols,
                             figsize=(one_graph_size * n_cols, one_graph_size * n_rows),
                             squeeze=False)
    fig.subplots_adjust(top=1.05)

    parallel = ProgressParallel(n_jobs=-1, total=len(numeric_pairs), require="sharedmem")
    with parallel:
        if style == "kde":
            parallel(delayed(sns.kdeplot)(x=df[col1],
                                          y=df[col2],
                                          ax=ax,
                                          warn_singular=False,
                                          color="darkred",
                                          fill=False,
                                          hue=df[target] if target else None)
                     for ax, (col1, col2) in zip(axes.ravel(), numeric_pairs))
        elif style == "scatter":
            parallel(delayed(sns.scatterplot)(x=df[col1],
                                              y=df[col2],
                                              ax=ax,
                                              hue=df[target] if target else None)
                     for ax, (col1, col2) in zip(axes.ravel(), numeric_pairs))
        elif style == "histplot":
            parallel(delayed(sns.histplot)(x=df[col1],
                                           y=df[col2],
                                           ax=ax,
                                           cmap="vlag",
                                           hue=df[target] if target else None)
                     for ax, (col1, col2) in zip(axes.ravel(), numeric_pairs))
        else:
            raise "style must be in [kde, scatter, histplot]"

    # Off unused plot's axis
    unused = n_cols * n_rows - len(numeric_pairs)
    if unused > 0:
        for ax in axes.ravel()[-unused:]:
            ax.set_axis_off()

    plt.tight_layout()
    return fig
