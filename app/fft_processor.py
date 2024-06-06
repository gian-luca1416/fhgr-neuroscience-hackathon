import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from filters import highpass_filter, lowpass_filter
import config


class FFTProcessor:
    def fft(self, eeg_data):
        ch1_data = [data["ch1"] for data in eeg_data]
        sampling_frequency = 250

        filtered_signal = highpass_filter(ch1_data, 3, sampling_frequency, 5)
        filtered_signal = lowpass_filter(filtered_signal, 100, sampling_frequency, 5)

        samples_to_skip = 1 * sampling_frequency
        filtered_signal_skipped = filtered_signal[samples_to_skip:]

        # Perform FFT
        if len(filtered_signal_skipped) < 1:
            return False
        fft_values = np.fft.fft(filtered_signal_skipped)
        fft_frequencies = np.fft.fftfreq(len(filtered_signal_skipped), d=1 / sampling_frequency)

        # Only keep the positive frequencies
        positive_freq_indices = np.where(fft_frequencies >= 0)
        fft_values = fft_values[positive_freq_indices]
        fft_frequencies = fft_frequencies[positive_freq_indices]

        if config.EEG_FILE_PATH != "":
            return fft_values, fft_frequencies, fft_values.mean()

        # Plot the results
        plt.figure(figsize=(12, 6))
        plt.plot(fft_frequencies, np.abs(fft_values))
        plt.title("FFT of EEG Data")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.xlim(0, 49)
        # plt.ylim(0, 2000)
        plt.show()

        return fft_values, fft_frequencies

    def interpret_fft_for_arousal(self, fft_values, fft_frequencies):
        # Define frequency bands
        alpha_band = (8, 13)
        beta_band = (14, 29)
        gamma_band = (30, 47)

        # Peak detection
        peaks, _ = find_peaks(np.abs(fft_values), height=0)
        peak_powers = np.abs(fft_values[peaks])

        # Define a threshold for peak prominence
        peak_threshold = (np.mean(peak_powers) + 2 * np.std(peak_powers) / config.PEAK_THRESHOLD)

        # Check if there are significant peaks in the beta and gamma bands
        significant_alpha_peaks = np.any(peak_powers[(fft_frequencies[peaks] >= alpha_band[0]) &
                                                     (fft_frequencies[peaks] <= alpha_band[1])] > peak_threshold)
        significant_beta_peaks = np.any(peak_powers[(fft_frequencies[peaks] >= beta_band[0]) &
                                                    (fft_frequencies[peaks] <= beta_band[1])] > peak_threshold)
        significant_gamma_peaks = np.any(peak_powers[(fft_frequencies[peaks] >= gamma_band[0]) &
                                                     (fft_frequencies[peaks] <= gamma_band[1])] > peak_threshold)

        if significant_alpha_peaks and significant_beta_peaks and significant_gamma_peaks:
            return True
        return False
