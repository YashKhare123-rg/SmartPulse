package com.smartpulse.simulator;

import java.util.List;

public class Main {

    public static void main(String[] args) {

        System.out.println("Starting SmartPulse Data Simulator...");

        MachineDataGenerator generator = new MachineDataGenerator();

        List<MachineRecord> records = generator.generateData();

        System.out.println("Data generation completed.");
        System.out.println("Total records generated: " + records.size());

        CSVWriter csvWriter = new CSVWriter();

        csvWriter.writeToCSV(
                records,
                "data/raw/machine_data.csv"
        );

        BadDataGenerator badDataGenerator = new BadDataGenerator();

        badDataGenerator.createCorruptedDataset(
                "data/raw/machine_data.csv",
                "data/raw/machine_data_corrupted.csv"
        );

        DataQualityValidator validator = new DataQualityValidator();

        validator.validateDataset(
                "data/raw/machine_data_corrupted.csv",
                "data/processed/valid_machine_data.csv",
                "data/invalid/invalid_machine_data.csv"
        );

        System.out.println("SmartPulse dataset processing completed.");
    }
}