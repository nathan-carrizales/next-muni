from playsound import playsound
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_PATH = BASE_DIR + '/blackbird.mp3'


def play_my_sound():
    playsound(SOUND_PATH)
    return None