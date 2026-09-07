import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"
MODEL_DIR = r"E:\SmartPulse\ml\models\random_forest_new_data"

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
print("SmartPulse Random Forest Model")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
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

print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model training completed.")

print("\nMaking predictions...")

y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_probability)

print("\n" + "=" * 60)
print("RANDOM FOREST MODEL EVALUATION")
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

print("\nFeature Importance:")

importance = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

for rank, (_, row) in enumerate(importance.iterrows(), start=1):
    print(
        f"{rank}. {row['feature']:25s} "
        f"{row['importance']:.4f}"
    )

print("\nSaving Random Forest model...")

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "random_forest_failure_model.pkl"
)

joblib.dump(model, MODEL_PATH)

print("Model saved to:")
print(MODEL_PATH)

print("\n" + "=" * 60)
print("SmartPulse Random Forest training completed successfully!")
print("=" * 60)