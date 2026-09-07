import pandas as pd

FEEDBACK_PATH = r"E:\SmartPulse\ml\data\maintenance_feedback.csv"
MODEL_DRIFT_REPORT = r"E:\SmartPulse\ml\data\model_drift_report.csv"

MINIMUM_FEEDBACK_RECORDS = 20
MINIMUM_FAILURE_RECORDS = 3
MAXIMUM_FALSE_NEGATIVE_RATE = 0.10


def main():

    print("=" * 80)
    print("SMARTPULSE 2.0 - INTELLIGENT RETRAINING TRIGGER")
    print("=" * 80)

    feedback = pd.read_csv(FEEDBACK_PATH)
    model_drift = pd.read_csv(MODEL_DRIFT_REPORT)

    total_records = len(feedback)

    actual_failures = feedback[
        feedback["actual_failure"] == True
        ]

    false_negatives = 0

    for _, row in feedback.iterrows():

        predicted_probability = row[
            "predicted_failure_probability"
        ]

        actual_failure = bool(
            row["actual_failure"]
        )

        predicted_failure = predicted_probability >= 0.50

        if not predicted_failure and actual_failure:
            false_negatives += 1

    if len(actual_failures) > 0:
        false_negative_rate = (
                false_negatives / len(actual_failures)
        )
    else:
        false_negative_rate = 0

    model_drift_detected = (
            "DRIFT" in model_drift["status"].values
    )

    enough_feedback = (
            total_records >= MINIMUM_FEEDBACK_RECORDS
    )

    enough_failures = (
            len(actual_failures) >= MINIMUM_FAILURE_RECORDS
    )

    excessive_false_negatives = (
            false_negative_rate > MAXIMUM_FALSE_NEGATIVE_RATE
    )

    print("\nCURRENT FEEDBACK STATUS")
    print("-" * 80)

    print(
        f"Feedback Records       : "
        f"{total_records}"
    )

    print(
        f"Actual Failures        : "
        f"{len(actual_failures)}"
    )

    print(
        f"False Negatives        : "
        f"{false_negatives}"
    )

    print(
        f"False Negative Rate    : "
        f"{false_negative_rate * 100:.2f}%"
    )

    print(
        f"Model Drift Detected   : "
        f"{model_drift_detected}"
    )

    print("\nRETRAINING CONDITIONS")
    print("-" * 80)

    print(
        f"Minimum Feedback       : "
        f"{MINIMUM_FEEDBACK_RECORDS}"
    )

    print(
        f"Minimum Failures       : "
        f"{MINIMUM_FAILURE_RECORDS}"
    )

    print(
        f"Maximum False Negative : "
        f"{MAXIMUM_FALSE_NEGATIVE_RATE * 100:.2f}%"
    )

    print("\nCONDITION CHECK")
    print("-" * 80)

    print(
        f"Enough Feedback        : "
        f"{enough_feedback}"
    )

    print(
        f"Enough Failures        : "
        f"{enough_failures}"
    )

    print(
        f"Excessive False Negatives: "
        f"{excessive_false_negatives}"
    )

    print(
        f"Model Drift            : "
        f"{model_drift_detected}"
    )

    retraining_required = False
    reason = ""

    if not enough_feedback:

        reason = (
            "Insufficient feedback data. "
            "Collect more operational outcomes before retraining."
        )

    elif not enough_failures:

        reason = (
            "Insufficient failure examples. "
            "More failure outcomes are required."
        )

    elif excessive_false_negatives:

        retraining_required = True

        reason = (
            "False negative rate exceeds the allowed threshold."
        )

    elif model_drift_detected:

        retraining_required = True

        reason = (
            "Model drift has been detected."
        )

    else:

        reason = (
            "Current evidence does not justify retraining."
        )

    print("\nRETRAINING DECISION")
    print("-" * 80)

    if retraining_required:

        print("Retraining Required : YES")

    else:

        print("Retraining Required : NO")

    print(f"Reason              : {reason}")

    print("\n" + "=" * 80)
    print("RETRAINING TRIGGER ANALYSIS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()