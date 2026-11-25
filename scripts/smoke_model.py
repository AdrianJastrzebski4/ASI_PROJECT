import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

DEFAULT_SAMPLE = Path(__file__).resolve().parents[1] / "data" / "01_raw" / "sample.csv"
SAMPLE_SIZE = 5


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pobiera produkcyjny pakiet z W&B i sprawdza pięć predykcji."
    )
    parser.add_argument("--artifact", required=True, help="Format: entity/project/artifact")
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    args = parser.parse_args()

    parts = args.artifact.split("/")
    if len(parts) != 3 or any(
        not part or ":" in part or any(char.isspace() for char in part) for part in parts
    ):
        parser.error("--artifact musi mieć format entity/project/artifact, bez aliasu.")

    if not args.sample.is_file():
        parser.error(f"Nie znaleziono pliku próbki: {args.sample}")

    import numpy as np
    import pandas as pd
    import wandb

    from asi_project.data import normalize_input
    from asi_project.model_package import load_model_package

    sample = pd.read_csv(args.sample, nrows=SAMPLE_SIZE)
    if len(sample) != SAMPLE_SIZE:
        parser.error(f"Próbka musi zawierać co najmniej {SAMPLE_SIZE} wierszy.")

    artifact_ref = f"{args.artifact}:production"
    with TemporaryDirectory(prefix="asi-smoke-") as download_dir:
        artifact = wandb.Api().artifact(artifact_ref, type="model")
        package_dir = Path(artifact.download(root=download_dir))
        model, metadata = load_model_package(package_dir)

        features = metadata["features"]
        missing_features = [feature for feature in features if feature not in sample.columns]
        if missing_features:
            parser.error(f"W próbce brakuje kolumn: {', '.join(missing_features)}")

        inputs = normalize_input(sample.loc[:, features])
        predictions = np.asarray(model.predict(inputs))

        if predictions.shape != (SAMPLE_SIZE,):
            parser.error(f"Oczekiwano pięciu etykiet, otrzymano kształt {predictions.shape}.")
        if not np.isin(predictions, [0, 1]).all():
            parser.error("Predykcje muszą zawierać wyłącznie etykiety 0 lub 1.")

        print(f"Smoke test OK dla {artifact_ref}. Predykcje: {predictions.tolist()}")


if __name__ == "__main__":
    main()
