from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    evaluate_model,
    log_baseline_node,
    run_autogluon_experiments_node,
    split_data,
    train_model,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["prepared_data", "params:split"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="model",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["model", "X_test", "y_test"],
                outputs="metrics",
                name="evaluate_model_node",
            ),
            node(
                func=log_baseline_node,
                inputs=["metrics", "prepared_data", "params:split", "params:wandb"],
                outputs="baseline_tracking_info",
                name="log_baseline_node",
            ),
            node(
                func=run_autogluon_experiments_node,
                inputs=[
                    "X_train",
                    "y_train",
                    "X_test",
                    "y_test",
                    "prepared_data",
                    "params:split",
                    "params:autogluon",
                    "params:wandb",
                ],
                outputs="autogluon_metrics",
                name="run_autogluon_experiments_node",
            ),
        ]
    )
