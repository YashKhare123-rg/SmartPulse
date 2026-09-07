package com.smartpulse.springboot.repository;

import com.smartpulse.springboot.model.MaintenanceAction;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class MaintenanceActionRepository {

    private final JdbcTemplate jdbcTemplate;

    public MaintenanceActionRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public void save(MaintenanceAction action) {

        String sql = """
                INSERT INTO maintenance_actions (
                    action_id,
                    machine_id,
                    action,
                    priority,
                    status,
                    reason,
                    failure_probability,
                    risk_score,
                    created_at,
                    completed_at,
                    actual_outcome
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """;

        jdbcTemplate.update(
                sql,
                action.getActionId(),
                action.getMachineId(),
                action.getAction(),
                action.getPriority(),
                action.getStatus(),
                action.getReason(),
                action.getFailureProbability(),
                action.getRiskScore(),
                action.getCreatedAt(),
                action.getCompletedAt(),
                action.getActualOutcome()
        );
    }

    public List<MaintenanceAction> findAll() {

        String sql = """
                SELECT
                    action_id,
                    machine_id,
                    action,
                    priority,
                    status,
                    reason,
                    failure_probability,
                    risk_score,
                    created_at,
                    completed_at,
                    actual_outcome
                FROM maintenance_actions
                ORDER BY created_at DESC
                """;

        return jdbcTemplate.query(
                sql,
                (rs, rowNum) -> new MaintenanceAction(
                        rs.getString("action_id"),
                        rs.getString("machine_id"),
                        rs.getString("action"),
                        rs.getString("priority"),
                        rs.getString("status"),
                        rs.getString("reason"),
                        rs.getDouble("failure_probability"),
                        rs.getDouble("risk_score"),
                        rs.getString("created_at"),
                        rs.getString("completed_at"),
                        rs.getString("actual_outcome")
                )
        );
    }

    public MaintenanceAction findById(String actionId) {

        String sql = """
                SELECT
                    action_id,
                    machine_id,
                    action,
                    priority,
                    status,
                    reason,
                    failure_probability,
                    risk_score,
                    created_at,
                    completed_at,
                    actual_outcome
                FROM maintenance_actions
                WHERE action_id = ?
                """;

        List<MaintenanceAction> results = jdbcTemplate.query(
                sql,
                (rs, rowNum) -> new MaintenanceAction(
                        rs.getString("action_id"),
                        rs.getString("machine_id"),
                        rs.getString("action"),
                        rs.getString("priority"),
                        rs.getString("status"),
                        rs.getString("reason"),
                        rs.getDouble("failure_probability"),
                        rs.getDouble("risk_score"),
                        rs.getString("created_at"),
                        rs.getString("completed_at"),
                        rs.getString("actual_outcome")
                ),
                actionId
        );

        if (results.isEmpty()) {
            return null;
        }

        return results.get(0);
    }

    public void updateStatus(
            String actionId,
            String status
    ) {

        String sql = """
                UPDATE maintenance_actions
                SET status = ?
                WHERE action_id = ?
                """;

        jdbcTemplate.update(
                sql,
                status,
                actionId
        );
    }

    public void completeAction(
            String actionId,
            String status,
            String completedAt,
            String actualOutcome
    ) {

        String sql = """
                UPDATE maintenance_actions
                SET
                    status = ?,
                    completed_at = ?,
                    actual_outcome = ?
                WHERE action_id = ?
                """;

        jdbcTemplate.update(
                sql,
                status,
                completedAt,
                actualOutcome,
                actionId
        );
    }
}