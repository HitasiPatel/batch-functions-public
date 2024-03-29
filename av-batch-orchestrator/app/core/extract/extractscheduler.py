"""This class schedules extraction jobs.
"""
import time
from core.config import Settings
from core.models.measurement import Measurement
from core.batch.task import Task
from core.batch.job import Job
from core.extract.taskbuilder import TaskBuilder


class ExtractScheduler:
    """This class schedules extraction jobs."""

    job: Job
    task: Task
    taskBuilder: TaskBuilder
    settings: Settings

    def __init__(self, job: Job, task: Task, settings: Settings) -> None:
        self.job = job
        self.task = task
        self.settings = settings
        self.taskBuilder = TaskBuilder(settings=settings, task=task)

    def scheduleMeasurementExtraction(self, measurement: Measurement, poolId: str) -> list:
        """This method schedules jobs/tasks for measurement extraction.

        Args:
            measurement (Measurement): Measurement Object
            poolId (str): Pool Id which will run the extraction jobs

        Returns:
            list: List of jobs created for the given measurement.
        """
        jobs = []
        for index, file in enumerate(measurement.files):
            fileName = f"/raw/{file}"
            destPath = "/"+measurement.extractedDataStreamPath
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            jobId = f"Ext_{measurement.measurementId}_{timestamp}_{index}"

            # Create a job that will run the tasks for extracting a bag file.
            self.job.createJob(jobId=jobId, poolId=poolId, useTaskDependency=True)

            # Create extraction tasks for the job
            tasks = self.taskBuilder.createExtractionTasks(
                fileName=fileName,
                destinationPath=destPath,
                measurementId=measurement.measurementId,
                datastreamId=measurement.extractedDataStreamId,
            )

            # Add the tasks to the job.
            self.job.addTasksToJob(jobId=jobId, taskList=tasks)
            jobs.append(jobId)
        return jobs
