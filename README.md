# USF Control of Mobile Robot Labs (Fall 2023)

This repository is an extension to the project framework, [FAIRIS-Lite](https://github.com/biorobaw/FAIRIS-Lite). It contains the necessary python controller files which I have created for the different lab tasks required by this course.

The controller files are used to simulate robot motion and sensor readings in the Webots development environment. The free, open source Webots simulator can be found [here](https://cyberbotics.com/).

The controller files are the main deliverables for each lab and can be found in ```WebotsSim/controllers```. 

Each Lab will be explained in more detail in the following sections:

## Lab 1 - Kinematics

### Objective
The objective for this lab is to use kinematics to move a 4-wheeled differential drive robot through a set of pre-defined waypoints. This is done using the Webots simulator that runs python code as instructions for the robot to follow.

The waypoints through the maze are displayed as follows:

<p align="center">
<img width="500" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/d749cde9-b0f8-4e77-a773-e434fe9f3f97">
</p>
<p align="center">
<em>Figure 1: Maze file with predefined waypoints the robot must navigate through</em>
</p>

To accomplish this task, required the use of several functions that make the robot perform straight-line, curved-line, and rotation motions. 
A full report with more information and calculations for this lab can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab1_Task1/lab1-kinematics.pdf).

Here is the corresponding python controller for lab 1: [Lab 1 Controller](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab1_Task1/Lab1_Task1.py)

And this is a video of it in action!

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/102984dd-1ef4-4ccf-a360-523d0c86b0dd

## Lab 2 - PID and Wall Following

### Objective
This lab requires the use of proportional gain to control the speed of the robot based on its distance from the wall. Additionally, using proportional gain and lidar scanners to detect, avoid, and follow walls.
