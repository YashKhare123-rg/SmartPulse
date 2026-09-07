import pandas as pd
import numpy as np
import os

REFERENCE_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"
CURRENT_PATH = r"E:\SmartPulse\ml\data\simulated_production_data.csv"

OUTPUT_PATH = r"E:\SmartPulse\ml\data\data_drift_report.csv"

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

PSI_STABLE = 0.10
PSI_WARNING = 0.20


def calculate_psi(reference, current, bins=10):

    reference = np.asarray(reference)
    current = np.asarray(current)

    breakpoints = np.percentile(
        reference,
        np.linspace(0, 100, bins + 1)
    )

    breakpoints = np.unique(breakpoints)

    if len(breakpoints) < 3:
        return 0.0

    reference_counts, _ = np.histogram(
        reference,
        bins=breakpoints
    )

    current_counts, _ = np.histogram(
        current,
        bins=breakpoints
    )

    reference_percentages = (
            reference_counts / len(reference)
    )

    current_percentages = (
            current_counts / len(current)
    )

    reference_percentages = np.where(
        reference_percentages == 0,
        0.0001,
        reference_percentages
    )

    current_percentages = np.where(
        current_percentages == 0,
        0.0001,
        current_percentages
    )

    psi = np.sum(
        (
                current_percentages
                - reference_percentages
        )
        *
        np.log(
            current_percentages
            / reference_percentages
        )
    )

    return psi


print("=" * 60)
print("SmartPulse Data Drift Detection")
print("=" * 60)

print("\nLoading reference dataset...")

reference_df = pd.read_csv(REFERENCE_PATH)

print(
    f"Reference records: {len(reference_df)}"
)

print("\nLoading current dataset...")

current_df = pd.read_csv(CURRENT_PATH)

print(
    f"Current records: {len(current_df)}"
)

print("\nCalculating Population Stability Index (PSI)...")

results = []

for feature in FEATURES:

    reference_values = reference_df[feature].dropna()
    current_values = current_df[feature].dropna()

    psi = calculate_psi(
        reference_values,
        current_values
    )

    if psi < PSI_STABLE:
        status = "STABLE"
    elif psi < PSI_WARNING:
        status = "WARNING"
    else:
        status = "DRIFT"

    results.append({
        "feature": feature,
        "psi": psi,
        "status": status
    })

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="psi",
    ascending=False
)

print("\n" + "=" * 60)
print("DATA DRIFT REPORT")
print("=" * 60)

for _, row in results_df.iterrows():

    print(
        f"{row['feature']:25s} "
        f"PSI: {row['psi']:.4f}   "
        f"STATUS: {row['status']}"
    )

print("\n" + "=" * 60)
print("DRIFT SUMMARY")
print("=" * 60)

stable_count = (
        results_df["status"] == "STABLE"
).sum()

warning_count = (
        results_df["status"] == "WARNING"
).sum()

drift_count = (
        results_df["status"] == "DRIFT"
).sum()

print(f"Stable features : {stable_count}")
print(f"Warning features: {warning_count}")
print(f"Drifted features: {drift_count}")

if drift_count > 0:
    print("\nOverall Status: DRIFT DETECTED")
elif warning_count > 0:
    print("\nOverall Status: WARNING")
else:
    print("\nOverall Status: STABLE")

print("\nSaving drift report...")

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("Drift report saved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 60)
print("SmartPulse drift detection completed successfully!")
print("=" * 60)