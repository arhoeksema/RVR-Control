import math
import evdev
from evdev import InputDevice, categorize, ecodes, ff, list_devices

#dev = evdev.InputDevice('/dev/input/event6')
#dev = InputDevice(list_devices()[6])

class gamepad():

    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)
    axis_tol = 10*330.0

    def __init__(self, file = '/dev/input/event3'):
        self.power_on = True
        self.device_file = InputDevice(file)
        self.joystick_left_y = 0 # [1] values are mapped to [-1 ... 1]
        self.joystick_left_x = 0 # [2] values are mapped to [-1 ... 1]
        self.joystick_right_x = 0 # [3] values are mapped to [-1 ... 1]
        self.joystick_right_y = 0 # [4] values are mapped to [-1 ... 1]
        self.trigger_right = 0 # [5] values are mapped to [0 ... 1]
        self.trigger_left = 0 # [6] values are mapped to [0 ... 1]
        self.button_x = False # [7]
        self.button_y = False # [8]
        self.button_b = False # [9]
        self.button_a = False # [10]
        self.dpad_up = False # [11]
        self.dpad_down = False # [12]
        self.dpad_left = False # [13]
        self.dpad_right = False # [14]
        self.bump_left = False # [15]
        self.bump_right = False # [16]
        
    def read(self):
        a = self.joystick_left_y
        b = self.joystick_right_x
        c = self.button_a
        d = self.button_b
        e = self.button_x
        f = self.button_y
        return [a, b, c, d, e, f]
  

    async def read_gamepad_input(self): # asyncronus read-out of events
        max_abs_joystick_left_y = 0xFFFF/2
        uncertainty_joystick_left_y = 2500
        max_abs_joystick_right_x = 0xFFFF/2
        uncertainty_joystick_right_x = 2000
        max_trigger = 1023
    
        while True:
            async for event in self.device_file.async_read_loop():
                if event.type == ecodes.EV_ABS:
                    if event.code == ecodes.ABS_Y:
                        self.joystick_left_y = event.state / gamepad.MAX_JOY_VAL
                    elif event.code == ecodes.ABS_RX:
                        self.joystick_right_x = event.state / gamepad.MAX_JOY_VAL

                    #if not(self.power_on): #stop reading device when power_on = false
                     #   break
                    #print(str(event.type) + ' ' + str(event.code) + ' ' + str(event.value))
                     #if event.type == 3: # type is analog trigger or joystick
                        if event.type == evdev.ecodes.ABS_Y: # left joystick y-axis
                            self.joystick_left_y = event.state / gamepad.MAX_JOY_VAL
                            
                            if -event.value > uncertainty_joystick_left_y:
                                self.joystick_left_y = (-event.value - uncertainty_joystick_left_y) / (max_abs_joystick_left_y - uncertainty_joystick_left_y + 1)
                            elif -event.value < -uncertainty_joystick_left_y:
                                self.joystick_left_y = (-event.value + uncertainty_joystick_left_y) / (max_abs_joystick_left_y - uncertainty_joystick_left_y + 1)
                            else:
                                self.joystick_left_y = 0
                            
                        elif event.code == 'ABS_RX': # right joystick x-axis
                            if event.value > uncertainty_joystick_right_x:
                                self.joystick_right_x = (event.value - uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                            elif event.value < -uncertainty_joystick_right_x:
                                self.joystick_right_x = (event.value + uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                            else:
                                self.joystick_right_x = 0
                        elif event.code == 'ABS_RZ': # right trigger
                            self.trigger_right = event.value / max_trigger
                        elif event.code == 'ABS_Z': # left trigger
                            self.trigger_left = event.value / max_trigger
                        elif event.code == 16: # right trigger
                            if(event.value == -1):
                                self.dpad_left = True
                                self.dpad_right = False
                            elif(event.value == 1):
                                self.dpad_left = False
                                self.dpad_right = True
                            else:
                                self.dpad_left = False
                                self.dpad_right = False
                        elif event.code == 17: # left trigger
                            if(event.value == -1):
                                self.dpad_up = True
                                self.dpad_down = False
                            elif(event.value == 1):
                                self.dpad_up = False
                                self.dpad_down = True
                            else:
                                self.dpad_up = False
                                self.dpad_down = False
    
                    if (event.type == 1): # type is button
                        if event.code == 'BTN_SOUTH': # button "A" pressed ?
                            self.button_a =  True
                        if event.code == 'BTN_WEST': # button "X" pressed ?
                            self.button_x = True
                        if event.code == 'BTN_NORTH': # button "Y" pressed ?
                            self.button_y = True
                        if event.code == 'BTN_EAST': # button "B" pressed ?
                            self.button_b = True
                        if event.code == 'BTN_TR': # bumper "right" pressed ?
                            self.bump_right = True if event.value == 1 else False
                        if event.code == 'BTN_TL': # bumper "left" pressed ?
                            self.bump_left = True if event.value == 1 else False



if __name__ == '__main__':
    joy = gamepad()
    while True:
        print(joy.read())
