#WebotsSim/controllers/Lab2_Task1/Lab2_Task1.py
# Changes Working Directory to be at the root of FAIRIS-Lite
import os
os.chdir("../..")

# Import MyRobot Class
from WebotsSim.libraries.MyRobot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = 'worlds/mazes/Labs/Lab2/Lab2_1.xml'
robot.load_environment(maze_file)

max_motor_velocity = 26 * robot.wheel_radius

d_maintain = -0.5
kp = 0.5


def saturation_func(signal):
    # test for saturation motor velocity
    if signal >= max_motor_velocity:
        signal = max_motor_velocity

    elif signal <= -max_motor_velocity:
        signal = -max_motor_velocity

    return signal


def proportional_gain():

    d_front = min(-1*robot.get_lidar_range_image()[350], -1*robot.get_lidar_range_image()[400],
                  -1*robot.get_lidar_range_image()[450])

    print("d_front: ", d_front)

    dist_error_front = d_maintain - d_front
    print("error_front: ", dist_error_front)
    v_front = kp * dist_error_front

    return v_front


def wall_avoidance_pid(d_mid=0.40, k_p=2.0):

    forward_velocity = proportional_gain()

    # get sensor readings to detect min distance to side walls
    d_left = min(robot.get_lidar_range_image()[100], robot.get_lidar_range_image()[200],
                 robot.get_lidar_range_image()[300])
    print("d_left ", d_left)
    d_right = min(robot.get_lidar_range_image()[500], robot.get_lidar_range_image()[600],
                  robot.get_lidar_range_image()[700])
    print("d_right: ", d_right)

    # perform wall avoidance
    if d_left < d_mid:
        error = d_mid - d_left
        v_left = saturation_func(forward_velocity)
        v_right = saturation_func(forward_velocity - abs(k_p*error))

    elif d_right < d_mid:
        error = d_mid - d_right
        v_left = saturation_func(forward_velocity - abs(k_p*error))
        v_right = saturation_func(forward_velocity)

    else:
        v_left = saturation_func(forward_velocity)
        v_right = saturation_func(forward_velocity)

    return v_left, v_right


if __name__ == "__main__":

    while robot.experiment_supervisor.step(robot.timestep) != -1:

        left_speed, right_speed = wall_avoidance_pid()

        left_speed_ang = left_speed / robot.wheel_radius
        right_speed_ang = right_speed / robot.wheel_radius

        print("left speed: ", left_speed_ang)
        robot.set_left_motors_velocity(left_speed_ang)
        print(" right speed: ", right_speed_ang)
        robot.set_right_motors_velocity(right_speed_ang)
