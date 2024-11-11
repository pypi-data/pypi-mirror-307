import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from mle_toolkit.common import get_extension


def read_file(path: Path | str, **kwargs):
    ext = get_extension(path)
    if ext == ".csv":
        return pd.read_csv(path)
    elif ext == ".parquet":
        return pd.read_parquet(path)
    elif ext == ".pickle":
        return pickle.load(open(path, "rb"))
    elif ext == ".npy":
        return np.load(str(path))
    elif ext == ".json":
        with open(path) as file:
            return json.load(file)
    elif ext == ".yaml":
        with open(path, "r") as file:
            return yaml.safe_load(file)
    else:
        raise NotImplementedError(f'Unknown file extension: {ext}')


def save_file(path: Path, data):
    if not path.parent.is_dir():
        path.parent.mkdir(exist_ok=True, parents=True)

    ext = get_extension(path)
    if ext == ".csv":
        if isinstance(data, pd.DataFrame):
            data.to_csv(path, index=False)
        else:
            raise Exception(f'Cant save data with type {type(data)} as .csv')
    elif ext == ".pickle":
        with open(path, "wb") as f:
            pickle.dump(data, f)
    elif ext == ".npy":
        np.save(str(path), data)
    elif ext == ".json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=True, indent=2)
    elif ext == ".yaml":
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
    else:
        raise NotImplementedError(f'Unknown file extension: {ext}')
