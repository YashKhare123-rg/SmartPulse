import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

MODEL_DIR = r"E:\SmartPulse\ml\models\new_data_baseline"


FEATURES = [
    "temperature",
    "vibration",
    "pressure",
    "power_consumption",
    "operating_hours",
    "load_percentage",
    "rotation_speed",
    "maintenance_count",
    "machine_age"
]

TARGET = "failure"


def main():

    print("=" * 60)
    print("SmartPulse ML Failure Prediction")
    print("=" * 60)

    print("\nLoading dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully.")
    print("Total records:", len(df))

    print("\nChecking missing values...")

    missing_values = df[FEATURES + [TARGET]].isnull().sum()

    if missing_values.sum() > 0:
        print("Missing values found:")
        print(missing_values)
        raise ValueError("Dataset contains missing values.")

    print("No missing values found.")

    print("\nSelecting features...")

    X = df[FEATURES]
    y = df[TARGET]

    print("Number of features:", len(FEATURES))

    print("Features:")

    for feature in FEATURES:
        print("-", feature)

    print("\nTarget:", TARGET)

    print("\nTarget distribution:")

    print(y.value_counts())

    print("\nSplitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("Training records:", len(X_train))
    print("Testing records:", len(X_test))

    print("\nScaling features...")

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)

    print("Feature scaling completed.")

    print("\nTraining Logistic Regression model...")

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(
        X_train_scaled,
        y_train
    )

    print("Model training completed.")

    print("\nMaking predictions...")

    y_pred = model.predict(X_test_scaled)

    y_probability = model.predict_proba(
        X_test_scaled
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred
    )

    recall = recall_score(
        y_test,
        y_pred
    )

    f1 = f1_score(
        y_test,
        y_pred
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )

    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print("\nSaving model...")

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model_path = os.path.join(
        MODEL_DIR,
        "failure_prediction_model.pkl"
    )

    scaler_path = os.path.join(
        MODEL_DIR,
        "feature_scaler.pkl"
    )

    joblib.dump(
        model,
        model_path
    )

    joblib.dump(
        scaler,
        scaler_path
    )

    print("Model saved to:")

    print(model_path)

    print("Scaler saved to:")

    print(scaler_path)

    print("\n" + "=" * 60)
    print("SmartPulse ML training completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()