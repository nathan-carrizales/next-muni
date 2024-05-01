import tkinter as tk
import datetime
from my_secrets import token as token_key
from next_muni import monitor_muni
import threading
from play_sound import play_my_sound


MINUTES_AWAY_ALERT = 10
MINUTES = 2
WIDTH = 1500
HEIGHT = 800
FONTSIZE = 44
FONTTYPE = 'Courier'
FOREGROUND = 'Yellow'
BACKGROUND = 'Black'
TKINTER_TITLE = 'NextMuni'


def make_api_requests_and_update_console(tk_label_obj, bus_stop: str, operator: str, token_id):

    pred_dict = monitor_muni(
        stop_id=bus_stop,
        operator_id=operator,
        api_token=token_id
    )

    stop_identifier = pred_dict[0]['StopPointRef']

    list_of_predictions = [
        f'\n {p["MinutesRemaining"]}-Minutes ({p["ArrivalTime (pretty)"]})' for _, p in pred_dict.items()
    ]

    now = (datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime('%l:%M%p').replace(" ", "")
    # now = (datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime('%X').replace(" ", "")
    tk_label_obj.configure(text=f'Time now: {now}. Stop ID: {stop_identifier}. \n {" ".join(list_of_predictions)}')
    tk_label_obj.after(
        1000*60*MINUTES,
        make_api_requests_and_update_console,
        tk_label_obj,
        bus_stop,
        operator,
        token_id
    )

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
    stop_id = '13327'
    my_operator_id = 'SF'

    start_monitoring_console(
        operator_id=my_operator_id,
        bustop_id=stop_id,
        token=token_key
    )
