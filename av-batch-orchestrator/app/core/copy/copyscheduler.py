"""This class schedules copy measurement jobs and tasks.
"""
import time
from core.batch.job import Job
from core.batch.task import Task


class CopyScheduler:
    """This class schedules copy measurement jobs and tasks."""

    task: Task = Task()
    job: Job = Job()
    poolId: str

    def __init__(self, poolId: str) -> None:
        self.poolId = poolId

    def scheduleCopyJob(self, measurementId: str, tasks: list):
        """This method schedules a copy job for the given measurement.

        Args:
            measurementId (str): measurement Id
            tasks (list): List of Tasks

        Returns:
            _type_: Returns the scheduled JobId
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        jobId = f"Copy_{measurementId}_{timestamp}"

        # Create Copy Job
        self.job.createJob(jobId=jobId, poolId=self.poolId, useTaskDependency=True)

        # Add copy task to job
        self.job.addTasksToJob(jobId, tasks)
        return jobId
