import pytest

from ..messages.commands import InvokerType, RunWorkflowParams


@pytest.mark.parametrize(
    "value,member",
    [
        ("BlockingLocalSubprocessInvoker", InvokerType.BLOCKING_SUBPROCESS),
        ("CloudBatchInvoker", InvokerType.CLOUD_BATCH),
        ("CloudRunJobsSandboxInvoker", InvokerType.CLOUD_RUN_JOBS_SANDBOX),
    ],
)
def test_invoker_type_values(value, member):
    assert InvokerType(value) is member


@pytest.mark.parametrize("invoker_type", list(InvokerType))
def test_run_workflow_params_accepts_all_invoker_types(invoker_type):
    params = RunWorkflowParams(
        match_spec="ecoscope-workflows-test==0.1.0",
        invoker_type=invoker_type.value,
        command="run",
    )
    assert params.invoker_type is invoker_type
