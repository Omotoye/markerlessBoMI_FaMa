import os
import time
from CoppeliaSim.scripts.modules import (
    sim as copp,
)  # access all the COPPELIASIM elements
import os

# os.startfile(
#     r"C:\Users\adeko\OneDrive\Desktop\markerlessBoMI_FaMa\CoppeliaSim\scenes\kuka_robot_scene.ttt"
# )


class PlanarManipulator:
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

        self.err_code, self.target_handle = copp.simxGetObjectHandle(
            self.clientID, "redundantRob_target", copp.simx_opmode_blocking
        )

    def move_manipulator_tip(self, target):
        copp.simxSetObjectPosition(
            self.clientID, self.target_handle, -1, target, copp.simx_opmode_blocking
        )


# copp.simxFinish(-1)  # just in case, close all opened connections

# clientID = copp.simxStart(
#     "127.0.0.1", 19999, True, False, 60000, 5
# )  # start a connection

# if clientID != -1:
#     print("Connected to remote API server")
# else:
#     print("Not connected to remote API server")
#     sys.exit("Could not connect")

# err_code, target = copp.simxGetObjectHandle(
#     clientID, "redundantRob_target", copp.simx_opmode_blocking
# )
# coord = [1, 1, 1]
# returnCode = copp.simxSetObjectPosition(
#     clientID, target, -1, coord, copp.simx_opmode_blocking
# )
