import json
import typing

import pydantic.json
import structlog

from mtmai.forge.sdk.artifact.models import Artifact, ArtifactType
from mtmai.forge.sdk.db.enums import OrganizationAuthTokenType
from mtmai.forge.sdk.db.models import (
    ArtifactModel,
    AWSSecretParameterModel,
    BitwardenLoginCredentialParameterModel,
    BitwardenSensitiveInformationParameterModel,
    OrganizationAuthTokenModel,
    OrganizationModel,
    OutputParameterModel,
    StepModel,
    TaskModel,
    WorkflowModel,
    WorkflowParameterModel,
    WorkflowRunModel,
    WorkflowRunOutputParameterModel,
    WorkflowRunParameterModel,
)
from mtmai.forge.sdk.models import Organization, OrganizationAuthToken, Step, StepStatus
from mtmai.forge.sdk.schemas.tasks import ProxyLocation, Task, TaskStatus
from mtmai.forge.sdk.workflow.models.parameter import (
    AWSSecretParameter,
    BitwardenLoginCredentialParameter,
    BitwardenSensitiveInformationParameter,
    OutputParameter,
    WorkflowParameter,
    WorkflowParameterType,
)
from mtmai.forge.sdk.workflow.models.workflow import (
    Workflow,
    WorkflowDefinition,
    WorkflowRun,
    WorkflowRunOutputParameter,
    WorkflowRunParameter,
    WorkflowRunStatus,
)
from mtmai.models.task import MtTask

LOG = structlog.get_logger()


@typing.no_type_check
def _custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    """
    return json.dumps(*args, default=pydantic.json.pydantic_encoder, **kwargs)


def convert_to_mttask(task_obj: MtTask, debug_enabled: bool = False) -> Task:
    if debug_enabled:
        LOG.debug("Converting TaskModel to Task", task_id=task_obj.task_id)
    task = Task(
        task_id=task_obj.task_id,
        status=TaskStatus(task_obj.status),
        created_at=task_obj.created_at,
        modified_at=task_obj.modified_at,
        title=task_obj.title,
        url=task_obj.url,
        webhook_callback_url=task_obj.webhook_callback_url,
        totp_verification_url=task_obj.totp_verification_url,
        totp_identifier=task_obj.totp_identifier,
        navigation_goal=task_obj.navigation_goal,
        data_extraction_goal=task_obj.data_extraction_goal,
        navigation_payload=task_obj.navigation_payload,
        extracted_information=task_obj.extracted_information,
        failure_reason=task_obj.failure_reason,
        organization_id=task_obj.organization_id,
        proxy_location=(
            ProxyLocation(task_obj.proxy_location) if task_obj.proxy_location else None
        ),
        extracted_information_schema=task_obj.extracted_information_schema,
        workflow_run_id=task_obj.workflow_run_id,
        order=task_obj.order,
        retry=task_obj.retry,
        max_steps_per_run=task_obj.max_steps_per_run,
        error_code_mapping=task_obj.error_code_mapping,
        errors=task_obj.errors,
    )
    return task
