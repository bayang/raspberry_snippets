These are only some snippets I use to play with a RGB led on my raspberry pi. The pins numbers are hardcoded.


`RGB_led.py` contains some functions, one to choose a color and light up the led.
The other one makes the led fade in and out in a never-ending loop cycling through all the colors.
These functions can be used through the CLI.

The `tk_gui_led.py` is a tkinter gui used to play with the functions.
You can run `python tk_gui_led.py`

No external dependencies required except `tkinter` and `Rpi.GPIO`. Both are usually available on a Raspberry Pi.
