import json
from pathlib import Path

import joblib

METADATA_KEYS = [
    "model_format",
    "features",
    "target",
    "positive_class",
    "metrics",
    "git_sha",
    "data_fingerprint",
    "library_versions",
]


def save_model_package(model, metadata, package_dir):
    missing = []
    for key in METADATA_KEYS:
        if key not in metadata:
            missing.append(key)

    if missing:
        raise ValueError(f"W metadata brakuje kluczy: {missing}")

    package_dir = Path(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    if metadata["model_format"] == "sklearn":
        joblib.dump(model, package_dir / "model.joblib")
    else:
        model.clone(str(package_dir / "model"), dirs_exist_ok=True)

    with open(package_dir / "metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    return package_dir


def load_model_package(package_dir):
    package_dir = Path(package_dir)

    with open(package_dir / "metadata.json", encoding="utf-8") as file:
        metadata = json.load(file)

    if metadata["model_format"] == "sklearn":
        model = joblib.load(package_dir / "model.joblib")
    else:
        from autogluon.tabular import TabularPredictor

        model = TabularPredictor.load(str(package_dir / "model"))

    return model, metadata
