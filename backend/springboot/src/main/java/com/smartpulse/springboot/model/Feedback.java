package com.smartpulse.springboot.model;

public class Feedback {

    private String feedbackId;
    private String machineId;
    private double predictedFailureProbability;
    private double riskScore;
    private String maintenanceAction;
    private String actualOutcome;
    private String createdAt;

    public Feedback() {
    }

    public Feedback(
            String feedbackId,
            String machineId,
            double predictedFailureProbability,
            double riskScore,
            String maintenanceAction,
            String actualOutcome,
            String createdAt) {

        this.feedbackId = feedbackId;
        this.machineId = machineId;
        this.predictedFailureProbability = predictedFailureProbability;
        this.riskScore = riskScore;
        this.maintenanceAction = maintenanceAction;
        this.actualOutcome = actualOutcome;
        this.createdAt = createdAt;
    }

    public String getFeedbackId() {
        return feedbackId;
    }

    public void setFeedbackId(String feedbackId) {
        this.feedbackId = feedbackId;
    }

    public String getMachineId() {
        return machineId;
    }

    public void setMachineId(String machineId) {
        this.machineId = machineId;
    }

    public double getPredictedFailureProbability() {
        return predictedFailureProbability;
    }

    public void setPredictedFailureProbability(double predictedFailureProbability) {
        this.predictedFailureProbability = predictedFailureProbability;
    }

    public double getRiskScore() {
        return riskScore;
    }

    public void setRiskScore(double riskScore) {
        this.riskScore = riskScore;
    }

    public String getMaintenanceAction() {
        return maintenanceAction;
    }

    public void setMaintenanceAction(String maintenanceAction) {
        this.maintenanceAction = maintenanceAction;
    }

    public String getActualOutcome() {
        return actualOutcome;
    }

    public void setActualOutcome(String actualOutcome) {
        this.actualOutcome = actualOutcome;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }
}