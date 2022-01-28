import os
import time
from CoppeliaSim.scripts.modules import (
    sim as copp,
)  # access all the COPPELIASIM elements
import sys
import os
import random
from math import sqrt

# os.startfile(
#     r"C:\Users\adeko\OneDrive\Desktop\markerlessBoMI_FaMa\CoppeliaSim\scenes\kuka_robot_scene.ttt"
# )
class KukaMobileRobot:
    def __init__(self):
        copp.simxFinish(-1)  # just in case, close all opened connections

        self.clientID = copp.simxStart(
            "127.0.0.1", 19999, True, False, 60000, 5
        )  # start a connection
        if self.clientID != -1:
            print("Connected to remote API server")
            self.connected = True
        else:
            print("Not connected to remote API server")
            self.connected = False

        self.err_code, self.fl_motor = copp.simxGetObjectHandle(
            self.clientID, "rollingJoint_fl", copp.simx_opmode_blocking
        )
        self.err_code, self.rl_motor = copp.simxGetObjectHandle(
            self.clientID, "rollingJoint_rl", copp.simx_opmode_blocking
        )
        self.err_code, self.rr_motor = copp.simxGetObjectHandle(
            self.clientID, "rollingJoint_rr", copp.simx_opmode_blocking
        )
        self.err_code, self.fr_motor = copp.simxGetObjectHandle(
            self.clientID, "rollingJoint_fr", copp.simx_opmode_blocking
        )

        self.current_position_x = 0.0
        self.current_position_y = 0.0
        self.SPEED = 10

    def get_required_velocity(self, target):

        dist_x = target.crs_x - self.current_position_x
        dist_y = target.crs_y - self.current_position_y

        self.current_position_x = target.crs_x
        self.current_position_y = target.crs_y

        distance_to_target = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        required_x_vel = dist_x / (distance_to_target / self.SPEED)
        required_y_vel = dist_y / (distance_to_target / self.SPEED)
        return required_x_vel, required_y_vel

    def move_mobile_robot(self, target):
        if self.connected:
            rotVel = 0.0
            forwBackVel, leftRightVel = self.get_required_velocity(target)
            self.err_code = copp.simxSetJointTargetVelocity(
                self.clientID,
                self.fl_motor,
                -forwBackVel - leftRightVel - rotVel,
                copp.simx_opmode_oneshot,
            )
            self.err_code = copp.simxSetJointTargetVelocity(
                self.clientID,
                self.rl_motor,
                -forwBackVel + leftRightVel - rotVel,
                copp.simx_opmode_oneshot,
            )
            self.err_code = copp.simxSetJointTargetVelocity(
                self.clientID,
                self.rr_motor,
                -forwBackVel - leftRightVel + rotVel,
                copp.simx_opmode_oneshot,
            )
            self.err_code = copp.simxSetJointTargetVelocity(
                self.clientID,
                self.fr_motor,
                -forwBackVel + leftRightVel + rotVel,
                copp.simx_opmode_oneshot,
            )
        else:
            return "Not Connected"


# copp.simxFinish(-1)  # just in case, close all opened connections

# clientID = copp.simxStart(
#     "127.0.0.1", 19999, True, False, 60000, 5
# )  # start a connection

# if clientID != -1:
#     print("Connected to remote API server")
# else:
#     print("Not connected to remote API server")
#     sys.exit("Could not connect")

# err_code, fl_motor = copp.simxGetObjectHandle(
#     clientID, "rollingJoint_fl", copp.simx_opmode_blocking
# )
# err_code, rl_motor = copp.simxGetObjectHandle(
#     clientID, "rollingJoint_rl", copp.simx_opmode_blocking
# )
# err_code, rr_motor = copp.simxGetObjectHandle(
#     clientID, "rollingJoint_rr", copp.simx_opmode_blocking
# )
# err_code, fr_motor = copp.simxGetObjectHandle(
#     clientID, "rollingJoint_fr", copp.simx_opmode_blocking
# )


# current_position_x = 0.0
# current_position_y = 0.0
# SPEED = 10


# def get_required_velocity():
#     """
#     Calculates the distance between the robot and the
#     target
#     Args:
#         target (Object): Object containing the x and y
#         coodinates of the new target
#     Returns:
#         (int): returns a tuple of the value of the
#         distance to the target and the required velocity
#         in the x and y direction to reach the target and
#         the distance to the target
#     """
#     global current_position_x, current_position_y
#     target_cord_x = random.randint(1, 10)
#     target_cord_y = random.randint(1, 10)

#     dist_x = target_cord_x - current_position_x
#     dist_y = target_cord_y - current_position_y

#     current_position_x = target_cord_x
#     current_position_y = target_cord_y

#     distance_to_target = sqrt((dist_x * dist_x) + (dist_y * dist_y))
#     required_x = dist_x / (distance_to_target / SPEED)
#     required_y = dist_y / (distance_to_target / SPEED)
#     return required_x, required_y


# def setMovement(forwBackVel, leftRightVel, rotVel):
#     err_code = copp.simxSetJointTargetVelocity(
#         clientID,
#         fl_motor,
#         -forwBackVel - leftRightVel - rotVel,
#         copp.simx_opmode_oneshot,
#     )
#     err_code = copp.simxSetJointTargetVelocity(
#         clientID,
#         rl_motor,
#         -forwBackVel + leftRightVel - rotVel,
#         copp.simx_opmode_oneshot,
#     )
#     err_code = copp.simxSetJointTargetVelocity(
#         clientID,
#         rr_motor,
#         -forwBackVel - leftRightVel + rotVel,
#         copp.simx_opmode_oneshot,
#     )
#     err_code = copp.simxSetJointTargetVelocity(
#         clientID,
#         fr_motor,
#         -forwBackVel + leftRightVel + rotVel,
#         copp.simx_opmode_oneshot,
#     )


# if __name__ == "__main__":
#     while 1:
#         x, y = get_required_velocity()
#         time.sleep(0.1)
#         setMovement(x, y, 0)
