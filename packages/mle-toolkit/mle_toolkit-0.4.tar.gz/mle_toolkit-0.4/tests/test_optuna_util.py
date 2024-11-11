import typing as tp

import optuna
import pytest

from mle_toolkit import get_n_best_trials

TRIALS = [
    dict(
        params={"x": 1.0},
        distributions={"x": optuna.distributions.FloatDistribution(1, 10)},
        value=0.1,
    ),
    dict(
        params={"x": 2.0},
        distributions={"x": optuna.distributions.FloatDistribution(1, 10)},
        value=0.2,
    ),
    dict(
        params={"x": 3.0},
        distributions={"x": optuna.distributions.FloatDistribution(1, 10)},
        value=0.3,
    ),
    dict(
        params={"x": 4.0},
        distributions={"x": optuna.distributions.FloatDistribution(1, 10)},
        value=0.2,
    ),
    dict(
        params={"x": 5.0},
        distributions={"x": optuna.distributions.FloatDistribution(1, 10)},
        value=0.2,
    ),
]


@pytest.mark.parametrize("case", [
    dict(
        n_top=2,
        direction="maximize",
        expected_trials=[1, 2],
    ),
    dict(
        n_top=2,
        direction="minimize",
        expected_trials=[0, 1],
    ),
    dict(
        n_top=1,
        direction="minimize",
        expected_trials=[0],
    ),
    dict(
        n_top=1,
        direction="maximize",
        expected_trials=[2],
    ),
])
def test_get_n_best_trials(case: tp.Dict) -> None:
    # Arrange
    study: optuna.Study = optuna.create_study(direction=case["direction"])
    for trial in TRIALS:
        study.add_trial(optuna.trial.create_trial(**trial))

    # Act
    actual_trials = get_n_best_trials(study, case["direction"], case["n_top"])

    # Assert
    assert set(actual_trials) == set(case["expected_trials"])
