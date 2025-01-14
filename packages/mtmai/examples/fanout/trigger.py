import asyncio
import base64
import json
import os

from dotenv import load_dotenv

from mtmaisdk import new_client
from mtmaisdk.clients.admin import TriggerWorkflowOptions
from mtmaisdk.clients.run_event_listener import StepRunEventType


async def main():
    load_dotenv()
    hatchet = new_client()

    hatchet.admin.run_workflow(
        "Parent",
        {"test": "test"},
        options={"additional_metadata": {"hello": "moon"}},
    )


if __name__ == "__main__":
    asyncio.run(main())
