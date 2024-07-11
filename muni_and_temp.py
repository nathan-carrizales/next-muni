from temperature import get_multi_temp_and_humidity_from_sensor
from muni_monitoring import get_bus_times_for_mission_and_haight


def get_temp_and_muni(operator, token_id, outdoor_sensor, indoor_sensor, outdoor_label, indoor_label):

    text_weather = get_multi_temp_and_humidity_from_sensor(
        outdoor_sensor,
        indoor_sensor,
        outdoor_label,
        indoor_label
    )

    text_from_muni = get_bus_times_for_mission_and_haight(
        operator,
        token_id
    )

    return text_weather + '\n \n' + text_from_muni


if __name__ == '__main__':
    from my_secrets import token as token_key
    import board
    from generic_tkinter import start_monitoring_console
    import adafruit_dht

    my_operator_id = 'SF'

    args = {
        'operator': my_operator_id,
        'token_id': token_key,
        'outdoor_sensor': adafruit_dht.DHT11(board.D18, use_pulseio=False),
        'indoor_sensor': adafruit_dht.DHT11(board.D4, use_pulseio=False),
        'outdoor_label': 'Outdoor',
        'indoor_label': 'Indoor'
    }

    start_monitoring_console(
        function_for_getting_text=get_temp_and_muni,
        function_arguments=args
    )
