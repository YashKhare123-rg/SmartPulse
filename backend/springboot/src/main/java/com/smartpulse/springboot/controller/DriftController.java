package com.smartpulse.springboot.controller;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

import java.util.List;

@RestController
@RequestMapping("/api")
public class DriftController {

    private final RestClient restClient;

    @Value("${smartpulse.ml.service.url}")
    private String mlServiceUrl;

    public DriftController(RestClient.Builder restClientBuilder) {
        this.restClient = restClientBuilder.build();
    }

    @GetMapping("/data-drift")
    public DataDriftResponse getDataDrift() {

        DataDriftResponse response = restClient
                .get()
                .uri(mlServiceUrl + "/data-drift")
                .retrieve()
                .body(DataDriftResponse.class);

        if (response == null) {
            throw new IllegalStateException(
                    "ML service returned no data drift response"
            );
        }

        return response;
    }

    @GetMapping("/model-drift")
    public ModelDriftResponse getModelDrift() {

        ModelDriftResponse response = restClient
                .get()
                .uri(mlServiceUrl + "/model-drift")
                .retrieve()
                .body(ModelDriftResponse.class);

        if (response == null) {
            throw new IllegalStateException(
                    "ML service returned no model drift response"
            );
        }

        return response;
    }

    public record DataDriftResponse(
            @JsonProperty("overall_status")
            String overallStatus,

            List<DriftFeature> features
    ) {
    }

    public record DriftFeature(
            String feature,
            double psi,
            String status
    ) {
    }

    public record ModelDriftResponse(
            @JsonProperty("overall_status")
            String overallStatus,

            List<ModelDriftMetric> metrics
    ) {
    }

    public record ModelDriftMetric(
            String metric,

            @JsonProperty("reference_value")
            double referenceValue,

            @JsonProperty("current_value")
            double currentValue,

            @JsonProperty("relative_change")
            double relativeChange,

            String status
    ) {
    }
}