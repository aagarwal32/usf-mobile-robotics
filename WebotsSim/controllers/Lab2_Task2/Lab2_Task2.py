# WebotsSim/controllers/Lab2_Task2/Lab2_Task2.py
# Changes Working Directory to be at the root of FAIRIS-Lite
import os
os.chdir("../..")

# Import MyRobot Class
from WebotsSim.libraries.MyRobot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = 'worlds/mazes/Labs/Lab2/Lab2_2.xml'
robot.load_environment(maze_file)
# Move robot to a random staring position listed in maze file
robot.move_to_start()

max_motor_velocity = robot.max_motor_velocity


def saturation_func(signal):
    # test for saturation motor velocity
    if signal >= max_motor_velocity:
        signal = max_motor_velocity / 2

    elif signal <= -max_motor_velocity:
        signal = -max_motor_velocity / 2

    return signal


def proportional_gain(d_maintain=0.30, kp=5.0):
    d_front = robot.get_lidar_range_image()[400]

    print("---------------------------------")
    print("d_front: ", d_front)

    dist_error_front = d_front - d_maintain
    print("error_front: ", dist_error_front)
    v_front = kp * dist_error_front

    return v_front


def wall_following_pid(wall_to_follow, d_mid=0.40, k_p=5.0):
    forward_velocity = proportional_gain()

    # get sensor readings to detect min distance to side walls
    d_left = min(robot.get_lidar_range_image()[200:300])
    print("d_left ", d_left)
    d_right = min(robot.get_lidar_range_image()[500:600])
    print("d_right: ", d_right)

    # perform wall following
    if wall_to_follow == "R":
        error = d_mid - d_right
        if d_right < d_mid:
            v_left = saturation_func(forward_velocity - abs(k_p*error))
            v_right = saturation_func(forward_velocity)

        elif d_right > d_mid:
            v_left = saturation_func(forward_velocity)
            v_right = saturation_func(forward_velocity - abs(k_p*error))

        else:
            v_left = saturation_func(forward_velocity)
            v_right = saturation_func(forward_velocity)

    else:
        error = d_mid - d_left
        if d_left < d_mid:
            v_right = saturation_func(forward_velocity - abs(k_p * error))
            v_left = saturation_func(forward_velocity)

        elif d_left > d_mid:
            v_right = saturation_func(forward_velocity)
            v_left = saturation_func(forward_velocity - abs(k_p * error))

        else:
            v_left = saturation_func(forward_velocity)
            v_right = saturation_func(forward_velocity)

    return v_left, v_right


if __name__ == "__main__":

    while robot.experiment_supervisor.step(robot.timestep) != -1:

        wall = "R"
        left_speed, right_speed = wall_following_pid(wall)

        print("left speed: ", left_speed)
        robot.set_left_motors_velocity(left_speed)
        print(" right speed: ", right_speed)
        robot.set_right_motors_velocity(right_speed)

        dist_front = robot.get_lidar_range_image()[400]
        dist_right = robot.get_lidar_range_image()[600]
        dist_left = robot.get_lidar_range_image()[200]

        # v_front = robot.proportional_gain(0.30, 5.0)
        # sat_vel = robot.saturation_func(v_front)
        # robot.wall_following_pid("R")

        if dist_front < 0.7 and wall == "R":
            robot.rotate(max_motor_velocity, -90)

        if dist_front < 0.6 and dist_left < 0.6 and wall == "L":
            robot.rotate(max_motor_velocity, 90)
