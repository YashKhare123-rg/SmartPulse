import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"
OUTPUT_DIR = r"E:\SmartPulse\ml\data\visualizations"

FEATURES = [
    "temperature",
    "vibration",
    "pressure",
    "power_consumption",
    "load_percentage",
    "rotation_speed"
]


def main():
    print("=" * 60)
    print("SmartPulse ML Data Visualization")
    print("=" * 60)

    print("\nLoading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully.")
    print("Total records:", len(df))

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for feature in FEATURES:
        print(f"\nCreating visualization for: {feature}")

        plt.figure(figsize=(10, 6))

        df[df["failure"] == 0][feature].plot(
            kind="hist",
            bins=30,
            alpha=0.6,
            label="No Failure"
        )

        df[df["failure"] == 1][feature].plot(
            kind="hist",
            bins=30,
            alpha=0.6,
            label="Failure"
        )

        plt.title(f"{feature} Distribution by Failure Status")
        plt.xlabel(feature)
        plt.ylabel("Frequency")
        plt.legend()
        plt.tight_layout()

        output_path = os.path.join(
            OUTPUT_DIR,
            f"{feature}_failure_distribution.png"
        )

        plt.savefig(output_path, dpi=150)
        plt.close()

        print("Saved:", output_path)

    print("\n" + "=" * 60)
    print("Creating correlation chart...")
    print("=" * 60)

    correlations = (
        df[FEATURES + ["failure"]]
        .corr()["failure"]
        .drop("failure")
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    correlations.plot(kind="barh")

    plt.title("Feature Correlation with Machine Failure")
    plt.xlabel("Correlation")
    plt.ylabel("Feature")
    plt.tight_layout()

    correlation_path = os.path.join(
        OUTPUT_DIR,
        "feature_failure_correlation.png"
    )

    plt.savefig(correlation_path, dpi=150)
    plt.close()

    print("Saved:", correlation_path)

    print("\n" + "=" * 60)
    print("Visualization completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()