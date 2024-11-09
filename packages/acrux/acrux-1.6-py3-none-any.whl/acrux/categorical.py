import typing as tp

import matplotlib.pylab as plt
import numpy as np
import pandas as pd

from .utils import get_grid_size, text_truncator


def categorical_eda(
        *,
        df,
        columns: tp.List[str],
        max_n_cols: int = 4,
        one_graph_size: int = 4,
        color: str,
        font_size: int,
        n_top: int = 10) -> tp.Optional[plt.Figure]:
    if not columns:
        return
    n_cols, n_rows = get_grid_size(len(columns), max_n_cols)
    fig = plt.figure(figsize=(one_graph_size * n_cols, one_graph_size * n_rows))
    fig.subplots_adjust(top=1.05)

    for index, c in enumerate(columns, start=1):
        ax = fig.add_subplot(n_rows, n_cols, index)
        _histogram(
            fig=fig,
            series=df[c],
            color=color,
            ax=ax,
            font_size=font_size,
            n_top=n_top,
        )
    plt.tight_layout()
    return fig


def _histogram(
        *,
        fig,
        series: pd.Series,
        color: str,
        n_top: int,
        font_size: int,
        ax: tp.Optional[plt.Axes] = None,
) -> None:
    """
    Plots for categorical data histogram. Only n_top frequent categories will be used, other will replace as "Other"
    """

    # Calculate frequency of categorical data
    stat = series.value_counts(ascending=False, normalize=False)
    missing_values_count = series.isna().sum()
    missing_value_ratio = round(missing_values_count / len(series) * 100, 2)

    # Replace n top categories with "Other"
    x = stat.index.to_list()[:n_top] + ["Other"]
    count = np.array(stat.values.tolist()[:n_top] + [stat.values[n_top:].sum()])

    # Create axes
    if ax is None:
        fig.subplots_adjust(top=0.85)
        ax = fig.add_subplot()

    # Set labels and title
    ax.set_title(str(series.name), fontsize=font_size)
    ax.set_xlabel("rank", fontsize=font_size)
    ax.set_ylabel("ratio, %", fontsize=font_size)
    ax.bar(range(len(x)), count, color=color)

    # Add text box
    text = '\n'.join(
        [f"{text_truncator(k, 30)}: {v}" for k, v in zip(x, count)] +
        [f'\nmissing values: count: = {missing_values_count} ({missing_value_ratio} %)']
    )
    ax.text(
        0.95,
        0.95,
        text,
        verticalalignment='top',
        horizontalalignment='right',
        transform=ax.transAxes,
        color='black',
        fontsize=font_size,
        bbox=dict(facecolor='white', alpha=0.7, edgecolor=color)
    )
