"""
.. module:: kuka_controller

:platform: Unix
:synopsis: Python module for the position controller of the kuka robot 

.. moduleauthor:: Omotoye Shamsudeen Adekoya, Leonardo Borgioli, Yara Abdelmottaleb, Adedamola Sode.

This script implements the position controller of the kuka robot
"""

import os
import time
from CoppeliaSim.scripts.modules import (
    sim as copp,
)  # access all the COPPELIASIM elements
import sys
import os
import random
from math import sqrt

class KukaMobileRobot:
    """
    A class responsible for communicating with the Kuka mobile robot and controlling it
    """
    def __init__(self):
        """
        Initialization of the KukaMobileRobot class
        Establishes the connection. Sets the port at which to communicate with CoppeliaSim
        Gets the object handles for the four motors of the Kuka robot
        Initialize current robot position to zero
      
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
        self.distance_to_target = 0.0
        self.SPEED = 1

    def get_required_velocity(self):
        """
        Computes the required x and y velocities to be sent to the robot based on the distance to the target
        The velocities are multiplied by a gain SPEED
      
        """
        x, y = self.target
        print(
            f"x:{x}, y:{y}, current_position_x: {self.current_position_x}, current_position_y: {self.current_position_y}\n\n"
        )
        #dist_x = abs(x - self.current_position_x)
        #dist_y = abs(y - self.current_position_y)
        
        dist_x=x - self.current_position_x
        dist_y = y - self.current_position_y

        self.current_position_x = x
        self.current_position_y = y
        distance_to_target = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        required_x_vel = dist_x / (distance_to_target / self.SPEED)
        required_y_vel = dist_y / (distance_to_target / self.SPEED)
        print(
            f"distance_to_target: {distance_to_target}, required_x_vel: {required_x_vel}, required_y_vel: {required_y_vel}"
        )
        return distance_to_target, required_x_vel, required_y_vel

    def move_mobile_robot(self, x, y):
        """
        responsible for moving the mobile robot given a target position x and y
        It gets the required x and y velocities for the robot using the function get_required_velocity() 
        and sets the motor velocity values based on these velocities
        :param x: the target x position
        :param y: the target y position
        :return:
        """
        if self.connected:
            rotVel = 0.0

            self.target = (x, y)
            (
                self.distance_to_target,
                forwBackVel,
                leftRightVel,
            ) = self.get_required_velocity()
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
