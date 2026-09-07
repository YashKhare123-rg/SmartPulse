package com.smartpulse.springboot.service;

import com.smartpulse.springboot.model.Feedback;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class FeedbackAnalyzerService {

    private final FeedbackService feedbackService;

    public FeedbackAnalyzerService(
            FeedbackService feedbackService) {

        this.feedbackService = feedbackService;
    }

    public FeedbackAnalysis analyzeFeedback() {

        List<Feedback> feedbackRecords =
                feedbackService.getAllFeedback();

        int totalRecords = feedbackRecords.size();

        if (totalRecords == 0) {
            return new FeedbackAnalysis(
                    0,
                    0,
                    0,
                    0,
                    0,
                    "INSUFFICIENT DATA"
            );
        }

        int successfulMaintenance = 0;
        int failedMaintenance = 0;

        for (Feedback feedback : feedbackRecords) {

            if ("MAINTENANCE_SUCCESSFUL"
                    .equalsIgnoreCase(feedback.getActualOutcome())) {

                successfulMaintenance++;

            } else if ("MAINTENANCE_FAILED"
                    .equalsIgnoreCase(feedback.getActualOutcome())) {

                failedMaintenance++;
            }
        }

        double successRate =
                (successfulMaintenance * 100.0)
                        / totalRecords;

        double failureRate =
                (failedMaintenance * 100.0)
                        / totalRecords;

        String learningStatus;

        if (totalRecords < 3) {
            learningStatus = "INSUFFICIENT DATA";
        } else if (failureRate > 10) {
            learningStatus = "RETRAINING RECOMMENDED";
        } else {
            learningStatus = "LEARNING SIGNAL ACCEPTABLE";
        }

        return new FeedbackAnalysis(
                totalRecords,
                successfulMaintenance,
                failedMaintenance,
                successRate,
                failureRate,
                learningStatus
        );
    }

    public record FeedbackAnalysis(
            int totalRecords,
            int successfulMaintenance,
            int failedMaintenance,
            double successRate,
            double failureRate,
            String learningStatus
    ) {
    }
}