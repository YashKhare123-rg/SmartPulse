import joblib
import numpy as np
import pandas as pd

MODEL_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\failure_prediction_model.pkl"
SCALER_PATH = r"E:\SmartPulse\ml\models\new_data_baseline\feature_scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("ML model loaded successfully")
print("Feature scaler loaded successfully")


FEATURE_NAMES = [
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


def create_feature_array(
        temperature,
        vibration,
        pressure,
        power_consumption,
        operating_hours,
        load_percentage,
        rotation_speed,
        maintenance_count,
        machine_age
):
    return pd.DataFrame(
        [[
            temperature,
            vibration,
            pressure,
            power_consumption,
            operating_hours,
            load_percentage,
            rotation_speed,
            maintenance_count,
            machine_age
        ]],
        columns=FEATURE_NAMES
    )


def predict_failure(
        temperature,
        vibration,
        pressure,
        power_consumption,
        operating_hours,
        load_percentage,
        rotation_speed,
        maintenance_count,
        machine_age
):
    features = create_feature_array(
        temperature,
        vibration,
        pressure,
        power_consumption,
        operating_hours,
        load_percentage,
        rotation_speed,
        maintenance_count,
        machine_age
    )

    scaled_features = scaler.transform(features)

    probability = model.predict_proba(scaled_features)[0][1]

    return probability


def explain_prediction(
        temperature,
        vibration,
        pressure,
        power_consumption,
        operating_hours,
        load_percentage,
        rotation_speed,
        maintenance_count,
        machine_age
):
    features = create_feature_array(
        temperature,
        vibration,
        pressure,
        power_consumption,
        operating_hours,
        load_percentage,
        rotation_speed,
        maintenance_count,
        machine_age
    )

    scaled_features = scaler.transform(features)

    probability = model.predict_proba(scaled_features)[0][1]

    coefficients = model.coef_[0]

    contributions = scaled_features[0] * coefficients

    explanations = []

    for i, feature in enumerate(FEATURE_NAMES):

        contribution = float(contributions[i])

        if contribution > 0:
            direction = "INCREASES_FAILURE_RISK"
        elif contribution < 0:
            direction = "DECREASES_FAILURE_RISK"
        else:
            direction = "NEUTRAL"

        absolute_contribution = abs(contribution)

        if absolute_contribution >= 0.75:
            impact = "HIGH"
        elif absolute_contribution >= 0.30:
            impact = "MEDIUM"
        else:
            impact = "LOW"

        explanations.append({
            "feature": feature,
            "value": float(features.iloc[0, i]),
            "scaled_value": float(scaled_features[0][i]),
            "contribution": round(contribution, 6),
            "absolute_contribution": round(
                absolute_contribution,
                6
            ),
            "direction": direction,
            "impact": impact
        })

    explanations.sort(
        key=lambda item: item["absolute_contribution"],
        reverse=True
    )

    return {
        "failure_probability": float(probability),
        "base_intercept": float(model.intercept_[0]),
        "explanations": explanations
    }


if __name__ == "__main__":

    probability = predict_failure(
        temperature=70.59,
        vibration=4.32,
        pressure=5.93,
        power_consumption=8.33,
        operating_hours=580.22,
        load_percentage=60.30,
        rotation_speed=1495.84,
        maintenance_count=0,
        machine_age=5
    )

    print()
    print("=" * 70)
    print("FAILURE PREDICTION")
    print("=" * 70)

    print(f"Failure probability: {probability:.4f}")
    print(f"Failure probability: {probability * 100:.2f}%")

    explanation = explain_prediction(
        temperature=70.59,
        vibration=4.32,
        pressure=5.93,
        power_consumption=8.33,
        operating_hours=580.22,
        load_percentage=60.30,
        rotation_speed=1495.84,
        maintenance_count=0,
        machine_age=5
    )

    print()
    print("=" * 70)
    print("EXPLAINABLE AI")
    print("=" * 70)

    for item in explanation["explanations"]:

        print(
            f"{item['feature']:25} "
            f"value={item['value']:10.2f}  "
            f"contribution={item['contribution']:8.4f}  "
            f"{item['direction']:25} "
            f"impact={item['impact']}"
        )