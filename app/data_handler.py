import time
from fft_processor import FFTProcessor
import spotify_client
import threading
import config


class DataHandler:
    trigger_count = 0
    threshold = config.SIGNAL_THRESHOLD
    lock = threading.Lock()

    def __init__(self):
        self.data_buffer = []
        self.fft_processor = FFTProcessor()
        self.sp = spotify_client.SpotifyClient()

    def handle_output(self, data):
        self.data_buffer.extend(data.message["raw_eeg"])

    def process_data_in_intervals(self, seconds):
        if self.data_buffer:
            latest_timestamp = self.data_buffer[-1]["timestamp"]
            threshold_timestamp = latest_timestamp - seconds
            recent_data = [data for data in self.data_buffer if data["timestamp"] >= threshold_timestamp]
            if len(recent_data) > 1:
                fft_result = self.fft_processor.fft(recent_data)
                if not fft_result:
                    return False
                result = self.fft_processor.interpret_fft_for_arousal(fft_result[0], fft_result[1])
                return result

    def periodic_processor(self):
        while True:
            # maybe more seconds here - time window we consider until decision is made
            time.sleep(3)
            result = self.process_data_in_intervals(3)

            if result:
                print("Signal")
                with DataHandler.lock:
                    DataHandler.trigger_count += 1
                    if DataHandler.trigger_count >= DataHandler.threshold:
                        print("SPOTIFY")
                        # only trigger if API key is defined
                        # self.sp.trigger()
                        DataHandler.trigger_count = 0

    def process_file(self, file_path):
        trigger_times = []

        with open(file_path, "r") as f:
            buffer = []
            for line in f:
                try:
                    timestamp, ch1 = map(float, line.strip().split(","))
                    buffer.append({"timestamp": timestamp, "ch1": ch1})

                    # there are ca. 750 events in 3 seconds (if we stream the data)
                    if len(buffer) >= 750:
                        self.data_buffer.extend(buffer)
                        buffer = []

                        result = self.process_data_in_intervals(3)
                        if result:
                            trigger_times.append("triggered")

                except ValueError:
                    continue

        print("Signals:", len(trigger_times))

        if len(trigger_times) >= DataHandler.threshold:
            print("SPOTIFY")
            # only trigger if API key is defined
            # self.sp.trigger()
