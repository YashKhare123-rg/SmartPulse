package com.smartpulse.springboot.controller;

import com.smartpulse.springboot.model.MaintenanceAction;
import com.smartpulse.springboot.service.MaintenanceActionService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/maintenance")
public class MaintenanceActionController {

    private final MaintenanceActionService maintenanceActionService;

    public MaintenanceActionController(
            MaintenanceActionService maintenanceActionService) {

        this.maintenanceActionService = maintenanceActionService;
    }

    @PostMapping
    public MaintenanceAction createAction(
            @RequestBody MaintenanceActionRequest request) {

        return maintenanceActionService.createAction(
                request.machineId(),
                request.action(),
                request.priority(),
                request.reason(),
                request.failureProbability(),
                request.riskScore()
        );
    }

    @GetMapping
    public List<MaintenanceAction> getAllActions() {
        return maintenanceActionService.getAllActions();
    }

    @GetMapping("/{actionId}")
    public MaintenanceAction getActionById(
            @PathVariable String actionId) {

        return maintenanceActionService.getActionById(actionId);
    }
    @PutMapping("/{actionId}/status")
    public MaintenanceAction updateStatus(
            @PathVariable String actionId,
            @RequestParam String status) {

        MaintenanceAction action =
                maintenanceActionService.updateStatus(
                        actionId,
                        status
                );

        if (action == null) {
            throw new IllegalArgumentException(
                    "Maintenance action not found: " + actionId
            );
        }

        return action;
    }
    @PutMapping("/{actionId}/complete")
    public MaintenanceAction completeAction(
            @PathVariable String actionId,
            @RequestParam String actualOutcome) {

        MaintenanceAction action =
                maintenanceActionService.completeAction(
                        actionId,
                        actualOutcome
                );

        if (action == null) {
            throw new IllegalArgumentException(
                    "Maintenance action not found: " + actionId
            );
        }

        return action;
    }

    public record MaintenanceActionRequest(
            String machineId,
            String action,
            String priority,
            String reason,
            double failureProbability,
            double riskScore
    ) {
    }
}