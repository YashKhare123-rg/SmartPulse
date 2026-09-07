from risk_cost_decision_engine import (
    calculate_risk_score,
    classify_risk,
    calculate_costs,
    determine_final_decision
)


SCENARIOS = [
    {
        "name": "Healthy Machine",
        "failure_probability": 0.08,
        "data_drift": "STABLE",
        "model_drift": "STABLE",
        "machine_age": 2,
        "maintenance_count": 3,
        "temperature": 55,
        "vibration": 2,
        "pressure": 5,
        "load": 50
    },
    {
        "name": "Medium Risk Machine",
        "failure_probability": 0.40,
        "data_drift": "WARNING",
        "model_drift": "STABLE",
        "machine_age": 8,
        "maintenance_count": 2,
        "temperature": 82,
        "vibration": 6,
        "pressure": 8,
        "load": 72
    },
    {
        "name": "High Risk Machine",
        "failure_probability": 0.68,
        "data_drift": "DRIFT",
        "model_drift": "STABLE",
        "machine_age": 12,
        "maintenance_count": 1,
        "temperature": 92,
        "vibration": 8,
        "pressure": 10,
        "load": 85
    },
    {
        "name": "Critical Machine",
        "failure_probability": 0.91,
        "data_drift": "DRIFT",
        "model_drift": "DRIFT",
        "machine_age": 18,
        "maintenance_count": 0,
        "temperature": 105,
        "vibration": 12,
        "pressure": 12,
        "load": 95
    }
]


def main():

    print("=" * 90)
    print("SMARTPULSE 2.0 - DECISION ENGINE SCENARIO TESTER")
    print("=" * 90)

    for scenario in SCENARIOS:

        risk_score = calculate_risk_score(
            scenario["failure_probability"],
            scenario["data_drift"],
            scenario["model_drift"],
            scenario["machine_age"],
            scenario["maintenance_count"],
            scenario["temperature"],
            scenario["vibration"],
            scenario["pressure"],
            scenario["load"]
        )

        risk_level = classify_risk(risk_score)

        (
            expected_repair_cost,
            expected_downtime_cost,
            expected_failure_cost
        ) = calculate_costs(
            scenario["failure_probability"]
        )

        decision = determine_final_decision(
            risk_level,
            scenario["failure_probability"],
            expected_failure_cost
        )

        print("\n" + "-" * 90)
        print(f"SCENARIO: {scenario['name']}")
        print("-" * 90)

        print(
            f"Failure Probability : "
            f"{scenario['failure_probability'] * 100:.2f}%"
        )

        print(f"Data Drift         : {scenario['data_drift']}")
        print(f"Model Drift        : {scenario['model_drift']}")

        print(f"Machine Age        : {scenario['machine_age']} years")
        print(
            f"Maintenance Count  : "
            f"{scenario['maintenance_count']}"
        )

        print(f"Temperature        : {scenario['temperature']}")
        print(f"Vibration          : {scenario['vibration']}")
        print(f"Pressure           : {scenario['pressure']}")
        print(f"Load               : {scenario['load']}%")

        print(f"\nRisk Score         : {risk_score}/100")
        print(f"Risk Level         : {risk_level}")

        print(
            f"\nExpected Failure Cost : "
            f"${expected_failure_cost:,.2f}"
        )

        print(f"Final Decision     : {decision}")

    print("\n" + "=" * 90)
    print("SCENARIO TESTING COMPLETED")
    print("=" * 90)


if __name__ == "__main__":
    main()