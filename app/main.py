import threading
import asyncio
from data_handler import DataHandler
from guardian_client import GuardianClientHandler

def main():
    data_handler = DataHandler()
    guardian_client_handler = GuardianClientHandler(data_handler)

    processing_thread = threading.Thread(target=data_handler.periodic_processor)
    processing_thread.daemon = True
    processing_thread.start()

    asyncio.run(guardian_client_handler.start())

if __name__ == "__main__":
    main()
