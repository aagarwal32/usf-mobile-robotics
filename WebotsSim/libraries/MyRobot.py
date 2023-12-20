# WebotsSim/libraries/myRobot.py

from WebotsSim.libraries.RobotLib.RosBot import RosBot
import math


class MyRobot(RosBot):

    def __init__(self):
        RosBot.__init__(self)

    def motion_to_goal(self):
        rec_objects = self.rgb_camera.getRecognitionObjects()

        speed = self.proportional_gain(0.2, 5.0)
        saturated_speed = self.saturation_func(speed)

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

                if landmark.getPosition()[0] < 0.5:
                    self.stop()
                # move forward
                elif landmark.getPosition()[0] < 3.0:
                    print("SPEED: ", round(saturated_speed, 2))
                    self.set_left_motors_velocity(saturated_speed)
                    self.set_right_motors_velocity(saturated_speed)

                else:
                    print("SPEED: ", 15.00)
                    self.set_left_motors_velocity(15)
                    self.set_right_motors_velocity(15)

    def saturation_func(self, signal):
        # test for saturation motor velocity
        if signal >= self.max_motor_velocity:
            signal = self.max_motor_velocity

        elif signal <= -self.max_motor_velocity:
            signal = -self.max_motor_velocity

        return signal

    def proportional_gain(self, d_maintain, kp, wall_to_follow="NONE"):
        # if this function is being used for wall follow, get corresponding front sensor range
        if wall_to_follow == "R":
            d_front = min(self.get_lidar_range_image()[400:600])
        elif wall_to_follow == "L":
            d_front = min(self.get_lidar_range_image()[200:400])
        else:
            # if not wall following, range is straight
            d_front = min(self.get_lidar_range_image()[300:500])

        # print("---------------------------------")
        # print("d_front: ", d_front)

        dist_error_front = d_front - d_maintain
        # print("error_front: ", dist_error_front)
        v_front = kp * dist_error_front

        return v_front

    def wall_following_pid(self, wall_to_follow, d_mid=0.40, k_p=5.0):
        forward_velocity = self.proportional_gain(0.10, 10.0, wall_to_follow)

        # get sensor readings to detect min distance to side walls
        d_left = min(self.get_lidar_range_image()[200:300])
        # print("d_left ", d_left)
        d_right = min(self.get_lidar_range_image()[500:600])
        # print("d_right: ", d_right)

        # perform wall following
        if wall_to_follow == "R":
            error = d_mid - d_right
            if d_right < d_mid:
                v_left = self.saturation_func(forward_velocity - abs(k_p * error))
                v_right = self.saturation_func(forward_velocity)

            elif d_right > d_mid:
                v_left = self.saturation_func(forward_velocity)
                v_right = self.saturation_func(forward_velocity - abs(k_p * error))

            else:
                v_left = self.saturation_func(forward_velocity)
                v_right = self.saturation_func(forward_velocity)

        else:
            error = d_mid - d_left
            if d_left < d_mid:
                v_right = self.saturation_func(forward_velocity - abs(k_p * error))
                v_left = self.saturation_func(forward_velocity)

            elif d_left > d_mid:
                v_right = self.saturation_func(forward_velocity)
                v_left = self.saturation_func(forward_velocity - abs(k_p * error))

            else:
                v_left = self.saturation_func(forward_velocity)
                v_right = self.saturation_func(forward_velocity)

        return v_left, v_right

    def encoder_reading(self):

        dist_front_left_wheel_travel = (self.wheel_radius * self.get_front_left_motor_encoder_reading())
        return dist_front_left_wheel_travel

    def move_distance(self, meters, move_speed):

        prev_encoder_reading = self.encoder_reading()
        while self.experiment_supervisor.step(self.timestep) != -1:
            current_encoder_reading = self.encoder_reading()
            if current_encoder_reading < prev_encoder_reading + meters:
                self.set_left_motors_velocity(move_speed)
                self.set_right_motors_velocity(move_speed)
            else:
                return

    def rotate_that_bot(self, rotation_speed=5):

        self.set_left_motors_velocity(-rotation_speed)
        self.set_right_motors_velocity(rotation_speed)

    def rotate_bot_degrees(self, rad_angle, rotate_speed):
        # distance of each wheel during rotation
        rotate_distance = rad_angle * (self.axel_length / 2)
        rotate_distance = abs(rotate_distance)

        if rad_angle < 0:
            prev_distance = self.encoder_reading()
            while self.experiment_supervisor.step(self.timestep) != -1:
                cur_distance = self.encoder_reading()
                if cur_distance > prev_distance - rotate_distance:
                    self.set_left_motors_velocity(-rotate_speed)
                    self.set_right_motors_velocity(rotate_speed)
                else:
                    return

        else:
            prev_distance = self.encoder_reading()
            while self.experiment_supervisor.step(self.timestep) != -1:
                cur_distance = self.encoder_reading()
                if cur_distance < prev_distance + rotate_distance:
                    self.set_left_motors_velocity(rotate_speed)
                    self.set_right_motors_velocity(-rotate_speed)
                else:
                    return

    def fix_direction(self):

        if self.get_compass_reading() in range(0, 90):
            while self.experiment_supervisor.step(self.timestep) != -1:
                if self.get_compass_reading() not in range(85, 95):
                    self.rotate_that_bot()
                else:
                    return

        elif self.get_compass_reading() in range(91, 180):
            while self.experiment_supervisor.step(self.timestep) != -1:
                if self.get_compass_reading() not in range(175, 185):
                    self.rotate_that_bot()
                else:
                    return

        elif self.get_compass_reading() in range(181, 270):
            while self.experiment_supervisor.step(self.timestep) != -1:
                if self.get_compass_reading() not in range(265, 275):
                    self.rotate_that_bot()
                else:
                    return

        elif self.get_compass_reading() in range(271, 359):
            while self.experiment_supervisor.step(self.timestep) != -1:
                if self.get_compass_reading() not in range(355, 359):
                    self.rotate_that_bot()
                else:
                    return
