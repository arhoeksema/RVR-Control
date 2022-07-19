import asyncio, math, os, signal, subprocess
import sys, threading, time, lgpio
from inputs import get_gamepad

import motor
import controller

status = 1
forward = 1 
backward = 0

leftSpeed = 100
rightSpeed = 100

def setup():
    motor.setup()
    controller.setup()

def driveMotor(direction, speed):
    if direction == "forward":
        motor.motor_1(status, forward, leftSpeed)
        motor.motor_2(status, forward, rightSpeed)
    elif direction == "backward":
        motor.motor_1(status, backward, leftSpeed)
        motor.motor_2(status, backward, rightSpeed)
    else:
        motor.motorStop()

"""
Need to figure out the code for controlling
the turning/direction of RVR

def motorDirection(x,y):

"""

while True:
    for event in 