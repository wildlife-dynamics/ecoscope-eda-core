from pydantic import BaseModel, Field
from .core import Command


class RunWorkflowParams(BaseModel):
    # ToDo: Add parameters
    pass


class RunWorkflow(Command):
    payload = RunWorkflowParams
