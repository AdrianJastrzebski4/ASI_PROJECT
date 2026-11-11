import pandas as pd

from asi_project.config import (
    DatasetContract,
    ProjectConfig,
    get_contract,
    load_project_config,
)
from asi_project.data import assert_valid, filter_training_rows, normalize_input


def validate_data_node(
    df: pd.DataFrame,
    contract: DatasetContract | None = None,
    config: ProjectConfig | None = None,
) -> pd.DataFrame:
    if contract is None:
        config = load_project_config()
        contract = get_contract(config)

    assert_valid(df, contract, config)
    return df


def normalize_input_node(df: pd.DataFrame) -> pd.DataFrame:
    return normalize_input(df)


def filter_training_rows_node(
    df: pd.DataFrame,
    contract: DatasetContract | None = None,
) -> pd.DataFrame:
    if contract is None:
        config = load_project_config()
        contract = get_contract(config)

    return filter_training_rows(df, contract)
