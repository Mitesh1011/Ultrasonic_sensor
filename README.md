# Autonomous Obstacle Avoidance Robot

## Overview
This project is an autonomous mobile robot developed using a Raspberry Pi 4, ultrasonic sensors, and DC motors. The robot is capable of detecting obstacles in real time and navigating around them without human intervention.

The system uses three ultrasonic sensors (left, center, and right) to measure distances and make movement decisions. PWM motor control is implemented for smooth navigation and turning.

---

## Features
- Autonomous obstacle detection
- Real-time obstacle avoidance
- Three ultrasonic sensors for directional awareness
- Forward, backward, left, and right movement control
- PWM motor speed control
- Collision avoidance algorithm
- Raspberry Pi GPIO integration

---

## Hardware Components
- Raspberry Pi 4
- HC-SR04 Ultrasonic Sensors ×3
- DC Motors ×2
- Motor Driver / Motor Shield
- Robot Chassis
- Battery Pack
- Jumper Wires

---

## Software Requirements
- Python 3
- RPi.GPIO Library

Install required library:

```bash
pip install RPi.GPIO
```

---

## GPIO Pin Configuration

### Motor Pins

| Function | GPIO Pin |
|----------|----------|
| Motor A Forward | 17 |
| Motor A Backward | 18 |
| Motor B Forward | 22 |
| Motor B Backward | 23 |

### Ultrasonic Sensor Pins

| Sensor | Trigger Pin | Echo Pin |
|--------|-------------|-----------|
| Center | 24 | 25 |
| Left | 5 | 6 |
| Right | 13 | 19 |

---

## How It Works
1. The robot continuously measures distances using three ultrasonic sensors.
2. If no obstacle is detected ahead, the robot moves forward.
3. If an obstacle is detected:
   - The robot compares left and right distances.
   - It turns toward the direction with more free space.
4. If all directions are blocked:
   - The robot reverses briefly.
   - Then performs a turn to find a new path.

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/Mitesh1011/Ultrasonic_sensor.git
```

Navigate to the project folder:

```bash
cd Ultrasonic_sensor
```

Run the Python file:

```bash
python3 obstacle_avoidance.py
```

---

## Project Structure

```text
project/
│
├── obstacle_avoidance.py
├── README.md
```

---

## Future Improvements
- Camera-based object detection
- SLAM navigation
- Path planning algorithms
- ROS integration
- Web/mobile robot control
- AI-based obstacle classification

---

## Author
Mitesh Salvi

MEng(Hons) Intelligent Automation and Robotics  
Edge Hill University

---

## License
This project is open-source and available for educational purposes.
