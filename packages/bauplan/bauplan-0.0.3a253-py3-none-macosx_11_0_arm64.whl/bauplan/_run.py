import io
import os
import shutil
import tempfile
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, TypeVar, Union

from google.protobuf.json_format import MessageToJson

from ._bpln_proto.commander.service.v2.code_snapshot_re_run_pb2 import (
    CodeSnapshotReRunRequest,
    CodeSnapshotReRunResponse,
)
from ._bpln_proto.commander.service.v2.code_snapshot_run_pb2 import (
    CodeSnapshotRunRequest,
    CodeSnapshotRunResponse,
)
from ._bpln_proto.commander.service.v2.common_pb2 import JobRequestCommon
from ._bpln_proto.commander.service.v2.subscribe_logs_pb2 import (
    SubscribeLogsRequest,
    SubscribeLogsResponse,
)
from ._common import (
    BAUPLAN_VERSION,
    CLIENT_HOSTNAME,
    Constants,
)
from ._common_getters import (
    _get_args,
    _get_optional_bool,
    _get_optional_namespace,
    _get_optional_on_off_flag,
    _get_optional_ref,
    _get_optional_string,
    _get_parameters,
    _get_pb2_optional_bool,
    _get_string,
)
from ._common_operation import (
    _JobLifeCycleHandler,
    _lifecycle,
    _OperationContainer,
)
from .state import CommonRunState, ReRunExecutionContext, ReRunState, RunExecutionContext, RunState

GenericState = TypeVar('GenericState', bound=CommonRunState)


@dataclass
class JobStatus:
    canceled: str = Constants.JOB_STATUS_CANCELLED
    cancelled: str = Constants.JOB_STATUS_CANCELLED
    failed: str = Constants.JOB_STATUS_FAILED
    rejected: str = Constants.JOB_STATUS_REJECTED
    success: str = Constants.JOB_STATUS_SUCCESS
    timeout: str = Constants.JOB_STATUS_TIMEOUT
    unknown: str = Constants.JOB_STATUS_UNKNOWN


def _upload_files(
    name: str, project_dir: Path, temp_dir: str, parameters: Dict[str, Union[str, int, float, bool]]
) -> List[str]:
    if not project_dir.exists():
        raise ValueError(f'{name} is not a valid path')
    if not project_dir.is_dir():
        raise ValueError(f'{name} is not a directory')

    project_file_path = project_dir / 'bauplan_project.yml'
    if not project_file_path.exists():
        raise ValueError(f'File {project_file_path} not found.')
    if not project_file_path.is_file():
        raise ValueError(f'File {project_file_path} must be a file.')

    upload_files = []

    for file in os.listdir(project_dir):
        if file.endswith(('.py', '.sql', 'requirements.txt', 'bauplan_project.yml')):
            src_path = os.path.join(project_dir, file)
            dst_path = os.path.join(temp_dir, file)
            shutil.copy(src_path, dst_path)
            upload_files.append(dst_path)

    parameter_entries = [f"    '{key}': {_python_code_str(value)}," for key, value in parameters.items()]
    parameter_entries_str = '\n'.join(parameter_entries)
    internal_py_content = f"""
_user_params = {{
{parameter_entries_str}
}}
"""

    internal_py_path = os.path.join(temp_dir, '_internal.py')
    fp = Path(internal_py_path)
    fp.write_text(internal_py_content, encoding='UTF-8')

    upload_files.append(internal_py_path)

    return upload_files


def _get_project_zip_bytes(
    name: str,
    project_dir: Union[str, Path],
    parameters: Dict[str, Union[str, int, float, bool]],
) -> Tuple[str, bytes]:
    project_dir = Path(project_dir).expanduser().resolve()
    with tempfile.TemporaryDirectory() as temp_dir:
        upload_files = _upload_files(name, project_dir, temp_dir, parameters)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in upload_files:
                zipf.write(file, os.path.basename(file))
    return str(project_dir), zip_buffer.getvalue()


def _python_code_str(value: Any) -> str:
    if isinstance(value, str):
        return f"'{value}'"
    if isinstance(value, bool):
        return str(value)
    return repr(value)


def _handle_log(
    log: SubscribeLogsResponse,
    run_state: CommonRunState,
    debug: Optional[bool],
    verbose: Optional[bool],
) -> bool:
    runner_event = log.runner_event
    event_type = runner_event.WhichOneof('event')
    run_state.runner_events.append(runner_event)
    if event_type == 'task_start':
        ev = runner_event.task_start
        run_state.tasks_started[ev.task_name] = datetime.now()
    elif event_type == 'task_completion':
        ev = runner_event.task_completion
        run_state.tasks_stopped[ev.task_name] = datetime.now()
    elif event_type == 'job_completion':
        match runner_event.job_completion.WhichOneof('outcome'):
            case 'success':
                run_state.job_status = JobStatus.success
            case 'failure':
                run_state.job_status = JobStatus.failed
            case 'rejected':
                run_state.job_status = JobStatus.rejected
            case 'cancellation':
                run_state.job_status = JobStatus.cancelled
            case 'timeout':
                run_state.job_status = JobStatus.timeout
            case _:
                run_state.job_status = JobStatus.unknown
        return True
    elif event_type == 'runtime_user_log':
        ev = runner_event.runtime_user_log
        run_state.user_logs.append(ev)
    elif debug or verbose:
        print(debug, 'Unknown event type', event_type)
    return False


def _handle_log_stream(
    state: GenericState,
    log_stream: Iterable[SubscribeLogsResponse],
    debug: Optional[bool],
    verbose: Optional[bool],
) -> GenericState:
    for log in log_stream:
        if verbose:
            print('log_stream:', log)
        if _handle_log(log, state, debug, verbose):
            break

    state.ended_at_ns = time.time_ns()

    return state


class _Run(_OperationContainer):
    @_lifecycle
    def run(
        self,
        project_dir: Optional[str] = None,
        ref: Optional[str] = None,
        namespace: Optional[str] = None,
        parameters: Optional[Dict[str, Union[str, int, float, bool]]] = None,
        cache: Optional[str] = None,
        transaction: Optional[str] = None,
        dry_run: Optional[bool] = None,
        strict: Optional[str] = None,
        preview: Optional[bool] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        # internal
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        lifecycle_handler: Optional[_JobLifeCycleHandler] = None,
    ) -> RunState:
        """
        Run a Bauplan project and return the state of the run. This is the equivalent of
        running through the CLI the ``bauplan run`` command.

        This uses a _JobLifecyleHandler to handle timeout issues (future: KeyboardInterrupt)
        We register the job_id, log_stream, and flight_client with the lifecycle_handler
        so we can do a graceful shutdown behind the scenes upon TimeoutError exception.
        """

        started_at_ns = time.time_ns()

        if lifecycle_handler is None:
            raise Exception('internal error: lifecycle_handler is required')

        # Params validation
        parameters = _get_parameters('parameters', parameters)
        project_dir = _get_optional_string('project_dir', project_dir) or str(self.profile.project_dir or '.')
        project_dir, zip_file = _get_project_zip_bytes(
            name='project_dir',
            project_dir=project_dir,
            parameters=parameters,
        )
        ref = _get_optional_ref('ref', ref, self.profile.branch)
        namespace = _get_optional_namespace('namespace', namespace, self.profile.namespace)
        cache_flag = _get_optional_on_off_flag('cache', cache, self.profile.cache)
        transaction_flag = _get_optional_on_off_flag('transaction', transaction)
        dry_run, dry_run_flag = _get_pb2_optional_bool('dry_run', dry_run)
        strict_flag = _get_optional_on_off_flag('strict', strict)
        debug, debug_flag = _get_pb2_optional_bool('debug', debug, self.profile.debug)
        preview, preview_flag = _get_pb2_optional_bool('preview', preview)
        args = _get_args('args', args, self.profile.args)
        verbose = _get_optional_bool('verbose', verbose)

        # We can now submit the request
        client_v2, metadata = self._common.get_commander_v2_and_metadata(args)

        plan_request = CodeSnapshotRunRequest(
            job_request_common=JobRequestCommon(
                module_version=BAUPLAN_VERSION,
                hostname=CLIENT_HOSTNAME,
                args=args,
                debug=debug_flag,
            ),
            zip_file=zip_file,
            ref=ref,
            namespace=namespace,
            dry_run=dry_run_flag,
            transaction=transaction_flag,
            strict=strict_flag,
            cache=cache_flag,
            preview=preview_flag,
        )
        if debug or verbose:
            print(
                'CodeSnapshotRunRequest',
                'project_dir',
                project_dir,
                'request',
                MessageToJson(plan_request),
            )

        plan_response: CodeSnapshotRunResponse = client_v2.CodeSnapshotRun(plan_request, metadata=metadata)
        if debug or verbose:
            print(
                'CodeSnapshotRunResponse',
                'job_id',
                plan_response.job_response_common.job_id,
                'response',
                MessageToJson(plan_response),
            )

        job_id = plan_response.job_response_common.job_id
        lifecycle_handler.register_job_id(job_id)

        # Subscribe to logs
        log_stream: Iterable[SubscribeLogsResponse] = client_v2.SubscribeLogs(
            SubscribeLogsRequest(job_id=job_id),
            metadata=metadata,
        )
        lifecycle_handler.register_log_stream(log_stream)

        return _handle_log_stream(
            state=RunState(
                job_id=plan_response.job_response_common.job_id,
                ctx=RunExecutionContext(
                    snapshot_id=plan_response.snapshot_id,
                    snapshot_uri=plan_response.snapshot_uri,
                    project_dir=project_dir,
                    ref=plan_response.ref,
                    namespace=plan_response.namespace,
                    dry_run=plan_response.dry_run,
                    transaction=plan_response.transaction,
                    strict=plan_response.strict,
                    cache=plan_response.cache,
                    preview=plan_response.preview,
                    debug=plan_response.job_response_common.debug,
                ),
                started_at_ns=started_at_ns,
            ),
            log_stream=log_stream,
            debug=debug,
            verbose=verbose,
        )

    @_lifecycle
    def rerun(
        self,
        job_id: str,
        ref: Optional[str] = None,
        namespace: Optional[str] = None,
        cache: Optional[str] = None,
        transaction: Optional[str] = None,
        dry_run: Optional[bool] = None,
        strict: Optional[str] = None,
        preview: Optional[bool] = None,
        debug: Optional[bool] = None,
        args: Optional[Dict[str, str]] = None,
        verbose: Optional[bool] = None,
        # internal
        client_timeout: Optional[Union[int, float]] = None,
        lifecycle_handler: Optional[_JobLifeCycleHandler] = None,
    ) -> ReRunState:
        """
        Run a Bauplan project and return the state of the run. This is the equivalent of
        running through the CLI the ``bauplan run`` command.

        This uses a _JobLifecyleHandler to handle timeout issues (future: KeyboardInterrupt)
        We register the job_id, log_stream, and flight_client with the lifecycle_handler
        so we can do a graceful shutdown behind the scenes upon TimeoutError exception.
        """

        started_at_ns = time.time_ns()

        if lifecycle_handler is None:
            raise Exception('internal error: lifecycle_handler is required')

        # Params validation
        re_run_job_id = _get_string('job_id', job_id)
        ref = _get_optional_ref('ref', ref, self.profile.branch)
        namespace = _get_optional_namespace('namespace', namespace, self.profile.namespace)
        cache_flag = _get_optional_on_off_flag('cache', cache, self.profile.cache)
        transaction_flag = _get_optional_on_off_flag('transaction', transaction)
        dry_run, dry_run_flag = _get_pb2_optional_bool('dry_run', dry_run)
        strict_flag = _get_optional_on_off_flag('strict', strict)
        debug, debug_flag = _get_pb2_optional_bool('debug', debug, self.profile.debug)
        preview, preview_flag = _get_pb2_optional_bool('preview', preview)
        args = _get_args('args', args, self.profile.args)
        verbose = _get_optional_bool('verbose', verbose)

        # We can now submit the request
        client_v2, metadata = self._common.get_commander_v2_and_metadata(args)

        plan_request = CodeSnapshotReRunRequest(
            job_request_common=JobRequestCommon(
                module_version=BAUPLAN_VERSION,
                hostname=CLIENT_HOSTNAME,
                args=args,
                debug=debug_flag,
            ),
            re_run_job_id=re_run_job_id,
            ref=ref,
            namespace=namespace,
            dry_run=dry_run_flag,
            transaction=transaction_flag,
            strict=strict_flag,
            preview=preview_flag,
            cache=cache_flag,
        )
        if debug or verbose:
            print(
                'CodeSnapshotReRunRequest',
                'request',
                MessageToJson(plan_request),
            )

        plan_response: CodeSnapshotReRunResponse = client_v2.CodeSnapshotReRun(
            plan_request, metadata=metadata
        )
        if debug or verbose:
            print(
                'CodeSnapshotReRunResponse',
                'job_id',
                plan_response.job_response_common.job_id,
                'response',
                MessageToJson(plan_response),
            )

        job = plan_response.job_response_common.job_id
        lifecycle_handler.register_job_id(job)

        # Subscribe to logs
        log_stream: Iterable[SubscribeLogsResponse] = client_v2.SubscribeLogs(
            SubscribeLogsRequest(job_id=job_id),
            metadata=metadata,
        )
        lifecycle_handler.register_log_stream(log_stream)

        return _handle_log_stream(
            state=ReRunState(
                job_id=plan_response.job_response_common.job_id,
                ctx=ReRunExecutionContext(
                    re_run_job_id=re_run_job_id,
                    ref=plan_response.ref,
                    namespace=plan_response.namespace,
                    dry_run=plan_response.dry_run,
                    transaction=plan_response.transaction,
                    strict=plan_response.strict,
                    cache=plan_response.cache,
                    preview=plan_response.preview,
                    debug=plan_response.job_response_common.debug,
                ),
                started_at_ns=started_at_ns,
            ),
            log_stream=log_stream,
            debug=debug,
            verbose=verbose,
        )
