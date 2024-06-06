import os
import importlib.util

MY_API_TOKEN = "123"
RECORDING_TIMER = 60 * 0.5
client_id = "123"
client_secret = "123"

EEG_FILE_PATH = "../experiments/k/like-muse_radio.csv"

EXPERIMENT_DIR = os.path.dirname(EEG_FILE_PATH)
CALIBRATION_FILE = os.path.join(EXPERIMENT_DIR, "calibration.py")

if os.path.exists(CALIBRATION_FILE):
    spec = importlib.util.spec_from_file_location("calibration", CALIBRATION_FILE)
    calibration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(calibration)
    PEAK_THRESHOLD = calibration.PEAK_THRESHOLD
    SIGNAL_THRESHOLD = calibration.SIGNAL_THRESHOLD
else:
    PEAK_THRESHOLD = 4
    SIGNAL_THRESHOLD = 3

