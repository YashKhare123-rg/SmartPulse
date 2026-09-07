package com.smartpulse.simulator;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class MachineDataGenerator {

    private final Random random = new Random();

    private static final int NUMBER_OF_MACHINES = 100;
    private static final int RECORDS_PER_MACHINE = 100;

    public List<MachineRecord> generateData() {

        List<MachineRecord> records = new ArrayList<>();

        for (int machine = 1; machine <= NUMBER_OF_MACHINES; machine++) {

            String machineId = String.format("M%03d", machine);

            int machineAge = 1 + random.nextInt(10);
            int maintenanceCount = random.nextInt(8);

            double baseOperatingHours =
                    500 + random.nextDouble() * 5000;

            double machineHealth =
                    0.75 + random.nextDouble() * 0.25;

            double degradationRate =
                    0.001 + random.nextDouble() * 0.002;

            double operatingHours = baseOperatingHours;

            for (int record = 0; record < RECORDS_PER_MACHINE; record++) {

                LocalDateTime timestamp =
                        LocalDateTime.now().minusMinutes(
                                (long) (
                                        NUMBER_OF_MACHINES
                                                * RECORDS_PER_MACHINE
                                                - record
                                )
                        );

                double degradation =
                        Math.min(
                                1.0,
                                record * degradationRate
                        );

                double health =
                        Math.max(
                                0.0,
                                machineHealth - degradation
                        );

                double loadPercentage =
                        20 + random.nextDouble() * 80;

                double thermalStress =
                        loadPercentage / 100.0
                                + (1.0 - health) * 0.8;

                double mechanicalStress =
                        loadPercentage / 100.0
                                + (1.0 - health) * 1.0;

                double electricalStress =
                        loadPercentage / 100.0
                                + (1.0 - health) * 0.7;

                double temperature =
                        40
                                + loadPercentage * 0.35
                                + machineAge * 1.2
                                + thermalStress * 8
                                + random.nextGaussian() * 2.0;

                double vibration =
                        1
                                + loadPercentage * 0.035
                                + operatingHours / 10000
                                + mechanicalStress * 1.2
                                + random.nextGaussian() * 0.25;

                double pressure =
                        4
                                + loadPercentage * 0.025
                                + mechanicalStress * 0.6
                                + random.nextGaussian() * 0.15;

                double rotationSpeed =
                        1000
                                + loadPercentage * 7
                                + mechanicalStress * 80
                                + random.nextGaussian() * 25;

                double powerConsumption =
                        3
                                + loadPercentage * 0.055
                                + temperature * 0.015
                                + electricalStress * 1.2
                                + random.nextGaussian() * 0.2;

                double agingRisk =
                        (operatingHours / 6000.0) * 0.35
                                + (machineAge / 10.0) * 0.20;

                double maintenanceRisk =
                        maintenanceCount <= 1
                                ? 0.15
                                : maintenanceCount <= 3
                                ? 0.08
                                : 0.02;

                double thermalRisk =
                        Math.max(
                                0,
                                (temperature - 65) / 25
                        );

                double vibrationRisk =
                        Math.max(
                                0,
                                (vibration - 3.0) / 3.0
                        );

                double loadRisk =
                        Math.max(
                                0,
                                (loadPercentage - 60) / 40
                        );

                double powerRisk =
                        Math.max(
                                0,
                                (powerConsumption - 7) / 4
                        );

                double pressureRisk =
                        Math.max(
                                0,
                                (pressure - 5.5) / 2
                        );

                double mechanicalRisk =
                        (vibrationRisk * 0.30)
                                + (loadRisk * 0.20)
                                + (pressureRisk * 0.15)
                                + (mechanicalStress * 0.35);

                double electricalRisk =
                        (powerRisk * 0.45)
                                + (loadRisk * 0.25)
                                + (electricalStress * 0.30);

                double totalRisk =
                        (thermalRisk * 0.22)
                                + (mechanicalRisk * 0.30)
                                + (electricalRisk * 0.23)
                                + (agingRisk * 0.15)
                                + (maintenanceRisk * 0.10);

                totalRisk =
                        Math.max(
                                0,
                                Math.min(1.0, totalRisk)
                        );

                double failureProbability =
                        1.0 /
                                (
                                        1.0
                                                + Math.exp(
                                                -10.0
                                                        * (
                                                        totalRisk
                                                                - 0.55
                                                )
                                        )
                                );

                failureProbability =
                        Math.max(
                                0.01,
                                Math.min(
                                        0.99,
                                        failureProbability
                                )
                        );

                int failure =
                        random.nextDouble()
                                < failureProbability
                                ? 1
                                : 0;

                MachineRecord machineRecord =
                        new MachineRecord(
                                machineId,
                                timestamp,
                                Math.max(20, temperature),
                                Math.max(0.1, vibration),
                                Math.max(1, pressure),
                                Math.max(0.5, powerConsumption),
                                operatingHours,
                                loadPercentage,
                                Math.max(500, rotationSpeed),
                                maintenanceCount,
                                machineAge,
                                failure
                        );

                records.add(machineRecord);

                operatingHours +=
                        1.0 + random.nextDouble() * 2.0;
            }
        }

        return records;
    }
}