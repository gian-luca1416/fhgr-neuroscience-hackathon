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
                if fft_result == False:
                    return False
                result = self.fft_processor.interpret_fft_for_arousal_2(fft_result[0], fft_result[1], fft_result[2])
                return result

    def periodic_processor(self):
        while True:
            time.sleep(3)
            result = self.process_data_in_intervals()
            current_time = time.time()

            if result:
                self.recent_high_results.append(current_time)

            while self.recent_high_results and (current_time - self.recent_high_results[0] > 10):
                self.recent_high_results.popleft()

            if len(self.recent_high_results) >= 3:
                print("TRIGGER")
                self.recent_high_results.clear()

    def process_file(self, file_path):
        trigger_times = []

        with open(file_path, 'r') as f:
            buffer = []
            for line in f:
                try:
                    timestamp, ch1 = map(float, line.strip().split(','))
                    buffer.append({'timestamp': timestamp, 'ch1': ch1})

                    if len(buffer) >= 700:
                        self.data_buffer.extend(buffer)
                        buffer = []

                        result = self.process_data_in_intervals()
                        current_time = timestamp

                        if result:
                            self.recent_high_results.append(current_time)

                        while self.recent_high_results and (current_time - self.recent_high_results[0] > 10):
                            self.recent_high_results.popleft()

                        if len(self.recent_high_results) >= 3:
                            trigger_times.append(current_time)
                            self.recent_high_results.clear()  # Clear after triggering to avoid continuous triggers

                except ValueError:
                    continue  # Skip lines that can't be parsed

        print("Trigger Timestamps:", len(trigger_times))
