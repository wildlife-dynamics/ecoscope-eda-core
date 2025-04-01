import pytest
from ..publishers import GCPPubSubPublisher
from ..messages import RunWorkflow, RunWorkflowParams


pytestmark = pytest.mark.asyncio


async def test_gcp_pubsub_publisher_minimal(mocker, pubsub_client_mock):
    mocker.patch(
        "src.ecoscope_eda_core.publishers.gcp_pubsub.pubsub.PublisherClient",
        return_value=pubsub_client_mock,
    )

    publisher = GCPPubSubPublisher(project="ecoscope-dev")
    run_workflow_command = RunWorkflow(
        payload=RunWorkflowParams(
            conda_channel="prefix-dev",
            conda_package="workflow-events-custom-pkg",
            command="run",
            invoker_kwargs={
                "mock_io": True,
                "results_url": "gs://bucket/results",
                "filter_events": {"min_x": -98.567, "max_x": 53.234},
            },
        )
    )
    await publisher.publish(messages=[run_workflow_command], topic="workflow-requests")

    # ToDo: Assert that publish was called with the correct arguments
    assert pubsub_client_mock.publish.called


# ToDo: Extend test coverage to more scenarios including usage as context manager and GCP PubSub availability issues
