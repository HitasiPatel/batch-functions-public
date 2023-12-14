"""Task configuration for creating container workloads.
"""
from core.config import Settings, getSettings


def getTaskDefinitions(settings: Settings = getSettings()) -> list:
    """Creates a map of extraction tasks required for a measurement.

    Returns:
        list: A list of task definitions.
    """
    return [
        {
            "name": "ExtractCameraDataTask",
            "imageName": f"{settings.CAMERA_PROCESSOR_IMAGE}",
            ##The message type supported by this processor is sensor_msgs/msg/Image and the same is passed for msgtype param
            "command": "python3 /code/app.py --measurementId ##MID## --dataStreamId ##DID## --inputpath ##INPUTFILE## --outputpath ##OUTPUTPATH## --msgtype sensor_msgs/msg/Image --apibaseurl ##APIBASEURL##",
            "taskSlotsRequired": 2,
        }
    ]
