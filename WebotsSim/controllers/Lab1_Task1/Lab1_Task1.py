# Changes Working Directory to be at the root of FAIRIS-Lite
import os
import math
os.chdir("../..")

# Import MyRobot Class
from WebotsSim.libraries.MyRobot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = 'worlds/mazes/Labs/Lab1/Lab1.xml'
robot.load_environment(maze_file)

fl_offset = 4.40 

x_start = 1.5
y_start = -6.0
prev_encoder = 0

# set angular velocity of robot
ang_speed = 7.5  # rad/sec

# linear velocity
linear_velocity = ang_speed * robot.wheel_radius

# axel distance from midpoint
d_mid = robot.axel_length / 2


def update_position():
    global x_start, y_start, prev_encoder
    theta = robot.get_compass_reading()

    enc_val = robot.get_encoder_readings()

    cur_encoder = (enc_val[0] + enc_val[1] + enc_val[2] + enc_val[3]) / 4

    distance_traveled = (cur_encoder - prev_encoder) * robot.wheel_radius

    angle_radians = math.radians(theta)

    x_start += distance_traveled * math.cos(angle_radians)
    y_start += distance_traveled * math.sin(angle_radians)

    print("x=", round(x_start, 1), end=" ")
    print("y=", round(y_start, 1), end=" ")
    print("Theta=", theta)

    prev_encoder = cur_encoder


# create function for rotation in place motion
def rotate_in_place(distance, rad_angle):

    # distance of each wheel during rotation
    rotate_distance = rad_angle * d_mid
    rotate_distance = abs(rotate_distance)

    if rad_angle < 0:
        # rotate counter-clockwise
        robot.set_left_motors_velocity(-(ang_speed/4))
        robot.set_right_motors_velocity(ang_speed/4)
        distance = distance - rotate_distance

    elif rad_angle > 0:
        # rotate clockwise
        robot.set_left_motors_velocity(ang_speed/4)
        robot.set_right_motors_velocity(-(ang_speed/4))
        distance = distance + rotate_distance

    else:
        print("Error: Angle not known to perform rotation in place! ")
        robot.stop()

    while robot.experiment_supervisor.step(robot.timestep) != -1:

        # Calculates distance the wheel has turned since beginning of simulation
        dist_front_left_wheel_travel = (robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) - fl_offset

        if rad_angle < 0 and dist_front_left_wheel_travel < distance:
            return distance
        if rad_angle > 0 and dist_front_left_wheel_travel > distance:
            return distance


# create function for circular motion
def move_along_curve(distance, inner_wheel):

    # circle radius
    circle_radius = 0.5

    # distance inner wheel travel for quarter circle
    quarter_dist_inner_wheel = (2 * math.pi * (circle_radius - d_mid)) / 4
    # distance outer wheel travel for quarter circle
    quarter_dist_outer_wheel = (2 * math.pi * (circle_radius + d_mid)) / 4

    # get angular velocity of curve
    ang_speed_curve = linear_velocity / (circle_radius + d_mid)

    # get linear velocity of inner wheel during curve
    inner_wheel_linear_vel = ang_speed_curve * (circle_radius - d_mid)

    # get angular velocity of inner wheel during curve
    inner_wheel_ang_vel = inner_wheel_linear_vel / robot.wheel_radius

    if inner_wheel == "left":

        robot.set_right_motors_velocity(ang_speed)
        robot.set_left_motors_velocity(inner_wheel_ang_vel)

        distance = distance + quarter_dist_inner_wheel

        # print linear velocity of inner and outer wheels
        print("Vl=", round(inner_wheel_linear_vel, 1), "m/s,", "Vr=", round(linear_velocity, 1), "m/s,", end=" ")

    elif inner_wheel == "right":

        robot.set_right_motors_velocity(inner_wheel_ang_vel)
        robot.set_left_motors_velocity(ang_speed)

        distance = distance + quarter_dist_outer_wheel

        # print linear velocity of inner and outer wheels
        print("Vl=", round(linear_velocity, 1), "m/s,", "Vr=", round(inner_wheel_linear_vel, 1), "m/s,", end=" ")

    else:
        print("Error: Inner wheel not known to perform curve! ")
        robot.stop()

    # print distance traveled during curve
    curve_dist = (2 * math.pi * circle_radius) / 4
    print("D=", round(curve_dist, 1), "m", end=" ")

    # print time taken to complete curve
    curve_linear_velocity = (inner_wheel_linear_vel + linear_velocity) / 2
    curve_time = curve_dist / curve_linear_velocity
    print("T=", round(curve_time, 1), "sec")

    while robot.experiment_supervisor.step(robot.timestep) != -1:

        # Calculates distance the wheel has turned since beginning of simulation
        dist_front_left_wheel_travel = (robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) - fl_offset

        update_position()

        if dist_front_left_wheel_travel > distance:
            return distance


# create function for straight line motion
def move_straight_line(distance, add_dist):

    robot.set_right_motors_velocity(ang_speed)
    robot.set_left_motors_velocity(ang_speed)

    distance = distance + add_dist
    straight_time = add_dist / linear_velocity
    # print distance and linear velocity of left/right wheels
    print("Vl=", round(linear_velocity, 1), "m/s,", "Vr=", round(linear_velocity, 1), "m/s,",
          "D=", round(add_dist, 1), "m",
          "T=", round(straight_time, 1), "sec")

    # Main Control Loop for Robot
    while robot.experiment_supervisor.step(robot.timestep) != -1:

        # Calculates distance the wheel has turned since beginning of simulation
        dist_front_left_wheel_travel = (robot.wheel_radius * robot.get_front_left_motor_encoder_reading()) - fl_offset

        update_position()

        if dist_front_left_wheel_travel > distance:
            return distance


if __name__ == "__main__":

    total_distance = 0

    print("P0 to P1:")
    total_distance = move_straight_line(total_distance, 2.5)

    print("P1 to P2:")
    total_distance = move_along_curve(total_distance, "left")

    print("P2 to P3:")
    total_distance = move_straight_line(total_distance, 2.0)

    print("P3 to P4:")
    total_distance = move_along_curve(total_distance, "left")

    print("P4 to P5:")
    total_distance = move_straight_line(total_distance, 0.5)

    total_distance = rotate_in_place(total_distance, -math.pi/2)

    print("P5 to P6:")
    total_distance = move_straight_line(total_distance, 1.5)

    print("P6 to P7:")
    total_distance = move_along_curve(total_distance, "right")
    print("P7 to P8:")
    total_distance = move_along_curve(total_distance, "right")

    print("P8 to P9:")
    total_distance = move_straight_line(total_distance, 1.0)

    print("P9 to P10:")
    total_distance = move_along_curve(total_distance, "left")
    print("P10 to P11:")
    total_distance = move_along_curve(total_distance, "left")

    print("P11 to P12:")
    total_distance = move_straight_line(total_distance, 1.5)

    robot.stop()
