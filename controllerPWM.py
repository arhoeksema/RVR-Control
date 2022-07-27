from inputs import get_gamepad
import lgpio
import math
import threading
import time

h = lgpio.gpiochip_open(0)
dcLeft_Y = (2.5 + 0.8206) / 0.0527
dcRight_X = (2.5 + 0.8795) / 0.0535 


class Controller(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.RightJoystickX = 0
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
        Left_Y = (self.LeftJoystickY * -2.5) + 2.5
        if Left_Y >= 4.75:
            Left_Y = 5.0
        elif 2.40 <= Left_Y <= 2.60:
            Left_Y = 2.5
        elif Left_Y <= .1:
            Left_Y = 0
        else:
            Left_Y = (self.LeftJoystickY * -2.5) + 2.5
        
        dcLeft_Y = (Left_Y + 0.8206) / 0.0527   #Duty cycle % for left joystick
        
        if dcLeft_Y > 100:
            dcLeft_Y = 100
            Left_Y = (0.0527 * dcLeft_Y) - 0.8206
        else:
            dcLeft_Y = (Left_Y + 0.8206) / 0.0527


        Right_X = (self.RightJoystickX * 2.5) + 2.5
        if Right_X >= 4.75:
            Right_X = 5.0
        elif 2.40 <= Right_X <= 2.60:
            Right_X = 2.5
        elif Right_X <= .1:
            Right_X = 0
        else:
            Right_X = (self.RightJoystickX * 2.5) + 2.5

        dcRight_X = (Right_X + 0.8795) / 0.0535   #Duty cycle % for right joystick
        if dcRight_X > 100:
            dcRight_X = 100
            Right_X = (0.0535 * dcRight_X) - 0.8795
        else:
            dcRight_X = (Right_X + 0.8795) / 0.0535

        button_A = self.A
        button_B = self.B
        button_Y = self.Y
        button_X = self.X
        return [Left_Y, dcLeft_Y, Right_X, dcRight_X, button_A, button_B, button_Y, button_X]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
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
    """
    def button(event):
            if event.code == 'BTN_THUMBL':
                lgpio.tx_pwm(h, LED, frequency, 0)
                #lgpio.tx_pwm(h, in1_pin, frequency, pwm_L)
                #lgpio.tx_pwm(h, in2_pin, frequency, pwm_R)
                lgpio.gpiochip_close(h)
"""

if __name__ == '__main__':
    joy = Controller()
    while True:
        print(joy.read())
        [Left_Y, dcLeft_Y, Right_X, dcRight_X, button_A, button_B, button_Y, button_X] = joy.read()
        frequency = 5000
        #in1_pin = 12
        #in2_pin = 13
        LED = 23
        pwm_L = 0
        pwm_R = dcRight_X
        lgpio.tx_pwm(h, LED, frequency, pwm_L)
        if button_A==1 & button_B==1:
            
            while True:
                print(joy.read())
                [Left_Y, dcLeft_Y, Right_X, dcRight_X, button_A, button_B, button_Y, button_X] = joy.read()
                frequency = 5000
                in1_pin = 12
                in2_pin = 13
                LED = 23
                pwm_L = dcLeft_Y
                pwm_R = dcRight_X
                lgpio.tx_pwm(h, LED, frequency, pwm_L)

                if button_A==0 & button_B==0:
                    continue
                elif button_A==1 & button_B==1:
                    pwm_L = 0
                    pwm_R = 0
                    lgpio.tx_pwm(h, LED, frequency, pwm_L)
                    break
            
            
            #lgpio.tx_pwm(h, in1_pin, frequency, pwm_L)
            #lgpio.tx_pwm(h, in2_pin, frequency, pwm_R)


    
