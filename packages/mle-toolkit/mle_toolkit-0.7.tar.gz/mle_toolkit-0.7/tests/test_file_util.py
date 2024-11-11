import typing as tp
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from mle_toolkit import read_file, save_file


@pytest.mark.parametrize("case", [
    dict(
        path=Path("data.npy"),
        data=np.array([1, 2, 3]),

    ),
    dict(
        path=Path("params.json"),
        data=dict(
            devices=[0, 2, 4],
            gpu=True,
            epochs=10,
            batch_size=16,
            mask=None,
        ),
    ),
    dict(
        path=Path("model.pickle"),
        data=[1, 2, 3],
    ),
    dict(
        path=Path("metrics.csv"),
        data=pd.DataFrame(dict(
            metric=["accuracy", "roc_auc"],
            value=[1, 2],  # NOTE: easy to assert with int values
        )),
    ),
])
def test_save_and_read(tmp_path, case: tp.Dict) -> None:
    path = tmp_path / "artifacts" / case["path"]

    # Act
    save_file(path, case["data"])
    data = read_file(path)

    # Assert
    if isinstance(data, np.ndarray):
        assert np.allclose(case["data"], data)
    elif isinstance(data, pd.DataFrame):
        assert data.equals(case["data"])
    else:
        assert case["data"] == data
