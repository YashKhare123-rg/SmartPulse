import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password=input("Enter MySQL password: "),
    database="smartpulse_db"
)

cursor = connection.cursor()

cursor.execute("""
               SELECT
                   feedback_id,
                   machine_id,
                   predicted_failure_probability,
                   risk_score,
                   maintenance_action,
                   actual_outcome,
                   created_at
               FROM feedback
               ORDER BY created_at DESC
               """)

rows = cursor.fetchall()

print("\nMySQL connection successful.")
print(f"Feedback records found: {len(rows)}")

for row in rows:
    print(row)

cursor.close()
connection.close()

print("\nConnection closed.")