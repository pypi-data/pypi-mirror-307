import pytest
import seaborn as sns

from acrux.pair_numeric import plot_pair_numeric_eda
from tests.utils import find_folder


@pytest.mark.parametrize("style", ["kde", "scatter", "histplot"])
def test_pair_numeric_eda(style: str):
    df = sns.load_dataset("iris")
    fig = plot_pair_numeric_eda(
        df=df,
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
        target="species",
        max_n_cols=3,
        one_graph_size=3,
        style=style,
    )
    artifact_folder = find_folder("tests_outputs")
    fig.savefig(f"{artifact_folder}/pair_numeric_eda_{style}.png")
