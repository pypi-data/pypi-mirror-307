import seaborn as sns

from acrux.heatmap import correlation_matrix, categorical_heatmap
from tests.utils import find_folder


def test_correlation_matrix():
    df = sns.load_dataset("iris")
    fig = correlation_matrix(
        df=df,
        numeric_columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
        fig_size=7,
        font_size=10,
    )
    artifact_folder = find_folder("tests_outputs")
    fig.savefig(f"{artifact_folder}/correlation_matrix.png")


def test_categorical_heatmap():
    df = sns.load_dataset("tips")
    fig = categorical_heatmap(
        df=df,
        columns=["sex", "smoker", "day"],
        max_n_cols=3,
        one_graph_size=3,
        n_top=10,
    )
    artifact_folder = find_folder("tests_outputs")
    fig.savefig(f"{artifact_folder}/categorical_heatmap.png")
