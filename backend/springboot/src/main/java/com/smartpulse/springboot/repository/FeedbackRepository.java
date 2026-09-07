package com.smartpulse.springboot.repository;

import com.smartpulse.springboot.model.Feedback;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class FeedbackRepository {

    private final JdbcTemplate jdbcTemplate;

    public FeedbackRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public void save(Feedback feedback) {

        String sql = """
                INSERT INTO feedback (
                    feedback_id,
                    machine_id,
                    predicted_failure_probability,
                    risk_score,
                    maintenance_action,
                    actual_outcome,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """;

        jdbcTemplate.update(
                sql,
                feedback.getFeedbackId(),
                feedback.getMachineId(),
                feedback.getPredictedFailureProbability(),
                feedback.getRiskScore(),
                feedback.getMaintenanceAction(),
                feedback.getActualOutcome(),
                feedback.getCreatedAt()
        );
    }

    public List<Feedback> findAll() {

        String sql = """
                SELECT
                    feedback_id,
                    machine_id,
                    predicted_failure_probability,
                    risk_score,
                    maintenance_action,
                    actual_outcome,
                    created_at
                FROM feedback
                ORDER BY created_at DESC
                """;

        return jdbcTemplate.query(
                sql,
                (rs, rowNum) -> new Feedback(
                        rs.getString("feedback_id"),
                        rs.getString("machine_id"),
                        rs.getDouble("predicted_failure_probability"),
                        rs.getDouble("risk_score"),
                        rs.getString("maintenance_action"),
                        rs.getString("actual_outcome"),
                        rs.getString("created_at")
                )
        );
    }

    public Feedback findById(String feedbackId) {

        String sql = """
                SELECT
                    feedback_id,
                    machine_id,
                    predicted_failure_probability,
                    risk_score,
                    maintenance_action,
                    actual_outcome,
                    created_at
                FROM feedback
                WHERE feedback_id = ?
                """;

        List<Feedback> results = jdbcTemplate.query(
                sql,
                (rs, rowNum) -> new Feedback(
                        rs.getString("feedback_id"),
                        rs.getString("machine_id"),
                        rs.getDouble("predicted_failure_probability"),
                        rs.getDouble("risk_score"),
                        rs.getString("maintenance_action"),
                        rs.getString("actual_outcome"),
                        rs.getString("created_at")
                ),
                feedbackId
        );

        if (results.isEmpty()) {
            return null;
        }

        return results.get(0);
    }
}