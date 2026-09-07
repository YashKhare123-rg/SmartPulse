import pandas as pd
import joblib

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"

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
print("SmartPulse Decision & Recommendation Engine")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded: {len(df)} records")

print("\nLoading ML model...")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Model loaded successfully.")
print("Scaler loaded successfully.")

print("\nSelecting machine record...")

sample = df.iloc[0]

machine_data = sample[FEATURES].to_frame().T

scaled_data = scaler.transform(machine_data)

failure_probability = model.predict_proba(
    scaled_data
)[0][1]

print(f"Machine ID: {sample['machine_id']}")

print("\nMachine condition:")

print(f"Temperature       : {sample['temperature']:.2f}")
print(f"Vibration         : {sample['vibration']:.2f}")
print(f"Pressure          : {sample['pressure']:.2f}")
print(f"Power Consumption : {sample['power_consumption']:.2f}")
print(f"Load Percentage   : {sample['load_percentage']:.2f}%")
print(f"Operating Hours   : {sample['operating_hours']:.2f}")
print(f"Machine Age       : {sample['machine_age']}")
print(f"Maintenance Count : {sample['maintenance_count']}")

print("\nFailure probability:")
print(f"{failure_probability * 100:.2f}%")

if failure_probability < 0.30:

    risk_level = "LOW"
    recommendation = "Continue normal operation."
    priority = "LOW"

elif failure_probability < 0.60:

    risk_level = "MEDIUM"
    recommendation = "Schedule routine inspection."
    priority = "MEDIUM"

elif failure_probability < 0.80:

    risk_level = "HIGH"
    recommendation = "Schedule preventive maintenance soon."
    priority = "HIGH"

else:

    risk_level = "CRITICAL"
    recommendation = "Perform immediate inspection and consider controlled shutdown."
    priority = "CRITICAL"

print("\n" + "=" * 60)
print("DECISION")
print("=" * 60)

print(f"Risk Level      : {risk_level}")
print(f"Priority        : {priority}")
print(f"Recommendation  : {recommendation}")

print("\n" + "=" * 60)
print("Decision engine completed successfully!")
print("=" * 60)