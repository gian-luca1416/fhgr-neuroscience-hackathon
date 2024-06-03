"""
Sample script for using the Guardian Earbud Client

Full example of recording data, generating reports and downloading the files
"""
import asyncio

from idun_guardian_sdk import GuardianClient, FileTypes


my_api_token = ""
my_device_id = ""
RECORDING_TIMER = 60 * 15  # 15 min


def print_data(data):
    print(data.message)


if __name__ == "__main__":
    client = GuardianClient(api_token=my_api_token, address="801C1CDF-94B2-33EB-A976-E8B415D718D6")
    #client.address = asyncio.run(client.search_device())
    client.address = "801C1CDF-94B2-33EB-A976-E8B415D718D6"

    client.subscribe_live_insights(raw_eeg=True, filtered_eeg=True, handler=print_data)
    client.subscribe_realtime_predictions(fft=True, jaw_clench=False, handler=print_data)

    asyncio.run(client.start_recording(recording_timer=RECORDING_TIMER))
    rec_id = client.get_recording_id()

    #client.end_recording(rec_id)

    print("RecordingId", rec_id)
    client.update_recording_tags(recording_id=rec_id, tags=["tag1", "tag2"])
    client.update_recording_display_name(recording_id=rec_id, display_name="todays_recordings")
    client.download_file(recording_id=rec_id, file_type=FileTypes.EEG)
    client.generate_and_download_sleep_report(recording_id=rec_id)
    client.generate_and_download_daytime_report(recording_id=rec_id)
