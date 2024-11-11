import logging
import sys
import typing as tp
from pathlib import Path

import optuna


def load_study(*,
               study_name: str,
               storage: str = "sqlite:///experiments.db",
               sampler: tp.Optional[optuna.samplers.BaseSampler] = None) -> optuna.Study:
    """
    Load an optuna study based on a name
    Args:
        study_name: Name of study
        storage: Path to the database where Optuna studies data are stored.
        sampler: Sampler for parameter grid. Defaults to TPESampler()
    Returns:
        Study: Existed Optuna study object
    """
    return optuna.load_study(
        study_name=study_name,
        storage=storage,
        sampler=sampler,
    )


def new_study(*,
              study_name: str,
              storage: str = "sqlite:///experiments.db",
              sampler: tp.Optional[optuna.samplers.BaseSampler] = None,
              direction: str = "maximize") -> optuna.Study:
    """
    Create New Optuna Study Object. If it exists it will fail.
    Args:
        study_name: Name of study
        storage: Database path to store optuna study data.
        sampler: Sampler for parameter grid. Defaults to TPESampler().
        direction: Direction of optimization.
    Returns:
         Study: New optuna study object.
    """
    if sampler is None:
        sampler = optuna.samplers.TPESampler()

    try:
        study = optuna.create_study(
            study_name=study_name,
            storage=storage,
            load_if_exists=False,
            sampler=sampler,
            direction=direction,
        )
        return study
    except optuna.exceptions.DuplicatedStudyError:
        print("Please specify a different study name. NOTE: All optuna studies can be stored in one database.")
        sys.exit(1)


def fork_study(study_name: str) -> str:
    """
    Name of the study to fork, to continue optimization
    see: https://medium.com/towards-data-science/mlops-with-optuna-b7c52d931b4b:

    Sometimes your model is making progress, but you haven’t quite run the model long enough.
    This is an easy fix for model optimization. But, this is a more difficult problem for hyperparameter optimization.

    Fortunately, with limited adjustment, you can load old studies and continue your search.
    Moreover, upon the analysis, you may find that your best models are within a certain range of hyperparameters.

    With the fork function, you can split off your studies and explore different hyper-parameter grids.

    Think your learning rate isn’t quite low enough? Adjust the parameter grid and keep running.
    The underlying objective model for the hyperparameter search continues to optimize when continuing the study.

    Args:
        study_name (str): Name of optuna study object
    Returns:
        str: Name of new forked study
    """
    to_study_name = study_name + '_fork'

    from_storage = f"sqlite:///{study_name}.db"
    to_storage = f"sqlite:///{to_study_name}.db"

    optuna.copy_study(
        from_study_name=study_name,
        from_storage=from_storage,
        to_study_name=to_study_name,
        to_storage=to_storage,
    )
    return to_study_name


def set_optuna_logger(log_format: str = "%(message)s", path: tp.Optional[Path] = None, mode: str = "a") -> None:
    """
    Args:
        log_format: format of logs, see https://docs.python.org/3/library/logging.html
        path: File name to writing Optuna logs
        mode: "a" - append logs, "w+" - clear all previous logs
    Returns: None
    """
    if path is None:
        handler = logging.StreamHandler(stream=sys.stdout)
    else:
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch(exist_ok=True)
        handler = logging.FileHandler(path, mode=mode)

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    optuna.logging.get_logger("optuna").addHandler(handler)


def get_n_best_trials(study: optuna.Study, direction: str, n: int) -> tp.List[int]:
    """
    Returns n best trials: if scores are same for 2 trials then older trial is better. This adds deterministic property.
    """
    trials = list(filter(lambda trial: trial.state == optuna.trial.TrialState.COMPLETE, study.get_trials()))

    def get_integer_value(trial) -> int:
        """
        Comparing float is bad, so use this function to convert it to integer
        """
        return int(trial.values[0] * 10 ** 8)

    if direction == "maximize":
        trials.sort(key=lambda trial: (get_integer_value(trial), -trial.number), reverse=True)
    else:
        trials.sort(key=lambda trial: (get_integer_value(trial), trial.number), reverse=False)

    return [trial.number for trial in trials[:n]]
