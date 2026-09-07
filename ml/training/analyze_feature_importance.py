import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

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
print("SmartPulse Feature Importance Analysis")
print("=" * 60)

print("\nLoading dataset...")
df = pd.read_csv(DATA_PATH)

print(f"Total records: {len(df)}")

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nScaling features...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

print("Feature scaling completed.")

print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train_scaled, y_train)

print("Model training completed.")

importance = pd.DataFrame({
    "feature": FEATURES,
    "coefficient": model.coef_[0],
    "absolute_importance": abs(model.coef_[0])
})

importance = importance.sort_values(
    by="absolute_importance",
    ascending=False
)

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

for _, row in importance.iterrows():
    direction = "INCREASES failure risk" if row["coefficient"] > 0 else "DECREASES failure risk"

    print(
        f"{row['feature']:25s} "
        f"Coefficient: {row['coefficient']:8.4f}   "
        f"{direction}"
    )

print("\n" + "=" * 60)
print("RANKING")
print("=" * 60)

for rank, (_, row) in enumerate(importance.iterrows(), start=1):
    print(
        f"{rank}. {row['feature']} "
        f"(importance = {row['absolute_importance']:.4f})"
    )

print("\nCreating feature importance chart...")

plt.figure(figsize=(10, 6))

plt.barh(
    importance["feature"],
    importance["absolute_importance"]
)

plt.xlabel("Absolute Model Coefficient")
plt.ylabel("Feature")
plt.title("SmartPulse Feature Importance")

plt.gca().invert_yaxis()

plt.tight_layout()

OUTPUT_PATH = r"E:\SmartPulse\ml\data\feature_importance.png"

plt.savefig(OUTPUT_PATH, dpi=300)

print(f"\nChart saved to:")
print(OUTPUT_PATH)

print("\nFeature importance analysis completed successfully!")