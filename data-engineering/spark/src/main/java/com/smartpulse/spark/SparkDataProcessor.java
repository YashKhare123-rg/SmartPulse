package com.smartpulse.spark;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import static org.apache.spark.sql.functions.*;

public class SparkDataProcessor {

    public static void main(String[] args) {

        SparkSession spark = SparkSession.builder()
                .appName("SmartPulse Data Transformation")
                .master("local[*]")
                .getOrCreate();

        System.out.println("Spark started successfully!");
        System.out.println("Spark version: " + spark.version());

        String inputPath = "E:/SmartPulse/data/processed/valid_machine_data.csv";
        String outputPath = "E:/SmartPulse/data/processed/machine_data_processed";
        String analyticsPath = "E:/SmartPulse/data/processed/machine_analytics";

        Dataset<Row> data = spark.read()
                .option("header", "true")
                .option("inferSchema", "true")
                .csv(inputPath);

        System.out.println();
        System.out.println("===== ORIGINAL DATA =====");
        System.out.println("Total records: " + data.count());

        System.out.println();
        System.out.println("===== DATA QUALITY STATISTICS =====");

        long totalRecords = data.count();
        long totalMachines = data.select("machine_id").distinct().count();
        long totalFailures = data.filter(col("failure").equalTo(1)).count();

        double failureRate =
                (double) totalFailures / totalRecords * 100;

        System.out.println("Total records: " + totalRecords);
        System.out.println("Total machines: " + totalMachines);
        System.out.println("Total failures: " + totalFailures);
        System.out.printf("Failure rate: %.2f%%%n", failureRate);

        System.out.println();
        System.out.println("Missing values:");

        String[] columns = data.columns();

        for (String column : columns) {

            long missingCount = data
                    .filter(
                            col(column).isNull()
                                    .or(col(column).cast("string").equalTo(""))
                    )
                    .count();

            System.out.println(
                    column + ": " + missingCount
            );
        }

        System.out.println();
        System.out.println("===== SENSOR STATISTICS =====");

        data.select(
                        min("temperature").alias("min_temperature"),
                        max("temperature").alias("max_temperature"),
                        avg("temperature").alias("avg_temperature"),

                        min("vibration").alias("min_vibration"),
                        max("vibration").alias("max_vibration"),
                        avg("vibration").alias("avg_vibration"),

                        min("pressure").alias("min_pressure"),
                        max("pressure").alias("max_pressure"),
                        avg("pressure").alias("avg_pressure"),

                        min("load_percentage").alias("min_load"),
                        max("load_percentage").alias("max_load"),
                        avg("load_percentage").alias("avg_load"),

                        min("power_consumption").alias("min_power"),
                        max("power_consumption").alias("max_power"),
                        avg("power_consumption").alias("avg_power")
                )
                .show(false);

        Dataset<Row> transformedData = data
                .withColumn(
                        "risk_score",
                        col("temperature").multiply(0.025)
                                .plus(col("vibration").multiply(0.35))
                                .plus(col("load_percentage").multiply(0.015))
                                .plus(col("operating_hours").divide(10000))
                                .plus(col("machine_age").multiply(0.04))
                )
                .withColumn(
                        "temperature_status",
                        when(col("temperature").lt(60), "NORMAL")
                                .when(col("temperature").lt(80), "WARNING")
                                .otherwise("CRITICAL")
                )
                .withColumn(
                        "load_category",
                        when(col("load_percentage").lt(50), "LOW")
                                .when(col("load_percentage").lt(80), "MEDIUM")
                                .otherwise("HIGH")
                )
                .withColumn(
                        "power_efficiency",
                        col("power_consumption").divide(col("load_percentage"))
                );

        System.out.println();
        System.out.println("===== TRANSFORMED DATA =====");

        System.out.println("Transformed columns added:");
        System.out.println("- risk_score");
        System.out.println("- temperature_status");
        System.out.println("- load_category");
        System.out.println("- power_efficiency");

        System.out.println();
        transformedData.printSchema();

        System.out.println();
        System.out.println("===== SAMPLE TRANSFORMED DATA =====");
        transformedData.show(10, false);

        transformedData.write()
                .mode("overwrite")
                .parquet(outputPath);

        System.out.println();
        System.out.println("Processed dataset saved successfully!");
        System.out.println("Location: " + outputPath);

        Dataset<Row> machineAnalytics = transformedData
                .groupBy("machine_id")
                .agg(
                        count("*").alias("total_records"),
                        avg("temperature").alias("average_temperature"),
                        max("temperature").alias("maximum_temperature"),
                        avg("vibration").alias("average_vibration"),
                        max("vibration").alias("maximum_vibration"),
                        avg("pressure").alias("average_pressure"),
                        avg("power_consumption").alias("average_power_consumption"),
                        avg("load_percentage").alias("average_load_percentage"),
                        avg("risk_score").alias("average_risk_score"),
                        max("risk_score").alias("maximum_risk_score"),
                        sum("failure").alias("total_failures")
                )
                .orderBy(desc("average_risk_score"));

        System.out.println();
        System.out.println("===== MACHINE ANALYTICS =====");

        machineAnalytics.printSchema();

        System.out.println();
        machineAnalytics.show(20, false);

        machineAnalytics.write()
                .mode("overwrite")
                .parquet(analyticsPath);

        System.out.println();
        System.out.println("===== ANALYTICS OUTPUT =====");
        System.out.println("Machine analytics saved successfully!");
        System.out.println("Location: " + analyticsPath);

        spark.stop();

        System.out.println();
        System.out.println("Spark stopped successfully!");
    }
}