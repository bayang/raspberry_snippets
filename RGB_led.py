# -*- coding:utf-8 -*-

"""usage:
setColor([red_value, green_value, blue_value])
0 < values < 255
and
fade_in_out(0.02)
"""

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

red = 17
green = 27
blue = 18

GPIO.setup(red, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

RED = GPIO.PWM(red, 100)
GREEN = GPIO.PWM(green, 100)
BLUE = GPIO.PWM(blue, 100)

RED.start(0)
GREEN.start(0)
BLUE.start(0)


def setColor(rgb=[]):
    rgb = [(x/255.0)*100 for x in rgb]
    RED.ChangeDutyCycle(rgb[0])
    GREEN.ChangeDutyCycle(rgb[1])
    BLUE.ChangeDutyCycle(rgb[2])

YELLOW = [255, 255, 0]
CYAN = [0, 255, 255]
MAGENTA = [255, 0, 255]


def fade_in_out(delay):
    # RED_INCREASING = True
    # GREEN_INCREASING = True
    # BLUE_INCREASING = True
    INCREASING = [True, True, True]  # tell if R, G, B are increasing
    red = 0
    green = 0
    blue = 0

    while True:
        setColor([red, green, blue])

        if all(INCREASING):
            red += 1
            sleep(delay)
            if red == 255:
                INCREASING[0] = False
        if INCREASING[1] and INCREASING[2] and not INCREASING[0]:
            green += 1
            sleep(delay)
            if green == 255:
                INCREASING[1] = False
        if INCREASING[2] and not INCREASING[0] and not INCREASING[1]:
            blue += 1
            sleep(delay)
            if blue == 255:
                INCREASING[2] = False
        if not any(INCREASING):
            red -= 1
            sleep(delay)
            if red == 1:
                INCREASING[0] = True
        if INCREASING[0] and not INCREASING[2] and not INCREASING[1]:
            green -= 1
            sleep(delay)
            if green == 1:
                INCREASING[1] = True
        if INCREASING[1] and INCREASING[0] and not INCREASING[2]:
            blue -= 1
            sleep(delay)
            if blue == 1:
                INCREASING[2] = True
