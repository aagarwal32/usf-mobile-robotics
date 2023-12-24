# USF Control of Mobile Robot Labs (Fall 2023)

This repository is an extension of the project framework, [FAIRIS-Lite](https://github.com/biorobaw/FAIRIS-Lite), enabling users to implement navigational control logic for robots in the Webots simulation. It includes the necessary Python controller files that I have created for the various lab tasks required by this course.

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

Here is the corresponding Python controller for lab 1: [Lab 1 Controller](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab1_Task1/Lab1_Task1.py)

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

The second part to this lab required the implementation of wall-following in combination with proportional gain control. Figure 3 below visualizes how wall-following works. Proportional gain slows down the robot as it gets closer to the walls and the wall-following algorithm tries to steer the robot back to the center line - essentially avoiding the walls.
<p align="center">
<img width="1397" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/d763d3e0-54bb-48fc-bd0e-60a0e0495df4">
</p>
<p align="center">
<em>Figure 3: Visualization of the wall-following algorithm</em>
</p>

A more in-depth overview of Lab 2 can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task2/lab2-PID-Wall-Following.pdf).

Here are the corresponding Python controllers for Lab 2: [Task 1](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task1/Lab2_Task1.py), [Task 2](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task2/Lab2_Task2.py).

The video below shows Lab 2 Task 2 in action with the robot navigating using proportional gain and wall-following:

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/444c6f39-51a0-4ab3-a5e7-7b76f5db982c

## Lab 3 - Bug0 Algorithm

### Objective
This lab implements the bug0 algorithm to navigate the robot to a specified goal. It utilizes the onboard camera to identify the goal and LiDAR scanner for wall-avoidance. If the camera detects the goal, it will perform straight line motion towards it. If blocked by an obstacle, it will perform wall-avoidance until the goal is visible again.

<p align="center">
<img width="424" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/1d2c4b84-5293-4b3b-9826-35698c4e3f65">
</p>
<p align="center">
<em>Figure 4: Visualization of the path followed by the robot using bug0</em>
</p>

In Figure 4, the blue shapes represent obstacles and the orange line is the path it would follow. From <em>q-start</em> to <em>q-H1</em> the robot detects the goal. The goal in this case would be a tall structure visible from any distance. At <em>q-H1</em>, which is also known as a "Hit-point", the onboard cameras of the robot lose sight of the goal as it is blocked by an obstacle. In this situation, it will perform obstacle avoidance until the goal is visible again. At <em>q-L1</em>, the "Leave-point", the robot's cameras detect the goal and initiate straight line motion to <em>q-goal</em>.

The following stages describe the bug0 algorithm:
<ol>
  <li>Head towards the goal (if not blocked by an obstacle).</li>
  <li>If obstacle is encountered, <strong>ALWAYS</strong> turn left or <strong>ALWAYS</strong> turn right.</li>
  <li>Follow obstacle until robot can perform straight line motion to goal at leave point.</li>
  <li>Repeat above stages until goal is reached.</li>
</ol>

A more in-depth overview explaining the programming and calculations for lab 3 can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab3_Task2/lab3-bug0-algorithm.pdf).

The Python controllers for both tasks part of lab 3: [Task 1](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab3_Task1/Lab3_Task1.py), [Task 2](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab3_Task2/Lab3_Task2.py).

The video below shows the lab 3 task 2 controller in action. The robot follows the bug0 algorithm - set to take right turns when met with an obstacle:

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/8cf7f384-cacf-4481-bade-6b9ef319369a
