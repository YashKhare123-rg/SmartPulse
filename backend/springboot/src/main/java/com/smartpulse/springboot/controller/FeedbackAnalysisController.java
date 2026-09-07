package com.smartpulse.springboot.controller;

import com.smartpulse.springboot.service.FeedbackAnalyzerService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/feedback-analysis")
public class FeedbackAnalysisController {

    private final FeedbackAnalyzerService feedbackAnalyzerService;

    public FeedbackAnalysisController(
            FeedbackAnalyzerService feedbackAnalyzerService) {

        this.feedbackAnalyzerService = feedbackAnalyzerService;
    }

    @GetMapping
    public FeedbackAnalyzerService.FeedbackAnalysis analyzeFeedback() {

        return feedbackAnalyzerService.analyzeFeedback();
    }
}