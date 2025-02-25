from google.protobuf import descriptor_pb2 as _descriptor_pb2
from mtmai.mtmpb import mtm_pb2 as _mtm_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ListMemberReq(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MemberList(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...
