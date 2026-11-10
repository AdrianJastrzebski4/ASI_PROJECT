import pandas as pd

from asi_project.config import DatasetContract, ProjectConfig
from asi_project.data import assert_valid, filter_training_rows, normalize_input


def validate_data_node(
    df: pd.DataFrame,
    contract: DatasetContract,
    config: ProjectConfig | None = None,
) -> pd.DataFrame:

    assert_valid(df, contract, config)
    return df


def normalize_input_node(df: pd.DataFrame) -> pd.DataFrame:
    return normalize_input(df)


def filter_training_rows_node(
    df: pd.DataFrame,
    contract: DatasetContract,
) -> pd.DataFrame:

    return filter_training_rows(df, contract)
