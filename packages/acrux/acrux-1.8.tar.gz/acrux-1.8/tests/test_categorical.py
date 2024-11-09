import seaborn as sns

from acrux.categorical import categorical_eda
from tests.utils import find_folder


def test_categorical_eda():
    df = sns.load_dataset("tips")
    fig = categorical_eda(
        df=df,
        columns=["sex", "smoker", "day", "time"],
        max_n_cols=2,
        one_graph_size=3,
        color="darkred",
        n_top=10,
        font_size=6,
    )
    artifact_folder = find_folder("tests_outputs")
    fig.savefig(f"{artifact_folder}/categorical_eda.png")
