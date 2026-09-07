import pandas as pd
import joblib

DATA_PATH = r"E:\SmartPulse\data\processed\valid_machine_data.csv"

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"

PREVENTIVE_MAINTENANCE_COST = 500
FAILURE_REPAIR_COST = 5000
DOWNTIME_COST_PER_HOUR = 1000
EXPECTED_DOWNTIME_HOURS = 4


def predict_failure(machine, model, scaler):

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

    X = pd.DataFrame(
        [machine[features].values],
        columns=features
    )

    X_scaled = scaler.transform(X)

    return model.predict_proba(X_scaled)[0][1]


def calculate_expected_cost(failure_probability):

    repair_cost = (
            failure_probability * FAILURE_REPAIR_COST
    )

    downtime_cost = (
            failure_probability
            * EXPECTED_DOWNTIME_HOURS
            * DOWNTIME_COST_PER_HOUR
    )

    return repair_cost + downtime_cost


def print_result(title, machine, probability, cost):

    print("\n" + "-" * 75)
    print(title)
    print("-" * 75)

    print(f"Temperature       : {machine['temperature']:.2f}")
    print(f"Vibration         : {machine['vibration']:.2f}")
    print(f"Pressure          : {machine['pressure']:.2f}")
    print(f"Load              : {machine['load_percentage']:.2f}%")
    print(f"Maintenance Count : {int(machine['maintenance_count'])}")

    print(
        f"\nFailure Probability : "
        f"{probability * 100:.2f}%"
    )

    print(
        f"Expected Failure Cost : "
        f"${cost:,.2f}"
    )


def main():

    print("=" * 75)
    print("SMARTPULSE 2.0 - WHAT-IF MAINTENANCE SIMULATOR")
    print("=" * 75)

    data = pd.read_csv(DATA_PATH)

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    original_machine = data.iloc[0].copy()

    print(f"\nMachine ID: {original_machine['machine_id']}")

    # BASELINE

    baseline_probability = predict_failure(
        original_machine,
        model,
        scaler
    )

    baseline_cost = calculate_expected_cost(
        baseline_probability
    )

    print_result(
        "BASELINE MACHINE",
        original_machine,
        baseline_probability,
        baseline_cost
    )

    # SCENARIO 1
    # Temperature increases by 10%

    temperature_scenario = original_machine.copy()

    temperature_scenario["temperature"] *= 1.10

    temperature_probability = predict_failure(
        temperature_scenario,
        model,
        scaler
    )

    temperature_cost = calculate_expected_cost(
        temperature_probability
    )

    print_result(
        "WHAT-IF 1: TEMPERATURE +10%",
        temperature_scenario,
        temperature_probability,
        temperature_cost
    )

    # SCENARIO 2
    # Load increases by 15%

    load_scenario = original_machine.copy()

    load_scenario["load_percentage"] = min(
        load_scenario["load_percentage"] * 1.15,
        100
    )

    load_probability = predict_failure(
        load_scenario,
        model,
        scaler
    )

    load_cost = calculate_expected_cost(
        load_probability
    )

    print_result(
        "WHAT-IF 2: LOAD +15%",
        load_scenario,
        load_probability,
        load_cost
    )

    # SCENARIO 3
    # Maintenance performed

    maintenance_scenario = original_machine.copy()

    maintenance_scenario["maintenance_count"] += 1

    maintenance_scenario["temperature"] *= 0.95
    maintenance_scenario["vibration"] *= 0.90
    maintenance_scenario["load_percentage"] *= 0.95

    maintenance_probability = predict_failure(
        maintenance_scenario,
        model,
        scaler
    )

    maintenance_cost = calculate_expected_cost(
        maintenance_probability
    )

    print_result(
        "WHAT-IF 3: PREVENTIVE MAINTENANCE",
        maintenance_scenario,
        maintenance_probability,
        maintenance_cost
    )

    # COMPARISON

    print("\n" + "=" * 75)
    print("SCENARIO COMPARISON")
    print("=" * 75)

    print(
        f"\nBaseline Failure Probability     : "
        f"{baseline_probability * 100:.2f}%"
    )

    print(
        f"Temperature +10%                 : "
        f"{temperature_probability * 100:.2f}%"
    )

    print(
        f"Load +15%                         : "
        f"{load_probability * 100:.2f}%"
    )

    print(
        f"After Preventive Maintenance      : "
        f"{maintenance_probability * 100:.2f}%"
    )

    print("\nEXPECTED COST COMPARISON")

    print(
        f"Baseline                          : "
        f"${baseline_cost:,.2f}"
    )

    print(
        f"Temperature +10%                 : "
        f"${temperature_cost:,.2f}"
    )

    print(
        f"Load +15%                         : "
        f"${load_cost:,.2f}"
    )

    print(
        f"After Preventive Maintenance      : "
        f"${maintenance_cost:,.2f}"
    )

    risk_reduction = (
            baseline_probability
            - maintenance_probability
    )

    cost_reduction = (
            baseline_cost
            - maintenance_cost
    )

    print("\nMAINTENANCE IMPACT")

    print(
        f"Failure Probability Reduction    : "
        f"{risk_reduction * 100:.2f} percentage points"
    )

    print(
        f"Expected Failure Cost Reduction  : "
        f"${cost_reduction:,.2f}"
    )

    print("\n" + "=" * 75)
    print("WHAT-IF SIMULATION COMPLETED")
    print("=" * 75)


if __name__ == "__main__":
    main()