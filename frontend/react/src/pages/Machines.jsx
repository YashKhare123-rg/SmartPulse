import { useEffect, useMemo, useState } from "react";
import axios from "axios";

function Machines({ machineFilter = "all" }) {
    const [machines, setMachines] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [searchTerm, setSearchTerm] = useState("");
    const [viewMode, setViewMode] = useState("latest");
    const [currentPage, setCurrentPage] = useState(1);

    const recordsPerPage = 10;

    useEffect(() => {
        const loadMachines = async () => {
            try {
                setLoading(true);
                setError("");

                const response = await axios.get(
                    "http://localhost:8080/api/machines"
                );

                setMachines(response.data);
            } catch (err) {
                console.error(err);

                setError(
                    "Unable to load machine data. Make sure Spring Boot is running."
                );
            } finally {
                setLoading(false);
            }
        };

        loadMachines();
    }, []);

    /*
     * Find the latest record for every machine.
     */
    const latestMachineRecords = useMemo(() => {
        const latestRecords = {};

        machines.forEach((machine) => {
            const machineId = machine.machine_id;

            if (
                !latestRecords[machineId] ||
                new Date(machine.timestamp) >
                new Date(latestRecords[machineId].timestamp)
            ) {
                latestRecords[machineId] = machine;
            }
        });

        return Object.values(latestRecords);
    }, [machines]);

    /*
     * Apply machine status filter.
     */
    const filteredByStatus = useMemo(() => {
        const source =
            viewMode === "latest"
                ? latestMachineRecords
                : machines;

        if (machineFilter === "healthy") {
            return source.filter(
                (machine) => Number(machine.failure) === 0
            );
        }

        if (machineFilter === "high-risk") {
            return source.filter(
                (machine) => Number(machine.failure) === 1
            );
        }

        return source;
    }, [
        machines,
        latestMachineRecords,
        machineFilter,
        viewMode
    ]);

    /*
     * Apply machine ID search.
     */
    const filteredMachines = useMemo(() => {
        const search = searchTerm.trim().toLowerCase();

        if (!search) {
            return filteredByStatus;
        }

        return filteredByStatus.filter((machine) =>
            String(machine.machine_id)
                .toLowerCase()
                .includes(search)
        );
    }, [
        filteredByStatus,
        searchTerm
    ]);

    /*
     * Pagination.
     */
    const totalPages = Math.max(
        1,
        Math.ceil(
            filteredMachines.length / recordsPerPage
        )
    );

    const paginatedMachines = useMemo(() => {
        const startIndex =
            (currentPage - 1) * recordsPerPage;

        return filteredMachines.slice(
            startIndex,
            startIndex + recordsPerPage
        );
    }, [
        filteredMachines,
        currentPage
    ]);

    /*
     * Reset pagination whenever
     * search/filter/view changes.
     */
    useEffect(() => {
        setCurrentPage(1);
    }, [
        machineFilter,
        searchTerm,
        viewMode
    ]);

    /*
     * Keep page valid if filtered
     * results become smaller.
     */
    useEffect(() => {
        if (currentPage > totalPages) {
            setCurrentPage(totalPages);
        }
    }, [
        currentPage,
        totalPages
    ]);

    const filterTitle =
        machineFilter === "healthy"
            ? "Healthy Machines"
            : machineFilter === "high-risk"
                ? "Failure-Flagged Machines"
                : "All Machines";

    const filterDescription =
        machineFilter === "healthy"
            ? "Machines whose latest recorded status is healthy."
            : machineFilter === "high-risk"
                ? "Machines whose latest recorded status contains a failure flag."
                : "All machine records available in the SmartPulse system.";

    const latestFilteredMachineCount = useMemo(() => {
        if (machineFilter === "healthy") {
            return latestMachineRecords.filter(
                (machine) =>
                    Number(machine.failure) === 0
            ).length;
        }

        if (machineFilter === "high-risk") {
            return latestMachineRecords.filter(
                (machine) =>
                    Number(machine.failure) === 1
            ).length;
        }

        return latestMachineRecords.length;
    }, [
        latestMachineRecords,
        machineFilter
    ]);

    const displayStart =
        filteredMachines.length === 0
            ? 0
            : (currentPage - 1) *
            recordsPerPage +
            1;

    const displayEnd =
        Math.min(
            currentPage * recordsPerPage,
            filteredMachines.length
        );

    if (loading) {
        return (
            <div className="page-content">

                <div className="loading-message">
                    Loading machine data...
                </div>

            </div>
        );
    }

    if (error) {
        return (
            <div className="page-content">

                <div className="prediction-error">
                    {error}
                </div>

            </div>
        );
    }

    return (
        <div className="page-content">

            {/* ================= PAGE HEADER ================= */}

            <div className="page-header">

                <div>

                    <h2>
                        Machine Monitoring
                    </h2>

                    <p>
                        Monitor machine sensor data and failure status.
                    </p>

                </div>

                <div className="machine-count">

                    {filteredMachines.length.toLocaleString()}{" "}

                    {viewMode === "latest"
                        ? "Machines"
                        : "Records"}

                </div>

            </div>

            {/* ================= ACTIVE FILTER ================= */}

            {machineFilter !== "all" && (

                <div className="machine-filter-banner">

                    <div>

                        <span>
                            ACTIVE FILTER
                        </span>

                        <strong>
                            {filterTitle}
                        </strong>

                        <p>
                            {filterDescription}
                        </p>

                    </div>

                    <div className="machine-filter-count">

                        {latestFilteredMachineCount}

                        <small>
                            machines
                        </small>

                    </div>

                </div>

            )}

            {/* ================= CONTROLS ================= */}

            <div className="machine-controls">

                <div className="machine-search">

                    <label>
                        Search Machine
                    </label>

                    <input
                        type="text"
                        placeholder="Search by Machine ID..."
                        value={searchTerm}
                        onChange={(event) =>
                            setSearchTerm(
                                event.target.value
                            )
                        }
                    />

                </div>

                <div className="machine-view-controls">

                    <button
                        className={
                            viewMode === "latest"
                                ? "view-button active"
                                : "view-button"
                        }
                        onClick={() =>
                            setViewMode("latest")
                        }
                    >
                        Latest Records
                    </button>

                    <button
                        className={
                            viewMode === "all"
                                ? "view-button active"
                                : "view-button"
                        }
                        onClick={() =>
                            setViewMode("all")
                        }
                    >
                        All Records
                    </button>

                </div>

            </div>

            {/* ================= RESULT INFORMATION ================= */}

            <div className="machine-result-info">

                <div>

                    {viewMode === "latest"
                        ? "Showing the latest reading for each machine."
                        : "Showing all available machine records."}

                </div>

                <div>

                    {filteredMachines.length.toLocaleString()}{" "}
                    matching{" "}
                    {viewMode === "latest"
                        ? "machines"
                        : "records"}

                </div>

            </div>

            {/* ================= MACHINE TABLE ================= */}

            <div className="machine-table-container">

                <table className="machine-table">

                    <thead>

                    <tr>

                        <th>
                            Machine
                        </th>

                        <th>
                            Timestamp
                        </th>

                        <th>
                            Temperature
                        </th>

                        <th>
                            Vibration
                        </th>

                        <th>
                            Pressure
                        </th>

                        <th>
                            Power
                        </th>

                        <th>
                            Load
                        </th>

                        <th>
                            Rotation
                        </th>

                        <th>
                            Failure
                        </th>

                    </tr>

                    </thead>

                    <tbody>

                    {paginatedMachines.map(
                        (machine, index) => (

                            <tr
                                key={`${machine.machine_id}-${machine.timestamp}-${index}`}
                            >

                                <td>

                                    <strong>
                                        {machine.machine_id}
                                    </strong>

                                </td>

                                <td>
                                    {machine.timestamp}
                                </td>

                                <td>
                                    {Number(
                                        machine.temperature
                                    ).toFixed(2)}{" "}
                                    °C
                                </td>

                                <td>
                                    {Number(
                                        machine.vibration
                                    ).toFixed(2)}
                                </td>

                                <td>
                                    {Number(
                                        machine.pressure
                                    ).toFixed(2)}
                                </td>

                                <td>
                                    {Number(
                                        machine.power_consumption
                                    ).toFixed(2)}
                                </td>

                                <td>
                                    {Number(
                                        machine.load_percentage
                                    ).toFixed(2)}%
                                </td>

                                <td>
                                    {Number(
                                        machine.rotation_speed
                                    ).toFixed(0)}{" "}
                                    RPM
                                </td>

                                <td>

                                    <span
                                        className={`failure-badge ${
                                            Number(
                                                machine.failure
                                            ) === 1
                                                ? "failure"
                                                : "normal"
                                        }`}
                                    >
                                        {Number(
                                            machine.failure
                                        ) === 1
                                            ? "FAILURE"
                                            : "NORMAL"}
                                    </span>

                                </td>

                            </tr>

                        )
                    )}

                    </tbody>

                </table>

            </div>

            {/* ================= EMPTY STATE ================= */}

            {filteredMachines.length === 0 && (

                <div className="empty-state">

                    No machine records match the selected filter.

                </div>

            )}

            {/* ================= PAGINATION ================= */}

            {filteredMachines.length > 0 && (

                <div className="machine-pagination">

                    <div className="pagination-info">

                        Showing{" "}

                        <strong>
                            {displayStart}
                        </strong>

                        {" - "}

                        <strong>
                            {displayEnd}
                        </strong>

                        {" of "}

                        <strong>
                            {filteredMachines.length.toLocaleString()}
                        </strong>

                    </div>

                    <div className="pagination-buttons">

                        <button
                            className="pagination-button"
                            disabled={
                                currentPage === 1
                            }
                            onClick={() =>
                                setCurrentPage(
                                    (page) =>
                                        page - 1
                                )
                            }
                        >
                            Previous
                        </button>

                        <span className="page-number">

                            Page{" "}
                            {currentPage}
                            {" "}of{" "}
                            {totalPages}

                        </span>

                        <button
                            className="pagination-button"
                            disabled={
                                currentPage === totalPages
                            }
                            onClick={() =>
                                setCurrentPage(
                                    (page) =>
                                        page + 1
                                )
                            }
                        >
                            Next
                        </button>

                    </div>

                </div>

            )}

        </div>
    );
}

export default Machines;