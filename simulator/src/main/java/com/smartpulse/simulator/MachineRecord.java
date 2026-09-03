package com.smartpulse.simulator;

import java.time.LocalDateTime;

public class MachineRecord {

    private String machineId;
    private LocalDateTime timestamp;
    private double temperature;
    private double vibration;
    private double pressure;
    private double powerConsumption;
    private double operatingHours;
    private double loadPercentage;
    private double rotationSpeed;
    private int maintenanceCount;
    private int machineAge;
    private int failure;

    public MachineRecord(
            String machineId,
            LocalDateTime timestamp,
            double temperature,
            double vibration,
            double pressure,
            double powerConsumption,
            double operatingHours,
            double loadPercentage,
            double rotationSpeed,
            int maintenanceCount,
            int machineAge,
            int failure) {

        this.machineId = machineId;
        this.timestamp = timestamp;
        this.temperature = temperature;
        this.vibration = vibration;
        this.pressure = pressure;
        this.powerConsumption = powerConsumption;
        this.operatingHours = operatingHours;
        this.loadPercentage = loadPercentage;
        this.rotationSpeed = rotationSpeed;
        this.maintenanceCount = maintenanceCount;
        this.machineAge = machineAge;
        this.failure = failure;
    }

    public String getMachineId() {
        return machineId;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public double getTemperature() {
        return temperature;
    }

    public double getVibration() {
        return vibration;
    }

    public double getPressure() {
        return pressure;
    }

    public double getPowerConsumption() {
        return powerConsumption;
    }

    public double getOperatingHours() {
        return operatingHours;
    }

    public double getLoadPercentage() {
        return loadPercentage;
    }

    public double getRotationSpeed() {
        return rotationSpeed;
    }

    public int getMaintenanceCount() {
        return maintenanceCount;
    }

    public int getMachineAge() {
        return machineAge;
    }

    public int getFailure() {
        return failure;
    }
}