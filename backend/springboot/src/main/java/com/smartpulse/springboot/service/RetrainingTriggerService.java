package com.smartpulse.springboot.service;

import org.springframework.stereotype.Service;

@Service
public class RetrainingTriggerService {

    private final FeedbackService feedbackService;
    private final FeedbackAnalyzerService feedbackAnalyzerService;

    private static final int MIN_FEEDBACK_RECORDS = 20;
    private static final int MIN_ACTUAL_FAILURES = 3;
    private static final double MAX_FAILURE_RATE = 10.0;

    public RetrainingTriggerService(
            FeedbackService feedbackService,
            FeedbackAnalyzerService feedbackAnalyzerService) {

        this.feedbackService = feedbackService;
        this.feedbackAnalyzerService = feedbackAnalyzerService;
    }

    public RetrainingDecision checkRetrainingRequired() {

        FeedbackAnalyzerService.FeedbackAnalysis analysis =
                feedbackAnalyzerService.analyzeFeedback();

        int totalRecords = analysis.totalRecords();
        int actualFailures = analysis.failedMaintenance();
        double failureRate = analysis.failureRate();

        boolean enoughFeedback =
                totalRecords >= MIN_FEEDBACK_RECORDS;

        boolean enoughFailures =
                actualFailures >= MIN_ACTUAL_FAILURES;

        boolean excessiveFailureRate =
                failureRate > MAX_FAILURE_RATE;

        boolean retrainingRequired =
                enoughFeedback
                        && enoughFailures
                        && excessiveFailureRate;

        String reason;

        if (retrainingRequired) {

            reason = "Feedback indicates that model retraining is required";

        } else if (!enoughFeedback) {

            reason = "Insufficient feedback data";

        } else if (!enoughFailures) {

            reason = "Insufficient actual failure cases";

        } else {

            reason = "Feedback performance is within acceptable limits";
        }

        return new RetrainingDecision(
                retrainingRequired,
                totalRecords,
                actualFailures,
                failureRate,
                reason
        );
    }

    public record RetrainingDecision(
            boolean retrainingRequired,
            int totalFeedbackRecords,
            int actualFailures,
            double failureRate,
            String reason
    ) {
    }
}