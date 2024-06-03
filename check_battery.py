"""
Sample script for using the Guardian Earbud Client

Checking battery level
"""
import asyncio

from idun_guardian_sdk import GuardianClient


if __name__ == "__main__":
    # Get device address
    client = GuardianClient()
    client.address = asyncio.run(client.search_device())

    # start battery session
    asyncio.run(client.check_battery())
