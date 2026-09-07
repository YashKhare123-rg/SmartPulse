import mysql.connector
import pandas as pd


def load_feedback():
    password = input("Enter MySQL password: ")

    connection = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password=password,
        database="smartpulse_db"
    )

    query = """
            SELECT
                feedback_id,
                machine_id,
                predicted_failure_probability,
                risk_score,
                maintenance_action,
                actual_outcome,
                created_at
            FROM feedback \
            """

    dataframe = pd.read_sql(query, connection)

    connection.close()

    return dataframe


def test_trigger():

    feedback = load_feedback()

    print("\nCURRENT DATABASE FEEDBACK")
    print("=" * 80)

    print(f"Total records: {len(feedback)}")

    actual_failures = feedback[
        feedback["actual_outcome"].isin([
            "MAINTENANCE_FAILED",
            "FAILURE_OCCURRED"
        ])
    ]

    print(
        f"Actual failures: "
        f"{len(actual_failures)}"
    )

    print("\nTESTING RETRAINING CONDITIONS")
    print("=" * 80)

    simulated_total_records = 20
    simulated_failures = 3

    simulated_failure_rate = (
                                     simulated_failures /
                                     simulated_total_records
                             ) * 100

    enough_feedback = (
            simulated_total_records >= 20
    )

    enough_failures = (
            simulated_failures >= 3
    )

    excessive_failure_rate = (
            simulated_failure_rate > 10
    )

    retraining_required = (
            enough_feedback
            and enough_failures
            and excessive_failure_rate
    )

    print(
        f"Simulated feedback records : "
        f"{simulated_total_records}"
    )

    print(
        f"Simulated failure records  : "
        f"{simulated_failures}"
    )

    print(
        f"Simulated failure rate     : "
        f"{simulated_failure_rate:.2f}%"
    )

    print(
        f"Enough feedback            : "
        f"{enough_feedback}"
    )

    print(
        f"Enough failures            : "
        f"{enough_failures}"
    )

    print(
        f"Excessive failure rate     : "
        f"{excessive_failure_rate}"
    )

    print("\nRETRAINING DECISION")
    print("=" * 80)

    print(
        f"Retraining Required : "
        f"{retraining_required}"
    )

    if retraining_required:
        print(
            "Reason              : "
            "Feedback indicates model retraining is required."
        )
    else:
        print(
            "Reason              : "
            "Retraining conditions were not satisfied."
        )


if __name__ == "__main__":
    test_trigger()