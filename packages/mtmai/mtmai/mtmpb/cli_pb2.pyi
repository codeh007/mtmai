from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CliCommandItem(_message.Message):
    __slots__ = ("id", "cmdLine", "label")
    ID_FIELD_NUMBER: _ClassVar[int]
    CMDLINE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    cmdLine: str
    label: str
    def __init__(self, id: _Optional[str] = ..., cmdLine: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...

class ListCliReq(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCliRes(_message.Message):
    __slots__ = ("items", "count")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[CliCommandItem]
    count: int
    def __init__(self, items: _Optional[_Iterable[_Union[CliCommandItem, _Mapping]]] = ..., count: _Optional[int] = ...) -> None: ...
