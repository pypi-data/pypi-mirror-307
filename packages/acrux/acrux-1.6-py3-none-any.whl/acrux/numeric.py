import typing as tp

import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns

from .utils import get_grid_size


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
    fig = plt.figure(figsize=(one_graph_size * n_cols, one_graph_size * n_rows))
    fig.subplots_adjust(top=1.05)

    for index, c in enumerate(columns, start=1):
        ax = fig.add_subplot(n_rows, n_cols, index)
        _kde(
            fig=fig,
            series=df[c],
            log_scale=log_scale,
            color=color,
            ax=ax,
            font_size=font_size,
        )
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
