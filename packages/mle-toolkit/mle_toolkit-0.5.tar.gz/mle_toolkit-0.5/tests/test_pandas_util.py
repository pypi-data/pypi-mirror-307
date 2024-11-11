import pandas as pd

from mle_toolkit import get_numeric_columns, get_categorical_columns


def test_columns_classification():
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })
    assert get_numeric_columns(df) == ["col1"]
    assert get_categorical_columns(df) == ["col2"]
