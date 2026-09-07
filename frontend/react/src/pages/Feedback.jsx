import { useEffect, useMemo, useState } from "react";
import axios from "axios";

function Feedback() {
    const [feedback, setFeedback] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const fetchFeedback = async () => {
        try {
            setLoading(true);
            setError("");

            const response = await axios.get(
                "http://localhost:8080/api/feedback"
            );

            setFeedback(response.data);
        } catch (err) {
            console.error(err);

            setError(
                "Unable to load feedback. Make sure Spring Boot is running."
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFeedback();
    }, []);

    const statistics = useMemo(() => {
        const total = feedback.length;

        const successful = feedback.filter(
            (item) =>
                item.actualOutcome === "MAINTENANCE_SUCCESSFUL"
        ).length;

        const failed = feedback.filter(
            (item) =>
                item.actualOutcome === "MAINTENANCE_FAILED" ||
                item.actualOutcome === "FAILURE_OCCURRED"
        ).length;

        const successRate =
            total > 0
                ? (successful / total) * 100
                : 0;

        return {
            total,
            successful,
            failed,
            successRate
        };
    }, [feedback]);

    const getOutcomeClass = (outcome) => {
        if (!outcome) {
            return "";
        }

        if (outcome === "MAINTENANCE_SUCCESSFUL") {
            return "successful";
        }

        if (
            outcome === "MAINTENANCE_FAILED" ||
            outcome === "FAILURE_OCCURRED"
        ) {
            return "failed";
        }

        return "unknown";
    };

    const formatOutcome = (outcome) => {
        if (!outcome) {
            return "UNKNOWN";
        }

        return outcome
            .replaceAll("_", " ")
            .toLowerCase()
            .replace(/\b\w/g, (char) =>
                char.toUpperCase()
            );
    };

    const formatDate = (date) => {
        if (!date) {
            return "—";
        }

        return new Date(date).toLocaleString();
    };

    return (
        <div className="page-content">
            <div className="page-header">
                <div>
                    <h2>Learning Loop</h2>

                    <p>
                        Monitor maintenance outcomes and SmartPulse
                        feedback used for continuous learning.
                    </p>
                </div>

                <button
                    className="feedback-refresh"
                    onClick={fetchFeedback}
                    disabled={loading}
                >
                    {loading ? "Refreshing..." : "Refresh"}
                </button>
            </div>

            <div className="feedback-summary">
                <div className="feedback-summary-card">
                    <span>Total Feedback</span>

                    <strong>
                        {statistics.total}
                    </strong>

                    <small>
                        Recorded maintenance outcomes
                    </small>
                </div>

                <div className="feedback-summary-card">
                    <span>Successful</span>

                    <strong>
                        {statistics.successful}
                    </strong>

                    <small>
                        Maintenance completed successfully
                    </small>
                </div>

                <div className="feedback-summary-card">
                    <span>Failed</span>

                    <strong>
                        {statistics.failed}
                    </strong>

                    <small>
                        Failures or unsuccessful maintenance
                    </small>
                </div>

                <div className="feedback-summary-card">
                    <span>Success Rate</span>

                    <strong>
                        {statistics.successRate.toFixed(1)}%
                    </strong>

                    <small>
                        Observed maintenance performance
                    </small>
                </div>
            </div>

            <div className="learning-loop-panel">
                <div className="learning-loop-header">
                    <div>
                        <span>
                            SELF-LEARNING PIPELINE
                        </span>

                        <h3>
                            From Maintenance to Model Learning
                        </h3>

                        <p>
                            SmartPulse records real maintenance
                            outcomes so future model decisions can
                            be evaluated against what actually
                            happened.
                        </p>
                    </div>
                </div>

                <div className="learning-flow">
                    <div className="learning-step">
                        <span className="learning-number">
                            01
                        </span>

                        <strong>
                            AI Prediction
                        </strong>

                        <small>
                            Failure probability is generated
                        </small>
                    </div>

                    <div className="learning-arrow">
                        →
                    </div>

                    <div className="learning-step">
                        <span className="learning-number">
                            02
                        </span>

                        <strong>
                            Maintenance
                        </strong>

                        <small>
                            Recommended action is performed
                        </small>
                    </div>

                    <div className="learning-arrow">
                        →
                    </div>

                    <div className="learning-step">
                        <span className="learning-number">
                            03
                        </span>

                        <strong>
                            Actual Outcome
                        </strong>

                        <small>
                            Result is recorded as feedback
                        </small>
                    </div>

                    <div className="learning-arrow">
                        →
                    </div>

                    <div className="learning-step">
                        <span className="learning-number">
                            04
                        </span>

                        <strong>
                            Model Learning
                        </strong>

                        <small>
                            Feedback becomes future training data
                        </small>
                    </div>
                </div>
            </div>

            {error && (
                <div className="feedback-error">
                    {error}
                </div>
            )}

            {loading ? (
                <div className="feedback-empty">
                    <h3>
                        Loading feedback...
                    </h3>

                    <p>
                        SmartPulse is retrieving learning-loop
                        information.
                    </p>
                </div>
            ) : feedback.length === 0 ? (
                <div className="feedback-empty">
                    <h3>
                        No Feedback Yet
                    </h3>

                    <p>
                        Complete a maintenance action to generate
                        feedback for the learning loop.
                    </p>
                </div>
            ) : (
                <div className="feedback-list">
                    <div className="feedback-list-header">
                        <div>
                            <span>
                                FEEDBACK HISTORY
                            </span>

                            <h3>
                                Maintenance Outcomes
                            </h3>
                        </div>

                        <span className="feedback-count">
                            {feedback.length} Records
                        </span>
                    </div>

                    {feedback.map((item) => (
                        <div
                            className="feedback-card"
                            key={item.feedbackId}
                        >
                            <div className="feedback-card-header">
                                <div>
                                    <span className="feedback-label">
                                        MACHINE
                                    </span>

                                    <h3>
                                        {item.machineId}
                                    </h3>
                                </div>

                                <span
                                    className={`feedback-outcome ${getOutcomeClass(
                                        item.actualOutcome
                                    )}`}
                                >
                                    {formatOutcome(
                                        item.actualOutcome
                                    )}
                                </span>
                            </div>

                            <div className="feedback-details">
                                <div>
                                    <span>
                                        Feedback ID
                                    </span>

                                    <strong>
                                        {item.feedbackId}
                                    </strong>
                                </div>

                                <div>
                                    <span>
                                        Predicted Probability
                                    </span>

                                    <strong>
                                        {(
                                            item.predictedFailureProbability *
                                            100
                                        ).toFixed(2)}
                                        %
                                    </strong>
                                </div>

                                <div>
                                    <span>
                                        Risk Score
                                    </span>

                                    <strong>
                                        {Number(
                                            item.riskScore
                                        ).toFixed(2)}
                                    </strong>
                                </div>

                                <div>
                                    <span>
                                        Maintenance Action
                                    </span>

                                    <strong>
                                        {item.maintenanceAction}
                                    </strong>
                                </div>
                            </div>

                            <div className="feedback-footer">
                                <span>
                                    Recorded:{" "}
                                    {formatDate(
                                        item.createdAt
                                    )}
                                </span>

                                <span>
                                    Actual outcome:
                                    {" "}
                                    {formatOutcome(
                                        item.actualOutcome
                                    )}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Feedback;