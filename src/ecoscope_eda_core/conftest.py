import asyncio

import aiohttp
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


@pytest.fixture
def pubsub_client_mock_with_one_timeout_error():
    client = AsyncMock()
    client.topic_path = lambda project, topic: f"projects/{project}/topics/{topic}"
    client.publish.side_effect = [
        asyncio.TimeoutError(),  # Timeout on the first call
        AsyncMock(return_value={"messageIds": ["7061707768812258"]}),
    ]
    client.__aenter__.return_value = async_return(client)
    client.__aexit__.return_value = async_return(None)
    client.close.return_value = async_return(None)
    return client


@pytest.fixture
def pubsub_client_mock_with_one_client_error():
    client = AsyncMock()
    client.topic_path = lambda project, topic: f"projects/{project}/topics/{topic}"
    client.publish.side_effect = [
        aiohttp.ClientError(),  # Error on the first call
        AsyncMock(return_value={"messageIds": ["7061707768812258"]}),
    ]
    client.__aenter__.return_value = async_return(client)
    client.__aexit__.return_value = async_return(None)
    client.close.return_value = async_return(None)
    return client
