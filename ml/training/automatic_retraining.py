import pandas as pd
import joblib
import os
import mysql.connector
import sys

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


DATA_PATH = (
    r"E:\SmartPulse\data\processed\valid_machine_data.csv"
)

CURRENT_MODEL_PATH = (
    r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
)

CURRENT_SCALER_PATH = (
    r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"
)

MODEL_DRIFT_REPORT = (
    r"E:\SmartPulse\ml\data\model_drift_report.csv"
)

RETRAINED_MODEL_DIR = (
    r"E:\SmartPulse\ml\models\retrained_model"
)

BACKUP_MODEL_DIR = (
    r"E:\SmartPulse\ml\models\model_backup"
)


MINIMUM_FEEDBACK_RECORDS = 20
MINIMUM_FAILURE_RECORDS = 3
MAXIMUM_FALSE_NEGATIVE_RATE = 0.10

ROC_AUC_MIN_IMPROVEMENT = 0.01
MAX_RECALL_DECREASE = 0.02
MAX_F1_DECREASE = 0.02
MAX_PRECISION_DECREASE = 0.05


TEST_MODE = "--test" in sys.argv


def load_feedback_from_mysql():

    password = os.getenv("SMARTPULSE_DB_PASSWORD")

    if not password:
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
            ORDER BY created_at ASC
            """

    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return pd.DataFrame(rows)


def calculate_metrics(y_true, y_pred, y_probability):

    return {
        "accuracy": accuracy_score(
            y_true,
            y_pred
        ),

        "precision": precision_score(
            y_true,
            y_pred,
            zero_division=0
        ),

        "recall": recall_score(
            y_true,
            y_pred,
            zero_division=0
        ),

        "f1": f1_score(
            y_true,
            y_pred,
            zero_division=0
        ),

        "roc_auc": roc_auc_score(
            y_true,
            y_probability
        )
    }


def check_retraining_trigger():

    feedback = load_feedback_from_mysql()

    model_drift = pd.read_csv(
        MODEL_DRIFT_REPORT
    )

    total_records = len(feedback)

    actual_failures = feedback[
        feedback["actual_outcome"].isin([
            "MAINTENANCE_FAILED",
            "FAILURE_OCCURRED"
        ])
    ]

    false_negatives = 0

    for _, row in feedback.iterrows():

        predicted_probability = (
            row["predicted_failure_probability"]
        )

        actual_failure = (
                row["actual_outcome"]
                in [
                    "MAINTENANCE_FAILED",
                    "FAILURE_OCCURRED"
                ]
        )

        predicted_failure = (
                predicted_probability >= 0.50
        )

        if not predicted_failure and actual_failure:
            false_negatives += 1

    if len(actual_failures) > 0:

        false_negative_rate = (
                false_negatives /
                len(actual_failures)
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
            false_negative_rate >
            MAXIMUM_FALSE_NEGATIVE_RATE
    )

    if TEST_MODE:

        print("\nTEST MODE ENABLED")

        print(
            "Real MySQL feedback will NOT be modified."
        )

        print(
            "The retraining pipeline will be simulated."
        )

        return (
            True,
            "Controlled retraining test requested."
        )

    if not enough_feedback:

        return (
            False,
            "Insufficient feedback data."
        )

    if not enough_failures:

        return (
            False,
            "Insufficient failure examples."
        )

    if excessive_false_negatives:

        return (
            True,
            "False negative rate exceeded threshold."
        )

    if model_drift_detected:

        return (
            True,
            "Model drift detected."
        )

    return (
        False,
        "Current evidence does not justify retraining."
    )


def promote_new_model(new_model_path, new_scaler_path):

    os.makedirs(
        BACKUP_MODEL_DIR,
        exist_ok=True
    )

    backup_model_path = os.path.join(
        BACKUP_MODEL_DIR,
        "failure_prediction_model_backup.pkl"
    )

    backup_scaler_path = os.path.join(
        BACKUP_MODEL_DIR,
        "feature_scaler_backup.pkl"
    )

    print("Creating backup of active model...")

    joblib.dump(
        joblib.load(CURRENT_MODEL_PATH),
        backup_model_path
    )

    joblib.dump(
        joblib.load(CURRENT_SCALER_PATH),
        backup_scaler_path
    )

    if not os.path.exists(backup_model_path):

        raise RuntimeError(
            "Model backup verification failed. "
            "Active model will not be replaced."
        )

    if not os.path.exists(backup_scaler_path):

        raise RuntimeError(
            "Scaler backup verification failed. "
            "Active scaler will not be replaced."
        )

    print("Backup verification successful.")

    print("Loading accepted model...")

    new_model = joblib.load(
        new_model_path
    )

    new_scaler = joblib.load(
        new_scaler_path
    )

    print("Promoting accepted model...")

    joblib.dump(
        new_model,
        CURRENT_MODEL_PATH
    )

    joblib.dump(
        new_scaler,
        CURRENT_SCALER_PATH
    )

    return (
        backup_model_path,
        backup_scaler_path
    )


def main():

    print("=" * 80)

    print(
        "SMARTPULSE 2.0 - "
        "SELF-HEALING RETRAINING PIPELINE"
    )

    print("=" * 80)

    if TEST_MODE:

        print("\n*** SAFE TEST MODE ***")

        print(
            "No fake feedback will be inserted."
        )

        print(
            "The active baseline model will not be overwritten."
        )

    print("\nSTEP 1 - RETRAINING TRIGGER")

    print("-" * 80)

    retraining_required, reason = (
        check_retraining_trigger()
    )

    print(
        f"Retraining Required : "
        f"{retraining_required}"
    )

    print(
        f"Reason              : "
        f"{reason}"
    )

    if not retraining_required:

        print(
            "\nNo retraining will be performed."
        )

        print(
            "The current model remains active."
        )

        print(
            "\n" + "=" * 80
        )

        print(
            "SELF-HEALING PIPELINE COMPLETED"
        )

        print("=" * 80)

        return

    print("\nSTEP 2 - LOADING DATA")

    print("-" * 80)

    data = pd.read_csv(
        DATA_PATH
    )

    features = [
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

    X = data[features]

    y = data["failure"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )

    print(
        f"Training Records : "
        f"{len(X_train)}"
    )

    print(
        f"Testing Records  : "
        f"{len(X_test)}"
    )

    print("\nSTEP 3 - EVALUATING CURRENT MODEL")

    print("-" * 80)

    current_model = joblib.load(
        CURRENT_MODEL_PATH
    )

    current_scaler = joblib.load(
        CURRENT_SCALER_PATH
    )

    X_test_scaled = (
        current_scaler.transform(X_test)
    )

    current_probability = (
        current_model.predict_proba(
            X_test_scaled
        )[:, 1]
    )

    current_prediction = (
            current_probability >= 0.50
    ).astype(int)

    current_metrics = calculate_metrics(
        y_test,
        current_prediction,
        current_probability
    )

    print(
        f"Accuracy  : "
        f"{current_metrics['accuracy']:.4f}"
    )

    print(
        f"Precision : "
        f"{current_metrics['precision']:.4f}"
    )

    print(
        f"Recall    : "
        f"{current_metrics['recall']:.4f}"
    )

    print(
        f"F1 Score  : "
        f"{current_metrics['f1']:.4f}"
    )

    print(
        f"ROC-AUC   : "
        f"{current_metrics['roc_auc']:.4f}"
    )

    print("\nSTEP 4 - TRAINING NEW MODEL")

    print("-" * 80)

    new_scaler = StandardScaler()

    X_train_scaled = (
        new_scaler.fit_transform(X_train)
    )

    X_test_new_scaled = (
        new_scaler.transform(X_test)
    )

    new_model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    new_model.fit(
        X_train_scaled,
        y_train
    )

    new_probability = (
        new_model.predict_proba(
            X_test_new_scaled
        )[:, 1]
    )

    new_prediction = (
            new_probability >= 0.50
    ).astype(int)

    new_metrics = calculate_metrics(
        y_test,
        new_prediction,
        new_probability
    )

    print(
        f"Accuracy  : "
        f"{new_metrics['accuracy']:.4f}"
    )

    print(
        f"Precision : "
        f"{new_metrics['precision']:.4f}"
    )

    print(
        f"Recall    : "
        f"{new_metrics['recall']:.4f}"
    )

    print(
        f"F1 Score  : "
        f"{new_metrics['f1']:.4f}"
    )

    print(
        f"ROC-AUC   : "
        f"{new_metrics['roc_auc']:.4f}"
    )

    print("\nSTEP 5 - MODEL COMPARISON")

    print("-" * 80)

    for metric in current_metrics:

        change = (
                new_metrics[metric]
                - current_metrics[metric]
        )

        print(
            f"{metric.upper():10} : "
            f"{change * 100:+.2f}%"
        )

    roc_auc_improvement = (
            new_metrics["roc_auc"]
            - current_metrics["roc_auc"]
    )

    recall_change = (
            new_metrics["recall"]
            - current_metrics["recall"]
    )

    f1_change = (
            new_metrics["f1"]
            - current_metrics["f1"]
    )

    precision_change = (
            new_metrics["precision"]
            - current_metrics["precision"]
    )

    new_model_is_better = (
            roc_auc_improvement >= ROC_AUC_MIN_IMPROVEMENT
            and
            recall_change >= -MAX_RECALL_DECREASE
            and
            f1_change >= -MAX_F1_DECREASE
            and
            precision_change >= -MAX_PRECISION_DECREASE
    )

    print("\nMODEL ACCEPTANCE RULES")

    print("-" * 80)

    print(
        f"Minimum ROC-AUC improvement : "
        f"{ROC_AUC_MIN_IMPROVEMENT * 100:.2f}%"
    )

    print(
        f"Maximum Recall decrease     : "
        f"{MAX_RECALL_DECREASE * 100:.2f}%"
    )

    print(
        f"Maximum F1 decrease         : "
        f"{MAX_F1_DECREASE * 100:.2f}%"
    )

    print(
        f"Maximum Precision decrease  : "
        f"{MAX_PRECISION_DECREASE * 100:.2f}%"
    )

    print(
        f"ROC-AUC improvement         : "
        f"{roc_auc_improvement * 100:+.2f}%"
    )

    print(
        f"Recall change               : "
        f"{recall_change * 100:+.2f}%"
    )

    print(
        f"F1 change                   : "
        f"{f1_change * 100:+.2f}%"
    )

    print(
        f"Precision change            : "
        f"{precision_change * 100:+.2f}%"
    )

    print("\nSTEP 6 - MODEL ACCEPTANCE")

    print("-" * 80)

    if new_model_is_better:

        os.makedirs(
            RETRAINED_MODEL_DIR,
            exist_ok=True
        )

        new_model_path = os.path.join(
            RETRAINED_MODEL_DIR,
            "failure_prediction_model.pkl"
        )

        new_scaler_path = os.path.join(
            RETRAINED_MODEL_DIR,
            "feature_scaler.pkl"
        )

        joblib.dump(
            new_model,
            new_model_path
        )

        joblib.dump(
            new_scaler,
            new_scaler_path
        )

        print(
            "New model accepted."
        )

        print(
            f"Model saved to  : "
            f"{new_model_path}"
        )

        print(
            f"Scaler saved to : "
            f"{new_scaler_path}"
        )

        if not TEST_MODE:

            print("\nMODEL PROMOTION")

            print("-" * 80)

            (
                backup_model_path,
                backup_scaler_path
            ) = promote_new_model(
                new_model_path,
                new_scaler_path
            )

            print(
                f"Backup model saved to  : "
                f"{backup_model_path}"
            )

            print(
                f"Backup scaler saved to : "
                f"{backup_scaler_path}"
            )

            print(
                "Accepted model promoted to active model."
            )

    else:

        print(
            "New model rejected."
        )

        print(
            "Current model remains active."
        )

    if TEST_MODE:

        print("\nTEST MODE SAFETY CHECK")

        print("-" * 80)

        print(
            "MySQL feedback was not modified."
        )

        print(
            "Baseline model was not overwritten."
        )

        print(
            "Retrained model, if accepted, was saved "
            "to the separate retrained_model directory."
        )

    print(
        "\n" + "=" * 80
    )

    print(
        "SELF-HEALING RETRAINING PIPELINE COMPLETED"
    )

    print("=" * 80)


if __name__ == "__main__":

    main()