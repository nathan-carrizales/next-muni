import time
import tkinter as tk
import datetime
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D18)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

MINUTES_AWAY_ALERT = 10
MINUTES = 2
WIDTH = 2000
HEIGHT = 1000
FONTSIZE = 44
FONTTYPE = 'Courier'
FOREGROUND = 'Yellow'
BACKGROUND = 'Black'
TKINTER_TITLE = 'NextMuni'


def make_api_requests_and_update_console(tk_label_obj):
    temperature_c = dhtDevice.temperature
    temperature_f = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity

    now = (datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime('%l:%M%p').replace(" ", "")

    my_text = f'Temperature is {temperature_f} F.' + f'\n \n Humidity is {humidity} %. \n \n Time is {now}'

    tk_label_obj.configure(text=my_text)
    tk_label_obj.after(
        1000*60*MINUTES,
        make_api_requests_and_update_console,
        tk_label_obj
    )

    return None


def start_monitoring_temperature():

    root = tk.Tk()
    root.title(TKINTER_TITLE)
    root.geometry(f"{WIDTH}x{HEIGHT}")

    clock = tk.Label(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND, fg=FOREGROUND, font=(FONTTYPE, FONTSIZE))
    clock.pack()

    make_api_requests_and_update_console(clock)

    root.mainloop()


start_monitoring_temperature()
