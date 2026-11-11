from kedro.pipeline import Pipeline, node, pipeline

from asi_project.pipelines.data_processing.nodes import (
    filter_training_rows_node,
    normalize_input_node,
    validate_data_node,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=validate_data_node,
                inputs="raw_data",
                outputs="validated_data",
                name="validate_data_node",
            ),
            node(
                func=normalize_input_node,
                inputs="validated_data",
                outputs="normalized_data",
                name="normalize_input_node",
            ),
            node(
                func=filter_training_rows_node,
                inputs="normalized_data",
                outputs="prepared_data",
                name="filter_training_rows_node",
            ),
        ]
    )
