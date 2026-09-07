import pandas as pd

FEEDBACK_PATH = r"E:\SmartPulse\ml\data\maintenance_feedback.csv"


def main():

    print("=" * 80)
    print("SMARTPULSE 2.0 - FEEDBACK PERFORMANCE ANALYZER")
    print("=" * 80)

    df = pd.read_csv(FEEDBACK_PATH)

    if df.empty:
        print("\nNo feedback records available.")
        return

    total_records = len(df)

    correct_predictions = 0
    false_positives = 0
    false_negatives = 0
    true_positives = 0
    true_negatives = 0

    for _, row in df.iterrows():

        predicted_probability = row[
            "predicted_failure_probability"
        ]

        actual_failure = bool(
            row["actual_failure"]
        )

        predicted_failure = predicted_probability >= 0.50

        if predicted_failure and actual_failure:
            true_positives += 1
        elif predicted_failure and not actual_failure:
            false_positives += 1
        elif not predicted_failure and actual_failure:
            false_negatives += 1
        else:
            true_negatives += 1

    correct_predictions = (
            true_positives + true_negatives
    )

    accuracy = (
            correct_predictions / total_records
    )

    if true_positives + false_positives > 0:
        precision = (
                true_positives
                / (true_positives + false_positives)
        )
    else:
        precision = 0

    if true_positives + false_negatives > 0:
        recall = (
                true_positives
                / (true_positives + false_negatives)
        )
    else:
        recall = 0

    maintenance_records = df[
        df["maintenance_performed"] == True
        ]

    successful_maintenance = maintenance_records[
        maintenance_records["actual_failure"] == False
        ]

    if len(maintenance_records) > 0:
        maintenance_success_rate = (
                len(successful_maintenance)
                / len(maintenance_records)
        )
    else:
        maintenance_success_rate = 0

    failure_records = df[
        df["actual_failure"] == True
        ]

    if len(failure_records) > 0:
        average_failure_probability = (
            failure_records[
                "predicted_failure_probability"
            ].mean()
        )
    else:
        average_failure_probability = 0

    non_failure_records = df[
        df["actual_failure"] == False
        ]

    if len(non_failure_records) > 0:
        average_non_failure_probability = (
            non_failure_records[
                "predicted_failure_probability"
            ].mean()
        )
    else:
        average_non_failure_probability = 0

    print("\nFEEDBACK DATASET")
    print("-" * 80)

    print(f"Total Feedback Records : {total_records}")

    print("\nPREDICTION PERFORMANCE")
    print("-" * 80)

    print(
        f"Correct Predictions   : "
        f"{correct_predictions}"
    )

    print(
        f"True Positives        : "
        f"{true_positives}"
    )

    print(
        f"True Negatives        : "
        f"{true_negatives}"
    )

    print(
        f"False Positives       : "
        f"{false_positives}"
    )

    print(
        f"False Negatives       : "
        f"{false_negatives}"
    )

    print(
        f"Accuracy              : "
        f"{accuracy * 100:.2f}%"
    )

    print(
        f"Precision             : "
        f"{precision * 100:.2f}%"
    )

    print(
        f"Recall                : "
        f"{recall * 100:.2f}%"
    )

    print("\nMAINTENANCE PERFORMANCE")
    print("-" * 80)

    print(
        f"Maintenance Actions   : "
        f"{len(maintenance_records)}"
    )

    print(
        f"Successful Maintenance: "
        f"{len(successful_maintenance)}"
    )

    print(
        f"Maintenance Success   : "
        f"{maintenance_success_rate * 100:.2f}%"
    )

    print("\nFAILURE ANALYSIS")
    print("-" * 80)

    print(
        f"Actual Failures       : "
        f"{len(failure_records)}"
    )

    print(
        f"Average Failure Risk  : "
        f"{average_failure_probability * 100:.2f}%"
    )

    print(
        f"Average Non-Failure Risk: "
        f"{average_non_failure_probability * 100:.2f}%"
    )

    print("\nMODEL LEARNING SIGNAL")
    print("-" * 80)

    if false_negatives > 0:
        print(
            "WARNING: False negatives detected."
        )
        print(
            "The model missed one or more failures."
        )
        print(
            "Additional training data should be considered."
        )

    elif false_positives > true_positives:
        print(
            "WARNING: High number of false positives."
        )
        print(
            "The model may be predicting excessive failure risk."
        )

    else:
        print(
            "Feedback performance is currently acceptable."
        )

    print("\n" + "=" * 80)
    print("FEEDBACK ANALYSIS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()