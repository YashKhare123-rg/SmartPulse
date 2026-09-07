package com.smartpulse.springboot.controller;

import com.smartpulse.springboot.service.RetrainingMLService;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/retraining")
public class RetrainingController {

    private final RetrainingMLService retrainingMLService;

    public RetrainingController(
            RetrainingMLService retrainingMLService) {

        this.retrainingMLService = retrainingMLService;
    }

    @PostMapping("/execute")
    public Map<String, Object> executeRetraining() {

        return retrainingMLService.executeRetraining();
    }
}