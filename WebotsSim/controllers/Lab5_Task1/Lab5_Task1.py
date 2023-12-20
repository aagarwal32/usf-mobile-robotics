# WebotsSim/controllers/Lab5_Task1/Lab5_Task1.py
# Changes Working Directory to be at the root of FAIRIS-Lite
import math
import numpy as np
# import matplotlib.pyplot as plt
import os
os.chdir("../..")

# Import MyRobot Class
from WebotsSim.libraries.MyRobot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = 'worlds/mazes/Labs/Lab5/Lab5_Maze1.xml'
robot.load_environment(maze_file)
# Move robot to a random staring position listed in maze file
robot.move_to_start()

# Get the robot's starting position after moving the robot to a random start
starting_x = robot.starting_position.x
starting_y = robot.starting_position.y
starting_theta = robot.starting_position.theta

unknown_val = 0.5
empty_val = 0.3
occupied_val = 0.6

c = 0.33    # block size

# Initialize maze_map as a 2D array
maze_map = np.full((12, 12), ' ')

maze_cells = [(0, 0), (0, 1), (0, 2), (0, 3),
              (1, 0), (1, 1), (1, 2), (1, 3),
              (2, 0), (2, 1), (2, 2), (2, 3),
              (3, 0), (3, 1), (3, 2), (3, 3)]

# 4d array of 3x3 sub cells for each 4x4 cells that contains default 0.5 value
log_odds = np.full((4, 4, 3, 3), np.log(unknown_val / (1 - unknown_val)))


def determine_locate_cells_index(x, y):
    # find row
    if 1 <= y <= 2:
        row = 0
    elif 0 <= y < 1:
        row = 1
    elif -1 <= y < 0:
        row = 2
    elif -2 <= y < -1:
        row = 3
    else:
        row = None

    # find column
    if -2 <= x <= -1:
        column = 0
    elif -1 < x <= 0:
        column = 1
    elif 0 < x <= 1:
        column = 2
    elif 1 < x <= 2:
        column = 3
    else:
        column = None

    current_idx = maze_cells.index((row, column))

    return current_idx


def stop_mapping():
    # Count the number of occurrences of the specific value
    count = np.count_nonzero(log_odds == np.log(unknown_val / (1 - unknown_val)))
    # Calculate the percentage
    percentage = (count / log_odds.size) * 100
    print(f"Percentage left to cover is {round(percentage, 2)}%")
    # if unknown cells are less than or equal to 10% return true
    if percentage <= 10:
        return 1


def wall_mapping(index):
    # Iterate through each element
    for i in range(log_odds.shape[0]):
        for j in range(log_odds.shape[1]):
            for k in range(log_odds.shape[2]):
                for l in range(log_odds.shape[3]):
                    if log_odds[i, j, 1, 1]:
                        # Gets an index from log_odds
                        index_4d = (i, j, 1, 1)  # center of sub cell (robot location)

                        # Map the index to maze_map
                        index_2d = (index_4d[0] * 3 + index_4d[2], index_4d[1] * 3 + index_4d[3])

                        if (i, j) == maze_cells[index]:
                            if robot.get_compass_reading() in range(85, 95):
                                maze_map[index_2d] = '\u2191'   # ^
                            elif robot.get_compass_reading() in range(265, 275):
                                maze_map[index_2d] = '\u2193'   # v
                            elif robot.get_compass_reading() in range(175, 185):
                                maze_map[index_2d] = '\u2190'   # <
                            else:
                                maze_map[index_2d] = '\u2192'  # >

                    prior = np.log(unknown_val / (1 - unknown_val))

                    wall_val = round(prior + log_inv_sensor_model(occupied_val, unknown_val), 2)

                    if log_odds[i, j, k, l] == wall_val:
                        # Gets an index from log_odds
                        index_4d = (i, j, k, l)  # sub cell index

                        # Map the 4d array index to 2d maze_map
                        index_2d = (index_4d[0] * 3 + index_4d[2], index_4d[1] * 3 + index_4d[3])

                        maze_map[index_2d] = 'W'

    print("+ -- -- -- - +")
    for row in maze_map:
        # Print left and right border
        print('|' + ''.join(row) + '|')
    print("+ -- -- -- - +")


# Occupancy Grid - Python Code
# Inverse sensor model in log-odds form (natural logarithm)
def log_inv_sensor_model(z, c_size):
    if c_size < z:
        # The sensor detects a wall for this cell
        return np.log(occupied_val / (1 - occupied_val))
    # The sensor detects free space for this cell
    return np.log(empty_val / (1 - empty_val))


def update_log_odds(z_val, cur_idx):
    prior = np.log(unknown_val / (1 - unknown_val))

    cell = maze_cells[cur_idx]
    x, y = cell
    sub_cells = log_odds[x, y]

    # Log-odds update formula for the cells
    # sub cell under robot is empty
    sub_cells[1, 1] = round(sub_cells[1, 1] - prior + log_inv_sensor_model(empty_val, c), 2)

    # update North sub cells
    sub_cells[0, 1] = round(sub_cells[0, 1] - prior + log_inv_sensor_model(z_val[0], c), 2)
    if z_val[0] == occupied_val:
        sub_cells[0, 0], sub_cells[0, 2] = sub_cells[0, 1], sub_cells[0, 1]
    # Apply the inverse transformation from log-odds to probability
    # m = 1 - 1. / (1 + np.exp(sub_cells[i, j]))

    # update East sub cells
    sub_cells[1, 2] = round(sub_cells[1, 2] - prior + log_inv_sensor_model(z_val[1], c), 2)
    if z_val[1] == occupied_val:
        sub_cells[0, 2], sub_cells[2, 2] = sub_cells[1, 2], sub_cells[1, 2]

    # update South sub cells
    sub_cells[2, 1] = round(sub_cells[2, 1] - prior + log_inv_sensor_model(z_val[2], c), 2)
    if z_val[2] == occupied_val:
        sub_cells[2, 0], sub_cells[2, 2] = sub_cells[2, 1], sub_cells[2, 1]

    # update West sub cells
    sub_cells[1, 0] = round(sub_cells[1, 0] - prior + log_inv_sensor_model(z_val[3], c), 2)
    if z_val[3] == occupied_val:
        sub_cells[0, 0], sub_cells[2, 0] = sub_cells[1, 0], sub_cells[1, 0]

# Plot the resulting estimate
# plt.plot(c, m)
# plt.xlabel("x-position [cm]")
# plt.ylabel("occupancy p(x)")
# plt.savefig("graph.pdf")
# plt.show()


def sensor(idx):
    z_left = empty_val if robot.lidar.getRangeImage()[200] > 0.7 else occupied_val
    z_front = empty_val if robot.lidar.getRangeImage()[400] > 0.7 else occupied_val
    z_right = empty_val if robot.lidar.getRangeImage()[600] > 0.7 else occupied_val
    z_back = empty_val if robot.lidar.getRangeImage()[0] > 0.7 else occupied_val

    # robot facing North
    if robot.get_compass_reading() in range(85, 95):
        z_sensor = [z_front, z_right, z_back, z_left]
        update_log_odds(z_sensor, idx)

    # robot facing South
    elif robot.get_compass_reading() in range(265, 275):
        z_sensor = [z_back, z_left, z_front, z_right]
        update_log_odds(z_sensor, idx)

    # robot facing West
    elif robot.get_compass_reading() in range(175, 185):
        z_sensor = [z_right, z_back, z_left, z_front]
        update_log_odds(z_sensor, idx)

    # robot facing East
    else:
        z_sensor = [z_left, z_front, z_right, z_back]
        update_log_odds(z_sensor, idx)


def update_cells(current_idx):

    if robot.get_compass_reading() in range(85, 95):
        next_cell = current_idx - 4
    elif robot.get_compass_reading() in range(175, 185):
        next_cell = current_idx - 1
    elif robot.get_compass_reading() in range(265, 275):
        next_cell = current_idx + 4
    else:
        next_cell = current_idx + 1

    current_idx = next_cell

    return current_idx


if __name__ == "__main__":

    # get direction of robot and next cell
    current_index = determine_locate_cells_index(starting_x, starting_y)

    while robot.experiment_supervisor.step(robot.timestep) != -1:

        sensor(current_index)

        # prints occupancy grid cell values
        # each cell's sub cells are printed
        cell_n = maze_cells[current_index]
        x_pos, y_pos = cell_n
        print("Occupancy Grid Cell:", current_index, "theta:", robot.get_compass_reading())
        print(log_odds[x_pos, y_pos])

        # prints the map of the maze in real time using occupancy grid values
        wall_mapping(current_index)

        # this block of code moves the robot through the maze
        if robot.get_lidar_range_image()[400] > 1.0:
            robot.move_distance(1.0, 10.0)
        elif robot.get_lidar_range_image()[200] > 1.0:
            robot.rotate_bot_degrees(math.pi + math.pi/1.5, 3)
            robot.fix_direction()
            robot.move_distance(1.0, 10.0)
        elif robot.get_lidar_range_image()[600] > 1.0:
            robot.rotate_bot_degrees(math.pi/1.5, 3)
            robot.fix_direction()
            robot.move_distance(1.0, 10.0)
        else:
            robot.rotate_bot_degrees(math.pi + math.pi/2, 3)
            robot.fix_direction()
            robot.move_distance(1.0, 10.0)

        current_index = update_cells(current_index)

        # stop robot and end task once at least 90% of sub cells are assigned new values
        if stop_mapping():
            break
    # stop robot
    robot.stop()
