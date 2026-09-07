package com.smartpulse.springboot.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class RetrainingMLService {

    private final RestClient restClient;

    public RetrainingMLService(
            @Value("${smartpulse.ml.service.url}") String mlServiceUrl) {

        this.restClient = RestClient.builder()
                .baseUrl(mlServiceUrl)
                .build();
    }

    public Map<String, Object> executeRetraining() {

        return restClient.post()
                .uri("/retrain")
                .retrieve()
                .body(Map.class);
    }
}