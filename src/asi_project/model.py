"""Model preprocessing i modele bazowe (Sprint 1).

Model preprocessing (imputacja, skalowanie, kodowanie — wszystko, co wymaga ``fit``) żyje
wewnątrz sklearn Pipeline. Dzięki temu przy predykcji wykonują się dokładnie te same kroki,
które zostały dopasowane na X_train, a cały model można zapisać jako jeden artefakt.
"""

from collections.abc import Sequence

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_dummy() -> DummyClassifier:
    """Baseline bez wiedzy o cechach: zawsze przewiduje najczęstszą klasę z X_train."""
    return DummyClassifier(strategy="most_frequent")


def build_baseline_pipeline(
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
) -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(numeric_features)),
            ("categorical", categorical_pipeline, list(categorical_features)),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
