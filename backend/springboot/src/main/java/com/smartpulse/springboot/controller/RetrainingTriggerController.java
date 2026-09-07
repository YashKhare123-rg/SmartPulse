package com.smartpulse.springboot.controller;

import com.smartpulse.springboot.service.RetrainingTriggerService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/retraining")
public class RetrainingTriggerController {

    private final RetrainingTriggerService retrainingTriggerService;

    public RetrainingTriggerController(
            RetrainingTriggerService retrainingTriggerService) {

        this.retrainingTriggerService = retrainingTriggerService;
    }

    @GetMapping("/check")
    public RetrainingTriggerService.RetrainingDecision checkRetraining() {

        return retrainingTriggerService.checkRetrainingRequired();
    }
}