import typing as tp

import pandas as pd


def exclude_columns(columns: tp.List[str], excludes: tp.List[str]) -> tp.List[str]:
    return [col for col in columns if col not in excludes]


def get_numeric_columns(df: pd.DataFrame) -> tp.List[str]:
    return df.select_dtypes(include=["number"]).columns.to_list()


def get_categorical_columns(df: pd.DataFrame) -> tp.List[str]:
    return list(set(df.columns.to_list()) - set(get_numeric_columns(df)))


def get_nan_columns(df: pd.DataFrame) -> tp.List[str]:
    return df.columns[df.isna().sum(axis=0) > 0].to_list()
