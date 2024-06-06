# FHGR Neuroscience Hackathon
A hackathon project to use a realtime feed of in-ear EEG data from IDUN Guardian to analyze emotional state and control Spotify with it.
If positive emotions are detected, the current song will be added into a playlist.

## Implementation
- Stream EEG data or use recorded data
- Periodic processor for streaming which runs every three seconds
- Modular interpretation functions
  - Peak detection (individual)
- Signal thresholds to generate trigger
- If trigger -> add current song to defined playlist

## How to Run
- Add settings into config.py file
- If there is an EEG file set in the config file, it will be analyzed - so no stream will be started and no IDUN device is required
- If not, a realtime feed will start
  - Remember to calibrate for yourself using the config file
    - This needs time
    - Play with the signals threshold and see how many signals get generated while listening to music you like or dislike
      - You want many signals for your favorite music and few signals for music you don't like
  - IDUN Guardian needs to be connected
    - Address is set in guardian_client.py
    - API key is set in config file
  - After a while the streaming starts
    - Realtime frequencies are shown
  - Recording time is configured in config file
    - Standard is 30sec
- The Spotify logic is implemented but deactivated in data_handler.py
  - Instead, a log message will appear
- In either execution way, you will see log outputs of signals and triggers
  - A signal is a detected positive emotion
  - If enough signals have occurred, a trigger will be created

## Reproduce Experiments
- There is a folder of one test subject in the experiments folder
  - If any of these files are set in the config file, you can see how many signal are generated and if there was a trigger
  - The file names are either a song or an artist + information if the subject likes or dislikes the song
    - We promise we didn't cheat :)

## Add New Experiments
- Use streaming function and create some files and move them into a new experiment folder
- Use them to calibrate

## Future Work
- Since the detection function is modular, any type of detection logic can be implemented and used
  - ML would be interesting, so that calibration becomes obsolete
