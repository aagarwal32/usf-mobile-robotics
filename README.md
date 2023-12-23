# USF Control of Mobile Robot Labs (Fall 2023)

This repository is an extension to the project framework, [FAIRIS-Lite](https://github.com/biorobaw/FAIRIS-Lite). It contains the necessary python controller files which I have created for the different lab tasks required by this course.

The controller files are used to simulate robot motion and sensor readings in the Webots development environment. The free, open source Webots simulator can be found [here](https://cyberbotics.com/).

The controller files are the main deliverables for each lab and can be found in ```WebotsSim/controllers```. 

Each Lab will be explained in more detail in the following sections:

## Lab 1 - Kinematics

### Objective
The objective for this lab is to use kinematics to move a 4-wheeled differential drive robot through a set of pre-defined waypoints. This is done using the Webots simulator that runs python code as instructions for the robot to follow.

<p align="center">The waypoints through the maze are displayed as follows:</p>

<p align="center">
<img width="500" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/d749cde9-b0f8-4e77-a773-e434fe9f3f97">
</p>
<p align="center">
<em>Figure 1: Maze file with predefined waypoints the robot must navigate through</em>
</p>

To accomplish this task, required the use of several functions that make the robot perform straight-line, curved-line, and rotation motions. 
A full report with more information and calculations for this lab can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab1_Task1/lab1-kinematics.pdf).

Here is the corresponding python controller for lab 1: [Lab 1 Controller](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab1_Task1/Lab1_Task1.py)

The video below shows Lab 1 in action as the robot follows the waypoints described in Figure 1.

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/102984dd-1ef4-4ccf-a360-523d0c86b0dd

## Lab 2 - PID and Wall Following

### Objective
This lab requires the use of proportional gain to control the speed of the robot based on its distance from the wall. Additionally, using proportional gain and LiDAR scanners to detect, avoid, and follow walls.

<p align="center">
<img width="816" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/57250cf0-fe24-421a-8fdf-a6339477d8b6">
</p>
<p align="center">
<em>Figure 2: A flowchart describing the process of proportional gain</em>
</p>

Proportional gain control works by first, finding the distance error, <em>e(t)</em>. This can be calculated by subtracting the current LiDAR distance sensor reading, <em>y(t)</em>, by the target distance, <em>r(t)</em>. Using the distance error, you can obtain the control signal, <em>u(t)</em>, which is the calculated velocity directly proportional to the error. This can be calculated by choosing a constant <em>Kp</em> value and multiplying it with the error. Passing this control signal into the saturation function allows the speed to stay within robot limits by testing the extremes.

The second part to this lab required the implementation of wall-following in combination with proportional gain control. Figure 3 below visualizes how wall-following works. Proportional gain slows down the robot as it gets closer to the walls and the wall-following algorithm tries to steer the robot to the center line - essentially avoiding the walls.
<p align="center">
<img width="1397" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/d763d3e0-54bb-48fc-bd0e-60a0e0495df4">
</p>
<p align="center">
<em>Figure 3: Visualization of the wall-following algorithm</em>
</p>

A more in-depth overview of Lab 2 can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task2/lab2-PID-Wall-Following.pdf).

Here are the corresponding python controllers for Lab 2: [Task 1](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task1/Lab2_Task1.py), [Task 2](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task2/Lab2_Task2.py).

The video below shows Lab 2 in action with the robot navigating using proportional gain and wall-following:

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/444c6f39-51a0-4ab3-a5e7-7b76f5db982c

