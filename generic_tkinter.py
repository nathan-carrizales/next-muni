import tkinter as tk
import requests
import json
import datetime as dt
import pandas as pd


STOP_REFERENCE = {
    '13327': '18th & Danvers (Haight)',
    '13328': '18th & Danvers (Mission)'
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


def update_console(tk_label_obj, my_function, my_arguments):

    my_text = my_function(**my_arguments)

    for var, val in my_arguments.items():
        c = f"{var}='{val}'"
        exec(c)

    my_variables = [i for i in my_arguments.keys()]

    tk_label_obj.configure(text=my_text)

    variables = ', '.join(my_variables)

    command = f"tk_label_obj.after(1000*60*{MINUTES}, update_console, tk_label_obj, my_function, {variables})"

    exec(command)

    return None


def start_monitoring_console(function_for_getting_text, function_arguments):

    root = tk.Tk()
    root.title(TKINTER_TITLE)
    root.geometry(f"{WIDTH}x{HEIGHT}")

    clock = tk.Label(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND, fg=FOREGROUND, font=(FONTTYPE, FONTSIZE))
    clock.pack()

    update_console(tk_label_obj=clock, my_function=function_for_getting_text, my_arguments=function_arguments)

    root.mainloop()


if __name__ == '__main__':

    # from library import function_that_gets_text
    def bus_times(variable1, variable2, variable3):
        return f'your variables are {variable1}, {variable2}, {variable3}'

    start_monitoring_console(
        function_for_getting_text=bus_times,
        function_arguments={'variable1': 1, 'variable2': 2, 'variable3': 3}
    )
