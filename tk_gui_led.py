#!/usr/bin/env python3
# coding : utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser


def PromptColor():
    chosenColor = colorchooser.askcolor(initialcolor='#00ff00',
                                        title="Pick a color")
    RED, GREEN, BLUE = [abs(int(x)) for x in chosenColor[0]]
    app.red_value.set(RED)
    app.green_value.set(GREEN)
    app.blue_value.set(BLUE)
    print(chosenColor[0])
    print(RED, GREEN, BLUE)


def setColor():
    """
    from :
    https://github.com/geerlingguy/raspberry-pi-dramble/blob/dfe8b763513566e664506ee06378b261673ab831/playbooks/roles/leds/templates/fade.j2
    """
    rgb = [app.red_value.get(), app.green_value.get(), app.blue_value.get()]
    rgb = [(x/255.0)*100 for x in rgb]
    app.RED_LED.ChangeDutyCycle(rgb[0])
    app.GREEN_LED.ChangeDutyCycle(rgb[1])
    app.BLUE_LED.ChangeDutyCycle(rgb[2])
    print(rgb)


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
        GPIO.cleanup()
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
        label = ttk.Label(self, text="Main Page")
        label.pack(pady=10, padx=10)
        chose_color_button = ttk.Button(self, text="Choose a color",
                                              command=PromptColor)
        chose_color_button.pack()
        set_color_button = ttk.Button(self, text="Apply color",
                                            command=setColor)
        set_color_button.pack()
        red_label = ttk.Label(self, text="Value you chose for red :")
        red_label.pack(pady=10, padx=10)
        red_value_label = ttk.Label(self, textvariable=controller.red_value)
        red_value_label.pack(pady=10, padx=10)
        green_label = ttk.Label(self, text="Value you chose for green :")
        green_label.pack(pady=10, padx=10)
        green_value_label = ttk.Label(self, textvariable=controller.green_value)
        green_value_label.pack(pady=10, padx=10)
        blue_label = ttk.Label(self, text="Value you chose for blue :")
        blue_label.pack(pady=10, padx=10)
        blue_value_label = ttk.Label(self, textvariable=controller.blue_value)
        blue_value_label.pack(pady=10, padx=10)


app = TkLedApp()
app.geometry("640x480")
app.mainloop()
