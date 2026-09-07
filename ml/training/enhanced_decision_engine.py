import pandas as pd
import joblib

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"

DATA_DRIFT_REPORT = r"E:\SmartPulse\ml\data\data_drift_report.csv"
MODEL_DRIFT_REPORT = r"E:\SmartPulse\ml\data\model_drift_report.csv"


def load_reports():
    data_drift = pd.read_csv(DATA_DRIFT_REPORT)
    model_drift = pd.read_csv(MODEL_DRIFT_REPORT)

    return data_drift, model_drift


def calculate_risk_score(
        failure_probability,
        data_drift_status,
        model_drift_status,
        machine_age,
        maintenance_count,
        temperature,
        vibration,
        pressure,
        load_percentage
):
    score = 0

    if failure_probability >= 0.80:
        score += 40
    elif failure_probability >= 0.60:
        score += 30
    elif failure_probability >= 0.30:
        score += 20
    else:
        score += 5

    if data_drift_status == "DRIFT":
        score += 15
    elif data_drift_status == "WARNING":
        score += 7

    if model_drift_status == "DRIFT":
        score += 15

    if machine_age >= 15:
        score += 10
    elif machine_age >= 10:
        score += 6
    elif machine_age >= 5:
        score += 3

    if maintenance_count == 0:
        score += 5
    elif maintenance_count >= 5:
        score += 4
    elif maintenance_count >= 3:
        score += 2

    if temperature >= 100:
        score += 5
    elif temperature >= 85:
        score += 3

    if vibration >= 10:
        score += 5
    elif vibration >= 7:
        score += 3

    if pressure >= 10:
        score += 3

    if load_percentage >= 90:
        score += 5
    elif load_percentage >= 75:
        score += 3

    return min(score, 100)


def classify_risk(score):
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"


def determine_priority(risk_level):
    if risk_level == "CRITICAL":
        return "URGENT"
    elif risk_level == "HIGH":
        return "HIGH"
    elif risk_level == "MEDIUM":
        return "MEDIUM"
    else:
        return "LOW"


def determine_action(risk_level):
    if risk_level == "CRITICAL":
        return "Immediate inspection and consider controlled shutdown"
    elif risk_level == "HIGH":
        return "Schedule preventive maintenance soon"
    elif risk_level == "MEDIUM":
        return "Schedule routine inspection"
    else:
        return "Continue normal operation"


def main():

    print("=" * 70)
    print("SMARTPULSE 2.0 - ENHANCED DECISION ENGINE")
    print("=" * 70)

    data = pd.read_csv(DATA_PATH)

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    data_drift, model_drift = load_reports()

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

    machine = data.iloc[0]

    X = pd.DataFrame(
        [machine[features].values],
        columns=features
    )

    X_scaled = scaler.transform(X)

    failure_probability = model.predict_proba(X_scaled)[0][1]

    drift_counts = data_drift["status"].value_counts().to_dict()

    data_drift_status = "STABLE"

    if drift_counts.get("DRIFT", 0) > 0:
        data_drift_status = "DRIFT"
    elif drift_counts.get("WARNING", 0) > 0:
        data_drift_status = "WARNING"

    model_drift_status = "STABLE"

    if "DRIFT" in model_drift["status"].values:
        model_drift_status = "DRIFT"

    risk_score = calculate_risk_score(
        failure_probability,
        data_drift_status,
        model_drift_status,
        machine["machine_age"],
        machine["maintenance_count"],
        machine["temperature"],
        machine["vibration"],
        machine["pressure"],
        machine["load_percentage"]
    )

    risk_level = classify_risk(risk_score)
    priority = determine_priority(risk_level)
    action = determine_action(risk_level)

    print("\nMACHINE INFORMATION")
    print("-" * 70)

    print(f"Machine ID           : {machine['machine_id']}")
    print(f"Temperature          : {machine['temperature']:.2f}")
    print(f"Vibration            : {machine['vibration']:.2f}")
    print(f"Pressure             : {machine['pressure']:.2f}")
    print(f"Power Consumption    : {machine['power_consumption']:.2f}")
    print(f"Operating Hours      : {machine['operating_hours']:.2f}")
    print(f"Load Percentage      : {machine['load_percentage']:.2f}%")
    print(f"Rotation Speed       : {machine['rotation_speed']:.2f}")
    print(f"Maintenance Count    : {int(machine['maintenance_count'])}")
    print(f"Machine Age          : {int(machine['machine_age'])} years")

    print("\nINTELLIGENCE SIGNALS")
    print("-" * 70)

    print(f"Failure Probability  : {failure_probability * 100:.2f}%")
    print(f"Data Drift Status    : {data_drift_status}")
    print(f"Model Drift Status   : {model_drift_status}")

    print("\nDECISION")
    print("-" * 70)

    print(f"Overall Risk Score   : {risk_score}/100")
    print(f"Risk Level           : {risk_level}")
    print(f"Priority             : {priority}")
    print(f"Recommended Action   : {action}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()