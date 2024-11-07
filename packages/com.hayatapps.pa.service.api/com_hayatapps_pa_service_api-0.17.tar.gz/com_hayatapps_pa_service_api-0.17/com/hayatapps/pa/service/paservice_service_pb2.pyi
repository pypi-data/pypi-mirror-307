from com.hayatapps.pa.model import paservice_pb2 as _paservice_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PAServiceRequest(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _paservice_pb2.PAService
    def __init__(self, service: _Optional[_Union[_paservice_pb2.PAService, _Mapping]] = ...) -> None: ...

class PAServiceResponse(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _paservice_pb2.PAService
    def __init__(self, service: _Optional[_Union[_paservice_pb2.PAService, _Mapping]] = ...) -> None: ...
