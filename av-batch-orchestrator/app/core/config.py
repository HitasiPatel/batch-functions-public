"""
Load environment configurations to Settings class.
"""
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings class for configurations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    RUN_ENVIRONMENT: str = None
    AZ_KEYVAULT_NAME: str = None
    AZ_BATCH_KEY_NAME: str = None
    AZ_BATCH_ACCOUNT_URL: str = None
    AZ_BATCH_ACCOUNT_NAME: str = None
    AZ_BATCH_EXECUTION_POOL_ID: str = None
    AZ_BATCH_ORCHESTRATOR_POOL_ID: str = None
    AZ_BATCH_KEY: str = None
    API_BASE_URL: str = None
    RAW_ZONE_CONTAINER: str = None
    EXTRACTED_ZONE_CONTAINER: str = None
    TASK_RETRY_COUNT: int
    MEASUREMENT_PROCESSING_THRESHOLD: int
    AZURE_LOG_LEVEL = "INFO"
    ENABLE_LOGS_ON_TRACES: bool = False
    APPLICATIONINSIGHTS_ROLENAME: str = "BATCH ORCHESTRATOR"
    AZURE_LOG_FORMAT: Optional[
        str
    ] = "%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d traceId=%(traceId)s spanId=%(spanId)s - %(message)s"

    # export duration in seconds
    AZURE_TRACE_EXPORT_DURATION = 2.0
    AZURE_LOG_EXPORT_DURATION = 1.0
    LANDING_ZONE_SA_URL: str = None
    RAW_ZONE_SA_URL: str = None
    ARCHIVE_ZONE_SA_URL: str = None
    EXTRACTED_ZONE_SA_URL: str = None
    LANDING_SAS_KEY: str = None
    RAW_SAS_KEY: str = None
    ARCHIVE_SAS_KEY: str = None
    EXTRACTED_ZONE_KEY: str = None
    RAW_ZONE_KEY: str = None
    VALIDATION_PROCESSOR_IMAGE: str = None
    CAMERA_PROCESSOR_IMAGE: str = None
    POINTCLOUD_PROCESSOR_IMAGE: str = None
    STRUCTURED_PROCESSOR_IMAGE: str = None
    STRING_PROCESSOR_IMAGE: str = None
    METADATA_PROCESSOR_IMAGE: str = None
    UTILITY_PROCESSOR_IMAGE: str = None

    class Config:
        """
        Environment file name
        """

        env_file = ".env"


@lru_cache()
def getSettings():
    """Get settings object.

    Returns:
        _type_: Returns Settings object
    """
    return Settings()
