import importlib
import logging
import os
import subprocess
import sys
import typing as tp
from pathlib import Path

import optuna
import pandas as pd


def exclude_columns(columns: tp.Tuple[str, ...], excludes: tp.Tuple[str, ...]) -> tp.Tuple[str, ...]:
    return tuple([col for col in columns if col not in excludes])


def get_numeric_columns(df: pd.DataFrame) -> tp.Tuple[str, ...]:
    return tuple(df.select_dtypes(include=["number"]).columns.to_list())


def get_categorical_columns(df: pd.DataFrame) -> tp.Tuple[str, ...]:
    """Categorical columns are which are not numerical."""
    return tuple(set(df.columns.to_list()) - set(get_numeric_columns(df)))


def get_nan_columns(df: pd.DataFrame) -> tp.Tuple[str, ...]:
    return df.columns[df.isna().sum(axis=0) > 0].to_list()


def get_extension(path: Path) -> str:
    return os.path.splitext(path)[-1]


def get_module(name: str):
    """
    Dynamic importing python modules
    Args:
        name: "sklearn.svm.SVC"
    Returns:
        sklearn.svm.SVC
    """
    module, function = name.rsplit(".", 1)
    module = importlib.import_module(module)
    return getattr(module, function)


def construct_path(*,
                   folder: Path,
                   trial_id: tp.Optional[int] = None,
                   fold_id: tp.Optional[int] = None,
                   mode: tp.Optional[str] = None,
                   extension: tp.Optional[str] = None) -> Path:
    name = ""
    if trial_id is not None:
        name = f"trial_{trial_id}"

    if fold_id is not None:
        name += f"_fold_{fold_id}" if name else f"fold_{fold_id}"

    if mode is not None:
        name += f"_mode_{mode}" if name else f"mode_{mode}"

    if extension is not None:
        return (folder / name).with_suffix(extension)
    else:
        return folder / name


def get_files(*,
              folder: Path,
              trial_id: tp.Optional[tp.Union[str, int]] = None,
              fold_id: tp.Optional[tp.Union[str, int]] = None,
              mode: tp.Optional[str] = None,
              extension: str = ".*") -> tp.List[Path]:
    """
    Returns list of files which name by "construct_path" function.
    NOTE: For getting all trial_id, fold_id use '*'
    """
    pattern = ""
    if trial_id is not None:
        pattern = f"trial_{trial_id}"

    if fold_id is not None:
        pattern += f"_fold_{fold_id}" if pattern else f"fold_{fold_id}"

    if mode is not None:
        pattern += f"_mode_{mode}" if pattern else f"mode_{mode}"

    pattern += extension

    return list(folder.glob(pattern))


def get_file_name(absolute_path: Path) -> str:
    return str(absolute_path).split('/')[-1].split('.')[0]


def get_fold_id(path: Path) -> int:
    path = get_file_name(path)
    if "_mode_" in path:
        path = path.split("_mode_")[0]
    return int(path.split("_fold_")[-1])


def get_mode(path: Path) -> str:
    path = get_file_name(path)
    if "mode" in str(path):
        return path.split("_mode_")[-1]
    raise Exception(f"{path} does not contain '_mode_'")


def get_trial_id(path: Path) -> int:
    path = get_file_name(path)
    if "trial" in str(path):
        return int(path.split("_")[1])
    raise Exception(f"{path} does not contain 'trial'")


def init_logger(*, name: str, path: tp.Optional[Path], level=logging.DEBUG, log_format: str = "%(message)s") -> None:
    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    formatter = logging.Formatter(log_format)

    if path is None:
        handler = logging.StreamHandler(stream=sys.stdout)
    else:
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch(exist_ok=True)
        handler = logging.FileHandler(path, mode="w+")

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def suggest_or_get_predefined_params(*,
                                     module: tp.Union[str, tp.Dict],
                                     optuna_suggester: tp.Callable,
                                     trial: optuna.Trial,
                                     kwargs: tp.Dict) -> tp.Optional[tp.Dict[str, tp.Any]]:
    if isinstance(module, str):
        return {
            "module": module,
            "params": optuna_suggester(module, trial, **kwargs),
        }
    elif isinstance(module, dict) and ("module" in module) and ("params" in module):
        return module


def get_last_study(artifact_dir: Path, study: str) -> str:
    """
    Useful while inference in order get the last study name.
    """
    all_studies = filter(lambda x: study in x.name, artifact_dir.glob("*"))
    return max(all_studies).name


def if_gpu_supported() -> bool:
    try:
        subprocess.check_output("nvidia-smi")
        return True
    except Exception:
        return False
