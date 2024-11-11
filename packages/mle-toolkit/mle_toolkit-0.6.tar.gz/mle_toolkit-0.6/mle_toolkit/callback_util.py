import typing as tp
from pathlib import Path

import pandas as pd

from .path_util import get_trial_id


def keep_only_selected_trials_artifacts(trials: tp.List[int], artifact_folder: Path):
    """
    Keeps in storage only specified trials artifacts. Using this function storage memory usage can be improved.
    """
    folders: tp.List[Path] = [path for path in artifact_folder.iterdir() if path.is_dir()]
    for folder in folders:
        for file in folder.glob("trial_*"):
            if get_trial_id(file) not in trials:
                file.unlink(missing_ok=True)


def filter_metrics(trials: tp.List[int], metric_df_path: Path):
    df_metric = pd.read_csv(metric_df_path)
    df_metric["trial"] = df_metric["trial"].astype(int)
    df_metric.merge(pd.Series(trials, name="trial"), how="inner").to_csv(metric_df_path, index=False)
