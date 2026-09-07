package com.smartpulse.springboot.controller;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.smartpulse.springboot.service.MaintenanceActionService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestClient;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

@RestController
@RequestMapping("/api/decision")
public class DecisionController {

    private static final String CSV_PATH =
            "E:/SmartPulse/data/processed/valid_machine_data.csv";

    private static final double REPAIR_COST = 5000.0;
    private static final double DOWNTIME_COST_PER_HOUR = 1000.0;
    private static final double EXPECTED_DOWNTIME_HOURS = 4.0;
    private static final double PREVENTIVE_MAINTENANCE_COST = 500.0;

    private final RestClient restClient;
    private final MaintenanceActionService maintenanceActionService;

    @Value("${smartpulse.ml.service.url}")
    private String mlServiceUrl;

    public DecisionController(
            RestClient.Builder restClientBuilder,
            MaintenanceActionService maintenanceActionService) {

        this.restClient = restClientBuilder.build();
        this.maintenanceActionService = maintenanceActionService;
    }

    /*
     * Normal decision endpoint.
     *
     * Maintenance actions ARE allowed.
     */
    @PostMapping
    public DecisionResponse makeDecision(
            @RequestBody DecisionRequest request) {

        return processDecision(
                request.machineId(),
                String.valueOf(request.temperature()),
                String.valueOf(request.vibration()),
                String.valueOf(request.pressure()),
                String.valueOf(request.powerConsumption()),
                String.valueOf(request.operatingHours()),
                String.valueOf(request.loadPercentage()),
                String.valueOf(request.rotationSpeed()),
                String.valueOf(request.maintenanceCount()),
                String.valueOf(request.machineAge()),
                true
        );
    }

    /*
     * What-If Analysis endpoint.
     *
     * This performs the complete analysis but DOES NOT
     * create a maintenance action or feedback record.
     */
    @PostMapping("/what-if")
    public DecisionResponse whatIfAnalysis(
            @RequestBody DecisionRequest request) {

        return processDecision(
                request.machineId(),
                String.valueOf(request.temperature()),
                String.valueOf(request.vibration()),
                String.valueOf(request.pressure()),
                String.valueOf(request.powerConsumption()),
                String.valueOf(request.operatingHours()),
                String.valueOf(request.loadPercentage()),
                String.valueOf(request.rotationSpeed()),
                String.valueOf(request.maintenanceCount()),
                String.valueOf(request.machineAge()),
                false
        );
    }

    /*
     * Decision endpoint for a specific machine.
     *
     * Maintenance actions ARE allowed.
     */
    @PostMapping("/{machineId}")
    public DecisionResponse makeDecisionForMachine(
            @PathVariable String machineId) throws IOException {

        Path path = Path.of(CSV_PATH);

        List<String> lines = Files.readAllLines(path);

        for (int i = lines.size() - 1; i >= 1; i--) {

            String[] values = lines.get(i).split(",");

            if (values.length != 12) {
                continue;
            }

            if (!values[0].equalsIgnoreCase(machineId)) {
                continue;
            }

            return processDecision(
                    values[0],
                    values[2],
                    values[3],
                    values[4],
                    values[5],
                    values[6],
                    values[7],
                    values[8],
                    values[9],
                    values[10],
                    true
            );
        }

        throw new IllegalArgumentException(
                "Machine not found: " + machineId
        );
    }

    /*
     * Explainable AI endpoint for a specific machine.
     *
     * This reads the latest machine record and sends it
     * to the FastAPI /explain endpoint.
     *
     * No maintenance action or feedback record is created.
     */
    @PostMapping("/{machineId}/explain")
    public ExplainResponse explainMachine(
            @PathVariable String machineId) throws IOException {

        Path path = Path.of(CSV_PATH);

        List<String> lines = Files.readAllLines(path);

        for (int i = lines.size() - 1; i >= 1; i--) {

            String[] values = lines.get(i).split(",");

            if (values.length != 12) {
                continue;
            }

            if (!values[0].equalsIgnoreCase(machineId)) {
                continue;
            }

            PredictionRequest request = new PredictionRequest(
                    Double.parseDouble(values[2]),
                    Double.parseDouble(values[3]),
                    Double.parseDouble(values[4]),
                    Double.parseDouble(values[5]),
                    Double.parseDouble(values[6]),
                    Double.parseDouble(values[7]),
                    Double.parseDouble(values[8]),
                    Integer.parseInt(values[9]),
                    Integer.parseInt(values[10])
            );

            ExplainResponse response = restClient
                    .post()
                    .uri(mlServiceUrl + "/explain")
                    .body(request)
                    .retrieve()
                    .body(ExplainResponse.class);

            if (response == null) {
                throw new IllegalStateException(
                        "ML service returned no XAI explanation"
                );
            }

            return response;
        }

        throw new IllegalArgumentException(
                "Machine not found: " + machineId
        );
    }

    /*
     * Main decision-processing method.
     *
     * createMaintenanceAction:
     * true  = normal decision, maintenance can be created
     * false = what-if simulation, no maintenance is created
     */
    private DecisionResponse processDecision(
            String machineId,
            String temperature,
            String vibration,
            String pressure,
            String powerConsumption,
            String operatingHours,
            String loadPercentage,
            String rotationSpeed,
            String maintenanceCount,
            String machineAge,
            boolean createMaintenanceAction) {

        /*
         * STEP 1
         * Get failure probability from ML service.
         */
        Double failureProbability = restClient
                .post()
                .uri(mlServiceUrl + "/predict")
                .body(new PredictionRequest(
                        Double.parseDouble(temperature),
                        Double.parseDouble(vibration),
                        Double.parseDouble(pressure),
                        Double.parseDouble(powerConsumption),
                        Double.parseDouble(operatingHours),
                        Double.parseDouble(loadPercentage),
                        Double.parseDouble(rotationSpeed),
                        Integer.parseInt(maintenanceCount),
                        Integer.parseInt(machineAge)
                ))
                .retrieve()
                .body(Double.class);

        if (failureProbability == null) {
            throw new IllegalStateException(
                    "ML service returned no failure probability"
            );
        }

        /*
         * STEP 2
         * Get data drift information.
         */
        DriftResponse dataDrift = restClient
                .get()
                .uri(mlServiceUrl + "/data-drift")
                .retrieve()
                .body(DriftResponse.class);

        if (dataDrift == null || dataDrift.overallStatus() == null) {
            throw new IllegalStateException(
                    "ML service returned invalid data drift response"
            );
        }

        /*
         * STEP 3
         * Get model drift information.
         */
        ModelDriftResponse modelDrift = restClient
                .get()
                .uri(mlServiceUrl + "/model-drift")
                .retrieve()
                .body(ModelDriftResponse.class);

        if (modelDrift == null || modelDrift.overallStatus() == null) {
            throw new IllegalStateException(
                    "ML service returned invalid model drift response"
            );
        }

        /*
         * STEP 4
         * Cost analysis.
         */
        CostAnalysisResponse costAnalysis = restClient
                .post()
                .uri(mlServiceUrl + "/cost-analysis")
                .body(new CostAnalysisRequest(
                        failureProbability,
                        PREVENTIVE_MAINTENANCE_COST,
                        REPAIR_COST,
                        DOWNTIME_COST_PER_HOUR,
                        EXPECTED_DOWNTIME_HOURS
                ))
                .retrieve()
                .body(CostAnalysisResponse.class);

        if (costAnalysis == null) {
            throw new IllegalStateException(
                    "ML service returned no cost analysis"
            );
        }

        /*
         * STEP 5
         * Calculate SmartPulse risk score.
         */
        double riskScore =
                calculateRiskScore(
                        failureProbability,
                        dataDrift.overallStatus(),
                        modelDrift.overallStatus(),
                        Integer.parseInt(machineAge),
                        Integer.parseInt(maintenanceCount),
                        Double.parseDouble(temperature),
                        Double.parseDouble(vibration),
                        Double.parseDouble(pressure),
                        Double.parseDouble(loadPercentage)
                );

        String riskLevel = determineRiskLevel(riskScore);

        String priority = determinePriority(riskScore);

        String recommendation = determineRecommendation(riskScore);

        /*
         * STEP 6
         * Make final maintenance decision.
         */
        String finalDecision = determineFinalDecision(
                riskScore,
                dataDrift.overallStatus(),
                modelDrift.overallStatus(),
                costAnalysis
        );

        String finalReason = determineFinalReason(
                riskScore,
                dataDrift.overallStatus(),
                modelDrift.overallStatus(),
                costAnalysis
        );

        /*
         * STEP 7
         * Automatically create maintenance action
         * only when explicitly allowed.
         */
        if (createMaintenanceAction
                && (finalDecision.equals("SCHEDULE MAINTENANCE")
                || finalDecision.equals("URGENT MAINTENANCE")
                || finalDecision.equals("EMERGENCY ACTION"))) {

            maintenanceActionService.createAction(
                    machineId,
                    finalDecision,
                    priority,
                    finalReason,
                    failureProbability,
                    riskScore
            );
        }

        /*
         * Calculate expected cost components.
         */
        double expectedRepairCost =
                failureProbability * REPAIR_COST;

        double expectedDowntimeCost =
                failureProbability
                        * DOWNTIME_COST_PER_HOUR
                        * EXPECTED_DOWNTIME_HOURS;

        /*
         * STEP 8
         * Return complete decision response.
         */
        return new DecisionResponse(
                machineId,
                failureProbability,
                dataDrift.overallStatus(),
                modelDrift.overallStatus(),
                expectedRepairCost,
                expectedDowntimeCost,
                costAnalysis.expectedFailureCost(),
                costAnalysis.preventiveMaintenanceCost(),
                costAnalysis.maintenanceRecommended()
                        ? "MAINTENANCE RECOMMENDED"
                        : "MAINTENANCE NOT REQUIRED",
                costAnalysis.potentialSavings(),
                riskScore,
                riskLevel,
                priority,
                recommendation,
                finalDecision,
                finalReason
        );
    }

    private double calculateRiskScore(
            double failureProbability,
            String dataDriftStatus,
            String modelDriftStatus,
            int machineAge,
            int maintenanceCount,
            double temperature,
            double vibration,
            double pressure,
            double loadPercentage) {

        double score = failureProbability * 70;

        if (dataDriftStatus.equalsIgnoreCase("DRIFT")) {
            score += 10;
        } else if (dataDriftStatus.equalsIgnoreCase("WARNING")) {
            score += 5;
        }

        if (modelDriftStatus.equalsIgnoreCase("DRIFT")) {
            score += 15;
        } else if (modelDriftStatus.equalsIgnoreCase("WARNING")) {
            score += 7;
        }

        if (machineAge >= 15) {
            score += 5;
        } else if (machineAge >= 10) {
            score += 3;
        }

        if (maintenanceCount == 0) {
            score += 3;
        }

        if (temperature >= 100) {
            score += 5;
        } else if (temperature >= 90) {
            score += 3;
        }

        if (vibration >= 10) {
            score += 5;
        } else if (vibration >= 8) {
            score += 3;
        }

        if (pressure >= 12) {
            score += 4;
        } else if (pressure >= 10) {
            score += 2;
        }

        if (loadPercentage >= 90) {
            score += 4;
        } else if (loadPercentage >= 80) {
            score += 2;
        }

        return Math.min(score, 100);
    }

    private String determineRiskLevel(double riskScore) {

        if (riskScore >= 80) {
            return "CRITICAL";
        }

        if (riskScore >= 60) {
            return "HIGH";
        }

        if (riskScore >= 30) {
            return "MEDIUM";
        }

        return "LOW";
    }

    private String determinePriority(double riskScore) {

        if (riskScore >= 80) {
            return "CRITICAL";
        }

        if (riskScore >= 60) {
            return "HIGH";
        }

        if (riskScore >= 30) {
            return "MEDIUM";
        }

        return "LOW";
    }

    private String determineRecommendation(double riskScore) {

        if (riskScore >= 80) {
            return "Immediate emergency action";
        }

        if (riskScore >= 60) {
            return "Urgent maintenance";
        }

        if (riskScore >= 30) {
            return "Schedule maintenance";
        }

        return "Continue normal operation";
    }

    private String determineFinalDecision(
            double riskScore,
            String dataDriftStatus,
            String modelDriftStatus,
            CostAnalysisResponse costAnalysis) {

        if (riskScore >= 80) {
            return "EMERGENCY ACTION";
        }

        if (modelDriftStatus.equalsIgnoreCase("DRIFT")
                && riskScore >= 60) {
            return "MODEL VALIDATION REQUIRED";
        }

        if (riskScore >= 60
                && costAnalysis.expectedFailureCost()
                > costAnalysis.preventiveMaintenanceCost()) {

            return "URGENT MAINTENANCE";
        }

        if (riskScore >= 30
                && costAnalysis.expectedFailureCost()
                > costAnalysis.preventiveMaintenanceCost()) {

            return "SCHEDULE MAINTENANCE";
        }

        if (riskScore < 30
                && !dataDriftStatus.equalsIgnoreCase("STABLE")) {

            return "CONTINUE WITH ENHANCED MONITORING";
        }

        return "CONTINUE NORMAL OPERATION";
    }

    private String determineFinalReason(
            double riskScore,
            String dataDriftStatus,
            String modelDriftStatus,
            CostAnalysisResponse costAnalysis) {

        if (riskScore >= 80) {
            return "Critical risk score requires immediate emergency action";
        }

        if (modelDriftStatus.equalsIgnoreCase("DRIFT")
                && riskScore >= 60) {
            return "High risk combined with model drift requires model validation";
        }

        if (riskScore >= 60
                && costAnalysis.expectedFailureCost()
                > costAnalysis.preventiveMaintenanceCost()) {

            return "High risk and expected failure cost significantly exceeds preventive maintenance cost";
        }

        if (riskScore >= 30
                && costAnalysis.expectedFailureCost()
                > costAnalysis.preventiveMaintenanceCost()) {

            return "Expected failure cost exceeds preventive maintenance cost";
        }

        if (riskScore < 30
                && !dataDriftStatus.equalsIgnoreCase("STABLE")) {

            return "Low risk but data drift requires enhanced monitoring";
        }

        return "Risk and expected failure cost do not justify maintenance";
    }

    public record DecisionRequest(
            String machineId,
            double temperature,
            double vibration,
            double pressure,
            double powerConsumption,
            double operatingHours,
            double loadPercentage,
            double rotationSpeed,
            int maintenanceCount,
            int machineAge
    ) {
    }

    public record PredictionRequest(
            double temperature,
            double vibration,
            double pressure,
            double power_consumption,
            double operating_hours,
            double load_percentage,
            double rotation_speed,
            int maintenance_count,
            int machine_age
    ) {
    }

    public record ExplainResponse(
            @JsonProperty("failure_probability")
            double failureProbability,

            @JsonProperty("base_intercept")
            double baseIntercept,

            List<ExplanationFeature> explanations
    ) {
    }

    public record ExplanationFeature(
            String feature,
            double value,

            @JsonProperty("scaled_value")
            double scaledValue,

            double contribution,

            @JsonProperty("absolute_contribution")
            double absoluteContribution,

            String direction,
            String impact
    ) {
    }

    public record DriftResponse(
            @JsonProperty("overall_status")
            String overallStatus,

            List<DriftFeature> features
    ) {
    }

    public record DriftFeature(
            String feature,
            double psi,
            String status
    ) {
    }

    public record ModelDriftResponse(
            @JsonProperty("overall_status")
            String overallStatus,

            List<ModelDriftMetric> metrics
    ) {
    }

    public record ModelDriftMetric(
            String metric,

            @JsonProperty("reference_value")
            double referenceValue,

            @JsonProperty("current_value")
            double currentValue,

            @JsonProperty("relative_change")
            double relativeChange,

            String status
    ) {
    }

    public record CostAnalysisRequest(
            double failure_probability,
            double preventive_maintenance_cost,
            double repair_cost,
            double downtime_cost_per_hour,
            double expected_downtime_hours
    ) {
    }

    public record CostAnalysisResponse(
            @JsonProperty("failure_probability")
            double failureProbability,

            @JsonProperty("expected_failure_cost")
            double expectedFailureCost,

            @JsonProperty("preventive_maintenance_cost")
            double preventiveMaintenanceCost,

            @JsonProperty("potential_savings")
            double potentialSavings,

            @JsonProperty("maintenance_recommended")
            boolean maintenanceRecommended
    ) {
    }

    public record DecisionResponse(
            String machineId,
            double failureProbability,
            String dataDriftStatus,
            String modelDriftStatus,
            double expectedRepairCost,
            double expectedDowntimeCost,
            double totalExpectedFailureCost,
            double preventiveMaintenanceCost,
            String costDecision,
            double potentialSavings,
            double riskScore,
            String riskLevel,
            String priority,
            String recommendation,
            String finalDecision,
            String finalReason
    ) {
    }
}