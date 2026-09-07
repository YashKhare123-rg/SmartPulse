package com.smartpulse.springboot.model;

public class MaintenanceAction {

    private String actionId;
    private String machineId;
    private String action;
    private String priority;
    private String status;
    private String reason;
    private double failureProbability;
    private double riskScore;
    private String createdAt;
    private String completedAt;
    private String actualOutcome;

    public MaintenanceAction() {
    }

    public MaintenanceAction(
            String actionId,
            String machineId,
            String action,
            String priority,
            String status,
            String reason,
            double failureProbability,
            double riskScore,
            String createdAt,
            String completedAt,
            String actualOutcome) {

        this.actionId = actionId;
        this.machineId = machineId;
        this.action = action;
        this.priority = priority;
        this.status = status;
        this.reason = reason;
        this.failureProbability = failureProbability;
        this.riskScore = riskScore;
        this.createdAt = createdAt;
        this.completedAt = completedAt;
        this.actualOutcome = actualOutcome;
    }

    public String getActionId() {
        return actionId;
    }

    public void setActionId(String actionId) {
        this.actionId = actionId;
    }

    public String getMachineId() {
        return machineId;
    }

    public void setMachineId(String machineId) {
        this.machineId = machineId;
    }

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

    public String getPriority() {
        return priority;
    }

    public void setPriority(String priority) {
        this.priority = priority;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public double getFailureProbability() {
        return failureProbability;
    }

    public void setFailureProbability(double failureProbability) {
        this.failureProbability = failureProbability;
    }

    public double getRiskScore() {
        return riskScore;
    }

    public void setRiskScore(double riskScore) {
        this.riskScore = riskScore;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public String getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(String completedAt) {
        this.completedAt = completedAt;
    }

    public String getActualOutcome() {
        return actualOutcome;
    }

    public void setActualOutcome(String actualOutcome) {
        this.actualOutcome = actualOutcome;
    }
}