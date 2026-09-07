package com.smartpulse.simulator;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.time.LocalDateTime;
import java.util.Properties;
import java.util.Random;

public class KafkaMachineProducer {

    public static void main(String[] args) {

        Properties properties = new Properties();

        properties.put(
                "bootstrap.servers",
                "localhost:9092"
        );

        properties.put(
                "key.serializer",
                "org.apache.kafka.common.serialization.StringSerializer"
        );

        properties.put(
                "value.serializer",
                "org.apache.kafka.common.serialization.StringSerializer"
        );

        KafkaProducer<String, String> producer =
                new KafkaProducer<>(properties);

        Random random = new Random();

        System.out.println("SmartPulse Kafka Machine Producer started...");
        System.out.println("Sending machine data to topic: machine-data");

        try {

            while (true) {

                String machineId =
                        String.format(
                                "M%03d",
                                1 + random.nextInt(100)
                        );

                double temperature =
                        40 + random.nextDouble() * 50;

                double vibration =
                        1 + random.nextDouble() * 5;

                double pressure =
                        4 + random.nextDouble() * 3;

                double powerConsumption =
                        4 + random.nextDouble() * 7;

                double operatingHours =
                        500 + random.nextDouble() * 5000;

                double loadPercentage =
                        20 + random.nextDouble() * 80;

                double rotationSpeed =
                        1000 + random.nextDouble() * 700;

                int maintenanceCount =
                        random.nextInt(8);

                int machineAge =
                        1 + random.nextInt(10);

                double riskScore =
                        (temperature * 0.025)
                                + (vibration * 0.35)
                                + (loadPercentage * 0.015)
                                + (operatingHours / 10000)
                                + (machineAge * 0.04);

                double failureProbability =
                        1.0 / (1.0 + Math.exp(-riskScore + 3.8));

                int failure =
                        random.nextDouble() < failureProbability ? 1 : 0;

                String message =
                        machineId + "," +
                                LocalDateTime.now() + "," +
                                temperature + "," +
                                vibration + "," +
                                pressure + "," +
                                powerConsumption + "," +
                                operatingHours + "," +
                                loadPercentage + "," +
                                rotationSpeed + "," +
                                maintenanceCount + "," +
                                machineAge + "," +
                                failure;

                ProducerRecord<String, String> record =
                        new ProducerRecord<>(
                                "machine-data",
                                machineId,
                                message
                        );

                producer.send(
                        record,
                        (metadata, exception) -> {

                            if (exception == null) {

                                System.out.println(
                                        "Sent: " + message
                                );

                            } else {

                                System.out.println(
                                        "Error: "
                                                + exception.getMessage()
                                );
                            }
                        }
                );

                producer.flush();

                Thread.sleep(2000);
            }

        } catch (InterruptedException e) {

            Thread.currentThread().interrupt();

        } finally {

            producer.close();

            System.out.println(
                    "SmartPulse Kafka Machine Producer stopped."
            );
        }
    }
}