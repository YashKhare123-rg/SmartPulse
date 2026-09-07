import { useEffect, useMemo, useState } from "react";
import axios from "axios";

function Predictions() {
    const [machines, setMachines] = useState([]);
    const [machineId, setMachineId] = useState("M001");
    const [prediction, setPrediction] = useState(null);
    const [explanation, setExplanation] = useState(null);

    const [loading, setLoading] = useState(false);
    const [loadingExplanation, setLoadingExplanation] = useState(false);
    const [loadingMachines, setLoadingMachines] = useState(true);

    const [whatIfLoading, setWhatIfLoading] = useState(false);
    const [whatIfResult, setWhatIfResult] = useState(null);

    const [error, setError] = useState("");

    const [whatIfValues, setWhatIfValues] = useState({
        temperature: 0,
        vibration: 0,
        pressure: 0,
        powerConsumption: 0,
        loadPercentage: 0
    });

    useEffect(() => {
        const fetchMachines = async () => {
            try {
                setLoadingMachines(true);
                setError("");

                const response = await axios.get(
                    "http://localhost:8080/api/machines"
                );

                const data = response.data;

                const latestRecords = {};

                data.forEach((record) => {
                    const id = record.machine_id;

                    if (
                        !latestRecords[id] ||
                        new Date(record.timestamp) >
                        new Date(latestRecords[id].timestamp)
                    ) {
                        latestRecords[id] = record;
                    }
                });

                const machineList = Object.values(latestRecords).sort(
                    (a, b) =>
                        a.machine_id.localeCompare(
                            b.machine_id,
                            undefined,
                            { numeric: true }
                        )
                );

                setMachines(machineList);

                if (machineList.length > 0) {
                    setMachineId(machineList[0].machine_id);
                }
            } catch (err) {
                console.error(err);

                setError(
                    "Unable to load machine list. Make sure Spring Boot is running."
                );
            } finally {
                setLoadingMachines(false);
            }
        };

        fetchMachines();
    }, []);

    const selectedMachine = useMemo(() => {
        return machines.find(
            (machine) => machine.machine_id === machineId
        );
    }, [machines, machineId]);

    useEffect(() => {
        if (selectedMachine) {
            setWhatIfValues({
                temperature: selectedMachine.temperature,
                vibration: selectedMachine.vibration,
                pressure: selectedMachine.pressure,
                powerConsumption: selectedMachine.power_consumption,
                loadPercentage: selectedMachine.load_percentage
            });

            setWhatIfResult(null);
        }
    }, [selectedMachine]);

    const runPrediction = async () => {
        if (!machineId) {
            setError("Please select a machine.");
            return;
        }

        setLoading(true);
        setLoadingExplanation(true);
        setError("");
        setPrediction(null);
        setExplanation(null);
        setWhatIfResult(null);

        try {
            const predictionResponse = await axios.post(
                `http://localhost:8080/api/decision/${machineId}`
            );

            setPrediction(predictionResponse.data);

            try {
                const explanationResponse = await axios.post(
                    `http://localhost:8080/api/decision/${machineId}/explain`
                );

                setExplanation(explanationResponse.data);
            } catch (explainError) {
                console.error(
                    "XAI explanation error:",
                    explainError
                );
            }
        } catch (err) {
            console.error(err);

            setError(
                "Unable to generate prediction. Make sure Spring Boot and the ML service are running."
            );
        } finally {
            setLoading(false);
            setLoadingExplanation(false);
        }
    };

    const handleWhatIfChange = (field, value) => {
        setWhatIfValues((previous) => ({
            ...previous,
            [field]: Number(value)
        }));

        setWhatIfResult(null);
    };

    const resetWhatIf = () => {
        if (!selectedMachine) {
            return;
        }

        setWhatIfValues({
            temperature: selectedMachine.temperature,
            vibration: selectedMachine.vibration,
            pressure: selectedMachine.pressure,
            powerConsumption: selectedMachine.power_consumption,
            loadPercentage: selectedMachine.load_percentage
        });

        setWhatIfResult(null);
    };

    const runWhatIfAnalysis = async () => {
        if (!selectedMachine) {
            setError("Please select a machine first.");
            return;
        }

        setWhatIfLoading(true);
        setError("");
        setWhatIfResult(null);

        try {
            const request = {
                machineId: selectedMachine.machine_id,
                temperature: whatIfValues.temperature,
                vibration: whatIfValues.vibration,
                pressure: whatIfValues.pressure,
                powerConsumption: whatIfValues.powerConsumption,
                operatingHours: selectedMachine.operating_hours,
                loadPercentage: whatIfValues.loadPercentage,
                rotationSpeed: selectedMachine.rotation_speed,
                maintenanceCount: selectedMachine.maintenance_count,
                machineAge: selectedMachine.machine_age
            };

            const response = await axios.post(
                "http://localhost:8080/api/decision/what-if",
                request
            );

            setWhatIfResult(response.data);
        } catch (err) {
            console.error(err);

            setError(
                "Unable to run What-If analysis. Make sure Spring Boot and the ML service are running."
            );
        } finally {
            setWhatIfLoading(false);
        }
    };

    const probabilityDifference =
        prediction && whatIfResult
            ? (whatIfResult.failureProbability -
                prediction.failureProbability) *
            100
            : null;

    const riskDifference =
        prediction && whatIfResult
            ? whatIfResult.riskScore - prediction.riskScore
            : null;

    const getChangeClass = (value) => {
        if (value < 0) {
            return "improved";
        }

        if (value > 0) {
            return "worsened";
        }

        return "unchanged";
    };

    const formatFeatureName = (feature) => {
        return feature
            .replaceAll("_", " ")
            .replace(/\b\w/g, (char) =>
                char.toUpperCase()
            );
    };

    return (
        <div className="page-content">
            <div className="page-header">
                <div>
                    <h2>Failure Prediction</h2>

                    <p>
                        AI-powered machine failure prediction and
                        risk analysis.
                    </p>
                </div>
            </div>

            <div className="prediction-control">
                <div className="machine-input">
                    <label>Machine ID</label>

                    <select
                        value={machineId}
                        onChange={(event) => {
                            setMachineId(event.target.value);
                            setPrediction(null);
                            setExplanation(null);
                            setWhatIfResult(null);
                            setError("");
                        }}
                        disabled={loadingMachines}
                    >
                        {loadingMachines ? (
                            <option>
                                Loading machines...
                            </option>
                        ) : (
                            machines.map((machine) => (
                                <option
                                    key={machine.machine_id}
                                    value={machine.machine_id}
                                >
                                    {machine.machine_id}
                                </option>
                            ))
                        )}
                    </select>
                </div>

                <button
                    className="prediction-button"
                    onClick={runPrediction}
                    disabled={
                        loading ||
                        loadingMachines ||
                        !machineId ||
                        machines.length === 0
                    }
                >
                    {loading
                        ? "Analyzing..."
                        : "Run Prediction"}
                </button>
            </div>

            {selectedMachine && (
                <div className="prediction-machine-info">
                    <div>
                        <span>Latest Temperature</span>
                        <strong>
                            {selectedMachine.temperature.toFixed(2)} °C
                        </strong>
                    </div>

                    <div>
                        <span>Vibration</span>
                        <strong>
                            {selectedMachine.vibration.toFixed(2)}
                        </strong>
                    </div>

                    <div>
                        <span>Load</span>
                        <strong>
                            {selectedMachine.load_percentage.toFixed(2)}%
                        </strong>
                    </div>

                    <div>
                        <span>Power Consumption</span>
                        <strong>
                            {selectedMachine.power_consumption.toFixed(2)}
                        </strong>
                    </div>
                </div>
            )}

            {error && (
                <div className="prediction-error">
                    {error}
                </div>
            )}

            {prediction && (
                <div className="prediction-results">
                    <div className="prediction-title">
                        <div>
                            <span>Prediction Result</span>

                            <h3>
                                {prediction.machineId}
                            </h3>
                        </div>

                        <div
                            className={`risk-badge ${prediction.riskLevel
                                .toLowerCase()
                                .replace(" ", "-")}`}
                        >
                            {prediction.riskLevel}
                        </div>
                    </div>

                    <div className="prediction-grid">
                        <div className="prediction-card">
                            <span>
                                Failure Probability
                            </span>

                            <strong>
                                {(
                                    prediction.failureProbability *
                                    100
                                ).toFixed(2)}
                                %
                            </strong>

                            <small>
                                AI model prediction
                            </small>
                        </div>

                        <div className="prediction-card">
                            <span>
                                Risk Score
                            </span>

                            <strong>
                                {prediction.riskScore.toFixed(2)}
                            </strong>

                            <small>
                                Overall SmartPulse risk
                            </small>
                        </div>

                        <div className="prediction-card">
                            <span>
                                Risk Level
                            </span>

                            <strong>
                                {prediction.riskLevel}
                            </strong>

                            <small>
                                Priority:{" "}
                                {prediction.priority}
                            </small>
                        </div>
                    </div>

                    <div className="analysis-grid">
                        <div className="analysis-card">
                            <h3>
                                System Intelligence
                            </h3>

                            <div className="analysis-row">
                                <span>Data Drift</span>

                                <strong>
                                    {prediction.dataDriftStatus}
                                </strong>
                            </div>

                            <div className="analysis-row">
                                <span>Model Drift</span>

                                <strong>
                                    {prediction.modelDriftStatus}
                                </strong>
                            </div>

                            <div className="analysis-row">
                                <span>Priority</span>

                                <strong>
                                    {prediction.priority}
                                </strong>
                            </div>

                            <div className="analysis-row">
                                <span>Recommendation</span>

                                <strong>
                                    {prediction.recommendation}
                                </strong>
                            </div>
                        </div>

                        <div className="analysis-card">
                            <h3>
                                Cost Analysis
                            </h3>

                            <div className="analysis-row">
                                <span>
                                    Expected Failure Cost
                                </span>

                                <strong>
                                    $
                                    {prediction.totalExpectedFailureCost.toFixed(
                                        2
                                    )}
                                </strong>
                            </div>

                            <div className="analysis-row">
                                <span>
                                    Preventive Maintenance
                                </span>

                                <strong>
                                    $
                                    {prediction.preventiveMaintenanceCost.toFixed(
                                        2
                                    )}
                                </strong>
                            </div>

                            <div className="analysis-row">
                                <span>
                                    Potential Savings
                                </span>

                                <strong>
                                    $
                                    {prediction.potentialSavings.toFixed(
                                        2
                                    )}
                                </strong>
                            </div>

                            <div className="analysis-row">
                                <span>
                                    Cost Decision
                                </span>

                                <strong>
                                    {prediction.costDecision}
                                </strong>
                            </div>
                        </div>
                    </div>

                    <div className="final-decision">
                        <span>
                            FINAL DECISION
                        </span>

                        <h2>
                            {prediction.finalDecision}
                        </h2>

                        <p>
                            {prediction.finalReason}
                        </p>
                    </div>

                    {loadingExplanation && (
                        <div className="xai-loading">
                            <span>EXPLAINABLE AI</span>

                            <h3>
                                Analyzing prediction factors...
                            </h3>

                            <p>
                                SmartPulse is determining which
                                machine conditions influenced the
                                prediction.
                            </p>
                        </div>
                    )}

                    {explanation && (
                        <div className="xai-section">
                            <div className="xai-header">
                                <div>
                                    <span>
                                        EXPLAINABLE AI
                                    </span>

                                    <h3>
                                        Why is this machine at risk?
                                    </h3>

                                    <p>
                                        The AI model identifies the
                                        sensor factors that increase
                                        or decrease the predicted
                                        failure risk.
                                    </p>
                                </div>

                                <div className="xai-probability">
                                    <span>
                                        AI Probability
                                    </span>

                                    <strong>
                                        {(
                                            explanation.failure_probability *
                                            100
                                        ).toFixed(2)}
                                        %
                                    </strong>
                                </div>
                            </div>

                            <div className="xai-features">
                                {explanation.explanations.map(
                                    (item) => (
                                        <div
                                            className={`xai-feature ${item.impact.toLowerCase()}`}
                                            key={item.feature}
                                        >
                                            <div className="xai-feature-top">
                                                <div>
                                                    <span className="xai-feature-name">
                                                        {formatFeatureName(
                                                            item.feature
                                                        )}
                                                    </span>

                                                    <strong>
                                                        {typeof item.value ===
                                                        "number"
                                                            ? item.value.toFixed(
                                                                2
                                                            )
                                                            : item.value}
                                                    </strong>
                                                </div>

                                                <span className="xai-impact">
                                                    {item.impact}
                                                </span>
                                            </div>

                                            <div className="xai-feature-bottom">
                                                <span>
                                                    {item.direction ===
                                                    "INCREASES_FAILURE_RISK"
                                                        ? "Increases failure risk"
                                                        : "Decreases failure risk"}
                                                </span>

                                                <strong>
                                                    {item.contribution >
                                                    0
                                                        ? "+"
                                                        : ""}
                                                    {item.contribution.toFixed(
                                                        3
                                                    )}
                                                </strong>
                                            </div>
                                        </div>
                                    )
                                )}
                            </div>
                        </div>
                    )}

                    <div className="what-if-section">
                        <div className="what-if-header">
                            <div>
                                <span>
                                    WHAT-IF SIMULATOR
                                </span>

                                <h3>
                                    Explore different machine conditions
                                </h3>

                                <p>
                                    Change operating conditions to
                                    see how SmartPulse would respond.
                                    No maintenance action will be
                                    created by this simulation.
                                </p>
                            </div>
                        </div>

                        <div className="what-if-grid">
                            <div className="what-if-input">
                                <label>
                                    Temperature
                                </label>

                                <div className="what-if-value">
                                    <input
                                        type="number"
                                        step="0.1"
                                        value={whatIfValues.temperature}
                                        onChange={(event) =>
                                            handleWhatIfChange(
                                                "temperature",
                                                event.target.value
                                            )
                                        }
                                    />

                                    <span>°C</span>
                                </div>
                            </div>

                            <div className="what-if-input">
                                <label>
                                    Vibration
                                </label>

                                <div className="what-if-value">
                                    <input
                                        type="number"
                                        step="0.1"
                                        value={whatIfValues.vibration}
                                        onChange={(event) =>
                                            handleWhatIfChange(
                                                "vibration",
                                                event.target.value
                                            )
                                        }
                                    />

                                    <span>units</span>
                                </div>
                            </div>

                            <div className="what-if-input">
                                <label>
                                    Pressure
                                </label>

                                <div className="what-if-value">
                                    <input
                                        type="number"
                                        step="0.1"
                                        value={whatIfValues.pressure}
                                        onChange={(event) =>
                                            handleWhatIfChange(
                                                "pressure",
                                                event.target.value
                                            )
                                        }
                                    />

                                    <span>units</span>
                                </div>
                            </div>

                            <div className="what-if-input">
                                <label>
                                    Power Consumption
                                </label>

                                <div className="what-if-value">
                                    <input
                                        type="number"
                                        step="0.1"
                                        value={
                                            whatIfValues.powerConsumption
                                        }
                                        onChange={(event) =>
                                            handleWhatIfChange(
                                                "powerConsumption",
                                                event.target.value
                                            )
                                        }
                                    />

                                    <span>units</span>
                                </div>
                            </div>

                            <div className="what-if-input">
                                <label>
                                    Load Percentage
                                </label>

                                <div className="what-if-value">
                                    <input
                                        type="number"
                                        min="0"
                                        max="100"
                                        step="0.1"
                                        value={
                                            whatIfValues.loadPercentage
                                        }
                                        onChange={(event) =>
                                            handleWhatIfChange(
                                                "loadPercentage",
                                                event.target.value
                                            )
                                        }
                                    />

                                    <span>%</span>
                                </div>
                            </div>
                        </div>

                        <div className="what-if-actions">
                            <button
                                className="what-if-reset"
                                onClick={resetWhatIf}
                                disabled={whatIfLoading}
                            >
                                Reset Values
                            </button>

                            <button
                                className="what-if-button"
                                onClick={runWhatIfAnalysis}
                                disabled={whatIfLoading}
                            >
                                {whatIfLoading
                                    ? "Simulating..."
                                    : "Run What-If Analysis"}
                            </button>
                        </div>

                        {whatIfResult && (
                            <div className="what-if-result">
                                <div className="what-if-result-header">
                                    <div>
                                        <span>
                                            SIMULATION RESULT
                                        </span>

                                        <h3>
                                            {whatIfResult.machineId}
                                        </h3>
                                    </div>

                                    <div
                                        className={`what-if-status ${getChangeClass(
                                            probabilityDifference
                                        )}`}
                                    >
                                        {probabilityDifference < 0
                                            ? "RISK IMPROVED"
                                            : probabilityDifference > 0
                                                ? "RISK INCREASED"
                                                : "RISK UNCHANGED"}
                                    </div>
                                </div>

                                <div className="what-if-comparison">
                                    <div className="comparison-card">
                                        <span>
                                            Current Probability
                                        </span>

                                        <strong>
                                            {(
                                                prediction.failureProbability *
                                                100
                                            ).toFixed(2)}
                                            %
                                        </strong>
                                    </div>

                                    <div className="comparison-arrow">
                                        →
                                    </div>

                                    <div className="comparison-card simulated">
                                        <span>
                                            Simulated Probability
                                        </span>

                                        <strong>
                                            {(
                                                whatIfResult.failureProbability *
                                                100
                                            ).toFixed(2)}
                                            %
                                        </strong>
                                    </div>
                                </div>

                                <div className="what-if-metrics">
                                    <div>
                                        <span>
                                            Probability Change
                                        </span>

                                        <strong
                                            className={getChangeClass(
                                                probabilityDifference
                                            )}
                                        >
                                            {probabilityDifference > 0
                                                ? "+"
                                                : ""}
                                            {probabilityDifference.toFixed(
                                                2
                                            )}
                                            %
                                        </strong>
                                    </div>

                                    <div>
                                        <span>
                                            Current Risk Score
                                        </span>

                                        <strong>
                                            {prediction.riskScore.toFixed(
                                                2
                                            )}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>
                                            Simulated Risk Score
                                        </span>

                                        <strong>
                                            {whatIfResult.riskScore.toFixed(
                                                2
                                            )}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>
                                            Risk Score Change
                                        </span>

                                        <strong
                                            className={getChangeClass(
                                                riskDifference
                                            )}
                                        >
                                            {riskDifference > 0
                                                ? "+"
                                                : ""}
                                            {riskDifference.toFixed(2)}
                                        </strong>
                                    </div>
                                </div>

                                <div className="what-if-analysis">
                                    <div>
                                        <span>
                                            Simulated Risk Level
                                        </span>

                                        <strong>
                                            {whatIfResult.riskLevel}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>
                                            Recommendation
                                        </span>

                                        <strong>
                                            {whatIfResult.recommendation}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>
                                            Final Decision
                                        </span>

                                        <strong>
                                            {whatIfResult.finalDecision}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>
                                            Reason
                                        </span>

                                        <strong>
                                            {whatIfResult.finalReason}
                                        </strong>
                                    </div>
                                </div>

                                <div className="what-if-cost">
                                    <h4>
                                        Simulated Cost Analysis
                                    </h4>

                                    <div className="what-if-cost-grid">
                                        <div>
                                            <span>
                                                Expected Failure Cost
                                            </span>

                                            <strong>
                                                $
                                                {whatIfResult.totalExpectedFailureCost.toFixed(
                                                    2
                                                )}
                                            </strong>
                                        </div>

                                        <div>
                                            <span>
                                                Preventive Maintenance
                                            </span>

                                            <strong>
                                                $
                                                {whatIfResult.preventiveMaintenanceCost.toFixed(
                                                    2
                                                )}
                                            </strong>
                                        </div>

                                        <div>
                                            <span>
                                                Potential Savings
                                            </span>

                                            <strong>
                                                $
                                                {whatIfResult.potentialSavings.toFixed(
                                                    2
                                                )}
                                            </strong>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Predictions;