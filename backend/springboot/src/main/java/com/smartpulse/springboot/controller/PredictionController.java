package com.smartpulse.springboot.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;
import org.springframework.beans.factory.annotation.Value;

@RestController
public class PredictionController {

    private final RestClient restClient;

    public PredictionController(
            RestClient.Builder builder,
            @Value("${smartpulse.ml.service.url}") String mlServiceUrl) {

        this.restClient = builder
                .baseUrl(mlServiceUrl)
                .build();
    }

    @PostMapping("/api/predict")
    public PredictionResponse predict(@RequestBody PredictionRequest request) {

        MlPredictionRequest mlRequest = new MlPredictionRequest(
                request.temperature(),
                request.vibration(),
                request.pressure(),
                request.powerConsumption(),
                request.operatingHours(),
                request.loadPercentage(),
                request.rotationSpeed(),
                request.maintenanceCount(),
                request.machineAge()
        );

        MlPredictionResponse mlResponse = restClient.post()
                .uri("/predict")
                .body(mlRequest)
                .retrieve()
                .body(MlPredictionResponse.class);

        return new PredictionResponse(
                request.machineId(),
                mlResponse.failureProbability(),
                mlResponse.riskLevel()
        );
    }

    public record PredictionRequest(
            String machineId,
            double temperature,
            double vibration,
            double pressure,
            double powerConsumption,
            double operatingHours,
            double loadPercentage,
            double rotationSpeed,
            int maintenanceCount,
            int machineAge
    ) {
    }

    public record MlPredictionRequest(
            double temperature,
            double vibration,
            double pressure,
            double power_consumption,
            double operating_hours,
            double load_percentage,
            double rotation_speed,
            int maintenance_count,
            int machine_age
    ) {
    }

    public record MlPredictionResponse(
            double failureProbability,
            String riskLevel
    ) {
    }

    public record PredictionResponse(
            String machineId,
            double failureProbability,
            String riskLevel
    ) {
    }
}