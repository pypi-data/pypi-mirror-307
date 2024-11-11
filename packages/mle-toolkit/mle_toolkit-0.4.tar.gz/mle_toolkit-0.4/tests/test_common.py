import typing as tp
from pathlib import Path

import pytest

from mle_toolkit import (
    get_extension,
    construct_path,
    get_fold_id,
    get_mode,
    get_trial_id,
    get_last_study,
    get_files,
)


@pytest.mark.parametrize("case", [
    dict(
        path=Path("a/b/data.csv"),
        expected=".csv",
    ),
    dict(
        path=Path("a/b/params.json"),
        expected=".json",
    ),
    dict(
        path=Path("a/b/c/model.pickle"),
        expected=".pickle",
    ),
])
def test_get_extension(case: tp.Dict) -> None:
    assert get_extension(case["path"]) == case["expected"]


@pytest.mark.parametrize("case", [
    dict(
        folder=Path("artifacts/models/"),
        trial_number=0,
        fold_id=0,
        mode=None,
        expectation=Path("artifacts/models/trial_0_fold_0"),
    ),
    dict(
        folder=Path("artifacts/models/"),
        trial_number=100,
        fold_id=23,
        mode=None,
        expectation=Path("artifacts/models/trial_100_fold_23"),
    ),
    dict(
        folder=Path("artifacts/predictions/"),
        trial_number=0,
        fold_id=0,
        mode="val",
        expectation=Path("artifacts/predictions/trial_0_fold_0_mode_val"),
    ),
    dict(
        folder=Path("artifacts/predictions/"),
        trial_number=100,
        fold_id=23,
        mode="test",
        expectation=Path("artifacts/predictions/trial_100_fold_23_mode_test"),
    ),
    dict(
        folder=Path("artifacts/params/"),
        trial_number=0,
        fold_id=None,
        mode=None,
        expectation=Path("artifacts/params/trial_0"),
    ),
    dict(
        folder=Path("artifacts/params/"),
        trial_number=1,
        fold_id=None,
        mode=None,
        expectation=Path("artifacts/params/trial_1"),
    ),
    dict(
        folder=Path("artifacts/params/"),
        trial_number=1,
        fold_id=None,
        mode=None,
        extension=".json",
        expectation=Path("artifacts/params/trial_1.json"),
    ),
    # Complex test case when there are keywords in path like "_mode", "_fold_", "trial"
    dict(
        folder=Path("artifacts/predictions_fold_21_mode_val/"),
        trial_number=100,
        fold_id=23,
        mode="test",
        expectation=Path("artifacts/predictions_fold_21_mode_val/trial_100_fold_23_mode_test"),
    ),
])
def test_construct_path(case: tp.Dict) -> None:
    output = construct_path(folder=case["folder"],
                            trial_id=case["trial_number"],
                            fold_id=case["fold_id"],
                            mode=case["mode"],
                            extension=case.get("extension"))
    assert case["expectation"] == output

    if case["fold_id"] is not None:
        assert case["fold_id"] == get_fold_id(output)

    if case["mode"] is not None:
        assert case["mode"] == get_mode(output)

    assert case["trial_number"] == get_trial_id(output)


FILES_TYPE_1 = [
    "trial_0.json",
    "trial_1.json",
]

FILES_TYPE_2 = [
    "trial_0_fold_0.pickle",
    "trial_0_fold_1.pickle",
    "trial_1_fold_0.pickle",
    "trial_1_fold_1.pickle",
]

FILES_TYPE_3 = [
    "trial_0_fold_0_mode_val.npy",
    "trial_0_fold_0_mode_train.npy",
    "trial_0_fold_1_mode_val.npy",
    "trial_0_fold_1_mode_train.npy",
    "trial_1_fold_0_mode_val.npy",
    "trial_1_fold_0_mode_train.npy",
    "trial_1_fold_1_mode_val.npy",
    "trial_1_fold_1_mode_train.npy",
]

FILES_TYPE_4 = [
    "fold_0_mode_val.npy",
    "fold_0_mode_train.npy",
    "fold_1_mode_val.npy",
    "fold_1_mode_train.npy",
    "fold_0_mode_val.npy",
    "fold_0_mode_train.npy",
    "fold_1_mode_val.npy",
    "fold_1_mode_train.npy",
]


@pytest.mark.parametrize("case", [
    # FILES_TYPE_1
    dict(
        trial_id="*",
        files=FILES_TYPE_1,
        expected=FILES_TYPE_1,
    ),
    dict(
        trial_id=0,
        files=FILES_TYPE_1,
        expected=["trial_0.json"],
    ),

    # FILES_TYPE_2
    dict(
        trial_id="*",
        fold_id="*",
        files=FILES_TYPE_2,
        expected=[
            "trial_0_fold_0.pickle",
            "trial_0_fold_1.pickle",
            "trial_1_fold_0.pickle",
            "trial_1_fold_1.pickle",
        ],
    ),
    dict(
        trial_id="*",
        fold_id=0,
        files=FILES_TYPE_2,
        expected=[
            "trial_0_fold_0.pickle",
            "trial_1_fold_0.pickle",
        ],
    ),
    dict(
        trial_id=0,
        fold_id="*",
        files=FILES_TYPE_2,
        expected=[
            "trial_0_fold_0.pickle",
            "trial_0_fold_1.pickle",
        ],
    ),
    dict(
        trial_id=0,
        fold_id=0,
        files=FILES_TYPE_2,
        expected=[
            "trial_0_fold_0.pickle",
        ],
    ),

    # FILES_TYPE_3
    dict(
        trial_id="*",
        fold_id="*",
        mode="*",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
            "trial_0_fold_0_mode_train.npy",
            "trial_0_fold_1_mode_val.npy",
            "trial_0_fold_1_mode_train.npy",
            "trial_1_fold_0_mode_val.npy",
            "trial_1_fold_0_mode_train.npy",
            "trial_1_fold_1_mode_val.npy",
            "trial_1_fold_1_mode_train.npy",
        ],
    ),
    dict(
        trial_id="*",
        fold_id="*",
        mode="val",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
            "trial_0_fold_1_mode_val.npy",
            "trial_1_fold_0_mode_val.npy",
            "trial_1_fold_1_mode_val.npy",
        ],
    ),
    dict(
        trial_id="*",
        fold_id=0,
        mode="*",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
            "trial_0_fold_0_mode_train.npy",
            "trial_1_fold_0_mode_val.npy",
            "trial_1_fold_0_mode_train.npy",
        ],
    ),
    dict(
        trial_id="*",
        fold_id=0,
        mode="val",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
            "trial_1_fold_0_mode_val.npy",
        ],
    ),
    dict(
        trial_id=0,
        fold_id="*",
        mode="*",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
            "trial_0_fold_0_mode_train.npy",
            "trial_0_fold_1_mode_val.npy",
            "trial_0_fold_1_mode_train.npy",
        ],
    ),
    dict(
        trial_id=0,
        fold_id="*",
        mode="val",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
            "trial_0_fold_1_mode_val.npy",
        ],
    ),
    dict(
        trial_id=0,
        fold_id=0,
        mode="*",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
            "trial_0_fold_0_mode_train.npy",
        ],
    ),
    dict(
        trial_id=0,
        fold_id=0,
        mode="val",
        files=FILES_TYPE_3,
        expected=[
            "trial_0_fold_0_mode_val.npy",
        ],
    ),

    # FILES_TYPE_4
    dict(
        trial_id=None,
        fold_id=0,
        mode="*",
        files=FILES_TYPE_4,
        expected=[
            "fold_0_mode_val.npy",
            "fold_0_mode_train.npy",
            "fold_0_mode_val.npy",
            "fold_0_mode_train.npy",
        ],
    ),
    dict(
        trial_id=None,
        fold_id=0,
        mode="train",
        files=FILES_TYPE_4,
        expected=[
            "fold_0_mode_train.npy",
            "fold_0_mode_train.npy",
        ],
    ),
])
def test_get_list_of_files(tmp_path, case: tp.Dict):
    # Arrange
    d = tmp_path / "artifacts"
    d.mkdir()

    for file in case["files"]:
        f = d / file
        f.touch()

    # Act
    output = get_files(folder=d,
                       trial_id=case.get("trial_id"),
                       fold_id=case.get("fold_id"),
                       mode=case.get("mode"),
                       extension=case.get("extension", ".*"))

    # Assert
    assert set(output) == set({d / f for f in case["expected"]})


@pytest.mark.parametrize("case", [
    dict(
        study="iris",
        studies=[
            "iris_2024_01_01_00_00_00",
            "iris_2024_02_01_00_00_00",
            "mnist_2024_02_01_00_00_00",
        ],
        expected="iris_2024_02_01_00_00_00",
    ),
])
def test_squeeze_target(tmp_path, case: tp.Dict) -> None:
    # Arrange
    for study in case["studies"]:
        (tmp_path / study).mkdir()

    # Act & Assert
    assert get_last_study(tmp_path, case["study"]) == case["expected"]
