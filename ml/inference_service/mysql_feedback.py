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
            FROM feedback
            ORDER BY created_at ASC \
            """

    dataframe = pd.read_sql(query, connection)

    connection.close()

    return dataframe


if __name__ == "__main__":
    feedback = load_feedback()

    print("\nFeedback loaded successfully.")
    print(f"Total records: {len(feedback)}")
    print("\nFeedback data:")
    print(feedback.to_string(index=False))