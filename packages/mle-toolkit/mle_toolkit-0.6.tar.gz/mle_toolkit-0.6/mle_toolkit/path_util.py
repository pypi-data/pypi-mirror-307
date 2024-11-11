import os
import typing as tp
from pathlib import Path


def get_extension(path: Path) -> str:
    return os.path.splitext(path)[-1]


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
