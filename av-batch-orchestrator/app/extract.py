"""
extract.py is the main file which will be invoked from ADF custom batch activity for extraction process.
"""
from os import path


import datetime
import argparse
import logging
import logging.config

from os import path

import logging
import logging.config
from core.extract.extractscheduler import ExtractScheduler
from core.batch.task import Task
from core.batch.job import Job
from core.config import getSettings
from core.models.measurement import Measurement
from utils.storageclient import StorageClient
from utils.confighelper import ConfigHelper


log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")


logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

settings = getSettings()
configHelper=ConfigHelper()
#setting it to applicationinsightconnection string so that it can be used other places

log = logging.getLogger(__name__)

def extract(cargs):
    task = Task()
    job = Job()
    configHelper = ConfigHelper()
    storageClient = StorageClient(
        storageAccountUrl=settings.RAW_ZONE_SA_URL,
        credentials=configHelper.getStorageAccountCredentials(settings.RAW_ZONE_KEY),
        containerName=settings.RAW_ZONE_CONTAINER,
    )
    log.info(f"Environment : {settings.RUN_ENVIRONMENT}")

    start_time = datetime.datetime.now().replace(microsecond=0)
    log.info(f"Extraction start time: {start_time}")

    measurementObj = Measurement(
        **{
            "measurementId": args.measurementId,
            "extractedDataStreamId": args.extractedDataStreamId,
            "rawDataStreamPath": args.rawDataStreamPath,
            "extractedDataStreamPath": args.extractedDataStreamPath,
        }
    )

    # Get the rosbag file list
    # Remove the container name from the rawdatastream path
    rosPath = measurementObj.rawDataStreamPath.replace(settings.RAW_ZONE_CONTAINER, "")
    files = storageClient.getFirstLevelListOfDirectoryNames(path=rosPath)
    measurementObj.files = files
    # Process measurement for extraction.
    extractionScheduler = ExtractScheduler(job=job, task=task, settings=settings)
    jobs = extractionScheduler.scheduleMeasurementExtraction(
        measurement=measurementObj, poolId=settings.AZ_BATCH_EXECUTION_POOL_ID
    )

    # Monitor Extraction jobs. Threshold is in minutes
    # Execution will wait for configured minutes to monitor task execution before terminating gracefully.
    job.monitorJobsToComplete(
        jobs=jobs, timeout=datetime.timedelta(minutes=settings.MEASUREMENT_PROCESSING_THRESHOLD)
    )

    # Extraction for measurement complete
    log.info(
        f"Measurement extraction completed for measurementIs: {measurementObj.measurementId}"
    )

    end_time = datetime.datetime.now().replace(microsecond=0)

    log.info(f"Extraction completion time: {end_time}")
    elapsed_time = end_time - start_time
    log.info(f"Elapsed time: {elapsed_time}")


if __name__ == '__main__':

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--measurementId", "-mId", help="Set the measurement Id")
        parser.add_argument(
            "--extractedDataStreamId", "-dId", help="Set the extracted datastream Id"
        )
        parser.add_argument("--rawDataStreamPath", "-rdp", help="Set the raw datastream path")
        parser.add_argument(
            "--extractedDataStreamPath", "-edp", help="Set the extracted datastream path"
        )
        parser.add_argument("--files", "-fs", help="Set the extracted datastream path")

        args = parser.parse_args()

        extract(args)

    except Exception as e:
        raise RuntimeError(f"Error: {e.__class__}")

