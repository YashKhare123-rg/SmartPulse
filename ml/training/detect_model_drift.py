import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"

OUTPUT_PATH = r"E:\SmartPulse\ml\data\model_drift_report.csv"

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

DRIFT_THRESHOLD = 0.10


print("=" * 60)
print("SmartPulse Model Drift Detection")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded: {len(df)} records")

X = df[FEATURES]
y = df[TARGET]

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")

print("\nLoading trained model...")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Model loaded successfully.")
print("Scaler loaded successfully.")

print("\nScaling test data...")

X_test_scaled = scaler.transform(X_test)

print("Scaling completed.")

print("\nGenerating predictions...")

y_pred = model.predict(X_test_scaled)
y_probability = model.predict_proba(X_test_scaled)[:, 1]

print("Predictions generated.")

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_probability)

print("\n" + "=" * 60)
print("CURRENT MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

reference_accuracy = 0.8536
reference_precision = 0.7863
reference_recall = 0.7429
reference_f1 = 0.7640
reference_roc_auc = 0.9132

print("\n" + "=" * 60)
print("REFERENCE MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy : {reference_accuracy:.4f}")
print(f"Precision: {reference_precision:.4f}")
print(f"Recall   : {reference_recall:.4f}")
print(f"F1 Score : {reference_f1:.4f}")
print(f"ROC-AUC  : {reference_roc_auc:.4f}")

metrics = {
    "accuracy": (
        reference_accuracy,
        accuracy
    ),
    "precision": (
        reference_precision,
        precision
    ),
    "recall": (
        reference_recall,
        recall
    ),
    "f1_score": (
        reference_f1,
        f1
    ),
    "roc_auc": (
        reference_roc_auc,
        roc_auc
    )
}

results = []

print("\n" + "=" * 60)
print("MODEL DRIFT ANALYSIS")
print("=" * 60)

for metric, values in metrics.items():

    reference_value = values[0]
    current_value = values[1]

    relative_change = (
            abs(current_value - reference_value)
            / reference_value
    )

    if relative_change >= DRIFT_THRESHOLD:
        status = "DRIFT"
    else:
        status = "STABLE"

    results.append({
        "metric": metric,
        "reference_value": reference_value,
        "current_value": current_value,
        "relative_change": relative_change,
        "status": status
    })

    print(
        f"{metric:15s} "
        f"Reference: {reference_value:.4f}   "
        f"Current: {current_value:.4f}   "
        f"Change: {relative_change * 100:.2f}%   "
        f"STATUS: {status}"
    )

results_df = pd.DataFrame(results)

drift_count = (
        results_df["status"] == "DRIFT"
).sum()

stable_count = (
        results_df["status"] == "STABLE"
).sum()

print("\n" + "=" * 60)
print("DRIFT SUMMARY")
print("=" * 60)

print(f"Stable metrics : {stable_count}")
print(f"Drifted metrics: {drift_count}")

if drift_count > 0:
    overall_status = "MODEL DRIFT DETECTED"
else:
    overall_status = "MODEL STABLE"

print(f"\nOverall Status: {overall_status}")

print("\nSaving model drift report...")

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("Model drift report saved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 60)
print("SmartPulse model drift detection completed successfully!")
print("=" * 60)