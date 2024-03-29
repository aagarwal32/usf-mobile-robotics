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
<img width="500" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/c40d3368-bbab-480d-86bf-2c97a84c3a6d">
</p>
<p align="center">
<em>Figure 1: Maze file with predefined waypoints the robot must navigate through</em>
</p>

To accomplish this task, required the use of several functions that make the robot perform straight-line, curved-line, and rotation motions. 
A full report with more information and calculations for this lab can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab1_Task1/lab1-kinematics.pdf).

Here is the corresponding Python controller for lab 1: [Lab 1 Controller](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab1_Task1/Lab1_Task1.py)

The video below shows Lab 1 in action as the robot follows the waypoints described in Figure 1.



https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/9b0d3649-8d3a-42cb-97b0-0fdb20f54aa6



## Lab 2 - PID and Wall Following

### Objective
This lab requires the use of proportional gain to control the speed of the robot based on its distance from the wall. Additionally, using proportional gain and LiDAR scanners to detect, avoid, and follow walls.

<p align="center">
<img width="812" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/b35c84bf-5c8a-40d0-b106-b3220305135f">
</p>
<p align="center">
<em>Figure 2: A flowchart describing the process of proportional gain</em>
</p>

Proportional gain control works by first, finding the distance error, <em>e(t)</em>. This can be calculated by subtracting the current LiDAR distance sensor reading, <em>y(t)</em>, by the target distance, <em>r(t)</em>. Using the distance error, you can obtain the control signal, <em>u(t)</em>, which is the calculated velocity directly proportional to the error. This can be calculated by choosing a constant <em>Kp</em> value and multiplying it with the error. Passing this control signal into the saturation function allows the speed to stay within robot limits by testing the extremes.

The second part to this lab required the implementation of wall-following in combination with proportional gain control. Figure 3 below visualizes how wall-following works. Proportional gain slows down the robot as it gets closer to the walls and the wall-following algorithm tries to steer the robot back to the center line - essentially avoiding the walls.
<p align="center">
<img width="1400" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/7b68ea8d-5d09-4b83-ba4f-a588251c0cc5">
</p>
<p align="center">
<em>Figure 3: Visualization of the wall-following algorithm</em>
</p>

A more in-depth overview of Lab 2 can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task2/lab2-PID-Wall-Following.pdf).

Here are the corresponding Python controllers for Lab 2: [Task 1](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task1/Lab2_Task1.py), [Task 2](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab2_Task2/Lab2_Task2.py).

The video below shows Lab 2 Task 2 in action with the robot navigating using proportional gain and wall-following:

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/cf51a1c7-36cd-4d70-8b3f-fa289027488d

## Lab 3 - Bug0 Algorithm

### Objective
This lab implements bug 0, a search algorithm that navigates the robot to a specified goal. It utilizes the onboard camera to identify the goal and LiDAR scanner for wall-avoidance. If the camera detects the goal, it will perform straight line motion towards it. If blocked by an obstacle, it will perform wall-avoidance until the goal is visible again.

<p align="center">
<img width="420" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/15af045c-e6e9-4b7a-995e-d2c35c883a1d">
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

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/c5367bcd-e2db-4627-997d-9435438171a4

## Lab 4 - Localization

### Objective
The objective for this lab is to perform trilateration calculations to estimate coordinates and cell location of the robot. The robot uses its onboard cameras and sensors to scan its surroundings, compute its pose, and navigate the maze while updating information for each new cell. The robot uses these localization methods to mark cells as visited and find unvisited cells. Additionally, it performs wall-based localization using probability and a sensor model.

As seen by Figure 5 below, trilateration can mathematically calculate the robot's x and y position. The center x, y coordinates of each circle and their distance from the robot (radius) are passed as inputs into the trilateration function. The position of the robot is computed at the intersection of the three circles:

<p align="center">
<img width="460" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/f7938292-1688-4ace-a0e0-ff00129baba1">
</p>
<p align="center">
<em>Figure 5: Visual representation of how trilateration works to find robot position</em>
</p>

Upon finding the current cell the robot is in, if the cell is <em>empty</em>, it marks it as <em>visited</em>. The goal of this lab is to mark all cells as <em>visited</em>. In order to do this more efficiently, if the current cell is already <em>visited</em>, the program finds the next <em>empty</em> cell in the map. Figure 6 below shows the algorithm to move the robot to the next empty cell:

<p align="center">
<img alt="image" width="800" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/3569bcfd-3083-45ae-a4d5-67d0a12934a8">
</p>
<p align="center">
<em>Figure 6: Visual representation of how the robot finds and moves to the next empty cell</em>
</p>

As seen by Figure 6, the robot is currently at cell 9. Before the robot moves, the program finds the next <em>empty</em> cell by iterating through the array of cells starting at index 0. The <em>target</em> is locked to cell 6 as it is the next empty cell. The robot compares its position to the <em>target</em> and takes a step-by-step approach to navigate to cell 6:

<ol>
  <li>The target row < current row</li>
  <li>Robot rotates to heading 90 deg from east and moves one cell (current - 4 = next)</li>
  <li>target row == current row and target cell > current cell</li>
  <li>Robot rotates to heading 0 deg from east and moves one cell (current + 1 = next)</li>
  <li>target cell == current cell</li>
  <li>mark current cell as <em>visited</em></li>
</ol>

Here is the Python controller for this task: [Task 1](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab4_Task1/Lab4_Task1.py).

A video of the robot performing trilateration calculations to determine pose and mark all cells in the map as visited is shown below:

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/4c0e7a3b-1cda-46ba-8b15-8677f8d785d6

The second part of this lab involves using Bayes theorem to determine <em>move</em> and <em>stay</em> probabilities for the robot. Using a given sensor model, the robot compares its calculated sensor readings to the actual environment. The sensor model is provided in Figure 7 below:

<p align="center">
<img width="800" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/47b6d44b-dd59-4aba-8dcf-8c8ef65a5c05">
</p>
<p align="center">
<em>Figure 7: Motion and sensor model for probability calculations</em>
</p>

Based on the motion model from Figure 7, 0.8 represents the probability of a forward <em>move</em> motion and 0.2 if the robot ended up to <em>stay</em> in place. In the same figure, the sensor model determines the probability of a wall being present at the current LiDAR reading. In the sensor model, <em>s</em> is the given value and <em>z</em> is the calculated value. 0 means "no wall" and 1 means "wall". Using this information, the robot can calculate <em>move</em> and <em>stay</em> probabilities while taking into account the current and next cell configurations.

A more in-depth overview for both lab 4 task 1 and task 2 can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab4_Task2/lab4-localization.pdf).

Here is the Python controller for this task: [Task 2](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab4_Task2/Lab4_Task2.py).

A video of the robot analyzing wall-configurations and calculating move and stay probabilities is shown below:

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/2761d38d-909c-441c-9286-8c7a72d65893

## Lab 5 - Mapping

### Objective
The objective for this lab is to create an occupancy grid that is used to generate a map based off the robot's surroundings. It uses its onboard LiDAR scanner to detect free and occupied spaces and updates the map accordingly.

To create the occupancy grid, the controller utilizes NumPy's 4D array to create a matrix of matrices. Each cell on the map contains sub cells that hold information on whether that space is <em>empty</em> or <em>occupied</em>. For this lab, each cell contains 3x3 matrix of sub cells. Figure 8 below visualizes this: 

<p align="center">
<img width="420" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/f1c069e9-9dd6-4fc9-a47a-c8fa36097a71">
</p>
<p align="center">
<em>Figure 8: A map consisting of 4x4 cells - each cell consisting of 3x3 sub cells</em>
</p>

The information that each sub cell holds is in the form of log odds. The <em>occupied</em> value is assigned 0.6 and the <em>empty</em> value, 0.3 (these values are adjustable). The calculated log odds with values determined by the LiDAR scanner readings are then updated on the occupancy grid map. An example of this is provided by Figure 9 below:

<p align="center">
<img width="420" alt="image" src="https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/25d64517-f4b8-4d26-898d-240c1c8dd481">
</p>
<p align="center">
<em>Figure 9: The robot's current cell occupancy values</em>
</p>

As seen by Figure 9, the cell the robot is currently in has occupancy values that match its surroundings. For instance, the log odd values, 0.41, match with the presence of the top and left walls - <em>occupied space</em>. The log odd values, -0.85, match with the presence of no walls right below the robot and to its immediate bottom and right surroundings - <em>empty space</em>. The occupancy grid is a key component in generating a map of the robot's surroundings. The final result is presented below in Figure 10:

<div align="center">
  
  Example Map 1                      |  Example Map 2
:-------------------------:|:-------------------------:
![maze-1](https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/f6ceeb95-75a0-4757-a7ee-ba5da927b862)   |  ![maze-2](https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/d3eda83d-2344-4833-9683-1f05ce30a6d1)

</div>

<p align="center">
<em>Figure 10: Generated maps based off the occupancy grid printed to the console</em>
</p>

The "W" in the generated map represents a wall, --> represents that the cell is visited and the direction the robot is facing, and any empty space means that there is no wall present. A more in-depth overview for this lab can be found in this [report](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab5_Task1/lab5-mapping.pdf).

Here is the Python controller for this task: [Task 1](https://github.com/aagarwal32/usf-mobile-robotics/blob/main/WebotsSim/controllers/Lab5_Task1/Lab5_Task1.py)

The video below shows the creation of the occupancy grid and map generation in real time as the robot navigates through the maze:

https://github.com/aagarwal32/usf-mobile-robotics/assets/152243328/21e2bc8d-4270-417e-828d-f7ca05d979a2

<!-- The End! -->
