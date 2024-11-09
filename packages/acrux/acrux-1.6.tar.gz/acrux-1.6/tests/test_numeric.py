import seaborn as sns

from acrux.numeric import numeric_eda
from tests.utils import find_folder


def test_numeric_eda():
    df = sns.load_dataset("iris")
    fig = numeric_eda(
        df=df,
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
        max_n_cols=4,
        one_graph_size=3,
        color="darkred",
        font_size=6,
        log_scale=False,
    )
    artifact_folder = find_folder("tests_outputs")
    fig.savefig(f"{artifact_folder}/numeric_eda.png")
