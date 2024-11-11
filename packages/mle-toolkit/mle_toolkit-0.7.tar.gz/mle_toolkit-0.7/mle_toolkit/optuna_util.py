import typing as tp
from pathlib import Path

import optuna


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


def get_last_study(artifact_dir: Path, study: str) -> str:
    """
    Useful while inference in order get the last study name.
    """
    all_studies = filter(lambda x: study in x.name, artifact_dir.glob("*"))
    return max(all_studies).name
