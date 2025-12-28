# Induction Motor Health and Performance Monitoring System

## Overview
An IoT-based system designed to monitor the health and performance of an induction motor in real time. The project integrates hardware sensors with microcontrollers to detect abnormal conditions and provide visual and remote status updates.

## Key Features
- Real-time monitoring of motor temperature and vibration
- Arduino-based sensor data acquisition
- Raspberry Pi for data processing and interfacing
- LED display for local status indication
- Visual circuit diagrams and system flowchart

## Tech Stack
- Arduino Uno
- Raspberry Pi
- C (Arduino)
- Python
- IoT Sensors

## Folder Structure
- `arduino/` – Arduino code for sensor data collection
- `raspberry_pi/` – Python scripts for data processing and interface
- `circuit_diagram/` – Hardware setup, flowchart, and interface diagrams

## How It Works
Sensors collect motor parameters which are processed by the Arduino and Raspberry Pi. The system displays motor health locally and can be extended for remote monitoring.

## Future Improvements
- Cloud-based data logging
- Predictive maintenance using machine learning
- Web or mobile dashboard
