import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from filters import highpass_filter, lowpass_filter
import config

class FFTProcessor:
    def fft(self, eeg_data):
        # Extract channel data
        ch1_data = [data['ch1'] for data in eeg_data]

        sampling_frequency = 250  # Hz

        # Apply highpass filter
        filtered_signal = highpass_filter(ch1_data, 3, sampling_frequency, 5)
        filtered_signal = lowpass_filter(filtered_signal, 100, sampling_frequency, 5)
        # Calculate the number of samples to skip (5 seconds)
        samples_to_skip = 1 * sampling_frequency
        # Skipping the first 5 seconds of the filtered signal
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
        plt.title('FFT of EEG Data')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.xlim(0, sampling_frequency / 2)  # Display only positive frequencies
        plt.ylim(0, 2000)  # Adjust the y-axis limit as needed to focus on relevant amplitudes
        plt.show()

        return fft_values, fft_frequencies, fft_values.mean()

    def interpret_fft_for_arousal(self, fft_values, fft_frequencies, mean):
        # Define frequency bands
        beta_band = (13, 30)
        gamma_band = (30, 45)

        # Calculate the power in the beta and gamma bands
        beta_power = np.sum(np.abs(fft_values[(fft_frequencies >= beta_band[0]) & (fft_frequencies <= beta_band[1])]))
        gamma_power = np.sum(
            np.abs(fft_values[(fft_frequencies >= gamma_band[0]) & (fft_frequencies <= gamma_band[1])]))

        # Simple rule for arousal measurement
        total_power = beta_power + gamma_power

        #print("P: ", total_power)
        #print("M: ", mean.real)

        # Peak detection
        peaks, _ = find_peaks(np.abs(fft_values), height=0)  # You can adjust the height parameter as needed
        peak_powers = np.abs(fft_values[peaks])

        # Define a threshold for peak prominence
        peak_threshold = (np.mean(peak_powers) + 2 * np.std(peak_powers) / 1.5)

        # Check if there are significant peaks in the beta and gamma bands
        significant_beta_peaks = np.any(peak_powers[(fft_frequencies[peaks] >= beta_band[0]) &
                                                    (fft_frequencies[peaks] <= beta_band[1])] > peak_threshold)
        significant_gamma_peaks = np.any(peak_powers[(fft_frequencies[peaks] >= gamma_band[0]) &
                                                     (fft_frequencies[peaks] <= gamma_band[1])] > peak_threshold)

        if significant_beta_peaks or significant_gamma_peaks:
            return True
        return False

    def interpret_fft_for_arousal_2(self, fft_values, fft_frequencies, mean):
        # Define frequency bands
        alpha_band = (8, 13)
        beta_band = (14, 29)
        gamma_band = (30, 47)

        # Calculate the power in the beta and gamma bands
        alpha_power = np.sum(np.abs(fft_values[(fft_frequencies >= alpha_band[0]) & (fft_frequencies <= alpha_band[1])]))
        beta_power = np.sum(np.abs(fft_values[(fft_frequencies >= beta_band[0]) & (fft_frequencies <= beta_band[1])]))
        gamma_power = np.sum(np.abs(fft_values[(fft_frequencies >= gamma_band[0]) & (fft_frequencies <= gamma_band[1])]))

        # Simple rule for arousal measurement
        total_power = alpha_power + beta_power + gamma_power

        #print("P: ", total_power)
        #print("M: ", mean.real)

        # Peak detection
        peaks, _ = find_peaks(np.abs(fft_values), height=0)
        peak_powers = np.abs(fft_values[peaks])

        # Define a threshold for peak prominence
        peak_threshold = (np.mean(peak_powers) + 2 * np.std(peak_powers) / 4)

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
