from bauplan._bpln_proto.commander.service.v2 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CodeSnapshotRunRequest(_message.Message):
    __slots__ = (
        'job_request_common',
        'zip_file',
        'ref',
        'namespace',
        'dry_run',
        'transaction',
        'strict',
        'cache',
        'preview',
    )
    JOB_REQUEST_COMMON_FIELD_NUMBER: _ClassVar[int]
    ZIP_FILE_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    CACHE_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    job_request_common: _common_pb2.JobRequestCommon
    zip_file: bytes
    ref: str
    namespace: str
    dry_run: _common_pb2.JobRequestOptionalBool
    transaction: str
    strict: str
    cache: str
    preview: _common_pb2.JobRequestOptionalBool
    def __init__(
        self,
        job_request_common: _Optional[_Union[_common_pb2.JobRequestCommon, _Mapping]] = ...,
        zip_file: _Optional[bytes] = ...,
        ref: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        dry_run: _Optional[_Union[_common_pb2.JobRequestOptionalBool, str]] = ...,
        transaction: _Optional[str] = ...,
        strict: _Optional[str] = ...,
        cache: _Optional[str] = ...,
        preview: _Optional[_Union[_common_pb2.JobRequestOptionalBool, str]] = ...,
    ) -> None: ...

class CodeSnapshotRunResponse(_message.Message):
    __slots__ = (
        'job_response_common',
        'snapshot_id',
        'snapshot_uri',
        'ref',
        'namespace',
        'dry_run',
        'transaction',
        'strict',
        'cache',
        'preview',
        'user_branch_prefix',
    )
    JOB_RESPONSE_COMMON_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_URI_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    CACHE_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    USER_BRANCH_PREFIX_FIELD_NUMBER: _ClassVar[int]
    job_response_common: _common_pb2.JobResponseCommon
    snapshot_id: str
    snapshot_uri: str
    ref: str
    namespace: str
    dry_run: bool
    transaction: str
    strict: str
    cache: str
    preview: bool
    user_branch_prefix: str
    def __init__(
        self,
        job_response_common: _Optional[_Union[_common_pb2.JobResponseCommon, _Mapping]] = ...,
        snapshot_id: _Optional[str] = ...,
        snapshot_uri: _Optional[str] = ...,
        ref: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        dry_run: bool = ...,
        transaction: _Optional[str] = ...,
        strict: _Optional[str] = ...,
        cache: _Optional[str] = ...,
        preview: bool = ...,
        user_branch_prefix: _Optional[str] = ...,
    ) -> None: ...
