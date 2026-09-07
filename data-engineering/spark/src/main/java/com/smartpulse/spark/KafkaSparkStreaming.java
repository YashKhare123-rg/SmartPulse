package com.smartpulse.spark;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import static org.apache.spark.sql.functions.*;

public class KafkaSparkStreaming {

    public static void main(String[] args) {

        SparkSession spark = SparkSession.builder()
                .appName("SmartPulse Kafka Streaming")
                .master("local[*]")
                .getOrCreate();

        spark.sparkContext().setLogLevel("WARN");

        System.out.println("SmartPulse Kafka-Spark Streaming started!");
        System.out.println("Spark version: " + spark.version());

        Dataset<Row> kafkaData = spark.readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("subscribe", "machine-data")
                .option("startingOffsets", "latest")
                .load();

        Dataset<Row> machineData = kafkaData
                .selectExpr(
                        "CAST(key AS STRING) AS machine_id",
                        "CAST(value AS STRING) AS machine_data"
                );

        Dataset<Row> parsedData = machineData
                .select(
                        split(col("machine_data"), ",").getItem(0).alias("machine_id"),
                        split(col("machine_data"), ",").getItem(1).alias("timestamp"),
                        split(col("machine_data"), ",").getItem(2).cast("double").alias("temperature"),
                        split(col("machine_data"), ",").getItem(3).cast("double").alias("vibration"),
                        split(col("machine_data"), ",").getItem(4).cast("double").alias("pressure"),
                        split(col("machine_data"), ",").getItem(5).cast("double").alias("power_consumption"),
                        split(col("machine_data"), ",").getItem(6).cast("double").alias("operating_hours"),
                        split(col("machine_data"), ",").getItem(7).cast("double").alias("load_percentage"),
                        split(col("machine_data"), ",").getItem(8).cast("double").alias("rotation_speed"),
                        split(col("machine_data"), ",").getItem(9).cast("int").alias("maintenance_count"),
                        split(col("machine_data"), ",").getItem(10).cast("int").alias("machine_age"),
                        split(col("machine_data"), ",").getItem(11).cast("int").alias("failure")
                );

        System.out.println("Connected to Kafka topic: machine-data");
        System.out.println("Waiting for machine data...");

        try {

            var query = parsedData.writeStream()
                    .format("console")
                    .outputMode("append")
                    .option("truncate", "false")
                    .option("numRows", 20)
                    .start();

            query.awaitTermination();

        } catch (Exception e) {

            System.out.println(
                    "Streaming error: " + e.getMessage()
            );

        } finally {

            spark.stop();

            System.out.println(
                    "SmartPulse Kafka-Spark Streaming stopped."
            );
        }
    }
}