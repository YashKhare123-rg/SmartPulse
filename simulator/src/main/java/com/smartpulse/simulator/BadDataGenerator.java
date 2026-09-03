package com.smartpulse.simulator;

import java.io.*;
import java.util.Random;

public class BadDataGenerator {

    public void createCorruptedDataset(String inputPath, String outputPath) {

        Random random = new Random(42);

        File inputFile = new File(inputPath);
        File outputFile = new File(outputPath);

        File parentDirectory = outputFile.getParentFile();

        if (parentDirectory != null && !parentDirectory.exists()) {
            parentDirectory.mkdirs();
        }

        try (
                BufferedReader reader = new BufferedReader(new FileReader(inputFile));
                BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))
        ) {

            String header = reader.readLine();
            writer.write(header);
            writer.newLine();

            String line;
            int rowNumber = 0;

            while ((line = reader.readLine()) != null) {

                rowNumber++;

                String corruptedLine = line;

                String[] values = line.split(",", -1);

                if (rowNumber % 250 == 0) {
                    writer.write(line);
                    writer.newLine();
                }

                if (rowNumber % 333 == 0) {
                    values[2] = "";
                }

                if (rowNumber % 400 == 0) {
                    values[4] = "-10";
                }

                if (rowNumber % 500 == 0) {
                    values[7] = "150";
                }

                if (rowNumber % 600 == 0) {
                    values[3] = "25";
                }

                if (rowNumber % 700 == 0) {
                    values[0] = "INVALID_MACHINE";
                }

                if (rowNumber % 800 == 0) {
                    values[1] = "INVALID_TIMESTAMP";
                }

                if (rowNumber % 1000 == 0) {
                    values[11] = "5";
                }

                corruptedLine = String.join(",", values);

                writer.write(corruptedLine);
                writer.newLine();
            }

            System.out.println("Corrupted dataset created successfully!");
            System.out.println("Location: " + outputFile.getAbsolutePath());

        } catch (IOException e) {
            System.out.println("Error creating corrupted dataset: " + e.getMessage());
        }
    }
}