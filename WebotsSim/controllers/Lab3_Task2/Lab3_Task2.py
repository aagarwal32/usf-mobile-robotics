# WebotsSim/controllers/Lab3_Task2/Lab3_Task2.py
# Changes Working Directory to be at the root of FAIRIS-Lite
import os
os.chdir("../..")

# Import MyRobot Class
from WebotsSim.libraries.MyRobot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = 'worlds/mazes/Labs/Lab3/Lab3_Task2_1.xml'
robot.load_environment(maze_file)
# Move robot to a random staring position listed in maze file
robot.move_to_start()


if __name__ == "__main__":

    while robot.experiment_supervisor.step(robot.timestep) != -1:
        rec_objects = robot.rgb_camera.getRecognitionObjects()
        d_front = robot.get_lidar_range_image()[400]
        wall = "L"      # choose wall to follow
        print("FRONT DIST: ", round(d_front, 2))

        # IF OBJECT NOT DETECTED
        if len(rec_objects) == 0:
            print("------------------------------")
            print("OBJECT NOT DETECTED")

            # STATE 2: ROTATE TO FOLLOW WALL
            if d_front < 3.0:
                print("ROTATING...")
                if wall == "R":
                    robot.set_left_motors_velocity(-robot.max_motor_velocity)
                    robot.set_right_motors_velocity(robot.max_motor_velocity)
                else:
                    robot.set_left_motors_velocity(robot.max_motor_velocity)
                    robot.set_right_motors_velocity(-robot.max_motor_velocity)

            # STATE 3: WALL FOLLOWING
            else:
                print("WALL FOLLOWING...")
                l_speed, r_speed = robot.wall_following_pid(wall, d_mid=0.55, k_p=8)
                print("LEFT SPEED: ", round(l_speed, 2), "RIGHT SPEED: ", round(r_speed, 2))
                robot.set_left_motors_velocity(l_speed)
                robot.set_right_motors_velocity(r_speed)

        # STATE 1: MOVE STRAIGHT TOWARDS GOAL IF OBJECT DETECTED
        if len(rec_objects) > 0:
            print("--------------------------------")
            print("OBJECT DETECTED! MOTION TO GOAL")
            robot.motion_to_goal()
