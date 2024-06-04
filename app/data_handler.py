import time
from collections import deque
from fft_processor import FFTProcessor

class DataHandler:
    def __init__(self):
        self.data_buffer = []
        self.fft_processor = FFTProcessor()
        self.recent_high_results = deque(maxlen=10)

    def handle_output(self, data):
        self.data_buffer.extend(data.message["raw_eeg"])

    def process_data_in_intervals(self):
        if self.data_buffer:
            latest_timestamp = self.data_buffer[-1]['timestamp']
            threshold_timestamp = latest_timestamp - 3
            recent_data = [data for data in self.data_buffer if data['timestamp'] >= threshold_timestamp]
            if len(recent_data) > 1:
                fft_result = self.fft_processor.fft(recent_data)
                result_baby = self.fft_processor.interpret_fft_for_arousal(fft_result[0], fft_result[1], fft_result[2])
                return result_baby

    def periodic_processor(self):
        while True:
            time.sleep(3)
            result = self.process_data_in_intervals()
            current_time = time.time()

            if result == "High":
                self.recent_high_results.append(current_time)

            while self.recent_high_results and (current_time - self.recent_high_results[0] > 10):
                self.recent_high_results.popleft()

            if len(self.recent_high_results) >= 3:
                print("TRIGGER")
                self.recent_high_results.clear()
