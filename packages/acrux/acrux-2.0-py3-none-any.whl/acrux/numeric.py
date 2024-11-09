import typing as tp

import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns
from joblib import delayed

from .utils import get_grid_size, ProgressParallel


def numeric_eda(
        *,
        df,
        columns: tp.List[str],
        max_n_cols: int,
        one_graph_size: int,
        color: str,
        font_size: int,
        log_scale: bool) -> tp.Optional[plt.Figure]:
    if not columns:
        return

    n_cols, n_rows = get_grid_size(len(columns), max_n_cols)
    fig, axes = plt.subplots(nrows=n_rows,
                             ncols=n_cols,
                             figsize=(one_graph_size * n_cols, one_graph_size * n_rows),
                             squeeze=False)
    fig.subplots_adjust(top=1.05)

    parallel = ProgressParallel(n_jobs=-1, total=len(columns), require="sharedmem")
    with parallel:
        parallel(delayed(_kde)(fig=fig,
                               series=df[c],
                               log_scale=log_scale,
                               color=color,
                               ax=ax,
                               font_size=font_size)
                 for ax, c in zip(axes.ravel(), columns))

    # Off unused plot's axis
    unused = n_cols * n_rows - len(columns)
    if unused > 0:
        for ax in axes.ravel()[-unused:]:
            ax.set_axis_off()

    plt.tight_layout()
    return fig


def _kde(
        *,
        fig,
        series: pd.Series,
        log_scale: bool,
        color: str,
        font_size: int,
        ax=None,
) -> None:
    """Plots KDE (Kernel Density Estimation) for given numeric Pandas series."""

    missing_values_count = series.isna().sum()
    missing_value_ratio = round(missing_values_count / len(series) * 100, 2)
    if missing_values_count > 0:
        text = f"missing values: count: {missing_values_count} ({missing_value_ratio})%"
    else:
        text = f"missing values: count: {missing_values_count}"

    if ax is None:
        fig.subplots_adjust(top=0.85)
        ax = fig.add_subplot()

    ax.set_title(text, fontsize=font_size)
    sns.histplot(data=series, ax=ax, kde=True, color=color, log_scale=log_scale)
