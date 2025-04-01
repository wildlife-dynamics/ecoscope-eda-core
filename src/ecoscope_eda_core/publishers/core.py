from abc import ABC, abstractmethod
from typing import List

from ..messages import Message


class PublisherBase(ABC):
    """
    Abstract class for message publishers.
    """

    @abstractmethod
    async def publish(self, messages: List[Message], topic: str, **kwargs):
        """
        Publish messages to a topic.
        :param messages: List of messages to publish.
        :param topic: Topic name.
        :param kwargs: Additional settings for the publisher.
        :return: Publisher response.
        """
        pass
