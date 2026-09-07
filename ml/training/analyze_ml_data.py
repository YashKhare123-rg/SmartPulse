import pandas as pd

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


def main():
    print("=" * 60)
    print("SmartPulse ML Data Analysis")
    print("=" * 60)

    print("\nLoading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Total records:", len(df))

    print("\n" + "=" * 60)
    print("FAILURE DISTRIBUTION")
    print("=" * 60)

    print(df[TARGET].value_counts())
    print("\nPercentage:")
    print((df[TARGET].value_counts(normalize=True) * 100).round(2))

    print("\n" + "=" * 60)
    print("FEATURE STATISTICS")
    print("=" * 60)

    print(df[FEATURES].describe().round(2).to_string())

    print("\n" + "=" * 60)
    print("AVERAGE VALUES BY FAILURE STATUS")
    print("=" * 60)

    comparison = df.groupby(TARGET)[FEATURES].mean().round(2)

    print(comparison.to_string())

    print("\n" + "=" * 60)
    print("FEATURE CORRELATION WITH FAILURE")
    print("=" * 60)

    correlations = (
        df[FEATURES + [TARGET]]
        .corr()[TARGET]
        .drop(TARGET)
        .sort_values(key=abs, ascending=False)
    )

    print(correlations.round(4).to_string())

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    print(df[FEATURES + [TARGET]].isnull().sum())

    print("\n" + "=" * 60)
    print("ML DATA ANALYSIS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()