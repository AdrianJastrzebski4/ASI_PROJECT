import pandas as pd

from asi_project.pipelines.data_processing.nodes import (
    filter_training_rows_node,
    normalize_input_node,
    validate_data_node,
)


def test_normalize_input_node_strips_text():
    raw_df = pd.DataFrame({"Type": [" L ", " M ", "H"]})
    result = normalize_input_node(raw_df)

    assert result["Type"].tolist() == ["L", "M", "H"]


def test_filter_training_rows_node_removes_duplicates_and_missing_target(
    toy_contract,
):
    df = pd.DataFrame(
        {
            "Type": ["L", "L", "M"],
            "Air temperature [K]": [300.0, 300.0, 295.0],
            toy_contract.target: [0, 0, None],
        }
    )
    filtered = filter_training_rows_node(df, toy_contract)

    assert len(filtered) == 1
    assert filtered.iloc[0]["Type"] == "L"


def test_validate_data_node_passes_valid_df(toy_contract, toy_frame):
    validated = validate_data_node(toy_frame, contract=toy_contract)
    assert len(validated) == len(toy_frame)
