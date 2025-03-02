import datetime
import json
from typing import Any, Dict, List, Optional, TypedDict

import grpc
from autogen_core import PROTOBUF_DATA_CONTENT_TYPE, try_get_known_serializers_for_type
from autogen_core._serialization import SerializationRegistry
from connecpy.context import ClientContext
from google.protobuf import any_pb2, timestamp_pb2
from google.protobuf import message as pb_message
from mtmai.core.config import settings
from mtmai.core.loader import ClientConfig
from mtmai.mtlibs.hatchet_utils import tenacity_retry
from mtmai.mtmpb import agent_worker_pb2, cloudevent_pb2, events_connecpy
from mtmai.mtmpb.events_pb2 import (
    BulkPushEventRequest,
    ChatSessionStartEvent,
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
        config: ClientConfig,
        eventService: events_connecpy.AsyncEventsServiceClient,
    ):
        self.client_context = ClientContext(
            headers={
                "Authorization": f"Bearer {config.token}",
                "X-Tid": config.tenant_id,
            }
        )
        self.namespace = config.namespace
        self.eventService = eventService
        self._serialization_registry = SerializationRegistry()
        self._serialization_registry.add_serializer(
            try_get_known_serializers_for_type(ChatSessionStartEvent)
        )

    @tenacity_retry
    async def push(self, event_key, payload, options: PushEventOptions = None) -> Event:
        namespace = self.namespace

        if (
            options is not None
            and "namespace" in options
            and options["namespace"] is not None
        ):
            namespace = options["namespace"]
            del options["namespace"]

        namespaced_event_key = namespace + event_key

        try:
            meta = None if options is None else options["additional_metadata"]
            meta_bytes = None if meta is None else json.dumps(meta).encode("utf-8")
        except Exception as e:
            raise ValueError(f"Error encoding meta: {e}")

        try:
            payload_bytes = json.dumps(payload).encode("utf-8")
        except json.UnicodeEncodeError as e:
            raise ValueError(f"Error encoding payload: {e}")

        request = PushEventRequest(
            key=namespaced_event_key,
            payload=payload_bytes,
            eventTimestamp=proto_timestamp_now(),
            additionalMetadata=meta_bytes,
        )

        try:
            return await self.eventService.Push(
                ctx=self.client_context,
                request=request,
                server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
            )
        except grpc.RpcError as e:
            raise ValueError(f"gRPC error: {e}")

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

        try:
            response = await self.eventService.BulkPush(
                ctx=self.client_context,
                request=bulk_request,
                server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
            )
            return response.events
        except grpc.RpcError as e:
            raise ValueError(f"gRPC error: {e}")

    async def log(self, message: str, step_run_id: str):
        try:
            request = PutLogRequest(
                stepRunId=step_run_id,
                createdAt=proto_timestamp_now(),
                message=message,
            )
            await self.eventService.PutLog(
                ctx=self.client_context,
                request=request,
                server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
            )

        except Exception as e:
            raise ValueError(f"Error logging: {str(e)}")

    async def stream(self, data: str | bytes, step_run_id: str):
        try:
            if isinstance(data, str):
                data_bytes = data.encode("utf-8")
            elif isinstance(data, bytes):
                data_bytes = data
            elif isinstance(data, BaseModel):
                data_bytes = data.model_dump_json().encode("utf-8")
            elif isinstance(data, ChatSessionStartEvent):
                result_type = self._serialization_registry.type_name(data)
                serialized_result = self._serialization_registry.serialize(
                    data,
                    type_name=result_type,
                    data_content_type=PROTOBUF_DATA_CONTENT_TYPE,
                )

                # serialized_message = self._serialization_registry.serialize(data)
                any_proto = any_pb2.Any()
                any_proto.ParseFromString(serialized_result)
                ce_message = cloudevent_pb2.CloudEvent(
                    # id=message_id,
                    spec_version="1.0",
                    # type=topic_id.type,
                    source="event_source",
                    # attributes=attributes,
                    proto_data=any_proto,
                )

                data_bytes = ce_message.SerializeToString()
            elif isinstance(data, agent_worker_pb2.Message):
                data_bytes = data.SerializeToString()
            elif isinstance(data, pb_message.Message):
                # data_bytes = data.model_dump_json().encode("utf-8")
                data_bytes = data.SerializeToString()

            else:
                raise ValueError("Invalid data type. Expected str, bytes, or file.")

            request = PutStreamEventRequest(
                stepRunId=step_run_id,
                createdAt=proto_timestamp_now(),
                message=data_bytes,
            )
            await self.eventService.PutStreamEvent(
                ctx=self.client_context,
                server_path_prefix=settings.GOMTM_API_PATH_PREFIX,
                request=request,
            )
        except Exception as e:
            raise ValueError(f"Error putting stream event: {str(e)}")
