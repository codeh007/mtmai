from google.protobuf import descriptor_pb2 as _descriptor_pb2
from mtmai.mtmpb import mtm_pb2 as _mtm_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DemoStream1Request(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DemoStream1Reply(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GreetRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GreetResponse(_message.Message):
    __slots__ = ("greeting",)
    GREETING_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    def __init__(self, greeting: _Optional[str] = ...) -> None: ...

class AgentRunInput(_message.Message):
    __slots__ = ("tenant_id", "run_id", "content", "run_step_id", "sessionId")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    RUN_STEP_ID_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    run_id: str
    content: str
    run_step_id: str
    sessionId: str
    def __init__(self, tenant_id: _Optional[str] = ..., run_id: _Optional[str] = ..., content: _Optional[str] = ..., run_step_id: _Optional[str] = ..., sessionId: _Optional[str] = ...) -> None: ...

class GetComponentReq(_message.Message):
    __slots__ = ("tenant_id", "component_id")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    component_id: str
    def __init__(self, tenant_id: _Optional[str] = ..., component_id: _Optional[str] = ...) -> None: ...

class ComponentListReq(_message.Message):
    __slots__ = ("Pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ...) -> None: ...

class Component(_message.Message):
    __slots__ = ("component_id", "component")
    COMPONENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    component_id: str
    component: bytes
    def __init__(self, component_id: _Optional[str] = ..., component: _Optional[bytes] = ...) -> None: ...

class ComponentListRes(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    items: _containers.RepeatedCompositeFieldContainer[Component]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Component, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ("meta", "id", "content", "role", "source", "created_at")
    META_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    meta: _mtm_pb2.APIResourceMeta
    id: str
    content: str
    role: str
    source: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, meta: _Optional[_Union[_mtm_pb2.APIResourceMeta, _Mapping]] = ..., id: _Optional[str] = ..., content: _Optional[str] = ..., role: _Optional[str] = ..., source: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EventEmbedding(_message.Message):
    __slots__ = ("coll", "texts")
    COLL_FIELD_NUMBER: _ClassVar[int]
    TEXTS_FIELD_NUMBER: _ClassVar[int]
    coll: str
    texts: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, coll: _Optional[str] = ..., texts: _Optional[_Iterable[str]] = ...) -> None: ...

class ChatMessageListReq(_message.Message):
    __slots__ = ("Pagination", "session_id")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    session_id: str
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., session_id: _Optional[str] = ...) -> None: ...

class ChatMessageList(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    items: _containers.RepeatedCompositeFieldContainer[ChatMessage]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ChatMessage, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...
