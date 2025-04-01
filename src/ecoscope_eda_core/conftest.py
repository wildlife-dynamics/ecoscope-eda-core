import asyncio
import pytest
from unittest.mock import MagicMock


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


@pytest.fixture
def pubsub_client_mock():
    client = MagicMock()
    client.topic_path.return_value = "projects/ecoscope-dev/topics/workflow-requests"
    client.publish.return_value = async_return({"messageIds": ["7061707768812258"]})
    client.__aenter__.return_value = async_return(client)
    client.__aexit__.return_value = async_return(None)
    client.close.return_value = async_return(None)
    return client
