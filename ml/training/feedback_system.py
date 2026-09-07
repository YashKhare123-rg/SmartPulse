import pandas as pd
import os
from datetime import datetime

FEEDBACK_PATH = r"E:\SmartPulse\ml\data\maintenance_feedback.csv"


def initialize_feedback_file():

    if not os.path.exists(FEEDBACK_PATH):

        columns = [
            "timestamp",
            "machine_id",
            "predicted_failure_probability",
            "predicted_risk_level",
            "recommended_action",
            "maintenance_performed",
            "actual_failure",
            "actual_outcome"
        ]

        df = pd.DataFrame(columns=columns)

        df.to_csv(
            FEEDBACK_PATH,
            index=False
        )


def add_feedback(
        machine_id,
        predicted_probability,
        risk_level,
        recommended_action,
        maintenance_performed,
        actual_failure,
        actual_outcome
):

    feedback = pd.DataFrame([
        {
            "timestamp": datetime.now().isoformat(),
            "machine_id": machine_id,
            "predicted_failure_probability": predicted_probability,
            "predicted_risk_level": risk_level,
            "recommended_action": recommended_action,
            "maintenance_performed": maintenance_performed,
            "actual_failure": actual_failure,
            "actual_outcome": actual_outcome
        }
    ])

    feedback.to_csv(
        FEEDBACK_PATH,
        mode="a",
        header=False,
        index=False
    )


def display_feedback():

    df = pd.read_csv(FEEDBACK_PATH)

    print("\n" + "=" * 80)
    print("SMARTPULSE 2.0 - MACHINE FEEDBACK SYSTEM")
    print("=" * 80)

    print(f"\nTotal feedback records: {len(df)}")

    if len(df) == 0:
        print("\nNo feedback records available.")
        return

    print("\nRECENT FEEDBACK")
    print("-" * 80)

    print(
        df.tail(10).to_string(index=False)
    )

    print("\n" + "=" * 80)


def main():

    initialize_feedback_file()

    print("=" * 80)
    print("SMARTPULSE 2.0 - ML FEEDBACK & SELF-LEARNING SYSTEM")
    print("=" * 80)

    add_feedback(
        machine_id="M001",
        predicted_probability=0.0920,
        risk_level="LOW",
        recommended_action="CONTINUE NORMAL OPERATION",
        maintenance_performed=False,
        actual_failure=False,
        actual_outcome="Machine operated normally"
    )

    add_feedback(
        machine_id="M002",
        predicted_probability=0.6840,
        risk_level="HIGH",
        recommended_action="URGENT MAINTENANCE",
        maintenance_performed=True,
        actual_failure=False,
        actual_outcome="Maintenance completed successfully"
    )

    add_feedback(
        machine_id="M003",
        predicted_probability=0.8730,
        risk_level="CRITICAL",
        recommended_action="EMERGENCY ACTION",
        maintenance_performed=True,
        actual_failure=True,
        actual_outcome="Failure occurred before maintenance completion"
    )

    display_feedback()


if __name__ == "__main__":
    main()