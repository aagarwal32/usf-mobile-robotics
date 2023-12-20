# WebotsSim/controllers/Lab3_Task1/Lab3_Task1.py
# Changes Working Directory to be at the root of FAIRIS-Lite
import os
os.chdir("../..")

# Import MyRobot Class
from WebotsSim.libraries.MyRobot import MyRobot

# Create the robot instance.
robot = MyRobot()

# Loads the environment from the maze file
maze_file = 'worlds/mazes/Labs/Lab3/Lab3_Task1.xml'
robot.load_environment(maze_file)
# Move robot to a random staring position listed in maze file
robot.move_to_start()


def motion_to_goal():
    rec_objects = robot.rgb_camera.getRecognitionObjects()

    speed = robot.proportional_gain(0.1, 10.0)
    saturated_speed = robot.saturation_func(speed)

    # if camera has detected an object
    if len(rec_objects) > 0:
        # extract detected an object
        landmark = rec_objects[0]

        # print positions
        print("x: ", round(landmark.getPosition()[0], 2))
        print("y: ", round(landmark.getPosition()[1], 2))
        print("z: ", round(landmark.getPosition()[2], 2))

        # if object is in the center of the camera +- 0.5 meters
        if 0.5 > landmark.getPosition()[1] > -0.5:
            # move forward
            print("OBJECT DETECTED. MOVING TO GOAL...")
            print("SPEED: ", round(saturated_speed/2, 2))
            robot.set_left_motors_velocity(saturated_speed/2)
            robot.set_right_motors_velocity(saturated_speed/2)

            if landmark.getPosition()[0] < 0.5:
                print("ROBOT STOPPED", round(landmark.getPosition()[0], 2), "METERS FROM GOAL")
                robot.stop()


if __name__ == "__main__":

    while robot.experiment_supervisor.step(robot.timestep) != -1:
        objects = robot.rgb_camera.getRecognitionObjects()
        print("-----------------------------------------")

        # STATE 2: Object not detected -- rotate to find object
        if len(objects) == 0:
            print("OBJECT NOT DETECTED. ROTATING...")
            robot.set_left_motors_velocity(-5)
            robot.set_right_motors_velocity(5)

        # STATE 1: Object detected -- motion to goal
        motion_to_goal()

