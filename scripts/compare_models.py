"""Porównanie modeli (Sprint 3, krok 4)."""

import os
import time
from pathlib import Path

import pandas as pd
import psutil
from sklearn.metrics import f1_score

from asi_project.pipelines.data_science.nodes import split_data

MODELS = {
    "baseline": "data/06_models/model.pkl",
    "ag_fast": "data/06_models/autogluon/ag_fast",
    "ag_good": "data/06_models/autogluon/ag_good",
}

data = pd.read_csv("data/02_intermediate/prepared.csv")
_, X_test, _, y_test = split_data(data, {"test_size": 0.2, "random_state": 42})

process = psutil.Process()
rows = []

for name, path in MODELS.items():
    if not os.path.exists(path):
        print("Brak modelu:", path)
        continue

    memory_before = process.memory_info().rss

    if path.endswith(".pkl"):
        model = pd.read_pickle(path)
        size = os.path.getsize(path)
    else:
        from autogluon.tabular import TabularPredictor

        model = TabularPredictor.load(path)
        size = 0
        for file_path in Path(path).rglob("*"):
            if file_path.is_file():
                size += os.path.getsize(file_path)

    memory = process.memory_info().rss - memory_before

    start = time.perf_counter()
    y_pred = model.predict(X_test)
    predict_time = time.perf_counter() - start

    rows.append(
        {
            "model": name,
            "f1": round(f1_score(y_test, y_pred), 3),
            "predict_time_ms": round(predict_time * 1000, 3),
            "artifact_size_mb": round(size / 1024**2, 3),
            "load_memory_mb": round(memory / 1024**2, 3),
        }
    )

table = pd.DataFrame(rows)
print("\nPorównanie modeli\n")
print(table.to_string(index=False))
