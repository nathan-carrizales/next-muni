import datetime
import requests
import json
import datetime as dt
import pandas as pd


STOP_REFERENCE = {
    '13327': '18th & Danvers (Haight)',
    '13328': '18th & Danvers (Mission)'
}


def monitor_muni(stop_id, api_token: str, operator_id: str):

    def return_relevant_metrics(predictions: list):
        dict_predictions = {}
        for i in predictions:
            expected_arrival_time = i['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']
            latitude = i['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
            longitude = i['MonitoredVehicleJourney']['VehicleLocation']['Longitude']

            n = predictions.index(i)
            arrival_time = (pd.to_datetime(expected_arrival_time) - dt.timedelta(hours=7))
            arrival_time_pretty = arrival_time.strftime('%l:%M%p').replace(" ", "")
            time_now = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)
            minutes = int((arrival_time - time_now).total_seconds() / 60)

            dict_predictions[n] = {}
            dict_predictions[n]['MinutesRemaining'] = minutes
            dict_predictions[n]['Time'] = ''
            dict_predictions[n]['Longitude'] = latitude
            dict_predictions[n]['Latitude'] = longitude
            dict_predictions[n]['ArrivalTime (pretty)'] = arrival_time_pretty
            dict_predictions[n]['ArrivalTime'] = arrival_time
            dict_predictions[n]['StopPointRef'] = i['MonitoredVehicleJourney']['MonitoredCall']['StopPointRef']

        return dict_predictions

    url = f'http://api.511.org/transit/StopMonitoring?api_key={api_token}&agency={operator_id}&stopCode={stop_id}'
    response = requests.get(url)
    dictionary_response = json.loads(response.content)

    try:
        my_predictions = return_relevant_metrics(
            predictions=dictionary_response['ServiceDelivery']['StopMonitoringDelivery']['MonitoredStopVisit']
        )
    except Exception as E:
        print('could not get predictions')
        print(E)
        my_predictions = list()

    return my_predictions


def get_bus_times_for_mission_and_haight(operator, token_id):

    mission_text = get_bus_times_in_text_for_bus_stop(operator, '13327', token_id)
    haight_text = get_bus_times_in_text_for_bus_stop(operator, '13328', token_id)

    return mission_text + '\n \n' + haight_text


def get_bus_times_in_text_for_bus_stop(operator, bus_stop, token_id):

    stop_identifier = STOP_REFERENCE[bus_stop]
    pred_dict = monitor_muni(
        stop_id=bus_stop,
        operator_id=operator,
        api_token=token_id
    )
    now = (datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime('%l:%M%p').replace(" ", "")

    if pred_dict:
        list_of_predictions = [
            f'\n {p["MinutesRemaining"]}-Minutes ({p["ArrivalTime (pretty)"]})' for _, p in pred_dict.items()
        ]
        my_text = f'Time now: {now}. Stop ID: {stop_identifier}. \n {" ".join(list_of_predictions)}'
    else:
        my_text = f'Time now: {now}. Stop ID: {stop_identifier}. \n \n No times available...'

    return my_text


if __name__ == '__main__':
    from generic_tkinter import start_monitoring_console
    from my_secrets import token as token_key
    my_operator_id = 'SF'

    args = {
        'operator': my_operator_id,
        'token_id': token_key
    }

    # text = get_bus_times_for_mission_and_haight(**args)

    start_monitoring_console(
        function_for_getting_text=get_bus_times_for_mission_and_haight,
        function_arguments=args
    )
