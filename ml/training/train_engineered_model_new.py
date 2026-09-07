import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)
import joblib
import os

DATA_PATH = r"E:\SmartPulse\ml\data\engineered_machine_data_new.csv"
MODEL_DIR = r"E:\SmartPulse\ml\models\engineered_new_data"

FEATURES = [
    "temperature",
    "vibration",
    "pressure",
    "power_consumption",
    "operating_hours",
    "load_percentage",
    "rotation_speed",
    "maintenance_count",
    "machine_age",
    "thermal_load",
    "vibration_load",
    "power_load_ratio",
    "temperature_vibration_interaction",
    "temperature_pressure_interaction",
    "load_speed_interaction",
    "power_temperature_interaction",
    "overall_stress_index"
]

TARGET = "failure"

print("=" * 60)
print("SmartPulse Engineered ML Model")
print("=" * 60)

print("\nLoading engineered dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded successfully.")
print(f"Total records: {len(df)}")

print("\nChecking missing values...")

missing = df[FEATURES + [TARGET]].isnull().sum().sum()

if missing == 0:
    print("No missing values found.")
else:
    print(f"Missing values found: {missing}")

print("\nSelecting features...")

X = df[FEATURES]
y = df[TARGET]

print(f"Number of features: {len(FEATURES)}")

for feature in FEATURES:
    print(f"- {feature}")

print(f"\nTarget: {TARGET}")

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

print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")

print("\nScaling features...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Feature scaling completed.")

print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=2000,
    random_state=42
)

model.fit(X_train_scaled, y_train)

print("Model training completed.")

print("\nMaking predictions...")

y_pred = model.predict(X_test_scaled)
y_probability = model.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_probability)

print("\n" + "=" * 60)
print("ENGINEERED MODEL EVALUATION")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nSaving engineered model...")

os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(
    MODEL_DIR,
    "engineered_failure_prediction_model.pkl"
)

scaler_path = os.path.join(
    MODEL_DIR,
    "engineered_feature_scaler.pkl"
)

joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)

print("Model saved to:")
print(model_path)

print("Scaler saved to:")
print(scaler_path)

print("\n" + "=" * 60)
print("SmartPulse engineered ML training completed successfully!")
print("=" * 60)