from idun_guardian_sdk import GuardianClient, FileTypes
import config

class GuardianClientHandler:
    def __init__(self, data_handler):
        self.client = GuardianClient(api_token=config.MY_API_TOKEN, address="801C1CDF-94B2-33EB-A976-E8B415D718D6")
        self.data_handler = data_handler

    async def start(self):
        self.client.subscribe_live_insights(raw_eeg=True, filtered_eeg=True, handler=self.data_handler.handle_output)
        await self.client.start_recording(recording_timer=config.RECORDING_TIMER)
        rec_id = self.client.get_recording_id()
        print("RecordingId", rec_id)
        self.client.update_recording_tags(recording_id=rec_id, tags=["tag1", "tag2"])
        self.client.update_recording_display_name(recording_id=rec_id, display_name="todays_recordings")
        self.client.download_file(recording_id=rec_id, file_type=FileTypes.EEG)
        #self.client.generate_and_download_sleep_report(recording_id=rec_id)
        #self.client.generate_and_download_daytime_report(recording_id=rec_id)
