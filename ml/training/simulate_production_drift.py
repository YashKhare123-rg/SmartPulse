import pandas as pd
import numpy as np

INPUT_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"
OUTPUT_PATH = r"E:\SmartPulse\ml\data\simulated_production_data.csv"

print("=" * 60)
print("SmartPulse Production Drift Simulator")
print("=" * 60)

print("\nLoading reference dataset...")

df = pd.read_csv(INPUT_PATH)

print(f"Reference records loaded: {len(df)}")

production_df = df.copy()

print("\nApplying simulated production changes...")

np.random.seed(42)

production_df["temperature"] = (
        production_df["temperature"] + 12
)

production_df["power_consumption"] = (
        production_df["power_consumption"] * 1.15
)

production_df["load_percentage"] = (
        production_df["load_percentage"] + 8
)

production_df["vibration"] = (
        production_df["vibration"] * 1.10
)

production_df["pressure"] = (
        production_df["pressure"] + 0.5
)

production_df["rotation_speed"] = (
        production_df["rotation_speed"] * 1.05
)

production_df["temperature"] += (
    np.random.normal(
        0,
        1.5,
        len(production_df)
    )
)

production_df["power_consumption"] += (
    np.random.normal(
        0,
        0.15,
        len(production_df)
    )
)

production_df["load_percentage"] += (
    np.random.normal(
        0,
        2,
        len(production_df)
    )
)

production_df["vibration"] += (
    np.random.normal(
        0,
        0.1,
        len(production_df)
    )
)

production_df["pressure"] += (
    np.random.normal(
        0,
        0.1,
        len(production_df)
    )
)

production_df["rotation_speed"] += (
    np.random.normal(
        0,
        15,
        len(production_df)
    )
)

print("\nChecking production data ranges...")

production_df["load_percentage"] = (
    production_df["load_percentage"].clip(0, 100)
)

production_df["temperature"] = (
    production_df["temperature"].clip(20, 120)
)

production_df["vibration"] = (
    production_df["vibration"].clip(0.1, 15)
)

production_df["pressure"] = (
    production_df["pressure"].clip(1, 15)
)

production_df["power_consumption"] = (
    production_df["power_consumption"].clip(0.5)
)

production_df["rotation_speed"] = (
    production_df["rotation_speed"].clip(500)
)

print("Production data ranges checked.")

print("\nSaving simulated production dataset...")

production_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nProduction dataset saved to:")
print(OUTPUT_PATH)

print(f"\nTotal records: {len(production_df)}")

print("\n" + "=" * 60)
print("Production drift simulation completed successfully!")
print("=" * 60)