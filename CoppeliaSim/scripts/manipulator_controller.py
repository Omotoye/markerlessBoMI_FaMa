"""
.. module:: manipulator_controller

:platform: Unix
:synopsis: Python module for the position controller of the manipulator

.. moduleauthor:: Omotoye Shamsudeen Adekoya, Leonardo Borgioli, Yara Abdelmottaleb, Adedamola Sode.

This script implements the position controller of the manipulator
"""

import os
import time
from CoppeliaSim.scripts.modules import (
    sim as copp,
)  # access all the COPPELIASIM elements
import os


class ManipulatorController:
    """
    A class responsible for communicating with the manipulator on CoppeliaSim and controlling it
    """
    def __init__(self):
        """
        Initialization of the ManipulatorController class
        Establishes the connection. Sets the port at which to communicate with CoppeliaSim
        Gets the handle for the target object attached to the tip of the manipulator     
        """
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
            self.clientID, "TargetObject", copp.simx_opmode_blocking
        )

    def move_manipulator_tip(self, target):
        """
        responsible for moving the manipulator's tip to a given target position
        :param target: target position for the tip (x,y,z)
        :return:
        """
        copp.simxSetObjectPosition(
            self.clientID, self.target_handle, -1, target, copp.simx_opmode_blocking
        )
