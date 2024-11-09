from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class GetBauplanInfoRequest(_message.Message):
    __slots__ = ('api_key',)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    def __init__(self, api_key: _Optional[str] = ...) -> None: ...

class RunnerNodeInfo(_message.Message):
    __slots__ = ('public_key', 'hostname')
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    public_key: str
    hostname: str
    def __init__(self, public_key: _Optional[str] = ..., hostname: _Optional[str] = ...) -> None: ...

class GetBauplanInfoResponse(_message.Message):
    __slots__ = ('runners', 'user', 'client_version', 'server_version')
    RUNNERS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    SERVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    runners: _containers.RepeatedCompositeFieldContainer[RunnerNodeInfo]
    user: str
    client_version: str
    server_version: str
    def __init__(
        self,
        runners: _Optional[_Iterable[_Union[RunnerNodeInfo, _Mapping]]] = ...,
        user: _Optional[str] = ...,
        client_version: _Optional[str] = ...,
        server_version: _Optional[str] = ...,
    ) -> None: ...
