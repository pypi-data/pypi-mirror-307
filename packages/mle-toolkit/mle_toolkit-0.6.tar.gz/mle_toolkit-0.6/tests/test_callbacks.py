import pandas as pd
import pytest

from mle_toolkit import (
    save_file,
    read_file,
    filter_metrics,
    keep_only_selected_trials_artifacts,
)


@pytest.mark.parametrize("case", [
    dict(
        metrics={
            "accuracy": [1, 2, 3, 4, 5, 6],
            "trial": [1, 1, 2, 2, 3, 3],

        },
        trials=[2, 3],
        expected={
            "accuracy": [3, 4, 5, 6],
            "trial": [2, 2, 3, 3],
        },
    ),
])
def test_merge_metrics_callback(tmp_path, case):
    # Arrange
    metrics_path = tmp_path / "metrics.csv"
    save_file(metrics_path, pd.DataFrame(case["metrics"]))

    # Act
    filter_metrics(case["trials"], metrics_path)

    # Assert
    actual_metrics = read_file(metrics_path)
    pd.testing.assert_frame_equal(pd.DataFrame(case["expected"]), actual_metrics)


@pytest.mark.parametrize("case", [
    dict(
        best_trials=[1, 2],
        folders={
            "folder1": [
                "trial_0.json",
                "trial_1.json",
                "trial_2.json",
            ],
            "folder2": [
                "trial_0_fold_0.json",
                "trial_1_fold_0.json",
                "trial_2_fold_0.json",
                "trial_0_fold_1.json",
                "trial_1_fold_1.json",
                "trial_2_fold_1.json",
            ],
            "folder3": [
                "trial_0_fold_0_mode_train.json",
                "trial_0_fold_1_mode_val.json",
                "trial_0_fold_2_mode_test.json",
                "trial_1_fold_0_mode_train.json",
                "trial_1_fold_1_mode_val.json",
                "trial_1_fold_2_mode_test.json",
                "trial_2_fold_0_mode_train.json",
                "trial_2_fold_1_mode_val.json",
                "trial_2_fold_2_mode_test.json",
            ],
        },
        expected={
            "folder1": [
                "trial_1.json",
                "trial_2.json",
            ],
            "folder2": [
                "trial_1_fold_0.json",
                "trial_2_fold_0.json",
                "trial_1_fold_1.json",
                "trial_2_fold_1.json",
            ],
            "folder3": [
                "trial_1_fold_0_mode_train.json",
                "trial_1_fold_1_mode_val.json",
                "trial_1_fold_2_mode_test.json",
                "trial_2_fold_0_mode_train.json",
                "trial_2_fold_1_mode_val.json",
                "trial_2_fold_2_mode_test.json",
            ],
        }
    ),
    dict(
        best_trials=[2],
        folders={
            "folder1": [
                "trial_0.json",
                "trial_1.json",
                "trial_2.json",
            ],
            "folder2": [
                "trial_0_fold_0.json",
                "trial_1_fold_0.json",
                "trial_2_fold_0.json",
                "trial_0_fold_1.json",
                "trial_1_fold_1.json",
                "trial_2_fold_1.json",
            ],
            "folder3": [
                "trial_0_fold_0_mode_train.json",
                "trial_0_fold_1_mode_val.json",
                "trial_0_fold_2_mode_test.json",
                "trial_1_fold_0_mode_train.json",
                "trial_1_fold_1_mode_val.json",
                "trial_1_fold_2_mode_test.json",
                "trial_2_fold_0_mode_train.json",
                "trial_2_fold_1_mode_val.json",
                "trial_2_fold_2_mode_test.json",
            ],
        },
        expected={
            "folder1": [
                "trial_2.json",
            ],
            "folder2": [
                "trial_2_fold_0.json",
                "trial_2_fold_1.json",
            ],
            "folder3": [
                "trial_2_fold_0_mode_train.json",
                "trial_2_fold_1_mode_val.json",
                "trial_2_fold_2_mode_test.json",
            ],
        }
    ),
])
def test_keep_best_n_trials_callback(tmp_path, case):
    # Arrange
    for folder, files in case["folders"].items():
        for file in files:
            save_file(tmp_path / folder / file, {"key": "value"})

    # Act
    keep_only_selected_trials_artifacts(trials=case["best_trials"], artifact_folder=tmp_path)

    # Assert
    for folder, files in case["expected"].items():
        assert set((tmp_path / folder).glob("trial_*")) == set([tmp_path / folder / file for file in files])
