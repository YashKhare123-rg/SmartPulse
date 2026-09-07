package com.smartpulse.spark;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;

import java.util.Arrays;

import static org.apache.spark.sql.functions.*;

public class StreamingDataQuality {

    public static void main(String[] args) {

        SparkSession spark = SparkSession.builder()
                .appName("SmartPulse Streaming Data Quality")
                .master("local[*]")
                .getOrCreate();

        spark.sparkContext().setLogLevel("WARN");

        System.out.println("SmartPulse Streaming Data Quality started!");
        System.out.println("Spark version: " + spark.version());

        Dataset<Row> kafkaData = spark.readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("subscribe", "machine-data")
                .option("startingOffsets", "latest")
                .load();

        Dataset<Row> machineData = kafkaData
                .selectExpr(
                        "CAST(value AS STRING) AS machine_data"
                );

        Dataset<Row> parsedData = machineData
                .select(

                        split(col("machine_data"), ",")
                                .getItem(0)
                                .alias("machine_id"),

                        split(col("machine_data"), ",")
                                .getItem(1)
                                .alias("timestamp"),

                        expr("try_cast(split(machine_data, ',')[2] AS DOUBLE)")
                                .alias("temperature"),

                        expr("try_cast(split(machine_data, ',')[3] AS DOUBLE)")
                                .alias("vibration"),

                        expr("try_cast(split(machine_data, ',')[4] AS DOUBLE)")
                                .alias("pressure"),

                        expr("try_cast(split(machine_data, ',')[5] AS DOUBLE)")
                                .alias("power_consumption"),

                        expr("try_cast(split(machine_data, ',')[6] AS DOUBLE)")
                                .alias("operating_hours"),

                        expr("try_cast(split(machine_data, ',')[7] AS DOUBLE)")
                                .alias("load_percentage"),

                        expr("try_cast(split(machine_data, ',')[8] AS DOUBLE)")
                                .alias("rotation_speed"),

                        expr("try_cast(split(machine_data, ',')[9] AS INT)")
                                .alias("maintenance_count"),

                        expr("try_cast(split(machine_data, ',')[10] AS INT)")
                                .alias("machine_age"),

                        expr("try_cast(split(machine_data, ',')[11] AS INT)")
                                .alias("failure"),

                        col("machine_data")
                );

        Dataset<Row> outputData = parsedData

                .withColumn(
                        "quality_status",

                        when(
                                size(split(col("machine_data"), ",")).notEqual(12),
                                "INVALID"
                        )

                                .when(
                                        col("machine_id").isNull()
                                                .or(
                                                        not(
                                                                col("machine_id")
                                                                        .rlike("^M\\d{3}$")
                                                        )
                                                ),
                                        "INVALID"
                                )

                                .when(
                                        expr("try_cast(timestamp AS timestamp)").isNull(),
                                        "INVALID"
                                )

                                .when(
                                        col("temperature").isNull()
                                                .or(
                                                        col("temperature").lt(20)
                                                                .or(
                                                                        col("temperature").gt(120)
                                                                )
                                                ),
                                        "INVALID"
                                )

                                .when(
                                        col("vibration").isNull()
                                                .or(
                                                        col("vibration").lt(0)
                                                                .or(
                                                                        col("vibration").gt(15)
                                                                )
                                                ),
                                        "INVALID"
                                )

                                .when(
                                        col("pressure").isNull()
                                                .or(
                                                        col("pressure").leq(0)
                                                                .or(
                                                                        col("pressure").gt(15)
                                                                )
                                                ),
                                        "INVALID"
                                )

                                .when(
                                        col("load_percentage").isNull()
                                                .or(
                                                        col("load_percentage").lt(0)
                                                                .or(
                                                                        col("load_percentage").gt(100)
                                                                )
                                                ),
                                        "INVALID"
                                )

                                .when(
                                        col("maintenance_count").isNull()
                                                .or(
                                                        col("maintenance_count").lt(0)
                                                ),
                                        "INVALID"
                                )

                                .when(
                                        col("machine_age").isNull()
                                                .or(
                                                        col("machine_age").lt(0)
                                                                .or(
                                                                        col("machine_age").gt(50)
                                                                )
                                                ),
                                        "INVALID"
                                )

                                .when(
                                        col("failure").isNull()
                                                .or(
                                                        col("failure").notEqual(0)
                                                                .and(
                                                                        col("failure").notEqual(1)
                                                                )
                                                ),
                                        "INVALID"
                                )

                                .otherwise("VALID")
                )

                .withColumn(
                        "quality_reason",

                        when(
                                size(split(col("machine_data"), ",")).notEqual(12),
                                "INVALID_COLUMN_COUNT"
                        )

                                .when(
                                        col("machine_id").isNull()
                                                .or(
                                                        not(
                                                                col("machine_id")
                                                                        .rlike("^M\\d{3}$")
                                                        )
                                                ),
                                        "INVALID_MACHINE_ID"
                                )

                                .when(
                                        expr("try_cast(timestamp AS timestamp)").isNull(),
                                        "INVALID_TIMESTAMP"
                                )

                                .when(
                                        col("temperature").isNull(),
                                        "INVALID_TEMPERATURE"
                                )

                                .when(
                                        col("temperature").lt(20)
                                                .or(
                                                        col("temperature").gt(120)
                                                ),
                                        "TEMPERATURE_OUT_OF_RANGE"
                                )

                                .when(
                                        col("vibration").isNull(),
                                        "INVALID_VIBRATION"
                                )

                                .when(
                                        col("vibration").lt(0)
                                                .or(
                                                        col("vibration").gt(15)
                                                ),
                                        "VIBRATION_OUT_OF_RANGE"
                                )

                                .when(
                                        col("pressure").isNull(),
                                        "INVALID_PRESSURE"
                                )

                                .when(
                                        col("pressure").leq(0)
                                                .or(
                                                        col("pressure").gt(15)
                                                ),
                                        "PRESSURE_OUT_OF_RANGE"
                                )

                                .when(
                                        col("load_percentage").isNull(),
                                        "INVALID_LOAD"
                                )

                                .when(
                                        col("load_percentage").lt(0)
                                                .or(
                                                        col("load_percentage").gt(100)
                                                ),
                                        "LOAD_OUT_OF_RANGE"
                                )

                                .when(
                                        col("maintenance_count").isNull(),
                                        "INVALID_MAINTENANCE_COUNT"
                                )

                                .when(
                                        col("maintenance_count").lt(0),
                                        "MAINTENANCE_COUNT_OUT_OF_RANGE"
                                )

                                .when(
                                        col("machine_age").isNull(),
                                        "INVALID_MACHINE_AGE"
                                )

                                .when(
                                        col("machine_age").lt(0)
                                                .or(
                                                        col("machine_age").gt(50)
                                                ),
                                        "MACHINE_AGE_OUT_OF_RANGE"
                                )

                                .when(
                                        col("failure").isNull(),
                                        "INVALID_FAILURE_VALUE"
                                )

                                .when(
                                        col("failure").notEqual(0)
                                                .and(
                                                        col("failure").notEqual(1)
                                                ),
                                        "INVALID_FAILURE_VALUE"
                                )

                                .otherwise("VALID")
                )

                .withColumnRenamed(
                        "machine_data",
                        "raw_machine_data"
                );

        System.out.println("Connected to Kafka topic: machine-data");
        System.out.println("Data quality validation is active.");
        System.out.println("Waiting for machine data...");

        try {

            var query = outputData.writeStream()

                    .option(
                            "checkpointLocation",
                            "E:/SmartPulse/data/processed/streaming_quality_checkpoint"
                    )

                    .foreachBatch(
                            (batch, batchId) -> {

                                System.out.println();
                                System.out.println(
                                        "========== QUALITY BATCH "
                                                + batchId
                                                + " =========="
                                );

                                batch.show(20, false);

                                long totalRecords = batch.count();

                                long validRecords = batch
                                        .filter(
                                                col("quality_status")
                                                        .equalTo("VALID")
                                        )
                                        .count();

                                long invalidRecords = batch
                                        .filter(
                                                col("quality_status")
                                                        .equalTo("INVALID")
                                        )
                                        .count();

                                System.out.println(
                                        "Total records: "
                                                + totalRecords
                                );

                                System.out.println(
                                        "Valid records: "
                                                + validRecords
                                );

                                System.out.println(
                                        "Invalid records: "
                                                + invalidRecords
                                );

                                String statisticsPath =
                                        "E:/SmartPulse/data/processed/quality_statistics";

                                StructType statisticsSchema =
                                        new StructType(
                                                new StructField[]{
                                                        new StructField(
                                                                "batch_id",
                                                                DataTypes.LongType,
                                                                false,
                                                                org.apache.spark.sql.types.Metadata.empty()
                                                        ),
                                                        new StructField(
                                                                "total_records",
                                                                DataTypes.LongType,
                                                                false,
                                                                org.apache.spark.sql.types.Metadata.empty()
                                                        ),
                                                        new StructField(
                                                                "valid_records",
                                                                DataTypes.LongType,
                                                                false,
                                                                org.apache.spark.sql.types.Metadata.empty()
                                                        ),
                                                        new StructField(
                                                                "invalid_records",
                                                                DataTypes.LongType,
                                                                false,
                                                                org.apache.spark.sql.types.Metadata.empty()
                                                        )
                                                }
                                        );

                                Dataset<Row> statistics =
                                        spark.createDataFrame(
                                                Arrays.asList(
                                                        RowFactory.create(
                                                                batchId,
                                                                totalRecords,
                                                                validRecords,
                                                                invalidRecords
                                                        )
                                                ),
                                                statisticsSchema
                                        );

                                statistics.write()
                                        .mode("append")
                                        .parquet(statisticsPath);

                                System.out.println(
                                        "Quality statistics saved to: "
                                                + statisticsPath
                                );

                                System.out.println();
                                System.out.println(
                                        "===== INVALID DATA REASONS ====="
                                );

                                batch
                                        .filter(
                                                col("quality_status")
                                                        .equalTo("INVALID")
                                        )
                                        .groupBy("quality_reason")
                                        .count()
                                        .orderBy(desc("count"))
                                        .show(false);

                                String validPath =
                                        "E:/SmartPulse/data/processed/valid_stream";

                                String invalidPath =
                                        "E:/SmartPulse/data/processed/invalid_stream";

                                if (validRecords > 0) {

                                    batch
                                            .filter(
                                                    col("quality_status")
                                                            .equalTo("VALID")
                                            )
                                            .write()
                                            .mode("append")
                                            .parquet(validPath);

                                    System.out.println(
                                            "Valid records saved to: "
                                                    + validPath
                                    );
                                }

                                if (invalidRecords > 0) {

                                    batch
                                            .filter(
                                                    col("quality_status")
                                                            .equalTo("INVALID")
                                            )
                                            .write()
                                            .mode("append")
                                            .parquet(invalidPath);

                                    System.out.println(
                                            "Invalid records quarantined to: "
                                                    + invalidPath
                                    );
                                }

                                System.out.println(
                                        "================================"
                                );
                            }
                    )

                    .start();

            query.awaitTermination();

        } catch (Exception e) {

            System.out.println(
                    "Streaming error: "
                            + e.getMessage()
            );

        } finally {

            spark.stop();

            System.out.println(
                    "SmartPulse Streaming Data Quality stopped."
            );
        }
    }
}