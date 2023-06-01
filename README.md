# SquirtleBot - TurtleBot Reconnaissance Mission
In this project, a simulation of a disaster environment was implemented using a TurtleBot3 hardware. The robot was used to survey the area by mapping its trajectory also the area and identify potential dangers and victims. The project demonstrated the efficiency of using a robot to map an area and identify hazards and injured people before sending human responders into the field. The performance of the mover_base and explore_lite packages were modified using ROS and Python in order to improve the robot's capabilities in terms of reliability and precision.

# Introduction and Motivation
The purpose the this project is to simulate a reconnaissance mission after a disaster
This could be a burned down building, hurricane, earthquake, etc.
To reduce the risk to first responders, robots would be deployed in dangerous environments to survey and report back
To model this scenario:
turtlebot -> mobile platform
apriltags -> victims
closed room with obstacles -> dangerous environment

# Turtlebot Types
There are 2 types of Turtlebots: 
1. Burger.
2. Waffle.
We are using turtlebot burger for our application for its better maneuverability, operation time and lightweightedness as compared to turtlebot waffle. 

#Turtlebot Specifications 
General Specifications :
Size : 138*178*192(mm)
Maximum translational velocity: 0.22 m/s
Maximum rotational velocity : 2.84 rad/s

Technical Specifications:
Raspberry pi 3 (Single board Computer)	
1024(1GB) RAM
64 bit Quad Core Arm Cortex - A53
Wifi : Dual band 2.4 & 5 GHz
Power Supply 5V.
OpenCR (Micro Controller Unit)
32 bit ARM Cortex -M7 with FPU
Power Supply 5v

Actuator (XL430 - W250)
Power supply 6.5-12V (11.1V recom).
No load Speed with recom power 57 rev/s.
Uses PID control Algorithm (Feedback : Position, Velocity, Load, Real Time tick, Trajectory, Temperature, Input Voltage, etc)
Laser Distance Sensor (360 LDS -01)
2D 360 Deg laser scanner.
Power Supply 5V.
Ambient light resistance <= 10,000 luminescence 

Camera - (Raspberry pi cam v2.1)
Sensor IMX219 - 8MP
Horizontal FoV - 62.2Deg.
Vertical FoV - 48.8 Deg.
IMU 
3-Axis Gyroscope
3-Axis Accelerometer
Battery 
Lithium polymer 11.1V 1800mAh / 19.98Wh 5C

#Turtlebot Initialization
Prior to starting to solve the problem:
OS installation
Network configuration
Camera and Lidar nodes
Camera Calibration
Starting point for our solution
Explore_lite
Apriltag_detection

#Camera Calibration
Found intrinsics of the camera using Kalibr
Central Pixel, focal length
Distortion coefficients
Low reprojection error
Less than a pixel in both axes

![Screenshot 2023-06-01 144952](https://github.com/prathimaAnand/SquirtleBot---TurtleBot-Reconnaissance-Mission/assets/65678711/12e8de98-e063-4c07-8ed1-9ef17273483c)



