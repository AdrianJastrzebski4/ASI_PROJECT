from pathlib import Path
from typing import Any

import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.pipeline import Pipeline

from asi_project.config import get_contract, load_project_config
from asi_project.data import make_xy, split_train_test
from asi_project.metrics import compute_metrics
from asi_project.model import build_baseline_pipeline
from asi_project.tracking import (
    compute_data_fingerprint,
    get_git_sha,
    log_wandb_run,
)


def split_data(
    prepared_data: pd.DataFrame,
    split_params: dict,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    config = load_project_config()
    contract = get_contract(config)

    X, y = make_xy(
        prepared_data,
        contract,
        config.model_features,
    )

    return split_train_test(
        X,
        y,
        contract,
        test_size=split_params["test_size"],
        random_state=split_params["random_state"],
    )


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> Pipeline:
    config = load_project_config()

    model = build_baseline_pipeline(
        numeric_features=config.numeric_features,
        categorical_features=config.categorical_features,
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    y_pred = model.predict(X_test)
    metrics = compute_metrics(y_test, y_pred)
    return metrics


def log_baseline_node(
    metrics: dict[str, Any],
    prepared_data: pd.DataFrame,
    split_params: dict[str, Any],
    wandb_params: dict[str, Any],
) -> dict[str, Any]:
    config = load_project_config()
    git_sha = get_git_sha()
    fingerprint = compute_data_fingerprint(prepared_data)

    run_config = {
        "model_family": "baseline_logistic_regression",
        "dataset_id": config.dataset_id,
        "git_sha": git_sha,
        "data_fingerprint": fingerprint,
        "numeric_features": list(config.numeric_features),
        "categorical_features": list(config.categorical_features),
        **split_params,
    }

    log_wandb_run(
        run_name="baseline-logreg",
        wandb_params=wandb_params,
        config_payload=run_config,
        metrics=metrics,
        tags=["sprint-3", "baseline"],
    )

    return {
        "git_sha": git_sha,
        "data_fingerprint": fingerprint,
        "metrics": metrics,
    }


def run_autogluon_experiments_node(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    prepared_data: pd.DataFrame,
    split_params: dict[str, Any],
    ag_params: dict[str, Any],
    wandb_params: dict[str, Any],
) -> dict[str, Any]:
    if not ag_params.get("enabled", True):
        return {"status": "disabled_in_config"}

    config = load_project_config()
    contract = get_contract(config)
    git_sha = get_git_sha()
    fingerprint = compute_data_fingerprint(prepared_data)

    target_col = contract.target
    train_df = X_train.copy()
    train_df[target_col] = y_train.values

    eval_metric = ag_params.get("eval_metric", "f1")
    base_models_dir = Path(ag_params.get("models_dir", "data/06_models/autogluon"))
    all_results: dict[str, Any] = {}

    for exp_name, exp_cfg in ag_params.get("experiments", {}).items():
        save_path = base_models_dir / exp_name
        presets = exp_cfg.get("presets", "medium_quality")
        time_limit = exp_cfg.get("time_limit", 30)

        predictor = TabularPredictor(
            label=target_col,
            eval_metric=eval_metric,
            path=str(save_path),
            verbosity=1,
        ).fit(
            train_data=train_df,
            presets=presets,
            time_limit=time_limit,
        )

        y_pred = predictor.predict(X_test)
        metrics = compute_metrics(y_test, y_pred)
        best_model_name = predictor.model_best

        run_config = {
            "model_family": "autogluon",
            "experiment_name": exp_name,
            "best_internal_model": best_model_name,
            "presets": presets,
            "time_limit": time_limit,
            "eval_metric": eval_metric,
            "dataset_id": config.dataset_id,
            "git_sha": git_sha,
            "data_fingerprint": fingerprint,
            "artifact_path": str(save_path),
            **split_params,
        }

        log_wandb_run(
            run_name=f"autogluon-{exp_name}",
            wandb_params=wandb_params,
            config_payload=run_config,
            metrics=metrics,
            tags=["sprint-3", "autogluon", exp_name],
        )

        all_results[exp_name] = {
            "best_model": best_model_name,
            "presets": presets,
            "time_limit": time_limit,
            "artifact_path": str(save_path),
            "git_sha": git_sha,
            "data_fingerprint": fingerprint,
            "metrics": metrics,
        }

    return all_results
