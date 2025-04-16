import datetime
import json
from typing import Any, Dict, List, Optional, TypedDict

from autogen_agentchat.base import TaskResult
from autogen_core import try_get_known_serializers_for_type
from autogen_core._serialization import SerializationRegistry
from connecpy.context import ClientContext
from fastapi.encoders import jsonable_encoder
from google.protobuf import message as pb_message
from google.protobuf import timestamp_pb2
from mtmai.clients.rest.models.chat_session_start_event import ChatSessionStartEvent
from mtmai.clients.rest.models.mt_task_result import MtTaskResult
from mtmai.context.ctx import get_step_run_id
from mtmai.core.config import settings
from mtmai.mtlibs.hatchet_utils import tenacity_retry
from mtmai.mtlibs.utils import get_type_name
from mtmai.mtmpb import agent_worker_pb2, events_connecpy
from mtmai.mtmpb.events_pb2 import (
    BulkPushEventRequest,
    Event,
    PushEventRequest,
    PutLogRequest,
    PutStreamEventRequest,
)
from pydantic import BaseModel


def proto_timestamp_now():
    t = datetime.datetime.now().timestamp()
    seconds = int(t)
    nanos = int(t % 1 * 1e9)

    return timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)


class PushEventOptions(TypedDict):
    additional_metadata: Dict[str, str] | None = None
    namespace: str | None = None


class BulkPushEventOptions(TypedDict):
    namespace: str | None = None


class BulkPushEventWithMetadata(TypedDict):
    key: str
    payload: Any
    additional_metadata: Optional[Dict[str, Any]]  # Optional metadata


class EventClient:
    def __init__(
        self,
        server_url: str,
        token: str,
        tenant_id: str | None = None,
        namespace: str | None = "",
    ):
        self.client_context = ClientContext(
            headers={
                "Authorization": f"Bearer {token}",
            }
        )
        self.namespace = namespace
        self.server_url = server_url
        self.eventsService = events_connecpy.AsyncEventsServiceClient(
            server_url,
            timeout=20,
        )
        self._serialization_registry = SerializationRegistry()
        self._serialization_registry.add_serializer(
            try_get_known_serializers_for_type(ChatSessionStartEvent)
        )

    @property
    def event_service(self):
        if hasattr(self, "_event_service"):
            return self._event_service
        self._event_service = events_connecpy.AsyncEventsServiceClient(
            self.server_url,
            timeout=20,
        )
        return self._event_service

    # @tenacity_retry
    # async def push(self, event_key, payload, options: PushEventOptions = None) -> Event:
    #     namespace = self.namespace

    #     if (
    #         options is not None
    #         and "namespace" in options
    #         and options["namespace"] is not None
    #     ):
    #         namespace = options["namespace"]
    #         del options["namespace"]

    #     namespaced_event_key = namespace + event_key

    #     meta = None if options is None else options["additional_metadata"]
    #     meta_bytes = None if meta is None else json.dumps(meta).encode("utf-8")

    #     payload_bytes = json.dumps(payload)

    #     request = PushEventRequest(
    #         key=namespaced_event_key,
    #         payload=payload_bytes,
    #         eventTimestamp=proto_timestamp_now(),
    #         additionalMetadata=meta_bytes,
    #     )

    #     return await self.event_service.Push(
    #         ctx=self.client_context,
    #         request=request,
    #         server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
    #     )

    @tenacity_retry
    async def bulk_push(
        self,
        events: List[BulkPushEventWithMetadata],
        options: BulkPushEventOptions = None,
    ) -> List[Event]:
        namespace = self.namespace

        if (
            options is not None
            and "namespace" in options
            and options["namespace"] is not None
        ):
            namespace = options["namespace"]
            del options["namespace"]

        bulk_events = []
        for event in events:
            event_key = namespace + event["key"]
            payload = event["payload"]

            try:
                meta = event.get("additional_metadata")
                meta_bytes = json.dumps(meta).encode("utf-8") if meta else None
            except Exception as e:
                raise ValueError(f"Error encoding meta: {e}")

            try:
                payload_bytes = json.dumps(payload).encode("utf-8")
            except json.UnicodeEncodeError as e:
                raise ValueError(f"Error encoding payload: {e}")

            request = PushEventRequest(
                key=event_key,
                payload=payload_bytes,
                eventTimestamp=proto_timestamp_now(),
                additionalMetadata=meta_bytes,
            )
            bulk_events.append(request)

        bulk_request = BulkPushEventRequest(events=bulk_events)

        response = await self.event_service.BulkPush(
            ctx=self.client_context,
            request=bulk_request,
            server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
        )
        return response.events

    async def log(self, message: str, step_run_id: str):
        request = PutLogRequest(
            stepRunId=step_run_id,
            createdAt=proto_timestamp_now(),
            message=message,
        )
        await self.event_service.PutLog(
            ctx=self.client_context,
            request=request,
            server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
        )

    async def emit(self, event: Any):
        step_run_id = get_step_run_id()
        json_bytes = None
        result_type = get_type_name(event)
        # if isinstance(event, str) or isinstance(event, bytes):
        #     await self.stream(event, step_run_id)
        obj_dict = {}
        if isinstance(event, BaseModel):
            obj_dict = event.model_dump()
        elif isinstance(event, TaskResult):
            # json_bytes = json.dumps(jsonable_encoder(event))
            # obj_dict = event.model_dump()
            messages = jsonable_encoder(event.messages)
            mt_result = MtTaskResult(
                messages=messages,
                stop_reason=event.stop_reason or "",
            )
            obj_dict = mt_result.model_dump()
        json_bytes = json.dumps(obj_dict)

        await self.stream(json_bytes, step_run_id=step_run_id)

    async def stream(self, data: str | bytes, step_run_id: str):
        if isinstance(data, str):
            data_bytes = data.encode("utf-8")
        elif isinstance(data, bytes):
            data_bytes = data
        elif isinstance(data, BaseModel):
            data_bytes = data.model_dump_json()
        elif isinstance(data, agent_worker_pb2.Message):
            data_bytes = data.SerializeToString()
        elif isinstance(data, pb_message.Message):
            data_bytes = data.SerializeToString()

        else:
            raise ValueError("(stream)未知数据类型")

        request = PutStreamEventRequest(
            stepRunId=step_run_id,
            createdAt=proto_timestamp_now(),
            message=data_bytes,
        )
        await self.event_service.PutStreamEvent(
            ctx=self.client_context,
            server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
            request=request,
        )
