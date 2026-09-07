package com.smartpulse.springboot.controller;

import com.smartpulse.springboot.model.Feedback;
import com.smartpulse.springboot.service.FeedbackService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/feedback")
public class FeedbackController {

    private final FeedbackService feedbackService;

    public FeedbackController(FeedbackService feedbackService) {
        this.feedbackService = feedbackService;
    }

    @GetMapping
    public List<Feedback> getAllFeedback() {
        return feedbackService.getAllFeedback();
    }

    @GetMapping("/{feedbackId}")
    public Feedback getFeedbackById(
            @PathVariable String feedbackId) {

        Feedback feedback =
                feedbackService.getFeedbackById(feedbackId);

        if (feedback == null) {
            throw new IllegalArgumentException(
                    "Feedback not found: " + feedbackId
            );
        }

        return feedback;
    }
}