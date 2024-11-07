from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PAService(_message.Message):
    __slots__ = ("service_id", "service_title", "created_at", "service_parent_id", "service_children")
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TITLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    service_id: int
    service_title: str
    created_at: str
    service_parent_id: int
    service_children: _containers.RepeatedCompositeFieldContainer[PAService]
    def __init__(self, service_id: _Optional[int] = ..., service_title: _Optional[str] = ..., created_at: _Optional[str] = ..., service_parent_id: _Optional[int] = ..., service_children: _Optional[_Iterable[_Union[PAService, _Mapping]]] = ...) -> None: ...
