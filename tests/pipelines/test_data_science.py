from asi_project.config import get_contract, load_project_config
from asi_project.data import (
    filter_training_rows,
    load_dataset,
    normalize_input,
)
from asi_project.pipelines.data_science.nodes import (
    evaluate_model,
    split_data,
    train_model,
)


def make_test_data():
    """Przygotowuje dane do testów z próbki CI."""
    config = load_project_config()
    contract = get_contract(config)

    raw = load_dataset(config, contract, mode="sample")
    return filter_training_rows(normalize_input(raw), contract)


def test_split_data():
    data = make_test_data()

    X_train, X_test, y_train, y_test = split_data(
        data,
        {"test_size": 0.2, "random_state": 42},
    )

    assert len(X_train) + len(X_test) == len(data)
    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)
    assert set(y_train.unique()) == {0, 1}
    assert set(y_test.unique()) == {0, 1}
    assert set(X_train.index).isdisjoint(X_test.index)


def test_train_model():
    data = make_test_data()

    X_train, _, y_train, _ = split_data(
        data,
        {"test_size": 0.2, "random_state": 42},
    )

    model = train_model(X_train, y_train)

    assert hasattr(model, "predict")
    assert "preprocessor" in model.named_steps
    assert "classifier" in model.named_steps


def test_evaluate_model():
    data = make_test_data()

    X_train, X_test, y_train, y_test = split_data(
        data,
        {"test_size": 0.2, "random_state": 42},
    )

    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)

    for name in ("accuracy", "precision", "recall", "f1"):
        assert name in metrics
        assert 0.0 <= metrics[name] <= 1.0

    matrix = metrics["confusion_matrix"]

    assert set(matrix) == {"tn", "fp", "fn", "tp"}
    assert sum(matrix.values()) == len(y_test)
