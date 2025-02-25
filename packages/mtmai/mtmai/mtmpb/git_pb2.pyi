from mtmai.mtmpb import mtm_pb2 as _mtm_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GitPullReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GitSetupReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GitSetupRes(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GitPullRes(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GitGetReq(_message.Message):
    __slots__ = ("slugs",)
    SLUGS_FIELD_NUMBER: _ClassVar[int]
    slugs: str
    def __init__(self, slugs: _Optional[str] = ...) -> None: ...

class GitInfo(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GitStartReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GitStartRes(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GitStopReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GitStopRes(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
