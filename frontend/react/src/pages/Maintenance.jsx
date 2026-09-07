import { useEffect, useState } from "react";
import axios from "axios";

function Maintenance() {
    const [actions, setActions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [updatingId, setUpdatingId] = useState(null);

    const [completeActionId, setCompleteActionId] = useState(null);
    const [actualOutcome, setActualOutcome] = useState("");

    const fetchActions = async () => {
        try {
            setLoading(true);
            setError("");

            const response = await axios.get(
                "http://localhost:8080/api/maintenance"
            );

            setActions(response.data);
        } catch (err) {
            console.error(err);

            setError(
                "Unable to load maintenance actions. Make sure Spring Boot is running."
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchActions();
    }, []);

    const updateStatus = async (actionId, status) => {
        try {
            setUpdatingId(actionId);
            setError("");

            await axios.put(
                `http://localhost:8080/api/maintenance/${actionId}/status`,
                null,
                {
                    params: {
                        status
                    }
                }
            );

            await fetchActions();
        } catch (err) {
            console.error(err);

            setError(
                "Unable to update maintenance status."
            );
        } finally {
            setUpdatingId(null);
        }
    };

    const openCompleteDialog = (actionId) => {
        setCompleteActionId(actionId);
        setActualOutcome("");
        setError("");
    };

    const closeCompleteDialog = () => {
        setCompleteActionId(null);
        setActualOutcome("");
    };

    const completeAction = async () => {
        if (!completeActionId) {
            return;
        }

        if (!actualOutcome) {
            setError("Please select an actual outcome.");
            return;
        }

        try {
            setUpdatingId(completeActionId);
            setError("");

            await axios.put(
                `http://localhost:8080/api/maintenance/${completeActionId}/complete`,
                null,
                {
                    params: {
                        actualOutcome
                    }
                }
            );

            closeCompleteDialog();
            await fetchActions();
        } catch (err) {
            console.error(err);

            setError(
                "Unable to complete maintenance action."
            );
        } finally {
            setUpdatingId(null);
        }
    };

    const getPriorityClass = (priority) => {
        if (!priority) {
            return "";
        }

        return priority
            .toLowerCase()
            .replace(" ", "-");
    };

    const getStatusClass = (status) => {
        if (!status) {
            return "";
        }

        return status
            .toLowerCase()
            .replace(" ", "-");
    };

    const formatDate = (date) => {
        if (!date) {
            return "—";
        }

        return new Date(date).toLocaleString();
    };

    const pendingCount = actions.filter(
        (action) => action.status === "PENDING"
    ).length;

    const inProgressCount = actions.filter(
        (action) => action.status === "IN PROGRESS"
    ).length;

    const completedCount = actions.filter(
        (action) => action.status === "COMPLETED"
    ).length;

    return (
        <div className="page-content">
            <div className="page-header">
                <div>
                    <h2>Maintenance Management</h2>

                    <p>
                        Monitor, manage and complete AI-generated
                        maintenance actions.
                    </p>
                </div>

                <button
                    className="maintenance-refresh"
                    onClick={fetchActions}
                    disabled={loading}
                >
                    {loading ? "Refreshing..." : "Refresh"}
                </button>
            </div>

            <div className="maintenance-summary">
                <div className="maintenance-summary-card">
                    <span>Total Actions</span>
                    <strong>{actions.length}</strong>
                </div>

                <div className="maintenance-summary-card">
                    <span>Pending</span>
                    <strong>{pendingCount}</strong>
                </div>

                <div className="maintenance-summary-card">
                    <span>In Progress</span>
                    <strong>{inProgressCount}</strong>
                </div>

                <div className="maintenance-summary-card">
                    <span>Completed</span>
                    <strong>{completedCount}</strong>
                </div>
            </div>

            {error && (
                <div className="maintenance-error">
                    {error}
                </div>
            )}

            {loading ? (
                <div className="maintenance-empty">
                    <h3>Loading maintenance actions...</h3>
                    <p>
                        SmartPulse is retrieving maintenance
                        information.
                    </p>
                </div>
            ) : actions.length === 0 ? (
                <div className="maintenance-empty">
                    <h3>No Maintenance Actions</h3>
                    <p>
                        No maintenance actions have been generated
                        yet.
                    </p>
                </div>
            ) : (
                <div className="maintenance-list">
                    {actions.map((action) => (
                        <div
                            className="maintenance-card"
                            key={action.actionId}
                        >
                            <div className="maintenance-card-header">
                                <div>
                                    <span className="maintenance-label">
                                        MACHINE
                                    </span>

                                    <h3>
                                        {action.machineId}
                                    </h3>
                                </div>

                                <div className="maintenance-badges">
                                    <span
                                        className={`maintenance-priority ${getPriorityClass(
                                            action.priority
                                        )}`}
                                    >
                                        {action.priority}
                                    </span>

                                    <span
                                        className={`maintenance-status ${getStatusClass(
                                            action.status
                                        )}`}
                                    >
                                        {action.status}
                                    </span>
                                </div>
                            </div>

                            <div className="maintenance-details">
                                <div>
                                    <span>Action</span>

                                    <strong>
                                        {action.action}
                                    </strong>
                                </div>

                                <div>
                                    <span>
                                        Failure Probability
                                    </span>

                                    <strong>
                                        {(
                                            action.failureProbability *
                                            100
                                        ).toFixed(2)}
                                        %
                                    </strong>
                                </div>

                                <div>
                                    <span>Risk Score</span>

                                    <strong>
                                        {action.riskScore.toFixed(2)}
                                    </strong>
                                </div>

                                <div>
                                    <span>Created</span>

                                    <strong>
                                        {formatDate(
                                            action.createdAt
                                        )}
                                    </strong>
                                </div>
                            </div>

                            <div className="maintenance-reason">
                                <span>Reason</span>

                                <p>
                                    {action.reason}
                                </p>
                            </div>

                            {action.actualOutcome && (
                                <div className="maintenance-outcome">
                                    <span>
                                        Actual Outcome
                                    </span>

                                    <strong>
                                        {action.actualOutcome}
                                    </strong>
                                </div>
                            )}

                            {action.completedAt && (
                                <div className="maintenance-completed">
                                    Completed:{" "}
                                    {formatDate(
                                        action.completedAt
                                    )}
                                </div>
                            )}

                            <div className="maintenance-actions">
                                {action.status === "PENDING" && (
                                    <button
                                        className="maintenance-start"
                                        onClick={() =>
                                            updateStatus(
                                                action.actionId,
                                                "IN PROGRESS"
                                            )
                                        }
                                        disabled={
                                            updatingId ===
                                            action.actionId
                                        }
                                    >
                                        {updatingId ===
                                        action.actionId
                                            ? "Updating..."
                                            : "Start Maintenance"}
                                    </button>
                                )}

                                {action.status ===
                                    "IN PROGRESS" && (
                                        <button
                                            className="maintenance-complete"
                                            onClick={() =>
                                                openCompleteDialog(
                                                    action.actionId
                                                )
                                            }
                                            disabled={
                                                updatingId ===
                                                action.actionId
                                            }
                                        >
                                            Complete Maintenance
                                        </button>
                                    )}

                                {action.status ===
                                    "COMPLETED" && (
                                        <span className="maintenance-finished">
                                        Maintenance Completed
                                    </span>
                                    )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {completeActionId && (
                <div className="maintenance-modal-overlay">
                    <div className="maintenance-modal">
                        <div className="maintenance-modal-header">
                            <div>
                                <span>
                                    MAINTENANCE COMPLETION
                                </span>

                                <h3>
                                    Record Actual Outcome
                                </h3>
                            </div>

                            <button
                                className="maintenance-modal-close"
                                onClick={
                                    closeCompleteDialog
                                }
                            >
                                ×
                            </button>
                        </div>

                        <p>
                            Record what actually happened after
                            the maintenance operation. This
                            information will be used by the
                            SmartPulse feedback loop.
                        </p>

                        <label>
                            Actual Outcome
                        </label>

                        <select
                            value={actualOutcome}
                            onChange={(event) =>
                                setActualOutcome(
                                    event.target.value
                                )
                            }
                        >
                            <option value="">
                                Select outcome
                            </option>

                            <option value="MAINTENANCE_SUCCESSFUL">
                                Maintenance Successful
                            </option>

                            <option value="MAINTENANCE_FAILED">
                                Maintenance Failed
                            </option>

                            <option value="FAILURE_OCCURRED">
                                Failure Occurred
                            </option>
                        </select>

                        <div className="maintenance-modal-actions">
                            <button
                                className="maintenance-cancel"
                                onClick={
                                    closeCompleteDialog
                                }
                            >
                                Cancel
                            </button>

                            <button
                                className="maintenance-submit"
                                onClick={completeAction}
                                disabled={
                                    updatingId ===
                                    completeActionId
                                }
                            >
                                {updatingId ===
                                completeActionId
                                    ? "Saving..."
                                    : "Complete Action"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Maintenance;