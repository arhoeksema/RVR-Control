import lgpio
import time

in1_pin = 13
frequency = 5000
h = lgpio.gpiochip_open(0)

try:
    while True:
        lgpio.tx_pwm(h, in1_pin, frequency, 63.168)
        time.sleep(.02)
        
except KeyboardInterrupt:
    #Set both signals to low
    lgpio.tx_pwm(h, in1_pin, frequency, 0)
    lgpio.gpiochip_close(h)
