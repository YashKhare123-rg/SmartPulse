package com.smartpulse.simulator;

import java.io.*;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.HashSet;
import java.util.Set;



public class DataQualityValidator {

    public void validateDataset(String inputPath, String validPath, String invalidPath) {

        File inputFile = new File(inputPath);
        File validFile = new File(validPath);
        File invalidFile = new File(invalidPath);

        createParentDirectory(validFile);
        createParentDirectory(invalidFile);

        int totalRecords = 0;
        int validRecords = 0;
        int invalidRecords = 0;
        Map<String,Integer> errorCounts = new HashMap<>();
        Set<String> seenRecords = new HashSet<>();

        try (
                BufferedReader reader = new BufferedReader(new FileReader(inputFile));
                BufferedWriter validWriter = new BufferedWriter(new FileWriter(validFile));
                BufferedWriter invalidWriter = new BufferedWriter(new FileWriter(invalidFile))
        ) {

            String header = reader.readLine();

            validWriter.write(header);
            validWriter.newLine();

            invalidWriter.write("reason," + header);
            invalidWriter.newLine();

            String line;

            while ((line = reader.readLine()) != null) {

                totalRecords++;

                String reason = validateRecord(line);

                if(seenRecords.contains(line)) {
                    reason= "DUPLICATE_RECORD";

                }
                else{
                    seenRecords.add(line);
                }

                if (reason.equals("VALID")) {

                    validWriter.write(line);
                    validWriter.newLine();
                    validRecords++;

                } else {

                    invalidWriter.write(reason + "," + line);
                    invalidWriter.newLine();
                    invalidRecords++;

                    errorCounts.put(
                            reason,
                            errorCounts.getOrDefault(reason,0)+1
                    );
                }
            }

            System.out.println();
            System.out.println("===== DATA QUALITY REPORT =====");
            System.out.println("Total records: " + totalRecords);
            System.out.println("Valid records: " + validRecords);
            System.out.println("Invalid records: " + invalidRecords);
            System.out.println("================================");

            System.out.println("Error Breakdown:");
            for(Map.Entry<String,Integer> entry:errorCounts.entrySet()){
                System.out.println(entry.getKey() + ": " + entry.getValue());
            }

            System.out.println("===================================");

            System.out.println("Valid data: " + validFile.getAbsolutePath());
            System.out.println("Invalid data: " + invalidFile.getAbsolutePath());

        } catch (IOException e) {
            System.out.println("Error validating dataset: " + e.getMessage());
        }
    }

    private String validateRecord(String line) {

        String[] values = line.split(",", -1);

        if (values.length != 12) {
            return "INVALID_COLUMN_COUNT";
        }

        if (values[0].isBlank()) {
            return "MISSING_MACHINE_ID";
        }

        if (!values[0].matches("M\\d{3}")) {
            return "INVALID_MACHINE_ID";
        }

        try {
            LocalDateTime.parse(values[1]);
        } catch (Exception e) {
            return "INVALID_TIMESTAMP";
        }

        double temperature;

        try {
            if (values[2].isBlank()) {
                return "MISSING_TEMPERATURE";
            }

            temperature = Double.parseDouble(values[2]);

        } catch (Exception e) {
            return "INVALID_TEMPERATURE";
        }

        if (temperature < 20 || temperature > 120) {
            return "TEMPERATURE_OUT_OF_RANGE";
        }

        double vibration;

        try {
            vibration = Double.parseDouble(values[3]);
        } catch (Exception e) {
            return "INVALID_VIBRATION";
        }

        if (vibration < 0 || vibration > 15) {
            return "VIBRATION_OUT_OF_RANGE";
        }

        double pressure;

        try {
            pressure = Double.parseDouble(values[4]);
        } catch (Exception e) {
            return "INVALID_PRESSURE";
        }

        if (pressure <= 0 || pressure > 15) {
            return "PRESSURE_OUT_OF_RANGE";
        }

        double load;

        try {
            load = Double.parseDouble(values[7]);
        } catch (Exception e) {
            return "INVALID_LOAD";
        }

        if (load < 0 || load > 100) {
            return "LOAD_OUT_OF_RANGE";
        }

        int maintenanceCount;

        try {
            maintenanceCount = Integer.parseInt(values[9]);
        } catch (Exception e) {
            return "INVALID_MAINTENANCE_COUNT";
        }

        if (maintenanceCount < 0) {
            return "MAINTENANCE_COUNT_OUT_OF_RANGE";
        }

        int machineAge;

        try {
            machineAge = Integer.parseInt(values[10]);
        } catch (Exception e) {
            return "INVALID_MACHINE_AGE";
        }

        if (machineAge < 0 || machineAge > 50) {
            return "MACHINE_AGE_OUT_OF_RANGE";
        }

        int failure;

        try {
            failure = Integer.parseInt(values[11]);
        } catch (Exception e) {
            return "INVALID_FAILURE_VALUE";
        }

        if (failure != 0 && failure != 1) {
            return "INVALID_FAILURE_VALUE";
        }

        return "VALID";
    }

    private void createParentDirectory(File file) {

        File parent = file.getParentFile();

        if (parent != null && !parent.exists()) {
            parent.mkdirs();
        }
    }
}