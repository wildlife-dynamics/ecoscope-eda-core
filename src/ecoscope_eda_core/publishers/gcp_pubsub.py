import os
import asyncio
from typing import List, Dict, Any, Optional

import aiohttp
import stamina
from gcloud.aio import pubsub
from .core import PublisherBase
from ..messages import Message


class GCPPubSubPublisher(PublisherBase):
    def __init__(
        self,
        project: Optional[str] = None,
        service_file: Optional[str] = None,
        token: Optional[str] = None,
        api_root: Optional[str] = None,
        timeout: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the GCP PubSub publisher.

        :param project: GCP project ID. If not provided, will be read from GCP_PROJECT env var.
        :param service_file: Path to the GCP service file. If not provided, will be read from GOOGLE_APPLICATION_CREDENTIALS env var.
        :param token: GCP token.
        :param api_root: GCP PubSub API root.
        :param timeout: Global request timeout settings as a dict, e.g. {"total": 60.0}.
        """
        self.project = project or os.getenv("GCP_PROJECT")
        assert self.project, "GCP project must be provided either by project argument or GCP_PROJECT env var"

        timeout_settings = timeout or {"total": 60.0}
        aiohttp_timeout = aiohttp.ClientTimeout(**timeout_settings)
        self._session = aiohttp.ClientSession(
            raise_for_status=True, timeout=aiohttp_timeout
        )

        self.service_file = service_file or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.token = token
        self.api_root = api_root

        self.pubsub_client = pubsub.PublisherClient(
            session=self._session,
            service_file=self.service_file,
            token=self.token,
            api_root=self.api_root,
        )

    @stamina.retry(
        on=(
            aiohttp.ClientError,
            asyncio.TimeoutError,
        ),  # Retry on PubSub availability issues
        attempts=5,
        wait_initial=4.0,
        wait_max=60,
        wait_jitter=5.0,  # Recommended retry settings for PubSub
    )
    async def publish(
        self, messages: List[Message], topic: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Publish messages to a GCP PubSub topic.
        :param messages: List of messages to publish.
        :param topic: PubSub Topic name.
        :param kwargs: Additional settings for the publish function.
        kwargs:
            project: Custom GCP project ID.
            session: Custom aiohttp session.
            timeout: Custom request timeout settings.
        :return: GCP response as a dict.
        """
        # Build gcp topic full name
        gcp_project = kwargs.get("project") or self.project
        topic = self.pubsub_client.topic_path(project=gcp_project, topic=topic)
        pubsub_messages = [
            pubsub.PubsubMessage(
                data=message.model_dump_json(exclude="attributes").encode("utf-8"),
                ordering_key=message.attributes.pop("ordering_key", "")
                if message.attributes
                else "",
                attributes=message.attributes,
            )
            for message in messages
        ]
        return await self.pubsub_client.publish(
            topic=topic,
            messages=pubsub_messages,
            session=kwargs.get("session"),
            timeout=kwargs.get("timeout", 30),
        )

    async def __aenter__(self) -> "GCPPubSubPublisher":
        await self.pubsub_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.close()
        await self.pubsub_client.close()
