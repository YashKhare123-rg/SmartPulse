import pandas as pd
import joblib
import numpy as np
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

OUTPUT_PATH = r"E:\SmartPulse\ml\data\degraded_model_performance.csv"

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

print("=" * 60)
print("SmartPulse Model Drift Simulator")
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

print("\nGenerating original predictions...")

X_test_scaled = scaler.transform(X_test)

original_probability = model.predict_proba(
    X_test_scaled
)[:, 1]

print("Original predictions generated.")

print("\nSimulating model degradation...")

np.random.seed(42)

degraded_probability = original_probability.copy()

noise = np.random.normal(
    0,
    0.35,
    len(degraded_probability)
)

degraded_probability = (
        degraded_probability + noise
)

degraded_probability = np.clip(
    degraded_probability,
    0.01,
    0.99
)

degraded_prediction = (
        degraded_probability >= 0.50
).astype(int)

print("Prediction degradation simulated.")

accuracy = accuracy_score(
    y_test,
    degraded_prediction
)

precision = precision_score(
    y_test,
    degraded_prediction,
    zero_division=0
)

recall = recall_score(
    y_test,
    degraded_prediction,
    zero_division=0
)

f1 = f1_score(
    y_test,
    degraded_prediction,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    degraded_probability
)

print("\n" + "=" * 60)
print("DEGRADED MODEL PERFORMANCE")
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

    if relative_change >= 0.10:
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
    print("\nOverall Status: MODEL DRIFT DETECTED")
else:
    print("\nOverall Status: MODEL STABLE")

print("\nSaving degraded model report...")

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("Degraded model report saved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 60)
print("SmartPulse model drift simulation completed successfully!")
print("=" * 60)