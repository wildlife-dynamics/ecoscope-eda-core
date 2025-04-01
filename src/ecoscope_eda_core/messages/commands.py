from enum import Enum
from typing import Dict, Any

from pydantic import BaseModel, Field
from .core import Command


class InvokerType(str, Enum):
    BLOCKING_SUBPROCESS = "BlockingLocalSubprocessInvoker"
    K8S_JOB = "K8sJobInvoker"


class RunWorkflowParams(BaseModel):
    conda_channel: str = Field(..., title="Conda channel")
    conda_package: str = Field(..., title="Package name")
    invoker_type: InvokerType = Field(
        InvokerType.BLOCKING_SUBPROCESS, title="Invoker type"
    )
    invoker_kwargs: Dict[str, Any] = Field(
        default_factory=dict, title="Invoker keyword arguments"
    )
    command: str = Field(..., title="Command to run")


class RunWorkflow(Command):
    payload: RunWorkflowParams
