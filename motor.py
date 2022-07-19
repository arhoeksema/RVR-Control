import lgpio
import time
import subprocess, controller

#General Info
frequency = 5000
h = lgpio.gpiochip_open(0)

#Pins the motors recieve PWM signals and connect to ground
#motor_1_dir = 0 #figure out GPIO output!
motor_1_in1 = 12 #pwm
#motor_2_dir = 0 #figure out GPIO output!
motor_2_in2 = 13 #pwm

#Motor direction
dir_forward = -1
dir_backward = 1
dir_left = -1
dir_right = 1

pwm_1 = 0
pwm_2 = 0

#Motor initialization & sets outputs to HIGH
def setup():
    controller.setup()
    global pwm_1, pwm_2
    #lgpio.gpio_claim_output(h, motor_1_dir, 1, 0) 
    lgpio.gpio_claim_output(h, motor_1_in1, 1, 0) 
    #lgpio.gpio_claim_output(h, motor_2_dir, 1, 0) 
    lgpio.gpio_claim_output(h, motor_2_in2, 1, 0) 
"""
    try:
        pwm_1 = lgpio.tx_pwm(h, motor_1_in1, frequency, DC_1)
        pwm_2 = lgpio.tx_pwm(h, motor_2_in2, frequency, DC_2)
    except:
        pass
"""
#Motor stops & sets outputs to LOW
def motorStop():
    #lgpio.gpio_claim_output(h, motor_1_dir, 0, 0) 
    lgpio.gpio_claim_output(h, motor_1_in1, 0, 0) 
    #lgpio.gpio_claim_output(h, motor_2_dir, 0, 0) 
    lgpio.gpio_claim_output(h, motor_2_in2, 0, 0) 

#Motor 1 positive and negative rotation
def motor_1(status, direction, speed):
    global pwm_1
    if status == 0:
        motorStop()
    else:
        if direction == dir_forward: 
            lgpio.gpio_claim_output(h, motor_1_in1, 1, 0) 
            pwm_1 = lgpio.tx_pwm(h, motor_1_in1, frequency, dcLY)
        elif direction == dir_backward:
            lgpio.gpio_claim_output(h, motor_1_in1, 0, 0) 
            pwm_1 = lgpio.tx_pwm(h, motor_1_in1, frequency, dcLY)
            

#Motor 2 positive and negative rotation
def motor_2(status, direction, speed):
    global pwm_2
    if status == 0:
        motorStop()
    else:
        if direction == dir_forward: 
            lgpio.gpio_claim_output(h, motor_2_in2, 1, 0) 
            pwm_2 = lgpio.tx_pwm(h, motor_2_in2, frequency, dcRX)
        elif direction == dir_backward:
            lgpio.gpio_claim_output(h, motor_2_in2, 0, 0) 
            pwm_2 = lgpio.tx_pwm(h, motor_2_in2, frequency, dcRX)     
    return direction


def destroy():
    motorStop()

try:
    pass
except KeyboardInterrupt:
    destroy()
    lgpio.gpiochip_close(h)