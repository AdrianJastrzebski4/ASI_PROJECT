import hashlib
import os
import subprocess
from typing import Any

import pandas as pd
import wandb


def get_git_sha() -> str:
    """Zwraca aktualny hash commita Git (SHA) lub 'unknown', jeśli repozytorium jest niedostępne."""
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return sha
    except Exception:
        return "unknown"


def compute_data_fingerprint(df: pd.DataFrame) -> str:
    """Oblicza deterministyczny skrót SHA-256 ramki danych niezależnie od systemu operacyjnego."""
    row_hashes = pd.util.hash_pandas_object(df, index=True).values.tobytes()
    col_names = "|".join(map(str, df.columns)).encode("utf-8")
    digest = hashlib.sha256(col_names + row_hashes).hexdigest()
    return digest[:16]


def log_wandb_run(
    run_name: str,
    wandb_params: dict[str, Any],
    config_payload: dict[str, Any],
    metrics: dict[str, Any],
    tags: list[str] | None = None,
) -> None:
    """Tworzy pojedynczy run w W&B, loguje konfigurację i metryki, a następnie zamyka sesję."""
    mode = os.environ.get("WANDB_MODE", wandb_params.get("mode", "online"))

    run = wandb.init(
        project=wandb_params.get("project", "asi-predictive-maintenance"),
        entity=wandb_params.get("entity") or None,
        name=run_name,
        config=config_payload,
        tags=tags or [],
        mode=mode,
        reinit="finish_previous",
    )
    if run is not None:
        run.log(metrics)
        run.finish()
