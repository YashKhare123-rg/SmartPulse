import { useEffect, useMemo, useState } from "react";
import axios from "axios";

function DriftMonitoring() {
    const [dataDrift, setDataDrift] = useState(null);
    const [modelDrift, setModelDrift] = useState(null);

    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState("");

    const fetchDriftData = async () => {
        try {
            setError("");

            const [dataResponse, modelResponse] =
                await Promise.all([
                    axios.get(
                        "http://localhost:8080/api/data-drift"
                    ),
                    axios.get(
                        "http://localhost:8080/api/model-drift"
                    )
                ]);

            setDataDrift(dataResponse.data);
            setModelDrift(modelResponse.data);
        } catch (err) {
            console.error(err);

            setError(
                "Unable to load drift information. Make sure Spring Boot and the ML service are running."
            );
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchDriftData();
    }, []);

    const handleRefresh = () => {
        setRefreshing(true);
        fetchDriftData();
    };

    const dataStatistics = useMemo(() => {
        const features = dataDrift?.features || [];

        const drifted = features.filter(
            (item) =>
                item.status?.toUpperCase() === "DRIFT"
        ).length;

        const warning = features.filter(
            (item) =>
                item.status?.toUpperCase() === "WARNING"
        ).length;

        const stable = features.filter(
            (item) =>
                item.status?.toUpperCase() === "STABLE"
        ).length;

        return {
            total: features.length,
            drifted,
            warning,
            stable
        };
    }, [dataDrift]);

    const modelStatistics = useMemo(() => {
        const metrics = modelDrift?.metrics || [];

        const drifted = metrics.filter(
            (item) =>
                item.status?.toUpperCase() === "DRIFT"
        ).length;

        const warning = metrics.filter(
            (item) =>
                item.status?.toUpperCase() === "WARNING"
        ).length;

        const stable = metrics.filter(
            (item) =>
                item.status?.toUpperCase() === "STABLE"
        ).length;

        return {
            total: metrics.length,
            drifted,
            warning,
            stable
        };
    }, [modelDrift]);

    const getStatusClass = (status) => {
        if (!status) {
            return "unknown";
        }

        const value = status.toUpperCase();

        if (value === "STABLE") {
            return "stable";
        }

        if (value === "WARNING") {
            return "warning";
        }

        if (value === "DRIFT") {
            return "drift";
        }

        return "unknown";
    };

    const formatStatus = (status) => {
        if (!status) {
            return "UNKNOWN";
        }

        return status
            .replaceAll("_", " ")
            .toLowerCase()
            .replace(/\b\w/g, (char) => char.toUpperCase());
    };

    const formatMetricName = (metric) => {
        if (!metric) {
            return "Unknown Metric";
        }

        return metric
            .replaceAll("_", " ")
            .replace(/\b\w/g, (char) => char.toUpperCase());
    };

    const formatPercentage = (value) => {
        if (value === null || value === undefined) {
            return "—";
        }

        return `${(Number(value) * 100).toFixed(2)}%`;
    };

    const formatPsi = (value) => {
        if (value === null || value === undefined) {
            return "—";
        }

        return Number(value).toFixed(4);
    };

    const overallDataStatus =
        dataDrift?.overallStatus || "UNKNOWN";

    const overallModelStatus =
        modelDrift?.overallStatus || "UNKNOWN";

    if (loading) {
        return (
            <div className="page-content">
                <div className="drift-loading">
                    <div className="drift-loading-spinner"></div>

                    <h3>
                        Loading Drift Monitoring
                    </h3>

                    <p>
                        SmartPulse is analyzing data and model stability.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="page-content">

            {/* PAGE HEADER */}

            <div className="page-header">
                <div>
                    <h2>
                        Drift Monitoring
                    </h2>

                    <p>
                        Monitor changes in incoming data and
                        machine-learning model performance.
                    </p>
                </div>

                <button
                    className="drift-refresh"
                    onClick={handleRefresh}
                    disabled={refreshing}
                >
                    {refreshing
                        ? "Refreshing..."
                        : "Refresh"}
                </button>
            </div>


            {/* ERROR */}

            {error && (
                <div className="drift-error">
                    {error}
                </div>
            )}


            {/* STATUS CARDS */}

            <div className="drift-status-grid">

                <div className="drift-status-card">
                    <div className="drift-status-top">
                        <span>
                            DATA DRIFT
                        </span>

                        <div
                            className={`drift-status-badge ${getStatusClass(
                                overallDataStatus
                            )}`}
                        >
                            {formatStatus(
                                overallDataStatus
                            )}
                        </div>
                    </div>

                    <strong>
                        {dataStatistics.drifted}
                    </strong>

                    <p>
                        Features showing significant distribution change
                    </p>

                    <div className="drift-card-footer">
                        <span>
                            {dataStatistics.total} monitored features
                        </span>

                        <span>
                            {dataStatistics.warning} warnings
                        </span>
                    </div>
                </div>


                <div className="drift-status-card">
                    <div className="drift-status-top">
                        <span>
                            MODEL DRIFT
                        </span>

                        <div
                            className={`drift-status-badge ${getStatusClass(
                                overallModelStatus
                            )}`}
                        >
                            {formatStatus(
                                overallModelStatus
                            )}
                        </div>
                    </div>

                    <strong>
                        {modelStatistics.drifted}
                    </strong>

                    <p>
                        Model metrics showing performance changes
                    </p>

                    <div className="drift-card-footer">
                        <span>
                            {modelStatistics.total} monitored metrics
                        </span>

                        <span>
                            {modelStatistics.warning} warnings
                        </span>
                    </div>
                </div>


                <div className="drift-status-card">
                    <div className="drift-status-top">
                        <span>
                            DATA STABILITY
                        </span>

                        <div className="drift-status-badge stable">
                            {dataStatistics.stable}
                            {" "}
                            Stable
                        </div>
                    </div>

                    <strong>
                        {dataStatistics.total > 0
                            ? Math.round(
                                (dataStatistics.stable /
                                    dataStatistics.total) *
                                100
                            )
                            : 0}
                        %
                    </strong>

                    <p>
                        Features currently within expected ranges
                    </p>
                </div>


                <div className="drift-status-card">
                    <div className="drift-status-top">
                        <span>
                            MODEL STABILITY
                        </span>

                        <div className="drift-status-badge stable">
                            {modelStatistics.stable}
                            {" "}
                            Stable
                        </div>
                    </div>

                    <strong>
                        {modelStatistics.total > 0
                            ? Math.round(
                                (modelStatistics.stable /
                                    modelStatistics.total) *
                                100
                            )
                            : 0}
                        %
                    </strong>

                    <p>
                        Model metrics within acceptable limits
                    </p>
                </div>

            </div>


            {/* MONITORING FLOW */}

            <div className="drift-flow-panel">

                <div className="drift-flow-header">
                    <div>
                        <span>
                            CONTINUOUS MONITORING
                        </span>

                        <h3>
                            SmartPulse Drift Detection Pipeline
                        </h3>

                        <p>
                            SmartPulse continuously checks whether
                            incoming machine data and model behavior
                            remain reliable.
                        </p>
                    </div>
                </div>

                <div className="drift-flow">

                    <div className="drift-flow-step">
                        <span>01</span>

                        <strong>
                            Incoming Data
                        </strong>

                        <small>
                            Machine sensor data enters the platform
                        </small>
                    </div>

                    <div className="drift-flow-arrow">
                        →
                    </div>

                    <div className="drift-flow-step">
                        <span>02</span>

                        <strong>
                            Data Drift
                        </strong>

                        <small>
                            Feature distributions are compared
                        </small>
                    </div>

                    <div className="drift-flow-arrow">
                        →
                    </div>

                    <div className="drift-flow-step">
                        <span>03</span>

                        <strong>
                            Model Drift
                        </strong>

                        <small>
                            Model performance is evaluated
                        </small>
                    </div>

                    <div className="drift-flow-arrow">
                        →
                    </div>

                    <div className="drift-flow-step">
                        <span>04</span>

                        <strong>
                            Model Validation
                        </strong>

                        <small>
                            Retraining can be triggered when required
                        </small>
                    </div>

                </div>
            </div>


            {/* DATA DRIFT */}

            <div className="drift-section">

                <div className="drift-section-header">

                    <div>
                        <span>
                            DATA QUALITY INTELLIGENCE
                        </span>

                        <h3>
                            Data Drift Analysis
                        </h3>

                        <p>
                            Population Stability Index values
                            indicate how much each feature has changed
                            compared with its reference distribution.
                        </p>
                    </div>

                    <div
                        className={`drift-section-status ${getStatusClass(
                            overallDataStatus
                        )}`}
                    >
                        {formatStatus(
                            overallDataStatus
                        )}
                    </div>

                </div>


                <div className="drift-feature-list">

                    {(dataDrift?.features || []).map(
                        (item, index) => (
                            <div
                                className="drift-feature-row"
                                key={`${item.feature}-${index}`}
                            >

                                <div className="drift-feature-name">
                                    <strong>
                                        {formatMetricName(
                                            item.feature
                                        )}
                                    </strong>

                                    <small>
                                        Population Stability Index
                                    </small>
                                </div>

                                <div className="drift-feature-psi">
                                    <span>
                                        PSI
                                    </span>

                                    <strong>
                                        {formatPsi(item.psi)}
                                    </strong>
                                </div>

                                <div
                                    className={`drift-row-status ${getStatusClass(
                                        item.status
                                    )}`}
                                >
                                    {formatStatus(
                                        item.status
                                    )}
                                </div>

                            </div>
                        )
                    )}

                </div>

            </div>


            {/* MODEL DRIFT */}

            <div className="drift-section">

                <div className="drift-section-header">

                    <div>
                        <span>
                            MODEL PERFORMANCE INTELLIGENCE
                        </span>

                        <h3>
                            Model Drift Analysis
                        </h3>

                        <p>
                            Current model metrics are compared
                            against their reference values to detect
                            performance degradation.
                        </p>
                    </div>

                    <div
                        className={`drift-section-status ${getStatusClass(
                            overallModelStatus
                        )}`}
                    >
                        {formatStatus(
                            overallModelStatus
                        )}
                    </div>

                </div>


                <div className="model-drift-list">

                    {(modelDrift?.metrics || []).map(
                        (item, index) => (
                            <div
                                className="model-drift-row"
                                key={`${item.metric}-${index}`}
                            >

                                <div className="model-metric-name">
                                    <strong>
                                        {formatMetricName(
                                            item.metric
                                        )}
                                    </strong>
                                </div>


                                <div className="model-metric-value">
                                    <span>
                                        Reference
                                    </span>

                                    <strong>
                                        {formatPercentage(
                                            item.referenceValue
                                        )}
                                    </strong>
                                </div>


                                <div className="model-metric-value">
                                    <span>
                                        Current
                                    </span>

                                    <strong>
                                        {formatPercentage(
                                            item.currentValue
                                        )}
                                    </strong>
                                </div>


                                <div className="model-metric-change">
                                    <span>
                                        Change
                                    </span>

                                    <strong
                                        className={
                                            item.relativeChange > 0
                                                ? "positive"
                                                : item.relativeChange < 0
                                                    ? "negative"
                                                    : ""
                                        }
                                    >
                                        {item.relativeChange > 0
                                            ? "+"
                                            : ""}
                                        {(
                                            Number(
                                                item.relativeChange
                                            ) * 100
                                        ).toFixed(2)}
                                        %
                                    </strong>
                                </div>


                                <div
                                    className={`drift-row-status ${getStatusClass(
                                        item.status
                                    )}`}
                                >
                                    {formatStatus(
                                        item.status
                                    )}
                                </div>

                            </div>
                        )
                    )}

                </div>

            </div>


            {/* SYSTEM RESPONSE */}

            <div className="drift-response-panel">

                <div className="drift-response-icon">
                    !
                </div>

                <div>
                    <span>
                        SELF-HEALING RESPONSE
                    </span>

                    <h3>
                        Drift-aware decision making
                    </h3>

                    <p>
                        Drift information is incorporated into
                        SmartPulse risk scoring and maintenance
                        decisions. Significant model drift can
                        require model validation before high-risk
                        decisions are executed.
                    </p>
                </div>

            </div>

        </div>
    );
}

export default DriftMonitoring;