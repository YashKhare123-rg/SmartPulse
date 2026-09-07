package com.smartpulse.simulator;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Properties;

public class KafkaProducerTest {

    public static void main(String[] args) {

        MachineDataGenerator generator = new MachineDataGenerator();

        List<MachineRecord> records = generator.generateData();

        MachineRecord record = records.get(0);

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

        String message =
                record.getMachineId() + "," +
                        record.getTimestamp() + "," +
                        record.getTemperature() + "," +
                        record.getVibration() + "," +
                        record.getPressure() + "," +
                        record.getPowerConsumption() + "," +
                        record.getOperatingHours() + "," +
                        record.getLoadPercentage() + "," +
                        record.getRotationSpeed() + "," +
                        record.getMaintenanceCount() + "," +
                        record.getMachineAge() + "," +
                        record.getFailure();

        ProducerRecord<String, String> kafkaRecord =
                new ProducerRecord<>(
                        "machine-data",
                        record.getMachineId(),
                        message
                );

        producer.send(
                kafkaRecord,
                (metadata, exception) -> {

                    if (exception == null) {

                        System.out.println(
                                "Real MachineRecord sent successfully!"
                        );

                        System.out.println(
                                "Machine ID: " + record.getMachineId()
                        );

                        System.out.println(
                                "Topic: " + metadata.topic()
                        );

                        System.out.println(
                                "Partition: " + metadata.partition()
                        );

                        System.out.println(
                                "Offset: " + metadata.offset()
                        );

                        System.out.println(
                                "Data: " + message
                        );

                    } else {

                        System.out.println(
                                "Error sending message: "
                                        + exception.getMessage()
                        );
                    }
                }
        );

        producer.flush();
        producer.close();

        System.out.println("Producer stopped.");
    }
}