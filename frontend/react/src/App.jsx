import { useState } from "react";
import "./App.css";

import Dashboard from "./pages/Dashboard";
import Machines from "./pages/Machines";
import Predictions from "./pages/Predictions";
import Maintenance from "./pages/Maintenance";
import DriftMonitoring from "./pages/DriftMonitoring";
import Feedback from "./pages/Feedback";
import WhatIfAnalysis from "./pages/WhatIfAnalysis";
import Retraining from "./pages/Retraining";

function App() {
  const [currentPage, setCurrentPage] = useState("dashboard");
  const [machineFilter, setMachineFilter] = useState("all");

  const showHealthyMachines = () => {
    setMachineFilter("healthy");
    setCurrentPage("machines");
  };

  const showHighRiskMachines = () => {
    setMachineFilter("high-risk");
    setCurrentPage("machines");
  };

  const openAllMachines = () => {
    setMachineFilter("all");
    setCurrentPage("machines");
  };

  const getPageTitle = () => {
    switch (currentPage) {
      case "dashboard":
        return "SmartPulse Dashboard";

      case "machines":
        return "Machine Monitoring";

      case "predictions":
        return "Failure Prediction";

      case "maintenance":
        return "Maintenance";

      case "drift":
        return "Drift Monitoring";

      case "feedback":
        return "Feedback & Learning";

      case "whatif":
        return "What-If Analysis";

      case "retraining":
        return "Model Retraining";

      default:
        return "SmartPulse Dashboard";
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return (
            <Dashboard
                onHealthyMachines={showHealthyMachines}
                onHighRiskMachines={showHighRiskMachines}
            />
        );

      case "machines":
        return (
            <Machines
                machineFilter={machineFilter}
            />
        );

      case "predictions":
        return <Predictions />;

      case "maintenance":
        return <Maintenance />;

      case "drift":
        return <DriftMonitoring />;

      case "feedback":
        return <Feedback />;

      case "whatif":
        return <WhatIfAnalysis />;

      case "retraining":
        return <Retraining />;

      default:
        return (
            <Dashboard
                onHealthyMachines={showHealthyMachines}
                onHighRiskMachines={showHighRiskMachines}
            />
        );
    }
  };

  return (
      <div className="app">

        {/* ================= SIDEBAR ================= */}

        <aside className="sidebar">

          <div className="logo">

            <div className="logo-icon">
              S
            </div>

            <div>
              <h2>SmartPulse</h2>
              <span>Industrial Intelligence</span>
            </div>

          </div>

          <nav>

            {/* Dashboard */}

            <button
                className={`nav-item ${
                    currentPage === "dashboard" ? "active" : ""
                }`}
                onClick={() => setCurrentPage("dashboard")}
            >
              Dashboard
            </button>

            {/* Machines */}

            <button
                className={`nav-item ${
                    currentPage === "machines" ? "active" : ""
                }`}
                onClick={openAllMachines}
            >
              Machines
            </button>

            {/* Predictions */}

            <button
                className={`nav-item ${
                    currentPage === "predictions" ? "active" : ""
                }`}
                onClick={() => setCurrentPage("predictions")}
            >
              Predictions
            </button>

            {/* Maintenance */}

            <button
                className={`nav-item ${
                    currentPage === "maintenance" ? "active" : ""
                }`}
                onClick={() => setCurrentPage("maintenance")}
            >
              Maintenance
            </button>

            {/* Drift Monitoring */}

            <button
                className={`nav-item ${
                    currentPage === "drift" ? "active" : ""
                }`}
                onClick={() => setCurrentPage("drift")}
            >
              Drift Monitoring
            </button>

            {/* Feedback */}

            <button
                className={`nav-item ${
                    currentPage === "feedback" ? "active" : ""
                }`}
                onClick={() => setCurrentPage("feedback")}
            >
              Feedback
            </button>

            {/* What-If Analysis */}

            <button
                className={`nav-item ${
                    currentPage === "whatif" ? "active" : ""
                }`}
                onClick={() => setCurrentPage("whatif")}
            >
              What-If Analysis
            </button>

            {/* Model Retraining */}

            <button
                className={`nav-item ${
                    currentPage === "retraining" ? "active" : ""
                }`}
                onClick={() => setCurrentPage("retraining")}
            >
              Model Retraining
            </button>

          </nav>

          {/* ================= SYSTEM STATUS ================= */}

          <div className="system-status">

            <span className="status-dot"></span>

            <div>
              <strong>System Online</strong>
              <small>All services operational</small>
            </div>

          </div>

        </aside>

        {/* ================= MAIN CONTENT ================= */}

        <main className="main-content">

          {/* ================= TOP BAR ================= */}

          <header className="topbar">

            <div>

              <h1>
                {getPageTitle()}
              </h1>

              <p>
                Self-Healing Industrial Intelligence Platform
              </p>

            </div>

            <div className="header-status">

              <span className="status-dot"></span>

              Backend Connected

            </div>

          </header>

          {/* ================= PAGE CONTENT ================= */}

          {renderPage()}

        </main>

      </div>
  );
}

export default App;