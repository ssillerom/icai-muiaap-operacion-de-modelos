from pathlib import Path

import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

FEATURES = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
]
TARGET = "quality"
RANDOM_STATE = 42
VALIDATION_SIZE = 0.15


def load_dataset(path: Path) -> pd.DataFrame:
    dataset = pd.read_csv(path)
    required_columns = [*FEATURES, TARGET]
    missing_columns = [
        column for column in required_columns if column not in dataset.columns
    ]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Faltan columnas obligatorias: {missing}")
    return dataset


def train_and_evaluate(path: Path) -> dict[str, object]:
    dataset = load_dataset(path)
    features = dataset[FEATURES]
    target = dataset[TARGET]
    train_features, validation_features, train_target, validation_target = (
        train_test_split(
            features,
            target,
            test_size=VALIDATION_SIZE,
            random_state=RANDOM_STATE,
            stratify=target,
        )
    )

    model = ExtraTreesClassifier(
        n_estimators=300,
        max_features=1.0,
        min_samples_leaf=1,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(train_features, train_target)
    predictions = model.predict(validation_features)

    return {
        "rows": len(dataset),
        "features": len(FEATURES),
        "classes": sorted(target.unique().tolist()),
        "validation_f1_macro": f1_score(
            validation_target,
            predictions,
            average="macro",
            zero_division=0,
        ),
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    metrics = train_and_evaluate(project_root / "data" / "raw" / "WineQT.csv")

    print(f"Filas: {metrics['rows']}")
    print(f"Variables: {metrics['features']}")
    print(f"Clases: {len(metrics['classes'])}")
    print(f"F1 macro: {metrics['validation_f1_macro']:.4f}")


if __name__ == "__main__":
    main()
