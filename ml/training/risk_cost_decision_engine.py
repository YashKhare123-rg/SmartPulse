import pandas as pd
import joblib

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"

DATA_DRIFT_REPORT = r"E:\SmartPulse\ml\data\data_drift_report.csv"
MODEL_DRIFT_REPORT = r"E:\SmartPulse\ml\data\model_drift_report.csv"

PREVENTIVE_MAINTENANCE_COST = 500
FAILURE_REPAIR_COST = 5000
DOWNTIME_COST_PER_HOUR = 1000
EXPECTED_DOWNTIME_HOURS = 4


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


def calculate_costs(failure_probability):

    expected_repair_cost = (
            failure_probability * FAILURE_REPAIR_COST
    )

    expected_downtime_cost = (
            failure_probability
            * EXPECTED_DOWNTIME_HOURS
            * DOWNTIME_COST_PER_HOUR
    )

    expected_failure_cost = (
            expected_repair_cost
            + expected_downtime_cost
    )

    return expected_repair_cost, expected_downtime_cost, expected_failure_cost


def determine_final_decision(
        risk_level,
        failure_probability,
        expected_failure_cost
):

    if risk_level == "CRITICAL":
        return "EMERGENCY ACTION"

    if risk_level == "HIGH":
        return "URGENT MAINTENANCE"

    if risk_level == "MEDIUM":
        if expected_failure_cost > PREVENTIVE_MAINTENANCE_COST:
            return "SCHEDULE MAINTENANCE"
        return "CONTINUE WITH MONITORING"

    if failure_probability >= 0.30:
        return "SCHEDULE INSPECTION"

    return "CONTINUE NORMAL OPERATION"


def main():

    print("=" * 70)
    print("SMARTPULSE 2.0 - RISK + COST DECISION ENGINE")
    print("=" * 70)

    data = pd.read_csv(DATA_PATH)

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    data_drift = pd.read_csv(DATA_DRIFT_REPORT)
    model_drift = pd.read_csv(MODEL_DRIFT_REPORT)

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

    (
        expected_repair_cost,
        expected_downtime_cost,
        expected_failure_cost
    ) = calculate_costs(failure_probability)

    final_decision = determine_final_decision(
        risk_level,
        failure_probability,
        expected_failure_cost
    )

    print("\nMACHINE INFORMATION")
    print("-" * 70)

    print(f"Machine ID           : {machine['machine_id']}")
    print(f"Temperature          : {machine['temperature']:.2f}")
    print(f"Vibration            : {machine['vibration']:.2f}")
    print(f"Pressure             : {machine['pressure']:.2f}")
    print(f"Load Percentage      : {machine['load_percentage']:.2f}%")
    print(f"Machine Age          : {int(machine['machine_age'])} years")
    print(f"Maintenance Count    : {int(machine['maintenance_count'])}")

    print("\nINTELLIGENCE SIGNALS")
    print("-" * 70)

    print(f"Failure Probability  : {failure_probability * 100:.2f}%")
    print(f"Data Drift Status    : {data_drift_status}")
    print(f"Model Drift Status   : {model_drift_status}")

    print("\nRISK ANALYSIS")
    print("-" * 70)

    print(f"Risk Score            : {risk_score}/100")
    print(f"Risk Level            : {risk_level}")

    print("\nCOST ANALYSIS")
    print("-" * 70)

    print(f"Expected Repair Cost  : ${expected_repair_cost:,.2f}")
    print(f"Expected Downtime Cost: ${expected_downtime_cost:,.2f}")
    print(f"Expected Failure Cost : ${expected_failure_cost:,.2f}")
    print(f"Preventive Maintenance: ${PREVENTIVE_MAINTENANCE_COST:,.2f}")

    print("\nFINAL DECISION")
    print("-" * 70)

    print(f"Decision              : {final_decision}")

    if final_decision == "EMERGENCY ACTION":
        print("Action                : Immediate inspection and controlled shutdown")
    elif final_decision == "URGENT MAINTENANCE":
        print("Action                : Perform preventive maintenance immediately")
    elif final_decision == "SCHEDULE MAINTENANCE":
        print("Action                : Schedule preventive maintenance")
    elif final_decision == "SCHEDULE INSPECTION":
        print("Action                : Schedule inspection and continue monitoring")
    else:
        print("Action                : Continue normal operation and monitoring")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()