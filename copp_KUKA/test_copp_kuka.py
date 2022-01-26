import numpy as np
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
#import sim
import sim as copp # access all the COPPELIASIM elements
import sys


copp.simxFinish(-1) # just in case, close all opened connections

clientID=copp.simxStart('127.0.0.1',19999,True,True,5000,5) # start a connection

if clientID!=-1:
    print ("Connected to remote API server")
else:
    print("Not connected to remote API server")
    sys.exit("Could not connect")

err_code, fl_motor = copp.simxGetObjectHandle(clientID,"rollingJoint_fl", copp.simx_opmode_blocking)
err_code, rl_motor = copp.simxGetObjectHandle(clientID,"rollingJoint_rl", copp.simx_opmode_blocking)
err_code, rr_motor = copp.simxGetObjectHandle(clientID,"rollingJoint_rr", copp.simx_opmode_blocking)
err_code, fr_motor = copp.simxGetObjectHandle(clientID,"rollingJoint_fr", copp.simx_opmode_blocking)


def setMovement(forwBackVel,leftRightVel,rotVel):
    err_code = copp.simxSetJointTargetVelocity(clientID, fl_motor, -forwBackVel-leftRightVel-rotVel, copp.simx_opmode_streaming)
    err_code = copp.simxSetJointTargetVelocity(clientID, rl_motor, -forwBackVel+leftRightVel-rotVel, copp.simx_opmode_streaming)
    err_code = copp.simxSetJointTargetVelocity(clientID, rr_motor, -forwBackVel-leftRightVel+rotVel, copp.simx_opmode_streaming)
    err_code = copp.simxSetJointTargetVelocity(clientID, fr_motor, -forwBackVel+leftRightVel+rotVel, copp.simx_opmode_streaming)

if __name__ == "__main__":
    setMovement(0,0.5,0)
    time.sleep(10) # Sleep for 20 seconds
    setMovement(0.5,0,0)