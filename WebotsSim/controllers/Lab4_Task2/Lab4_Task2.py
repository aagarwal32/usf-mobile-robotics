# WebotsSim/controllers/Lab4_Task2/Lab4_Task2.py
# Changes Working Directory to be at the root of FAIRIS-Lite
import math
import os
os.chdir("../..")

# Import MyRobot Class
from WebotsSim.libraries.MyRobot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = 'worlds/mazes/Labs/Lab4/Lab4_Task2_1.xml'
robot.load_environment(maze_file)
# Move robot to a random staring position listed in maze file
robot.move_to_start()

# Get the robot's starting position after moving the robot to a random start
starting_x = robot.starting_position.x
starting_y = robot.starting_position.y
starting_theta = robot.starting_position.theta


# This code provides a very simple implementation of the maze and how the maze's walls can be printed visually.
# You may use this as a starting point or develop your own maze implementation.

class Cell:
    def __init__(self, west, north, east, south, visited=False):
        # There are 4 walls per cell
        # Wall values can be 'W', 'O', or '?' (wall, open, or unknown)
        self.west = west
        self.north = north
        self.east = east
        self.south = south

        # Store whether the cell has been visited before
        self.visited = visited


# Helper function that verifies all the walls of the maze
def detectMazeInconsistencies(maze):
    # Check horizontal walls
    for i in range(3):
        for j in range(4):
            pos1 = i * 4 + j
            pos2 = i * 4 + j + 4
            hWall1 = maze[pos1].south
            hWall2 = maze[pos2].north
            assert hWall1 == hWall2, " Cell " + str(pos1) + "'s south wall doesn't equal cell " + str(
                pos2) + "'s north wall! ('" + str(hWall1) + "' != '" + str(hWall2) + "')"

    # Check vertical walls
    for i in range(4):
        for j in range(3):
            pos1 = i * 4 + j
            pos2 = i * 4 + j + 1
            vWall1 = maze[pos1].east
            vWall2 = maze[pos2].west
            assert vWall1 == vWall2, " Cell " + str(pos1) + "'s east wall doesn't equal cell " + str(
                pos2) + "'s west wall! ('" + str(vWall1) + "' != '" + str(vWall2) + "')"


# You don't have to understand how this function works
def printMaze(maze, hRes=4, vRes=2):
    assert hRes > 0, "Invalid horizontal resolution"
    assert vRes > 0, "Invalid vertical resolution"

    # Get the dimensions of the maze drawing
    hChars = 4 * (hRes + 1) + 2
    vChars = 4 * (vRes + 1) + 1

    # Store drawing into a list
    output = [" "] * (hChars * vChars - 1)

    # Draw top border
    for i in range(1, hChars - 2):
        output[i] = "_"

    # Draw bottom border
    for i in range(hChars * (vChars - 1) + 1, hChars * (vChars - 1) + hChars - 2):
        output[i] = "¯"

    # Draw left border
    for i in range(hChars, hChars * (vChars - 1), hChars):
        output[i] = "|"

    # Draw right border
    for i in range(2 * hChars - 2, hChars * (vChars - 1), hChars):
        output[i] = "|"

    # Draw newline characters
    for i in range(hChars - 1, hChars * vChars - 1, hChars):
        output[i] = "\n"

    # Draw dots inside maze
    for i in range((vRes + 1) * hChars, hChars * (vChars - 1), (vRes + 1) * hChars):
        for j in range(hRes + 1, hChars - 2, hRes + 1):
            output[i + j] = "·"

    # Draw question marks if cell is unvisited
    for i in range(4):
        for j in range(4):
            cellNum = i * 4 + j
            if maze[cellNum].visited:
                continue
            origin = (i * hChars * (vRes + 1) + hChars + 1) + (j * (hRes + 1))
            for k in range(vRes):
                for l in range(hRes):
                    output[origin + k * hChars + l] = "?"

    # Draw horizontal walls
    for i in range(3):
        for j in range(4):
            cellNum = i * 4 + j
            origin = ((i + 1) * hChars * (vRes + 1) + 1) + (j * (hRes + 1))
            hWall = maze[cellNum].south
            for k in range(hRes):
                output[origin + k] = "-" if hWall == 'W' else " " if hWall == 'O' else "?"

    # Draw vertical walls
    for i in range(4):
        for j in range(3):
            cellNum = i * 4 + j
            origin = hChars + (hRes + 1) * (j + 1) + i * hChars * (vRes + 1)
            vWall = maze[cellNum].east
            for k in range(vRes):
                output[origin + k * hChars] = "|" if vWall == 'W' else " " if vWall == 'O' else "?"

    # Print drawing
    print(''.join(output))


# Initialize the maze with a set of walls and visited cells
# The bottom right cell is marked as unvisited and with unknown walls
# W N E S

MAP_IDX = 1

if MAP_IDX == 1:
    maze = [
        Cell('W', 'W', 'O', 'O', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False),
        Cell('O', 'W', 'W', 'O', False),
        Cell('W', 'O', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'W', 'W', 'O', False),
        Cell('W', 'O', 'W', 'O', False),
        Cell('W', 'W', 'O', 'O', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'O', 'W', 'W', False),
        Cell('W', 'O', 'W', 'O', False),
        Cell('W', 'O', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False),
        Cell('O', 'O', 'W', 'W', False)
    ]
elif MAP_IDX == 2:
    maze = [
        Cell('W', 'W', 'O', 'O', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False),
        Cell('O', 'W', 'W', 'O', False),
        Cell('W', 'O', 'O', 'W', False), Cell('O', 'W', 'O', 'O', False), Cell('O', 'W', 'W', 'O', False),
        Cell('W', 'O', 'W', 'O', False),
        Cell('W', 'W', 'W', 'O', False), Cell('W', 'O', 'O', 'W', False), Cell('O', 'O', 'W', 'W', False),
        Cell('W', 'O', 'W', 'O', False),
        Cell('W', 'O', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False),
        Cell('O', 'O', 'W', 'W', False)
    ]

else:
    maze = [
        Cell('W', 'W', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'W', 'O', 'O', False),
        Cell('O', 'W', 'W', 'O', False),
        Cell('W', 'W', 'O', 'O', False), Cell('O', 'W', 'W', 'O', False), Cell('W', 'O', 'W', 'O', False),
        Cell('W', 'O', 'W', 'O', False),
        Cell('W', 'O', 'W', 'O', False), Cell('W', 'O', 'O', 'W', False), Cell('O', 'O', 'W', 'W', False),
        Cell('W', 'O', 'W', 'O', False),
        Cell('W', 'O', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False), Cell('O', 'W', 'O', 'W', False),
        Cell('O', 'O', 'W', 'W', False)
    ]

# How to modify a cell
# maze[0].east = 'W'
# maze[0].visited = False


maze_cells = [(0, 0), (0, 1), (0, 2), (0, 3),
              (1, 0), (1, 1), (1, 2), (1, 3),
              (2, 0), (2, 1), (2, 2), (2, 3),
              (3, 0), (3, 1), (3, 2), (3, 3)]


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


def prob(S, Z):

    pb = 0

    if S == 0:
        if Z == 0:
            pb = 0.7
        else:
            pb = 0.3

    else:
        if Z == 1:
            pb = 0.9
        else:
            pb = 0.1

    return pb


def find_pb(current_idx):

    # Actual values (Z)
    z_left = 0 if robot.lidar.getRangeImage()[200] > 0.7 else 1
    z_front = 0 if robot.lidar.getRangeImage()[400] > 0.7 else 1
    z_right = 0 if robot.lidar.getRangeImage()[600] > 0.7 else 1
    z_back = 0 if robot.lidar.getRangeImage()[0] > 0.7 else 1

    print("Current cell: ", current_idx, "Theta:", robot.get_compass_reading())

    # set cell to visited
    maze[current_idx].visited = True

    if robot.get_compass_reading() in range(85, 95):
        next_cell = current_idx - 4
    elif robot.get_compass_reading() in range(175, 185):
        next_cell = current_idx - 1
    elif robot.get_compass_reading() in range(265, 275):
        next_cell = current_idx + 4
    else:
        next_cell = current_idx + 1

    print("Next cell: ", next_cell)
    current_idx = next_cell

    # Given values (S) for next cell
    next_west = 1 if maze[next_cell].west == "W" else 0
    next_north = 1 if maze[next_cell].north == "W" else 0
    next_east = 1 if maze[next_cell].east == "W" else 0
    next_south = 1 if maze[next_cell].south == "W" else 0

    # Given values (S) for current cell
    cur_west = 1 if maze[current_idx].west == "W" else 0
    cur_north = 1 if maze[current_idx].north == "W" else 0
    cur_east = 1 if maze[current_idx].east == "W" else 0
    cur_south = 1 if maze[current_idx].south == "W" else 0

    move_pb = 0.8 * prob(next_west, z_left) * prob(next_north, z_front) * prob(next_east, z_right) * prob(next_south, z_back)
    stay_pb = 0.2 * prob(cur_west, z_left) * prob(cur_north, z_front) * prob(cur_east, z_right) * prob(cur_south, z_back)

    sum_pb = move_pb + stay_pb

    normalized_move_pb = move_pb / sum_pb
    normalized_stay_pb = stay_pb / sum_pb

    print("Move Probability (Normalized): ", round(normalized_move_pb, 5))
    print("Stay Probability (Normalized): ", round(normalized_stay_pb, 5))

    return current_idx


if __name__ == "__main__":

    # get direction of robot and next cell
    current_index = determine_locate_cells_index(starting_x, starting_y)

    while robot.experiment_supervisor.step(robot.timestep) != -1:
        # detectMazeInconsistencies(maze)
        printMaze(maze)

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

        print("------------------------------------")
        current_index = find_pb(current_index)
