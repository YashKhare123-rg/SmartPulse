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
            double operatingHours = 500 + random.nextDouble() * 5000;

            for (int record = 0; record < RECORDS_PER_MACHINE; record++) {

                LocalDateTime timestamp =
                        LocalDateTime.now().minusMinutes(
                                (long) (NUMBER_OF_MACHINES * RECORDS_PER_MACHINE - record)
                        );

                double loadPercentage = 20 + random.nextDouble() * 80;

                double temperature =
                        40
                                + (loadPercentage * 0.35)
                                + (machineAge * 1.2)
                                + random.nextGaussian() * 4;

                double vibration =
                        1
                                + (loadPercentage * 0.035)
                                + (operatingHours / 10000)
                                + random.nextGaussian() * 0.5;

                double pressure =
                        4
                                + (loadPercentage * 0.025)
                                + random.nextGaussian() * 0.3;

                double rotationSpeed =
                        1000
                                + (loadPercentage * 7)
                                + random.nextGaussian() * 50;

                double powerConsumption =
                        3
                                + (loadPercentage * 0.055)
                                + (temperature * 0.015)
                                + random.nextGaussian() * 0.3;

                double riskScore =
                        (temperature * 0.025)
                                + (vibration * 0.35)
                                + (loadPercentage * 0.015)
                                + (operatingHours / 10000)
                                + (machineAge * 0.04);

                double failureProbability =
                        1.0 / (1.0 + Math.exp(-riskScore + 3.8));

                int failure =
                        random.nextDouble() < failureProbability ? 1 : 0;

                MachineRecord machineRecord = new MachineRecord(
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

                operatingHours += random.nextDouble() * 2;
            }
        }

        return records;
    }
}