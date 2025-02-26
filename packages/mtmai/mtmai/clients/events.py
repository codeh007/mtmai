import asyncio
import datetime
import json
from typing import Any, Dict, List, Optional, TypedDict

import grpc
from connecpy.context import ClientContext
from google.protobuf import timestamp_pb2
from mtmai.loader import ClientConfig
from mtmai.mtlibs.hatchet_utils import tenacity_retry
from mtmai.mtmpb import events_connecpy
from mtmai.mtmpb.events_pb2 import (
    BulkPushEventRequest,
    Event,
    PushEventRequest,
    PutLogRequest,
    PutStreamEventRequest,
)

mtmclient_path_prefix = "/mtmapi"

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
    def __init__(self,
                 config: ClientConfig,
                 eventService: events_connecpy.AsyncEventsServiceClient):
        self.client_context = ClientContext(
            headers={
                "Authorization": f"Bearer {config.token}",
                "X-Tid": config.tenant_id,
            }
        )
        self.namespace = config.namespace
        self.eventService = eventService

    async def async_push(
        self, event_key, payload, options: Optional[PushEventOptions] = None
    ) -> Event:
        return await asyncio.to_thread(
            self.push, event_key=event_key, payload=payload, options=options
        )

    async def async_bulk_push(
        self,
        events: List[BulkPushEventWithMetadata],
        options: Optional[BulkPushEventOptions] = None,
    ) -> List[Event]:
        return await asyncio.to_thread(self.bulk_push, events=events, options=options)

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
            # return self.client.Push(request, metadata=get_metadata(self.token))
            return await self.eventService.Push(
                ctx=self.client_context,
                request=request,
                server_path_prefix=mtmclient_path_prefix,
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
                server_path_prefix=mtmclient_path_prefix,
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
                server_path_prefix=mtmclient_path_prefix,
            )

        except Exception as e:
            raise ValueError(f"Error logging: {str(e)}")

    async def stream(self, data: str | bytes, step_run_id: str):
        try:
            if isinstance(data, str):
                data_bytes = data.encode("utf-8")
            elif isinstance(data, bytes):
                data_bytes = data
            else:
                raise ValueError("Invalid data type. Expected str, bytes, or file.")

            request = PutStreamEventRequest(
                stepRunId=step_run_id,
                createdAt=proto_timestamp_now(),
                message=data_bytes,
            )
            await self.eventService.PutStreamEvent(
                ctx=self.client_context,
                server_path_prefix=mtmclient_path_prefix,
                request=request,
            )
        except Exception as e:
            raise ValueError(f"Error putting stream event: {str(e)}")
