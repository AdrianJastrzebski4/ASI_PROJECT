import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Publikuje pakiet modelu w W&B z aliasem production."
    )
    parser.add_argument("--package-dir", required=True, type=Path)
    parser.add_argument("--artifact", required=True, help="Format: entity/project/artifact")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Wyślij pakiet i ustaw alias production.",
    )
    args = parser.parse_args()

    parts = args.artifact.split("/")
    if len(parts) != 3 or any(
        not part or ":" in part or any(char.isspace() for char in part) for part in parts
    ):
        parser.error("--artifact musi mieć format entity/project/artifact, bez aliasu.")
    entity, project, artifact_name = parts

    if not args.package_dir.is_dir():
        parser.error(f"Katalog pakietu nie istnieje: {args.package_dir}")

    metadata_path = args.package_dir / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.error(f"Nie można odczytać {metadata_path}: {error}")

    if not isinstance(metadata, dict):
        parser.error("metadata.json musi zawierać obiekt JSON.")

    if not ((args.package_dir / "model.joblib").is_file() or (args.package_dir / "model").is_dir()):
        parser.error("Pakiet musi zawierać plik model.joblib lub katalog model/.")

    if not args.publish:
        print(f"Pakiet przeszedł walidację. Docelowy artefakt: {args.artifact}:production")
        return

    import wandb

    with wandb.init(entity=entity, project=project, job_type="publish-model", mode="online") as run:
        artifact = wandb.Artifact(name=artifact_name, type="model")
        artifact.add_dir(str(args.package_dir))
        logged_artifact = run.log_artifact(artifact, aliases=["production"])
        logged_artifact.wait()
        print(f"Opublikowano {args.artifact}:{logged_artifact.version} z aliasem production.")


if __name__ == "__main__":
    main()
