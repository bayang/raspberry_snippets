#!/usr/bin/env python3
# coding : utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import RPi.GPIO as GPIO
from time import sleep
import atexit
from threading import Thread


@atexit.register
def cleanup():
    GPIO.cleanup()


def PromptColor():
    chosenColor = colorchooser.askcolor(initialcolor='#00ff00',
                                        title="Pick a color")
    RED, GREEN, BLUE = [abs(int(x)) for x in chosenColor[0]]
    app.red_value.set(RED)
    app.green_value.set(GREEN)
    app.blue_value.set(BLUE)
    print(chosenColor[0])
    print(RED, GREEN, BLUE)


def setColor(rgb):
    """
    from :
    https://github.com/geerlingguy/raspberry-pi-dramble/blob/dfe8b763513566e664506ee06378b261673ab831/playbooks/roles/leds/templates/fade.j2
    """
    # rgb = [app.red_value.get(), app.green_value.get(), app.blue_value.get()]
    rgb = [(x/255.0)*100 for x in rgb]
    app.RED_LED.ChangeDutyCycle(rgb[0])
    app.GREEN_LED.ChangeDutyCycle(rgb[1])
    app.BLUE_LED.ChangeDutyCycle(rgb[2])
    print(rgb)


def fade_in_out(delay=0.05):
    """
    usage : fade_in_out(delay)
    press ctrl-C to stop it, it runs forever
    """
    INCREASING = "111"  # one digit for each component of the rgb led,1=ascending
    red = 0
    green = 0
    blue = 0

    if app.CYCLING.get() !=1:
        while True:
            setColor([red, green, blue])

            if INCREASING == "111":
                red += 1
                sleep(delay)
                if red >= 255:
                    INCREASING = "011"
            elif INCREASING == "011":
                green += 1
                sleep(delay)
                if green >= 255:
                    INCREASING = "001"
            elif INCREASING == "001":
                blue += 1
                sleep(delay)
                if blue >= 255:
                    INCREASING = "000"
            elif INCREASING == "000":
                red -= 1
                sleep(delay)
                if red <= 1:
                    INCREASING = "100"
            elif INCREASING == "100":
                green -= 1
                sleep(delay)
                if green <= 1:
                    INCREASING = "110"
            elif INCREASING == "110":
                blue -= 1
                sleep(delay)
                if blue <= 1:
                    INCREASING = "111"
    else:
        break


def thread_fade_in_out():
    fade_thread = Thread(target=fade_in_out)
    fade_thread.start()


class TkLedApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Controlling an RGB led")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.red_value = tk.IntVar()
        self.red_value.set(0)
        self.green_value = tk.IntVar()
        self.green_value.set(0)
        self.blue_value = tk.IntVar()
        self.blue_value.set(0)

        self.CYCLING = tk.IntVar()
        self.CYCLING.set(0)

        self.frames = {}

        frame = LedMainPage(container, self)

        self.frames[LedMainPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.setup()

        self.show_frame(LedMainPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def setup(self):

        GPIO.setmode(GPIO.BCM)

        red_pin = 17
        green_pin = 27
        blue_pin = 18

        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)

        self.RED_LED = GPIO.PWM(red_pin, 100)
        self.GREEN_LED = GPIO.PWM(green_pin, 100)
        self.BLUE_LED = GPIO.PWM(blue_pin, 100)

        self.RED_LED.start(0)
        self.GREEN_LED.start(0)
        self.BLUE_LED.start(0)


class LedMainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text="Main Page")
        self.label.pack(pady=10, padx=10)
        self.chose_color_button = ttk.Button(self, text="Choose a color",
                                              command=PromptColor)
        self.chose_color_button.pack()
        self.set_color_button = ttk.Button(self, text="Apply color",
            command=lambda: setColor([app.red_value.get(), app.green_value.get(), app.blue_value.get()]))
        self.set_color_button.pack()
        self.red_label = ttk.Label(self, text="Value you chose for red :")
        self.red_label.pack(pady=10, padx=10)
        self.red_value_label = ttk.Label(self, textvariable=controller.red_value)
        self.red_value_label.pack(pady=10, padx=10)
        self.green_label = ttk.Label(self, text="Value you chose for green :")
        self.green_label.pack(pady=10, padx=10)
        self.green_value_label = ttk.Label(self, textvariable=controller.green_value)
        self.green_value_label.pack(pady=10, padx=10)
        self.blue_label = ttk.Label(self, text="Value you chose for blue :")
        self.blue_label.pack(pady=10, padx=10)
        self.blue_value_label = ttk.Label(self, textvariable=controller.blue_value)
        self.blue_value_label.pack(pady=10, padx=10)
        self.cycle_button = ttk.Button(self, text="Start",
                                  command=self.toggle_fade_in_out)
        self.cycle_button.pack()
        self.off_button = ttk.Button(self, text="Turn off the led",
            command=lambda: setColor([0, 0, 0]))
        self.off_button.pack()

    def toggle_fade_in_out(self):
        if app.CYCLING.get() == 0:
            self.cycle_button.config(text='Stop')
            thread_fade_in_out()
            app.CYCLING.set(1)

        elif app.CYCLING.get() == 1:
            self.cycle_button.config(text='Start')
            thread_fade_in_out()
            app.CYCLING.set(0)

app = TkLedApp()
app.geometry("640x480")
app.mainloop()
