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


def make_api_requests_and_update_console(foobar):
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        my_text = f'\n Temperature is {temperature_f} F.' + f'\n \n Humidity is {humidity} %.'

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        my_text = error.args[0]

    now = (datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime('%l:%M%p').replace(" ", "")

    my_text = f'Time: {now}' + my_text

    return my_text


if __name__ == '__main__':
    from generic_tkinter import start_monitoring_console

    args = {
        'foobar': 'baz'
    }

    start_monitoring_console(
        function_for_getting_text=make_api_requests_and_update_console,
        function_arguments=args
    )
