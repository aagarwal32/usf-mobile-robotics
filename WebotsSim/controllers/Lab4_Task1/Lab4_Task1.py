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
maze_file = 'worlds/mazes/Labs/Lab4/Lab4_Task1.xml'
robot.load_environment(maze_file)
# Move robot to a random staring position listed in maze file
robot.move_to_start()

cyl_radius = 0.314
total_distance = 0

visited_cells = ['.', '.', '.', '.',
                 '.', '.', '.', '.',
                 '.', '.', '.', '.',
                 '.', '.', '.', '.']

locate_cells = [(0, 0), (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 0), (2, 1), (2, 2), (2, 3),
                (3, 0), (3, 1), (3, 2), (3, 3)]


def locate_empty_cell(row, column):
    empty_cell_idx = None

    for idx, cell in enumerate(visited_cells):
        if cell == '.':
            empty_cell_idx = idx
            print("")
            print("NEXT EMPTY CELL::: ", empty_cell_idx)
            break

    current_index = locate_cells.index((row, column))

    while robot.experiment_supervisor.step(robot.timestep) != -1:
        print("Current Index... ", current_index)

        if empty_cell_idx < current_index:

            if robot.get_compass_reading() in range(0, 359):
                while robot.experiment_supervisor.step(robot.timestep) != -1:
                    if robot.get_compass_reading() not in range(85, 95):
                        robot.rotate_that_bot()
                    else:
                        break

            if empty_cell_idx in range(0, 4) and current_index not in range(0, 4):
                robot.move_distance(1.0, 5)
                current_index -= 4
            elif empty_cell_idx in range(4, 8) and current_index not in range(4, 8):
                robot.move_distance(1.0, 5)
                current_index -= 4
            elif empty_cell_idx in range(8, 12) and current_index not in range(8, 12):
                robot.move_distance(1.0, 5)
                current_index -= 4
            elif empty_cell_idx in range(12, 16) and current_index not in range(12, 16):
                robot.move_distance(1.0, 5)
                current_index -= 4
            else:
                robot.rotate_bot_degrees(-math.pi/4, 3)
                fix_direction()
                while robot.experiment_supervisor.step(robot.timestep) != -1:
                    if empty_cell_idx == current_index:
                        return
                    robot.move_distance(1.0, 5)
                    current_index -= 1

        elif empty_cell_idx > current_index:

            if robot.get_compass_reading() in range(0, 359):
                while robot.experiment_supervisor.step(robot.timestep) != -1:
                    if robot.get_compass_reading() not in range(265, 275):
                        robot.rotate_that_bot()
                    else:
                        break

            if empty_cell_idx in range(0, 4) and current_index not in range(0, 4):
                robot.move_distance(1.0, 5)
                current_index += 4
            elif empty_cell_idx in range(4, 8) and current_index not in range(4, 8):
                robot.move_distance(1.0, 5)
                current_index += 4
            elif empty_cell_idx in range(8, 12) and current_index not in range(8, 12):
                robot.move_distance(1.0, 5)
                current_index += 4
            elif empty_cell_idx in range(12, 16) and current_index not in range(12, 16):
                robot.move_distance(1.0, 5)
                current_index += 4
            else:
                robot.rotate_bot_degrees(-math.pi / 4, 3)
                fix_direction()
                while robot.experiment_supervisor.step(robot.timestep) != -1:
                    if empty_cell_idx == current_index:
                        return
                    robot.move_distance(1.0, 5)
                    current_index += 1

        else:
            return


def mark_visited_cells(idx, current_row, current_col):
    has_visited = 0

    if visited_cells[idx] == 'X':
        print("Cell already visited!")
        has_visited = 1

        print("-------FINDING EMPTY CELL---------")

        locate_empty_cell(current_row, current_col)

        pass

    else:
        visited_cells[idx] = 'X'
        display_cells = ''
        print("Visited Cells: ")

        for i in range(len(visited_cells)):
            if i % 4 == 0 and i != 0:
                display_cells += '\n'
            display_cells += visited_cells[i]

        print(display_cells)

    return has_visited


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

    return row, column


def trilateration(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    A = 2 * (-x1 + x2)
    B = 2 * (-y1 + y2)
    C = (r1 ** 2) - (r2 ** 2) - (x1 ** 2) + (x2 ** 2) - (y1 ** 2) + (y2 ** 2)

    D = 2 * (-x2 + x3)
    E = 2 * (-y2 + y3)
    F = (r2 ** 2) - (r3 ** 2) - (x2 ** 2) + (x3 ** 2) - (y2 ** 2) + (y3 ** 2)

    x = ((C * E) - (F * B)) / ((E * A) - (B * D))
    y = ((C * D) - (A * F)) / ((B * D) - (A * E))

    return x, y


def fix_direction():

    print("Fixing Direction...")

    if robot.get_compass_reading() in range(0, 90):
        while robot.experiment_supervisor.step(robot.timestep) != -1:
            if robot.get_compass_reading() not in range(85, 95):
                robot.rotate_that_bot()
            else:
                return

    elif robot.get_compass_reading() in range(91, 180):
        while robot.experiment_supervisor.step(robot.timestep) != -1:
            if robot.get_compass_reading() not in range(175, 185):
                robot.rotate_that_bot()
            else:
                return

    elif robot.get_compass_reading() in range(181, 270):
        while robot.experiment_supervisor.step(robot.timestep) != -1:
            if robot.get_compass_reading() not in range(265, 275):
                robot.rotate_that_bot()
            else:
                return

    elif robot.get_compass_reading() in range(271, 359):
        while robot.experiment_supervisor.step(robot.timestep) != -1:
            if robot.get_compass_reading() not in range(355, 359):
                robot.rotate_that_bot()
            else:
                return


if __name__ == "__main__":
    # set variables initially
    red_r1, green_r2, blue_r3 = None, None, None
    flag1, flag2, flag3 = 0, 0, 0

    while robot.experiment_supervisor.step(robot.timestep) != -1:
        rec_objects = robot.rgb_camera.getRecognitionObjects()

        robot.rotate_that_bot()

        # if camera has detected an object
        if len(rec_objects) > 0:
            # extract detected an object
            lm = rec_objects[0]

            # if camera detects yellow, ignore by moving to next iteration
            if lm.getColors()[0] == 1 and lm.getColors()[1] == 1:
                # print("Ignoring yellow...")
                continue

            # if camera detects red cylinder
            if lm.getColors()[0] == 1:
                red_r1 = lm.getPosition()[0] + cyl_radius
                flag1 = 1
                # print("Flag 1 met")

            # if camera detects green cylinder
            if lm.getColors()[1] == 1:
                green_r2 = lm.getPosition()[0] + cyl_radius
                flag2 = 1
                # print("Flag 2 met")

            # if camera detects blue cylinder
            if lm.getColors()[2] == 1:
                blue_r3 = lm.getPosition()[0] + cyl_radius
                flag3 = 1
                # print("Flag 3 met")

            # if all 3 cylinders detected, call trilateration to get x and y positions
            if flag1 == 1 and flag2 == 1 and flag3 == 1:
                print("--------------------------------")
                print("Scan complete!")

                fix_direction()

                x_pos, y_pos = trilateration(2, 2, red_r1, -2, -2, green_r2, 2, -2, blue_r3)

                row_n, col_n = determine_locate_cells_index(x_pos, y_pos)

                visited_cells_idx = locate_cells.index((row_n, col_n))

                # return boolean value if cell has been visited before
                visited = mark_visited_cells(visited_cells_idx, row_n, col_n)

                # put under if-statement later with boolean value from above
                if not visited:
                    print("x:", round(x_pos, 2), "y:", round(y_pos, 2), "n:", visited_cells_idx,
                          "Theta:", robot.get_compass_reading())

                # reset variables
                red_r1, green_r2, blue_rs = None, None, None
                flag1, flag2, flag3 = 0, 0, 0

                d_front = robot.get_lidar_range_image()[400]

                if d_front < 1.0:
                    print("WALL DETECTED! Turning around...")
                    robot.rotate_bot_degrees(-math.pi/2, 10)
                    fix_direction()

                if not visited:
                    print("Moving to next cell...")
                    robot.move_distance(1.0, 5)
