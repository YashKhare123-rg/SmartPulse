
from fastapi import FastAPI
from pydantic import BaseModel

from predictor import predict_failure, explain_prediction
from retraining_service import run_retraining

import os
import pandas as pd


app = FastAPI(
    title="SmartPulse 2.0 ML Service",
    description="Machine failure prediction, explainable AI, drift monitoring, cost analysis and self-healing retraining",
    version="2.0"
)


class PredictionRequest(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    power_consumption: float
    operating_hours: float
    load_percentage: float
    rotation_speed: float
    maintenance_count: float
    machine_age: float


class CostAnalysisRequest(BaseModel):
    failure_probability: float
    preventive_maintenance_cost: float = 500.0
    repair_cost: float = 5000.0
    downtime_cost_per_hour: float = 1000.0
    expected_downtime_hours: float = 4.0


@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "SmartPulse ML Service",
        "version": "2.0"
    }


@app.post("/predict")
def predict(request: PredictionRequest):

    return predict_failure(
        temperature=request.temperature,
        vibration=request.vibration,
        pressure=request.pressure,
        power_consumption=request.power_consumption,
        operating_hours=request.operating_hours,
        load_percentage=request.load_percentage,
        rotation_speed=request.rotation_speed,
        maintenance_count=request.maintenance_count,
        machine_age=request.machine_age
    )


@app.post("/explain")
def explain(request: PredictionRequest):

    return explain_prediction(
        temperature=request.temperature,
        vibration=request.vibration,
        pressure=request.pressure,
        power_consumption=request.power_consumption,
        operating_hours=request.operating_hours,
        load_percentage=request.load_percentage,
        rotation_speed=request.rotation_speed,
        maintenance_count=request.maintenance_count,
        machine_age=request.machine_age
    )


@app.post("/cost-analysis")
def cost_analysis(request: CostAnalysisRequest):

    failure_probability = request.failure_probability

    expected_failure_cost = failure_probability * (
            request.repair_cost
            + request.downtime_cost_per_hour
            * request.expected_downtime_hours
    )

    preventive_maintenance_cost = (
        request.preventive_maintenance_cost
    )

    maintenance_recommended = (
            expected_failure_cost
            > preventive_maintenance_cost
    )

    savings = (
            expected_failure_cost
            - preventive_maintenance_cost
    )

    return {
        "failure_probability": failure_probability,
        "expected_failure_cost": round(
            expected_failure_cost,
            2
        ),
        "preventive_maintenance_cost": round(
            preventive_maintenance_cost,
            2
        ),
        "potential_savings": round(
            max(savings, 0),
            2
        ),
        "maintenance_recommended": maintenance_recommended
    }


@app.get("/data-drift")
def data_drift():

    drift_report_path = (
        r"E:\SmartPulse\ml\data\data_drift_report.csv"
    )

    if not os.path.exists(drift_report_path):

        return {
            "status": "NOT_AVAILABLE",
            "message": "Data drift report not found."
        }

    report = pd.read_csv(drift_report_path)

    records = report.to_dict(
        orient="records"
    )

    drift_detected = any(
        str(row.get("status", "")).upper()
        == "DRIFT"
        for row in records
    )

    warning_detected = any(
        str(row.get("status", "")).upper()
        == "WARNING"
        for row in records
    )

    if drift_detected:

        overall_status = "DRIFT DETECTED"

    elif warning_detected:

        overall_status = "WARNING"

    else:

        overall_status = "STABLE"

    return {
        "overall_status": overall_status,
        "features": records
    }


@app.get("/model-drift")
def model_drift():

    drift_report_path = (
        r"E:\SmartPulse\ml\data\model_drift_report.csv"
    )

    if not os.path.exists(drift_report_path):

        return {
            "status": "NOT_AVAILABLE",
            "message": "Model drift report not found."
        }

    report = pd.read_csv(
        drift_report_path
    )

    records = report.to_dict(
        orient="records"
    )

    drift_detected = any(
        str(row.get("status", "")).upper()
        == "DRIFT"
        for row in records
    )

    if drift_detected:

        overall_status = "MODEL DRIFT DETECTED"

    else:

        overall_status = "STABLE"

    return {
        "overall_status": overall_status,
        "metrics": records
    }


@app.post("/retrain")
def retrain_model():

    password = os.getenv(
        "SMARTPULSE_DB_PASSWORD"
    )

    if not password:

        return {
            "success": False,
            "message": (
                "SMARTPULSE_DB_PASSWORD "
                "environment variable is not configured."
            )
        }

    result = run_retraining(
        test_mode=False,
        db_password=password
    )

    return {
        "success": result["success"],
        "return_code": result["return_code"],
        "output": result["output"],
        "error": result["error"]
    }