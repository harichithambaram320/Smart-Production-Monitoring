from flask import Flask, render_template
import pandas as pd
import os
import joblib
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

# Load Predictive Maintenance Model
model_path = os.path.join(
    "models",
    "predictive_maintenance_model.pkl"
)

predictive_model = joblib.load(model_path)

model_accuracy = predictive_model.model_accuracy

top_feature = predictive_model.top_feature
top_feature_importance = predictive_model.top_feature_importance


@app.route("/")
def home():

    file_path = os.path.join("data", "sensor_data.csv")

    df = pd.read_csv(file_path)


    # -----------------------------
    # Anomaly Detection
    # -----------------------------

    features = [
        "temperature",
        "vibration",
        "pressure",
        "error_count"
    ]

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    df["anomaly_prediction"] = model.fit_predict(
        df[features]
    )

    df["anomaly_status"] = df["anomaly_prediction"].apply(
        lambda x: "Anomaly" if x == -1 else "Normal"
    )


    # -----------------------------
    # Latest Machine Readings
    # -----------------------------

    latest_data = (
        df.sort_values("timestamp")
        .groupby("machine")
        .tail(1)
    )

    machines = latest_data.to_dict(
        orient="records"
    )

    # -----------------------------
    # Predictive Maintenance Model
    # -----------------------------

    prediction_features = [
        "temperature",
        "vibration",
        "pressure",
        "production_count",
        "error_count"
    ]

    latest_features = latest_data[prediction_features]

    latest_predictions = predictive_model.predict(
        latest_features
    )

    for machine, prediction in zip(
        machines,
        latest_predictions
    ):
        machine["predicted_condition"] = prediction

    # -----------------------------
    # Machine Health Score
    # -----------------------------

    for machine in machines:

        temperature_score = max(
            0,
            100 - abs(machine["temperature"] - 65) * 2
        )

        vibration_score = max(
            0,
            100 - abs(machine["vibration"] - 2.5) * 20
        )

        pressure_score = max(
            0,
            100 - abs(machine["pressure"] - 5.5) * 15
        )

        error_score = max(
            0,
            100 - machine["error_count"] * 10
        )

        machine["health_score"] = round(
            (
                temperature_score * 0.35
                + vibration_score * 0.30
                + pressure_score * 0.20
                + error_score * 0.15
            ),
            1
        )

                # Failure Risk Prediction

        failure_risk = (
            (100 - machine["health_score"]) * 0.7
            + machine["error_count"] * 3
            + max(0, machine["temperature"] - 65) * 0.5
        )

        machine["failure_risk"] = round(
            min(100, max(0, failure_risk)),
            1
        )

        if machine["failure_risk"] >= 70:

            machine["failure_risk_status"] = "High Risk"

        elif machine["failure_risk"] >= 40:

            machine["failure_risk_status"] = "Medium Risk"

        else:

            machine["failure_risk_status"] = "Low Risk"

                    # Failure Risk Reason

        risk_reasons = []

        if machine["temperature"] > 75:
            risk_reasons.append("High temperature")

        if machine["vibration"] > 3.5:
            risk_reasons.append("High vibration")

        if machine["pressure"] > 6.2:
            risk_reasons.append("High pressure")

        if machine["error_count"] >= 5:
            risk_reasons.append("High error count")

        if not risk_reasons:
            risk_reasons.append("Sensor readings within normal range")

        machine["failure_risk_reason"] = " + ".join(
            risk_reasons
        )


        if machine["health_score"] >= 90:

            machine["health_status"] = "Healthy"

        elif machine["health_score"] >= 70:

            machine["health_status"] = "Attention"

        else:

            machine["health_status"] = "High Risk"


        # Maintenance Recommendation

        if machine["predicted_condition"] == "Critical":
            machine["maintenance_recommendation"] = (
                "Immediate inspection recommended"
            )

        elif machine["predicted_condition"] == "Warning":
            machine["maintenance_recommendation"] = (
                "Monitor machine closely"
            )

        elif machine["anomaly_status"] == "Anomaly":
            machine["maintenance_recommendation"] = (
                "Inspect abnormal sensor readings"
            )

        else:
            machine["maintenance_recommendation"] = (
                "Machine operating normally"
            )

        

    # -----------------------------
    # Production KPI
    # -----------------------------

    total_production = sum(
        machine["production_count"]
        for machine in machines
    )

    total_errors = sum(
        machine["error_count"]
        for machine in machines
    )

    average_health = round(
        sum(
            machine["health_score"]
            for machine in machines
        )
        / len(machines),
        1
    )

    # -----------------------------
    # Failure Risk Summary
    # -----------------------------

    low_risk_count = sum(
        machine["failure_risk_status"] == "Low Risk"
        for machine in machines
    )

    medium_risk_count = sum(
        machine["failure_risk_status"] == "Medium Risk"
        for machine in machines
    )

    high_risk_count = sum(
        machine["failure_risk_status"] == "High Risk"
        for machine in machines
    )


    # -----------------------------
    # Dashboard Summary
    # -----------------------------

    total_machines = len(machines)

    normal_count = (
        latest_data["machine_condition"] == "Normal"
    ).sum()

    warning_count = (
        latest_data["machine_condition"] == "Warning"
    ).sum()

    critical_count = (
        latest_data["machine_condition"] == "Critical"
    ).sum()


    # -----------------------------
    # Machine Performance Summary
    # -----------------------------

    performance_summary = []

    for machine in machines:

        performance_summary.append({
            "machine": machine["machine"],
            "production": machine["production_count"],
            "errors": machine["error_count"],
            "health_score": machine["health_score"],
            "health_status": machine["health_status"]
        })

    # -----------------------------
    # At-Risk Machine Ranking
    # -----------------------------

    at_risk_machines = sorted(
        machines,
        key=lambda machine: machine["failure_risk"],
        reverse=True
    )


    # -----------------------------
    # Active Maintenance Alerts
    # -----------------------------

    active_alerts = []

    for machine in machines:

        if (
            machine["health_status"] != "Healthy"
            or machine["anomaly_status"] == "Anomaly"
        ):

            active_alerts.append({
                "machine": machine["machine"],
                "health_score": machine["health_score"],
                "health_status": machine["health_status"],
                "anomaly_status": machine["anomaly_status"],
                "recommendation": machine["maintenance_recommendation"]
            })


    # -----------------------------
    # Chart Data
    # -----------------------------

    chart_data = df.tail(50).to_dict(
        orient="records"
    )


    # -----------------------------
    # Render Dashboard
    # -----------------------------

    return render_template(
        "dashboard.html",

        machines=machines,

        total_production=total_production,

        total_errors=total_errors,

        model_accuracy=model_accuracy,

        top_feature=top_feature,
        
top_feature_importance=top_feature_importance,

        average_health=average_health,

            low_risk_count=low_risk_count,

    medium_risk_count=medium_risk_count,

    high_risk_count=high_risk_count,

        chart_data=chart_data,

        active_alerts=active_alerts,

        performance_summary=performance_summary,

        at_risk_machines=at_risk_machines,

        total_machines=total_machines,

        normal_count=normal_count,

        warning_count=warning_count,

        critical_count=critical_count
    )


if __name__ == "__main__":

    app.run(debug=False)