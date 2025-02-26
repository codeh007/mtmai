from __future__ import annotations

import asyncio
import inspect
import json
import logging
import signal
import uuid
import warnings
from asyncio import Future, Task
from collections import defaultdict
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    DefaultDict,
    Dict,
    List,
    Literal,
    Mapping,
    ParamSpec,
    Sequence,
    Set,
    Type,
    TypeVar,
    cast,
)

from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import (
    HandoffMessage,
    MultiModalMessage,
    StopMessage,
    TextMessage,
    ToolCallExecutionEvent,
    ToolCallRequestEvent,
)
from autogen_core import (
    JSON_DATA_CONTENT_TYPE,
    PROTOBUF_DATA_CONTENT_TYPE,
    Agent,
    AgentId,
    AgentInstantiationContext,
    AgentMetadata,
    AgentRuntime,
    AgentType,
    CancellationToken,
    MessageContext,
    MessageHandlerContext,
    MessageSerializer,
    SingleThreadedAgentRuntime,
    Subscription,
    TopicId,
)
from autogen_core._runtime_impl_helpers import SubscriptionManager, get_impl
from autogen_core._serialization import SerializationRegistry
from autogen_core._telemetry import (
    MessageRuntimeTracingConfig,
    TraceHelper,
    get_telemetry_grpc_metadata,
)
from autogen_ext.runtimes.grpc import _constants
from autogen_ext.runtimes.grpc._utils import subscription_to_proto
from autogen_ext.runtimes.grpc.protos import agent_worker_pb2, cloudevent_pb2
from autogenstudio.datamodel import LLMCallEventMessage
from connecpy.context import ClientContext
from google.protobuf import any_pb2
from loguru import logger
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents.team_builder.article_gen_teambuilder import ArticleGenTeamBuilder
from mtmai.agents.team_builder.assisant_team_builder import AssistantTeamBuilder
from mtmai.agents.team_builder.m1_web_builder import M1WebTeamBuilder
from mtmai.agents.team_builder.swram_team_builder import SwramTeamBuilder
from mtmai.agents.team_builder.travel_builder import TravelTeamBuilder
from mtmai.agents.tenant_agent.tenant_agent import MsgResetTenant
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.mt_component import MtComponent
from mtmai.core.config import settings
from mtmai.mtlibs.id import generate_uuid
from mtmai.mtmpb import ag_pb2
from opentelemetry.trace import TracerProvider

# logger = logging.getLogger("autogen_core")
# event_logger = logging.getLogger("autogen_core.events")

P = ParamSpec("P")
T = TypeVar("T", bound=Agent)


type_func_alias = type


class QueueAsyncIterable(AsyncIterator[Any], AsyncIterable[Any]):
    def __init__(self, queue: asyncio.Queue[Any]) -> None:
        self._queue = queue

    async def __anext__(self) -> Any:
        return await self._queue.get()

    def __aiter__(self) -> AsyncIterator[Any]:
        return self


class WorkerTeam:
    # TODO: Needs to handle agent close() call
    def __init__(
        self,
        tracer_provider: TracerProvider | None = None,
        payload_serialization_format: str = JSON_DATA_CONTENT_TYPE,
    ) -> None:
        self._trace_helper = TraceHelper(
            tracer_provider, MessageRuntimeTracingConfig("Worker Runtime")
        )
        self._per_type_subscribers: DefaultDict[tuple[str, str], Set[AgentId]] = (
            defaultdict(set)
        )
        self._agent_factories: Dict[
            str,
            Callable[[], Agent | Awaitable[Agent]]
            | Callable[[AgentRuntime, AgentId], Agent | Awaitable[Agent]],
        ] = {}
        self._instantiated_agents: Dict[AgentId, Agent] = {}
        self._known_namespaces: set[str] = set()
        self._read_task: None | Task[None] = None
        self._running = False
        self._pending_requests: Dict[str, Future[Any]] = {}
        self._pending_requests_lock = asyncio.Lock()
        self._next_request_id = 0
        self._background_tasks: Set[Task[Any]] = set()
        self._subscription_manager = SubscriptionManager()
        self._serialization_registry = SerializationRegistry()

        if payload_serialization_format not in {
            JSON_DATA_CONTENT_TYPE,
            PROTOBUF_DATA_CONTENT_TYPE,
        }:
            raise ValueError(
                f"Unsupported payload serialization format: {payload_serialization_format}"
            )

        self._payload_serialization_format = payload_serialization_format
        self._runtime = SingleThreadedAgentRuntime(
            tracer_provider=tracer_provider,
            # payload_serialization_format=self._payload_serialization_format,
        )

    async def start(self) -> None:
        """Start the runtime in a background task."""
        if self._running:
            raise ValueError("runtime is already running.")
        logger.info(f"gomtm runtime start: {settings.GOMTM_URL}")
        self._runtime.start()
        self._running = True

        await self._init_ingestor()
        logger.info(f"(Gomtm) runtime started with apiurl: {self.api_url}")

    def _raise_on_exception(self, task: Task[Any]) -> None:
        exception = task.exception()
        if exception is not None:
            raise exception

    async def stop(self) -> None:
        """Stop the runtime immediately."""
        if not self._running:
            raise RuntimeError("Runtime is not running.")
        self._running = False
        # Wait for all background tasks to finish.
        final_tasks_results = await asyncio.gather(
            *self._background_tasks, return_exceptions=True
        )
        for task_result in final_tasks_results:
            if isinstance(task_result, Exception):
                logger.error("Error in background task", exc_info=task_result)
        # Close the host connection.
        if self._host_connection is not None:
            try:
                await self._host_connection.close()
            except asyncio.CancelledError:
                pass
        # Cancel the read task.
        if self._read_task is not None:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass

    async def stop_when_signal(
        self, signals: Sequence[signal.Signals] = (signal.SIGTERM, signal.SIGINT)
    ) -> None:
        """Stop the runtime when a signal is received."""
        loop = asyncio.get_running_loop()
        shutdown_event = asyncio.Event()

        def signal_handler() -> None:
            logger.info("Received exit signal, shutting down gracefully...")
            shutdown_event.set()

        for sig in signals:
            loop.add_signal_handler(sig, signal_handler)
        await shutdown_event.wait()
        await self.stop()

    @property
    def _known_agent_names(self) -> Set[str]:
        return set(self._agent_factories.keys())

    async def _send_message(
        self,
        runtime_message: agent_worker_pb2.Message,
        send_type: Literal["send", "publish"],
        recipient: AgentId | TopicId,
        telemetry_metadata: Mapping[str, str],
    ) -> None:
        if self._host_connection is None:
            raise RuntimeError("Host connection is not set.")
        with self._trace_helper.trace_block(
            send_type, recipient, parent=telemetry_metadata
        ):
            await self._host_connection.send(runtime_message)

    async def send_message(
        self,
        message: Any,
        recipient: AgentId,
        *,
        sender: AgentId | None = None,
        cancellation_token: CancellationToken | None = None,
        message_id: str | None = None,
    ) -> Any:
        # TODO: use message_id
        if not self._running:
            raise ValueError("Runtime must be running when sending message.")
        if self._host_connection is None:
            raise RuntimeError("Host connection is not set.")
        data_type = self._serialization_registry.type_name(message)
        with self._trace_helper.trace_block(
            "create",
            recipient,
            parent=None,
            extraAttributes={"message_type": data_type},
        ):
            # create a new future for the result
            future = asyncio.get_event_loop().create_future()
            request_id = await self._get_new_request_id()
            self._pending_requests[request_id] = future
            serialized_message = self._serialization_registry.serialize(
                message,
                type_name=data_type,
                # data_content_type=JSON_DATA_CONTENT_TYPE,
                data_content_type=PROTOBUF_DATA_CONTENT_TYPE,
            )
            telemetry_metadata = get_telemetry_grpc_metadata()
            runtime_message = agent_worker_pb2.Message(
                request=agent_worker_pb2.RpcRequest(
                    request_id=request_id,
                    target=agent_worker_pb2.AgentId(
                        type=recipient.type, key=recipient.key
                    ),
                    source=agent_worker_pb2.AgentId(type=sender.type, key=sender.key)
                    if sender is not None
                    else None,
                    metadata=telemetry_metadata,
                    payload=agent_worker_pb2.Payload(
                        data_type=data_type,
                        data=serialized_message,
                        data_content_type=JSON_DATA_CONTENT_TYPE,
                    ),
                )
            )

            # TODO: Find a way to handle timeouts/errors
            task = asyncio.create_task(
                self._send_message(
                    runtime_message, "send", recipient, telemetry_metadata
                )
            )
            self._background_tasks.add(task)
            task.add_done_callback(self._raise_on_exception)
            task.add_done_callback(self._background_tasks.discard)
            return await future

    async def publish_message(
        self,
        message: Any,
        topic_id: TopicId,
        *,
        sender: AgentId | None = None,
        cancellation_token: CancellationToken | None = None,
        message_id: str | None = None,
    ) -> None:
        if not self._running:
            raise ValueError("Runtime must be running when publishing message.")
        if self._host_connection is None:
            raise RuntimeError("Host connection is not set.")
        if message_id is None:
            message_id = str(uuid.uuid4())

        message_type = self._serialization_registry.type_name(message)
        with self._trace_helper.trace_block(
            "create",
            topic_id,
            parent=None,
            extraAttributes={"message_type": message_type},
        ):
            serialized_message = self._serialization_registry.serialize(
                message,
                type_name=message_type,
                data_content_type=self._payload_serialization_format,
            )

            sender_id = sender or AgentId("unknown", "unknown")
            attributes = {
                _constants.DATA_CONTENT_TYPE_ATTR: cloudevent_pb2.CloudEvent.CloudEventAttributeValue(
                    ce_string=self._payload_serialization_format
                ),
                _constants.DATA_SCHEMA_ATTR: cloudevent_pb2.CloudEvent.CloudEventAttributeValue(
                    ce_string=message_type
                ),
                _constants.AGENT_SENDER_TYPE_ATTR: cloudevent_pb2.CloudEvent.CloudEventAttributeValue(
                    ce_string=sender_id.type
                ),
                _constants.AGENT_SENDER_KEY_ATTR: cloudevent_pb2.CloudEvent.CloudEventAttributeValue(
                    ce_string=sender_id.key
                ),
                _constants.MESSAGE_KIND_ATTR: cloudevent_pb2.CloudEvent.CloudEventAttributeValue(
                    ce_string=_constants.MESSAGE_KIND_VALUE_PUBLISH
                ),
            }

            # If sending JSON we fill text_data with the serialized message
            # If sending Protobuf we fill proto_data with the serialized message
            # TODO: add an encoding field for serializer

            if self._payload_serialization_format == JSON_DATA_CONTENT_TYPE:
                runtime_message = agent_worker_pb2.Message(
                    cloudEvent=cloudevent_pb2.CloudEvent(
                        id=message_id,
                        spec_version="1.0",
                        type=topic_id.type,
                        source=topic_id.source,
                        attributes=attributes,
                        # TODO: use text, or proto fields appropriately
                        binary_data=serialized_message,
                    )
                )
            else:
                # We need to unpack the serialized proto back into an Any
                # TODO: find a way to prevent the roundtrip serialization
                any_proto = any_pb2.Any()
                any_proto.ParseFromString(serialized_message)
                runtime_message = agent_worker_pb2.Message(
                    cloudEvent=cloudevent_pb2.CloudEvent(
                        id=message_id,
                        spec_version="1.0",
                        type=topic_id.type,
                        source=topic_id.source,
                        attributes=attributes,
                        proto_data=any_proto,
                    )
                )

            telemetry_metadata = get_telemetry_grpc_metadata()
            task = asyncio.create_task(
                self._send_message(
                    runtime_message, "publish", topic_id, telemetry_metadata
                )
            )
            self._background_tasks.add(task)
            task.add_done_callback(self._raise_on_exception)
            task.add_done_callback(self._background_tasks.discard)

    async def save_state(self) -> Mapping[str, Any]:
        raise NotImplementedError("Saving state is not yet implemented.")

    async def load_state(self, state: Mapping[str, Any]) -> None:
        raise NotImplementedError("Loading state is not yet implemented.")

    async def agent_metadata(self, agent: AgentId) -> AgentMetadata:
        raise NotImplementedError("Agent metadata is not yet implemented.")

    async def agent_save_state(self, agent: AgentId) -> Mapping[str, Any]:
        raise NotImplementedError("Agent save_state is not yet implemented.")

    async def agent_load_state(self, agent: AgentId, state: Mapping[str, Any]) -> None:
        raise NotImplementedError("Agent load_state is not yet implemented.")

    async def _get_new_request_id(self) -> str:
        async with self._pending_requests_lock:
            self._next_request_id += 1
            return str(self._next_request_id)

    async def _process_request(self, request: agent_worker_pb2.RpcRequest) -> None:
        assert self._host_connection is not None
        recipient = AgentId(request.target.type, request.target.key)
        sender: AgentId | None = None
        if request.HasField("source"):
            sender = AgentId(request.source.type, request.source.key)
            logging.info(f"Processing request from {sender} to {recipient}")
        else:
            logging.info(f"Processing request from unknown source to {recipient}")

        # Deserialize the message.
        message = self._serialization_registry.deserialize(
            request.payload.data,
            type_name=request.payload.data_type,
            data_content_type=request.payload.data_content_type,
        )

        # Get the receiving agent and prepare the message context.
        rec_agent = await self._get_agent(recipient)
        message_context = MessageContext(
            sender=sender,
            topic_id=None,
            is_rpc=True,
            cancellation_token=CancellationToken(),
            message_id=request.request_id,
        )

        # Call the receiving agent.
        try:
            with MessageHandlerContext.populate_context(rec_agent.id):
                with self._trace_helper.trace_block(
                    "process",
                    rec_agent.id,
                    parent=request.metadata,
                    attributes={"request_id": request.request_id},
                    extraAttributes={"message_type": request.payload.data_type},
                ):
                    result = await rec_agent.on_message(message, ctx=message_context)
        except BaseException as e:
            response_message = agent_worker_pb2.Message(
                response=agent_worker_pb2.RpcResponse(
                    request_id=request.request_id,
                    error=str(e),
                    metadata=get_telemetry_grpc_metadata(),
                ),
            )
            # Send the error response.
            await self._host_connection.send(response_message)
            return

        # Serialize the result.
        result_type = self._serialization_registry.type_name(result)
        serialized_result = self._serialization_registry.serialize(
            result, type_name=result_type, data_content_type=JSON_DATA_CONTENT_TYPE
        )

        # Create the response message.
        response_message = agent_worker_pb2.Message(
            response=agent_worker_pb2.RpcResponse(
                request_id=request.request_id,
                payload=agent_worker_pb2.Payload(
                    data_type=result_type,
                    data=serialized_result,
                    data_content_type=JSON_DATA_CONTENT_TYPE,
                ),
                metadata=get_telemetry_grpc_metadata(),
            )
        )

        # Send the response.
        await self._host_connection.send(response_message)

    async def _process_response(self, response: agent_worker_pb2.RpcResponse) -> None:
        with self._trace_helper.trace_block(
            "ack",
            None,
            parent=response.metadata,
            attributes={"request_id": response.request_id},
            extraAttributes={"message_type": response.payload.data_type},
        ):
            # Deserialize the result.
            result = self._serialization_registry.deserialize(
                response.payload.data,
                type_name=response.payload.data_type,
                data_content_type=response.payload.data_content_type,
            )
            # Get the future and set the result.
            future = self._pending_requests.pop(response.request_id)
            if len(response.error) > 0:
                future.set_exception(Exception(response.error))
            else:
                future.set_result(result)

    async def _process_event(self, event: cloudevent_pb2.CloudEvent) -> None:
        event_attributes = event.attributes
        sender: AgentId | None = None
        if (
            _constants.AGENT_SENDER_TYPE_ATTR in event_attributes
            and _constants.AGENT_SENDER_KEY_ATTR in event_attributes
        ):
            sender = AgentId(
                event_attributes[_constants.AGENT_SENDER_TYPE_ATTR].ce_string,
                event_attributes[_constants.AGENT_SENDER_KEY_ATTR].ce_string,
            )
        topic_id = TopicId(event.type, event.source)
        # Get the recipients for the topic.
        recipients = await self._subscription_manager.get_subscribed_recipients(
            topic_id
        )

        message_content_type = event_attributes[
            _constants.DATA_CONTENT_TYPE_ATTR
        ].ce_string
        message_type = event_attributes[_constants.DATA_SCHEMA_ATTR].ce_string

        if message_content_type == JSON_DATA_CONTENT_TYPE:
            message = self._serialization_registry.deserialize(
                event.binary_data,
                type_name=message_type,
                data_content_type=message_content_type,
            )
        elif message_content_type == PROTOBUF_DATA_CONTENT_TYPE:
            # TODO: find a way to prevent the roundtrip serialization
            proto_binary_data = event.proto_data.SerializeToString()
            message = self._serialization_registry.deserialize(
                proto_binary_data,
                type_name=message_type,
                data_content_type=message_content_type,
            )
        else:
            raise ValueError(
                f"Unsupported message content type: {message_content_type}"
            )

        # TODO: dont read these values in the runtime
        topic_type_suffix = (
            topic_id.type.split(":", maxsplit=1)[1] if ":" in topic_id.type else ""
        )
        is_rpc = topic_type_suffix == _constants.MESSAGE_KIND_VALUE_RPC_REQUEST
        is_marked_rpc_type = (
            _constants.MESSAGE_KIND_ATTR in event_attributes
            and event_attributes[_constants.MESSAGE_KIND_ATTR].ce_string
            == _constants.MESSAGE_KIND_VALUE_RPC_REQUEST
        )
        if is_rpc and not is_marked_rpc_type:
            warnings.warn(
                "Received RPC request with topic type suffix but not marked as RPC request.",
                stacklevel=2,
            )

        # Send the message to each recipient.
        responses: List[Awaitable[Any]] = []
        for agent_id in recipients:
            if agent_id == sender:
                continue
            message_context = MessageContext(
                sender=sender,
                topic_id=topic_id,
                is_rpc=is_rpc,
                cancellation_token=CancellationToken(),
                message_id=event.id,
            )
            agent = await self._get_agent(agent_id)
            with MessageHandlerContext.populate_context(agent.id):

                def stringify_attributes(
                    attributes: Mapping[
                        str, cloudevent_pb2.CloudEvent.CloudEventAttributeValue
                    ],
                ) -> Mapping[str, str]:
                    result: Dict[str, str] = {}
                    for key, value in attributes.items():
                        item = None
                        match value.WhichOneof("attr"):
                            case "ce_boolean":
                                item = str(value.ce_boolean)
                            case "ce_integer":
                                item = str(value.ce_integer)
                            case "ce_string":
                                item = value.ce_string
                            case "ce_bytes":
                                item = str(value.ce_bytes)
                            case "ce_uri":
                                item = value.ce_uri
                            case "ce_uri_ref":
                                item = value.ce_uri_ref
                            case "ce_timestamp":
                                item = str(value.ce_timestamp)
                            case _:
                                raise ValueError("Unknown attribute kind")
                        result[key] = item

                    return result

                async def send_message(
                    agent: Agent, message_context: MessageContext
                ) -> Any:
                    with self._trace_helper.trace_block(
                        "process",
                        agent.id,
                        parent=stringify_attributes(event.attributes),
                        extraAttributes={"message_type": message_type},
                    ):
                        await agent.on_message(message, ctx=message_context)

                future = send_message(agent, message_context)
            responses.append(future)
        # Wait for all responses.
        try:
            await asyncio.gather(*responses)
        except BaseException as e:
            logger.error("Error handling event", exc_info=e)

    async def register_factory(
        self,
        type: str | AgentType,
        agent_factory: Callable[[], T | Awaitable[T]],
        *,
        expected_class: type[T] | None = None,
    ) -> AgentType:
        if isinstance(type, str):
            type = AgentType(type)

        if type.type in self._agent_factories:
            raise ValueError(f"Agent with type {type} already exists.")
        if self._host_connection is None:
            raise RuntimeError("Host connection is not set.")

        async def factory_wrapper() -> T:
            maybe_agent_instance = agent_factory()
            if inspect.isawaitable(maybe_agent_instance):
                agent_instance = await maybe_agent_instance
            else:
                agent_instance = maybe_agent_instance

            if (
                expected_class is not None
                and type_func_alias(agent_instance) != expected_class
            ):
                raise ValueError("Factory registered using the wrong type.")

            return agent_instance

        self._agent_factories[type.type] = factory_wrapper

        # Send the registration request message to the host.
        message = agent_worker_pb2.RegisterAgentTypeRequest(type=type.type)
        _response: agent_worker_pb2.RegisterAgentTypeResponse = (
            await self._host_connection.stub.RegisterAgent(
                message, metadata=self._host_connection.metadata
            )
        )
        return type

    async def _invoke_agent_factory(
        self,
        agent_factory: Callable[[], T | Awaitable[T]]
        | Callable[[AgentRuntime, AgentId], T | Awaitable[T]],
        agent_id: AgentId,
    ) -> T:
        with AgentInstantiationContext.populate_context((self, agent_id)):
            if len(inspect.signature(agent_factory).parameters) == 0:
                factory_one = cast(Callable[[], T], agent_factory)
                agent = factory_one()
            elif len(inspect.signature(agent_factory).parameters) == 2:
                warnings.warn(
                    "Agent factories that take two arguments are deprecated. Use AgentInstantiationContext instead. Two arg factories will be removed in a future version.",
                    stacklevel=2,
                )
                factory_two = cast(Callable[[AgentRuntime, AgentId], T], agent_factory)
                agent = factory_two(self, agent_id)
            else:
                raise ValueError("Agent factory must take 0 or 2 arguments.")

            if inspect.isawaitable(agent):
                return cast(T, await agent)

        return agent

    async def _get_agent(self, agent_id: AgentId) -> Agent:
        if agent_id in self._instantiated_agents:
            return self._instantiated_agents[agent_id]

        if agent_id.type not in self._agent_factories:
            raise ValueError(f"Agent with name {agent_id.type} not found.")

        agent_factory = self._agent_factories[agent_id.type]
        agent = await self._invoke_agent_factory(agent_factory, agent_id)
        self._instantiated_agents[agent_id] = agent
        return agent

    # TODO: uncomment out the following type ignore when this is fixed in mypy: https://github.com/python/mypy/issues/3737
    async def try_get_underlying_agent_instance(
        self, id: AgentId, type: Type[T] = Agent
    ) -> T:  # type: ignore[assignment]
        if id.type not in self._agent_factories:
            raise LookupError(f"Agent with name {id.type} not found.")

        # TODO: check if remote
        agent_instance = await self._get_agent(id)

        if not isinstance(agent_instance, type):
            raise TypeError(f"Agent with name {id.type} is not of type {type.__name__}")

        return agent_instance

    async def add_subscription(self, subscription: Subscription) -> None:
        if self._host_connection is None:
            raise RuntimeError("Host connection is not set.")

        message = agent_worker_pb2.AddSubscriptionRequest(
            subscription=subscription_to_proto(subscription)
        )
        _response: agent_worker_pb2.AddSubscriptionResponse = (
            await self._host_connection.stub.AddSubscription(
                message, metadata=self._host_connection.metadata
            )
        )

        # Add to local subscription manager.
        await self._subscription_manager.add_subscription(subscription)

    async def remove_subscription(self, id: str) -> None:
        if self._host_connection is None:
            raise RuntimeError("Host connection is not set.")

        message = agent_worker_pb2.RemoveSubscriptionRequest(id=id)
        _response: agent_worker_pb2.RemoveSubscriptionResponse = (
            await self._host_connection.stub.RemoveSubscription(
                message, metadata=self._host_connection.metadata
            )
        )

        await self._subscription_manager.remove_subscription(id)

    async def get(
        self,
        id_or_type: AgentId | AgentType | str,
        /,
        key: str = "default",
        *,
        lazy: bool = True,
    ) -> AgentId:
        return await get_impl(
            id_or_type=id_or_type,
            key=key,
            lazy=lazy,
            instance_getter=self._get_agent,
        )

    def add_message_serializer(
        self, serializer: MessageSerializer[Any] | Sequence[MessageSerializer[Any]]
    ) -> None:
        self._serialization_registry.add_serializer(serializer)

    # async def _init_ingestor(self):
    #     """食入外部消息,包括用户输入的消息"""
    #     maxRetry = settings.WORKER_MAX_RETRY
    #     for i in range(maxRetry):
    #         try:
    #             self.wfapp = Hatchet.from_config(
    #                 loader.ConfigLoader().load_client_config(
    #                     loader.ClientConfig(
    #                         server_url=settings.GOMTM_URL,
    #                         # 绑定 python 默认logger,这样,就可以不用依赖 hatchet 内置的ctx.log()
    #                         # logger=logger,
    #                     )
    #                 ),
    #                 debug=True,
    #             )
    #             await self.wfapp.boot()

    #             self.worker = self.wfapp.worker(settings.WORKER_NAME)
    #             await self.setup_hatchet_workflows()

    #             logger.info("connect gomtm server success")
    #             break

    #         except Exception as e:
    #             if i == maxRetry - 1:
    #                 sys.exit(1)
    #             logger.info(f"failed to connect gomtm server, retry {i + 1},err:{e}")
    #             # raise e
    #             await asyncio.sleep(settings.WORKER_INTERVAL)
    #     # 非阻塞启动(注意: eventloop, 如果嵌套了,可能会莫名其妙的退出)
    #     # self.worker.setup_loop(asyncio.new_event_loop())
    #     # asyncio.create_task(self.worker.async_start())
    #     # 阻塞启动
    #     await self.worker.async_start()

    async def handle_message(self, message: AgentRunInput) -> TaskResult:
        tenant_id: str | None = message.tenant_id
        run_id = message.run_id
        user_input = message.content
        if user_input.startswith("/tenant/seed"):
            logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
            result = await self._runtime.send_message(
                MsgResetTenant(tenant_id=tenant_id),
                self.tenant_agent_id,
            )
            return
        team_comp_data: MtComponent = None
        if not message.team_id:
            # team_id = "fake_team_id"
            # result = await self._runtime.send_message(
            #     MsgGetTeamComponent(tenant_id=message.tenant_id, component_id=team_id),
            #     self.tenant_agent_id,
            # )
            tenant_teams = await self.list_team_component(message.tenant_id)
            logger.info(f"get team component: {tenant_teams}")
            message.team_id = tenant_teams[0].metadata.id

        team_comp_data = await self.wfapp._client.ag.GetComponent(
            ctx=ClientContext(),
            request=ag_pb2.GetComponentReq(
                tenant_id=message.tenant_id, component_id=message.team_id
            ),
        )

        component_json = json.loads(team_comp_data.component)

        team = Team.load_component(component_json)
        team_id = message.team_id
        if not team_id:
            team_id = generate_uuid()

        thread_id = message.session_id
        if not thread_id:
            thread_id = generate_uuid()
        else:
            logger.info(f"现有session: {thread_id}")
            # 加载团队状态
            # await self.load_state(thread_id)
            ...

        task_result: TaskResult | None = None
        try:
            async for event in team.run_stream(
                task=message.content,
                # cancellation_token=ctx.cancellation_token,
            ):
                # if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
                #     break

                if isinstance(event, TaskResult):
                    logger.info(f"Worker Agent 收到任务结果: {event}")
                    task_result = event
                elif isinstance(
                    event,
                    (
                        TextMessage,
                        MultiModalMessage,
                        StopMessage,
                        HandoffMessage,
                        ToolCallRequestEvent,
                        ToolCallExecutionEvent,
                        LLMCallEventMessage,
                    ),
                ):
                    if event.content:
                        await self.handle_message_create(
                            ChatMessageUpsert(
                                content=event.content,
                                tenant_id=message.tenant_id,
                                component_id=message.team_id,
                                threadId=thread_id,
                                role=event.source,
                                runId=run_id,
                                stepRunId=message.step_run_id,
                            ),
                        )
                        await self.wfapp.event.stream(
                            "hello1await22222222", step_run_id=message.step_run_id
                        )
                    else:
                        logger.warn(f"worker Agent 消息没有content: {event}")
                else:
                    logger.info(f"worker Agent 收到(未知类型)消息: {event}")
        finally:
            await self.save_team_state(
                team=team,
                team_id=team_id,
                tenant_id=tenant_id,
                run_id=run_id,
            )
        return task_result

    # async def setup_hatchet_workflows(self):
    #     wfapp = self.wfapp
    #     worker_app = self

    #     class MyResultType(TypedDict):
    #         my_func: str

    #     @wfapp.function(
    #         name="my_func2232",
    #     )
    #     def my_func(context: Context) -> MyResultType:
    #         return MyResultType(my_func="testing123")

    #     @wfapp.workflow(
    #         name="ag",
    #         on_events=["ag:run"],
    #         input_validator=AgentRunInput,
    #     )
    #     class FlowAg:
    #         @self.wfapp.step(timeout="60m")
    #         async def step_entry(self, hatctx: Context):
    #             set_gomtm_api_context(hatctx.aio)
    #             input = cast(AgentRunInput, hatctx.workflow_input())
    #             if not input.run_id:
    #                 input.run_id = hatctx.workflow_run_id()
    #             if not input.step_run_id:
    #                 input.step_run_id = hatctx.step_run_id
    #             task_result = await worker_app.handle_message(input)
    #             # Convert TaskResult to a JSON-serializable dict
    #             return {
    #                 # "messages": [
    #                 #     msg.model_dump() if hasattr(msg, "model_dump") else msg
    #                 #     for msg in task_result.messages
    #                 # ],
    #                 "ok": True,
    #             }

    #     self.worker.register_workflow(FlowAg())

    # async def setup_browser_workflows(self):
    #     @self.wfapp.workflow(
    #         on_events=["browser:run"],
    #         # input_validator=CrewAIParams,
    #     )
    #     class FlowBrowser:
    #         @self.wfapp.step(timeout="10m", retries=1)
    #         async def run(self, hatctx: Context):
    #             from mtmai.clients.rest.models import BrowserParams

    #             # from mtmai.agents.browser_agent import BrowserAgent

    #             input = BrowserParams.model_validate(hatctx.workflow_input())
    #             # init_mtmai_context(hatctx)

    #             # ctx = get_mtmai_context()
    #             # tenant_id = ctx.tenant_id
    #             # llm_config = await wfapp.rest.aio.llm_api.llm_get(
    #             #     tenant=tenant_id, slug="default"
    #             # )
    #             # llm = ChatOpenAI(
    #             #     model=llm_config.model,
    #             #     api_key=llm_config.api_key,
    #             #     base_url=llm_config.base_url,
    #             #     temperature=0,
    #             #     max_tokens=40960,
    #             #     verbose=True,
    #             #     http_client=httpx.Client(transport=LoggingTransport()),
    #             #     http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
    #             # )

    #             # 简单测试llm 是否配置正确
    #             # aa=llm.invoke(["Hello, how are you?"])
    #             # print(aa)
    #             # agent = BrowserAgent(
    #             #     generate_gif=False,
    #             #     use_vision=False,
    #             #     tool_call_in_content=False,
    #             #     # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
    #             #     task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'",
    #             #     llm=llm,
    #             #     browser=Browser(config=BrowserConfig(headless=False)),
    #             # )
    #             # await agent.run()

    #     self.worker.register_workflow(FlowBrowser())

    async def list_team_component(self, tenant_id: str):
        return await self.tenant_reset_teams(tenant_id)

    async def tenant_reset_teams(self, tenant_id: str):
        logger.info(f"TenantAgent 重置租户信息: {tenant_id}")
        results = []
        teams_list = await self.wfapp.rest.aio.coms_api.coms_list(
            tenant=tenant_id, label="default"
        )
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            results.append(teams_list.rows[0])
        defaultModel = await self.wfapp.rest.aio.model_api.model_get(
            tenant=tenant_id, model="default"
        )
        model_dict = defaultModel.config.model_dump()
        model_dict.pop("n", None)
        model_client = MtmOpenAIChatCompletionClient(
            **model_dict,
        )

        self.team_builders = [
            AssistantTeamBuilder(),
            SwramTeamBuilder(),
            ArticleGenTeamBuilder(),
            M1WebTeamBuilder(),
            TravelTeamBuilder(),
        ]
        for team_builder in self.team_builders:
            label = team_builder.name
            logger.info(f"create team for tenant {tenant_id}")
            team_comp = await team_builder.create_team(model_client)
            component_model = team_comp.dump_component()
            new_team = await self.wfapp.rest.aio.coms_api.coms_upsert(
                tenant=tenant_id,
                com=generate_uuid(),
                mt_component=MtComponent(
                    label=label,
                    description=component_model.description or "",
                    componentType="team",
                    component=component_model.model_dump(),
                ).model_dump(),
            )
            results.append(new_team)
        return results

    async def save_team_state(
        self, team: Team, team_id: str, tenant_id: str, run_id: str
    ) -> None:
        """保存团队状态"""
        logger.info("保存团队状态")
        # 确保停止团队的内部 agents
        if team and hasattr(team, "_participants"):
            for agent in team._participants:
                if hasattr(agent, "close"):
                    await agent.close()
        state = await team.save_state()
        await self.wfapp.rest.aio.ag_state_api.ag_state_upsert(
            tenant=tenant_id,
            ag_state_upsert=AgStateUpsert(
                componentId=team_id,
                runId=run_id,
                state=state,
            ).model_dump(),
        )

    async def handle_message_create(self, message: ChatMessageUpsert) -> None:
        await self.wfapp.rest.aio.chat_api.chat_message_upsert(
            tenant=message.tenant_id,
            chat_message_upsert=message.model_dump(),
        )
