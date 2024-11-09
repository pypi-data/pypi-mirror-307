# Acrux

Simple Exploratory Data Analysis tool.

Example:

```python
import seaborn as sns
from acrux.eda import ExploratoryDataAnalysis

df = sns.load_dataset("iris")

eda = ExploratoryDataAnalysis(df=df)

eda.cat_futures_eda(one_graph_size=3)
eda.numeric_futures_eda(log_scale=False, one_graph_size=3)
eda.heat_map(one_graph_size=3, sample_count=len(df))
```