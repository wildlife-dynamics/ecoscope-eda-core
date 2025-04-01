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
            conda_channel="https://repo.prefix.dev/ecoscope-workflows/",
            conda_package="custom-events-workflow-pkg",
            conda_package_version="0.0.65",
            command="run",
            invoker_kwargs={
                "mock_io": True,
                "results_url": "gs://bucket/results",
                "filter_events": {"min_x": -98.567, "max_x": 53.234},
            },
        )
    )
    await publisher.publish(messages=[run_workflow_command], topic="workflow-requests")
    await publisher.close()
    # ToDo: Assert that publish was called with the correct arguments
    assert pubsub_client_mock.publish.called


# ToDo: Extend test coverage to more scenarios including usage as context manager and GCP PubSub availability issues
