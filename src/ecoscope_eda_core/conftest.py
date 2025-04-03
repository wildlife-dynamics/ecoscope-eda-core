import asyncio
import pytest
from unittest.mock import AsyncMock


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


@pytest.fixture
def pubsub_client_mock():
    client = AsyncMock()
    client.topic_path = lambda project, topic: f"projects/{project}/topics/{topic}"
    client.publish.return_value = AsyncMock(
        return_value={"messageIds": ["7061707768812258"]}
    )
    client.__aenter__.return_value = async_return(client)
    client.__aexit__.return_value = async_return(None)
    client.close.return_value = async_return(None)
    return client
