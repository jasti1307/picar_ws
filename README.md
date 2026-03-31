# PiCar ROS 2 Workspace (`picar_ws`)

This repository contains the ROS 2 Humble workspace for a Raspberry Pi-based robot. It includes custom drivers for motor control, sensor integration (Ultrasonic/Lidar), and safety features.

## 🛠 Project Structure
* **src/my_picar_driver**: Core ROS 2 package containing Python nodes.
    * `car_driver.py`: PWM/Motor control for movement.
    * `safety_node.py`: Emergency braking and collision avoidance.
    * `ultrasonic_node.py`: Distance sensing via HC-SR04.
    * `camera_driver.py`: OpenCV-based image streaming.
    * `battery_node.py`: Voltage monitoring.

## 🚀 Getting Started

### Prerequisites
* Ubuntu 22.04 (or compatible)
* ROS 2 Humble
* Python 3.10+
* `python3-pip` (for dependencies like `websockets` or `RPi.GPIO`)

### Installation & Build
1. Clone the repository:
   ```bash
   git clone git@github.com:jasti1307/picar_ws.git
   cd picar_ws
	```

2.  Build the workspace:
    
  
    ```
    colcon build --symlink-install
    
    ```
    
3.  Source the setup file:
    
    
    
    ```
    source install/setup.bash
 
    ```
    

## 🎮 Usage

### Run the Teleop (Manual Control)

Bash

```
ros2 run my_picar_driver car_driver

```

### Start Safety Features (AEB)

```
ros2 run my_picar_driver safety_node
```

