# FHGR Neuroscience Hackathon
A hackathon project to use a realtime feed of in-ear EEG data from IDUN Guardian to analyze emotional state and control
Spotify with it. If positive emotions are detected, the current song will be added into a playlist.

Your can either stream data from a connected device or analyze existing files (no device required). 
If you stream data, the recording will save the file in the project directory.

For settings, there is a config file.

## Config File
- MY_API_TOKEN: API token for IDUN Guardian
- ADDRESS: IDUN device address
- RECORDING_TIMER: How long a recording lasts if data is streamed
- CLIENT_ID: Spotify API client id
- CLIENT_SECRET: Spotify API client secret
- EEG_FILE_PATH: File path to an eeg file you want to analyze (leave empty for data streaming)
- PEAK_THRESHOLD and SIGNAL_THRESHOLD: Calibration for interpretation functions which generates signals
  - This is very individual
  - If you analyze a given eeg file, the calibration will be loaded automatically (if one is provided in the folder)

## How to Run
- Add settings into config.py file
- If there is an EEG file set in the config file, it will be analyzed - so no stream will be started and no IDUN device is required
- If there is no EEG file given, a realtime feed will start (for RECORDING_TIMER seconds)
  - Remember to calibrate for yourself using the config file (this needs time)
    - Play with the signals threshold and see how many signals get generated while listening to music you like or dislike
      - You want many signals for your favorite music and few signals for music you don't like
  - IDUN Guardian needs to be connected
    - API key and address are set in config file
  - After a while the streaming starts
    - Realtime frequencies are shown as plots
- The Spotify logic is implemented but deactivated in data_handler.py
  - Instead, a log message will appear
- In either execution way, you will see log outputs of signals and triggers
  - **A signal is a detected positive emotion**
  - **If enough signals have occurred, a trigger will be created**

## Reproduce Experiments
- There is a folder of one test subject in the experiments folder
  - If any of these files are set in the config file, you can see how many signals are generated and if there was a trigger
  - The file names are either a song or an artist + information if the subject likes or dislikes the song
    - We promise we didn't cheat :)

## Add New Experiments
- Use streaming function and create some files and move them into a new experiment folder
- Use them to calibrate

## Implementation Details
- Stream EEG data or use recorded data
- Periodic processor for streaming which runs every three seconds (and takes a look at last three seconds)
- Modular interpretation functions
  - Peak detection (individual)
- Signal thresholds to generate trigger
- If trigger -> add current song to defined playlist

### Classes
- GuardianClientHandler
  - Handles connection to IDUN device
  - Manages recordings
- DataHandler
  - Receives data from IDUN device
  - Processes data in intervals
  - Processes existing files
- FFTProcessor
  - Generate FFT data from eeg data
  - Interpret the FFT data
  - Create more interpretation functions if you like
- SpotifyClient
  - Implements the logic for Spotify API

## Future Work
- Since the detection function is modular, any type of detection logic can be implemented and used
  - ML would be interesting, so that calibration becomes obsolete
