from asi_project.config import get_contract, load_project_config
from asi_project.data import filter_training_rows, load_dataset, normalize_input
from asi_project.model_package import load_model_package, save_model_package
from asi_project.pipelines.data_science.nodes import split_data, train_model


def test_save_load_predict(tmp_path):
    config = load_project_config()
    contract = get_contract(config)
    raw = load_dataset(config, contract, mode="sample")
    data = filter_training_rows(normalize_input(raw), contract)

    X_train, X_test, y_train, _ = split_data(data, {"test_size": 0.2, "random_state": 42})
    model = train_model(X_train, y_train)

    metadata = {
        "model_format": "sklearn",
        "features": list(config.model_features),
        "target": contract.target,
        "positive_class": contract.positive_class,
        "metrics": {"f1": 0.5},
        "git_sha": "test",
        "data_fingerprint": "test",
        "library_versions": {},
    }

    save_model_package(model, metadata, tmp_path)
    loaded_model, loaded_metadata = load_model_package(tmp_path)

    assert loaded_metadata == metadata
    assert list(loaded_model.predict(X_test.head(5))) == list(model.predict(X_test.head(5)))
