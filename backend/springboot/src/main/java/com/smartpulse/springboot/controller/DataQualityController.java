package com.smartpulse.springboot.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

@RestController
@RequestMapping("/api")
public class DataQualityController {

    private static final String RAW_DATA_PATH =
            "E:/SmartPulse/data/raw/machine_data_corrupted.csv";

    private static final String VALID_DATA_PATH =
            "E:/SmartPulse/data/processed/valid_machine_data.csv";

    @GetMapping("/data-quality")
    public DataQualityResponse getDataQuality() throws IOException {

        long totalProcessed = countDataRows(RAW_DATA_PATH);
        long validRecords = countDataRows(VALID_DATA_PATH);

        long invalidRecords =
                Math.max(totalProcessed - validRecords, 0);

        double qualityPercentage = totalProcessed == 0
                ? 0.0
                : (validRecords * 100.0) / totalProcessed;

        return new DataQualityResponse(
                totalProcessed,
                validRecords,
                invalidRecords,
                qualityPercentage
        );
    }

    private long countDataRows(String filePath) throws IOException {

        Path path = Path.of(filePath);

        if (!Files.exists(path)) {
            throw new IllegalStateException(
                    "Data quality file not found: " + filePath
            );
        }

        try (BufferedReader reader = Files.newBufferedReader(path)) {

            long count = 0;

            String line;

            boolean firstLine = true;

            while ((line = reader.readLine()) != null) {

                if (firstLine) {
                    firstLine = false;
                    continue;
                }

                if (!line.trim().isEmpty()) {
                    count++;
                }
            }

            return count;
        }
    }

    public record DataQualityResponse(
            long totalProcessed,
            long validRecords,
            long invalidRecords,
            double qualityPercentage
    ) {
    }
}