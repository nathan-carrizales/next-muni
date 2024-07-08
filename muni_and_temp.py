from s import get_temperature_and_humidity
from muni_monitoring import get_bus_times_for_mission_and_haight


def get_temp_and_muni(operator, token_id, foobar):

    text_temperature = get_temperature_and_humidity(foobar)
    text_from_muni = get_bus_times_for_mission_and_haight(operator, token_id)
    return text_temperature + '\n ' + text_from_muni


if __name__ == '__main__':
    from my_secrets import token as token_key
    from generic_tkinter import start_monitoring_console

    my_operator_id = 'SF'

    args = {
        'operator': my_operator_id,
        'token_id': token_key,
        'foobar': 'baz'
    }

    start_monitoring_console(
        function_for_getting_text=get_temp_and_muni,
        function_arguments=args
    )