from .core import PublisherBase


#ToDo: Implement this class
class GCPPubSubPublisher(PublisherBase):

    def __init__(self, **kwargs):
        pass

    # Support using this client as an async context manager.
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def publish(self, message, topic_id, **kwargs):
        pass

    async def close(self):
        pass