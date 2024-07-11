import datetime
import numpy as np


def get_multi_temp_and_humidity_from_sensor(outdoor_sensor, indoor_sensor, outdoor_label, indoor_label):

    _, _, outdoor_data_text = get_temp_and_humidity_from_sensor(outdoor_sensor, outdoor_label)

    _, _, indoor_data_text = get_temp_and_humidity_from_sensor(indoor_sensor, indoor_label)

    return outdoor_data_text + '\t' + indoor_data_text + ' (Temp, Humid)'


def get_temp_and_humidity_from_sensor(adafruit_sensor, label):

    try:
        temperature_c = adafruit_sensor.temperature
        temperature_f = int(temperature_c * (9 / 5) + 32, 2)
        temp_sign = '°'
    except Exception:
        temperature_f = '-'
        temp_sign = ''

    try:
        humidity = adafruit_sensor.humidity
        humidity_sign = '%'
    except Exception:
        humidity = '-'
        humidity_sign = ''

    text = f'{temperature_f}{temp_sign}, {humidity}{humidity_sign}.'

    text = label + ': ' + text if label else text

    return temperature_f, humidity, text


if __name__ == '__main__':
    import board
    from generic_tkinter import start_monitoring_console
    import adafruit_dht

    args = {
        'outdoor_sensor': adafruit_dht.DHT11(board.D18),
        'indoor_sensor': adafruit_dht.DHT11(board.D4),
        'outdoor_label': 'Outdoor',
        'indoor_label': 'Indoor'
    }

    start_monitoring_console(
        function_for_getting_text=get_multi_temp_and_humidity_from_sensor,
        function_arguments=args
    )
