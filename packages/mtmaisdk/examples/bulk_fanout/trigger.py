import asyncio
import base64
import json
import os

from dotenv import load_dotenv

from mtmaisdk import new_client
from mtmaisdk.clients.admin import TriggerWorkflowOptions
from mtmaisdk.clients.rest.models.workflow_run import WorkflowRun
from mtmaisdk.clients.run_event_listener import StepRunEventType


async def main():
    load_dotenv()
    hatchet = new_client()

    workflowRuns: WorkflowRun = []

    event = hatchet.event.push(
        "parent:create", {"n": 999}, {"additional_metadata": {"no-dedupe": "world"}}
    )


if __name__ == "__main__":
    asyncio.run(main())
