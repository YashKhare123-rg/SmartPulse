package com.smartpulse.springboot.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

@RestController
public class MachineController {

    private static final String CSV_PATH =
            "E:/SmartPulse/data/processed/valid_machine_data.csv";

    @GetMapping("/api/machines")
    public List<MachineResponse> getMachines() throws IOException {

        Path path = Path.of(CSV_PATH);

        List<String> lines = Files.readAllLines(path);

        List<MachineResponse> machines = new ArrayList<>();

        for (int i = 1; i < lines.size(); i++) {

            String[] values = lines.get(i).split(",");

            if (values.length != 12) {
                continue;
            }

            MachineResponse machine = new MachineResponse(
                    values[0],
                    values[1],
                    Double.parseDouble(values[2]),
                    Double.parseDouble(values[3]),
                    Double.parseDouble(values[4]),
                    Double.parseDouble(values[5]),
                    Double.parseDouble(values[6]),
                    Double.parseDouble(values[7]),
                    Double.parseDouble(values[8]),
                    Integer.parseInt(values[9]),
                    Integer.parseInt(values[10]),
                    Integer.parseInt(values[11])
            );

            machines.add(machine);
        }

        return machines;
    }

    @GetMapping("/api/machines/{machineId}")
    public List<MachineResponse> getMachineById(
            @PathVariable String machineId) throws IOException {

        Path path = Path.of(CSV_PATH);

        List<String> lines = Files.readAllLines(path);

        List<MachineResponse> machines = new ArrayList<>();

        for (int i = 1; i < lines.size(); i++) {

            String[] values = lines.get(i).split(",");

            if (values.length != 12) {
                continue;
            }

            if (!values[0].equalsIgnoreCase(machineId)) {
                continue;
            }

            MachineResponse machine = new MachineResponse(
                    values[0],
                    values[1],
                    Double.parseDouble(values[2]),
                    Double.parseDouble(values[3]),
                    Double.parseDouble(values[4]),
                    Double.parseDouble(values[5]),
                    Double.parseDouble(values[6]),
                    Double.parseDouble(values[7]),
                    Double.parseDouble(values[8]),
                    Integer.parseInt(values[9]),
                    Integer.parseInt(values[10]),
                    Integer.parseInt(values[11])
            );

            machines.add(machine);
        }

        return machines;
    }

    public record MachineResponse(
            String machine_id,
            String timestamp,
            double temperature,
            double vibration,
            double pressure,
            double power_consumption,
            double operating_hours,
            double load_percentage,
            double rotation_speed,
            int maintenance_count,
            int machine_age,
            int failure
    ) {
    }
}