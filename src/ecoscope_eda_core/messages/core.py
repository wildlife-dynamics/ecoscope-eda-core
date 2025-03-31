from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo


class Message(BaseModel):
    """Base class for messages in event-driven architecture."""
    SCHEMA_VERSION: str = "v1"

    message_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")),
        title="ISO Timestamp",
        description="The date and time when the message was created.",
        example="2025-01-01T12:01:02+00:00",
    )
    schema_version: str = Field(
        default=SCHEMA_VERSION,
        frozen=True,
        description="Message schema version",
    )
    payload: Optional[Any] = Field(
        default_factory=dict,
        example="{}",
        description="Message payload. This can be overwritten in specific commands or events",
    )

    @property
    def message_type(self) -> str:
        return self.__class__.__name__


class Command(Message):
    """Base class for commands in event-driven architecture."""
    pass


class Event(Message):
    """Base class for events in event-driven architecture."""
    pass