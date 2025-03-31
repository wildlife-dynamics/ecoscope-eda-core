from abc import ABC, abstractmethod
from ..messages import Message


class PublisherBase(ABC):
    """
    Abstract class for message publishers.
    """

    @abstractmethod
    async def publish(self, message: Message, topic_id: str,  **kwargs):
        pass

