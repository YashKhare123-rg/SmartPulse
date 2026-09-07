package com.smartpulse.springboot.service;

import com.smartpulse.springboot.model.MaintenanceAction;
import com.smartpulse.springboot.repository.MaintenanceActionRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class MaintenanceActionService {

    private final MaintenanceActionRepository maintenanceActionRepository;
    private final FeedbackService feedbackService;

    public MaintenanceActionService(
            MaintenanceActionRepository maintenanceActionRepository,
            FeedbackService feedbackService) {

        this.maintenanceActionRepository = maintenanceActionRepository;
        this.feedbackService = feedbackService;
    }

    public MaintenanceAction createAction(
            String machineId,
            String action,
            String priority,
            String reason,
            double failureProbability,
            double riskScore) {

        MaintenanceAction maintenanceAction =
                new MaintenanceAction(
                        UUID.randomUUID().toString(),
                        machineId,
                        action,
                        priority,
                        "PENDING",
                        reason,
                        failureProbability,
                        riskScore,
                        LocalDateTime.now().toString(),
                        null,
                        null
                );

        maintenanceActionRepository.save(
                maintenanceAction
        );

        return maintenanceAction;
    }

    public List<MaintenanceAction> getAllActions() {

        return maintenanceActionRepository.findAll();
    }

    public MaintenanceAction getActionById(
            String actionId) {

        return maintenanceActionRepository.findById(
                actionId
        );
    }

    public MaintenanceAction updateStatus(
            String actionId,
            String status) {

        MaintenanceAction action =
                getActionById(actionId);

        if (action == null) {
            return null;
        }

        maintenanceActionRepository.updateStatus(
                actionId,
                status
        );

        action.setStatus(status);

        return action;
    }

    public MaintenanceAction completeAction(
            String actionId,
            String actualOutcome) {

        MaintenanceAction action =
                getActionById(actionId);

        if (action == null) {
            return null;
        }

        String completedAt =
                LocalDateTime.now().toString();

        maintenanceActionRepository.completeAction(
                actionId,
                "COMPLETED",
                completedAt,
                actualOutcome
        );

        action.setStatus("COMPLETED");
        action.setCompletedAt(completedAt);
        action.setActualOutcome(actualOutcome);

        feedbackService.createFeedback(
                action.getMachineId(),
                action.getFailureProbability(),
                action.getRiskScore(),
                action.getAction(),
                actualOutcome
        );

        return action;
    }
}