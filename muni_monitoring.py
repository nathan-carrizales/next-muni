import tkinter as tk
import datetime
import threading
from play_sound import play_my_sound
import requests
import json
import datetime as dt
import pandas as pd
from my_secrets import token as token_key


STOP_REFERENCE = {
    '13327': '18th & Danvers (Mission)',
    '13328': '18th & Danvers (Haight)'
}

MINUTES_AWAY_ALERT = 10
MINUTES = 2
WIDTH = 2000
HEIGHT = 1000
FONTSIZE = 44
FONTTYPE = 'Courier'
FOREGROUND = 'Yellow'
BACKGROUND = 'Black'
TKINTER_TITLE = 'NextMuni'


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


def make_api_requests_and_update_console(tk_label_obj, bus_stop: str, operator: str, token_id):
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

    tk_label_obj.configure(text=my_text)
    tk_label_obj.after(
        1000*60*MINUTES,
        make_api_requests_and_update_console,
        tk_label_obj,
        bus_stop,
        operator,
        token_id
    )

    if pred_dict:
        if pred_dict[0]['MinutesRemaining'] <= MINUTES_AWAY_ALERT:
            x = threading.Thread(target=play_my_sound)
            x.start()

    return None


def start_monitoring_console(operator_id: str, bustop_id: str, token: str):

    root = tk.Tk()
    root.title(TKINTER_TITLE)
    root.geometry(f"{WIDTH}x{HEIGHT}")

    clock = tk.Label(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND, fg=FOREGROUND, font=(FONTTYPE, FONTSIZE))
    clock.pack()

    make_api_requests_and_update_console(tk_label_obj=clock, operator=operator_id, bus_stop=bustop_id, token_id=token)

    root.mainloop()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Just an example",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--id', default=None)  # option that takes a value
    args = vars(parser.parse_args())

    if args['id']:
        stop_id = str(args['id'])
        print(f'stop ID is "{stop_id}"')
    else:
        stop_id = '13327'

    my_operator_id = 'SF'

    start_monitoring_console(
        operator_id=my_operator_id,
        bustop_id=stop_id,
        token=token_key
    )
