"""SyncroniseArgs details passed from ADF to batch orchestrator.
"""
from uuid import UUID
from pydantic import BaseModel


class SyncroniseArgs(BaseModel):
    """SyncroniseArgs object for the orchestrator json argument

    Args:
        object (string): A stringified json of arguments.
    """

    measurementId: UUID
    rawDataStreamPath: str
    extractedDataStreamPath: str
    rawDataStreamId: UUID
