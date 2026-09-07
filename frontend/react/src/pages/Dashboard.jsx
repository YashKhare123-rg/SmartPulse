import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard({
                       onHealthyMachines,
                       onHighRiskMachines,
                   }) {
    const [machines, setMachines] = useState([]);
    const [feedbackAnalysis, setFeedbackAnalysis] = useState(null);
    const [dataDrift, setDataDrift] = useState(null);
    const [modelDrift, setModelDrift] = useState(null);
    const [dataQuality, setDataQuality] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadDashboardData = async () => {
        try {
            setLoading(true);
            setError("");

            const [
                machinesResponse,
                feedbackResponse,
                dataDriftResponse,
                modelDriftResponse,
                dataQualityResponse,
            ] = await Promise.all([
                axios.get("http://localhost:8080/api/machines"),
                axios.get("http://localhost:8080/api/feedback-analysis"),
                axios.get("http://localhost:8080/api/data-drift"),
                axios.get("http://localhost:8080/api/model-drift"),
                axios.get("http://localhost:8080/api/data-quality"),
            ]);

            setMachines(machinesResponse.data);
            setFeedbackAnalysis(feedbackResponse.data);
            setDataDrift(dataDriftResponse.data);
            setModelDrift(modelDriftResponse.data);
            setDataQuality(dataQualityResponse.data);
        } catch (err) {
            console.error(err);

            setError(
                "Unable to load dashboard data. Make sure Spring Boot is running."
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDashboardData();
    }, []);

    const uniqueMachines = new Set(
        machines.map((machine) => machine.machine_id)
    );

    const totalMachines = uniqueMachines.size;

    const latestMachineRecords = {};

    machines.forEach((machine) => {
        const machineId = machine.machine_id;

        if (
            !latestMachineRecords[machineId] ||
            new Date(machine.timestamp) >
            new Date(latestMachineRecords[machineId].timestamp)
        ) {
            latestMachineRecords[machineId] = machine;
        }
    });

    const latestRecords = Object.values(latestMachineRecords);

    const healthyMachines = latestRecords.filter(
        (machine) => Number(machine.failure) === 0
    ).length;

    const highRiskMachines = latestRecords.filter(
        (machine) => Number(machine.failure) === 1
    ).length;

    const healthyPercentage =
        totalMachines > 0
            ? (healthyMachines / totalMachines) * 100
            : 0;

    const highRiskPercentage =
        totalMachines > 0
            ? (highRiskMachines / totalMachines) * 100
            : 0;

    const driftFeatures =
        dataDrift?.features?.filter(
            (feature) =>
                String(feature.status).toUpperCase() === "DRIFT"
        ).length || 0;

    const modelHealthMetric =
        modelDrift?.metrics?.find((metric) => {
            const metricName = String(metric.metric)
                .toLowerCase()
                .replace(/[-_\s]/g, "");

            return metricName === "rocauc";
        });

    const modelHealth = modelHealthMetric
        ? Number(modelHealthMetric.current_value) * 100
        : 0;

    const feedbackRecords =
        feedbackAnalysis?.totalRecords ?? 0;

    const dataDriftStatus =
        dataDrift?.overall_status || "UNKNOWN";

    const modelDriftStatus =
        modelDrift?.overall_status || "UNKNOWN";

    const qualityPercentage =
        dataQuality?.qualityPercentage ?? 0;

    const validRecords =
        dataQuality?.validRecords ?? 0;

    const totalProcessed =
        dataQuality?.totalProcessed ?? 0;

    if (loading) {
        return (
            <section className="dashboard-content">
                <div className="loading-message">
                    Loading dashboard data...
                </div>
            </section>
        );
    }

    if (error) {
        return (
            <section className="dashboard-content">
                <div className="prediction-error">
                    {error}
                </div>
            </section>
        );
    }

    return (
        <section className="dashboard-content">

            <div className="welcome-card">

                <div>

          <span className="eyebrow">
            SMARTPULSE 2.0
          </span>

                    <h2>
                        Industrial Intelligence Center
                    </h2>

                    <p>
                        Monitor machine health, predict failures,
                        detect drift, optimize maintenance and
                        continuously improve the system.
                    </p>

                </div>

                <div className="pulse">

                    <div className="pulse-ring"></div>

                    <div className="pulse-core">
                        SP
                    </div>

                </div>

            </div>

            <div className="stats-grid">

                <div className="stat-card">

          <span>
            Total Machines
          </span>

                    <strong>
                        {totalMachines}
                    </strong>

                    <small>
                        Monitored machines
                    </small>

                </div>

                <div className="stat-card">

          <span>
            Healthy Machines
          </span>

                    <strong>
                        {healthyMachines}
                    </strong>

                    <small>
                        Latest failure status is normal
                    </small>

                </div>

                <div className="stat-card">

          <span>
            High Risk
          </span>

                    <strong>
                        {highRiskMachines}
                    </strong>

                    <small>
                        Latest failure flag detected
                    </small>

                </div>

                <div className="stat-card">

          <span>
            System Status
          </span>

                    <strong className="online">
                        ONLINE
                    </strong>

                    <small>
                        Dashboard services connected
                    </small>

                </div>

            </div>

            <div className="dashboard-risk-section">

                <div className="section-title">

                    <div>

                        <h2>
                            Machine Risk Overview
                        </h2>

                        <p>
                            Current distribution based on latest machine records
                        </p>

                    </div>

                </div>

                <div className="risk-overview-card">

                    <div className="risk-overview-header">

                        <div>

              <span>
                MACHINE HEALTH DISTRIBUTION
              </span>

                            <h3>
                                {totalMachines} Machines Monitored
                            </h3>

                        </div>

                        <div className="risk-total">

                            <strong>
                                {highRiskPercentage.toFixed(1)}%
                            </strong>

                            <small>
                                failure flagged
                            </small>

                        </div>

                    </div>

                    <div className="risk-bar">

                        <div
                            className="risk-bar-healthy"
                            style={{
                                width: `${healthyPercentage}%`,
                            }}
                        ></div>

                        <div
                            className="risk-bar-high"
                            style={{
                                width: `${highRiskPercentage}%`,
                            }}
                        ></div>

                    </div>

                    <div className="risk-legend">

                        <div
                            className="risk-legend-item risk-clickable"
                            onClick={onHealthyMachines}
                            role="button"
                            tabIndex={0}
                            onKeyDown={(event) => {
                                if (
                                    event.key === "Enter" ||
                                    event.key === " "
                                ) {
                                    onHealthyMachines();
                                }
                            }}
                        >

                            <span className="risk-dot healthy"></span>

                            <div>

                                <strong>
                                    {healthyMachines}
                                </strong>

                                <small>
                                    Healthy
                                </small>

                            </div>

                        </div>

                        <div
                            className="risk-legend-item risk-clickable"
                            onClick={onHighRiskMachines}
                            role="button"
                            tabIndex={0}
                            onKeyDown={(event) => {
                                if (
                                    event.key === "Enter" ||
                                    event.key === " "
                                ) {
                                    onHighRiskMachines();
                                }
                            }}
                        >

                            <span className="risk-dot high"></span>

                            <div>

                                <strong>
                                    {highRiskMachines}
                                </strong>

                                <small>
                                    Failure Flagged
                                </small>

                            </div>

                        </div>

                    </div>

                    <div className="risk-hint">
                        Click a category to view machines
                    </div>

                </div>

            </div>

            <div className="section-title">

                <div>

                    <h2>
                        System Intelligence
                    </h2>

                    <p>
                        Current SmartPulse monitoring status
                    </p>

                </div>

                <button
                    className="refresh-button"
                    onClick={loadDashboardData}
                >
                    Refresh
                </button>

            </div>

            <div className="monitor-grid">

                <div className="monitor-card">

                    <div className="card-heading">

                        <h3>
                            Data Quality
                        </h3>

                        <span className="badge stable">
              STABLE
            </span>

                    </div>

                    <p>
                        Machine records validated before entering
                        the intelligence pipeline.
                    </p>

                    <div className="progress">

                        <div
                            className="progress-fill"
                            style={{
                                width: `${qualityPercentage}%`,
                            }}
                        ></div>

                    </div>

                    <small>
                        {qualityPercentage.toFixed(2)}% valid
                        {" · "}
                        {validRecords.toLocaleString()}
                        {" / "}
                        {totalProcessed.toLocaleString()} records
                    </small>

                </div>

                <div className="monitor-card">

                    <div className="card-heading">

                        <h3>
                            Data Drift
                        </h3>

                        <span
                            className={`badge ${
                                dataDriftStatus.includes("DRIFT")
                                    ? "warning"
                                    : dataDriftStatus === "STABLE"
                                        ? "stable"
                                        : "info"
                            }`}
                        >
              {dataDriftStatus}
            </span>

                    </div>

                    <p>
                        Production sensor distributions are
                        continuously monitored.
                    </p>

                    <div className="metric-value">
                        {driftFeatures}
                    </div>

                    <small>
                        features showing drift
                    </small>

                </div>

                <div className="monitor-card">

                    <div className="card-heading">

                        <h3>
                            Model Health
                        </h3>

                        <span
                            className={`badge ${
                                modelDriftStatus.includes("DRIFT")
                                    ? "warning"
                                    : "stable"
                            }`}
                        >
              {modelDriftStatus}
            </span>

                    </div>

                    <p>
                        Current failure prediction model
                        performance.
                    </p>

                    <div className="metric-value">
                        {modelHealth.toFixed(1)}%
                    </div>

                    <small>
                        Current ROC-AUC
                    </small>

                </div>

                <div className="monitor-card">

                    <div className="card-heading">

                        <h3>
                            Learning Loop
                        </h3>

                        <span className="badge info">
              ACTIVE
            </span>

                    </div>

                    <p>
                        Maintenance outcomes are being collected
                        for future model improvement.
                    </p>

                    <div className="metric-value">
                        {feedbackRecords}
                    </div>

                    <small>
                        feedback records collected
                    </small>

                </div>

            </div>

        </section>
    );
}

export default Dashboard;