import { useState } from "react";
import axios from "axios";

function Retraining() {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const executeRetraining = async () => {
        try {
            setLoading(true);
            setError("");
            setResult(null);

            const response = await axios.post(
                "http://localhost:8080/api/retraining/execute"
            );

            setResult(response.data);
        } catch (err) {
            console.error(err);

            setError(
                "Unable to execute retraining. Make sure Spring Boot and the ML service are running."
            );
        } finally {
            setLoading(false);
        }
    };

    const formatKey = (key) => {
        return key
            .replaceAll("_", " ")
            .replace(/([a-z])([A-Z])/g, "$1 $2")
            .replace(/\b\w/g, (char) =>
                char.toUpperCase()
            );
    };

    const formatValue = (value) => {
        if (value === null || value === undefined) {
            return "—";
        }

        if (typeof value === "boolean") {
            return value ? "Yes" : "No";
        }

        if (typeof value === "number") {
            return Number.isInteger(value)
                ? value
                : value.toFixed(4);
        }

        return String(value);
    };

    const getResultStatus = () => {
        if (!result) {
            return null;
        }

        if (
            result.success === true ||
            result.accepted === true ||
            result.retrainingRequired === false
        ) {
            return "success";
        }

        if (
            result.success === false ||
            result.accepted === false
        ) {
            return "failed";
        }

        return "info";
    };

    const resultStatus = getResultStatus();

    return (
        <div className="page-content">

            {/* PAGE HEADER */}

            <div className="page-header">
                <div>
                    <h2>
                        Model Retraining
                    </h2>

                    <p>
                        Evaluate new model candidates and safely
                        update the active prediction model.
                    </p>
                </div>

                <button
                    className="retraining-button"
                    onClick={executeRetraining}
                    disabled={loading}
                >
                    {loading
                        ? "Running Retraining..."
                        : "Execute Retraining"}
                </button>
            </div>


            {/* MODEL LIFECYCLE */}

            <div className="retraining-lifecycle">

                <div className="retraining-lifecycle-header">
                    <span>
                        SELF-HEALING MODEL LIFECYCLE
                    </span>

                    <h3>
                        Safe Model Improvement
                    </h3>

                    <p>
                        SmartPulse does not automatically replace
                        the active model with every retrained model.
                        Candidate models are evaluated before
                        promotion.
                    </p>
                </div>

                <div className="retraining-flow">

                    <div className="retraining-step">
                        <span>01</span>

                        <strong>
                            Feedback
                        </strong>

                        <small>
                            Collect real maintenance outcomes
                        </small>
                    </div>

                    <div className="retraining-arrow">
                        →
                    </div>

                    <div className="retraining-step">
                        <span>02</span>

                        <strong>
                            Retrain
                        </strong>

                        <small>
                            Train a candidate model
                        </small>
                    </div>

                    <div className="retraining-arrow">
                        →
                    </div>

                    <div className="retraining-step">
                        <span>03</span>

                        <strong>
                            Evaluate
                        </strong>

                        <small>
                            Compare candidate against current model
                        </small>
                    </div>

                    <div className="retraining-arrow">
                        →
                    </div>

                    <div className="retraining-step">
                        <span>04</span>

                        <strong>
                            Promote
                        </strong>

                        <small>
                            Activate only if safety criteria pass
                        </small>
                    </div>

                </div>
            </div>


            {/* RETRAINING CONTROL */}

            <div className="retraining-control">

                <div>
                    <span>
                        MODEL MANAGEMENT
                    </span>

                    <h3>
                        Retraining Control
                    </h3>

                    <p>
                        Execute the backend retraining workflow.
                        The system evaluates the candidate model
                        before allowing promotion.
                    </p>
                </div>

                <button
                    className="retraining-main-button"
                    onClick={executeRetraining}
                    disabled={loading}
                >
                    {loading
                        ? "Processing..."
                        : "Run Model Evaluation"}
                </button>

            </div>


            {/* ERROR */}

            {error && (
                <div className="retraining-error">
                    {error}
                </div>
            )}


            {/* RESULT */}

            {result && (
                <div
                    className={`retraining-result ${resultStatus}`}
                >

                    <div className="retraining-result-header">
                        <div>
                            <span>
                                RETRAINING RESULT
                            </span>

                            <h3>
                                Evaluation Complete
                            </h3>
                        </div>

                        <div
                            className={`retraining-result-badge ${resultStatus}`}
                        >
                            {resultStatus === "success"
                                ? "SUCCESS"
                                : resultStatus === "failed"
                                    ? "FAILED"
                                    : "COMPLETED"}
                        </div>
                    </div>


                    <div className="retraining-result-grid">

                        {Object.entries(result).map(
                            ([key, value]) => (
                                <div
                                    className="retraining-result-item"
                                    key={key}
                                >
                                    <span>
                                        {formatKey(key)}
                                    </span>

                                    <strong>
                                        {formatValue(value)}
                                    </strong>
                                </div>
                            )
                        )}

                    </div>

                </div>
            )}


            {/* EXPLANATION */}

            <div className="retraining-safety">

                <div className="retraining-safety-icon">
                    ✓
                </div>

                <div>
                    <span>
                        SAFE MODEL PROMOTION
                    </span>

                    <h3>
                        Existing model remains protected
                    </h3>

                    <p>
                        A retrained model should only become the
                        active model after passing the configured
                        evaluation and promotion criteria. This
                        prevents model degradation from being
                        introduced into production.
                    </p>
                </div>

            </div>

        </div>
    );
}

export default Retraining;