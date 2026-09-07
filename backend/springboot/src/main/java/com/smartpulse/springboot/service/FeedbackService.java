package com.smartpulse.springboot.service;

import com.smartpulse.springboot.model.Feedback;
import com.smartpulse.springboot.repository.FeedbackRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class FeedbackService {

    private final FeedbackRepository feedbackRepository;

    public FeedbackService(FeedbackRepository feedbackRepository) {
        this.feedbackRepository = feedbackRepository;
    }

    public Feedback createFeedback(
            String machineId,
            double predictedFailureProbability,
            double riskScore,
            String maintenanceAction,
            String actualOutcome) {

        Feedback feedback = new Feedback(
                UUID.randomUUID().toString(),
                machineId,
                predictedFailureProbability,
                riskScore,
                maintenanceAction,
                actualOutcome,
                LocalDateTime.now().toString()
        );

        feedbackRepository.save(feedback);

        return feedback;
    }

    public List<Feedback> getAllFeedback() {
        return feedbackRepository.findAll();
    }

    public Feedback getFeedbackById(String feedbackId) {
        return feedbackRepository.findById(feedbackId);
    }
}