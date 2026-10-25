from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from features import extract_features


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "phishing_urls.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "phishguard_model.joblib"


def prepare_dataset():
    """Load the CSV and prepare URL features and labels."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    data = pd.read_csv(DATASET_PATH)

    # Standardize column names.
    data.columns = [
        str(column).strip().lower() for column in data.columns
    ]

    # Find the URL column.
    url_candidates = ["url", "urls", "website", "domain"]
    url_column = next(
        (column for column in url_candidates if column in data.columns),
        None,
    )

    # Find the label column.
    label_candidates = [
        "label", "verdict", "status", "type", "class", "result"
    ]
    label_column = next(
        (column for column in label_candidates if column in data.columns),
        None,
    )

    if url_column is None or label_column is None:
        raise ValueError(
            f"Could not identify URL and label columns. "
            f"Available columns: {list(data.columns)}"
        )

    data = data[[url_column, label_column]].dropna()
    data.columns = ["url", "label"]

    # Convert supported labels to our convention:
    # 0 = legitimate, 1 = phishing.
    def convert_label(value):
        normalized = str(value).strip().lower()

        label_mapping = {
            "0": 0,
            "1": 1,
            "legitimate": 0,
            "benign": 0,
            "safe": 0,
            "good": 0,
            "phishing": 1,
            "phish": 1,
            "malicious": 1,
            "bad": 1,
        }

        if normalized in label_mapping:
            return label_mapping[normalized]

        raise ValueError(
            f"Unsupported label '{value}'. "
            "Inspect the dataset labels and update convert_label()."
        )

    data["label"] = data["label"].apply(convert_label)

    # Remove duplicate URLs and empty values.
    data["url"] = data["url"].astype(str).str.strip()
    data = data[data["url"] != ""]
    data = data.drop_duplicates(subset=["url"])

    if data["label"].nunique() != 2:
        raise ValueError(
            "The dataset must contain both legitimate and phishing examples."
        )

    print("\nDataset loaded successfully!")
    print(f"Total URLs: {len(data)}")
    print("\nClass distribution:")
    print(data["label"].map({
        0: "Legitimate",
        1: "Phishing",
    }).value_counts())

    return data


def train_model():
    """Extract features, train the classifier, and evaluate it."""

    data = prepare_dataset()

    print("\nExtracting URL features...")

    feature_rows = [
        extract_features(url)
        for url in data["url"]
    ]

    X = pd.DataFrame(feature_rows)
    y = data["label"]

    # Keep unseen examples aside for evaluation.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"Training examples: {len(X_train)}")
    print(f"Testing examples: {len(X_test)}")

    # Train the Random Forest classifier.
    print("\nTraining Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # Evaluate on held-out examples.
    predictions = model.predict(X_test)

    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Legitimate", "Phishing"],
            zero_division=0,
        )
    )

    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions,
            labels=[0, 1],
        )
    )

    # Save the trained model.
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved successfully at:\n{MODEL_PATH}")


if __name__ == "__main__":
    train_model()