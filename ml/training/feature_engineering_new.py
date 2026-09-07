import pandas as pd

INPUT_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"
OUTPUT_PATH = r"E:\SmartPulse\ml\data\engineered_machine_data_new.csv"

print("=" * 60)
print("SmartPulse Feature Engineering")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_PATH)

print(f"Records loaded: {len(df)}")

print("\nCreating engineered features...")

df["thermal_load"] = (
        df["temperature"] * df["load_percentage"]
)

df["vibration_load"] = (
        df["vibration"] * df["load_percentage"]
)

df["power_load_ratio"] = (
        df["power_consumption"] /
        (df["load_percentage"] + 1)
)

df["temperature_vibration_interaction"] = (
        df["temperature"] * df["vibration"]
)

df["temperature_pressure_interaction"] = (
        df["temperature"] * df["pressure"]
)

df["load_speed_interaction"] = (
        df["load_percentage"] * df["rotation_speed"]
)

df["power_temperature_interaction"] = (
        df["power_consumption"] * df["temperature"]
)

df["overall_stress_index"] = (
        df["temperature"] / 100
        + df["vibration"] / 10
        + df["pressure"] / 10
        + df["power_consumption"] / 10
        + df["load_percentage"] / 100
)

print("Feature engineering completed.")

print("\nNew features created:")

new_features = [
    "thermal_load",
    "vibration_load",
    "power_load_ratio",
    "temperature_vibration_interaction",
    "temperature_pressure_interaction",
    "load_speed_interaction",
    "power_temperature_interaction",
    "overall_stress_index"
]

for feature in new_features:
    print(f"- {feature}")

print("\nChecking missing values...")

missing_values = df.isnull().sum().sum()

if missing_values == 0:
    print("No missing values found.")
else:
    print(f"Missing values found: {missing_values}")

print("\nSaving engineered dataset...")

df.to_csv(OUTPUT_PATH, index=False)

print(f"Engineered dataset saved to:")
print(OUTPUT_PATH)

print(f"\nTotal columns: {len(df.columns)}")
print(f"Total records: {len(df)}")

print("\n" + "=" * 60)
print("Feature engineering completed successfully!")
print("=" * 60)