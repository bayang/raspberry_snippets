# -*- coding:utf-8 -*-

"""usage:
setColor([red_value, green_value, blue_value])
where 0 < values < 255
and
fade_in_out(delay)
for example :
fade_in_out(0.02)

inspired by : https://github.com/geerlingguy/raspberry-pi-dramble/blob/dfe8b763513566e664506ee06378b261673ab831/playbooks/roles/leds/templates/fade.j2
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


def setup():
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
    """
    from :
    https://github.com/geerlingguy/raspberry-pi-dramble/blob/dfe8b763513566e664506ee06378b261673ab831/playbooks/roles/leds/templates/fade.j2
    """
    rgb = [(x/255.0)*100 for x in rgb]
    RED.ChangeDutyCycle(rgb[0])
    GREEN.ChangeDutyCycle(rgb[1])
    BLUE.ChangeDutyCycle(rgb[2])

YELLOW = [255, 255, 0]
CYAN = [0, 255, 255]
MAGENTA = [255, 0, 255]
WHITE = [255, 255, 255]
OFF = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]


def fade_in_out(delay):
    """
    usage : fade_in_out(delay)
    press ctrl-C to stop it, it runs forever
    """
    INCREASING = "111"  # one digit for each component of the rgb led,1=ascending
    red = 0
    green = 0
    blue = 0

    while True:
        setColor([red, green, blue])

        if INCREASING == "111":
            red += 1
            sleep(delay)
            if red == 255:
                INCREASING = "011"
        if INCREASING == "011":
            green += 1
            sleep(delay)
            if green == 255:
                INCREASING == "001"
        if INCREASING == "001":
            blue += 1
            sleep(delay)
            if blue == 255:
                INCREASING = "000"
        if INCREASING == "000":
            red -= 1
            sleep(delay)
            if red == 1:
                INCREASING == "100"
        if INCREASING == "100":
            green -= 1
            sleep(delay)
            if green == 1:
                INCREASING == "110"
        if INCREASING == "110":
            blue -= 1
            sleep(delay)
            if blue == 1:
                INCREASING == "111"
