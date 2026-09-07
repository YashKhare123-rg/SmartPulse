import os
import pandas as pd

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"
OUTPUT_PATH = r"E:\SmartPulse\ml\data\engineered_machine_data.csv"


def main():
    print("=" * 60)
    print("SmartPulse Feature Engineering")
    print("=" * 60)

    print("\nLoading validated dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully.")
    print("Original records:", len(df))
    print("Original features:", len(df.columns))

    print("\nCreating engineered features...")

    df["thermal_load"] = (
            df["temperature"] * df["load_percentage"] / 100
    )

    df["vibration_load"] = (
            df["vibration"] * df["load_percentage"] / 100
    )

    df["power_load_ratio"] = (
            df["power_consumption"] /
            df["load_percentage"].replace(0, 1)
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
            + df["load_percentage"] / 100
            + df["power_consumption"] / 10
    )

    print("Feature engineering completed.")

    print("\nNew engineered features:")

    engineered_features = [
        "thermal_load",
        "vibration_load",
        "power_load_ratio",
        "temperature_vibration_interaction",
        "temperature_pressure_interaction",
        "load_speed_interaction",
        "power_temperature_interaction",
        "overall_stress_index"
    ]

    for feature in engineered_features:
        print("-", feature)

    print("\nChecking generated features for missing values...")

    missing_values = df[engineered_features].isnull().sum()

    print(missing_values)

    if missing_values.sum() > 0:
        raise ValueError(
            "Engineered features contain missing values."
        )

    print("\nChecking generated feature statistics...")

    print(
        df[engineered_features]
        .describe()
        .round(4)
        .to_string()
    )

    print("\nSaving engineered dataset...")

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("Engineered dataset saved to:")
    print(OUTPUT_PATH)

    print("\nFinal dataset shape:")
    print("Records:", len(df))
    print("Columns:", len(df.columns))

    print("\n" + "=" * 60)
    print("SmartPulse Feature Engineering completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()