import asyncio
import json
import uuid
from asyncio import Task
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    ClassVar,
    ParamSpec,
    Sequence,
    Tuple,
    TypeVar,
    cast,
)

from autogen_core import Agent
from autogen_ext.runtimes.grpc._constants import GRPC_IMPORT_ERROR_STR
from autogen_ext.runtimes.grpc._type_helpers import ChannelArgumentType
from loguru import logger
from mtmai.core.loader import ClientConfig
from mtmai.mtmpb import agent_worker_pb2
from mtmai.mtmpb.agent_worker_pb2_grpc import AgentRpcStub
from typing_extensions import Self

try:
    import grpc.aio
except ImportError as e:
    raise ImportError(GRPC_IMPORT_ERROR_STR) from e

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


class AgentRuntimeClient:
    DEFAULT_GRPC_CONFIG: ClassVar[ChannelArgumentType] = [
        (
            "grpc.service_config",
            json.dumps(
                {
                    "methodConfig": [
                        {
                            "name": [{}],
                            "retryPolicy": {
                                "maxAttempts": 3,
                                "initialBackoff": "0.01s",
                                "maxBackoff": "5s",
                                "backoffMultiplier": 2,
                                "retryableStatusCodes": ["UNAVAILABLE"],
                            },
                        }
                    ],
                }
            ),
        )
    ]

    def __init__(self, channel: grpc.aio.Channel, stub: Any) -> None:  # type: ignore
        self._channel = channel
        self._send_queue = asyncio.Queue[agent_worker_pb2.Message]()
        self._recv_queue = asyncio.Queue[agent_worker_pb2.Message]()
        self._connection_task: Task[None] | None = None
        self._stub = stub
        self._client_id = str(uuid.uuid4())

    @property
    def stub(self) -> Any:
        return self._stub

    @property
    def metadata(self) -> Sequence[Tuple[str, str]]:
        return [("client-id", self._client_id)]

    @classmethod
    async def from_client_config(
        cls,
        config: ClientConfig,
        extra_grpc_config: ChannelArgumentType = DEFAULT_GRPC_CONFIG,
    ) -> Self:
        # logger.info("Connecting to %s", host_address)
        #  Always use DEFAULT_GRPC_CONFIG and override it with provided grpc_config

        merged_options = [
            (k, v)
            for k, v in {
                **dict(AgentRuntimeClient.DEFAULT_GRPC_CONFIG),
                **dict(extra_grpc_config),
            }.items()
        ]

        channel = grpc.aio.insecure_channel(
            config.host_port,
            options=merged_options,
        )
        stub = AgentRpcStub(channel)  # type: ignore
        instance = cls(channel, stub)

        # # channel.
        # instance._connection_task = await instance._connect(
        #     stub, instance._send_queue, instance._recv_queue, instance._client_id
        # )

        return instance

    async def close(self) -> None:
        if self._connection_task is None:
            raise RuntimeError("Connection is not open.")
        await self._channel.close()
        await self._connection_task

    @staticmethod
    async def _connect(
        stub: Any,  # AgentRpcAsyncStub
        send_queue: asyncio.Queue[agent_worker_pb2.Message],
        receive_queue: asyncio.Queue[agent_worker_pb2.Message],
        client_id: str,
    ) -> Task[None]:
        from grpc.aio import StreamStreamCall

        # TODO: where do exceptions from reading the iterable go? How do we recover from those?
        stream: StreamStreamCall[agent_worker_pb2.Message, agent_worker_pb2.Message] = (
            stub.OpenChannel(  # type: ignore
                QueueAsyncIterable(send_queue), metadata=[("client-id", client_id)]
            )
        )

        await stream.wait_for_connection()

        async def read_loop() -> None:
            while True:
                message = cast(agent_worker_pb2.Message, await stream.read())  # type: ignore
                if message == grpc.aio.EOF:  # type: ignore
                    logger.info("EOF")
                    break
                # logger.info(f"(loop)Received: {message}")
                await receive_queue.put(message)
                # logger.info("Put message in receive queue")

        return asyncio.create_task(read_loop())

    async def start(self) -> None:
        self._connection_task = await self._connect(
            self._stub,
            self._send_queue,
            self._recv_queue,
            self._client_id,
        )

    async def send(self, message: agent_worker_pb2.Message) -> None:
        await self._send_queue.put(message)
        # logger.info(f"(MTM Runtime) send: {message}")

        # logger.info("Put message in send queue")

    async def recv(self) -> agent_worker_pb2.Message:
        data = await self._recv_queue.get()
        # logger.info(f"(MTM Runtime) Received: {data}")
        return data
