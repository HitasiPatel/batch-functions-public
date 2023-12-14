"""
copybags.py is the main file which will be invoked from ADF custom batch activity for copying bag files from landing to raw.
"""
import datetime
import logging
import logging.config

import time
import argparse

from os import path

from core.batch.task import Task
from core.batch.job import Job
from core.copy.taskbuilder import TaskBuilder
from core.copy.copyscheduler import CopyScheduler
from core.config import getSettings
from utils.confighelper import ConfigHelper

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

settings = getSettings()
configHelper = ConfigHelper()

log = logging.getLogger(__name__)


def process_copy_bags(cargs):

    configHelper = ConfigHelper()
    task = Task()
    job = Job()
    log.info(f"Environment : {settings.RUN_ENVIRONMENT}")
    start_time = datetime.datetime.now().replace(microsecond=0)
    log.info(f"Copy start time: {start_time} for measurementId: {cargs.measurementId}")
    rawSasKey = configHelper.getConfigKeyValue(settings.RAW_SAS_KEY)
    landingSasKey = configHelper.getConfigKeyValue(settings.LANDING_SAS_KEY)
    archiveSasKey = configHelper.getConfigKeyValue(settings.ARCHIVE_SAS_KEY)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    # Create a task for copy from landing to raw
    taskBuilder = TaskBuilder(
        source=cargs.landingPath,
        target=cargs.rawDataStreamPath,
        sourceSasKey=landingSasKey,
        targetSasKey=rawSasKey,
    )
    command = taskBuilder.getRawCopyCommand()
    rawCopyTask = f"{cargs.measurementId}_{timestamp}_1"
    copyBagsToRawTask = task.createTask(
        name=rawCopyTask, command=command, dependentTaskIds=None, exitJobOnFailure=True
    )
    # Create a task for copy from landing to archive
    taskBuilder = TaskBuilder(
        source=cargs.landingPath,
        target=cargs.archivePath,
        sourceSasKey=landingSasKey,
        targetSasKey=archiveSasKey,
    )
    command = taskBuilder.getArchiveCopyCommand()
    archiveCopyTask = f"{cargs.measurementId}_{timestamp}_2"
    copyToArchiveTask = task.createTask(
        name=archiveCopyTask, command=command, dependentTaskIds=None, exitJobOnFailure=True
    )
    # Create a task for removing measurement data from landing
    taskBuilder = TaskBuilder(
        source=cargs.landingPath, target=None, sourceSasKey=landingSasKey, targetSasKey=None
    )
    command = taskBuilder.getRemoveLandingDataCommand()
    removeLandingDataTask = f"{cargs.measurementId}_{timestamp}_3"
    removeFromLandingTask = task.createTask(
        name=removeLandingDataTask,
        command=command,
        dependentTaskIds=[rawCopyTask, archiveCopyTask],
        exitJobOnFailure=True,
    )
    # Copy measurement from landing to Raw.
    copyScheduler = CopyScheduler(poolId=settings.AZ_BATCH_ORCHESTRATOR_POOL_ID)
    copyJob = copyScheduler.scheduleCopyJob(
        cargs.measurementId, [copyBagsToRawTask, copyToArchiveTask, removeFromLandingTask]
    )
    # Monitor copy jobs. Threshold is in minutes
    # Execution will wait for configured minutes to monitor task execution before terminating gracefully.
    job.monitorJobsToComplete(
        [copyJob], datetime.timedelta(minutes=settings.MEASUREMENT_PROCESSING_THRESHOLD)
    )
    # Get failed tasks for a job
    failedTasks = job.getFailedTasks(jobId=copyJob)
    if len(failedTasks) > 0:
        raise RuntimeError(f"One or more tasks failed for this job. {failedTasks}")
    # Copy job completed
    log.info(f"Measurement copy completed for measurementId: {cargs.measurementId}")
    end_time = datetime.datetime.now().replace(microsecond=0)
    log.info(f"Copy completion time: {end_time}")
    elapsed_time = end_time - start_time
    log.info(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--measurementId", "-mId", help="Set the measurement Id")
        parser.add_argument("--rawDataStreamId", "-rId", help="Set the raw datastream Id")
        parser.add_argument("--rawDataStreamPath", "-rdp", help="Set the raw datastream path")
        parser.add_argument("--landingPath", "-lp", help="Set the landing path")
        parser.add_argument("--archivePath", "-arp", help="Set the archive path")
        args = parser.parse_args()

        process_copy_bags(args)

    except Exception as e:
        raise RuntimeError(f"Error: {e.__class__}")
