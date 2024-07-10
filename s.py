import datetime
import board
import adafruit_dht
import numpy as np

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D18)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT11(board.D18, use_pulseio=False)


def get_temperature_and_humidity(foobar):
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = int(temperature_c * (9 / 5) + 32, 2)
        humidity = dhtDevice.humidity
        my_text = f'\n Temperature is {temperature_f} F. ' + f'Humidity is {humidity} %.'

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        my_text = '\n Error:' + str(error.args[0])

    return my_text


if __name__ == '__main__':
    from generic_tkinter import start_monitoring_console

    args = {
        'foobar': 'baz'
    }

    start_monitoring_console(
        function_for_getting_text=get_temperature_and_humidity,
        function_arguments=args
    )
