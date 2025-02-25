from mtmai.mtmpb import cloudevent_pb2 as _cloudevent_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AgentId(_message.Message):
    __slots__ = ("type", "key")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    type: str
    key: str
    def __init__(self, type: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class Payload(_message.Message):
    __slots__ = ("data_type", "data_content_type", "data")
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data_type: str
    data_content_type: str
    data: bytes
    def __init__(self, data_type: _Optional[str] = ..., data_content_type: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class RpcRequest(_message.Message):
    __slots__ = ("request_id", "source", "target", "method", "payload", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    source: AgentId
    target: AgentId
    method: str
    payload: Payload
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, request_id: _Optional[str] = ..., source: _Optional[_Union[AgentId, _Mapping]] = ..., target: _Optional[_Union[AgentId, _Mapping]] = ..., method: _Optional[str] = ..., payload: _Optional[_Union[Payload, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RpcResponse(_message.Message):
    __slots__ = ("request_id", "payload", "error", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    payload: Payload
    error: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, request_id: _Optional[str] = ..., payload: _Optional[_Union[Payload, _Mapping]] = ..., error: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RegisterAgentTypeRequest(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class RegisterAgentTypeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TypeSubscription(_message.Message):
    __slots__ = ("topic_type", "agent_type")
    TOPIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    AGENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    topic_type: str
    agent_type: str
    def __init__(self, topic_type: _Optional[str] = ..., agent_type: _Optional[str] = ...) -> None: ...

class TypePrefixSubscription(_message.Message):
    __slots__ = ("topic_type_prefix", "agent_type")
    TOPIC_TYPE_PREFIX_FIELD_NUMBER: _ClassVar[int]
    AGENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    topic_type_prefix: str
    agent_type: str
    def __init__(self, topic_type_prefix: _Optional[str] = ..., agent_type: _Optional[str] = ...) -> None: ...

class Subscription(_message.Message):
    __slots__ = ("id", "typeSubscription", "typePrefixSubscription")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPESUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPEPREFIXSUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    typeSubscription: TypeSubscription
    typePrefixSubscription: TypePrefixSubscription
    def __init__(self, id: _Optional[str] = ..., typeSubscription: _Optional[_Union[TypeSubscription, _Mapping]] = ..., typePrefixSubscription: _Optional[_Union[TypePrefixSubscription, _Mapping]] = ...) -> None: ...

class AddSubscriptionRequest(_message.Message):
    __slots__ = ("subscription",)
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    subscription: Subscription
    def __init__(self, subscription: _Optional[_Union[Subscription, _Mapping]] = ...) -> None: ...

class AddSubscriptionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RemoveSubscriptionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RemoveSubscriptionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSubscriptionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSubscriptionsResponse(_message.Message):
    __slots__ = ("subscriptions",)
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    subscriptions: _containers.RepeatedCompositeFieldContainer[Subscription]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[Subscription, _Mapping]]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("request", "response", "cloudEvent")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLOUDEVENT_FIELD_NUMBER: _ClassVar[int]
    request: RpcRequest
    response: RpcResponse
    cloudEvent: _cloudevent_pb2.CloudEvent
    def __init__(self, request: _Optional[_Union[RpcRequest, _Mapping]] = ..., response: _Optional[_Union[RpcResponse, _Mapping]] = ..., cloudEvent: _Optional[_Union[_cloudevent_pb2.CloudEvent, _Mapping]] = ...) -> None: ...

class SaveStateRequest(_message.Message):
    __slots__ = ("agentId",)
    AGENTID_FIELD_NUMBER: _ClassVar[int]
    agentId: AgentId
    def __init__(self, agentId: _Optional[_Union[AgentId, _Mapping]] = ...) -> None: ...

class SaveStateResponse(_message.Message):
    __slots__ = ("state", "error")
    STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    state: str
    error: str
    def __init__(self, state: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class LoadStateRequest(_message.Message):
    __slots__ = ("agentId", "state")
    AGENTID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    agentId: AgentId
    state: str
    def __init__(self, agentId: _Optional[_Union[AgentId, _Mapping]] = ..., state: _Optional[str] = ...) -> None: ...

class LoadStateResponse(_message.Message):
    __slots__ = ("error",)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: str
    def __init__(self, error: _Optional[str] = ...) -> None: ...

class ControlMessage(_message.Message):
    __slots__ = ("rpc_id", "destination", "respond_to", "rpcMessage")
    RPC_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    RESPOND_TO_FIELD_NUMBER: _ClassVar[int]
    RPCMESSAGE_FIELD_NUMBER: _ClassVar[int]
    rpc_id: str
    destination: str
    respond_to: str
    rpcMessage: _any_pb2.Any
    def __init__(self, rpc_id: _Optional[str] = ..., destination: _Optional[str] = ..., respond_to: _Optional[str] = ..., rpcMessage: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
