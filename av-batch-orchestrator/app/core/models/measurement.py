"""Measurement details passed from ADF to batch orchestrator.
"""
from typing import List, Optional
from uuid import UUID
from pydantic import Field
from pydantic import BaseModel


class Measurement(BaseModel):
    """Measurement object for the orchestrator json argument

    Args:
        object (string): A stringified json of arguments.
    """

    measurementId: UUID
    rawDataStreamPath: str
    files: Optional[List] = Field(min_items=1)
    extractedDataStreamPath: str
    extractedDataStreamId: UUID
