from re import L
from inputs import get_gamepad
import math
import threading
from gpiozero import PWMOutputDevice, DigitalOutputDevice, LED
from signal import pause

class Controller(object):
    #Normalize values to -1,0,1
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        #Identify buttons on controller
        self.LeftJoystickY = 0
        self.RightJoystickY = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this method
        Left_Y = self.LeftJoystickY 
        Right_Y = self.RightJoystickY 
        leftTrigger = self.LeftTrigger
        rightTrigger = self.RightTrigger
        leftBumper = self.LeftBumper
        rightBumper = self.RightBumper

        return [Left_Y, Right_Y, leftTrigger, rightTrigger]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                #Obtain input from the controller
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state


if __name__ == '__main__':
    joy = Controller()
    frequency = 50
    
    # Setup motor 1 PWM and direction
    pwm1_pin = PWMOutputDevice(12)
    pwm1_pin.frequency = frequency
    dir1_pin = DigitalOutputDevice(20)

    pwm2_pin = PWMOutputDevice(13)
    pwm2_pin.frequency = frequency
    dir2_pin = DigitalOutputDevice(19)

    led = LED(21)
    led.on()

    while True:
        while joy:  
            #led.on()      
            [Left_Y, Right_Y, leftTrigger, rightTrigger] = joy.read()
            deadzone = 0.2

            motor1_throttle = -1.0*Left_Y
            motor2_throttle = 1.0*Right_Y

            if motor1_throttle > deadzone:
                dir1_pin.on()
                pwm1_pin.value = abs(motor1_throttle)
            elif -1.0*deadzone < motor1_throttle < deadzone:
                dir1_pin.off()
                pwm1_pin.value = 0.0
            elif motor1_throttle < -1.0*deadzone:
                dir1_pin.off()
                pwm1_pin.value = abs(motor1_throttle)
            
            if motor2_throttle > deadzone:
                dir2_pin.on()
                pwm2_pin.value = abs(motor2_throttle)
            elif -1.0*deadzone < motor2_throttle < deadzone:
                dir2_pin.off()
                pwm2_pin.value = 0.0
            elif motor2_throttle < -1.0*deadzone:
                dir2_pin.off()
                pwm2_pin.value = abs(motor2_throttle)

                


         
            print(f'{dir1_pin.value} {pwm1_pin.value} {dir2_pin.value} {pwm2_pin.value}')

        pwm1_pin.value = 0.0
        pwm2_pin.value = 0.0
        led.off()

    """ 
    joy = Controller()
    frequency = 50
    in1_pin = PWMOutputDevice(12)
    in1_pin.frequency = frequency  
    in2_pin = PWMOutputDevice(13)
    in2_pin.frequency = frequency 
    led = LED(26)
    while True:               
        print(joy.read())
        [Left_Y, dcLeft_Y, Right_X, dcRight_Y, leftBumper, rightBumper] = joy.read()
        in1_pin.value = dcLeft_Y/100     #Duty cycle for pin 12
        in2_pin.value = dcRight_Y/100    #Duty cycle for pin 13
        led.on()

    while True:
        print(joy.read())
        [Left_Y, dcLeft_Y, Right_Y, dcRight_X, leftBumper, rightBumper] = joy.read()
        dcLeft_Y = (2.5 + 0.8206) / 0.0527
        dcRight_Y = (2.5 + 0.8795) / 0.0535
        in1_pin.value = 0
        in1_pin.value = 0
        led.off()
        #in1_pin.value = dcLeft_Y/100     #Duty cycle for pin 12
        #in2_pin.value = dcRight_Y/100    #Duty cycle for pin 13
        if leftBumper==1 & rightBumper==1:
    
            while True:               
                print(joy.read())
                [Left_Y, dcLeft_Y, Right_Y, dcRight_Y, leftBumper, rightBumper] = joy.read()
                in1_pin.value = dcLeft_Y/100     #Duty cycle for pin 12
                in2_pin.value = dcRight_Y/100    #Duty cycle for pin 13
                led.on()
                
                if leftBumper==0 & rightBumper==0:
                    continue
                elif leftBumper==1 & rightBumper==1:
                    break
                

        else:
            continue
            
    """
