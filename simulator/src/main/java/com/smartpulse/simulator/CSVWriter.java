package com.smartpulse.simulator;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class CSVWriter {

    public void writeToCSV(List<MachineRecord> records, String filePath) {

        File file = new File(filePath);

        File parentDirectory = file.getParentFile();

        if (parentDirectory != null && !parentDirectory.exists()) {
            parentDirectory.mkdirs();
        }

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {

            writer.write(
                    "machine_id,timestamp,temperature,vibration,pressure," +
                            "power_consumption,operating_hours,load_percentage," +
                            "rotation_speed,maintenance_count,machine_age,failure"
            );

            writer.newLine();

            for (MachineRecord record : records) {

                writer.write(
                        record.getMachineId() + "," +
                                record.getTimestamp() + "," +
                                record.getTemperature() + "," +
                                record.getVibration() + "," +
                                record.getPressure() + "," +
                                record.getPowerConsumption() + "," +
                                record.getOperatingHours() + "," +
                                record.getLoadPercentage() + "," +
                                record.getRotationSpeed() + "," +
                                record.getMaintenanceCount() + "," +
                                record.getMachineAge() + "," +
                                record.getFailure()
                );

                writer.newLine();
            }

            System.out.println("CSV file created successfully!");
            System.out.println("Location: " + file.getAbsolutePath());
            System.out.println("Records written: " + records.size());

        } catch (IOException e) {
            System.out.println("Error writing CSV file: " + e.getMessage());
        }
    }
}