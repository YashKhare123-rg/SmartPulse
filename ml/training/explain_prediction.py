import pandas as pd
import numpy as np
import joblib

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"
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

print("=" * 60)
print("SmartPulse Explainable AI")
print("=" * 60)

print("\nLoading trained model...")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Model loaded successfully.")
print("Scaler loaded successfully.")

print("\nLoading machine dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded: {len(df)} records")

print("\nSelecting sample machine record...")

sample = df.iloc[0]

machine_data = sample[FEATURES].to_frame().T

print(f"Machine ID: {sample['machine_id']}")
print(f"Actual Failure: {int(sample['failure'])}")

print("\nMachine sensor values:")

for feature in FEATURES:
    print(f"{feature:25s}: {sample[feature]:.4f}")

print("\nScaling machine data...")

scaled_data = scaler.transform(machine_data)

print("Scaling completed.")

print("\nMaking prediction...")

prediction = model.predict(scaled_data)[0]
failure_probability = model.predict_proba(scaled_data)[0][1]

print("\n" + "=" * 60)
print("PREDICTION")
print("=" * 60)

print(f"Machine ID       : {sample['machine_id']}")
print(f"Failure Prediction: {'FAILURE' if prediction == 1 else 'NO FAILURE'}")
print(f"Failure Probability: {failure_probability * 100:.2f}%")

print("\nCalculating feature contributions...")

coefficients = model.coef_[0]

contributions = scaled_data[0] * coefficients

explanation = pd.DataFrame({
    "feature": FEATURES,
    "value": machine_data.iloc[0].values,
    "scaled_value": scaled_data[0],
    "coefficient": coefficients,
    "contribution": contributions,
    "absolute_contribution": np.abs(contributions)
})

explanation = explanation.sort_values(
    by="absolute_contribution",
    ascending=False
)

print("\n" + "=" * 60)
print("FEATURE CONTRIBUTIONS")
print("=" * 60)

for _, row in explanation.iterrows():

    if row["contribution"] > 0:
        effect = "INCREASES failure risk"
    elif row["contribution"] < 0:
        effect = "DECREASES failure risk"
    else:
        effect = "NO EFFECT"

    print(
        f"{row['feature']:25s} "
        f"Value: {row['value']:10.3f} "
        f"Contribution: {row['contribution']:9.4f} "
        f"{effect}"
    )

print("\n" + "=" * 60)
print("TOP RISK FACTORS")
print("=" * 60)

risk_factors = explanation[
    explanation["contribution"] > 0
    ].head(5)

for rank, (_, row) in enumerate(risk_factors.iterrows(), start=1):

    print(
        f"{rank}. {row['feature']} "
        f"(contribution: {row['contribution']:.4f})"
    )

print("\n" + "=" * 60)
print("XAI ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)