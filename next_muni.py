import requests
import json
import datetime as dt
import pandas as pd


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


def monitor_muni(stop_id, api_token: str, operator_id: str):

    url = f'http://api.511.org/transit/StopMonitoring?api_key={api_token}&agency={operator_id}&stopCode={stop_id}'
    response = requests.get(url)
    dictionary_response = json.loads(response.content)
    my_predictions = return_relevant_metrics(
        predictions=dictionary_response['ServiceDelivery']['StopMonitoringDelivery']['MonitoredStopVisit']
    )

    return my_predictions


if __name__ == '__main__':
    from my_secrets import token

    bus_stop_id = '13328'
    my_operator_id = 'SF'

    a = monitor_muni(
        stop_id=bus_stop_id,
        operator_id=my_operator_id,
        api_token=token
    )

    print(a)
    print()
