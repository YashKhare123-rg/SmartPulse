import pandas as pd
import joblib

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"


PREVENTIVE_MAINTENANCE_COST = 500
FAILURE_REPAIR_COST = 5000
DOWNTIME_COST_PER_HOUR = 1000
EXPECTED_DOWNTIME_HOURS = 4


def calculate_costs(failure_probability):

    expected_failure_cost = (
            failure_probability * FAILURE_REPAIR_COST
    )

    expected_downtime_cost = (
            failure_probability
            * EXPECTED_DOWNTIME_HOURS
            * DOWNTIME_COST_PER_HOUR
    )

    total_expected_failure_cost = (
            expected_failure_cost
            + expected_downtime_cost
    )

    maintenance_cost = PREVENTIVE_MAINTENANCE_COST

    return (
        expected_failure_cost,
        expected_downtime_cost,
        total_expected_failure_cost,
        maintenance_cost
    )


def determine_decision(
        failure_probability,
        total_expected_failure_cost,
        maintenance_cost
):

    if failure_probability >= 0.80:
        return "EMERGENCY ACTION"

    if total_expected_failure_cost >= maintenance_cost * 2:
        return "URGENT MAINTENANCE"

    if total_expected_failure_cost > maintenance_cost:
        return "SCHEDULE MAINTENANCE"

    return "CONTINUE"


def main():

    print("=" * 70)
    print("SMARTPULSE 2.0 - COST-AWARE MAINTENANCE OPTIMIZER")
    print("=" * 70)

    data = pd.read_csv(DATA_PATH)

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

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

    (
        expected_failure_cost,
        expected_downtime_cost,
        total_expected_failure_cost,
        maintenance_cost
    ) = calculate_costs(failure_probability)

    decision = determine_decision(
        failure_probability,
        total_expected_failure_cost,
        maintenance_cost
    )

    potential_savings = (
            total_expected_failure_cost - maintenance_cost
    )

    print("\nMACHINE INFORMATION")
    print("-" * 70)

    print(f"Machine ID           : {machine['machine_id']}")
    print(f"Failure Probability  : {failure_probability * 100:.2f}%")

    print("\nCOST PARAMETERS")
    print("-" * 70)

    print(f"Preventive Maintenance Cost : ${maintenance_cost:,.2f}")
    print(f"Failure Repair Cost         : ${FAILURE_REPAIR_COST:,.2f}")
    print(f"Downtime Cost / Hour        : ${DOWNTIME_COST_PER_HOUR:,.2f}")
    print(f"Expected Downtime           : {EXPECTED_DOWNTIME_HOURS} hours")

    print("\nEXPECTED COST ANALYSIS")
    print("-" * 70)

    print(f"Expected Repair Cost        : ${expected_failure_cost:,.2f}")
    print(f"Expected Downtime Cost      : ${expected_downtime_cost:,.2f}")
    print(f"Total Expected Failure Cost : ${total_expected_failure_cost:,.2f}")
    print(f"Maintenance Cost            : ${maintenance_cost:,.2f}")

    print("\nOPTIMIZATION RESULT")
    print("-" * 70)

    print(f"Maintenance Decision        : {decision}")

    if potential_savings > 0:
        print(f"Potential Cost Saving       : ${potential_savings:,.2f}")
    else:
        print("Potential Cost Saving       : $0.00")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()