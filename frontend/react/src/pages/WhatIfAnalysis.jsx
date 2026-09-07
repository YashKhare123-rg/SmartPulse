import { useState } from "react";
import axios from "axios";

function WhatIfAnalysis() {
    const [inputs, setInputs] = useState({
        machineId: "M001",
        temperature: 88,
        vibration: 5.2,
        pressure: 6.7,
        powerConsumption: 10,
        operatingHours: 2340,
        loadPercentage: 80,
        rotationSpeed: 1620,
        maintenanceCount: 1,
        machineAge: 9,
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (event) => {
        const { name, value } = event.target;

        setInputs((previous) => ({
            ...previous,
            [name]:
                name === "machineId"
                    ? value.toUpperCase()
                    : Number(value),
        }));
    };

    const runSimulation = async () => {
        try {
            setLoading(true);
            setError("");
            setResult(null);

            const response = await axios.post(
                "http://localhost:8080/api/decision/what-if",
                inputs
            );

            setResult(response.data);
        } catch (err) {
            console.error(err);

            setError(
                "Unable to run what-if simulation. Make sure Spring Boot and the ML service are running."
            );
        } finally {
            setLoading(false);
        }
    };

    const resetSimulation = () => {
        setInputs({
            machineId: "M001",
            temperature: 88,
            vibration: 5.2,
            pressure: 6.7,
            powerConsumption: 10,
            operatingHours: 2340,
            loadPercentage: 80,
            rotationSpeed: 1620,
            maintenanceCount: 1,
            machineAge: 9,
        });

        setResult(null);
        setError("");
    };

    return (
        <div className="page-content">
            <div className="page-header">
                <div>
                    <h2>What-If Analysis</h2>

                    <p>
                        Simulate machine conditions and evaluate potential
                        failure risk and maintenance decisions.
                    </p>
                </div>
            </div>

            <div className="whatif-layout">
                <div className="whatif-input-card">
                    <div className="whatif-card-title">
                        <span>SIMULATION INPUT</span>

                        <h3>Machine Conditions</h3>
                    </div>

                    <div className="whatif-form">
                        <div className="whatif-field">
                            <label>Machine ID</label>

                            <input
                                type="text"
                                name="machineId"
                                value={inputs.machineId}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Temperature (°C)</label>

                            <input
                                type="number"
                                name="temperature"
                                value={inputs.temperature}
                                onChange={handleChange}
                                step="0.1"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Vibration</label>

                            <input
                                type="number"
                                name="vibration"
                                value={inputs.vibration}
                                onChange={handleChange}
                                step="0.1"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Pressure</label>

                            <input
                                type="number"
                                name="pressure"
                                value={inputs.pressure}
                                onChange={handleChange}
                                step="0.1"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Power Consumption</label>

                            <input
                                type="number"
                                name="powerConsumption"
                                value={inputs.powerConsumption}
                                onChange={handleChange}
                                step="0.1"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Operating Hours</label>

                            <input
                                type="number"
                                name="operatingHours"
                                value={inputs.operatingHours}
                                onChange={handleChange}
                                step="1"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Load Percentage</label>

                            <input
                                type="number"
                                name="loadPercentage"
                                value={inputs.loadPercentage}
                                onChange={handleChange}
                                step="0.1"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Rotation Speed (RPM)</label>

                            <input
                                type="number"
                                name="rotationSpeed"
                                value={inputs.rotationSpeed}
                                onChange={handleChange}
                                step="1"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Maintenance Count</label>

                            <input
                                type="number"
                                name="maintenanceCount"
                                value={inputs.maintenanceCount}
                                onChange={handleChange}
                                step="1"
                                min="0"
                            />
                        </div>

                        <div className="whatif-field">
                            <label>Machine Age</label>

                            <input
                                type="number"
                                name="machineAge"
                                value={inputs.machineAge}
                                onChange={handleChange}
                                step="1"
                                min="0"
                            />
                        </div>
                    </div>

                    <div className="whatif-buttons">
                        <button
                            className="whatif-run-button"
                            onClick={runSimulation}
                            disabled={loading}
                        >
                            {loading ? "Simulating..." : "Run Simulation"}
                        </button>

                        <button
                            className="whatif-reset-button"
                            onClick={resetSimulation}
                        >
                            Reset
                        </button>
                    </div>
                </div>

                <div className="whatif-result-card">
                    <div className="whatif-card-title">
                        <span>SIMULATION RESULT</span>

                        <h3>
                            {result
                                ? result.machineId
                                : "Awaiting Simulation"}
                        </h3>
                    </div>

                    {error && (
                        <div className="prediction-error">
                            {error}
                        </div>
                    )}

                    {!result && !error && (
                        <div className="whatif-empty">
                            Change the machine conditions and run a simulation
                            to see how SmartPulse responds.
                        </div>
                    )}

                    {result && (
                        <>
                            <div className="whatif-result-grid">
                                <div className="whatif-result-item">
                                    <span>Failure Probability</span>

                                    <strong>
                                        {(result.failureProbability * 100).toFixed(2)}%
                                    </strong>
                                </div>

                                <div className="whatif-result-item">
                                    <span>Risk Score</span>

                                    <strong>
                                        {Number(result.riskScore).toFixed(2)}
                                    </strong>
                                </div>

                                <div className="whatif-result-item">
                                    <span>Risk Level</span>

                                    <strong>
                                        {result.riskLevel}
                                    </strong>
                                </div>

                                <div className="whatif-result-item">
                                    <span>Priority</span>

                                    <strong>
                                        {result.priority}
                                    </strong>
                                </div>
                            </div>

                            <div className="whatif-analysis">
                                <div>
                                    <span>Expected Failure Cost</span>

                                    <strong>
                                        $
                                        {Number(
                                            result.totalExpectedFailureCost
                                        ).toFixed(2)}
                                    </strong>
                                </div>

                                <div>
                                    <span>Preventive Maintenance</span>

                                    <strong>
                                        $
                                        {Number(
                                            result.preventiveMaintenanceCost
                                        ).toFixed(2)}
                                    </strong>
                                </div>

                                <div>
                                    <span>Potential Savings</span>

                                    <strong>
                                        $
                                        {Number(
                                            result.potentialSavings
                                        ).toFixed(2)}
                                    </strong>
                                </div>

                                <div>
                                    <span>Cost Decision</span>

                                    <strong>
                                        {result.costDecision}
                                    </strong>
                                </div>
                            </div>

                            <div className="whatif-final">
                                <span>FINAL DECISION</span>

                                <h2>
                                    {result.finalDecision}
                                </h2>

                                <p>
                                    {result.finalReason}
                                </p>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

export default WhatIfAnalysis;