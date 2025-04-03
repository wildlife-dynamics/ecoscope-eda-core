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
    pubsub_client_mock.publish.assert_called_once()
    call_args = pubsub_client_mock.publish.call_args
    assert call_args.kwargs["topic"] == "projects/ecoscope-dev/topics/workflow-requests"
    assert len(call_args.kwargs["messages"]) == 1
    pubsub_message = call_args.kwargs["messages"][0]
    expected_data = run_workflow_command.model_dump_json(exclude="attributes").encode(
        "utf-8"
    )
    assert pubsub_message.data == expected_data
    assert pubsub_message.ordering_key == ""  # No ordering_key in attributes
    assert pubsub_message.attributes == {}  # No attributes provided
    assert call_args.kwargs["session"] is None
    assert call_args.kwargs["timeout"] == 30  # Default timeout


async def test_gcp_pubsub_publisher_minimal_as_async_ctx_mgr(
    mocker, pubsub_client_mock
):
    mocker.patch(
        "src.ecoscope_eda_core.publishers.gcp_pubsub.pubsub.PublisherClient",
        return_value=pubsub_client_mock,
    )

    async with GCPPubSubPublisher(project="ecoscope-dev") as publisher:
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
    pubsub_client_mock.publish.assert_called_once()
    call_args = pubsub_client_mock.publish.call_args
    assert call_args.kwargs["topic"] == "projects/ecoscope-dev/topics/workflow-requests"
    assert len(call_args.kwargs["messages"]) == 1
    pubsub_message = call_args.kwargs["messages"][0]
    expected_data = run_workflow_command.model_dump_json(exclude="attributes").encode(
        "utf-8"
    )
    assert pubsub_message.data == expected_data
    assert pubsub_message.ordering_key == ""  # No ordering_key in attributes
    assert pubsub_message.attributes == {}  # No attributes provided
    assert call_args.kwargs["session"] is None
    assert call_args.kwargs["timeout"] == 30  # Default timeout
    assert pubsub_client_mock.close.called


async def test_gcp_pubsub_publisher_with_attributes(mocker, pubsub_client_mock):
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
        ),
        attributes={"ordering_key": "12345", "key1": "value1", "key2": "value2"},
    )
    await publisher.publish(messages=[run_workflow_command], topic="workflow-requests")
    await publisher.close()
    pubsub_client_mock.publish.assert_called_once()
    call_args = pubsub_client_mock.publish.call_args
    assert call_args.kwargs["topic"] == "projects/ecoscope-dev/topics/workflow-requests"
    assert len(call_args.kwargs["messages"]) == 1
    pubsub_message = call_args.kwargs["messages"][0]
    expected_data = run_workflow_command.model_dump_json(exclude="attributes").encode(
        "utf-8"
    )
    assert pubsub_message.data == expected_data
    assert (
        pubsub_message.ordering_key == run_workflow_command.attributes["ordering_key"]
    )
    assert pubsub_message.attributes == {
        "key1": "value1",
        "key2": "value2",
        # 'ordering_key' is not included in attributes
    }


async def test_gcp_pubsub_publisher_with_custom_timeout(mocker, pubsub_client_mock):
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
    await publisher.publish(
        messages=[run_workflow_command], topic="workflow-requests", timeout=60
    )
    await publisher.close()
    pubsub_client_mock.publish.assert_called_once()
    call_args = pubsub_client_mock.publish.call_args
    assert call_args.kwargs["topic"] == "projects/ecoscope-dev/topics/workflow-requests"
    assert len(call_args.kwargs["messages"]) == 1
    pubsub_message = call_args.kwargs["messages"][0]
    expected_data = run_workflow_command.model_dump_json(exclude="attributes").encode(
        "utf-8"
    )
    assert pubsub_message.data == expected_data
    assert pubsub_message.ordering_key == ""  # No ordering_key in attributes
    assert pubsub_message.attributes == {}  # No attributes provided
    assert call_args.kwargs["session"] is None
    assert call_args.kwargs["timeout"] == 60  # Custom timeout


async def test_gcp_pubsub_publisher_retries_on_request_timeout(
    mocker, pubsub_client_mock_with_one_timeout_error
):
    mocker.patch(
        "src.ecoscope_eda_core.publishers.gcp_pubsub.pubsub.PublisherClient",
        return_value=pubsub_client_mock_with_one_timeout_error,
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
    pubsub_client_mock_with_one_timeout_error.publish.assert_called()
    assert pubsub_client_mock_with_one_timeout_error.publish.call_count == 2


async def test_gcp_pubsub_publisher_retries_on_connect_error(
    mocker, pubsub_client_mock_with_one_client_error
):
    mocker.patch(
        "src.ecoscope_eda_core.publishers.gcp_pubsub.pubsub.PublisherClient",
        return_value=pubsub_client_mock_with_one_client_error,
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
    pubsub_client_mock_with_one_client_error.publish.assert_called()
    assert pubsub_client_mock_with_one_client_error.publish.call_count == 2
