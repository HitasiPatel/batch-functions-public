"""This class is for building extration tasks.
"""
from logging import Logger, getLogger

from core.config import Settings, getSettings
from core.batch.task import Task
from core.extract.extracttasks import getTaskDefinitions


class TaskBuilder:
    """This class is for building extration tasks."""

    settings: Settings
    log: Logger
    task: Task

    def __init__(self, settings: Settings, task: Task, log: Logger = getLogger(__name__)) -> None:
        self.settings = settings
        self.task = task
        self.log = log

    def createExtractionTasks(
        self, fileName: str, destinationPath: str, measurementId: str, datastreamId: str
    ) -> list:
        """This method creates required extraction tasks for individual bag file.

        Args:
            fileName (str): Full path of the file.
            destinationPath (str): Output path where the extracted data will be stored.
            measurementId (str): measurement Id
            datastreamId (str): datastream Id

        Returns:
            list: A list of tasks.
        """
        tasks = []
        # Read taskdefinitions to create a task list for the given file.
        for taskDef in getTaskDefinitions():
            self.log.info(f"Creating {taskDef['name']} for [{fileName}]")
            command = self.createCommand(
                commandTemplate=taskDef["command"],
                fileName=fileName,
                destinationPath=destinationPath,
                measurementId=measurementId,
                datastreamId=datastreamId,
            )
            requiredSlots = 1
            exitJobOnFailure = False
            taskDependencies = None
            if "taskSlotsRequired" in taskDef:
                requiredSlots = taskDef["taskSlotsRequired"]
            if "exitJobOnFailure" in taskDef:
                exitJobOnFailure = taskDef["exitJobOnFailure"]
            if "taskDependencies" in taskDef:
                taskDependencies = taskDef["taskDependencies"]
            tasks.append(
                self.task.createTask(
                    name=taskDef["name"],
                    command=command,
                    dependentTaskIds=taskDependencies,
                    image=taskDef["imageName"],
                    requiredSlots=requiredSlots,
                    exitJobOnFailure=exitJobOnFailure,
                )
            )
        return tasks

    def createCommand(
        self,
        commandTemplate: str,
        fileName: str,
        destinationPath: str,
        measurementId: str,
        datastreamId: str,
    ):
        """This method replaces the templated params with the actual params.

        Args:
            commandTemplate (str): template command with param placeholders
            fileName (str): Actual file name
            destinationPath (str): destination path
            measurementId (str): measurement Id
            datastreamId (str): datastream Id

        Returns:
            _type_: A command string with actual params
        """
        return (
            commandTemplate.replace("##MID##", str(measurementId))
            .replace("##DID##", str(datastreamId))
            .replace("##INPUTFILE##", fileName)
            .replace("##OUTPUTPATH##", f"{destinationPath}")
            .replace("##APIBASEURL##", getSettings().API_BASE_URL)
        )
